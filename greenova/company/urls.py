from django.urls import path

from . import views
from .views import CompanyListView

app_name = 'company'

urlpatterns = [
    # Company list and detail
    path('list/', CompanyListView.as_view(), name='list'),
    path('search/', CompanyListView.as_view(), name='search'),
    path('<int:company_id>/', views.company_detail, name='detail'),

    # Company CRUD operations
    path('create/', views.company_create, name='create'),
    path('<int:company_id>/edit/', views.company_edit, name='edit'),
    path('<int:company_id>/delete/', views.company_delete, name='delete'),

    # Company membership management
    path('<int:company_id>/members/', views.manage_members, name='members'),
    path('<int:company_id>/members/add/', views.add_member, name='add_member'),
    path('<int:company_id>/members/<int:member_id>/remove/', views.remove_member, name='remove_member'),
    path('<int:company_id>/members/<int:member_id>/update-role/', views.update_member_role, name='update_role'),

    # Company document management
    path('<int:company_id>/documents/upload/', views.upload_document, name='upload_document'),
    path('<int:company_id>/documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
]
