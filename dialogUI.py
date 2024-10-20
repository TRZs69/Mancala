from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread
import random
from gameController import gameWithGUI
from minimaxAgent import minimaxAgent
import pygame

leftUp=[(161,110),(161,190),(161,266),(161,350),(161,429),(161,506),(17,592),(17,506),(17,429),(17,350),(17,266),(17,190),(17,110),(17,35)]
width=65
height1=208
height2=90

class myThread(QThread):
    def __init__(self, game, action):
        super().__init__()
        self.game = game
        self.action = action

    def run(self):
        if self.action == -1:
            self.game.play()
        else:
            self.game.manPlay(self.action)

class newLabel(QtWidgets.QLabel):
    def __init__(self,Dialog,UI,id):
        super().__init__(Dialog)
        self.parentUI=UI
        self.enable=False
        self.id=id

    def enableAction(self,enable):
        self.enable=enable

    def mousePressEvent(self, event):
        if self.enable:
            if event.buttons () == QtCore.Qt.LeftButton:
                self.parentUI.play(self.id)
                    
class Ui_Dialog(object):
    def setupUi(self, Dialog):       
        pygame.mixer.init()
        
        self.bgm = pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play()

        self.buttonClickSound = pygame.mixer.Sound("click.wav")
        self.buttonClickSound.set_volume(0.75)
        
        #Main Window
        Dialog.setObjectName("Dialog")
        Dialog.resize(1064, 355)
        Dialog.setMinimumSize(QtCore.QSize(1064, 355))
        Dialog.setMaximumSize(QtCore.QSize(1064, 355))
        
        #Icon Set
        icon = QtGui.QIcon("mancala.png")  
        Dialog.setWindowIcon(icon)
        
        #Win Label
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(380, 30, 658, 300))
        self.label.setObjectName("label")
        self.winningLabel = QtWidgets.QLabel(Dialog)
        self.winningLabel.setGeometry(QtCore.QRect(565, 130, 300, 100))
        self.winningLabel.setObjectName("winningLabel")
        
        #Start P1
        self.startP1 = QtWidgets.QPushButton(Dialog)
        self.startP1.setGeometry(QtCore.QRect(10, 20, 181, 61))
        self.startP1.setObjectName("startP1")
        
        #Start P2
        self.startP2 = QtWidgets.QPushButton(Dialog)
        self.startP2.setGeometry(QtCore.QRect(190, 20, 181, 61))
        self.startP2.setObjectName("startP2")
        
        #Start AI vs AI
        self.AIvsAI = QtWidgets.QPushButton(Dialog)
        self.AIvsAI.setGeometry(QtCore.QRect(100, 200, 181, 61))
        self.AIvsAI.setObjectName("startAIvsAI")
        
        #Restart game
        self.reset = QtWidgets.QPushButton(Dialog)
        self.reset.setGeometry(QtCore.QRect(100, 270, 181, 61))
        self.reset.setObjectName("resetButton")
        
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 80, 181, 80))
        self.groupBox.setObjectName("groupBox")
        
        #GB P1
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup.setObjectName("buttonGroup")
        
        #MinimaxP1
        self.P1minimax = QtWidgets.QRadioButton(self.groupBox)
        self.P1minimax.setGeometry(QtCore.QRect(20, 30, 100, 20))
        self.P1minimax.setChecked(True)
        self.P1minimax.setObjectName("P1minimax")
        self.buttonGroup.addButton(self.P1minimax)
        
        #GB P2
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(190, 80, 181, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        
        #MinimaxP2
        self.P1minimax_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.P1minimax_2.setGeometry(QtCore.QRect(20, 30, 100, 20))
        self.P1minimax_2.setChecked(True)
        self.P1minimax_2.setObjectName("P1minimax_2")
        self.buttonGroup_2.addButton(self.P1minimax_2)

        #Options Handling
        self.AIvsAI.clicked.connect(self.versus)
        self.AIvsAI.clicked.connect(self.playClickSound)
        
        self.startP1.clicked.connect(self.p1Start)
        self.startP1.clicked.connect(self.playClickSound)
        
        self.startP2.clicked.connect(self.p2Start)
        self.startP2.clicked.connect(self.playClickSound)
        
        self.reset.clicked.connect(self.playClickSound)
        self.reset.clicked.connect(self.resetGame)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        plate = QtGui.QPixmap("wadah.png").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(plate)

        self.winningLabel.hide()
        self.winningLabel.setStyleSheet("font: bold; font-size:48px; color: rgb(255, 0, 0)")
        self.numLabels=[]

        self.cmdG=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.cmds=[]
        for j in range(14):
            if (j==6) or (j==13):
                continue
            for i in range(4):
                label2 = QtWidgets.QLabel(Dialog)
                label2.setGeometry(QtCore.QRect(380, 20, 50, 50))
                if i==0:
                    label2.setPixmap(QtGui.QPixmap("gem.png").scaled(label2.width(), label2.height()))
                if i==1:
                    label2.setPixmap(QtGui.QPixmap("gem2.png").scaled(label2.width(), label2.height()))
                if i==2:
                    label2.setPixmap(QtGui.QPixmap("gem3.png").scaled(label2.width(), label2.height()))
                if i==3:
                    label2.setPixmap(QtGui.QPixmap("gem4.png").scaled(label2.width(), label2.height()))
                self.cmdG[j].append(label2)
                self.cmds.append(label2)
        
        for i in range(14):
            if i<7:
                label2 = newLabel(Dialog,self,i)
            else:
                label2 = newLabel(Dialog,self,i-7)
            label2.setGeometry(QtCore.QRect(360+leftUp[i][1]-10,8+leftUp[i][0]-5 , 50, 50))
            pe = QtGui.QPalette()
            pe.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white)
            label2.setPalette(pe)
            ft=QtGui.QFont()
            ft.setBold(True)
            ft.setPointSize(24)
            label2.setFont(ft)
            label2.setText(str(len(self.cmdG[i])))
            self.numLabels.append(label2)
            
        self.paintInit()
        self.firstTurn=True

    def resetGame(self):
        self.buttonClickSound.play()
        self.winningLabel.hide()
    
        self.startP1.setEnabled(True)
        self.startP2.setEnabled(True)
        self.AIvsAI.setEnabled(True)

        if hasattr(self, 'agame'):
            self.agame.reset()  
            self.paintInit() 


    def playClickSound(self):
        """Plays the button click sound."""
        self.buttonClickSound.play()
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Mancala"))
        self.label.setText(_translate("Dialog", "Wadah"))
        self.startP1.setText(_translate("Dialog", "Start as P1"))
        self.startP2.setText(_translate("Dialog", "Start as P2"))
        self.AIvsAI.setText(_translate("Dialog", "AI vs AI"))
        self.reset.setText(_translate("Dialog", "Reset Game"))
        self.groupBox.setTitle(_translate("Dialog", "P1 AI:"))
        self.P1minimax.setText(_translate("Dialog", "Minimax(AB)"))
        self.groupBox_2.setTitle(_translate("Dialog", "P2 AI:"))
        self.P1minimax_2.setText(_translate("Dialog", "Minimax(AB)"))

    def generatePosition(self,target):
        base=(340,0)
        commanderSize=(50,50)
        minx=base[0]+leftUp[target][1]+commanderSize[1]/2
        maxx=base[0]+leftUp[target][1]-commanderSize[1]/2+int(width*1.3)
        miny=base[1]+leftUp[target][0]+commanderSize[0]/2
        if (target==6) or (target==13):
            maxy=base[1]+leftUp[target][0]-commanderSize[0]/2+int(height1*1.3)
        else:
            maxy=base[1]+leftUp[target][0]-commanderSize[0]/2+int(height2*1.3)
        posx=random.randrange(minx,maxx+1,20)
        posy=random.randrange(miny,maxy+1,5)
        return (posy,posx)

    def paintInit(self):
        self.winningLabel.hide()
        for j in range(14):
            for i in range(len(self.cmdG[j])):
                posy,posx=self.generatePosition(j)
                self.cmdG[j][i].setGeometry(QtCore.QRect(posx, posy,50,50))
                self.cmdG[j][i].update()
        for i in range(14):
            self.numLabels[i].setText(str(len(self.cmdG[i])))
            self.numLabels[i].update()
    
    def colorRollBack(self):
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white)
        for i in range(14):
            self.numLabels[i].setPalette(pe)

    def paintMove(self,start,end,num):
        pygame.mixer.init() 
        sound = pygame.mixer.Sound("move.wav")  
        
        for i in range(num):
            label = self.cmdG[start].pop()
            posy, posx = self.generatePosition(end)
            label.setGeometry(QtCore.QRect(posx, posy, 50, 50))
            self.cmdG[end].append(label)

            self.numLabels[start].setText(str(len(self.cmdG[start])))
            self.numLabels[start].update()
            self.numLabels[end].setText(str(len(self.cmdG[end])))
            self.numLabels[end].update()
            
            sound.play()  
            
            self.label.update()

    def paintWinning(self,judge):
        _translate = QtCore.QCoreApplication.translate
        self.winningLabel.setText(_translate("Dialog", judge))
        self.winningLabel.setGeometry(QtCore.QRect(589, 110, 300, 100))
        self.winningLabel.setVisible(True)
        self.winningLabel.update()

    def getAgents(self):
        if self.P1minimax.isChecked():
            agent1=minimaxAgent()
        if self.P1minimax_2.isChecked():
            agent2=minimaxAgent()
        return agent1,agent2

    def play(self, action):
        self.thread = myThread(self.agame, action)
        self.thread.start()

    def uiInit(self):
        self.startP1.setDisabled(True)
        self.startP1.update()
        self.startP2.setDisabled(True)
        self.startP2.update()
        self.AIvsAI.setDisabled(True)
        self.AIvsAI.update()
        if not self.firstTurn:
            self.cmdG=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
            k=0
            for j in range(14):
                if (j==6) or (j==13):
                    continue
                for i in range(4):
                    self.cmdG[j].append(self.cmds[k])
                    k+=1
            self.paintInit()
        else:
            self.firstTurn=False
    
    def uiTerminal(self,judge):
        self.paintWinning(judge)
        self.startP1.setEnabled(True)
        self.startP1.update()
        self.startP2.setEnabled(True)
        self.startP2.update()
        self.startP2.setEnabled(True)
        self.AIvsAI.update()

    def versus(self):
        agent1,agent2=self.getAgents()
        self.agame=gameWithGUI(agent1,agent2,self)
        self.uiInit()
        self.play(-1)

    def p1Start(self):
        self.player=True
        agent1,agent2=self.getAgents()
        self.agame=gameWithGUI(None,agent2,self)
        self.uiInit()
        self.play(-1)
    
    def p2Start(self):
        self.player=False
        agent1,agent2=self.getAgents()
        self.agame=gameWithGUI(agent1,None,self)
        self.uiInit()
        self.play(-1)
    
    def enableManualAction(self,state):
        if state:
            for i in range(0,6):
                self.numLabels[i].enableAction(True)
        else:
            for i in range(7,13):
                self.numLabels[i].enableAction(True)
    
    def disableManualAction(self,state):
        if state:
            for i in range(0,6):
                self.numLabels[i].enableAction(False)
        else:
            for i in range(7,13):
                self.numLabels[i].enableAction(False)