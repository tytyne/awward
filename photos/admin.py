from django.contrib import admin
from .models import Project,tags
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal =('tags',)

# admin.site.register(User)
admin.site.register(Project,ProjectAdmin)
admin.site.register(tags)
