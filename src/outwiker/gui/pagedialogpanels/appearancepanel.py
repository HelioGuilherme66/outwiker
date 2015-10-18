# -*- coding: UTF-8 -*-

import wx
import wx.combo


class AppearancePanel (wx.Panel):
    def __init__ (self, parent):
        super (AppearancePanel, self).__init__ (parent)

        self.styleText = wx.StaticText (self, -1, _("Page style"))
        self.styleCombo = wx.ComboBox (self,
                                       -1,
                                       choices=[],
                                       style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)

        self.__layout ()


    def __layout (self):
        styleSizer = wx.FlexGridSizer (1, 2, 0, 0)
        styleSizer.AddGrowableCol (1)
        styleSizer.Add (self.styleText, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        styleSizer.Add (self.styleCombo, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 4)

        self.SetSizer (styleSizer)
        self.Layout()