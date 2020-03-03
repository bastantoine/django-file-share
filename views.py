import mimetypes
import os

import magic
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.conf import settings

from .models import UploadedFile
from .forms import UploadFileForm


class BaseView(View):
    pass


class ProtectedView(BaseView):
    pass


class HomeView(BaseView):

    def get(self, request):
        return render(request, 'file_explorer/home.html')


class AdminView(ProtectedView):

    def get(self, request):
        context = {
            'all_files': UploadedFile.objects.filter(available__exact=True)
        }
        return render(request, 'file_explorer/admin.html', context=context)


class UploadFileView(BaseView):

    def get(self, request):
        context = {
            'form': UploadFileForm()
        }
        return render(request, 'file_explorer/upload.html', context=context)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('file_explorer:home')

class GetFileView(BaseView):

    def guess_mime_type_encoding(self, file_path):
        dummy, encoding = mimetypes.guess_type(file_path)
        # From https://medium.com/@ajrbyers/file-mime-types-in-django-ee9531f3035b
        mime = magic.from_file(file_path, mime=True)
        return (mime, encoding)

    def get(self, request, uuid):
        file = get_object_or_404(UploadedFile, uuid__exact=uuid)
        mimetype, encoding = self.guess_mime_type_encoding(
            os.path.join(settings.UPLOAD_ROOT, file.uploaded_file.name)
        )
        if not mimetype:
            mimetype = 'application/octet-stream'
        response = HttpResponse(
            file.uploaded_file.read(),
            content_type=mimetype,
        )
        response['Content-Disposition'] = 'attachment; filename="%s"' % file.filename
        return response
