from django import forms

from django_select2.forms import Select2Widget

from schedule.models import Availability


class AvailabilityForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time.hour >= end_time.hour:
            st_str = start_time.strftime('%H:%M')
            error_msg = f"Ending time must be later than {st_str}"
            self.add_error('end_time', error_msg)

        return cleaned_data

    class Meta:
        model = Availability
        fields = (
            "neighborhood", "start_day", "end_day", "start_time", "end_time"
        )
        widgets = {
            'neighborhood': Select2Widget
        }
