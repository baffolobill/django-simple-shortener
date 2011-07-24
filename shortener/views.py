import logging
from urlparse import urlparse

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django import http
from django.utils import simplejson
from django.template import RequestContext
from django.core.urlresolvers import reverse

from shortener.baseconv import base62
from shortener.models import Link, LinkSubmitForm

class JSONResponse(http.HttpResponse):
    def __init__(self, data, **kwargs):
        defaults = {
            'content_type': 'application/json',
            }
        defaults.update(kwargs)
        super(JSONResponse, self).__init__(simplejson.dumps(data), defaults)

def follow(request, base62_id):
    """ 
    View which gets the link for the given base62_id value
    and redirects to it.
    """
    key = base62.to_decimal(base62_id)
    link = get_object_or_404(Link, pk = key)
    link.usage_count += 1
    link.save()
    return http.HttpResponsePermanentRedirect(link.url)

def submit__ajax(request):
    url = None
    link_form = None
    if request.GET:
        link_form = LinkSubmitForm(request.GET)
    elif request.POST:
        link_form = LinkSubmitForm(request.POST)

    if link_form:
        if link_form.is_valid():
            url = link_form.cleaned_data['u']
            link = None
            try:
                if settings.SITE_NAME in url:
                    _u = urlparse(url)
                    link = Link.objects.get(pk=base62.to_decimal(_u.path))
                else:
                    link = Link.objects.get(url=url)
            except Link.DoesNotExist:
                pass
            if link == None:
                new_link = Link(url=url)
                new_link.save()
                link = new_link

            return JSONResponse({'url': url,
                                 'short_url': link.short_url(),
                                 'score': link.usage_count,
                                 'submitted': link.date_submitted.strftime('%b %d, %Y')})
        else:
            return JSONResponse({'error':[link_form.error_class.as_text(v) for k, v in link_form.errors.items()]})


    return JSONResponse({'error':'URL submission failed'})


def index(request):
    """
    View for main page (lists recent and popular links)
    """
    values = {'link_form':LinkSubmitForm()}
    return render_to_response('shortener/index.html',
                              values,
                              context_instance=RequestContext(request))
