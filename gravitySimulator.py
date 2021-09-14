"""
NOTES:
    first need to install Arcade, using command

"""
import pygame as pg
import time

###CONSTANTS###
width = 1000
height = 1000
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
white = (255,255,255)

default_increment = 1000
increment = default_increment #seconds
dimensions = 3.0

G = 6.674 / (10**11) #units are kg, m, s
sun_m = 1.9885 * (10**30) #in kg
numerator = G*sun_m #yes, we could just multiply the above, but precision matters

r0 = 149597870000 #meters from earth
x = 0
y = -1*r0
vx = 29722.2222 #m/s
vy = 0



#input points with origin at center of screen, output shifts accordingly
#normalizes inputs so that the initial r0 is 1/4 of the height
def f(x,y):
    screen_to_universe_scale = height/(4.0*r0) #multiplying by r0 yields 1/4*height
    x0 = x*screen_to_universe_scale
    y0 = y*screen_to_universe_scale
    return (x0+width/2, height/2-y0)

###START THE GAME###

refresh_rate = 10

pg.init()

print("**********************************")
print("You are now running the gravity simulation tool.")
print("To tweak dimensionality, press the up/down arrows.")
print("To tweak the speed/accuracy balance, press the left/right arrows.")
print("To quit the simulation, simply quit out of the program.")
print("**********************************")



screen = pg.display.set_mode((width, height))
sun = pg.draw.circle(screen, red, f(0,0), 20)
earth = pg.draw.circle(screen, blue, f(x,y), 3)
data = pg.draw.rect(screen, white, pg.Rect(0, 0, 100, 100))


def setValues(dims, incr):
    pg.draw.rect(screen, black, pg.Rect(0,0,width, 75))
    font = pg.font.Font('freesansbold.ttf', 32) #get the desired font
    dim_string = "Dimensions: " + str(round(dims,2))
    incr_string = "Speed up (accuracy suffers): " + str(round(incr/default_increment,2)) + "x"
    dim_text = font.render(dim_string, True, white, black) #get image of text from font
    incr_text = font.render(incr_string, True, white, black)
    screen.blit(dim_text, (0,0)) #draws at the given location, top left as index
    screen.blit(incr_text, (0,incr_text.get_height()))

def reset():
    x = 0
    y = -149597870000
    vx = 29722.2222 #m/s
    vy = 0
    screen.fill(black)
    sun = pg.draw.circle(screen, red, f(0,0), 20)
    earth = pg.draw.circle(screen, blue, f(x,y), 3)
    return (x,y,vx,vy, earth)


reset()
setValues(dimensions, increment)
refresh_counter = 0
done = False
keyPressed = None

while(not(done)):
    setValues(dimensions, increment)
    if (refresh_counter == 0):
        pg.draw.circle(screen, green, earth.center, 3)
        earth = pg.draw.circle(screen, blue, f(x, y), 3)
        if (keyPressed != None):
            if (keyPressed == pg.K_UP):
                dimensions += 0.01
            elif (keyPressed == pg.K_DOWN):
                if (dimensions > 2.5):
                    dimensions -= 0.01
            elif (keyPressed == pg.K_LEFT):
                increment /= 1.05
            elif (keyPressed == pg.K_RIGHT):
                increment *= 1.05
    

    
    refresh_counter = (refresh_counter+1)%refresh_rate

    x += vx*increment
    y += vy*increment

    r = (x**2 + y**2)**(0.5)

    total_force = numerator/(r**(dimensions-1))
    vx += total_force*(-x/r)*increment
    vy += total_force*(-y/r)*increment



    (sx, sy) = f(x,y)
    if (sx > width or sx < 0 or sy > height or sy < 0):
        print("Earth went out of range")
        break

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.KEYDOWN:
            keyPressed = event.key
            if (keyPressed == pg.K_r):
                (x,y,vx,vy, earth) = reset()
                keyPressed = None
        elif event.type == pg.KEYUP:
            keyPressed = None

    pg.display.flip()


print("Simulation completed.")




