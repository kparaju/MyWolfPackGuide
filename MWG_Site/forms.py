from django import forms
from MWG_Site.models import Address, Event
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.us.forms import USStateSelect



class AddressForm(forms.ModelForm):
    state_abbrev = forms.CharField(widget=USStateSelect(), initial='NC', label="State")

    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'city', 'state_abbrev', 'zipcode']


class EventForm(forms.ModelForm):
    time = forms.CharField(widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:MM:SS"}))
    description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Event
        exclude = ['address', 'created_by']
