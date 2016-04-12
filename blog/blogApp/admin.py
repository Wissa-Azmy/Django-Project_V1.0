from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import *
from .models import *


def make_admin(modeladmin, request, queryset):
    queryset.update(role='A')
make_admin.short_description = "Make Admin"

def make_editor(modeladmin, request, queryset):
    queryset.update(role='E')
make_editor.short_description = "Make Editor"

def make_regular(modeladmin, request, queryset):
    queryset.update(role='R')
make_regular.short_description = "Make Regular"



def approve(modeladmin, request, queryset):
    queryset.update(approved=True)
approve.short_description = "Approve"

def publish(modeladmin, request, queryset):
    queryset.update(publish=True)
publish.short_description = "Publish"

def make_draft(modeladmin, request, queryset):
    queryset.update(publish=False)
make_draft.short_description = "Make Draft"




class UserProfileInline(admin.StackedInline):
    model = UserProfile

    can_delete = False
    


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    # list_display = ['email']
    actions = [make_admin, make_editor, make_regular]

    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image', 'approved', 'publish', 'author']
    list_display_links = ['description', 'image']
    list_editable = ['title']
    list_filter = ['publish_date', 'update_date', 'approved', 'publish', 'tags']
    search_fields = ['title', 'description','body']
    form = ArticleForm
    actions = [approve, publish, make_draft]



# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Comment)




