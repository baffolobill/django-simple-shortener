from django.contrib import admin

from shortener.models import Link

class LinkAdmin(admin.ModelAdmin):
    model = Link
    extra = 3

admin.site.register(Link, LinkAdmin)
