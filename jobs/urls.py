from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('list/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('application/<int:application_id>/', views.manage_application, name='manage_application'),
]
