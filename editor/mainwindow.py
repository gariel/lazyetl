
import wx
from i18n import translate

@translate("mainwindow")
class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.lang("title", self.SetTitle)
        self.Centre()
        self.SetMenuBar(self.create_menus())
        self.panel = wx.Panel(self)
        self.lang_set("en-us")

    def create_menus(self):
        menubar = wx.MenuBar()
        def menu(tkey):
            m = wx.Menu()
            menubar.Append(m, tkey)
            nmenu = menubar.GetMenuCount()-1
            self.lang(tkey, lambda t: menubar.SetMenuLabel(nmenu, t))
            return m

        def menuitem(menu, icon, tname, tdesc, action):
            mitem = menu.Append(icon, tname, tdesc)
            self.lang(tname, mitem.SetText)
            self.lang(tdesc, mitem.SetHelp)
            self.Bind(wx.EVT_MENU, action, mitem)

        filemenu = menu("menu.file")
        menuitem(filemenu, wx.ID_NEW, "menu.file.new", None, self.OnNew)
        menuitem(filemenu, wx.ID_OPEN, "menu.file.open", None, self.OnOpen)
        menuitem(filemenu, wx.ID_SAVE, "menu.file.save", None, self.OnSave)
        menuitem(filemenu, wx.ID_SAVEAS, "menu.file.saveas", None, self.OnSaveAs)
        menuitem(filemenu, wx.ID_EXIT, "menu.file.exit", None, self.OnExit)
        return menubar

    def OnNew(self, e):
        pass
        
    def OnOpen(self, e):
        pass

    def OnSave(self, e):
        pass

    def OnSaveAs(self, e):
        pass

    def OnExit(self, e):
        pass
