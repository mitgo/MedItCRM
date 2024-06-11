from django.db.models.aggregates import Max
from django.db.models.functions import Concat, Upper
from django.db.models import F, Q, Value, ProtectedError, Count
import datetime
from .models import Esigns, EsignStatus, Persons, Decrees, Departments, Settings
from .forms import PersonForm, EsignForm, DecreeForm, DepartmentForm
from ecp.misdb import get_not_installed_keys
from ecp.onecdb import import_person_from_1c
from django.shortcuts import get_object_or_404


# Transform FIO string to list
def get_fio_from_str(fio_str):
    fio_list = fio_str.split()
    fio_params_list = ['fam', 'im', 'ot']
    fio_dict = {}
    while len(fio_list) > 0:
        fio_dict[fio_params_list.pop(0)] = fio_list.pop(0)
    while len(fio_params_list) > 0:
        fio_dict[fio_params_list.pop(0)] = ''
    return fio_dict


# ----------------------------------CODE FOR DASHBOARD----------------------------
# Get count of new ecps for widget
def get_count_new_esigns():
    new_esigns = get_new_esigns()['list']
    return new_esigns.count()


# Get count ended esigns
def get_count_ended_esigns():
    ended_esigns = get_ended_esigns()['list']
    return ended_esigns.count()


# Get count persons who has valid esign
def get_count_who_has_valid_esign():
    valid_esigns = get_persons_who_has_valid_esign()['list']
    return valid_esigns.count()


# Count of persons who haven't decree
def count_persons_without_decree():
    persons_without_decree = get_persons_without_decree()['list']
    return persons_without_decree.count()


# Get count of not installed esigns on MIS
def count_not_installed_esigns():
    not_installed_esigns = get_not_installed_esigns()['list']
    if not_installed_esigns:
        return not_installed_esigns.count()
    else:
        return 0


# Count esigns without KEY for widget
def count_no_key_esigns():
    no_key_esigns = get_no_key_esigns()['list']
    return no_key_esigns.count()


# Get coung esigns without FILE for widget
def count_no_file_esigns():
    no_file_esigns = get_no_file_esigns()['list']
    return no_file_esigns.count()


# Get count doubled persons for widget
def count_double_persons():
    double_persons = get_double_persons()['list']
    return double_persons.count()


def count_rejected_persons():
    rejected_persons = get_processed_requests(1)['list']
    return rejected_persons.count()


def count_prompted_persons():
    prompted_persons = get_processed_requests(2)['list']
    return prompted_persons.count()


def count_overdue_requests(type: int):
    overdue_requests = get_overdue_requests(type)['list']
    return overdue_requests.count()


# Get count of active persons for badge
def count_persons():
    return Persons.objects.filter(is_active=True).count()


# Get count of decrees for badge
def count_decrees():
    return Decrees.objects.count()


# Get count of departments for badge
def count_departments():
    return Departments.objects.count()


def get_widgets():
    widgets = [
        {
            'cnt': get_count_ended_esigns(),
            'bg': 'danger',
            'header': 'Истекает срок ЭЦП',
            'icon': 'warning-alt',
            'kind_href': 'ended_esigns',
        },
        {
            'cnt': get_count_who_has_valid_esign(),
            'bg': 'green',
            'header': 'Сотрудники с валидными ЭЦП',
            'icon': 'warning-alt',
            'kind_href': 'valid_esigns',
        },
        {
            'cnt': count_overdue_requests(0),
            'bg': 'fuchsia',
            'header': 'Истек срок заявления',
            'icon': 'crown-king',
            'kind_href': 'overdue_requests',
        },
        {
            'cnt': count_no_key_esigns(),
            'bg': 'danger',
            'header': 'ЭЦП без серийника сертификата',
            'icon': 'certificate',
            'kind_href': 'no_key_esigns',
        },
        {
            'cnt': count_no_file_esigns(),
            'bg': 'danger',
            'header': 'ЭЦП без прикрепленного файла',
            'icon': 'folder-remove',
            'kind_href': 'no_file_esigns',
        },
        {
            'cnt': count_double_persons(),
            'bg': 'danger',
            'header': 'Дубли сотрудников',
            'icon': 'users-social',
            'kind_href': 'double_persons',
        },
        {
            'cnt': count_persons_without_decree(),
            'bg': 'gray',
            'header': 'Сотрудники без приказа',
            'icon': 'attachment',
            'kind_href': 'persons_without_decree',
        },
        {
            'cnt': count_not_installed_esigns(),
            'bg': 'warning',
            'header': 'Не установлено в МИС',
            'icon': 'disability-race',
            'kind_href': 'not_installed_esigns',
        },
        {
            'cnt': count_overdue_requests(1),
            'bg': 'fuchsia',
            'header': 'Истекает срок заявления',
            'icon': 'crown-king',
        },
        {
            'cnt': get_count_new_esigns() + count_rejected_persons() + count_prompted_persons(),
            'bg': 'teal',
            'header': 'Эцп в стадии изготовления',
            'icon': 'industries-3',
            'kind_href': 'overdue_requests',
            'footer': True,
            'new': get_count_new_esigns(),
        },
    ]
    return widgets
# ----------------------------------END CODE FOR DASHBOARD----------------------------


# ----------------------------------CODE ESIGNS LISTS--------------------------------
# Get ECPs in progress, if search str - then All, include not Active
def get_new_esigns(fio_dict=None):
    overdue_persons = list(get_overdue_requests(0)['list'].values_list('full_name', flat=True))
    new_esigns = Esigns.objects.filter(date_valid__isnull=True, person__is_active=True)
    new_esigns = new_esigns.values('person_id', 'person__dep__name', 'date_start', 'pk')\
        .annotate(full_name=Concat('person__fam', Value(' '), 'person__im', Value(' '), 'person__ot'))\
        .exclude(esignstatus__status_code__isnull=False)\
        .exclude(full_name__in=overdue_persons)\
        .order_by('date_start', 'full_name', 'person__dep__name')
    if fio_dict:
        new_esigns = new_esigns.filter(person__fam__regex=fio_dict['fam'], person__im__regex=fio_dict['im'],
                                       person__ot__regex=fio_dict['ot'])
    header = {
        'full_name': 'ФИО',
        'person__dep__name': 'Подразделение',
        'date_start': 'Дата начала оформления'
    }
    esigns_list = {
        'header': header,
        'list': new_esigns,
    }
    return esigns_list


def get_persons_who_has_valid_esign(deptype=None):
    header = {
        'full_name': 'ФИО',
        'person__snils': 'СНИЛС',
        'max_date': 'Дата окончания'
    }

    if deptype is None:
        ecp_ended_notify_period = int(get_setting_value('ecp_ended_notify_period'))
        # Отклоненные
        include_persons = list(get_processed_requests(1)['list'].values_list('full_name', flat=True))
        # Приглашение на визит
        include_persons += list(get_processed_requests(2)['list'].values_list('full_name', flat=True))

        valid_esigns = Persons.objects \
            .annotate(max_date=Max('esigns__date_valid'),
                      full_name=Concat('fam', Value(' '), 'im', Value(' '), 'ot'),
                      person__id=F('pk'), person__snils=F('snils')) \
            .values('max_date', 'full_name', 'person__id', 'person__snils') \
            .filter(
                    Q(max_date__gte=(datetime.date.today() + datetime.timedelta(days=ecp_ended_notify_period))) |
                    Q(full_name__in=include_persons),
                    is_active=True) \
            .order_by('max_date', 'full_name')
    else:
        valid_esigns = Esigns.objects \
                .annotate(full_name=Concat('person__fam', Value(' '), 'person__im', Value(' '), 'person__ot'),
                          max_date=F('date_valid')) \
                .values('max_date', 'full_name', 'person__id', 'person__post') \
                .filter(date_valid__gte=datetime.date.today(), person__dep__type_id=deptype)
    esigns_list = {
        'header': header,
        'list': valid_esigns,
    }
    return esigns_list

# Get ended ECPs, if search str - then All, include not Active
def get_ended_esigns():
    header = {
        'full_name': 'ФИО',
        'person__dep__name': 'Подразделение',
        'max_date': 'Дата действия'
    }
    ecp_ended_notify_period = int(get_setting_value('ecp_ended_notify_period'))
    exclude_persons = list(get_new_esigns()['list'].values_list('full_name', flat=True))
    exclude_persons += list(get_processed_requests(1)['list'].values_list('full_name', flat=True))
    exclude_persons += list(get_processed_requests(2)['list'].values_list('full_name', flat=True))
    exclude_persons += list(get_overdue_requests(0)['list'].values_list('full_name', flat=True))
    ended_esigns = Persons.objects\
        .annotate(max_date=Max('esigns__date_valid'),
                  full_name=Concat('fam', Value(' '), 'im', Value(' '), 'ot'),
                  person__id=F('pk'), person__dep__name=F('dep__name'))\
        .values('max_date', 'full_name', 'person__id', 'person__dep__name', 'pk')\
        .filter(
            Q(max_date__lte=(datetime.date.today() + datetime.timedelta(days=ecp_ended_notify_period)))
            | Q(max_date=None), is_active=True) \
        .exclude(full_name__in=exclude_persons) \
        .order_by('max_date', 'full_name', 'person__dep__name')

    esigns_list = {
        'header': header,
        'list': ended_esigns,
    }
    return esigns_list


def get_processed_requests(type_responce: int):
    header = {
        'full_name': 'ФИО',
        'max_date': 'Дата отклонения приглашения на визит',
    }
    overdue_persons = list(get_overdue_requests(0)['list'].values_list('full_name', flat=True))
    requests = EsignStatus.objects.\
        annotate(full_name=Concat('esign__person__fam', Value(' '), 'esign__person__im', Value(' '),
                                  'esign__person__ot'),
                 max_date=Max('date'), person_id=F('esign__person_id'), pk=F('esign_id')).\
        filter(status_code=type_responce, esign__person__is_active=True, esign__date_get=None, esign__date_valid__day=None).\
        values('full_name', 'max_date', 'person_id', 'pk', 'status_txt', 'link', 'reason', 'esign__request_num').\
        exclude(full_name__in=overdue_persons)
    if type_responce == 1:
        header['reason'] = 'Причина'
        header['max_date'] = 'Дата отклонения'
        header['status_txt'] = 'Статус'
    else:
        header['max_date'] = 'Дата приглашения на визит'
        rejected_persons = list(get_processed_requests(1)['list'].values_list('full_name', flat=True))
        requests = requests.exclude(full_name__in=rejected_persons)
        requests.values('full_name', 'max_date', 'person_id', 'pk')
    esigns_list = {
        'header': header,
        'list': requests,
    }
    return esigns_list


# Просроченные заявления
def get_overdue_requests(type: int):
    header = {
        'full_name': 'ФИО',
        'max_date': 'Дата подачи заявления',
        'person__dep__name': 'Отделение',
    }
    date_delta = int(get_setting_value('request_alive_days'))
    requests = Esigns.objects. \
        annotate(full_name=Concat('person__fam', Value(' '), 'person__im', Value(' '), 'person__ot'),
                 max_date=Max('date_start')). \
        values('full_name', 'person__dep__name', 'max_date', 'person__id', 'pk'). \
        order_by('person__dep__name', 'max_date').\
        filter(date_get__isnull=True, date_valid__isnull=True, person__is_active=True)
    if type == 1:
        date_delta -= int(get_setting_value('request_alive_notify'))
        requests = requests.filter(Q(max_date__lte=(datetime.date.today() - datetime.timedelta(days=date_delta))),
                    ~Q(max_date__lte=(datetime.date.today() - datetime.timedelta(days=date_delta))))
    else:
        requests = requests.filter(Q(max_date__lte=(datetime.date.today() - datetime.timedelta(days=date_delta))))

    esigns_lists = {
        'header': header,
        'list': requests,
    }
    return esigns_lists


# Get persons who haven't decree
def get_persons_without_decree():
    pers_no_decree = Persons.objects \
        .annotate(full_name=Concat('fam', Value(' '), 'im', Value(' '), 'ot'),
                  person__id=F('pk')) \
        .values('person__id', 'full_name') \
        .filter(decrees__isnull=True, is_active=True).order_by('full_name')
    header = {
        'full_name': 'ФИО',
    }
    esigns_list = {
        'header': header,
        'list': pers_no_decree,
    }
    return esigns_list


# Get not installed to MIS esigns
def get_not_installed_esigns():
    not_installed_esigns = None
    active_esigns = Esigns.objects \
        .annotate(full_name=Concat('person__fam', Value(' '), 'person__im', Value(' '), 'person__ot')) \
        .filter(Q(date_valid__gte=datetime.date.today()), key__isnull=False)
    if active_esigns:
        act_keys = "('" + "','".join(active_esigns.values_list('key', flat=True)) + "')"
        act_keys = act_keys.replace(' ', '').upper()
        act_fios = "('" + "','".join(active_esigns.values_list('full_name', flat=True)) + "')"
        act_fios = act_fios.upper()
        not_installed_keys = get_not_installed_keys(act_keys, act_fios)
        if not_installed_keys:
            not_installed_esigns = Esigns.objects.\
                values('person__id', 'date_valid', 'pk', 'key', 'date_start') \
                .annotate(full_name=Concat('person__fam', Value(' '), 'person__im', Value(' '), 'person__ot')) \
                .filter(full_name__in=not_installed_keys).filter(Q(date_valid__gte=datetime.date.today()))\
                .order_by('date_start')
    header = {
        'full_name': 'ФИО',
        'date_valid': 'Дата окончания действия',
        'date_start': 'Дата подачи запроса',
        'key': 'Серийный номер',
    }
    esigns_list = {
        'header': header,
        'list': not_installed_esigns,
    }
    return esigns_list


# All esigns without KEY
def get_no_key_esigns():
    no_key_esigns = Esigns.objects \
        .filter(date_valid__isnull=False, date_start__isnull=False, key__isnull=True) \
        .values('person__id', 'date_start', 'pk') \
        .annotate(full_name=Concat('person__fam', Value(' '), 'person__im', Value(' '), 'person__ot'))
    header = {
        'full_name': 'ФИО',
        'date_start': 'Дата подачи заявления',
    }
    esigns_list = {
        'header': header,
        'list': no_key_esigns,
    }
    return esigns_list


# Get esigns without FILE
def get_no_file_esigns():
    no_file_esigns = Persons.objects \
        .filter(esigns__date_valid__isnull=False, esigns__date_start__isnull=False, esigns__cert__exact='') \
        .values('esigns__date_start', 'esigns__id') \
        .annotate(full_name=Concat('fam', Value(' '), 'im', Value(' '), 'ot'), date_start=F('esigns__date_start'),
                  person__id=F('pk'), pk=F('esigns__id'))
    header = {
        'full_name': 'ФИО',
        'date_start': 'Дата подачи заявления',
    }
    esigns_list = {
        'header': header,
        'list': no_file_esigns,
    }
    return esigns_list


# Get list of doubled persons
def get_double_persons():
    double_persons = Persons.objects \
        .annotate(full_name=Concat(Upper('fam'), Value(' '), Upper('im'), Value(' '), Upper('ot'))) \
        .values('full_name') \
        .annotate(cnt=Count('*')) \
        .filter(cnt__gt=1) \
        .values('full_name', 'db', 'cnt')
    header = {
        'full_name': 'ФИО',
        'db': 'Дата рождения',
        'cnt': 'Количество дублей'
    }
    esigns_list = {
        'header': header,
        'list': double_persons,
    }
    return esigns_list
# ----------------------------------END CODE ESIGNS LISTS-----------------------------

# -----------------------------------CODE FOR ESIGNS STATUSES-------------------------


def create_esign_status(status):
    try:
        EsignStatus.objects.get_or_create(**status)
        return True
    except Exception as error:
        # todo предусмотреть логирование
        return False

# ---------------------------------END CODE FOR ESIGNS STATUSES------------------------


# ----------------------------------CODE FOR PERSONS------------------------------
# Search Person
def search_person(fio=None):
    persons = None
    if fio:
        fio_dict = get_fio_from_str(fio)
        persons = Persons.objects.filter(fam__iregex=fio_dict['fam'], im__iregex=fio_dict['im'],
                                         ot__iregex=fio_dict['ot'])\
            .annotate(full_name=Concat('fam', Value(' '), 'im', Value(' '), 'ot'))\
            .values('full_name', 'pk', 'dep__name', 'is_active').order_by('dep__name', 'full_name')
    header = {
        'is_active': 'Активен?',
        'full_name': 'ФИО',
        'dep__name': 'Подразделение',
    }
    esigns_list = {
        'header': header,
        'list': persons,
    }
    return esigns_list


# Fill all person form fields with data from 1C
def fill_person_form_from_1c(sotr_id):
    person = import_person_from_1c(sotr_id)
    department = Departments.objects.get_or_create(name=person[0].dep)
    data = {
        'fam': person[0].fam,
        'im': person[0].im,
        'ot': person[0].ot,
        'db': person[0].db,
        'bitrh_place': person[0].bitrh_place.replace('0,', '')
        .replace(',,', ',').replace(',', ', ').replace(' , ', ' ').strip(),
        'post': person[0].post,
        'phone': person[0].phone.replace(' ', '').replace('-', '')[-10:],
        'dep': department[0],
        'snils': person[0].snils.replace(' ', '').replace('-', ''),
        'inn': person[0].inn,
        'pasp_s': person[0].pasp_s,
        'pasp_n': person[0].pasp_n,
        'pasp_dep': person[0].pasp_dep,
        'pasp_date': person[0].pasp_date,
        'pasp_kem': person[0].pasp_kem,
        'is_active': True
    }
    return PersonForm(data)


# Fill peron form fields from app
def fill_person_form_from_app(pk=None):
    if pk:
        person = get_object_or_404(Persons, pk=pk)
        person_form = PersonForm(instance=person)
    else:
        person = None
        person_form = PersonForm()
    return [person, person_form]


# Save person info
def save_person_form(post, person):
    person_form = PersonForm(post, instance=person)
    if person_form.is_valid():
        try:
            person = person_form.save()
            return person.pk
        except Exception as error:
            return 'Ошибки при сохранении сотрудника: ' + str(error)
    else:
        return "Ошибки валидации на форме: " + repr(person_form.errors)


def delete_person(pk):
    try:
        person = Persons.objects.get(id=pk)
        person.delete()
        return True
    except ProtectedError as error:
        return 'У пользователя есть зарегистрированные ЭЦП, сначала удалите ЭЦП: ' + str(error)


def get_person_esigns(pk):
    person = get_object_or_404(Persons, pk=pk)
    esigns = {
        'person': person,
        'n_esigns': Esigns.objects.filter(person=person.id, date_valid__isnull=True),
        'g_esigns': Esigns.objects.filter(person=person.id, date_valid__gt=datetime.date.today()),
        'b_esigns': Esigns.objects.filter(person=person.id, date_valid__lte=datetime.date.today())
                                  .order_by('-date_valid')[:5],
    }
    return esigns
# ------------------------------END CODE FOR PERSONS---------------------------------


# ------------------------------CODE FOR DEPARTMENTS---------------------------------
# Get all departments
def get_departments(pk=None):
    if pk:
        departments = get_object_or_404(Departments, pk=pk)
    else:
        departments = Departments.objects.all().order_by('type')
    return departments


def save_department_form(post, instance):
    department_form = DepartmentForm(post, instance=instance)
    if department_form.is_valid():
        try:
            department_form.save()
            return True
        except Exception as error:
            return 'Не удалось сохранить отделение' + str(error)
    else:
        return "Ошибки валидации на форме: " + repr(department_form.errors)


def fill_department_form(instance):
    department_form = DepartmentForm(instance=instance)
    return department_form


def get_persons_in_department(dep_pk):
    persons_in_department = Persons.objects.filter(dep=dep_pk)
    return persons_in_department
# -----------------------------------------END CODE FOR DEPARTMENTS---------------------


# -----------------------------------------CODE FOR ESIGNS -----------------------------
def get_esign(pk):
    esign = get_object_or_404(Esigns, pk=pk)
    return esign


def fill_esign_form(pk=None):
    if pk:
        esign = get_esign(pk)
        esign_form = EsignForm(instance=esign)
    else:
        esign_form = EsignForm()
    return esign_form


def get_person_for_esign(pk=None, fk=None):
    person = None
    if fk:
        person = Persons.objects. \
            values('pk', 'pasp_n', 'pasp_s', 'pasp_date', 'pasp_dep', 'pasp_kem', 'db', 'bitrh_place', 'fam',
                   'im', 'ot', 'inn', 'snils', 'dep__name', 'post', 'phone', 'decrees__number', 'decrees__pk',
                   'decrees__d_date'). \
            annotate(max_date=Max('decrees__d_date')). \
            order_by('-max_date'). \
            filter(pk=fk).first()
    if pk:
        person = Persons.objects.values('pk', 'fam', 'im', 'ot').filter(esigns__pk=pk).first()
    return person


def save_esign_form(request, pk=None, fk=None):
    esign = None
    esign_form = None
    # Если сохраняем новую подпись, нужно привязать ее к сотруднику - извлекаем сотрудника
    if fk:
        esign_form = EsignForm(request.POST, request.FILES)
        # Собираем необходимые данные для оформления подписи на сайте уфк
    # Если сохраняем уже существующую то подставляем данные из переданного инстанса
    if pk:
        esign = get_esign(pk)
        # Если прилетел файл, то нужно из старого инстанса его удалить
        if request.FILES:
            esign.cert.delete()
            esign.cer.delete()
            EsignStatus.objects.filter(esign=esign).delete()
        esign_form = EsignForm(request.POST or None, request.FILES or None, instance=esign)
    try:
        if esign_form.is_valid():
            # Если сохраняем новую подпись - нужно подставить сотрудника
            if fk:
                person_for_form = get_object_or_404(Persons, pk=fk)
                esign = esign_form.save(commit=False)
                esign.person = person_for_form
            esign.save()
            return esign.id
        # else:
        #     return "Ошибки валидации на форме: " + repr(esign_form.errors)
    except Exception as error:
        return "Не удалось сохранить ЭЦП: " + str(error)


def delete_esign(pk=None):
    try:
        esign = Esigns.objects.get(id=pk)
        esign.cert.delete()
        esign.cer.delete()
        esign.delete()
        return esign.person.pk
    except Exception as error:
        return "Ошибки при удалении ЭЦП: " + str(error)


def get_esign_by_req_num(req_num):
    try:
        esign = Esigns.objects.filter(request_num=req_num).first()
        return esign
    except Exception:
        return False


def get_esign_by_req_uuid(uuid):
    try:
        esign = Esigns.objects.filter(request_link__iregex=uuid).first()
        return esign
    except Exception:
        return False


def get_esign_by_fio(fio):
    fio = fio.split()
    try:
        esign = Esigns.objects.filter(person__fam__iregex=fio[0], person__im__iregex=fio[1], person__ot__iexact=fio[2],
                                      date_valid__isnull=True, date_get__isnull=True).first()
        return esign
    except Exception:
        return False


def update_esign_by_fio(fio, content):
    fio = fio.split()
    try:
        esign = Esigns.objects.filter(person__fam__iregex=fio[0], person__im__iregex=fio[1], person__ot__iexact=fio[2],
                                      date_valid__isnull=True, date_get__isnull=True).update(**content)
        if esign == 0:
            return False
        return True
    except Exception as error:
        print(repr(error))
        return False


# -----------------------------------------END CODE FOR ESIGNS -------------------------


# ---------------------------------------------CODE FOR DECREES ---------------------------------
def get_all_decreees():
    decrees = Decrees.objects.all()
    return decrees


# Get decree detail
def get_decree(pk):
    decree_detail = get_object_or_404(Decrees, pk=pk)
    return decree_detail


def get_decree_form(pk=None):
    if pk:
        decreee_detail = get_decree(pk)
        decree_form = DecreeForm(instance=decreee_detail)
    else:
        decree_form = DecreeForm()
    return decree_form


def save_decree_form(request, pk=None):
    if pk:
        decreedet = get_decree(pk)
        if request.FILES:
            decreedet.file.delete()
        decree_form = DecreeForm(request.POST, request.FILES, instance=decreedet)
    else:
        decree_form = DecreeForm(request.POST, request.FILES)
    if decree_form.is_valid():
        try:
            decree_form.save()
            return True
        except Exception as error:
            return 'При сохранении возникли ошибки: ' + str(error)
    else:
        return "Ошибки валидации на форме: " + repr(decree_form.errors)


# Get persons for decree_detail
def get_persons_by_decree(decree_pk):
    persons = Persons.objects.filter(decrees__pk=decree_pk)
    return persons


# upload persons from csv to decree
def upload_persons_from_csv(request, pk):
    err_pers = []
    try:
        persons_list_file = request.FILES['persons']
        if not persons_list_file.name.endswith('.csv'):
            return 'Файл должен быть формата CSV'
        else:
            if persons_list_file.multiple_chunks():
                return'Слишком большой файл'
            else:
                file_data = persons_list_file.read().decode("utf-8")
                lines = file_data.split("\r\n")
                decree = Decrees.objects.get(pk=pk)
                decree.persons.clear()
                for line in lines:
                    fields = line.split(" ")
                    try:
                        person = Persons.objects.get(fam=fields[0], im=fields[1], ot=fields[2])
                        if person:
                            decree.persons.add(person.id)
                    except (Persons.DoesNotExist, IndexError):
                        err_pers.append(line)
        return err_pers
    except Exception as error:
        return 'Невозможно загрузить/обработать файл: ' + repr(error)
# ---------------------------------------------END CODE FOR DECREEES-----------------------------


# -----------------------------------------------CODE FOR REPORT-------------------------------------
def get_esigns_report():
    esigns = Esigns.objects \
            .values('person__dep__type__name', 'person__dep__type_id') \
            .annotate(cnt=Count('pk')) \
            .filter(date_valid__gte=datetime.date.today())
    return esigns
# ------------------------------------------------END CODE FOR REPORT--------------------------------


# ----------------------------------------------CODE FOR DOWNLOAD FILE-------------------------------
def download_file(file_type, entity_id):
    entity = None
    if file_type == 'decree':
        entity = get_object_or_404(Decrees, pk=entity_id)
        entity = entity.file
    if file_type == 'cert':
        entity = get_object_or_404(Esigns, pk=entity_id)
        entity = entity.cert
    if file_type == 'cer':
        entity = get_object_or_404(Esigns, pk=entity_id)
        entity = entity.cer
    return entity
# -------------------------------------------END CODE FOR DOWNLOAD FILE -----------------------------

# ------------------------------------------OTHER----------------------------------------------------


def get_setting_value(setting_name):
    setting = Settings.objects.get(setting_name=setting_name).setting_value
    return setting


def get_all_settings_email_subject():
    subjects = Settings.objects.filter(setting_name__regex="subject_email_cert").\
        values('setting_name', 'setting_value').order_by('setting_name')
    return subjects
# ----------------------------------------END OTHER--------------------------------------------------
