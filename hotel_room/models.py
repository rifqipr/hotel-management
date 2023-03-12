from django.db import models
from django.conf import settings

class Room(models.Model):
    CATEGORIES = [
        ("STD", "STANDARD"),
        ("DLX", "DELUXE"),
        ("VIP", "VIP"),
        ("KNG", "KING"),
    ]
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=CATEGORIES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room number {self.number}, category {self.category} for {self.capacity}"
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    checkin = models.DateTimeField()
    checkout = models.DateTimeField()

    def __str__(self):
        return f"{self.room} is booked by {self.user} from {self.checkin} to {self.checkout}"