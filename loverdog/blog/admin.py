from django.contrib import admin
from .models import Post, Category, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

# admin화면(관리자)에 post를 볼 수 있도록 한다
admin.site.register(Post)
admin.site.register(Comment)


#CategoryAdmin : 사용자정의 클래스
# prepopulated_fields:
# admin 페이지에서 특정 필드를 자동으로 채울 수 있도록 설정
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)

admin.site.register(Tag, TagAdmin)
