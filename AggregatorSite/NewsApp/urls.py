from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('Headlines', views.render_articles, name='render_articles'),
    path('Articles/<int:id>/', views.generate_bias_view, name='generate_bias_view'),
    path('', RedirectView.as_view(url='/NewsApp/Headlines', permanent=False), name='index'),
    path('register',views.register,name='register'),
    path('manage_feed',views.manage_feed,name="manage_feed"),
    path('feed',views.feed,name="feed"),
    path('logout',views.logout_view,name="logout")
]