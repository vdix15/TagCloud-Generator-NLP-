import wx
import os
from os import path
from collections import namedtuple
import  wx.lib.rcsizer  as rcs
from wordcloud import STOPWORDS
from wx import adv
from utility_template import layout_template
import wordcloud_gen as wcg
import wx.lib.agw.gradientbutton as gbtn

__author__ = 'Vageesh-Saksham'
__mail__ = 'vd6123@srmist.edu.in'

imgformat = "jpg (*.jpg)|*.jpg|"     \
           "jpeg(*.jpeg) |*.jpeg|"\
           "png(*.png) |*.png|"\
           "tiff(*.tif) |*.tiff|"\
           "All files (*.*)|*.*"

txtformat = "txt (*.txt)|*.txt|"\
            "All files (*.*)|*.*"

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(600,-1))
        Size = namedtuple("Size",['x','y'])
        s = Size(400,100)

        self.cn_text = None
        self.en_text = None
        cwd = os.getcwd()
        self.mask_path = path.join(path.abspath(cwd),'self.choose_file')
        self.user_sw = STOPWORDS

        self.lt = layout_template()
        self.name = 'WordCloud Generator'
        
        self.des = '''Draw the word cloud.\n'''
        self.version = '1.0'
        self.website = "https://www.srmist.edu.in/"

        self.copyright = "SRMIST"
        
        """Menu bar creating"""
        filemenu = wx.Menu()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit\tCtrl+Q","Terminate the program")

        confmenu = wx.Menu()
        menuSw = confmenu.Append(wx.ID_ANY,"StopWords","Add user StopWords dictionary")
        menuMask = confmenu.Append(wx.ID_ANY,"Mask","Set mask image")
        
        helpmenu = wx.Menu ()
        menuAbout = helpmenu.Append(wx.ID_ABOUT ,"&About","Information about this program")

        menuBar = wx.MenuBar ()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(helpmenu,"&Help")
        self.SetMenuBar(menuBar)
        
        """Input box"""
        self.in1 = wx.TextCtrl(self,-1,size = (2*s.x,s.y))

        """Input buttons"""
        b1 = gbtn.GradientButton(self, -1, label = "Add TEXT")
        b2 = gbtn.GradientButton(self, -1, label = "RUN!!")
        b3 = gbtn.GradientButton(self, -1, label= "Upload image")
        b4 = gbtn.GradientButton(self, -1, label= "Add Stopwords")
        """prompt message of the input box"""
        self.in1.SetToolTip('Choose the text file')

        """GUI layouts and alignment"""
        self.sizer0 = rcs.RowColSizer()
        self.sizer0.Add(b1,row = 3,col = 1)
        self.sizer0.Add(self.in1,row = 2,col = 2)
        self.sizer0.Add(b2,row = 3,col = 3)
        self.sizer0.Add(b3,row = 6,col = 2)
        self.sizer0.Add(b4,row = 6,col = 3)
        """Binding callback functions"""
        self.Bind(wx.EVT_BUTTON, self.choose_cn, b1)
        self.Bind(wx.EVT_BUTTON, self.draw_cn, b2)
        self.Bind(wx.EVT_BUTTON, self.get_mask, b3)
        self.Bind(wx.EVT_BUTTON, self.get_stopwords, b4)

        '''Menu binding functions'''
        self.Bind(wx.EVT_MENU,self.OnExit,menuExit)
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)
        
        self.Bind(wx.EVT_MENU,self.get_stopwords,menuSw)
        self.Bind(wx.EVT_MENU,self.get_mask,menuMask)
        
        self.SetSizer(self.sizer0)
        self.SetAutoLayout(1)
        self.sizer0.Fit(self)
        self.CreateStatusBar()
        self.Show(True)

    def get_stopwords(self,evt):
        fn = self.choose_file(txtformat)
        if fn is None:
            return None
        else:
            self.user_sw = wcg.user_stopwords(fn)

    def get_mask(self,evt):
        temp = self.choose_file(imgformat)
        if temp is not None:
            self.mask_path = temp

    def choose_cn(self,evt):
        """Choose a cn text file"""
        self.cn_text = None
        self.cn_text = self.choose_file(txtformat)
        if self.cn_text is None:
            pass
        else:
            self.in1.Clear()
            self.in1.write(self.cn_text)
            
    def choose_file(self,wildcard):
        '''choose img'''
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            dlg.Destroy()
            return paths[0]
        else:
            return None

    def draw_cn(self,evt):
        if self.cn_text is None:
            self.raise_msg(u'please Choose a text file first.')
            return None
        else:
            text = wcg.get_text_cn(self.cn_text)
            wcg.draw_wc(text,self.mask_path,self.user_sw)

    def raise_msg(self,msg):
        '''add the warning message'''
        info = adv.AboutDialogInfo()
        info.Name = "Warning Message"
        info.Copyright = msg
        wx.AboutBox(info)

    def OnAbout(self, evt):
        info = self.lt.About_info(self.name,self.version,self.copyright,
                                  self.des,self.website,
                                  __author__+'\n'+__mail__,wx.ClientDC(self))   
        adv.AboutBox(info)
        
    def OnExit(self,event):
        """exit funct"""
        self.Close()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None,'WordCloud_draw')
    app.MainLoop()
    
