
import wx
import mainwindow


def main():
    app = wx.App()
    window = mainwindow.MainWindow()
    window.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
