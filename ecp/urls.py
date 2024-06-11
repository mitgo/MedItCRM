from django.urls import path
from . import views

app_name = 'ecp'
urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),
    # Person
    path('person/<int:pk>/', views.person_esigns, name='person_esigns'),
    path('person/new/', views.person_detail, name='person_new'),
    path('person/new/<str:sotr_id>', views.person_detail, name='person_from_1c'),
    path('person/<int:pk>/edit/', views.person_detail, name='person_detail'),
    path('person/<int:pk>/del/', views.person_delete, name='person_del'),
    # Departments
    path('departments/', views.departments, name='departments'),
    path('departments/<int:pk>', views.department_detail, name='department_detail'),
    path('departments/<int:pk>/persons', views.persons_in_department, name='persons_in_department'),
    # Esigns
    path('esign/new/<int:fk>/', views.esign_detail, name='esign_new'),
    path('esign/<int:pk>/edit/', views.esign_detail, name='esign_detail'),
    path('esign/<int:pk>/del/', views.esign_delete, name='esign_del'),
    # Decrees
    path('decrees/', views.decrees, name='decrees'),
    path('decree/new', views.decree_detail, name='decree_new'),
    path('decree/<int:pk>/edit/', views.decree_detail, name='decree_detail'),
    path('decree/<int:pk>/persons', views.decree_upload_persons, name='decree_upload_persons'),
    # Other
    path('detailedlist/<str:kind>', views.detailed_list, name='detailed_list'),
    path('detailedlist/<str:kind>/<int:deptype>', views.detailed_list, name='detailed_list_dep'),
    path('reports/', views.reports, name='reports'),
    path('download/<str:file_type>/<int:entity_id>/', views.download_file, name='download'),
]
