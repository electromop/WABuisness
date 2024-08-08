from typing import Any
from django.contrib.admin.utils import model_format_dict

from django.contrib import admin
from .models import User, UserMaterials, Keyword
from import_export import resources
from import_export.admin import ExportActionModelAdmin
from django.http import HttpRequest
from django.utils.timezone import make_aware
from datetime import UTC
from .filters import *


class DBModelAdmin(ExportActionModelAdmin):

    import_export_change_list_template = (
        "admin/change_list_import_export_save.html"
    )

    show_save = False

    def get_changelist_instance(self, request):
        if not request.user.is_superuser:
            list_editable = []
            for field in self.list_display:
                field_perm = f'change_{field}'
                if request.user.has_perm(f'{self.model._meta.app_label}.{field_perm}'):
                    list_editable.append(field)
            self.list_editable = list_editable
        return super().get_changelist_instance(request)
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        if not request.user.is_superuser:
            readonly_fields = []
            for field in self.list_display:
                field_perm = f'change_{field}'
                if not request.user.has_perm(f'{self.model._meta.app_label}.{field_perm}'):
                    readonly_fields.append(field)
            self.readonly_fields = readonly_fields

        return super().get_readonly_fields(request, obj)
    
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context["show_save"] = len(self.list_editable)
        return super().changelist_view(request, extra_context)
    

    def get_action_choices(self, request, default_choices=models.BLANK_CHOICE_DASH):
        """
        Return a list of choices for use in a form object.  Each choice is a
        tuple (name, description).
        """
        choices = []
        for func, name, description in self.get_actions(request).values():
            choice = (name, description % model_format_dict(self.opts))
            choices.append(choice)
        return choices

class KeywordResource(resources.ModelResource):
    class Meta:
        model = Keyword


class UserResource(resources.ModelResource):
    class Meta:
        model = User

    # def dehydrate_date(self, user):
    #     if user.date:
    #         return make_aware(user.date, timezone=UTC)
    #     return None

    def dehydrate_key_word(self, user):
        return user.key_word.key_word

class UserAdminInline(admin.TabularInline):
    model = User


class KeywordAdmin(DBModelAdmin):
    list_display = ["id", "key_word"]
    list_editable = ["key_word"]
    inlines = [UserAdminInline]
    resource_classes = [KeywordResource]
    
    list_filter = keyword_filters


class UserMaterialsResource(resources.ModelResource):
    class Meta:
        model = UserMaterials

    def dehydrate_date(self, user_material):
         if user_material.date:
             return str(user_material.date)
         return None

    def dehydrate_user(self, user_material):
        return user_material.user.id


class UserMaterialsAdmin(DBModelAdmin):

    model = UserMaterials

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ["user_phone", "count", "material_name", "date"]
    resource_classes = [UserMaterialsResource]
    
    list_filter = user_material_filters


class UserMaterialsInLine(admin.TabularInline):
    model = UserMaterials


class UserAdmin(DBModelAdmin):
    list_display = ["id", "phone_number", "name", "key_word" , "role", "chat_id", "date", "region"]
    list_editable = ["phone_number", "name", "key_word", "role", "chat_id", "date", "region"]
    inlines = [UserMaterialsInLine]
    resource_classes = [UserResource]
    
    list_filter = user_filters
    
    
admin.site.register(User, UserAdmin)
admin.site.register(UserMaterials, UserMaterialsAdmin)
admin.site.register(Keyword, KeywordAdmin)
