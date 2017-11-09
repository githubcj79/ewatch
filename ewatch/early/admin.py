# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Country, View

admin.site.register(Country)
admin.site.register(View)