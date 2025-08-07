# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
# from . import views as config_views # <-- この行を削除

urlpatterns = [
    path('', RedirectView.as_view(url='/memos/', permanent=True), name='home'), 

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('memos/', include('memo_app.urls')),
    path('rag_evaluations/', include('rag_app.urls')),
    path('rag_configs/', include('rag_config_log.urls')),
    path('rag_evaluator/', include('rag_evaluator_tool.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)