from django.urls import path
from . import views
from django.http import HttpResponse
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('superadmin/',views.admin_home,name='super'),
    path('student/',views.stud_home,name='student'),   
    path('profesor/',views.prof_home,name='profesor'),
    path('', views.home,name="home"),
    path('login/',auth_views.LoginView.as_view(template_name='index.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='projekti/logout.html'),name='logout'),
    path('super/adduser',views.adduser,name='adduser'),
    path('super/professors',views.professors,name='professors'),
    path('super/students',views.students,name='students'),
    path('super/addpred',views.addpredmet,name='addpred'),
    path('super/predmet',views.predmeti,name='predmeti'),
    path('super/edituser/<str:pk>/',views.edituser,name='edituser'),
    path('super/editpredmet/<str:pk>/',views.editpredmet,name='editpredmet'),
    path('super/addupis/<str:student_id>/',views.upis_studenta,name='addupis'),
    path('super/students/upisi/<str:pk>/',views.listupis,name='upis'),
    path('super/students/upisi/editupis/<str:pk>/',views.change_upis,name='editupis'),
    path('super/predmeti/liststud/<str:pk>/',views.list_users_per_predmet,name='studpred'),
    path('profesor/profpred',views.listpredmet,name='profpred'),
    path('profesor/profpred/<str:pk>',views.liststud,name='seestud'),
    path('profesor/profpred/upis/<str:pk>/<str:fk>/',views.changestatus,name='editupis'),
    path('student/predstud/',views.listpred,name='predstud'),
    path('student/addupis/<str:pk>',views.add_upis_student,name='addupisstud'),
    path('student/seeupisi/',views.current_upisi,name='seeupis'),
    path('upis/delete/<int:upis_id>/', views.delete_upis, name='delete_upis'),
    path('super/<int:pk>/delete/', views.delete_user, name='delete_user'),
    
]