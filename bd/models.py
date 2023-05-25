from django.contrib.auth.models import User
from django.db import models


class Authors(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField('Фамилия', max_length=30)
    name = models.CharField('Имя', max_length=30)
    email = models.EmailField('email')

    def __str__(self):
        return f'Автор:{self.surname} {self.name}'

    def get_absolute_url(self):
        return f'/update_author/{self.id}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Courses(models.Model):
    header = models.TextField('Заголовок',max_length=50)
    description = models.TextField('Описание',max_length=50)
    main_text = models.TextField('Основной текст',max_length=50)
    start_date = models.DateField('Начало курса',null=True)
    end_date = models.DateField('Конец курса',null=True)
    id_author = models.OneToOneField(Authors, on_delete=models.CASCADE)

    def __str__(self):
        return f'Курс:{self.header}'

    def get_absolute_url(self):
        return f'/update_course/{self.id}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class UsersCourses(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f'Курсы пользователя:{self.id_user}'

    class Meta:
        verbose_name = 'Курсы пользователя'
        verbose_name_plural = 'Курсы пользователей'
