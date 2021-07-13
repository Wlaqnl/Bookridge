from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import LibraryLocation
from .serializers import LibraryLocationSerializer
# Create your views here.

@csrf_exempt
def get_lib_all(request):
    libs = LibraryLocation.objects.all()
    libs_serial = LibraryLocationSerializer(libs)
    # print(libs_serial.data)
    return JsonResponse(libs_serial.data)