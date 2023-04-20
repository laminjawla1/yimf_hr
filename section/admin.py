from django.contrib import admin
from .models import Classification, Title, Department, Division

# Register your models here.
admin.site.register(Classification)
admin.site.register(Title)
admin.site.register(Department)
admin.site.register(Division)
