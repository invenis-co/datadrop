from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.http.request import split_domain_port
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, DeleteView, FormView, CreateView, UpdateView

from app.forms import UploadForm
from app.models import Upload, Download, Link


def index(request):
    # pylint: disable=missing-function-docstring
    return render(request, 'app/index.html', {})


class LinkCreate(LoginRequiredMixin, CreateView):
    """View to create a link a auto generate an UUID"""
    model = Link
    fields = ['enabled', 'email', 'company', 'first_name', 'last_name']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('update-link', kwargs={'pk': obj.pk}))


class LinkUpdate(LoginRequiredMixin, UpdateView):
    # pylint: disable=missing-class-docstring
    model = Link
    fields = ['enabled', 'email', 'company', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('update-link', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url'] = self.request.build_absolute_uri(reverse('upload', kwargs={'uuid': self.object.uuid}))
        context['upload_count'] = Upload.objects.filter(link=self.object).count
        return context


class LinkList(LoginRequiredMixin, ListView):
    # pylint: disable=missing-class-docstring
    model = Link

    def get_queryset(self):
        return Link.objects.all().annotate(upload_count=Count('upload')).order_by('-created_at')


class LinkDelete(LoginRequiredMixin, DeleteView):
    # pylint: disable=missing-class-docstring
    model = Link
    success_url = '/links'


class FileFieldView(FormView):
    """
    Main page: file upload form.
    Deals with multiple files upload
    """

    form_class = UploadForm
    template_name = 'app/upload_form.html'
    success_url = '/thanks'
    link = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.link = get_object_or_404(Link, uuid=self.kwargs['uuid'])
        if not self.link.enabled:
            self.template_name = 'app/link-disabled.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['link'] = self.link
        return context

    def post(self, request, *args, **kwargs):
        if not self.link.enabled:  # A user can still have the form opened even if the link is disabled
            return HttpResponseRedirect(reverse('link-disabled'))
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            for file in files:
                upload = Upload(file=file, link=self.link)
                upload.save()
            domain, _ = split_domain_port(self.request.get_host())

            context = {
                'filenames': {file.name for file in files},
                'link_url': request.build_absolute_uri(reverse('update-link', kwargs={'pk': self.link.pk})),
                'link_name': self.link.nice_name,
            }
            link_creator = self.link.created_by
            link_creator.email_user(
                subject=_('Data has arrived'),
                message=_('Please go to %s') % context["link_url"],
                html_message=render_to_string(template_name='app/mail_notification.html', context=context),
                from_email=f'datadropbot@{domain}',
                fail_silently=True,
            )
            return self.form_valid(form)
        return self.form_invalid(form)


class UploadDelete(LoginRequiredMixin, DeleteView):
    # pylint: disable=missing-class-docstring
    model = Upload
    success_url = '/uploads'


class UploadList(LoginRequiredMixin, ListView):
    # pylint: disable=missing-class-docstring
    model = Upload

    def get_queryset(self):
        if 'pk' in self.kwargs:
            uploads = Upload.objects.filter(link__pk=self.kwargs['pk'])
        else:
            uploads = Upload.objects.all()
        return uploads.annotate(download_count=Count('download')).order_by('-created_at')


class DownloadList(LoginRequiredMixin, ListView):
    # pylint: disable=missing-class-docstring
    model = Download

    def get_queryset(self):
        upload = get_object_or_404(Upload, pk=self.kwargs['upload_pk'])
        return Download.objects.filter(upload=upload).prefetch_related('downloader').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload'] = get_object_or_404(Upload, pk=self.kwargs['upload_pk'])
        return context
