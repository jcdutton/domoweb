#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Module purpose
==============

Django web UI views

Implements
==========


@author: Domogik project
@copyright: (C) 2007-2010 Domogik project
@license: GPL(v3)
@organization: Domogik
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings
from domoweb.utils import *
from domoweb.rinor.pipes import *

from django_pipes.exceptions import ResourceNotAvailableException
from httplib import BadStatusLine

@rinor_isconfigured
def login(request):
    """
    Login process
    @param request : HTTP request
    @return an HttpResponse object
    """
    next = request.GET.get('next', '')

    page_title = _("Login page")
    page_messages = []
    if request.method == 'POST':
        return _auth(request, next)
    else:
        try:
            users = UserPipe().get_list()
        except BadStatusLine:
            return redirect("error_badstatusline_view")
        except ResourceNotAvailableException:
            return redirect("error_resourcenotavailable_view")
        return go_to_page(
            request, 'login.html',
            page_title,
            page_messages,
            next=next,
            account_list=users
        )

def logout(request):
    """
    Logout process
    @param request: HTTP request
    @return an HttpResponse object
    """
    request.session.clear()
    return HttpResponseRedirect('/')

@rinor_isconfigured
def _auth(request, next):
    # An action was submitted => login action
    user_login = request.POST.get("login",'')
    user_password = request.POST.get("password",'')
    try:
        account = UserPipe().get_auth(user_login, user_password)
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")
    if account:
        request.session['user'] = {
            'login': account.login,
            'is_admin': (account.is_admin == "True"),
            'first_name': account.person.first_name,
            'last_name': account.person.last_name,
            'skin_used': account.skin_used
        }
        if next != '':
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/view/')
    else:
        # User not found, ask again to log in
        error_msg = ugettext(u"Sorry unable to log in. Please check login name / password and try again.")
        return HttpResponseRedirect('/admin/login/?status=error&msg=%s' % error_msg)

@rinor_isconfigured
@admin_required
def admin_management_accounts(request):
    """
    Method called when the admin accounts page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """
    
    page_title = _("Accounts management")
    page_messages = []
    try:
        users = UserPipe().get_list()
        people = PersonPipe().get_list()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")
    return go_to_page(
        request, 'management/accounts.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_management_accounts = "selected",
        accounts_list=users,
        people_list=people
    )

@rinor_isconfigured
@admin_required
def admin_organization_devices(request):
    """
    Method called when the admin devices organization page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Devices organization")
    page_messages = []

    id = request.GET.get('id', 0)
    try:
        devices = DeviceExtendedPipe().get_list()
        usages = DeviceUsagePipe().get_list()
        types = DeviceTypePipe().get_list()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return go_to_page(
        request, 'organization/devices.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_organization_devices = "selected",
        id=id,
        devices_list=devices,
        usages_list=usages,
        types_list=types
    )

@rinor_isconfigured
@admin_required
def admin_organization_rooms(request):
    """
    Method called when the admin rooms organization page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Rooms organization")
    page_messages = []

    id = request.GET.get('id', 0)
    try:
        rooms = RoomExtendedPipe().get_list()
        house_rooms = RoomExtendedPipe().get_list_noarea()
        areas = AreaExtendedPipe().get_list()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return go_to_page(
        request, 'organization/rooms.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_organization_rooms = "selected",
        id=id,
        rooms_list=rooms,
        house_rooms=house_rooms,
        areas_list=areas
    )

@rinor_isconfigured
@admin_required
def admin_organization_areas(request):
    """
    Method called when the admin areas organization page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Areas organization")
    page_messages = []

    id = request.GET.get('id', 0)
    try:
        areas = AreaExtendedPipe().get_list()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return go_to_page(
        request, 'organization/areas.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_organization_areas = "selected",
        id=id,
        areas_list=areas
    )

@rinor_isconfigured
@admin_required
def admin_organization_house(request):
    """
    Method called when the admin house organization page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """
    
    page_title = _("House organization")
    page_messages = []

    try:
        house = UiConfigPipe().get_filtered(name='house')[0]
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return go_to_page(
        request, 'organization/house.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_organization_house = "selected",
        house_name=house.value
    )

@rinor_isconfigured
@admin_required
def admin_organization_widgets(request):
    """
    Method called when the admin widgets organization page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Widgets organization")
    page_messages = []

    try:
        rooms = RoomExtendedPipe().get_list()
        areas = AreaExtendedPipe().get_list()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return go_to_page(
        request, 'organization/widgets.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_organization_widgets = "selected",
        areas_list=areas,
        rooms_list=rooms
    )

@rinor_isconfigured
@admin_required
def admin_plugins_plugin(request, plugin_host, plugin_name, plugin_type):
    """
    Method called when the admin plugin command page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_messages = []

    try:
        plugin = PluginPipe().get_detail(plugin_host, plugin_name)
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")
    if plugin_type == "plugin":
        page_title = _("Plugin")
        return go_to_page(
            request, 'plugins/plugin.html',
            page_title,
            page_messages,
            nav1_admin = "selected",
            nav2_plugins_plugin = "selected",
            plugin=plugin
        )
    if plugin_type == "hardware":
        page_title = _("Hardware")
        return go_to_page(
            request, 'plugins/hardware.html',
            page_title,
            page_messages,
            nav1_admin = "selected",
            nav2_plugins_plugin = "selected",
            plugin=plugin
        )

@rinor_isconfigured
@admin_required
def admin_tools_helpers(request):
    """
    Method called when the admin helpers tool page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Helpers tools")
    page_messages = []

    return go_to_page(
        request, 'tools/helpers.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_tools_helpers = "selected",
    )

@rinor_isconfigured
@admin_required
def admin_tools_rinor(request):
    """
    Method called when the admin rest page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("RINOR informations")
    page_messages = []

    try:
        info = InfoPipe().get_info()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")
    return go_to_page(
        request, 'tools/rinor.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_tools_rinor = "selected",
        rinor=info
    )

@rinor_isconfigured
@admin_required
def admin_packages_repositories(request):
    """
    Method called when the admin repositories page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Packages repositories")
    page_messages = []
    
    try:
        repositories = RepositoryPipe().get_list()
#        if (repositories_result.status == 'OK'):
#            repositories=repositories_result.repository
#        else:
#            repositories=None
#            page_messages.append({'status':'error', 'msg':repositories_result.description})
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")
    return go_to_page(
        request, 'packages/repositories.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_packages_repositories = "selected",
        repositories=repositories
    )

@rinor_isconfigured
@admin_required
def admin_packages_plugins(request):
    """
    Method called when the admin plugins page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Plugins packages")
    page_messages = []
    try:
        packages = PackageExtendedPipe().get_list_plugin()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")
    
    return go_to_page(
        request, 'packages/plugins.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_packages_plugins = "selected",
        packages=packages
    )

@rinor_isconfigured
@admin_required
def admin_packages_hardwares(request):
    """
    Method called when the admin hardwares page is accessed
    @param request : HTTP request
    @return an HttpResponse object
    """

    page_title = _("Hardwares packages")
    page_messages = []
    try:
        packages = PackageExtendedPipe().get_list_external()
        rinor = InfoPipe().get_info()
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return go_to_page(
        request, 'packages/hardwares.html',
        page_title,
        page_messages,
        nav1_admin = "selected",
        nav2_packages_hardwares = "selected",
        packages=packages,
        host=rinor.info.Host
    )

@rinor_isconfigured
@admin_required
def admin_packages_install(request, package_host, package_name, package_release):
    """
    Method called for installing a package
    @param request : HTTP request
    @return an HttpResponse object
    """
    try:
        PackagePipe.put_install(package_host, package_name, package_release)
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return redirect('admin_packages_plugins_view')

@rinor_isconfigured
@admin_required
def admin_packages_enable(request, package_host, package_name, action):
    """
    Method called for installing a package
    @param request : HTTP request
    @return an HttpResponse object
    """
    try:
        PluginPipe.command_detail(package_host, package_name, action)
    except BadStatusLine:
        return redirect("error_badstatusline_view")
    except ResourceNotAvailableException:
        return redirect("error_resourcenotavailable_view")

    return redirect('admin_packages_plugins_view')