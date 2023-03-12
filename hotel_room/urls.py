from django.urls import path
from .views import *
from .api import *

app_name="hotel"

urlpatterns = [
    path("", RoomList.as_view(), name="home"),
    path("bookings/", BookingList.as_view(), name="booking_list"),
    path("bookings/<int:pk>", BookingDetails.as_view(), name="booking_detail"),
    path("bookings/<int:pk>/delete", BookingDelete.as_view(), name="delete_booking"),
    path("new_booking/", BookingView.as_view(), name="create_booking"),

    # APIs
    path('api/rooms/', RoomListApiView.as_view(), name='room_list_api'),
    path('api/bookings/', BookingListApiView.as_view(), name='booking_list_api'),
    path('api/booking/<int:pk>/', BookingDetailsApiView.as_view(), name='booking_details_api'),
    path('api/booking/<int:pk>/delete/', BookingDeleteApiView.as_view(), name='booking_delete_api'),
    path('api/new_booking/', BookingApiView.as_view(), name='booking_api'),
    path('api/new_room/', RoomApiView.as_view(), name='room_api'),
]