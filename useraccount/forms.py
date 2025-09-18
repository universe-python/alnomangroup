from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

password_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$',
    message="Password must contain at least one uppercase letter, one lowercase letter, and one number. No special characters allowed."
)

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        validators=[RegexValidator('^[^\W\d_]+$', message="Only alphabets")],
        help_text="Required. Letters only. No numbers or special characters."
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[password_validator],
        help_text="Must include uppercase, lowercase letters, and numbers. No symbols."
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        validators=[password_validator],
        help_text="Repeat the same password. Must include uppercase, lowercase, and numbers."
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
    username = forms.CharField(validators =[RegexValidator('^[^\W\d_]+$',message="Only Alphabets")])
    class Meta:
        model = User
        fields = ['username',]

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Old Password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='New Password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Confirme-Password', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = '__all__'
