from django import forms
from .models import Attendance
from members.models import Staff

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['event_type', 'date', 'attended', 'notes']
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BulkAttendanceForm(forms.Form):
    event_type = forms.ChoiceField(
        choices=Attendance.EVENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )
    staff_members = forms.ModelMultipleChoiceField(
        queryset=Staff.objects.filter(is_active=True).order_by('first_name'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label='Staff Members',
    )

    def clean_date(self):
        date = self.cleaned_data['date']
        from datetime import date as dt_date
        if date > dt_date.today():
            raise forms.ValidationError("Date cannot be in the future.")
        return date
