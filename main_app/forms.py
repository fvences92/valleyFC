from django.forms import ModelForm
from .models import Record


class FeedingForm(ModelForm):
    class Meta:
        model = Record
        fields = ['date', 'stat']
