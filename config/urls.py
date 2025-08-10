# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #パスワードリセット用
from django.conf.urls.i18n import set_language # 多言語対応
from django.urls import reverse_lazy
from . import views as config_views


urlpatterns = [
    path('', RedirectView.as_view(url='/memos/', permanent=True), name='home'), 

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    # 管理画面
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # 学習メモ
    path('memos/', include('memo_app.urls')),
    # ToDo管理
    path('todos/', include('todo_app.urls')),
    # RAG評価ログ
    path('rag_evaluations/', include('rag_app.urls')),
    # AIエージェント構成
    path('rag_configs/', include('rag_config_log.urls')),
    # RAG評価ツール（将来の機能拡張）
    path('rag_evaluator/', include('rag_evaluator_tool.urls')),

    # 言語切り替えのためのURL
    path('i18n/setlang/', set_language, name='set_language'),

    # 検索ビューへのパス
    path('search/', config_views.search_results_view, name='search_results'),

    # パスワードリセットのURL
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)