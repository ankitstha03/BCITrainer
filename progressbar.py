import time
import wx
import threading
from threading import Thread
from wx.lib.pubsub import pub


class DataThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self._stop_event = threading.Event()

    def run(self):
        for i in range(20):
            time.sleep(0.25)
            wx.CallAfter(pub.sendMessage, "update", msg="")


class ProgressBar(wx.Dialog):
    def __init__(self, label):
        wx.Dialog.__init__(self, None, title="Progress")
        download_dir = "Data.csv"
        self.label = label
        self.count = 0
        self.progress = wx.Gauge(self, range=20)
        self.SetSize((400, 28))
        self.csv = open(download_dir, "a")
        width, height = wx.DisplaySize()
        width -= 400
        height -= 28
        self.SetPosition((width, height))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)
        pub.subscribe(self.updateProgress, "update")

    def updateProgress(self, msg):
        self.count += 1
        if self.count >= 20:
            self.EndModal(0)
            print(self.label)
            string = self.label + '\n'
            self.csv.write(string)
        self.progress.SetValue(self.count)
