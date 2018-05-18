import wx
import random
import progressbar as bar


class TrainerApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.SetAppDisplayName('Trainer')
        self.frame = wx.Frame(None, title='Trainer Control')
        self.panel = wx.Panel(self.frame)
        self.createWidgets()
        self.PhotoMaxSize = 1000
        self.frame.Show()
        self.counter = 0

    def createWidgets(self):
        image = wx.EmptyImage(1000, 1000)
        self.imageBitmap = (wx.StaticBitmap(self.panel, wx.ID_ANY,
                                            wx.Bitmap(image)))
        self.btn = wx.Button(self.panel, label='Start')
        self.btn.Bind(wx.EVT_BUTTON, self.slideShow)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(
            self.imageBitmap,
            50,
            wx.EXPAND,
        )
        self.hsizer.Add(self.btn, 0, wx.ALL, 5)
        self.sizer.Add(self.hsizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self.frame)

    def slideShow(self, event):
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.btn.Hide()
        self.timer.Start(0)
        self.Bind(wx.EVT_TIMER, self.onNext)

    def onNext(self, event):
        t = random.randrange(1, 5, 1)
        print(t)
        image = wx.Image("image_{a}.png".format(a=str(t)), wx.BITMAP_TYPE_ANY)
        W = image.GetWidth()
        H = image.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        image = image.Scale(NewW, NewH)
        self.imageBitmap.SetBitmap(wx.Bitmap(image))
        self.panel.Refresh()
        thread = bar.DataThread()
        width, height = wx.DisplaySize()
        width -= 400
        height -= 28
        dlg = bar.ProgressBar(str(t))
        dlg.SetPosition((1520, 996))
        dlg.ShowModal()
        dlg.Destroy()
        print(dlg.GetPosition())
        if not thread.is_alive():
            self.counter += 1

        if self.counter == 9:
            self.counter = 0
            print("dead")
            self.timer.Stop()
            self.btn.Show()


if __name__ == "__main__":
    app = TrainerApp()
    app.MainLoop()
