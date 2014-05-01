from django import forms
from MWG_Site.models import Address, Event
# from localflavor.us.forms import USStateSelect
from bootstrap3_datetime.widgets import DateTimePicker



class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'city', 'state_abbrev', 'zipcode']


class EventForm(forms.ModelForm):

    time = forms.DateTimeField(
        required=True,
        widget=DateTimePicker(
            options={"format": "YYYY-MM-DD HH:mm"}
            )
        )

    class Meta:
        model = Event
        exclude = ['address', 'created_by']

