from tkinter import *
from zermeloapi import Zapi
import time, datetime, re, os, sys
from functools import partial
class Example:
    def __init__(self, root):
        self.colordict = {
        'exam' : 'light goldenrod',
        'lesson' : 'steel blue',
        'activity' : 'pale green'
        }
        self.week = 1
        self.user = '~me'
        self.root = root
        self.canvas = Canvas(self.root, borderwidth=0, height=700, width=648)
        self.frame = Frame(self.canvas)



        self.framepie= Frame(self.root, height=26)
        self.framepie.pack(side='bottom', fill='x')
        Button(self.framepie, text='←', command=partial(self.killall, -1)).place(relx=0.45, rely=0.5, anchor=CENTER)
        Button(self.framepie, text='→', command=partial(self.killall, 1)).place(relx=0.55, rely=0.5, anchor=CENTER)
        Button(self.framepie, text='users', command=partial(self.main2)).place(relx=0.03, rely=0.5, anchor=CENTER)
        self.label1 = Label(self.framepie, text='')
        self.label1.place(relx=0.97, rely=0.5, anchor=CENTER)


        self.vsb = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.populate()
#        self.main()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def populate(self):

        min10 = 25
        zermelo = Zapi()
        if not self.user == '~me':
            self.label1.configure(text=self.user)
        else:
            self.label1.configure(text='')
        self.weekschedule = zermelo.schedule_week(weeks = self.week, user=self.user)
        self.weekschedule
        self.startlist = []
        for i in self.weekschedule:
            self.startlist.append(i['start'])
        self.weekschedule= sorted(self.weekschedule, key = lambda x: self.startlist[self.weekschedule.index(x)])
        daysofweek = [[],[],[],[],[]]
        self.daylist = []
        for i in range(5):
            self.daylist.append(Frame(self.frame, width = 130, height=500))
            self.daylist[i].pack(side='left', anchor='nw', fill='y')
        for i in self.weekschedule:
            if not i['moved']:
                if i['valid']:
                    timelesson = time.localtime(i['start'])
        #            print(i['start'], timelesson.tm_year, timelesson.tm_mon, timelesson.tm_mday, str(timelesson.tm_hour) + ':' + str(timelesson.tm_min), 'start')
                    daysofweek[datetime.datetime(timelesson.tm_year, timelesson.tm_mon, timelesson.tm_mday).weekday()].append(i)
#            timelesson = time.localtime(i['end'])
#            print(i['end'], timelesson.tm_year, timelesson.tm_mon, timelesson.tm_mday, str(timelesson.tm_hour) + ':' + str(timelesson.tm_min), 'end')
        #print(daysofweek)
        FMT = '%H,%M'
        for counter, i in enumerate(daysofweek):
            for counter2, x in enumerate(i):
                if counter2 == 0:
                    starttime = '8,00'
                    comparison = f"{time.localtime(x['start']).tm_hour},{time.localtime(x['start']).tm_min}"
                else:
                    comparison = f"{time.localtime(x['start']).tm_hour},{time.localtime(x['start']).tm_min}"
                    starttime = f"{time.localtime(i[counter2-1]['end']).tm_hour},{time.localtime(i[counter2-1]['end']).tm_min}"

                frameheight = (datetime.datetime.strptime(comparison, FMT) - datetime.datetime.strptime(starttime, FMT)).seconds/60
                frameheight *= 1.62
                if not frameheight == 0:
                    frame1 = Frame(self.daylist[counter],width = 130, height=frameheight).pack(side='top',anchor='w')

                if x['cancelled']:
                    backgroundcolor = 'sienna1'
                else:
                    backgroundcolor = self.colordict[x['type']]
                FMT = '%H,%M'
                comparison = f"{time.localtime(x['start']).tm_hour},{time.localtime(x['start']).tm_min}"
                starttime = f"{time.localtime(x['end']).tm_hour},{time.localtime(x['end']).tm_min}"
                buttonheight = (datetime.datetime.strptime(starttime, FMT) - datetime.datetime.strptime(comparison, FMT)).seconds/600

                Button(self.daylist[counter], text=f'''{', '.join([i for i in x["subjects"]])}\n{', '.join([i for i in x["teachers"]])}\n{', '.join([i for i in x["locations"]])}\n{time.localtime(x['start']).tm_hour}:{time.localtime(x['start']).tm_min}-{time.localtime(x['end']).tm_hour}:{time.localtime(x['end']).tm_min}''', font=(NORMAL, 8), width=20,height=int(buttonheight),anchor='center', bg= backgroundcolor).pack(side='top',anchor='w')

    def killall(self, number):
        self.week += number
        for i in self.daylist:
            i.destroy()
        self.populate()





    def main2(self):
        self.root2 = Tk()
        self.root2.bind('<Return>',self.search)
        self.canvas2 = Canvas(self.root2, borderwidth=0, background="#ffffff", width=200)
        self.frame2 = Frame(self.canvas2, background="#ffffff")

        self.framepie2= Frame(self.root2)
        self.framepie2.pack(side='bottom', fill='x')
        self.entry1 = Entry(self.framepie2, text= 'Turn all on', width = 13)
        self.entry1.pack(side='left', anchor='sw')
        self.entry1.focus()
        search = Button(self.framepie2, text= 'search', command=self.search)
        search.pack(side='left', anchor='sw')
        Button(self.framepie2, text='Own schedule', command=partial(self.get_code, '~me')).pack(side='left', anchor='sw')

        self.vsb2 = Scrollbar(self.root2, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=self.vsb2.set)

        self.vsb2.pack(side="right", fill="y")
        self.canvas2.pack(side="left", fill="both", expand=True)
        self.canvas2.create_window((4,4), window=self.frame2, anchor="nw",
                                  tags="self.frame2")
        self.frame2.bind("<Configure>", self.onFrameConfigure2)
        self.populate2()
#        self.main()
        self.canvas2.bind_all("<MouseWheel>", self._on_mousewheel2)

    def _on_mousewheel2(self, event):
        self.canvas2.yview_scroll(int(-2*(event.delta/120)), "units")


    def search(self,event=None):
        new = [i for i in self.userlist if re.match(r'[\w\W]{0,}' +self.entry1.get() + r'[\w\W]{0,}', i, re.IGNORECASE)]
#        new.extend([i['firstName'] + ' ' + i['prefix'] + ' ' + i['lastName'] if i['prefix'] else i['firstName'] + ' ' + i['lastName']  for i in self.users if re.match('^'+ self.entry1.get() + r'[\w\W]{0,}', i['lastName'], re.IGNORECASE)])
        new = list(dict.fromkeys(new))
        for i in self.buttonlist:
            i.destroy()
        self.names(new)
    def get_code(self, counter):
        if not counter == "~me":
            result = re.search(r'\(([0-9]{6})\)',self.secondary[counter])
            self.user = result.group(1)
        else:
            self.user = '~me'
        for i in self.daylist:
            i.destroy()
        self.populate()
        self.root2.destroy()
    def names(self, secondary):
        self.buttonlist = []
#        print(self.userlist)
        secondary.sort()
        self.secondary = secondary
        for counter, i in enumerate(secondary):
            self.buttonlist.append(Button(self.frame2, text=i, command=partial(self.get_code, counter)))
            self.buttonlist[counter].grid(column=0, row=counter, sticky='w')

    def populate2(self):


        zermelo2 = Zapi()
        self.users = zermelo2.get_users()
#        self.entry2 = Entry(self.root)
#        self.entry2.pack(side='top')
        self.userlist = [i['firstName'] + ' ' + i['prefix'] + ' ' + i['lastName'] + ' ('+ i['code'] + ')' if i['prefix'] else i['firstName'] + ' ' + i['lastName'] + ' ('+ i['code'] + ')' for i in self.users]
        first = self.userlist
        self.names(first)


    def onFrameConfigure2(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#        self.entry2 = Entry(self.root)
#        self.entry2.pack(side='top')
class koppelen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x270")
        self.root.resizable(0,0)
        self.root.bind('<Return>', self.done)
        self.buttons()
    def buttons(self):
        self.entry1 = Entry(self.root, width=30)
        self.entry2 = Entry(self.root, width=30)
        label1 = Label(self.root, text='School:')
        label2 = Label(self.root, text='Koppelcode:')
        button1 = Button(self.root, text='Done',command=self.done)
        self.entry1.place(relx=0.5,rely=0.45,anchor=CENTER)
        self.entry2.place(relx=0.5,rely=0.55, anchor=CENTER)
        label1.place(relx=0.172,rely=0.45,anchor=CENTER)
        label2.place(relx=0.2,rely=0.55, anchor=CENTER)
        button1.place(relx=0.96,rely=0.95, anchor=CENTER)
    def done(self, event=None):
        print(self.entry1.get(), self.entry2.get())
        tempZer = Zapi(school=self.entry1.get(), token=self.entry2.get())
        del tempZer
        self.root.destroy()
        maingui()
def maingui():
    root=Tk()
    root.title('Rooster')
    gui = Example(root)
    gui.root.mainloop()
def koppelgui():
    root = Tk()
    root.title('Koppel app')
    gui1 = koppelen(root)
    gui1.root.mainloop()

if os.path.isfile('token.json'):
    maingui()
else:
    koppelgui()
