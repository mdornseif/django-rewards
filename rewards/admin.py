# -*- coding: utf-8 -*-
"""
Admin configuration for for django-rewards.

Created by Maximillian Dornseif on 2010-01-26.
Copyright (c) 2010  Maximillian Dornseif. All rights reserved.
"""

### SAMPLE CODE FOLLOWS

from django.contrib import admin
from rewards.models import Campaign, Inflow

class CampaignAdmin(admin.ModelAdmin):
    """Configuration of the Django Admin Interface."""
    date_hierarchy = 'created_at'
    #list_display = ('pk', 'liefer_name1', 'bestelldatum')
    #list_filter = ('status', 'kundennr')
    #search_fields = ('guid', 'kundenauftragsnr', 'auftragsnr')
    #save_on_top = True
    #raw_id_fields = ('verladung', )
    

class InflowAdmin(admin.ModelAdmin):
    """Configuration of the Django Admin Interface."""
    date_hierarchy = 'created_at'
    raw_id_fields = ('campaign', )
    

# register admin classes
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Inflow, InflowAdmin)
