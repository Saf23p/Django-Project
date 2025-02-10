from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from tfcargo.forms import AddPostForm, UploadFileForm
from tfcargo.models import Tfcargo, Category, TagPost, UploadFiles
from tfcargo.utils import DataMixin

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'}
]

class TFCargoHome(DataMixin, ListView):
    # model = Tfcargo
    template_name = 'tfcargo/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Tfcargo.published.all().select_related('cat')


def handle_upload_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# def about(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # handle_upload_file(form.cleaned_data['file'])
#             fp = UploadFiles(file=form.cleaned_data['file'])
#             fp.save()
#     else:
#         form = UploadFileForm()
#     return render(request, 'tfcargo/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})

@login_required
def about(request):
    contact_list = Tfcargo.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tfcargo/about.html',
                  {'title': 'О сайте', 'menu': menu, 'page_obj': page_obj})

class ShowPost(DataMixin, DetailView):
    model = Tfcargo
    template_name = 'tfcargo/post.html'  # нужный шаблон
    slug_url_kwarg = 'post_slug'  # для обозначения точного слага
    context_object_name = 'post'  # переименование для шаблона вместо object будет привычный post

    def get_context_data(self, **kwargs):  # для правильного отображения заголовка, меню
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title = context['post'].title)

    def get_object(self, queryset=None):  # для показа только опубликованных статей (is_published) - true
        return get_object_or_404(Tfcargo.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):  # для добавления записи в БД
    # form_class = AddPostForm #ссылаемся на созданный класс формы
    template_name = 'tfcargo/addpage.html'
    model = Tfcargo
    fields = "__all__"
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)
    # success_url = reverse_lazy('home') #возрващает полный маршрут сайта по имени после успешной формы



class UpdatePage(DataMixin, UpdateView):  # Ддля изменения записи в БД
    template_name = 'tfcargo/addpage.html'
    fields = ['title', 'content', 'photo', 'is_published', 'cat'] #поля для редактирования
    model = Tfcargo
    fields = "__all__"
    success_url = reverse_lazy('home') #возрващает полный маршрут сайта по имени после успешной формы
    title_page = 'Редактирование статьи'


def contact(requests):
    return HttpResponse('Обратная связь')


def login(requests):
    return HttpResponse('Авторизация')


class Tfcategory(DataMixin, ListView):
    template_name = 'tfcargo/index.html'
    context_object_name = 'posts'
    allow_empty = False  # при пустом списке cat = context['posts'] выводит ошибку 404

    def get_queryset(self):
        # для выбора статей по слагу
        return Tfcargo.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title= 'Категория + ' + cat.name,
                                      cat_selected = cat.pk
                                      )

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Tfcargo.Status.PUBLISHED)
    data = {
        "title": f"Тег: {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None
    }

    return render(request, 'tfcargo/index.html', context=data)


def page_not_found(requests, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
