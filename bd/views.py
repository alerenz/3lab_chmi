from django.contrib.auth import login, logout
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegisterUserForm, LoginUserForm, AuthorsForm, CourseForm
from .models import Authors, Courses, UsersCourses


# Create your views here.
def index(request):
    return render(request, 'bd/index.html')

def all_authors(request):
    authors = Authors.objects.all()
    return render(request, 'bd/adminPanel/all_authors.html', {'authors': authors})


def all_courses(request):
    courses = Courses.objects.all()
    return render(request, 'bd/adminPanel/all_courses.html', {'courses': courses})


def all_usrcrs(request):
    usr_crs = UsersCourses.objects.all()
    return render(request, 'bd/adminPanel/all_usercourses.html', {'usr_crs': usr_crs})


def courses(request):
    courses = Courses.objects.all()
    return render(request, 'bd/courses.html', {'courses': courses})

def timetable(request):
    courses = Courses.objects.all()
    return render(request, 'bd/timetable.html', {'courses': courses})


def authors(request):
    authors = Authors.objects.all()
    is_autor = Authors.objects.filter(id_user_id=request.user.id).exists()
    return render(request, 'bd/authors.html', {'rol': get_rol(request), 'authors': authors,
        'is_autor': is_autor})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'bd/register.html'
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.all()[2])
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'bd/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def get_rol(request):
    rol = ''
    if request.user.is_authenticated:
        if request.user.groups.all()[0].name == 'admins':
            rol = 'admin'
        elif request.user.groups.all()[0].name == 'avtors':
            rol = 'avtors'
        else:
            rol = 'user'

    return rol


def set_author(request):
    request.user.groups.remove(Group.objects.all()[2])
    request.user.groups.add(Group.objects.all()[1])

    return render(request, 'bd/index.html', {'rol': get_rol(request)})


def author_create(request):
    error = ''
    form = AuthorsForm(initial={'id_user': request.user})
    data = {
        'form': form,
        'error': error,
    }
    if request.method == 'POST':
        form = AuthorsForm(request.POST, initial={'id_user': request.user})
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            error = 'Неверное заполнение данных'

    return render(request, 'bd/addTables/create_author.html', data)


def get_author(request):
    author = Authors.objects.get(id_user_id=request.user.id)
    return author


def get_course(request):
    author = get_author(request)
    course = Courses.objects.get(id_author=author)
    return course


def course_create(request):
    author = get_author(request)
    error = ''
    form = CourseForm(initial={'id_author': author})
    data = {
        'form': form,
        'error': error,
    }
    if request.method == 'POST':
        form = CourseForm(request.POST, initial={'id_author': author})
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            error = 'Неверное заполнение данных'

    return render(request, 'bd/addTables/create_course.html', data)


def course(request, pk):
    flag = False
    crs = Courses.objects.all().filter(id=pk)
    if crs.exists():
        tmpUC = UsersCourses.objects.all().filter(id_user_id=request.user.id, id_course_id=pk)
        if not tmpUC.exists():
            flag = True

    obj_course = Courses.objects.get(id=pk)
    obj_author = Authors.objects.get(id=obj_course.id_author_id)
    author = 0
    if get_rol(request) == 'avtor':
        author = get_author(request)
    return render(request, 'bd/course.html', {'obj_course': obj_course, 'obj_author': obj_author, 'flag': flag,
                                                'rol': get_rol(request), 'author': author})


def create_favorite_course(request, pk):
    UsersCourses.objects.create(id_user_id=request.user.id, id_course_id=pk)
    return course(request, pk)


def output_author_course(request):
    name = 'Мои курсы'
    description = 'У вас пока нет опубликованных курсов'
    courses = Courses.objects.all().filter(id_author=get_author(request).id)
    author = 0
    if get_rol(request) == 'avtor':
        author = get_author(request)
    if not courses.exists():
        courses = 0
    return render(request, 'bd/mycourses.html', {'my_courses': courses, 'rol': get_rol(request),
                                                          'author': author, 'name': name, 'description': description})


def output_favorite_course(request):
    name = 'Избранные курсы'
    description = 'У вас нет избранных курсов'
    favorite_courses = Courses.objects.all().filter(userscourses__id_user_id=request.user.id)
    if not favorite_courses.exists():
        favorite_courses = 0
    return render(request, 'bd/usercourses.html', {'favorite_courses': favorite_courses,
                                                           'name': name, 'description': description})


def user_profile(request):
    is_autor = Authors.objects.filter(id_user_id=request.user.id).exists()
    data = {
        'role': get_rol(request),
        'is_autor': is_autor
    }
    return render(request, 'bd/user_profile.html', data)


class redact_course(UpdateView):
    model = Courses
    template_name = 'bd/addTables/create_course.html'
    form_class = CourseForm

    def get_success_url(self):
        return reverse_lazy('output_author_course')


def del_entry(request,pk):
    course = Courses.objects.get(pk=pk)
    return render(request, 'bd/deleteEntry.html', {'course': course})


def delete_course(request, pk):
    course = Courses.objects.get(pk=pk)
    course.delete()
    course_new = Courses.objects.all()
    return render(request, 'bd/courses.html', {'courses': course_new})

def delete_author(request, pk):
    author = Authors.objects.get(pk=pk)
    author.delete()
    author_new = Authors.objects.all()
    return render(request, 'bd/adminPanel/all_authors.html', {'authors': author_new})

def delete_uscrs(request, pk):
    usr_crs = UsersCourses.objects.get(pk=pk)
    usr_crs.delete()
    usr_crs_new = UsersCourses.objects.all()
    return render(request, 'bd/adminPanel/all_usercourses.html', {'usercourses': usr_crs_new})

class redact_course_admin(UpdateView):
    model = Courses
    template_name = 'bd/addTables/create_course.html'
    form_class = CourseForm

    def get_success_url(self):
        return reverse_lazy('admin_courses')

class redact_author(UpdateView):
    model = Authors
    template_name = 'bd/addTables/create_author.html'
    form_class = AuthorsForm

    def get_success_url(self):
        return reverse_lazy('admin_authors')