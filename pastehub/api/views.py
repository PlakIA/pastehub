from rest_framework import generics

from api.serializers import PasteSerializer
from paste.models import Paste


class PasteList(generics.ListCreateAPIView):
    """
    List all pastes
    """
    queryset = Paste.objects.all()
    serializer_class = PasteSerializer



class PasteDetail(generics.RetrieveDestroyAPIView):
    queryset = Paste.objects.all()
    serializer_class = PasteSerializer
