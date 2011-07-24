from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'shortener.views.index'),    
#    (r'^admin/(.*)', admin.site.root),    
      url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
      url(r'^admin/', include(admin.site.urls)),
#    (r'^submit/$', 'shortener.views.submit'),
    (r'^submit/ajax/$', 'shortener.views.submit__ajax', {}, 'submit-ajax'),
    (r'^(?P<base62_id>\w+)$', 'shortener.views.follow'),
#    (r'^info/(?P<base62_id>\w+)$', 'shortener.views.info', {}, 'link-info'),    

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_DOC_ROOT}),
)
