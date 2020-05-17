from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import path, include
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.static import serve

from app import views
from app.models import Upload, Download


@never_cache  # need to count correctly
@login_required  # security : must be authenticated to access media
def protected_serve_log(request, upload_pk, document_root=None, show_indexes=False):
    """
    Only logged user can download media and downloads are logged
    """
    upload = get_object_or_404(Upload, pk=upload_pk)
    download = Download(downloader=request.user, upload=upload)
    download.save()
    return serve(request, upload.file.name, document_root, show_indexes)


urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'link', views.LinkCreate.as_view(), name='link'),
    path(r'link/<int:pk>/', views.LinkUpdate.as_view(), name='update-link'),
    path(r'links', views.LinkList.as_view(), name='links'),
    path(r'delete-link/<int:pk>/', views.LinkDelete.as_view(), name='delete-link'),

    path(r'upload/<str:uuid>/', views.FileFieldView.as_view(), name='upload'),
    path(r'uploads', views.UploadList.as_view(), name='uploads'),
    path(r'uploads/<int:pk>', views.UploadList.as_view(), name='uploads'),
    path(r'delete-upload/<int:pk>/', views.UploadDelete.as_view(), name='delete-upload'),

    path(r'download/<int:upload_pk>/', protected_serve_log, {'document_root': settings.MEDIA_ROOT}, name='download'),
    path(r'downloads/<int:upload_pk>/', views.DownloadList.as_view(), name='downloads'),
    path(r'thanks', TemplateView.as_view(template_name='app/thanks.html'), name='thanks'),
    path(r'link-disabled', TemplateView.as_view(template_name='app/link-disabled.html'), name='link-disabled'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'%s<int:pk>' % settings.MEDIA_URL[1:], protected_serve_log, {'document_root': settings.MEDIA_ROOT}),
]
# NEVER ADD MEDIA URL DIRECTLY HERE WITHOUT LOGIN REQUIRED
