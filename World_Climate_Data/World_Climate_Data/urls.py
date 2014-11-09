from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'World_Climate_Data.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('core.urls'))

)
