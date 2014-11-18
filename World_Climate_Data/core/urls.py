from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
	url('^display?', views.main_display),
    url('^$', TemplateView.as_view(template_name='index.html')),
)
