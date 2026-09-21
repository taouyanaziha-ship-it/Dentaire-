from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('patients/', views.patients_list, name='patients_list'),
    path('patients/ajouter/', views.ajouter_patient, name='ajouter_patient'),

    path('dentistes/',views.dentistes_list, name='dentistes_list'),
    path('dentistes/ajouter/',views.ajouter_dentistes, name='ajouter_dentistes'),

    path('rendezvous/',views.rendezvous_list, name='rendezvous_list'),
    path('rendezvous/ajouter/',views.ajouter_rendezvous, name='ajouter_rendezvous'),

    path('paiements/', views.paiements, name='paiements_liste'),
    path('recu/ajouter/<int:rdv_id>/',views.recu_ajouter,name='recu_ajouter'),
    path('recu/<int:pk>/',views.recu_detail, name='recu_detail'),
   path('recu/<int:pk>/pdf/',views.recu_pdf,name='recu_pdf'),
]
