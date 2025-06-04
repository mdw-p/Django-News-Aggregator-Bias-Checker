from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Headlines", views.render_articles, name="render_articles"),
    path("Articles/<int:id>/", views.generate_bias_view, name="generate_bias_view"),
]