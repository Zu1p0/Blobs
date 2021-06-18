from tkinter import *
from random import *
from time import *
from math import sqrt

# ideas:
# - set a pause button that allow to pick a blob and see its characteristics, including drawing the visibility circle
# - set visibility indicators as variables: when it changes
# - set different colour gradient when blob is black
#
fen = Tk()
fen.title("Simulation d'une vie simplifié")
terre = Canvas(fen, bg = "green", width = 1000, height = 700)
terre.grid(column = 1, row = 0, rowspan = 3)

fdon = LabelFrame(fen, text = "Données",  width = 200, height = 200)
fdon.grid(column = 0, row = 0)

lblob = Label(fdon)
lblob.grid(column = 0, row = 0)
lgrain = Label(fdon)
lgrain.grid(column = 0, row = 1)
lmoy = Label(fdon)
lmoy.grid(column = 0, row = 2)

fcon = LabelFrame(fen, text = "Parametres",  width = 200, height = 600)
fcon.grid(column = 0, row = 1, padx = 10)

tpsc = IntVar()
tpsc.set(5)

tpsm = IntVar()
tpsm.set(300)

ryt = StringVar()
ryt.set("0.03")

Label(fcon, text = "le temps entre chaque répétition :").grid(row = 0, column = 0)
en = Entry(fcon, textvariable = ryt).grid(column = 1, row = 0)

def newblob():
    global listeblob
    listeblob.append(Blob(terre))

Label(fcon, text = " pour ajouter un nouveau blob...").grid(row = 1, column = 0)
bb = Button(fcon, text = "appuie sur ce bouton", command = newblob).grid(row = 1, column = 1)

s1 = Scale(fcon, orient='vertical', from_= 100, to = 1, resolution = 1, tickinterval = 20, length = 200, label='Le temps où un nouveau grain apparait', variable = tpsc).grid(column = 0, row = 2, columnspan = 2)
s2 = Scale(fcon, orient='vertical', from_= 300, to = 10, resolution = 1, tickinterval = 50, length = 200, label="Le temps où l'on vérifie la nourriture", variable = tpsm).grid(column = 0, row = 3, columnspan = 2)

fset = LabelFrame(fen, text = "Controles",  width = 200, height = 100)
fset.grid(column = 0, row = 2, padx = 10)

pause = False
def Change_State():
    global pause
    if pause == False:
        pause = True
    else:
        pause = False


nbgrain = 100
nbblob = 10

class Blob(object):
    def __init__(self, can, x = None, y = None, vis = 50):
        self.can = can
        self.dir = randint(1,4)      #la direction est ainsi: droite=1, haut=2, gauche=3, bas=4
        self.nour = 0
        self.tpsvie = 1
        if x == None:
            self.pos = [randint(0,int(self.can['width'])),randint(0,int(self.can['height']))]
        else:
            self.pos = [int(x),int(y)]
        self.vis = vis
        try:
            self.fig = self.can.create_oval(self.pos[0]-10,self.pos[1]-10,self.pos[0]+10,self.pos[1]+10, fill = rgbth(((255-vis*2),(255-vis*2),(255-vis*2))))
        except:
            self.fig = self.can.create_oval(self.pos[0]-10,self.pos[1]-10,self.pos[0]+10,self.pos[1]+10, fill = rgbth(((vis*2),(vis*2),(vis*2))))
            
    def destroy(self):
        self.can.delete(self.fig)

    def changenour(self, nour):
        self.nour = nour

    def addnour(self,nour):
        self.changenour(self.nour + nour)
    
    def déplace(self):
            ob = closest(self)
            if ob != False and distance(self, ob) < self.vis:
                if abs(ob.pos[0]-self.pos[0]) > abs(ob.pos[1]-self.pos[1]) :
                    if ob.pos[0]-self.pos[0] < 0:
                        self.dir = 3
                    else:
                        self.dir = 1
                else:
                    if ob.pos[1]-self.pos[1] < 0:
                        self.dir = 2
                    else:
                        self.dir = 4
            else:
                if randint(0,5) == 3:
                    self.dir = randint(1,4)
                if self.pos[0] < 10:
                    self.dir = 1
                elif self.pos[0] > int(self.can['width'])-10:
                    self.dir = 3
                elif self.pos[1] < 10:
                    self.dir = 4
                elif self.pos[1] > int(self.can['height'])-10:
                    self.dir = 2
                    
            if self.dir == 1:
                self.can.move(self.fig, 10,0)
            elif self.dir == 2:
                self.can.move(self.fig, 0,-10)
            elif self.dir == 3:
                self.can.move(self.fig, -10,0)
            else:
                    self.can.move(self.fig, 0,10)
            self.pos = [self.can.coords(self.fig)[0]+10,self.can.coords(self.fig)[1]+10]

class Grain(object):
    def __init__(self, can, colour = "blue"):
        self.can = can
        self.colour = colour
        self.pos = [randint(0,int(self.can['width'])),randint(0,int(self.can['height']))]
        self.fig = self.can.create_oval(self.pos[0]-5,self.pos[1]-5,self.pos[0]+5,self.pos[1]+5, fill = self.colour)

    def destroy(self):
        self.can.delete(self.fig)
        
def somme(liste):
    _somme = 0
    for i in liste:
        _somme = _somme + i.vis
    return _somme

def moyenne(liste):
    try:
        return somme(liste)/len(liste)
    except ZeroDivisionError:
        return 0

def bouget(liste):
    for blob in liste:
        blob.tpsvie += 1
        blob.déplace()

def rgbth(rgb):
    return '#%02x%02x%02x' % rgb

def closest(ob):
    dist = 500000000000
    ag = None
    for g in listegrain:
        d = distance(ob,g)
        if d < dist:
            dist = d
            ag = g
    if dist == 500000000000:
        return False
    else:
        return ag

def distance(ob1, ob2):
    return sqrt(((ob2.pos[0]-ob1.pos[0])*(ob2.pos[0]-ob1.pos[0]))+((ob2.pos[1]-ob1.pos[1])*(ob2.pos[1]-ob1.pos[1])))

def touche(ob1, ob2):
    if distance(ob1, ob2) < 15:
        return True
    else:
        return False

def touchet():
    global listeblob
    global listegrain
    listtb = []
    for blob in listeblob:
        #print(blob.nour)
        for grain in listegrain:
            if touche(blob, grain):
                blob.addnour(1)
                if blob.nour > 1:
                    if randint(0,5) == 2:
                        vis = blob.vis + 10
                    else:
                        vis = blob.vis
                    listtb.append(Blob(terre,blob.pos[0],blob.pos[1], vis = vis))
                    #print("un nouveau blob de parent numéro "+ str(listeblob.index(blob)))
                    blob.changenour(0)
                    blob.tpsvie = 1
                grain.destroy()
                del(listegrain[listegrain.index(grain)])
        if blob.nour > 0:
            blob.addnour(-0.1)
    for blob in listtb:
        listeblob.append(blob)

def mort():
    global listeblob
    global tpsm
    for blob in listeblob:
        if blob.nour < 0.1:
            if blob.tpsvie % tpsm.get() == 0:
                blob.destroy()
                #print("le blob numero " + str(listeblob.index(blob))+ " est mort...")
                del(listeblob[listeblob.index(blob)])

tps = 0
listeblob = []
for x in range(nbblob):
    b = Blob(terre)
    listeblob.append(b)

listegrain = []
for x in range(nbgrain):
    b = Grain(terre)
    listegrain.append(b)

while True:
        bouget(listeblob)
        touchet()
        terre.update()
        try:
            sleep(float(ryt.get()))
        except ValueError:
            sleep(0.03)
            
        tps += 1
        if tps % tpsc.get() == 0:
            listegrain.append(Grain(terre, colour = "blue"))
            #print("un nouveau grain!")
        mort()
        
        lblob.config(text = "Le nombre de blob est de : " + str(len(listeblob)))
        lgrain.config(text = "Le nombre de grain est de : " + str(len(listegrain)))
        lmoy.config(text = 'La vision moyenne est de ' + str(round(moyenne(listeblob), 1)))
