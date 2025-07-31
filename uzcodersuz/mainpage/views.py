from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Posts
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.is_superuser and user.is_authenticated

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def Signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'auth/signup.html', {'form': form})


class Login(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
        
class Logout(View):
    def get(self, request):
        logout(request)
        return render(request, 'auth/logout.html')

    class Meta:
        verbose_name = 'Logout'
        verbose_name_plural = 'Logout'

class PasswordResetView(View):
    def get(self, request):
        return render(request, 'auth/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Here you would typically send an email with a reset link
            return HttpResponse(f'Password reset link sent to {email}')
        except User.DoesNotExist:
            return HttpResponse('User with this email does not exist', status=404)

    class Meta:
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'

@user_passes_test(is_superuser)
def manage_users(request):
    users = User.objects.exclude(is_superuser=True)  # Hide the superuser from themselves
    return render(request, 'manage/manage_users.html', {'users': users})

@user_passes_test(is_superuser)
def toggle_staff(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = not user.is_staff
    user.save()
    return redirect('manage_users')

@user_passes_test(is_superuser)
def toggle_active(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('manage_users')

@user_passes_test(is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('manage_users')
    return render(request, 'manage/edit_user.html', {'user': user})


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