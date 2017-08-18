from django.contrib import admin
from .models import Post,UserProfile
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
    'status',)
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    #in admin we have to input a primary key, in this case id i.e 1,2...
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Post,PostAdmin)
admin.site.register(UserProfile)
