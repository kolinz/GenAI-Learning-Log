# memo_app/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.hashers import make_password, identify_hasher

from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from import_export.admin import ImportExportModelAdmin

from .models import LearningMemo, Tag, MemoAttachment

admin.site.register(LearningMemo)
admin.site.register(Tag)
admin.site.register(MemoAttachment)

# --- ここから User の import-export 対応 ---
class UserResource(resources.ModelResource):
    groups = fields.Field(
        column_name="groups",
        attribute="groups",
        widget=ManyToManyWidget(Group, field="name", separator="|"),
    )
    user_permissions = fields.Field(
        column_name="permissions",
        attribute="user_permissions",
        widget=ManyToManyWidget(Permission, field="codename", separator="|"),
    )
    raw_password = fields.Field(column_name="raw_password", attribute=None)

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name",
            "is_active", "is_staff", "is_superuser",
            "groups", "permissions", "password", "raw_password",
        )
        export_order = fields
        import_id_fields = ("username",)
        skip_unchanged = True
        report_skipped = True
    
    # エクスポート時はハッシュを出さない
    def dehydrate_password(self, obj):
        return ""
    
    def before_import_row(self, row, **kwargs):
        raw = (row.get("raw_password") or "").strip()
        if raw:
            try:
                identify_hasher(raw)  # 既にハッシュなら通る
                row["password"] = raw
            except Exception:
                row["password"] = make_password(raw)
        else:
            row.pop("password", None)

    def after_import_row(self, row, row_result, **kwargs):
        row.pop("raw_password", None)

# 既定の UserAdmin を置き換える
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, DjangoUserAdmin):
    resource_class = UserResource
    list_display = ("username", "email", "is_staff", "is_active", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")