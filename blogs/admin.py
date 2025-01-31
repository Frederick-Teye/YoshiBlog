from django.contrib import admin
from .models import Blog, Comment

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "get_tags"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    @admin.display(description="tags")
    def get_tags(self, obj):
        return ", ".join(o for o in obj.tags.names())


admin.site.register(Blog, BlogAdmin)


admin.site.register(Comment)
