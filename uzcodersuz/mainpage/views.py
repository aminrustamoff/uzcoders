from django.shortcuts import render, HttpResponse 
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Posts
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def home(request):
    return render(request, 'index.html')

class PostsView(ListView):
    model = Posts
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
class PostDetailView(DetailView):
    model = Posts
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post.view_count += 1
        post.save()
        return context

    class Meta:
        verbose_name = 'Post Detail'
        verbose_name_plural = 'Post Details'

class CreatePostView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'mainpage.add_posts'

    def get(self, request):
        return render(request, 'create_post.html')

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = request.user
        post = Posts.objects.create(user=user, title=title, content=content)
        return HttpResponse(f'Post "{post.title}" created successfully!') 

    class Meta:
        verbose_name = 'Create Post'
        verbose_name_plural = 'Create Posts'