from django.contrib import admin
from .models import Profile
from .models import Task
from .models import Quote
from .models import Gratitude

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Quote)
admin.site.register(Gratitude)
