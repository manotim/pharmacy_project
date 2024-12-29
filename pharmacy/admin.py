from django.contrib import admin
from .models import Drug, Type, Cart

# Register your models here.
admin.site.register(Drug)
admin.site.register(Type)
admin.site.register(Cart)