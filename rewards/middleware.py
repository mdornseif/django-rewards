#!/usr/bin/env python
# encoding: utf-8
"""
middleware.py

created by Maximillian Dornseif on 2009-02-07.
Copyright (c) 2009, 2010 HUDORA. All rights reserved.
"""

from rewards.models import Campaign, Inflow
import re

# get_ip is from http://code.google.com/p/django-tracking/source/browse/tracking/utils.py
# this is not intended to be an all-knowing IP address regex
IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.
    """

    # if neither header contain a value, just use local loopback
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR',
                                  request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip_address:
        # make sure we have one and only one IP
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
            else:
                # no IP, probably from some dirty proxy or other device
                # throw in some bogus IP
                ip_address = '10.0.0.1'
        except IndexError:
            pass

    return ip_address


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

        # create some useful variables
        ip_address = get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        referer = request.META.get('HTTP_REFERER', '')[:255]
        campaign.inflow_set.create(ip_address=ip_address, user_agent=user_agent, referer=referer)
    
