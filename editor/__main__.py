
import os
import sys
import wx

def prepare_path():
    current_dir = os.path.dirname(__file__)
    etl_dir = os.path.join(current_dir, "..", "etl")
    sys.path.insert(0, os.path.abspath(etl_dir))


class Application(wx.App):
    def __init__(self):
        super(Application, self).__init__(0)

    def OnInit(self):
        import mainwindow
        window = mainwindow.MainWindow()
        self.SetTopWindow(window)
        window.Show()
        return True

    def Run(self):
        try:
            self.MainLoop()
        except wx._core.wxAssertionError as e:
            # TODO: This error is occurring when closing the application:
            # C++ assertion "GetEventHandler() == this" failed at 
            # ..\..\src\common\wincmn.cpp(478) in wxWindowBase::~wxWindowBase(): 
            # any pushed event handlers must have been removed
            pass


def main():
    prepare_path()
    Application().Run()


if __name__ == "__main__":
    main()