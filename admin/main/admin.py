from django.contrib import admin
from .models import User, UserMaterials, Material, Question, Keyword


@admin.register(User)
class UserAdmin(admin.InlineModelAdmin):
    list_display = ["id", "phone_number", "name", "role", "chat_id", "date", "region"]
    inlines = [Keyword]
    list_editable = ["phone_number", "name", "role", "chat_id", "date", "region"]


@admin.register(UserMaterials)
class UserMaterialsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    inlines = [UserAdmin, Material]
    list_display = ["user_number", "count", "material_name", "date"]


@admin.register(Material)
class MaterialAdmin(admin.InlineModelAdmin):
    list_display = ["id", "name", "key_word"]
    list_editable = ["name", "key_word"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "question"]
    list_editable = ["phone_number", "question"]


@admin.register(Keyword)
class KeywordAdmin(admin.InlineModelAdmin):
    list_display = ["id", "key_word"]
    list_editable = ["key_word"]

