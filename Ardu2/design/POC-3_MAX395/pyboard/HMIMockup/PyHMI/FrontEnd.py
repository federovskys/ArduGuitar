import Classes,  SplitPot, TrackBall, oClasses, sParse
from config import PyGuitarConf
from Presets import Preset
from PyboardMgr import PyboardMgr

DEBUG = True

class Q:
    qLen = 20
    
    def __init__(self):
        self.pptr = 0  # put pointer
        self.gptr = 0  # get pointer
        self.qNbObj=0  # object counter
        self.q = [None for i in range(Q.qLen)]

    def push(self,e):
        if self.qNbObj == Q.qLen:
            raise Exception('Q Full! ignoring push!')
        else:
            self.q[self.pptr] = e
            self.pptr = (self.pptr+1) % Q.qLen
            self.qNbObj += 1
            #print('push:\t' + hex(e))
            
    def pop(self):
        res = None
        if self.qNbObj:
            res = self.q[self.gptr]
            self.gptr = (self.gptr+1) % Q.qLen
            self.qNbObj -=1
            #print('pop:\t' + hex(res))
        return res
            

class HMIMgr:
    funcVec= ['inc', 'pb','conf','vol','tone']
    targVec = [['MVol','MTone'],
               [0,1,2,3,4,5],
               [0,1], #horizontal, vertical
               ['M','A','B','C','D','TR']]

    def toPrint(self):
        print('********** START SEND: %d **********'%self.sendCounter)
        for i in self.outgoing:
            print(i)
        print('********** END SEND: %d **********'%self.sendCounter)
        self.outgoing  = []
        self.sendCounter+=1
    
    def sendToPyboard(self):
        #print('********** START SEND: %d **********'%self.sendCounter)
        
        print(self.pyboardMgr.send(self.outgoing))
        
        #print('********** END SEND: %d **********'%self.sendCounter)
        self.outgoing  = []
        #self.sendCounter+=1
        
    def initPyGuitar(self):
        initSeq = ['from app import App',
                   'from state import State',
                   'a=App()',
                   'a.showConfig()'
                   ]
        self.outgoing += initSeq
        self.sendToPyboard()
        
        
    def __init__(self):
        
        self.outgoing = []

        if DEBUG:
            self.sendCounter=0
            self.toPyboard = self.toPrint
        else:
            self.pyboardMgr = PyboardMgr()
            self.toPyboard  = self.sendToPyboard
            self.initPyGuitar()
        
        self.q = Q()
        self.conf = PyGuitarConf()
        self.preset = Preset(self.conf)

        self.ld = Classes.LedDisplay(PyGuitarConf.Layout.oLD,(self.preset.currentDict,self.conf.vocab.configKeys[1:7])) #not an active component, so no Q needed
        
        self.ledPbA = Classes.LedPBArray(PyGuitarConf.Layout.oLPA,self.q,self.preset.currentDict,self.conf.vocab.configKeys[10:]+self.conf.vocab.configKeys[8:10])
        self.spa    = SplitPot.SplitPotArray(PyGuitarConf.Layout.oSPA,HMIMgr.targVec[3],self.q)        
        self.lcdMgr = oClasses.LCDMgr((self.preset.currentDict,'S','Name'),Classes.LCD(PyGuitarConf.Layout.oLCD),self.q,self.validateAndApplyLCDInput)
        self.sh     = Classes.Selector(PyGuitarConf.Layout.oSH,Classes.Selector.white,True,self.q) 
        self.sv     = Classes.Selector(PyGuitarConf.Layout.oSV,Classes.Selector.black,False,self.q)
        self.tb     = TrackBall.TrackBall(PyGuitarConf.Layout.oTB, self.q, PyGuitarConf.Layout.bg) # stubs.hTBFunc,stubs.vTBFunc,PyGuitarConf.Layout.bg)
        self.setVec = [self.inc, self.pb, self.doConf, self.vol, self.tone]
        
        self.sendReset()
        self.loadConf(self.preset.presets[(self.sh.pos,self.sv.pos)])
        self.sendX()
    
    def sendX(self):
        #print('a.x()')
        self.outgoing.append('a.x()')
        self.toPyboard()
        
    def sendReset(self):
        #print('a.reset()')
        self.outgoing.append('a.reset()')
        #self.toPyboard()
    
    def pollInterrupters(self):
        self.ld.display()
        self.ledPbA.display()
        self.lcdMgr.display()
        self.sh.display()
        self.sv.display()
        self.tb.display()
    
    def pollPollables(self):    
        self.spa.display()
    
    def display(self):
        self.pollInterrupters()   # Poll interrupt generating objects, includes enqueue, not needed when interupts can happen!
        self.pollPollables()      #  Poll split pots includes enqueue,
        self.processQ()
        
    def processQ(self):
        work = self.q.pop()
        worked = False
        self.outgoing = []
        while (work != None):
            worked = self.x(work) or worked
            work = self.q.pop()
        if worked:
            self.sendX()

    def x(self,twoBytes):
        V = twoBytes & 0xFF
        K = (twoBytes>>8) & 0xFF
        mask = 0x80
        res = False
        #print('X:\tK:\t' + hex(K)) + '\tV:\t'+ hex(V) 
        for i in range(5):
            if K & (mask>>i):
                who = HMIMgr.targVec[min(i,3)][K & 0b111]
                val = (0xFF & V) if (V & 0xFF)<128 else (V & 0XFF)-256
                res = self.setVec[i](who,val) or res
                break
        return res
    
    def inc(self,who,val):
        # who is 'MVol','MTone'
        #print('INC:\t' + str(who) +'\t' + str(val))
        if who == HMIMgr.targVec[0][0]: 
            # its vol
            newVol = max(0,(min(self.preset.currentDict['M'][0] + val,5)))
            return self.vol(who[0],newVol)
            #self.preset.currentDict['M'][0] = newVol
            #print(who +':\t' + str(newVol))
        else:
            newTone = max(0,(min(self.preset.currentDict['M'][1] + val,5)))
            return self.tone(who[0],newTone)
            #self.preset.currentDict['M'][1] = newTone
            #print(who +':\t' + str(newTone))
            
    def vol(self,who,val,force=False):
        # who is 'M','A','B','C','D'
        if force or val != self.preset.currentDict[who][0]:
            #print('VOL:\t' + str(who) +'\t' + str(val))
            #print("a.set('%s',State.Vol,State.l%s)"%(who,(str(val) if val !=0 else 'Off')))
            self.outgoing.append("a.set('%s',State.Vol,State.l%s)"%(who,(str(val)))) # if val !=0 else 'Off')))
            self.preset.currentDict[who][0] = val
            return True
        return False

    def tone(self,who,val,force=False):
        # who is 'M','A','B','C','D','TR'
        if force or val != self.preset.currentDict[who][1]:
            #print('TONE:\t' + str(who) +'\t' + str(val))
            trVal = 'Off'
            toneVal = '0'
            if who =='TR':
                trVal =  str(val-1) if val else 'Off'
                targ = 'M'
                toneVal = None
            elif who == 'M':
                targ = who
                trVal = None
                toneVal = str(val-1) if val else 'Off'
            else:
                targ = who
                trVal = '0' if val else 'Off'
                toneVal = str(val-1) if val else 'Off'
            if trVal != None:
                self.outgoing.append("a.set('%s',State.ToneRange,State.l%s)"%(targ,trVal))
                #print("a.set('%s',State.ToneRange,State.l%s)"%(targ,trVal))
            if toneVal != None:
                self.outgoing.append("a.set('%s',State.Tone,State.l%s)"%(targ,toneVal))
                #print("a.set('%s',State.Tone,State.l%s)"%(targ,toneVal))
            self.preset.currentDict[who][1] = val
            return True
        return False
                
    def doConf(self,who,val):
        # who is 0 for horizontal, 1 for vertical    
        #print('CONF:\t' + str((val if not who else None,None if not who else val)))
        self.sendReset()
        self.loadConf(self.preset.presets[(self.sh.pos,self.sv.pos)])
        return True
    
    def pb(self,who,unused):
        whoFuncs = [(self.ledPbA.ledPbs[0].toggle,self.displayCurrentConf),     # this one has no real function, currently is used for debugging
                    (self.saveCurrentConfAsPreset,self.ledPbA.ledPbs[1].flash), # this is the one saves the preset, 
                    (self.toggleTrem,), #,self.ledPbA.ledPbs[2].toggle,stubs.g),                             # Tremolo
                    (self.toggleVib,), #self.ledPbA.ledPbs[3].toggle,stubs.b),                             # Vibrato
                    (self.lcdMgr.onLeftButton,),
                    (self.lcdMgr.onRightButton,)]
        #print('PB:\t' + str(who))  
        res = False         
        for f in whoFuncs[who]:
            res = f() or res
        return res # True if who in [2,3] else False
    
    def toggleTrem(self):
        #trem =2, vibrato =3
        self.preset.currentDict[self.conf.vocab.configKeys[8]] = 0 if self.preset.currentDict[self.conf.vocab.configKeys[8]] else 1
        v = str(1) if self.preset.currentDict[self.conf.vocab.configKeys[8]] else 'Off'
        print ("CANNOT YET SEND:\ta.set('M',State.Tremolo,l%s)"%v)
        #self.outgoing.append("a.set('M',State.Tremolo,l%s)"%v)
        return False # True
    def toggleVib(self):
        #trem =2, vibrato =3
        self.preset.currentDict[self.conf.vocab.configKeys[9]] = 0 if self.preset.currentDict[self.conf.vocab.configKeys[9]] else 1
        v = str(1) if self.preset.currentDict[self.conf.vocab.configKeys[9]] else 'Off'
        print ("CANNOT YET SEND:\ta.set('M',State.Vibtrato,l%s)"%v)
        #self.outgoing.append("a.set('M',State.Vibtrato,l%s)"%v)
        return False #True
    def displayCurrentConf(self):
        print(self.preset.currentDict)
    
    def loadConf(self, conf):
        try:
            res = self.doParse(conf[self.conf.vocab.configKeys[7]])
            for e in res:
                #print(e)
                self.outgoing.append(e)
            for key in self.preset.currentDict.keys():
                self.preset.currentDict[key] = conf[key]
        except Exception as e:
            print (e)
            self.doParse(self.conf.presetConf.defaultConfDict[self.conf.vocab.configKeys[7]])
            for key in self.conf.presetConf.defaultConfDict.keys():
                self.preset.currentDict[key] = self.conf.presetConf.defaultConfDict[key]
            self.preset.currentDict[self.conf.vocab.configKeys[0]] = 'DEFAULT PRESET'
        
        self.tone('TR',self.preset.currentDict['TR'][1],True)
        for c in ['A','B','C','D','M']:
            self.vol(c,self.preset.currentDict[c][0],True)
            self.tone(c,self.preset.currentDict[c][1],True)
        self.toggleTrem()
        self.toggleVib()
        self.lcdMgr.loadConf()
        #self.displayCurrentConf()
        
    def saveCurrentConfAsPreset(self):
        self.preset.saveCurrentConfigAsPreset((self.sh.pos,self.sv.pos))
    
    def validateAndApplyLCDInput(self,confString):
        try:
            res = self.doParse(confString.strip())
            for e in res:
                #print(e)
                self.outgoing.append(e)
            self.sendX()
            return True
        except Exception as e:
            print (e)
            return False
        
    def doParse(self,confString):
        sp = sParse.SExpParser(confString.strip())
        return sp.execute()