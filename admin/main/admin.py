from django.contrib import admin
from .models import User, UserMaterials, Material, Question, Keyword


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserMaterials)
class UserMaterialsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "question"]
    list_editable = ["phone_number", "question"]


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass

