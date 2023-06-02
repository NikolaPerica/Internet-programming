from django.contrib import admin
from django.urls import path
from cinemaApp import views


app_name = "cinemaApp"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base),
    path('main/', views.main),
    path('movies/', views.getAllMovies), 
    path('all_tickets/', views.getAllTickets),
    path('usertickets/user/<int:user_id>/', views.usertickets, name='usertickets'),
    path('buy_ticket/', views.buyTicket, name='buy_ticket'),
    path('projections/', views.all_projections, name='projections'),
   
]
