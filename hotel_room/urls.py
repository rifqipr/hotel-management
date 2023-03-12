from django.urls import path
from .views import *

app_name="hotel"

urlpatterns = [
    path("", RoomList.as_view(), name="home"),
    path("bookings/", BookingList.as_view(), name="booking_list"),
    path("bookings/<int:pk>", BookingDetails.as_view(), name="booking_detail"),
    path("bookings/<int:pk>/delete", BookingDelete.as_view(), name="delete_booking"),
    path("new_booking/", BookingView.as_view(), name="create_booking"),
]