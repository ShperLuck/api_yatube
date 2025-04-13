from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CommentSerializer, GroupSerializer,
                             PostSerializer, UserSerializer)
from posts.models import Group, Post, User


# ViewSet для работы с пользователями
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''Серия пользователей и их данные.'''
    queryset = User.objects.all()  
    serializer_class = UserSerializer 


# ViewSet для работы с постами
class PostViewSet(viewsets.ModelViewSet):
    '''Обрабатываем запросы для постов: создание, получение и изменение.'''
    queryset = Post.objects.all()  
    serializer_class = PostSerializer  
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)  # Разрешение только для авторизованных пользователей

    # Когда новый пост, то привязываем его к текущему пользователю
    def perform_create(self, serializer):
        '''Метод для создания поста с привязкой к автору.'''
        return serializer.save(author=self.request.user)  # Автор сохраняется как свой пользователь


# ViewSet для работы с группами
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''Работаем с группами и получаем их информацию.'''
    queryset = Group.objects.all()  
    serializer_class = GroupSerializer  
    permission_classes = (IsAuthenticated,)  # Только для авторизованных пользователей


# ViewSet для комментариев
class CommentViewSet(viewsets.ModelViewSet):
    '''Обрабатываем комментарии: создание, получение и изменение.'''
    serializer_class = CommentSerializer  
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly,)  # Только авторизованные пользователи и авторы могут изменять

    # Получаем все комментарии для конкретного поста
    def get_queryset(self):
        '''Выбираем комментарии для указанного поста.'''
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))  # Ищем пост по id
        return post.comments.all()  # Возврат на все комментарии к посту

    
    def perform_create(self, serializer):
        '''Создаём комментарий для выбранного поста.'''
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))  # Ищем пост по id
        serializer.save(author=self.request.user, post=post)  # Привязка коммента к пользователю и вроде к посту
