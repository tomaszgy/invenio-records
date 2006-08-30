# -*- coding: utf-8 -*-
## $Id$

## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Some misc function for the external collections search.
"""

__lastupdated__ = """$Date$"""

__version__ = "$Id$"

__revision__ = "0.0.1"

from copy import copy

from invenio.dbquery import run_sql, escape_string

def get_verbose_print(req, prefix, cur_verbosity_level):
    """Return a function used to print verbose message."""

    def vprint(verbosity_level, message):
        """Print a verbose message."""
        if cur_verbosity_level >= verbosity_level:
            req.write('<br><span class="quicknote">' + prefix + message + '</span><br>')

    return vprint

def warning(message):
    """Issue a warning alert."""
    print "WARNING: %(message)s" % locals()

def escape_dictionary(dictionary):
    """Escape values of dictionary of type string with escape_string. Used for building sql query."""
    dictionary = copy(dictionary)
    for key in dictionary.keys():
        if isinstance(dictionary[key], basestring):
            dictionary[key] = escape_string(dictionary[key])
    return dictionary

# Collections function
collections_id = None

def collections_id_load(force_reload=False):
    """If needed, load the database for building the dictionnary collection_name -> collection_id."""

    global collections_id

    if not (force_reload or collections_id == None):
        return

    collections_id = {}
    results = run_sql("SELECT id, name FROM collection;")
    for result in results:
        collection_id = result[0]
        name = result[1]

        collections_id[name] = collection_id

def get_collection_id(name):
    """Return the id of a collection named 'name'."""

    collections_id_load()

    if collections_id.has_key(name):
        return collections_id[name]
    else:
        return None

def get_collection_descendants(id_dad):
    "Returns list of all descendants of the collection having for id id_dad."

    descendants = []
    results = run_sql( "SELECT id_son FROM collection_collection WHERE id_dad=%(id_dad)d;" %
        escape_dictionary({'id_dad' : id_dad}))
    for result in results:
        id_son = int(result[0])
        descendants.append(id_son)
        descendants += get_collection_descendants(id_son)

    return descendants
