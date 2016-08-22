from django.contrib import admin
from .models import Category, Post, OrderCategory
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

def Indent_category(obj):
    if obj.level == 1:
        return obj.name
    else:
        name = '|'+'----|'*(obj.level-1)+'&raquo;&nbsp;'+ obj.name
        return format_html("{}".format(name))
Indent_category.short_description = '이름'

class CategoryAdmin(admin.ModelAdmin):
    list_display = [Indent_category,'level']
    ordering = ['ordercategory__order_num']


admin.site.register(Category,CategoryAdmin)
admin.site.register(OrderCategory)
admin.site.register(Post,PostAdmin)