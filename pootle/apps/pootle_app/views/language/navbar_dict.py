#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2012 Zuza Software Foundation
#
# This file is part of Pootle.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Helper methods for the navigation bar."""

from pootle.i18n.gettext import tr_lang
from pootle_app.views.language import dispatch, item_dict
from pootle_misc import url_manip


def make_directory_pathlinks(project_url, url, links):
    if url != project_url:
        links.append({'href': url,
                      'text': url_manip.basename(url)})
        return make_directory_pathlinks(project_url, url_manip.parent(url), links)
    else:
        return list(reversed(links))

def make_navbar_path_dict(request, path_links=None):
    language = request.translation_project.language
    project = request.translation_project.project
    return {
        'language':  {'href': dispatch.open_language(language.code),
                      'text': tr_lang(language.fullname)},
        'project':   {'href': dispatch.open_translation_project(language.code, project.code),
                      'text': project.fullname},
        'pathlinks': path_links}

def make_directory_navbar_dict(request, directory, terminology=False):
    result = item_dict.make_directory_item(request, directory, terminology)
    project_url = request.translation_project.directory.pootle_path
    path_links = make_directory_pathlinks(project_url, directory.pootle_path, [])

    result.update({'path': make_navbar_path_dict(request, path_links)})
    del result['title']
    return result
