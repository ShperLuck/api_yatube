from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views

from api.views import CommentViewSet, GroupViewSet, PostViewSet

# Тут создаём роутер для автоматической генерации адресов
main_router = routers.DefaultRouter()

# Регистрируем обработчик для постов - не работает!

# basename
main_router.register('posts', PostViewSet, basename='posts')

# Регистр для групп
main_router.register('groups', GroupViewSet, basename='groups')

# АХ, комменты 

main_router.register(
    r'posts/(?P<post_id>.+)/comments',
    CommentViewSet,
    basename='comments'
)

# итог
urlpatterns = [
    # токен для авторизации
    path('v1/api-token-auth/', views.obtain_auth_token),

    # Упало
    path('v1/', include(main_router.urls)),
]
