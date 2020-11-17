from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.viewsets import (
    ModelViewSet,
)

from .serializers import (
    PostSerializer,
)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()
