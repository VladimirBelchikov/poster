from django.shortcuts import render
from django.http import HttpResponse
import json

from website.models import get_sorted_list


def index(request):
    return render(request, 'index.html')


def get_dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def get_clients_data(request):
    data = get_sorted_list()
    return HttpResponse(json.dumps(data))
