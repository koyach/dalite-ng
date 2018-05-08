# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.views.decorators.clickjacking import xframe_options_sameorigin


import views
import peerinst.views

admin.site.site_header = admin.site.site_title = _('Dalite NG administration')

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'admin_index_wrapper/', views.admin_index_wrapper, name='admin_index_wrapper'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lti/', include('django_lti_tool_provider.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(\
    url(r'', include('peerinst.urls')),\
    url(r'^assignment/(?P<assignment_id>[^/]+)/', include([\
        # Question table of contents for assignment - Enforce sameorigin to prevent access from LMS
        url(r'^$', xframe_options_sameorigin(peerinst.views.QuestionListView.as_view()), name='question-list'),\
        url(r'(?P<question_id>\d+)/', include([\
            # Dalite question
            url(r'^$', peerinst.views.question, name='question'),\
            # Question reset (for testing purposes) - Enforce sameorigin to prevent access from LMS
            url(r'^reset/$', peerinst.views.reset_question, name='reset-question'),
        ])),
        url(r'^update/$',peerinst.views.AssignmentUpdateView.as_view(),name='assignment-update')
    ])),)