from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm, UserForm


class PostList(ListView):
    model = Post
    ordering = '-dateCreated'
    template_name = 'newslist.html'
    context_object_name = 'allnews'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        context['login_user_id'] = self.request.user.pk
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-dateCreated'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'details.html'
    context_object_name = 'details'


class PostCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = 'news.add_post'
    form_class = PostForm
    post = Post
    template_name = 'post_edit.html'
    html_content = render_to_string(
        'newpost.html',
        {
            'post': post,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{post.header}',
        body=post.text,
        from_email='pavecvet@gmail.com',
        to=[]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class UserEdit(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['login_user_id'] = self.request.user.pk
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('dateCreated')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.categories.subscribers.all()
        context['category'] = self.categories
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    msg = 'Thanks for subscribing to news in '
    return render(request, 'news/subscribe.html', {'category': category, 'message': msg})
