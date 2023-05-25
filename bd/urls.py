from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('courses', views.courses, name='courses'),
    path('author', views.authors, name='authors'),
    path('user', views.user_profile, name='user_profile'),
    path('set_author', views.set_author, name='set_author'),
    path('author_create', views.author_create, name='author_create'),
    path('course_create', views.course_create, name='course_create'),
    path('course/<int:pk>', views.course, name='course_only'),
    path('create_favorite_course/<int:pk>', views.create_favorite_course, name='create_favorite_course'),
    path('output_favorite_course/', views.output_favorite_course, name='output_favorite_course'),
    path('output_author_course/', views.output_author_course, name='output_author_course'),
    path('update_course/<int:pk>', views.redact_course.as_view(), name='update_course'),
    path('del_entry/<int:pk>', views.del_entry, name='delete_entry'),
    path('delete_course/<int:pk>', views.delete_course, name='delete_course'),
    path('delete_author/<int:pk>', views.delete_author, name='delete_author'),
    path('delete_usercourses/<int:pk>', views.delete_uscrs, name='delete_usrcrs'),
    path('update_course_admin/<int:pk>', views.redact_course_admin.as_view(), name='update_course_admin'),
    path('update_author/<int:pk>', views.redact_author.as_view(), name='update_author'),
    path('admin_author', views.all_authors, name='admin_authors'),
    path('admin_course', views.all_courses, name='admin_courses'),
    path('admin_usercourses', views.all_usrcrs, name='admin_usercourses'),
    path('timetable', views.timetable, name='timetable')

]
