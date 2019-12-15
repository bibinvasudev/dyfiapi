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
    image = forms.ImageField(label="Image", required=False)
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
    group_ids = forms.MultipleChoiceField(label="Groups", choices=Group.objects.all().values_list("id"), required=False)
    level_id = forms.CharField(label="Level", required=False)
    is_active = forms.BooleanField(label="Is Active?", required=False)
    is_admin = forms.BooleanField(label="Is Admin?", required=False)


class MemberSearchForm(forms.Form):
    mobile_no = forms.CharField(label="Username", max_length=10,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'mobile_no'}),
                                required=True, validators=[validators.BaseValidator])
    dob = forms.DateField(label="Date Of Birth", required=True)

    blood_group = forms.CharField(label="Blood Group")
    qualification = forms.CharField(label="Qualification")
    job = forms.CharField(label="Job")
    email = forms.CharField(label="Email")
    image = forms.FileField(label="Image")
    age = forms.CharField(label="Age")
    gender = forms.Select(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other'), "Gender"))
    name = forms.CharField(label="Name")
    address = forms.CharField(label="Address")
    group_ids = forms.SelectMultiple()
    level_id = forms.CharField(label="Level")
    is_active = forms.BooleanField(label="Is Active?")
    is_admin = forms.BooleanField(label="Is Admin?")

