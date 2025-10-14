from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    """Simple registration form with email and password"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    full_name = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    mobile = forms.CharField(
        required=False,
        max_length=17,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '01712345678',
            'type': 'tel'
        }),
        help_text="Bangladesh mobile number (e.g., 01712345678 or +8801712345678)"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'mobile']