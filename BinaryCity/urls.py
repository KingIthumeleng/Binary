from django.urls import path
from BinaryCityApp import views

urlpatterns = [
    path('', views.client_page_view, name='client_view'),
    path('contacts_view/', views.contact_page_view, name='contacts_view'),
    path('success_contact_added/', views.success_contact_added, name='success_contact_added'),
    path('success_linked/<str:client_code>/', views.success_contact_linked, name='client_link'),
    path('success_contact_linked/<str:contact_code>/', views.success_client_link, name='contact_link'),
    path('success_unlinked/<int:contact_code>/', views.success_contact_unlinked, name='client_unlink'),
    path('deleteDB/', views.deleteDB, name='content_delete'),

    
    
]
