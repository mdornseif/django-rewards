#!/usr/bin/env python
# encoding: utf-8
"""
middleware.py

created by Maximillian Dornseif on 2009-02-07.
Copyright (c) 2009, 2010 HUDORA. All rights reserved.
"""

from rewards.models import Campaign, Inflow
from rewards.tools import get_ip

class RewardsMiddleware(object):
    
    def process_request(self, request):
        if not hasattr(request, 'session'):
            raise RuntimeError('No session information! Do you use SessionMiddleware'
                               ' and have it loaded before RewardsMiddleware?')

        # don't process AJAX requests
        if request.is_ajax():
            return
        # only process GET requests with an 'aff' parameter
        if (request.method != 'GET') or ('aff' not in request.GET):
            return
        
        session_key = request.session.session_key
        campagin_designator = request.GET['aff']
        campaigns = Campaign.objects.filter(designator__iexact=campagin_designator)
        if not len(campaigns):
            # invalid Campaign
            return
        
        campaign = campaigns[0]
        request.session['campaign'] = campaign.designator
        # register inflow
        ip_address = get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        referer = request.META.get('HTTP_REFERER', '')[:255]
        Inflow.objects.create(campaign_designator=campaign.designator, ip_address=ip_address,
                              user_agent=user_agent, referer=referer)
        return
