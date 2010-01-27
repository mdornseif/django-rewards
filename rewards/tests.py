#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Maximillian Dornseif on 2010-01-27.
Copyright (c) 2010 HUDORA. All rights reserved.
"""

from django.test import TestCase
from django.http import HttpRequest
from django.middleware.common import CommonMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings
from rewards.middleware import RewardsMiddleware

class RewardsMiddlewareTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get_request(self, path, query_string=''):
        request = HttpRequest()
        request.method = 'GET'
        request.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
            'QUERY_STRING': query_string,
        }
        request.path = request.path_info = "/middleware/%s" % path
        SessionMiddleware().process_request(request)
        return request

    def test_require_session_middleware(self):
        """Tests that sessions middlewares existence are enforced."""
        request = self._get_request('foo')
        del(request.session) # act as no session middleware would be loaded
        self.assertRaises(RuntimeError, RewardsMiddleware().process_request, request)

    def test_no_campaign_registered(self):
        """
        Tests that no Campagin gets written into the session if there is no ?aff= parameter.
        """
        request = self._get_request('foo')
        RewardsMiddleware().process_request(request)
        self.assertEquals(request.session.get('campaign', None), None)

    def test_invalid_parameter(self):
        """
        Tests that no Campagin gets written into the session if there is an invalid ?aff= parameter.
        """
        request = self._get_request('foo', 'aff=GIBBETNICH')
        RewardsMiddleware().process_request(request)
        self.assertEquals(request.session.get('campaign', None), None)

    def test_campain_with_valid_parameter(self):
        """
        Tests that Campagin gets written into the session.
        """
        request = self._get_request('foo', 'aff=dcTESTESTESTESTESTESTESTESTE')
        RewardsMiddleware().process_request(request)
        self.assertEquals(request.session.get('campaign', None), None)

    def test_post_ignored(self):
        """
        Tests that no Campagin gets written into the session if the request was a POST request.
        """
        request = self._get_request('foo', 'aff=dcTESTESTESTESTESTESTESTESTE')
        request.method = 'POST'
        RewardsMiddleware().process_request(request)
        self.assertEquals(request.session.get('campaign', None), None)
