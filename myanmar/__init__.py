# __init__.py - main module
# coding: utf-8
#
# Copyright (C) 2010, 2011 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""A Python module to parse, validate and reformat standard numbers
and codes in different formats.

"""

import json
from myanmar.converter import TlsMyanmarConverter

__CONVERTERS = {}
for jFile in  ['zawgyi.json']: #'wininnwa.json', 'wwin_burmese.json']:
    try:
        import pkgutil
        data = pkgutil.get_data(__name__, 'data/' + jFile)
    except ImportError:
        import pkg_resources
        data = pkg_resources.resource_string(__name__, 'data/' + jFile)

    data = unicode(data.decode ('utf-8'))
    __CONVERTERS[jFile[:jFile.find('.')]] = TlsMyanmarConverter (json.loads (data))
