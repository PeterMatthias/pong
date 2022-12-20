from ST7735 import TFT,TFTColor		# 128*160
from machine import SPI,Pin
import utime
import urandom

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(11), miso=Pin(12))
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)
tft.fill(TFT.WHITE)

color_back = TFT.WHITE
color_pad = TFT.BLACK
color_ball = TFT.BLUE

p_width = 20
p_height = 10
oldx = p_width // 2
dx = 1
ypos = 140
ball_oldx = oldx
ball_oldy = ypos

button_left = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_right = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)
       
def mv_paddle_left(dx):
    global oldx
    if oldx > p_width // 2:
        tft.fillrect((oldx + p_width // 2, ypos), (-dx, p_height), color_back)	#clear old paddle
        oldx += dx
        tft.fillrect((oldx - p_width // 2, ypos), (-dx, p_height), color_pad)	#draw new paddle

def mv_paddle_right(dx):
    global oldx
    if oldx < 118:
        tft.fillrect((oldx - p_width // 2, ypos), (dx, p_height), color_back)	#clear old paddle
        oldx += dx
        tft.fillrect((oldx +  p_width // 2, ypos), (dx, p_height), color_pad)	#draw new paddle

def mv_ball(dx, dy):
    global ball_dx, ball_dy, ball_oldx, ball_oldy
    tft.fillrect((ball_oldx, ball_oldy), (5, 5), color_back)
    if dx > 0:
        if ball_oldx + dx < 124:
            ball_oldx += dx
        else:
            ball_dx = -dx
    if dx < 0:
        if ball_oldx + dx >= 0:
            ball_oldx += dx
        else:
            ball_dx = -dx
    if dy > 0:
        if ball_oldy + dy < 136:
            ball_oldy += dy
        else:
            ball_dy = -dy
            #check paddle
    if dy < 0:
        if ball_oldy + dy >= 0:
            ball_oldy += dy
        else:
            ball_dy = -dy
    tft.fillrect((ball_oldx, ball_oldy), (5, 5), color_ball)
            
ball_dx = urandom.uniform(-1, 1)
ball_dy = -1
while True:
    mv_ball(ball_dx, ball_dy)
    if button_left.value():
        mv_paddle_left(-dx)
    if button_right.value():
        mv_paddle_right(dx)
    utime.sleep(0.005)

spi.deinit()
