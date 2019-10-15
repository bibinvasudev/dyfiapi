from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import ConfigForm
from .models import CommonConfig


def common_config_view(request):
    config = CommonConfig.objects.first()
    if config:
        config.delete()
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('config:success')
    else:
        form = ConfigForm()
    return render(request, 'common_config.html', {'form': form})


def success(request):
    return HttpResponse('Successfully uploaded')


def get_common_config_view(request):
    if request.method == 'GET':
        config = CommonConfig.objects.first()
        return render(request, 'common_config_view.html', {'configs': [config]})
