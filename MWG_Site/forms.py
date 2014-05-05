from django import forms
from MWG_Site.models import Address, Event, Tag
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.us.forms import USStateSelect
from django.utils.translation import ugettext as _

class TagForm(forms.ModelForm):
    existing_tag = forms.ModelChoiceField(queryset=Tag.objects.all(),
                    label="Choose an Existing Tag",
                    empty_label="Select a Tag",
                    required=False
                    )
    new_tag      = forms.CharField(max_length=35, label="Create a New Tag", required=False)

    class Meta:
        model = Tag
        fields = ['existing_tag', 'new_tag']

    def clean(self):
        if not self.cleaned_data['existing_tag'] and not self.cleaned_data['new_tag']:
            raise forms.ValidationError(_('Please apply a tag to your event.'), code='invalid')
        elif self.cleaned_data['existing_tag'] and self.cleaned_data['new_tag']:
            raise forms.ValidationError(_('You may only apply one tag at a time.'), code='invalid')

        return self.cleaned_data


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
        exclude = ['address', 'created_by', 'attendees', 'tags']
