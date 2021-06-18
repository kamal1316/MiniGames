#For Graphics
import turtle

window = turtle.Screen()
window.title("Pong")
window.bgcolor("black")
window.setup(width = 800, height = 600)
#stops the window from automatic updating
window.tracer(0)

#Score
score_a = 0
score_b = 0

#Left Paddle
paddle_a = turtle.Turtle()
#Speed of the animation
paddle_a.speed(2)
paddle_a.shape("square")
paddle_a.color("white")
#width = 5 * 20, length = 1 * 20
paddle_a.shapesize(stretch_wid = 5, stretch_len = 1)
paddle_a.penup()
paddle_a.goto(-350, 0)

#Right Paddle
paddle_b = turtle.Turtle()
#Speed of the animation
paddle_b.speed(2)
paddle_b.shape("square")
paddle_b.color("white")
#width = 5 * 20, lenght = 1 * 20
paddle_b.shapesize(stretch_wid = 5, stretch_len = 1)
paddle_b.penup()
paddle_b.goto(350, 0)

#Ball
ball = turtle.Turtle()
#Speed of the animation
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
#Every time balls move by 2 pixels
ball.dx = 0.8
ball.dy = 0.8

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("PlayerA: {}  PlayerB: {}".format(score_a, score_b), align = "center", font = ("Courier", 24, "normal"))

#Functions
def paddle_a_up() :
    y = paddle_a.ycor()
    y += 20
    y = min(y, 230)
    paddle_a.sety(y)

def paddle_a_down() :
    y = paddle_a.ycor()
    y -= 20
    y = max(y, -230)
    paddle_a.sety(y)

def paddle_b_up() :
    y = paddle_b.ycor()
    y += 20
    y = min(y, 230)
    paddle_b.sety(y)

def paddle_b_down() :
    y = paddle_b.ycor()
    y -= 20
    y = max(y, -230)
    paddle_b.sety(y)

#Keyboard binding
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

#Main game Loop
while True :
    window.update()

    #Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #Border Checking
    if ball.ycor() > 280 :
        ball.sety(280)
        ball.dy *= -1

    if ball.ycor() < -280 :
        ball.sety(-280)
        ball.dy *= -1

    if ball.xcor() > 380 :
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1

    if ball.xcor() < -380 :
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1

    #Paddle and ball collisions
    if (ball.xcor() <= -330 and ball.xcor() >= -340) and\
            (ball.ycor() >= paddle_a.ycor() - 50 and ball.ycor() <= paddle_a.ycor() + 50):
        ball.dx *= -1

    if (ball.xcor() >= 330 and ball.xcor() <= 340) and\
            (ball.ycor() >= paddle_b.ycor() - 50 and ball.ycor() <= paddle_b.ycor() + 50):
        ball.dx *= -1

    pen.clear()
    pen.write("PlayerA: {}  PlayerB: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

