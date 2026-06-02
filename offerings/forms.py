from django import forms
from .models import Offering


class OfferingForm(forms.ModelForm):
    class Meta:
        model = Offering
        fields = ['member', 'offering_type', 'amount', 'date', 'payment_method', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'offering_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        error_messages={'min_value': 'Amount must be greater than 0.'},
    )
