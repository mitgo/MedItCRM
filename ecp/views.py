import functools
# import traceback

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from ecp.onecdb import persons_from_1c
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from ecp.mailclient import update_certs_from_mail

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


import ecp.utils as utils

# TODO списки сотрудников по датам визитов (не явились 1й раз, не явились 2й раз)

active_menu = {
    'parent': 'ОИиВТ',
    'segment': 'ЭЦП',
}


# Default decorator for all views
def base_view(func):
    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return func(request, *args, **kwargs)
        except Exception as e:
            # TODO надо что-то делать с экзепшинами (возможно логировать)
            messages.error(request, e, 'text-danger')
            return redirect('index')
    return inner


# Dashboard page of ECP APP
@permission_required("ecp.view_esigns")
@base_view
def index(request):
    one_c_pers = None
    search_str_fio = None
    if request.method == 'POST':
        search_str_fio = request.POST['search_str_fio']
        fio_dict = utils.get_fio_from_str(search_str_fio)
        new_esigns = utils.get_new_esigns(fio_dict),
        search_str_fio_mod = search_str_fio.replace(' ', '%') + '%'
        one_c_pers = persons_from_1c(search_str_fio_mod)
    else:
        new_esigns = utils.get_new_esigns()
    badges = {
        'count_persons': utils.count_persons(),
        'count_decrees': utils.count_decrees(),
        'count_departments': utils.count_departments,
    }
    widgets = utils.get_widgets()
    context = {
        'badges': badges,
        'widgets': widgets,
        'search_str_fio': search_str_fio,
        'one_c_pers': one_c_pers,
        'table_of_esigns': new_esigns,
        'table_of_rejected_requests': utils.get_processed_requests(1),
        'table_of_prompted_requests': utils.get_processed_requests(2),
        'finded_persons': utils.search_person(search_str_fio),
        'ogrn': utils.get_setting_value('OGRN'),
        'rejected': utils.count_rejected_persons(),
        'prompted': utils.count_prompted_persons(),
    }
    context |= active_menu
    return render(request, 'index.html', context)


@permission_required("ecp.view_esigns")
@base_view
def detailed_list(request, kind, deptype=None):
    context = {}
    if kind == 'ended_esigns':
        context['table_of_esigns'] = utils.get_ended_esigns()
        context['title'] = 'ЭЦП с истекающим сроком:'
    if kind == 'valid_esigns':
        context['table_of_esigns'] = utils.get_persons_who_has_valid_esign(deptype)
        context['title'] = 'Сотрудники с действующими ЭЦП:'
    if kind == 'no_key_esigns':
        context['table_of_esigns'] = utils.get_no_key_esigns()
        context['title'] = 'ЭЦП без указания серийного номера сертификата:'
    if kind == 'no_file_esigns':
        context['table_of_esigns'] = utils.get_no_file_esigns()
        context['title'] = 'ЭЦП без прикрепленного сертификата:'
    if kind == 'double_persons':
        context['table_of_esigns'] = utils.get_double_persons()
        context['title'] = 'Дубли сотрудников:'
    if kind == 'persons_without_decree':
        context['table_of_esigns'] = utils.get_persons_without_decree()
        context['title'] = 'Сотрудники без приказа:'
    if kind == 'not_installed_esigns':
        context['table_of_esigns'] = utils.get_not_installed_esigns()
        context['title'] = 'Не установленные в МИС ЭЦП:'
    if kind == 'overdue_requests':
        context['table_of_esigns'] = utils.get_overdue_requests(0)
        context['title'] = 'Просроченные заявления:'
    context |= active_menu
    return render(request, 'detailedlist.html', context)


@permission_required("ecp.view_esigns")
@base_view
def person_esigns(request, pk):
    context = active_menu | utils.get_person_esigns(pk)
    return render(request, "person.html", context)


@permission_required("ecp.change_persons")
@base_view
def person_detail(request, pk=None, sotr_id=None):
    person = None
    person_form = None
    if sotr_id and request.method != 'POST':
        try:
            person_form = utils.fill_person_form_from_1c(sotr_id)
        except IndexError:
            messages.error(request, "Сотрудник которого пытались импортировать из \
                                    1С не привязан ни к одному из отделений, вопрос к кадрам!")
            return redirect('ecp:index')
    if pk:
        [person, person_form] = utils.fill_person_form_from_app(pk)
    else:
        if not sotr_id:
            [person, person_form] = utils.fill_person_form_from_app()
    if request.method == 'POST':
        result_save_person = utils.save_person_form(request.POST, person)
        if type(result_save_person) == int:
            return redirect('ecp:person_esigns', pk=result_save_person)
        else:
            messages.error(request, result_save_person)
    context = {
        'form': person_form,
        'pk': pk,
    }
    context |= active_menu
    return render(request, 'persondetail.html', context)


@permission_required("ecp.delete_persons")
@base_view
def person_delete(request, pk):
    delete_result = utils.delete_person(pk)
    if delete_result is True:
        return redirect('ecp:index')
    else:
        messages.error(request, delete_result, 'text-danger')
        return redirect('ecp:person_detail', pk=pk)


@permission_required("ecp.view_departments")
@base_view
def departments(request):
    departments_detail = utils.get_departments()
    context = {
        'departments': departments_detail,
    }
    context |= active_menu
    return render(request, 'departments.html', context)


@permission_required("ecp.change_departments")
@base_view
def department_detail(request, pk):
    department = utils.get_departments(pk=pk)
    if request.method == 'POST':
        if request.user.has_perm("ecp.change_departments"):
            save_department_result = utils.save_department_form(request.POST, department)
            if save_department_result is not True:
                messages.error(request, save_department_result, 'text-danger')
            return redirect('ecp:departments')
        else:
            return django.http.HttpResponseForbidden()
    else:
        department_form = utils.fill_department_form(department)
    context = {
        'department_form': department_form,
        'pk': pk,
    }
    context |= active_menu
    return render(request, 'departments.html', context)


@permission_required("ecp.view_persons")
@base_view
def persons_in_department(request, pk):
    persons_in_dep = utils.get_persons_in_department(pk)
    department = utils.get_departments(pk=pk)
    context = {
        'persons_in_department': persons_in_dep,
        'Department': department,
    }
    context |= active_menu
    return render(request, 'departments.html', context)


@permission_required("ecp.change_esigns")
@base_view
def esign_detail(request, pk=None, fk=None):
    person = None
    esign_form = None
    orgn = utils.get_setting_value('OGRN')
    # Обращаемся к уже существующей подписи
    if pk:
        person = utils.get_person_for_esign(pk=pk)
        # Сохраняем уже существующую подпись
        if request.method == 'POST':
            save_esign_result = utils.save_esign_form(request, pk=pk)
            if type(save_esign_result) != int:
                messages.error(request, save_esign_result, 'text-danger')
                save_esign_result = pk
            return redirect('ecp:esign_detail', pk=save_esign_result)
        # Открываем на редактирование существующую подпись
        else:
            esign_form = utils.fill_esign_form(pk=pk)
    # Создаем подпись для сотрудника
    if fk:
        person = utils.get_person_for_esign(fk=fk)
        # Заполняем форму новой подписи
        if request.method != 'POST':
            esign_form = utils.fill_esign_form()
        # Сохраняем новую подпись для сотрудника
        else:
            save_esign_result = utils.save_esign_form(request, fk=fk)
            if type(save_esign_result) != int:
                messages.error(request, save_esign_result, 'text-danger')
                return redirect('ecp:person_esigns', pk=fk)
            return redirect('ecp:esign_detail', pk=save_esign_result)
    context = {
        'form': esign_form,
        'pk': pk,
        'person': person,
        'ogrn': orgn,
    }
    context |= active_menu
    return render(request, "ecpdetail.html", context)


@permission_required("ecp.delete_esigns")
@base_view
def esign_delete(request, pk):
    result_delete_esign = utils.delete_esign(pk)
    if type(result_delete_esign) != int:
        messages.error(request, result_delete_esign, 'text-danger')
    return redirect('ecp:person_esigns', pk=result_delete_esign)


@permission_required("ecp.delete_decrees")
@base_view
def decrees(request):
    decreeslist = utils.get_all_decreees()
    context = {
        'decrees': decreeslist
    }
    context |= active_menu
    return render(request, 'decrees.html', context)


@permission_required("ecp.change_decrees")
@base_view
def decree_detail(request, pk=None):
    persons = utils.get_persons_by_decree(pk)
    decree_form = utils.get_decree_form(pk)
    if request.method == 'POST':
        save_decree_result = utils.save_decree_form(request, pk)
        if save_decree_result is not True:
            messages.error(request, save_decree_result, 'text-danger')
        return redirect('ecp:decrees')
    context = {
        'form': decree_form,
        'persons': persons,
        'pk': pk
    }
    context = active_menu | context
    return render(request, 'decreedetail.html', context)


@permission_required("ecp.change_decrees")
@base_view
def decree_upload_persons(request, pk):
    err_pers = None
    upload_result = utils.upload_persons_from_csv(request, pk)
    if type(upload_result) == list:
        err_pers = upload_result
    else:
        messages.error(request, upload_result, 'text-danger')
    form = utils.get_decree_form(pk)
    persons = utils.get_persons_by_decree(pk)
    context = {
        'form': form,
        'err_pers': err_pers,
        'persons': persons,
        'pk': pk,
    }
    context |= active_menu
    return render(request, 'decreedetail.html', context)


@permission_required("ecp.view_esigns")
@base_view
def download_file(request, file_type=None, entity_id=None):
    entity = utils.download_file(file_type, entity_id)
    response = HttpResponse(entity, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{entity.name.split("/")[-1]}"'
    return response


@permission_required("ecp.view_esigns")
@base_view
def reports(request):
    esigns_report = utils.get_esigns_report()
    context = {
        'esigns_report': esigns_report,
    }
    context = active_menu | context
    return render(request, 'reports.html', context)
