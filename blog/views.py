from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

# Home page view
class HomeView(ListView):
    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'articles'
    
# Article CRUD views
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', pk=pk)
    form = CommentForm()
    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments, 'form': form})

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('home')
    form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('article_detail', pk=article.pk)
    form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('home')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})

@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_pk = comment.article.pk
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('article_detail', pk=article_pk)
    form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_pk = comment.article.pk
    if request.method == 'POST':
        comment.delete()
        return redirect('article_detail', pk=article_pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})

# User views
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'blog/signup.html'

    def form_valid(self, form):
        view = super(SignUpView, self).form_valid(form)
        login(self.request, self.object)
        return view

class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'blog/login.html'

class LogoutView(LogoutView):
    next_page = 'home'