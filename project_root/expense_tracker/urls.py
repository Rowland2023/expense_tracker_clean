# expense_tracker/urls.py
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include(('books.urls', 'books'), namespace='books')),  # app routes under /books/
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
