from django import forms
from .models import Esigns, Persons, Departments, Decrees


class PersonForm(forms.ModelForm):
    class Meta:
        model = Persons
        fields = ('fam', 'im', 'ot', 'db', 'bitrh_place', 'phone', 'dep', 'post', 'snils', 'inn', 'pasp_s', 'pasp_n',
                  'pasp_dep', 'pasp_date', 'pasp_kem', 'decrees', 'is_active')
        widgets = {
            'fam': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                  'style': 'width: 300px;'}),
            'im': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                 'style': 'width: 300px;'}),
            'ot': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                 'style': 'width: 300px;'}),
            'dep': forms.widgets.Select(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                               'style': 'width: 300px;'}),
            'db': forms.widgets.DateInput(attrs={
                'class': 'form-control btn-pill form-control-sm digits input-air-primary',
                'type': 'date', 'style': 'width: 300px;'}, format='%Y-%m-%d'),
            'bitrh_place': forms.widgets.TextInput(attrs={
                'class': 'form-control btn-pill form-control-sm input-air-primary', 'style': 'width: 300px;'}),
            'phone': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                    'style': 'width: 300px;'}),
            'post': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                   'style': 'width: 300px;'}),
            'snils': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                    'style': 'width: 300px;'}),
            'inn': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                  'style': 'width: 300px;'}),
            'pasp_s': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                     'style': 'width: 300px;'}),
            'pasp_n': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                     'style': 'width: 300px;'}),
            'pasp_dep': forms.widgets.TextInput(attrs={
                'class': 'form-control btn-pill form-control-sm input-air-primary', 'style': 'width: 300px;'}),
            'pasp_kem': forms.widgets.TextInput(attrs={
                'class': 'form-control btn-pill form-control-sm input-air-primary', 'style': 'width: 300px;'}),
            'pasp_date': forms.widgets.DateInput(attrs={
                'class': 'form-control btn-pill form-control-sm input-air-primary',
                'type': 'date', 'style': 'width: 300px;'}, format='%Y-%m-%d'),
            'decrees': forms.widgets.SelectMultiple(attrs={'class': 'select2',
                                                           'data-placeholder': 'Выберите приказ(ы)',
                                                           'style': 'width: 300px;'}),
            'is_active': forms.widgets.CheckboxInput(attrs={'class': 'custom-control-input'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ('id', 'name', 'type')
        widgets = {
            'name': forms.widgets.TextInput(attrs={
                'class': 'form-control btn-pill form-control-sm input-air-primary', 'style': 'width: 300px;'}),
            'type': forms.widgets.Select(attrs={
                'class': 'form-control btn-pill form-control-sm input-air-primary', 'style': 'width: 300px;'}),
        }


class EsignForm(forms.ModelForm):
    class Meta:
        model = Esigns
        fields = ('id', 'request_num', 'request_link', 'date_start', 'date_get',
                  'date_valid', 'key', 'cert', 'cer', 'note')
        widgets = {
            'request_num': forms.widgets.TextInput(attrs={
                'class': 'form-control', 'style': 'width: 300px;'}),
            'request_link': forms.widgets.TextInput(attrs={
                'class': 'form-control'}),
            'date_start': forms.widgets.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
                'style': 'width: 300px;'}, format='%Y-%m-%d'),
            'date_get': forms.widgets.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
                'style': 'width: 300px;'}, format='%Y-%m-%d'),
            'date_valid': forms.widgets.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
                'style': 'width: 300px;'}, format='%Y-%m-%d'),
            'key': forms.widgets.TextInput(attrs={
                'class': 'form-control', 'style': 'width: 300px;'}),
            'cert': forms.widgets.FileInput(attrs={
                'class': 'custom-file-input', 'type': 'file'}),
            'cer': forms.widgets.FileInput(attrs={
                'class': 'custom-file-input', 'type': 'file', 'disabled': 'disabled'}),
            'note': forms.widgets.TextInput(attrs={
                'class': 'form-control', 'style': 'width: 450;'})
        }


class DecreeForm(forms.ModelForm):
    class Meta:
        model = Decrees
        fields = '__all__'
        widgets = {
            'number': forms.widgets.TextInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                     'style': 'width: 300px;'}),
            'd_date': forms.widgets.DateInput(attrs={'class': 'form-control btn-pill form-control-sm input-air-primary',
                                                     'type': 'date', 'style': 'width: 300px;'}, format='%Y-%m-%d'),
            'file': forms.widgets.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
        }


# class UploadPersonsForm(forms.Form):
#     file = forms.FileField()
