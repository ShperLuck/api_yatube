from rest_framework import serializers

from posts.models import Comment, Group, Post, User

# модель пользователя
class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(
        many=True,  # много постов по идеи
        read_only=True,  # не менять список постов отсюда
        slug_field='posts',  # передачка
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')


# Серия1 посты, это основная модель
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, 
        slug_field='username',  # имя
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')

#????

# Серия2 группы — это категории для постов
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')

#????

# Серия3 комментарии — к постам можно писать комментарии
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,  # автор комментарияя автоматом
        slug_field='username', 
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,  # чтобы нельзя было подменить пост в комментарии
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
