from django.urls import path
from . import views, processing
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='preprocessing-index'),
    path('about/', views.about, name='preprocessing-about'),
    path('image/', views.image, name='preprocessing-image'),
    path('image/<int:pk>/', views.delete_image, name='delete_image'),
    path('text/', views.text, name='preprocessing-text'),
    path('text/text_upload', views.upload_text, name = 'upload_text'),
    path('text/<int:pk>/', views.delete_text, name='delete_text'),
    path('process_text/', views.process_text, name = 'process_text'),
    path('process_text/report<int:pk>/', views.generate_report, name = 'generate_report'),
    path('process_image/', views.process_image, name = 'process_image'),
    path('process_text/a/', processing.redirect_text_process, name = 'text_call'),
    path('process_text/merge/', processing.merge, name = 'merge'),
    path('process_text/edit/', views.edit_file, name = 'edit_file'),
    path('process_text/edit/rename/', processing.rename, name = 'rename'),
    path('process_image/', processing.redirect_img_process, name = 'img_call'),
    path('process_text/visualize<int:pk>/', views.visualize_data, name = 'visualize'),
    path('process_text/visualize<int:pk>/pass_visualization<int:pk/', processing.pass_visualizations, name = 'pass_vis')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)