from django import forms

class BookingForm(forms.Form):
    CATEGORIES = [
        ("STD", "STANDARD"),
        ("DLX", "DELUXE"),
        ("VIP", "VIP"),
        ("KNG", "KING"),
    ]
    category = forms.ChoiceField(choices=CATEGORIES, required=True)
    checkin = forms.DateTimeField(required=True, input_formats=['%d/%m/%Y %H:%M'])
    checkout = forms.DateTimeField(required=True, input_formats=['%d/%m/%Y %H:%M'])