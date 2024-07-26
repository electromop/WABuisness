from django.contrib import admin
from .models import User, UserMaterials, Material, Question, Keyword


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserMaterials)
class UserMaterialsAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass

