# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import set_language # 多言語対応
from django.urls import reverse_lazy


urlpatterns = [
    path('', RedirectView.as_view(url='/memos/', permanent=True), name='home'), 

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('memos/', include('memo_app.urls')),
    path('rag_evaluations/', include('rag_app.urls')),
    path('rag_configs/', include('rag_config_log.urls')),
    path('rag_evaluator/', include('rag_evaluator_tool.urls')),

    # 言語切り替えのためのURL
    path('i18n/setlang/', set_language, name='set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)