from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from .models import *

class MultipleChoiceListFilterWithCheckbox(MultipleChoiceListFilter):
    template = 'admin/filters.html'



class UserIDFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Пользователь'
    parameter_name = 'id__in'
    
    def lookups(self, request, model_admin):
        return [(obj.id, obj.id) for obj in User.objects.distinct('id')]
    
    
class UserPhoneFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Телефон'
    parameter_name = 'phone_number__in'
    
    def lookups(self, request, model_admin):
        return [(obj.phone_number, obj.phone_number) for obj in User.objects.distinct('phone_number')]
    

class UserNameFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Имя'
    parameter_name = 'name__in'
    
    def lookups(self, request, model_admin):
        return User.objects.distinct().values_list('name', 'name')
    

class UserKeyWordFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Ключевое слово'
    parameter_name = 'key_word__in'
    
    def lookups(self, request, model_admin):
        return Keyword.objects.distinct().values_list('id', 'key_word')
    
class UserRoleFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Роль'
    parameter_name = 'role__in'
    
    def lookups(self, request, model_admin):
        return User.objects.distinct().values_list('role', 'role')
    
class UserChatIDFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Chat ID'
    parameter_name = 'chat_id__in'
    
    def lookups(self, request, model_admin):
        return User.objects.distinct().values_list('chat_id', 'chat_id')
    
class UserRegionFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Регион'
    parameter_name = 'region__in'
    
    def lookups(self, request, model_admin):
        return User.objects.distinct().values_list('region', 'region')
    

user_filters = [UserIDFilter, UserPhoneFilter, UserNameFilter, UserKeyWordFilter, UserRoleFilter, UserChatIDFilter, UserRegionFilter,'date']


class KeywordIDFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'ID'
    parameter_name = 'id__in'
    
    def lookups(self, request, model_admin):
        return Keyword.objects.distinct().values_list('id', 'id')


class KeywordNameFilter(MultipleChoiceListFilterWithCheckbox):
    title = 'Ключевое слово'
    parameter_name = 'key_word__in'
    
    def lookups(self, request, model_admin):
        return Keyword.objects.distinct().values_list('key_word', 'key_word')

keyword_filters = [KeywordIDFilter, KeywordNameFilter]


class UserMaterialPhoneFIlter(MultipleChoiceListFilterWithCheckbox):
    title = 'Телефон'
    parameter_name = 'user_phone__in'
    
    def lookups(self, request, model_admin):
        return UserMaterials.objects.distinct().values_list('user_phone', 'user_phone')

class UserMaterialNameFIlter(MultipleChoiceListFilterWithCheckbox):
    title = 'Материал'
    parameter_name = 'material_name__in'
    
    def lookups(self, request, model_admin):
        return UserMaterials.objects.distinct().values_list('material_name', 'material_name')


user_material_filters = [UserMaterialNameFIlter, UserMaterialPhoneFIlter, 'date']