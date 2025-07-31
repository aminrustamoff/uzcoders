from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.PostsView.as_view(), name='posts_list'),
    path('contact/', views.contact, name='contact'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', views.CreatePostView.as_view(), name='create_post'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/logout/', views.Logout.as_view(), name='logout'),
    path('accounts/signup/', views.Signup, name='signup'),
    path('accounts/reset_password/', views.PasswordResetView.as_view(), name='password_reset'),
    path('manage/users/', views.manage_users, name='manage_users'),
    path('manage/users/<int:user_id>/toggle-staff/', views.toggle_staff, name='toggle_staff'),
    path('manage/users/<int:user_id>/toggle-active/', views.toggle_active, name='toggle_active'),
    path('manage/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
]