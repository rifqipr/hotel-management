from django.views.generic import ListView, DetailView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages

from .models import *
from .forms import *

class RoomListApiView(ListView):
    model = Room

    def get(self, request, *args, **kwargs):
        rooms = self.get_queryset()
        data = list(rooms.values())
        return JsonResponse(data, safe=False)

class BookingListApiView(ListView):
    model = Booking

    def get(self, request, *args, **kwargs):
        bookings = self.get_queryset()
        data = list(bookings.values())
        return JsonResponse(data, safe=False)
    
class BookingDetailsApiView(DetailView):
    model = Booking

    def get(self, request, *args, **kwargs):
        booking = self.get_object()
        data = serializers.serialize('json', [booking])
        return JsonResponse(data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class BookingApiView(FormView):
    form_class = BookingForm

    def form_valid(self, form):
        data = form.cleaned_data
        valid_rooms = []
        all_rooms = Room.objects.filter(category=data["category"])
        for room in all_rooms:
            if check_availability(room, data["checkin"], data["checkout"]):
                valid_rooms.append(room)
        
        if len(valid_rooms) == 0:
            response_data = {"message": "Booking failed"}
            return JsonResponse(response_data, status=400)

        chosen_room = valid_rooms[0]
        booking = Booking.objects.create(
            user = data["name"],
            room = chosen_room,
            checkin = data["checkin"],
            checkout = data["checkout"]
        )
        booking.save()
        response_data = {"message": f"Booked a {chosen_room.category} room number {chosen_room.number}"}
        return JsonResponse(response_data, status=201)

    def form_invalid(self, form):
        response_data = {"message": "Booking form is invalid"}
        return JsonResponse(response_data, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class RoomApiView(FormView):
    form_class = RoomForm

    def form_valid(self, form):
        data = form.cleaned_data
        all_rooms = Room.objects.all()
        for room in all_rooms:
            if data["number"] == room.number:
                response_data = {"message" : "Room number exists"}
                return JsonResponse(response_data, status=400)
            
        new_room = Room.objects.create(
            number = data["number"],
            category = data["category"],
            capacity = data["capacity"]
        )
        new_room.save()
        response_data = {"message" : f"Created a {new_room.category}, numbered {new_room.number}"}
        return JsonResponse(response_data, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class BookingDeleteApiView(DeleteView):
    model = Booking

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = {'message': 'Booking deleted successfully.'}
        self.object.delete()
        return JsonResponse(success_message)

def check_availability(room, checkin, checkout):
    available = []
    all_bookings = Booking.objects.filter(room=room)
    for booking in all_bookings:
        if booking.checkin > checkout or booking.checkout < checkin:
            available.append(True)
        else:
            available.append(False)
    return all(available)