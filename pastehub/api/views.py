from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse

import api.permissions
from api.serializers import CategorySerializer, PasteSerializer, UserSerializer
from core.storage import get_from_storage, upload_to_storage
from paste.models import Category, Paste
from users.models import CustomUser


class ApiRoot(views.APIView):
    def get(self, request, format=None):
        return Response(
            {
                "users": reverse(
                    "api:user-list",
                    request=request,
                    format=format,
                ),
                "pastes": reverse(
                    "api:paste-list",
                    request=request,
                    format=format,
                ),
            },
        )


class PasteList(generics.ListCreateAPIView):
    queryset = Paste.objects.all()
    serializer_class = PasteSerializer

    def perform_create(self, serializer):
        paste = serializer.save(
            author=(
                self.request.user
                if self.request.user.is_authenticated
                else None
            ),
        )
        upload_to_storage(f"pastes/{paste.id}", self.request.data["content"])


class PasteDetail(generics.RetrieveDestroyAPIView):
    queryset = Paste.objects.all()
    serializer_class = PasteSerializer
    permission_classes = [
        api.permissions.IsAuthorOrReadOnly,
    ]
    lookup_field = Paste.short_link.field.name


class PasteHighlight(generics.GenericAPIView):
    queryset = Paste.objects.all()
    renderer_classes = [renderers.TemplateHTMLRenderer]
    lookup_field = Paste.short_link.field.name

    def get(self, request, *args, **kwargs):
        paste = self.get_object()
        return Response(
            {"content": get_from_storage(f"pastes/{paste.id}")},
            template_name="api/simple_highlight.html",
        )


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetail(generics.RetrieveDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


__all__ = ()
