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

def make_published(modeladmin, request, queryset):
    queryset.update(article_status='P')
make_published.short_description = "Mark as Published"

	

def make_draft(modeladmin, request, queryset):
    queryset.update(article_status='R')
make_draft.short_description = "Mark as Draft"


class UserProfileInline(admin.StackedInline):
    model = UserProfile

    can_delete = False
    


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    # list_display = ['email']
    actions = [make_admin, make_editor, make_regular]

    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_title', 'article_desc', 'article_img', 'article_status', 'article_author']
    list_display_links = ['article_desc', 'article_img']
    list_editable = ['article_title']
    list_filter = ['article_add_date', 'article_update_date', 'article_status', 'article_tags']
    search_fields = ['article_title', 'article_desc','article_body']
    form = ArticleForm
    actions = [make_published, make_draft]



# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Comment)




