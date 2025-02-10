from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.TFCargoHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name="post"),
    path('category/<slug:cat_slug>/', views.Tfcategory.as_view(), name="category"),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page')
]
