from django import forms
from .models import CommonConfig


class ConfigForm(forms.ModelForm):
    class Meta:
        model = CommonConfig
        fields = ['name', 'banner_image']