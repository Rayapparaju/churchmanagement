from django import forms
from .models import PrayerRequest


class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'phone', 'request', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'request': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PrayerUpdateForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'admin_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
