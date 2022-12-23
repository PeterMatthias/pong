from ST7735 import TFT, TFTColor    # 128*160
from machine import SPI, Pin
import utime
import urandom
from sysfont import sysfont

button_left = Pin(21, Pin.IN, Pin.PULL_DOWN)
button_right = Pin(20, Pin.IN, Pin.PULL_DOWN)
spi = SPI(1, baudrate = 20000000, polarity = 0, phase = 0, sck=Pin(14), mosi=Pin(11), miso=Pin(12))
tft = TFT(spi, 16, 17, 18)
tft.initr()
tft.rgb(True)

color_back = tft.WHITE
color_pad = tft.BLACK
color_ball = tft.BLUE

d_width = 128
p_width = 20
p_height = 8
b_width = 4
ypos = 140

def wait():
    while button_right.value() or button_left.value():
        utime.sleep(0.1)
    while not (button_left.value() or button_right.value()):
        utime.sleep(0.1)

def mv_paddle_left():
    global p_oldx
    if p_oldx >= 0:
        tft.fillrect((p_oldx + p_width, ypos), (1, p_height), color_back) # clear old paddle
        tft.fillrect((p_oldx, ypos), (1, p_height), color_pad)            # draw new paddle
        p_oldx -= 1

def mv_paddle_right():
    global p_oldx
    if p_oldx < d_width - p_width:
        tft.fillrect((p_oldx, ypos), (1, p_height), color_back)           # clear old paddle
        tft.fillrect((p_oldx + p_width, ypos), (1, p_height), color_pad)  # draw new paddle
        p_oldx += 1

def mv_ball(dx, dy):
    global ball_dx, ball_dy, ball_oldx, ball_oldy, points
    tft.fillrect((ball_oldx, ball_oldy), (b_width, b_width), color_back)
    if dx > 0:
        if ball_oldx + dx < d_width -b_width:
            ball_oldx += dx
        else:
            ball_dx = -dx
    if dx < 0:
        if ball_oldx + dx >= 0:
            ball_oldx += dx
        else:
            ball_dx = -dx
    if dy > 0:
        if ball_oldy + dy < ypos - b_width:
            ball_oldy += dy
        else:
            ball_dy = -dy
            distance_to_paddle = (p_oldx + (p_width - b_width) // 2 - ball_oldx)
            if abs(distance_to_paddle) < p_width // 2:
                points += 1
                tft.text((5, ypos + 10), f"Punkte: {points}", tft.RED, sysfont, 1)
            else:
                global dead
                dead = True   
    if dy < 0:
        if ball_oldy + dy >= 0:
            ball_oldy += dy
        else:
            ball_dy = -dy
    tft.fillrect((ball_oldx, ball_oldy), (b_width, b_width), color_ball)
            
tft.fill(tft.BLACK)
while True:
    tft.text((14, 100), "press key to play", tft.WHITE, sysfont, 1)
    wait()
    ball_dx = urandom.uniform(-1, 1)
    ball_dy = -1
    points = 0
    dead = False
    p_oldx = 0
    ball_oldx = 0
    ball_oldy = ypos - b_width
    tft.fill(color_back)
    tft.fillrect((p_oldx, ypos), (p_width , p_height), color_pad)
    tft.fillrect((0, ypos + 9), (d_width, 11), tft.BLACK)
    while dead == False:
        mv_ball(ball_dx, ball_dy)
        if button_left.value():
            mv_paddle_left()
        if button_right.value():
            mv_paddle_right()
            if button_left.value():  # pause
                wait()
        utime.sleep(0.004)
    tft.fillrect((0, 0), (d_width, ypos + 10), tft.BLACK)
    tft.text((16, 60), "Verloren!", tft.RED, sysfont, 2)
spi.deinit()
