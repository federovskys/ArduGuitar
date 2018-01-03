from Classes import Positionable, MouseLockable,EnQueueable

class TrackBall(Positionable,MouseLockable,EnQueueable):
    radius = 22*Positionable.scaleFactor
    lineColor = '#FFFFFF'
    markColor = '#FF0000' 
    delayMS = 50  # time to wait between line draws
    minL = 3 # min line length
    redLines=True
    
    def __init__(self,(x,y), q, bg):
        Positionable.__init__(self,x,y)
        MouseLockable.__init__(self,MouseLockable.TRACKBALL)
        EnQueueable.__init__(self,EnQueueable.INC,q)
        self.bg = bg
        self.mouseStartX = 0
        self.mouseEndX = 0
        self.startPointX = 0 
        self.mouseStartY = 0
        self.mouseEndY = 0
        self.startPointY = 0
        self.hI=0
        self.vI=0
        self.hSteps=0
        self.vSteps=0
        self.oX = TrackBall.radius
        self.oY = TrackBall.radius
        self.sliding=False
        self.lastLineDraw = millis()
        
    def display(self):
        pushMatrix()
        translate(self.x*Positionable.scaleFactor,self.y*Positionable.scaleFactor)
        self.incH(True)
        self.incH(False)
        self.outline()
        self.lines(True)
        self.lines(False)
        popMatrix()
    
    def outline(self):
        stroke(self.markColor)
        #stroke(255)
        fill(self.bg)
        ellipseMode(CENTER)
        R=self.oX  # can use either since it's a circle
        H = 2*TrackBall.radius
        ellipse(R,R,H,H)
    
    def lines(self,isVertical):
        stroke(TrackBall.lineColor)
        R = TrackBall.radius
        for i in range(self.vI if isVertical else self.hI, 190,10):
            d = R*(1-cos(radians(i)))
            if isVertical:
                line (d,self.oY-max(3,sqrt(d*(2*R-d))),d,self.oY+max(3,sqrt(d*(2*R-d))))
            else:
                line (self.oX-max(TrackBall.minL,sqrt(d*(2*R-d))),d,self.oX+max(TrackBall.minL,sqrt(d*(2*R-d))), d)
        if TrackBall.redLines:
            stroke(TrackBall.markColor)
            for a in [0,45,90,135,180]:
                d = R*(1-cos(radians(a)))
                if isVertical:
                    line (d,self.oY-max(TrackBall.minL,sqrt(d*(2*R-d))),d,self.oY+max(TrackBall.minL,sqrt(d*(2*R-d))))
                else:
                    line (self.oX-max(TrackBall.minL,sqrt(d*(2*R-d))),d,self.oX+max(TrackBall.minL,sqrt(d*(2*R-d))), d)
                    
    def setSliding(self, start):
        if start:
            self.sliding=True
            self.mouseStartX = mouseX
            self.startPointX = mouseX
            self.mouseStartY = mouseY
            self.startPointY = mouseY
        else:
            self.sliding=False
            
    def slidingHelper(self):
            self.mouseEndX = mouseX
            self.mouseEndY = mouseY
            dX = self.mouseEndX - self.startPointX
            dY = self.mouseEndY - self.startPointY
            w= TrackBall.radius*2
            dV = int(round(map(dX,-w,w,-5,5)))
            dT = int(round(map(dY,-w,w,-5,5)))
            if dV!=0:
                self.push(0,dV) 
                self.startPointX= self.mouseEndX
            if dT!=0:
                self.push(1,dT)
                self.startPointY= self.mouseEndY
           
    def getSet(unused,isHorizontal):
        if isHorizontal:
            return (mouseY, 'self.mouseStartY','self.hSteps','self.hI')
        else:
            return  (mouseX, 'self.mouseStartX','self.vSteps','self.vI')
        
    def incH(self,isHorizontal=False):
        if mousePressed:
            if not self.isOver():
                return
            if not self.sliding:
                self.setSliding(True)
            (mouse,mouseStartS,StepS,IS) = self.getSet(isHorizontal)
            positiveMovement= eval(mouseStartS)<= mouse
            exec(StepS + '= map(abs(mouse-eval(mouseStartS)),0,2*TrackBall.radius,0,18)')
            exec(mouseStartS + ' = mouse')
            if eval(StepS)>0:
                if positiveMovement:
                    exec(IS + '= (' + IS + '+1)%10')
                else: 
                    exec(IS + '= (9 if ' + IS + '==0 else ' + IS +' -1)')
                exec(StepS  +'-=1')
                self.slidingHelper();
        elif self.sliding:
            # we are over and locked and release mouse
            self.setSliding(False)
            self.unlock()

    def isOver(self):
        oX = TrackBall.radius+self.x*Positionable.scaleFactor
        oY = TrackBall.radius+self.y*Positionable.scaleFactor
        res= (sq(mouseX-oX) + sq(mouseY-oY) <= sq(TrackBall.radius)) and self.lock()  
        return res