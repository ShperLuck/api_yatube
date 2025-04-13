from django.contrib import admin

from posts.models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')  
    list_display_links = ('text', 'author')  
    list_editable = ('group',)  
    list_filter = ('pub_date', 'group')
    empty_value_display = '-пусто-'
    search_fields = ('text',)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    list_display_links = ('title',)
    list_editable = ('slug',)
    empty_value_display = '-пусто-'


# Это для управления комментариями в админке
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'post', 'created')
    list_editable = ('text',)  # текст коммента можно будет править сразу
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)  # Показываем, кто на кого подписан


# Регистрируем все !МОДЕЛИ! для админки
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)