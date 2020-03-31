# -*- coding: utf-8 -*-

def classFactory(iface):
    from .PostNAS_Search import PostNAS_Search
    return PostNAS_Search(iface)
