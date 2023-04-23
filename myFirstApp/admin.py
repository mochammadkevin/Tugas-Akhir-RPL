from django.contrib import admin
from .models import Profile
from .models import Task
from .models import Quote

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Quote)

