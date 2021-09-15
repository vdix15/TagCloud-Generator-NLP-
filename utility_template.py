#-*- coding: utf-8 -*-

import wx
from wx.lib.wordwrap import wordwrap

__author__ = 'vdix_srm'

class layout_template():
    def About_info(self,name,version,cr,des,website,developers,client):
        info = wx.adv.AboutDialogInfo()
        info.Name = name
        info.Version = version
        info.Copyright = cr
        info.Description = wordwrap(des,350,client)
        info.WebSite = (website, "feedback")
        info.Developers = [developers]
        return info
