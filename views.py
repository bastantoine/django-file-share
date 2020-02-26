from django.shortcuts import render
from django.views import View


class BaseView(View):
    pass


class ProtectedView(BaseView):
    pass


class HomeView(BaseView):

    def get(self, request):
        return render(request, 'file_explorer/home.html')


class AdminView(ProtectedView):

    def get(self, request):
        return render(request, 'file_explorer/admin.html')


class UploadFileView(BaseView):

    def get(self, request):
        return render(request, 'file_explorer/upload.html')


class GetFileView(BaseView):

    def get(self, request):
        return render(request, 'file_explorer/get.html')
