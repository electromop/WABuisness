import enum

from django.db import models
from django.utils.timezone import now


class UserRole(enum.Enum):
    user = 'user'
    admin = 'admin'


class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    key_word = models.CharField(max_length=255)  # Adjust max_length as needed

    def __str__(self):
        return self.key_word

    class Meta:
        db_table = "keywords"
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)  # Adjust max_length as needed
    key_word = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=5, choices=[(role.value, role.name) for role in UserRole], default=UserRole.user)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Adjust max_length as needed
    chat_id = models.CharField(max_length=255, null=True, blank=True)  # Adjust max_length as needed
    date = models.DateTimeField(default=now)
    region = models.CharField(max_length=255, null=True, blank=True)  # Adjust max_length as needed

    def __str__(self):
        return f"{self.phone_number} | {self.role} | {self.key_word}"

    def add_material(self, material):
        user_material, created = UserMaterials.objects.get_or_create(
            user=self,
            material=material,
            defaults={'count': 1, 'user_phone': self.phone_number, 'material_name': material.name}
        )
        if not created:
            user_material.count += 1
            user_material.save()

    class Meta:
        db_table = "users"
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"


class UserMaterials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=True, primary_key=True)
    count = models.PositiveIntegerField(default=1)
    user_phone = models.CharField(max_length=15)  # Adjust max_length as needed
    material_name = models.CharField(max_length=255)  # Adjust max_length as needed
    date = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('user', 'material_name')
        db_table = "user_materials"
        verbose_name = "Материал пользователя"
        verbose_name_plural = "Материалы пользователя"

    def __str__(self):
        return f'{self.user.phone_number} | {self.material.name} | {self.date.strftime("%d/%m/%Y")}'

