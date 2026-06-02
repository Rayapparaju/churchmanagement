from django import forms
from .models import Ministry


class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = ['name', 'description', 'leader', 'meeting_schedule', 'meeting_location', 'is_active', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_schedule': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_location': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
