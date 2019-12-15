from django import forms
from django.core import validators


class LoginForm(forms.Form):
    mobile_no = forms.CharField(label="Username", max_length=10,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'mobile_no'}),
                                required=True, validators=[validators.BaseValidator])
    dob = forms.DateField(label="Date Of Birth", required=True)