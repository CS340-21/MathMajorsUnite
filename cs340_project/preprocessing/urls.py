from django.urls import path
from . import views, processing
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='preprocessing-index'),
    path('about/', views.about, name='preprocessing-about'),
    path('text/', views.text, name='preprocessing-text'),
    path('text/text_upload', views.upload_text, name = 'upload_text'),
    path('text/<int:pk>/', views.delete_text, name='delete_text'),
    path('process_text/', views.process_text, name = 'process_text'),
    path('process_text/report<int:pk>/', views.generate_report, name = 'generate_report'),
    path('process_text/a/', processing.redirect_text_process, name = 'text_call'),
    path('process_text/edit<int:pk>', views.edit_file, name = 'edit_file'),
    path('process_text/edit/rename<int:pk>', processing.rename, name = 'rename'),
    path('process_text/edit/drop_cols<int:pk>', processing.drop_cols, name = 'drop'),
    path('process_text/visualize<int:pk>/', views.visualize_data, name = 'visualize'),
    path('text/regression/', views.regression_main, name='regression_main'),
    path('text/regression/<int:pk>/', views.regression_file, name='regression_file')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)