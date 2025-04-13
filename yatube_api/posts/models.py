from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    # Здесь будет храниться основной текст статьи
    text = models.TextField(
        verbose_name='Текст статьи',
        help_text='Введите текст статьи',
    )

    # Дата будет ставиться автоматически при создании записи
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Укажите дату публикации',
    )

    # Здесь будет храниться автор, связывается с моделью пользователя
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор статьи',
        help_text='Укажите автора статьи',
    )

    # Это связь с моделью Group, если пост входит в какую-то категорию
    group = models.ForeignKey(
        'Group',
        blank=True,  # группа может быть не указана
        null=True,
        on_delete=models.SET_NULL,  # если группа удалится, пост останется, просто без группы
        related_name='posts',
        verbose_name='Группа статей',
        help_text='Выберите тематическую группу '
                  'в выпадающем списке по желанию',
    )

    image = models.ImageField(
        verbose_name='Картинка статьи',
        help_text='Добавьте картинку статьи',
        upload_to='posts/',  # картинки будут сохраняться в папке posts/
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-pub_date',)  # статьи будут выводиться по убыванию даты публикации

    def __str__(self):
        return self.text[:15]  # для отображения в админке показываем первые 15 символов


class Group(models.Model):
    # Название группы, вроде категории
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Введите название тематической группы',
    )

    slug = models.SlugField(
        unique=True,  # должно быть уникальным, будет использоваться в URL
        verbose_name='Номер группы',
        help_text='Укажите порядковый номер группы',
    )

    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Добавьте текст описания группы',
    )

    class Meta:
        verbose_name = 'Группа статей'
        verbose_name_plural = 'Группы статей'
        ordering = ('-title',)  # сортировка по алфавиту, но в обратном порядке

    def __str__(self):
        return self.title


class Comment(models.Model):
    # здесь будет связь с постом, к которому написан комментарий
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Имя поста',
        help_text='Укажите имя поста',
    )

    # автор комментария (связь с пользователем)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Имя автора',
        help_text='Укажите автора',
    )

    text = models.TextField(
        max_length=300,  # ограничение на длину комментария
        verbose_name='Текст комментария',
        help_text='Укажите текст комментария',
    )

    created = models.DateTimeField(
        auto_now_add=True,  # автоматически добавляет дату при создании
        verbose_name='Дата комментария',
        help_text='Укажите дату комментария',
    )
    
    # Вроде работает, обрезает текст 
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created',)  # новые комментарии будут сверху

    def __str__(self) -> str:
        
        return self.text[:15]


class Follow(models.Model):
    # Здесь указываем, кто подписался
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Укажите подписчика',
        help_text='Подписчик',
    )

    # А это — на кого подписались
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Укажите на кого подписываемся',
        help_text='Автор поста',
    )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follows',  # не допускаем дублирующие подписки
            ),
        )

    def __str__(self) -> str:
        
        return f'{self.user.username} подписан на {self.author.username}'
