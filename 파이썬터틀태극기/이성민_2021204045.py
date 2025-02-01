import turtle
import math

numangle = 50
length = 500 / numangle
radius = length / (2 * math.sin(math.pi / numangle))

def draw_square(t, s, numangle, length, radius):
    if (s == 1):
        size = radius * (11/24)
    elif (s == 2):
        size = radius
    t.forward(size)
    t.right(90)
    t.forward(radius / 6)
    t.right(90)
    t.forward(size)
    t.right(90)
    t.forward(radius / 6)

def draw_small_square(t, numangle, length, radius):
    draw_square(t, 1, numangle, length, radius)
    t.right(90)
    t.penup()
    t.forward(radius * (13/24))
    t.pendown()
    draw_square(t, 1, numangle, length, radius)
    t.left(90)
    t.penup()
    t.forward(radius * (13/24))

def draw_teaguk(t,  numangle, length, radius):
    t.penup()
    t.goto(-radius * 0.8, radius * 0.6)
    t.pendown()

    t.right(90 + 33.86)
    for _ in range(numangle):
        t.forward(length)
        t.left(360 / numangle)
    
    for _ in range(int(numangle / 2), numangle):
        t.forward(length / 2)
        t.left(360 / numangle)
    
    for _ in range(int(numangle / 2), numangle):
        t.forward(length / 2)
        t.right(360 / numangle)

def draw_gun(t, numangle, length, radius):
    t.penup()
    t.home()
    t.seth(180 - 33.86)
    t.forward(radius * (29/12))
    t.left(90)
    t.forward(radius/2)
    t.right(180)
    t.pendown()

    for i in range(3):
        draw_square(t, 2, numangle, length, radius)
        t.penup()
        t.right(180)
        t.forward(radius / 4)
        t.pendown()
        t.left(90)

def draw_gon(t, numangle, length, radius):
    t.penup()
    t.home()
    t.seth(180 + 33.86)
    t.forward(radius * (23/12))
    t.left(90)
    t.forward(radius/2)
    t.right(180)
    t.pendown()

    draw_square(t, 2, numangle, length, radius)

    t.penup()
    t.forward(radius / 4)
    t.right(90)
    t.pendown()
    
    draw_small_square(t, numangle, length, radius)
    t.right(90)
    t.forward(radius/4)
    t.pendown()
    t.right(90)
    draw_square(t, 2, numangle, length, radius)

def draw_gam(t, numangle, length, radius):
    t.penup()
    t.home()
    t.seth(33.86)
    t.forward(radius * (23/12))
    t.left(90)
    t.forward(radius/2)
    t.right(180)
    t.pendown()


    draw_small_square(t, numangle, length, radius)
    t.penup()
    t.right(90)
    t.forward(radius / 4)
    t.right(90)
    t.pendown()
    draw_square(t, 2, numangle, length, radius)
    t.penup()
    t.forward(radius / 4)
    t.right(90)
    t.pendown()
    draw_small_square(t, numangle, length, radius)

def draw_ri(t, numangle, length, radius):
    t.penup()
    t.home()
    t.seth(-33.86)
    t.forward(radius * (29/12))
    t.left(90)
    t.forward(radius/2)
    t.right(180)
    t.pendown()

    draw_small_square(t, numangle, length, radius)
    t.penup()
    t.left(90)
    t.forward(radius / 4)
    t.left(90)
    t.pendown()
    draw_small_square(t, numangle, length, radius)
    t.penup()
    t.left(90)
    t.forward(radius / 4)
    t.left(90)
    t.pendown()
    draw_small_square(t, numangle, length, radius)

def paper(t, numangle, length, radius):
    t.penup()
    t.home()
    t.seth(-90)
    t.forward(radius * 2)
    t.pendown()
    t.right(90)
    t.forward(radius * 3)
    t.right(90)
    t.forward(radius * 4)
    t.right(90)
    t.forward(radius * 6)
    t.right(90)
    t.forward(radius * 4)
    t.right(90)
    t.forward(radius * 3)
    
    

turtle1 = turtle.Turtle()
turtle1.speed(10)


draw_teaguk(turtle1, numangle, length, radius)
draw_gun(turtle1, numangle, length, radius)
draw_gon(turtle1, numangle, length, radius)
draw_gam(turtle1, numangle, length, radius)
draw_ri(turtle1, numangle, length, radius)
paper(turtle1, numangle, length, radius)

turtle.done()