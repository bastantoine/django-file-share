from django.shortcuts import render, redirect
from django.views import View

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

    def get(self, request):
        return render(request, 'file_explorer/get.html')
