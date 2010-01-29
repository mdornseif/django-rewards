# -*- coding: utf-8 -*-
"""
Models for django-rewards.

Created by Maximillian Dornseif on 2010-01-26.
Copyright (c) 2010  Maximillian Dornseif. All rights reserved.
"""

import base64
import hashlib
import random
import time
from django.db import models
from rewards.tools import get_ip


CONVERSION_STATUS_CHOICES = (('created', 'created'), ('processed', 'processed'),
                             ('finished', 'finished'), ('canceled', 'canceled'))

class Campaign(models.Model):
    designator = models.CharField(max_length=28, null=True, blank=True, editable=False,
                                  unique=True, db_index=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        """Additional imformation for the ORM."""
        get_latest_by = 'created_at'
        ordering = ['-created_at']
    
    def __unicode__(self):
        """Return a Unicode/String representation of the Object."""
        return u"Campaign %s" % (self.designator)
    

def campaign_post_save(signal, sender, instance, **kwargs):
    """Generate a designator"""
    if not instance.designator:
        chash = hashlib.md5("%f-%f-%d" % (random.random(), time.time(), instance.id))
        instance.designator = "dc%s" % base64.b32encode(chash.digest()).rstrip('=')
        instance.save()


models.signals.post_save.connect(campaign_post_save, Campaign)


class Inflow(models.Model):
    # this has the potential to get an ugly DB bottleneck, so we vo not use something which enforces
    # referential intigrity, like
    # campaign = models.ForeignKey(Campaign, to_field='designator')
    # but instead:
    campaign_designator = models.CharField(max_length=28, db_index=True)
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=255)
    referer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class Conversion(models.Model):
    campaign = models.ForeignKey(Campaign, to_field='designator')
    value = models.IntegerField(blank=True, null=True)
    reference = models.CharField(max_length=64, blank=True, default='', db_index=True)
    text = models.CharField(max_length=255)
    ip_address = models.IPAddressField()
    user_agent = models.CharField(max_length=255)
    referer = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=CONVERSION_STATUS_CHOICES,
                              default=CONVERSION_STATUS_CHOICES[0][0])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)



    
    