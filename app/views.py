from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, FormView

from app.forms import UploadForm
from app.models import Upload, Download


class FileFieldView(FormView):
    """
    Main page: file upload form.
    Deals with multiple files upload
    """

    form_class = UploadForm
    template_name = 'app/upload_form.html'
    success_url = 'thanks'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            for file in files:
                upload = Upload(company=form.cleaned_data['company'], file=file)
                upload.save()
            return self.form_valid(form)
        return self.form_invalid(form)


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
