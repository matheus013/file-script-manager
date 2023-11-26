from django.urls import path

from core.views.file import *
from core.views.execute import *

urlpatterns = [
    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('files/<int:file_id>/download/', FileDownloadView.as_view(), name='file-download'),
    path('file-scripts/', FileScriptListCreateView.as_view(), name='file-script-list-create'),
    path('file-scripts/<int:pk>/', FileScriptDetailView.as_view(), name='file-script-detail'),
    path('execute/<int:file_id>/<int:script_id>/', ApplyScriptToFileDialogView.as_view(), name='apply')
]
