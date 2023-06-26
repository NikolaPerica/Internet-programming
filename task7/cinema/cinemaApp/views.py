from django.shortcuts import render, redirect
from .models import Projection, Ticket
from django.contrib.auth import get_user_model
from django.http import HttpResponseNotAllowed
from .forms import TicketForm
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.db.models import Count


# Create your views here.
def base(request):
    greeting = "Hello"
    return render(request, "base.html", {"data": greeting})

def main(request):
    users = User.objects.all()
    return render(request, "main.html", {"users": users})

def getAllMovies(request):
    projekcije = Projection.objects.all()
    return render(request, "movies.html", {"projekcije": projekcije})

def getAllTickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'all_tickets.html', {'tickets': tickets})

def usertickets(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        karte = Ticket.objects.filter(idKorisnik=user)
        return render(request, "usertickets.html", {"karte": karte, "user": user})
    except User.DoesNotExist:
        return render(request, "user_not_found.html")

def buyTicket(request):
    User = get_user_model()
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            broj_sjedala = form.cleaned_data['brojSjedala']
            projekcija = form.cleaned_data['projekcija']
            korisnik = User.objects.get(username=username)

            Ticket.objects.create(
                brojSjedala=broj_sjedala,
                idKorisnik=korisnik,
                idProjekcija=projekcija
            )
            return redirect('http://localhost:8000/main/')
    else:
        form = TicketForm()

    return render(request, "buy_ticket.html", {"form": form})

def all_projections(request):
    ticket_counts = Ticket.objects.filter(idProjekcija=OuterRef('pk')).values('idProjekcija').annotate(count=Count('id')).values('count')
    projections = Projection.objects.annotate(taken_seats=Subquery(ticket_counts))
    projection_list = []
    
    for projection in projections:
        taken_seats = projection.taken_seats or 0
        available_seats = projection.kapacitetDvorane - taken_seats
        projection_list.append((projection, available_seats))
    
    context = {'projection_list': projection_list}
    return render(request, 'projections.html', context)



