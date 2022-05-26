from django.urls import path
from granite import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', views.homeview.as_view(), name='home'),
    path('about/', views.Aboutview.as_view(), name='about'),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='Logout'),
    path('products/', views.ProductView.as_view(), name='products'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('cart/',views.Cartview.as_view(), name='cart'),
    path('delete/',views.Removecart.as_view(), name='delete'),
    path('add/',views.Addcart.as_view(), name='add'),
    path('search/',  cache_page(60 * 15)(views.SearchView.as_view()),name='search')


]
