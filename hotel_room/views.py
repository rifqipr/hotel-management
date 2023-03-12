from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse
from django.views.generic import ListView, DetailView, FormView, DeleteView
from .forms import *
from .models import *

class RoomList(ListView):
    model = Room

class BookingList(ListView):
    model = Booking

class BookingDetails(DetailView):
    model = Booking
    template_name = "hotel_room/booking_details.html"

class BookingDelete(DeleteView):
    model = Booking
    template_name = "hotel_room/delete_booking.html"
    success_url = reverse_lazy("hotel:booking_list")

class BookingView(FormView):
    form_class = BookingForm
    template_name = "booking_form.html"
    
    def form_valid(self, form):
        data = form.cleaned_data
        valid_rooms = []
        all_rooms = Room.objects.filter(category=data["category"])
        for room in all_rooms:
            if check_availability(room, data["checkin"], data["checkout"]):
                valid_rooms.append(room)
        
        if len(valid_rooms) == 0:
            messages.error(self.request, f"Booking failed")
            return redirect("/hotel/")

        chosen_room = valid_rooms[0]
        booking = Booking.objects.create(
            user = self.request.user,
            room = chosen_room,
            checkin = data["checkin"],
            checkout = data["checkout"]
        )
        booking.save()
        messages.success(self.request, f"Booked a {chosen_room.category} room number {chosen_room.number}")
        return redirect("/hotel/")

def check_availability(room, checkin, checkout):
    available = []
    all_bookings = Booking.objects.filter(room=room)
    for booking in all_bookings:
        if booking.checkin > checkout or booking.checkout < checkin:
            available.append(True)
        else:
            available.append(False)
    return all(available)