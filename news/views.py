from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from .filters import PostFilter
from .forms import PostForm
from .models import Post

class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    # model = Post
    # Поле, которое будет использоваться для сортировки объектов
    # ordering = '-time_creates'
    queryset = Post.objects.filter(
        choice_content='AR'
    )
    template_name = 'posts.html'
    context_object_name = 'headings'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class NewsList(ListView):
    queryset = Post.objects.filter(
        choice_content='NW'
    )
    template_name = 'news.html'
    context_object_name = 'headings'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'text_posts.html'
    context_object_name = 'heading'

class NewsDetail(DetailView):
    model = Post
    template_name = 'text_news.html'
    context_object_name = 'heading'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_content='AR'
        return super().form_valid(form)

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.choice_content='NW'
        return super().form_valid(form)

class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'

class NewsEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('post_list')

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

class NewsSearch(ListView):
    model = Post
    ordering = 'heading'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


