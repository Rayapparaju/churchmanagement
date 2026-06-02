from django import forms
from django.contrib.auth.models import User
from .models import Member, Staff


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth', 'phone', 'email',
            'address', 'photo', 'occupation', 'marital_status', 'baptism_status',
            'baptism_date', 'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relation', 'family_head', 'is_active', 'is_voter', 'voter_id', 'notes',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'baptism_status': forms.Select(attrs={'class': 'form-control'}),
            'baptism_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'family_head': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_voter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'voter_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ABC1234567'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class StaffForm(forms.ModelForm):
    create_user = forms.BooleanField(
        required=False,
        label='Create User Account',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Staff
        fields = [
            'user', 'first_name', 'last_name', 'role', 'phone', 'email',
            'address', 'photo', 'ministry', 'is_active', 'notes',
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'ministry': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        create_user = cleaned_data.get('create_user')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if create_user:
            if not username:
                self.add_error('username', 'Username is required when creating a user account.')
            if not password:
                self.add_error('password', 'Password is required when creating a user account.')
            if username and User.objects.filter(username=username).exists():
                self.add_error('username', 'This username is already taken.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        create_user = self.cleaned_data.get('create_user')

        if create_user and not instance.user:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=self.cleaned_data.get('first_name', ''),
                last_name=self.cleaned_data.get('last_name', ''),
                email=self.cleaned_data.get('email', ''),
            )
            instance.user = user

        if commit:
            instance.save()
        return instance
