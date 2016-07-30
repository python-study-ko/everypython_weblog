from django.contrib import admin
from blog.models import Category, Post, OrderCategory
from django.utils.html import format_html

def Tag_list(obj):
    tags = obj.tag.get_queryset().values_list('name',flat=True)
    if len(tags) >= 4:
        tags = tags[:3]+['...']
    return ', '.join(tag for tag in tags)

Tag_list.short_description = '태그'
Tag_list.allow_tags = True

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk','category','publish','title',Tag_list,'create_date','edit_date')
    list_display_links = ['title']
    list_filter = ('category', 'publish','edit_date')
    search_fields = ['title','content','description']
    date_hierarchy = 'create_date'

    actions = ['make_published','make_unpublish']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(publish=True)
        if rows_updated == 1:
            message_bit = "포스트 한개가 발행됬습니다."
        else:
            message_bit = "%s 개의 포스트가 발행됬습니다." % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    def make_unpublish(self, requset, queryset):
        rows_updated = queryset.update(publish=False)

    make_published.short_description = "선택한 포스트를 발행하기"
    make_unpublish.short_description = "선택한 포스트의 발행을 취소하기   "

admin.site.register(Category)
admin.site.register(OrderCategory)
admin.site.register(Post,PostAdmin)