from django import forms
from .models import Sermon


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'speaker': forms.TextInput(attrs={'class': 'form-control'}),
            'bible_verse': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control'}),
            'video_link': forms.URLInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'series': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
