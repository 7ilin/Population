from django.db import models
from django.utils.translation import ugettext_lazy as _
import json


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = _(u'Region')
        verbose_name_plural = _(u'Regions')

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    people = models.IntegerField(null=False, blank=False)
    region = models.ForeignKey(Region, related_name='cities')

    class Meta:
        verbose_name = _(u'City')
        verbose_name_plural = _(u'Cities')
        unique_together = ("name", "region",)

    def __unicode__(self):
        return u"%s->%s = %i" % (self.region.name, self.name, self.people)

    def to_json(self):
        data = {
            'name': self.name,
            'people': self.people
        }
        return data
