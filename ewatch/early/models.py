# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Country(models.Model):
    country_text = models.CharField(max_length=200)

    def __str__(self):
        return self.country_text

@python_2_unicode_compatible  # only if you need to support Python 2
class View(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    view_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.view_text
