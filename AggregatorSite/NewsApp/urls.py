from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("Headlines", views.render_articles, name="render_articles"),
    path("Articles/<int:id>/", views.generate_bias_view, name="generate_bias_view"),
    path('', RedirectView.as_view(url='/Headlines', permanent=False), name='index')
]