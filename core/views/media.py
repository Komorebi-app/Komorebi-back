import os

from django.conf import settings
from django.http import FileResponse, Http404

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

class MediaViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve_file(self, _, filename):
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        _, extension = os.path.splitext(filename)

        if not os.path.exists(file_path):
            raise Http404("L'image n'existe pas sur le serveur.")

        content_type = f"image/{extension[1:]}"
        return FileResponse(open(file_path, 'rb'), content_type=content_type)
