from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from MWG_Site.models import Address, Event

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'city', 'state_abbrev', 'zipcode']


class EventForm(forms.ModelForm):
    time = forms.DateTimeField(widget=DateTimePicker())

    class Meta:
        model = Event
        exclude = ['address', 'created_by']
