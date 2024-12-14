from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser

from api.serializers import PasteSerializer
from paste.models import Paste


@csrf_exempt
def paste_list(request):
    if request.method == "GET":
        pastes = Paste.objects.all()
        serializer = PasteSerializer(pastes, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = PasteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    


def paste_detail(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)

    if request.method == "GET":
        serializer = PasteSerializer(paste)
        return JsonResponse(serializer.data)
    
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = PasteSerializer(paste, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == "DELETE":
        paste.delete()
        return HttpResponse(status=204)