from ST7735 import TFT, TFTColor    # 128*160
from machine import SPI, Pin
import utime
import urandom
from sysfont import sysfont

button_left = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_right = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_DOWN)

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(11), miso=Pin(12))
tft=TFT(spi, 16, 17, 18)
tft.initr()
tft.rgb(True)

tft.fill(tft.WHITE)

color_back = tft.WHITE
color_pad = tft.BLACK
color_ball = tft.RED

p_width = 20
p_height = 10
oldx = p_width // 2
dx = 1
ypos = 140
ball_oldx = oldx
ball_oldy = ypos
dead = False
points = 0
paused = False
       
def mv_paddle_left(dx):
    global oldx
    if oldx > p_width // 2:
        tft.fillrect((oldx + p_width // 2, ypos), (-dx, p_height), color_back)   # clear old paddle
        oldx += dx
        tft.fillrect((oldx - p_width // 2, ypos), (-dx, p_height), color_pad)    # draw new paddle

def mv_paddle_right(dx):
    global oldx
    if oldx < 118:
        tft.fillrect((oldx - p_width // 2, ypos), (dx, p_height), color_back)    # clear old paddle
        oldx += dx
        tft.fillrect((oldx +  p_width // 2, ypos), (dx, p_height), color_pad)    # draw new paddle

def mv_ball(dx, dy):
    global ball_dx, ball_dy, ball_oldx, ball_oldy, points
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
            distance_to_paddle_abs = abs(oldx - ball_oldx + 2)
            distance_to_paddle = oldx - ball_oldx + 2
            if distance_to_paddle_abs - 4 < p_width // 2:
                points += 1
##                ball_oldx += distance_to_paddle // 2
##                tft.fillrect((120, 5), (5, 80), tft.BLACK)
##                tft.text((120, 5), f"Punkte {points}", tft.RED, sysfont, 1)
                tft.fillrect((0, 150), (128, 10), tft.BLACK)
                tft.text((5, 150), f"Punkte {points}", tft.RED, sysfont, 1)
            else:
                global dead
                dead = True
                
    if dy < 0:
        if ball_oldy + dy >= 0:
            ball_oldy += dy
        else:
            ball_dy = -dy
    tft.fillrect((ball_oldx, ball_oldy), (5, 5), color_ball)
            
ball_dx = urandom.uniform(-1, 1)
ball_dy = -1

while True:
    while dead == False:
        if paused == False:
            mv_ball(ball_dx, ball_dy)
            if button_left.value():
                mv_paddle_left(-dx)
            if button_right.value():
                mv_paddle_right(dx)
            if button_left.value() and button_right.value():
                paused = True
            utime.sleep(0.004)
        elif paused:
            if button_left.value() or button_right.value():
                utime.sleep(0.25)
                if button_left.value() or button_right.value():
                    paused = False
    if dead == True:
        tft.fill(tft.BLACK)
        tft.text((16, 60), "Verloren!", tft.RED, sysfont, 2)
#        tft.text((120, 5), f"Punkte {points}", tft.WHITE, sysfont, 1)
        tft.fillrect((0, 150), (128, 10), tft.BLACK)
        tft.text((5, 150), f"Punkte {points}", tft.WHITE, sysfont, 1)
        utime.sleep(1)
    while dead == True:
        if button_left.value() or button_right.value():
            utime.sleep(1)
            ball_dx = urandom.uniform(-1, 1)
            dead = False
            tft.fill(color_back)
            points = 0
spi.deinit()
