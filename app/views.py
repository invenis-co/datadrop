from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView

from app.models import Upload, Download


class UploadCreate(CreateView):
    # pylint: disable=missing-class-docstring
    model = Upload
    fields = ['company', 'file', ]


class UploadDelete(DeleteView):
    # pylint: disable=missing-class-docstring
    model = Upload
    success_url = '/uploads'


class UploadList(ListView):
    # pylint: disable=missing-class-docstring
    model = Upload

    def get_queryset(self):
        return Upload.objects.all().annotate(download_count=Count('download')).order_by('-created_at')


class DownloadList(ListView):
    # pylint: disable=missing-class-docstring
    model = Download

    def get_queryset(self):
        upload = get_object_or_404(Upload, pk=self.kwargs['upload_pk'])
        return Download.objects.filter(upload=upload).prefetch_related('downloader').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload'] = get_object_or_404(Upload, pk=self.kwargs['upload_pk'])
        return context
