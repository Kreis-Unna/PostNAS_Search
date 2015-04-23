# -*- coding: utf-8 -*-
"""
/***************************************************************************
    PostNAS_Search
    -------------------
    Date                : April 2015
    copyright          : (C) 2015 by Kreis-Unna
    email                : marvin.brandt@kreis-unna.de
 ***************************************************************************
 *                                                                                                                                    *
 *   This program is free software; you can redistribute it and/or modify                                       *
 *   it under the terms of the GNU General Public License as published by                                      *
 *   the Free Software Foundation; either version 2 of the License, or                                          *
 *   (at your option) any later version.                                                                                    *
 *                                                                                                                                    *
 ***************************************************************************/
"""

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """
        Load PostNAS_Search class from file PostNAS_Search.
        
        :param iface: A QGIS interface instance.
        :type iface: QgsInterface
    """
    
    from .PostNAS_Search import PostNAS_Search
    return PostNAS_Search(iface)
