"""Implements a character based lcd connected via PCF8574 on i2c."""

from pyb import Pin
from pyb import delay, millis
from pyb_gpio_lcd import GpioLcd

# Wiring used for this example:
#
#  1 - Vss (aka Ground) - Connect to one of the ground pins on you pyboard.
#  2 - VDD - connected to VIN which is 5 volts when your pyboard is powerd vi USB
#  3 - VE - connected to VIN (Contrast voltage) - I'll discuss this below
#  4 - RS (Register Select) connect to Y12 (as per call to GpioLcd)
#  5 - RW (Read/Write) - connect to ground
#  6 - EN (Enable) connect to Y11 (as per call to GpioLcd)
#  7 - D0 - leave unconnected
#  8 - D1 - leave unconnected
#  9 - D2 - leave unconnected
# 10 - D3 - leave unconnected
# 11 - D4 - connect to Y5 (as per call to GpioLcd)
# 12 - D5 - connect to Y6 (as per call to GpioLcd)
# 13 - D6 - connect to Y7 (as per call to GpioLcd)
# 14 - D7 - connect to Y8 (as per call to GpioLcd)
# 15 - A (BackLight Anode) - Connect to VIN
# 16 - K (Backlight Cathode) - Connect to Ground
#
# The Contrast line (pin 3) typically connects to the center tap of a
# 10K potentiometer, and the other 2 legs of the 10K potentiometer are
# connected to pins 1 and 2 (Ground and VDD)
#
# The wiring diagram on the followig page shows a typical "base" wiring:
# http://www.instructables.com/id/How-to-drive-a-character-LCD-displays-using-DIP-sw/step2/HD44780-pinout/
# Add to that the EN, RS, and D4-D7 lines.

class LcdDisplay(GpioLcd):
    def __init__(self,
                 rs_pin=Pin.board.Y12,
                 enable_pin=Pin.board.Y11,
                 d4_pin=Pin.board.Y5,
                 d5_pin=Pin.board.Y6,
                 d6_pin=Pin.board.Y7,
                 d7_pin=Pin.board.Y8,
                 num_lines=2,
                 num_columns=16):
        GpioLcd.__init__(self,
                         rs_pin,
                         enable_pin,
                         d4_pin,
                         d5_pin,
                         d6_pin,
                         d7_pin,
                         num_lines,
                         num_columns)
        self.lns =['0123456789ABCDEF','0123456789ABCDEF']
    
    def setLn(self, lineNb, val):
        """
        Set the LCD line linNb to display the val;
        val is left justified to num_cols to overwrite any 
        characters leftover from previous writes.
        """
        self.lns[lineNb] = '%-*s' % ((self.num_columns), val)
        self.move_to(0,lineNb)
        self.putstr(self.lns[lineNb])
        return self
  
    def getLn(self, lineNb):
        return self.lns[lineNb]
        
lcd = LcdDisplay(rs_pin=Pin.board.X18,
                 enable_pin=Pin.board.Y7,
                 d4_pin=Pin.board.Y8,
                 d5_pin=Pin('A15',mode=Pin.OUT_PP), #board.P3
                 d6_pin=Pin('A14',mode=Pin.OUT_PP), #board.P4,
                 d7_pin=Pin('A13',mode=Pin.OUT_PP), #board.P5,
                 num_lines=2,
                 num_columns=16)

def testLCD():
    """
    Test function for verifying basic functionality.
    """
    global lcd
    print("Running test_main")
     #lcd.putstr("It Works!\nSecond Line")
    lcd.setLn(0,'It Works!')
    lcd.setLn(1,'Second Line')
    delay(3000)
    #lcd.backlight_off()
    #lcd.clear()
    count = 0
    while count<20:
        #lcd.move_to(0, 0)
        #lcd.putstr(str(millis() // 1000))
        lcd.setLn(0,str(millis() // 1000))
        delay(1000)
        count += 1
    #return lcd

