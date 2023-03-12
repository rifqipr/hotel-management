from django import forms

class RoomForm(forms.Form):
    number = forms.IntegerField()
    CATEGORIES = [
        ("STD", "STANDARD"),
        ("DLX", "DELUXE"),
        ("VIP", "VIP"),
        ("KNG", "KING"),
    ]
    category = forms.ChoiceField(choices=CATEGORIES, required=True)
    capacity = forms.IntegerField()

class BookingForm(forms.Form):
    name = forms.CharField(max_length=20)
    CATEGORIES = [
        ("STD", "STANDARD"),
        ("DLX", "DELUXE"),
        ("VIP", "VIP"),
        ("KNG", "KING"),
    ]
    category = forms.ChoiceField(choices=CATEGORIES, required=True)
    checkin = forms.DateTimeField(required=True, input_formats=['%d/%m/%Y %H:%M'])
    checkout = forms.DateTimeField(required=True, input_formats=['%d/%m/%Y %H:%M'])