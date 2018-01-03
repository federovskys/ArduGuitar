
import sys,csv


# this is where I put all the preset configs

"""
Each config is a dictionary of this form:
currentDict = {'Name': 'EasyMusic','M' : [0,0],'A' : [0,0],'B' : [0,0],'C' : [0,0],'D' : [0,0],'TR' : [None,0],'S' : '(|(+A(|BC)D)','TREM' : 0,'VIB' : 0}
"""
# configs is a dictionary with key (hs,vs) where hs is horizontal selector pos, and vs is vertical selector pos
"""
Configs  = {(0,0): {'Name':'(0,0)','M' : [0,0],'A' : [0,0],'B' : [0,0],'C' : [0,0],'D' : [0,0],'TR' : [None,0],'S' : '(|(Ab)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (1,0): {'Name':'(1,0)','M' : [1,0],'A' : [1,0],'B' : [1,0],'C' : [1,0],'D' : [1,0],'TR' : [None,0],'S' : '(|BA)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (2,0): {'Name':'(2,0)','M' : [2,0],'A' : [2,0],'B' : [2,0],'C' : [2,0],'D' : [2,0],'TR' : [None,0],'S' : '(|CA)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (3,0): {'Name':'(3,0)','M' : [3,0],'A' : [3,0],'B' : [3,0],'C' : [3,0],'D' : [3,0],'TR' : [None,0],'S' : '(|DA)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (4,0): {'Name':'(4,0)','M' : [4,0],'A' : [4,0],'B' : [4,0],'C' : [4,0],'D' : [4,0],'TR' : [None,0],'S' : '(|dA)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (0,1): {'Name':'(0,1)','M' : [0,1],'A' : [0,1],'B' : [0,1],'C' : [0,1],'D' : [0,1],'TR' : [None,0],'S' : '(|AB)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (1,1): {'Name':'(1,1)','M' : [1,1],'A' : [1,1],'B' : [1,1],'C' : [1,1],'D' : [1,1],'TR' : [None,0],'S' : '(|Bc)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (2,1): {'Name':'(2,1)','M' : [2,1],'A' : [2,1],'B' : [2,1],'C' : [2,1],'D' : [2,1],'TR' : [None,0],'S' : '(|CB)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (3,1): {'Name':'(3,1)','M' : [3,1],'A' : [3,1],'B' : [3,1],'C' : [3,1],'D' : [3,1],'TR' : [None,0],'S' : '(|DB)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (4,1): {'Name':'(4,1)','M' : [4,1],'A' : [4,1],'B' : [4,1],'C' : [4,1],'D' : [4,1],'TR' : [None,0],'S' : '(|dB)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (0,2): {'Name':'(0,2)','M' : [0,2],'A' : [0,2],'B' : [0,2],'C' : [0,2],'D' : [0,2],'TR' : [None,0],'S' : '(|AC)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (1,2): {'Name':'(1,2)','M' : [1,2],'A' : [1,2],'B' : [1,2],'C' : [1,2],'D' : [1,2],'TR' : [None,0],'S' : '(|BC)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (2,2): {'Name':'(2,2)','M' : [2,2],'A' : [2,2],'B' : [2,2],'C' : [2,2],'D' : [2,2],'TR' : [None,0],'S' : '(|Cd)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (3,2): {'Name':'(3,2)','M' : [3,2],'A' : [3,2],'B' : [3,2],'C' : [3,2],'D' : [3,2],'TR' : [None,0],'S' : '(|DC)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (4,2): {'Name':'(4,2)','M' : [4,2],'A' : [4,2],'B' : [4,2],'C' : [4,2],'D' : [4,2],'TR' : [None,0],'S' : '(|dC)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (0,3): {'Name':'(0,3)','M' : [0,3],'A' : [0,3],'B' : [0,3],'C' : [0,3],'D' : [0,3],'TR' : [None,0],'S' : '(|AD)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (1,3): {'Name':'(1,3)','M' : [1,3],'A' : [1,3],'B' : [1,3],'C' : [1,3],'D' : [1,3],'TR' : [None,0],'S' : '(|BD)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (2,3): {'Name':'(2,3)','M' : [2,3],'A' : [2,3],'B' : [2,3],'C' : [2,3],'D' : [2,3],'TR' : [None,0],'S' : '(|CD)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (3,3): {'Name':'(3,3)','M' : [3,3],'A' : [3,3],'B' : [3,3],'C' : [3,3],'D' : [3,3],'TR' : [None,0],'S' : '(|Da)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (4,3): {'Name':'(4,3)','M' : [4,3],'A' : [4,3],'B' : [4,3],'C' : [4,3],'D' : [4,3],'TR' : [None,0],'S' : '(|da)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (0,4): {'Name':'(0,4)','M' : [0,4],'A' : [0,4],'B' : [0,4],'C' : [0,4],'D' : [0,4],'TR' : [None,0],'S' : '(|Ad)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (1,4): {'Name':'(1,4)','M' : [1,4],'A' : [1,4],'B' : [1,4],'C' : [1,4],'D' : [1,4],'TR' : [None,0],'S' : '(|Bd)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (2,4): {'Name':'(2,4)','M' : [2,4],'A' : [2,4],'B' : [2,4],'C' : [2,4],'D' : [2,4],'TR' : [None,0],'S' : '(|Cd)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            (3,4): {'Name':'(3,4)','M' : [3,4],'A' : [3,4],'B' : [3,4],'C' : [3,4],'D' : [3,4],'TR' : [None,0],'S' : '(|Da)','TREM' : 1,'VIB' : 1, 'AUX0' : 1, 'AUX1' : 1},
            (4,4): {'Name':'(4,4)','M' : [4,4],'A' : [4,4],'B' : [4,4],'C' : [4,4],'D' : [4,4],'TR' : [None,0],'S' : '(|Da)','TREM' : 0,'VIB' : 0, 'AUX0' : 0, 'AUX1' : 0},
            }
"""
class Preset():

    def __init__(self,pyGuitarConf,fileName=None):
            # the fileName is used to load a presets file, if one exists,
            # if not, one is created
            self.conf = pyGuitarConf
            self.presets = {}
            if fileName==None:
                self.filePath =  self.conf.LocalConf.presetDir +   self.conf.LocalConf.dirSeparator +  self.conf.LocalConf.presetFileName
            else:
                self.filePath = fileName
            print "creating preset instance from:\t" + self.filePath
            try:
                with open(self.filePath, 'r') as csvfile:
                    #print "opened file: " + self.filePath
                    reader = csv.DictReader(csvfile,fieldnames = self.conf.Vocab.headings,delimiter=',')
                    self.header = reader.next()
                    for row in reader:
                        self.rowDict2confDict(row)
            except:
                print "error reading preset file!  Creating new one!"
                self.createDefaultPresets()
            self.currentDict = {}
            for k in self.presets[(0,0)].keys():
                self.currentDict[k] = self.presets[(0,0)][k]

    def rowDict2confDict(self,row):
        curConfDict= {}
        self.presets[(int(row[self.conf.Vocab.headings[0]]),int(row[self.conf.Vocab.headings[1]]))]= curConfDict
        curConfDict[self.conf.Vocab.configKeys[0]] = row[self.conf.Vocab.headings[2]]
        for i in  range(1,6):
            curConfDict[self.conf.Vocab.configKeys[i]] = [int(row[self.conf.Vocab.headings[1+2*i]]),int(row[self.conf.Vocab.headings[2+2*i]])]
        curConfDict[self.conf.Vocab.configKeys[6]] = [None,int(row[self.conf.Vocab.headings[13]])]
        curConfDict[self.conf.Vocab.configKeys[7]] = row[self.conf.Vocab.configKeys[7]]
        for k in self.conf.Vocab.configKeys[8:]:
                curConfDict[k] = int(row[k])
                        
    def createDefaultPresets(self):
        # this will create a default preset file in the default location
        # with default content
        for i in range(5):
            for j in range(5):
                self.presets[(i,j)] = self.conf.presetConf.defaultConfDict
        self.header = self.conf.Vocab.headings
        #self.toFile(self.conf..presetFileName)
    
    def toFile(self, file = None):
        # this will write the presets to a file,
        # if a file argument is provided it is used and it
        # updates the instance filePath
        # otherwise the current instance filePath is used
        if file: 
            self.filePath = file
        with open(self.filePath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames = self.conf.Vocab.headings,
                                    delimiter=',')
                                    #quotechar="'", 
                                    #quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.header)
            for p in self.presets.keys():
                writer.writerow(self.confDict2RowDict(p,self.presets[p]))
        print "Wrote file:\t" + self.filePath
        
    def confDict2RowDict(self,key,conf):
        curRowDict= {}
        # horiz and verti
        for i in range(2):
            curRowDict[self.conf.Vocab.headings[i]] = key[i]
        #Name
        curRowDict[self.conf.Vocab.headings[2]] = conf[self.conf.Vocab.headings[2]]
        
        #M,A,B,C,D  vol and tone    
        for i in  range(1,6):
            curRowDict[self.conf.Vocab.headings[1+2*i]] = conf[self.conf.Vocab.configKeys[i]][0]
            curRowDict[self.conf.Vocab.headings[2+2*i]] = conf[self.conf.Vocab.configKeys[i]][1]
        # TneRange    
        curRowDict[self.conf.Vocab.headings[13]] = conf[self.conf.Vocab.configKeys[6]][1]
        #S,TREM,VIB,AUX0,AUX1
        for k in self.conf.Vocab.headings[14:]:
                curRowDict[k] = conf[k]
        return curRowDict
    
    def add(self,name,vDict):
        # add this to the presets, if the vDict is proper length:
        # and no keys are wrong
        # print "preset.add(",name,vDict,")", self.header
        newDict = {}
        for k in vDict.keys():
            newDict[k] = vDict[k]
        self.presets[name]=newDict
        
    def remove(self,name):
        # just remove it or do nothing if not possible
        if name in self.presets.keys():
            del self.presets[name]
    
    def rename(self,old,new):
        # to rename a preset, we create a new dict copied from previous one
        # put it in with the new name
        # and remove the reference to the old name
        # if the old name is not found, do nothing
        # return True if success, False otherwise
        # print "renaming preset: " + old + " to: " + new
        res = False
        if old in self.presets.keys():
            newDict = {}
            for k in self.presets[old].keys():
                newDict[k] = self.presets[old][k]
            self.presets[new] = newDict
            del self.presets[old]
            res = True
        return res
    
    def saveCurrentConfigAsPreset(self, key):
        self.currentDict[self.conf.vocab.configKeys[11]] = 0
        self.add(key,self.currentDict)
        self.toFile()
            