from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginview, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutview, name='logout'),
    path('habit/', views.habit, name='habit'),
    path('habit_create/', views.habitcreate, name='habit_create'),
    path('habit_update/<int:id>/', views.habitupdate, name='habit_update'),
    path('habit_edit/<int:id>/', views.habit_edit, name='habit_edit'),
    path('habit_delete/<int:id>/', views.habitdelete, name='habit_delete'),
    path('habit_detail/<int:id>/', views.habitdetail, name='habit_detail'),
    path('task_list/', views.tasklist, name='tasks'),
    path('task/<int:pk>/', views.taskdetail, name='task'),
    path('task_create/', views.taskcreate, name='task_create'),
    path('task_delete/<int:pk>/', views.taskdelete, name='task_delete'),
    path('task_complete/<int:pk>/', views.taskcomplete, name='task_complete'),
    path('task_update/<int:pk>/', views.taskupdate, name='task_update'),
    path('settings/', views.settings, name='settings'),
    path('gratitude/', views.gratitude, name='gratitude'),
    path('gratitude_create/', views.gratitudecreate, name='gratitude_create'),
    path('gratitude_journal/', views.gratitudejournal, name='gratitude_journal'),
    path('gratitude_delete/<int:pk>/', views.gratitudedelete, name='gratitude_delete'),
    path('settingsedit/', views.settingsedit, name='settingsedit'),
    path('financetracker/', views.financetracker, name='financetracker'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
