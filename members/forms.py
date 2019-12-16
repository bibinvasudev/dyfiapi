from django import forms
from django.core import validators
from groups.models import Group


class MemberForm(forms.Form):
    mobile_no = forms.CharField(label="Mobile No", max_length=10, required=True)
    dob = forms.DateField(label="Date Of Birth", required=True)

    blood_group = forms.CharField(label="Blood Group", required=False)
    qualification = forms.CharField(label="Qualification", required=False)
    job = forms.CharField(label="Job", required=False)
    email = forms.CharField(label="Email", required=False)
    image = forms.CharField(label="Image", required=False)
    age = forms.CharField(label="Age", required=False)
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), label="Gender")
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    house = forms.CharField(label="House", required=False)
    street = forms.CharField(label="Street", required=False)
    city = forms.CharField(label="City", required=False)
    district = forms.CharField(label="District", required=False)
    state = forms.CharField(label="State", required=False)
    pin_code = forms.CharField(label="PIN", required=False)
    # level_id = forms.CharField(label="Level", required=False)
    is_active = forms.BooleanField(label="Is Active?", required=False)
    is_admin = forms.BooleanField(label="Is Admin?", required=False)


class MemberSearchForm(forms.Form):
    mobile_no = forms.CharField(label="Mobile No", max_length=10, required=False)
    dob = forms.DateField(label="Date Of Birth", required=False)

    blood_group = forms.CharField(label="Blood Group", required=False)
    qualification = forms.CharField(label="Qualification", required=False)
    job = forms.CharField(label="Job", required=False)
    email = forms.CharField(label="Email", required=False)
    age = forms.CharField(label="Age", required=False)
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), label="Gender", required=False)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    house = forms.CharField(label="House", required=False)
    street = forms.CharField(label="Street", required=False)
    city = forms.CharField(label="City", required=False)
    district = forms.CharField(label="District", required=False)
    state = forms.CharField(label="State", required=False)
    pin_code = forms.CharField(label="PIN", required=False)
    is_active = forms.BooleanField(label="Is Active?", required=False)
    is_admin = forms.BooleanField(label="Is Admin?", required=False)

