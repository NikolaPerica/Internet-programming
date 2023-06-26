from django.forms import ModelForm
from .models import Projection
from .models import Ticket
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketForm(forms.Form):
    username = forms.CharField(max_length=150)
    projekcija = forms.ModelChoiceField(queryset=Projection.objects.all(), empty_label=None)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        projekcija = cleaned_data.get('projekcija')

        if username and projekcija:
            user = User.objects.filter(username=username).first()
            if not user:
                raise forms.ValidationError("Invalid username.")

            existing_ticket = Ticket.objects.filter(idProjekcija=projekcija, idKorisnik=user).first()
            if existing_ticket:
                raise forms.ValidationError("User has already bought a ticket for this projection.")

            taken_seats = Ticket.objects.filter(idProjekcija=projekcija).values_list('brojSjedala', flat=True)
            kapacitet_dvorane = projekcija.kapacitetDvorane

            if len(taken_seats) >= kapacitet_dvorane:
                raise forms.ValidationError("The capacity is full for the selected movie.")

            # Find the next available seat number
            next_seat = None
            for i in range(1, kapacitet_dvorane + 1):
                if i not in taken_seats:
                    next_seat = i
                    break

            if next_seat is None:
                raise forms.ValidationError("No seats available for the selected movie.")

            cleaned_data['brojSjedala'] = next_seat
            cleaned_data['idKorisnik'] = user

            # Create and save the ticket
            ticket = Ticket.objects.create(
                idProjekcija=projekcija,
                brojSjedala=next_seat,
                idKorisnik=user
            )

            # Decrease the available seats
            projekcija.available_seats = kapacitet_dvorane - taken_seats
            projekcija.save()

        return cleaned_data

