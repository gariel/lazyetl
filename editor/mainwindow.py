
import wx
import wx.aui

from i18n import translate

import steps

@translate()
class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.SetSizeHints(wx.Size(800,600))
        self.create_manager()
        self.lang("mainwindow.title", self.SetTitle)
        self.SetMenuBar(self.create_menus())
        self.Layout()
        self.Centre()
        self.load_data()

    def load_data(self):
        self.tvSteps.DeleteAllItems()
        modulekeys = {c.__name__: k for k, c in steps.definition.items()}
        
        root = self.tvSteps.AddRoot("")
        for modulename in steps.__all__:
            #self.tvSteps.SetPyData(root, ('key', 'value'))
            item = self.tvSteps.AppendItem(root, "")
            langitemsetter = lambda item: lambda x: self.tvSteps.SetItemText(item, x)
            self.lang("steps.module." + modulename, langitemsetter(item), modulename)

            module = getattr(steps, modulename)
            for name in dir(module):
                if name in modulekeys.keys():
                    child = self.tvSteps.AppendItem(item, modulekeys[name])
                    

        #self.lang_set("en-us")
        self.lang_set("pt-br")

    def create_manager(self):
        self.manager = wx.aui.AuiManager()
        self.manager.SetManagedWindow(self)
        
        self.tvSteps = wx.TreeCtrl(self, style=\
              wx.TR_DEFAULT_STYLE
            | wx.TR_FULL_ROW_HIGHLIGHT
            | wx.TR_HIDE_ROOT
        )
        self.tvSteps.SetMinSize(wx.Size(200,-1))
        self.manager.AddPane(self.tvSteps, wx.aui.AuiPaneInfo()
            .Left()
            .Dock()
            .Resizable()
            .CloseButton(False) # TODO: create a menu to reopen this window
            .BottomDockable(False)
            .TopDockable(False)
            .MinSize(wx.Size(200,-1)))

        self.tabEditor = wx.aui.AuiNotebook(self)
        self.manager.AddPane(self.tabEditor, wx.aui.AuiPaneInfo()
            .Left()
            .CaptionVisible(False)
            .CloseButton(False)
            .PaneBorder(False)
            .Dock()
            .Resizable()
            .CentrePane())

        self.manager.Update()

    def create_tab(self, title):
        scrollPage = wx.ScrolledWindow(self.tabEditor, style=wx.HSCROLL|wx.VSCROLL)
        scrollPage.SetScrollRate(5, 5)
        self.tabEditor.AddPage(scrollPage, title, True)
        return scrollPage

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

        filemenu = menu("mainwindow.menu.file")
        menuitem(filemenu, wx.ID_NEW, "mainwindow.menu.file.new", None, self.OnNew)
        menuitem(filemenu, wx.ID_OPEN, "mainwindow.menu.file.open", None, self.OnOpen)
        menuitem(filemenu, wx.ID_SAVE, "mainwindow.menu.file.save", None, self.OnSave)
        menuitem(filemenu, wx.ID_SAVEAS, "mainwindow.menu.file.saveas", None, self.OnSaveAs)
        menuitem(filemenu, wx.ID_EXIT, "mainwindow.menu.file.exit", None, self.OnExit)
        return menubar

    def OnNew(self, e):
        self.create_tab("[*]")
        
    def OnOpen(self, e):
        pass

    def OnSave(self, e):
        pass

    def OnSaveAs(self, e):
        pass

    def OnExit(self, e):
        pass

    def __del__(self):
        self.manager.UnInit()
