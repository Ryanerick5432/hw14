import turtle, random, math
# additional function: creating all text on turtle window, stopping turning and fuel consumption after the game ends, a background, an explosion when crashing, a loop on either side of the screen, a game loss when going too high, and creating the moon
class Game:
    '''
    Purpose: plays a spacecraft game, contains the controls
    Instance vars: self = initializing variable
        self.player = the game spacecraft object
    Methods: init = initializes and runs the game
    '''
    def __init__(self):
        #Bottom left corner of screen is (0, 0)
        #Top right corner is (500, 500)
        turtle.setworldcoordinates(0, 0, 500, 500)
        cv = turtle.getcanvas()
        cv.adjustScrolls()

        #Ensure turtle is running as fast as possible
        turtle.delay(0)
        sx = random.uniform(100,400)
        sy = random.uniform(250,450)
        svx = random.uniform(-4,4)
        svy =random.uniform(-2,0)
        self.player = SpaceCraft(sx, sy, svx ,svy)
        #for i in range(0,10):
        #    self.a1 = obs(random.uniform(50,450), random.uniform(100,490), sx, sy, svx,svy)
        #    self.a1.gameloop()
        self.player.gameloop()
        surf()
        turtle.onkeypress(self.player.thrust, 'Up')
        turtle.onkeypress(self.player.left_turn,'Left')
        turtle.onkeypress(self.player.right_turn, 'Right')
        
        #These two lines must always be at the BOTTOM of __init__
        turtle.listen()
        turtle.mainloop()


class SpaceCraft(turtle.Turtle):
    '''
    Purpose: moves and changes the movement of the spacecraft "player" in the game class
    Instance variables:
        self = the initializing variable
        xpos = initial xposition
        ypos = initial y
        xvel = initial (and changing) velocity in x dir
        yvel = initial y velocity
        self.fuel = the starting fuel amount to consume
        self.alive = determines whether the game is active to prevent fuel consumption post game
        self.a_s = list of asteroids
        self.turt = turtle object for writing words
    Methods: init = initializes values and location of spacecraft, and runs through asteroid and star creation
    move = moves the spacecraft according to its velocity in the 'gravity' field per each call
    gameloop = loops the move function to create continuous gravity, as well as loops movement of each asteroid, and checks for collision
    thrust = accelerates the velocity of the spacecraft by a set amount in the direction faced and depletes one fuel
    left_turn = turns the spacecraft 15 degrees left and depletes a fuel
    right_turn: turns the spacecraft 15 degrees right and depletes a fuel
    '''
    def __init__(self,xpos,ypos,xvel,yvel):
        turtle.Turtle.__init__(self)
        turtle.bgcolor('black')
        self.x = xpos
        self.y = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.fuel = 40
        self.alive = True
        self.color('white')
        self.left(90)
        self.penup()
        self.speed = 0
        self.goto(self.x,self.y)
        self.turtlesize(2)
        self.pendown()
        self.turt = turtle
        self.a_s = []
        for i in range(0,15):
            self.a_s.append(obs(random.uniform(50,450), random.uniform(100,490)))
        for i in range(0,50):
            star(random.uniform(3,497), random.uniform(30, 497))

        #turtle.exitonclick()
    def move(self):
        self.yvel -= 0.0486
        self.x = self.xcor() + self.xvel
        self.y = self.ycor() + self.yvel
        self.goto(self.x, self.y)
        if self.xcor() > 500:
            self.penup()
            self.goto(0,self.ycor())
            self.pendown()
        if self.xcor() < 0:
            self.penup()
            self.goto(500,self.ycor())
            self.pendown()
    def gameloop(self):
        d = []
        for i in range(len(self.a_s)):
            d.append(math.sqrt((self.xcor()-self.a_s[i].xcor())**2+(self.ycor()-self.a_s[i].ycor())**2))
        if self.ycor() <= 20:
            if self.xvel < 3 and self.xvel > -3 and self.yvel < 3 and self.yvel > -3:
                self.turt.goto(250,250)
                self.turt.clear()
                self.turt.hideturtle()
                self.turt.color('green')
                self.turt.write(arg='Successful landing!', align='center', font=('Arial', 30, 'normal'))
                self.alive = 'Win!'
            else:
                self.turt.goto(250,250)
                self.turt.clear()
                self.turt.hideturtle()
                self.turt.color('red')
                self.turt.write(align='center', arg='You crashed!', font=('Arial', 30, 'normal'))
                explode(self.xcor(), self.ycor())
                self.alive = False    
        elif self.ycor() > 600 and self.yvel > 2.5:
                self.turt.goto(250,250)
                self.turt.clear()
                self.turt.hideturtle()
                self.turt.color('red')
                self.turt.write(arg='Mission Fail (left orbit)', align='center', font=('Arial', 30, 'normal'))
                self.alive = 'loss'
        else:
            for i in range(len(d)):
                if d[i] < 8:
                    self.turt.goto(250,250)
                    self.turt.clear()
                    self.turt.hideturtle()
                    self.turt.color('red')
                    self.turt.write(align='center', arg='You crashed!', font=('Arial', 30, 'normal'))
                    explode(self.xcor(), self.ycor())
                    self.alive = False
                    return 
            for i in range(len(self.a_s)):
                self.a_s[i].move()
            self.move()
            turtle.ontimer(self.gameloop, 30)
    def thrust(self):
        if self.alive == True:
            if self.fuel != 0:
                self.xvel += math.cos(math.radians(self.heading()))
                self.yvel += math.sin(math.radians(self.heading())) 
                self.turt.clear()
                self.turt.color('blue')
                self.turt.hideturtle()
                self.turt.penup()
                self.turt.goto(450,450)
                self.turt.write(f'{self.fuel} gallons of fuel remaining!', align='right')
                self.fuel -= 1
            else:
                self.turt.clear()
                self.turt.color('red')
                self.turt.hideturtle()
                self.turt.write('Out of Fuel!', align='right')
    def left_turn(self):
        if self.alive == True:
            if self.fuel != 0:
                self.left(15)
                self.turt.clear()
                self.turt.color('blue')
                self.turt.hideturtle()
                self.turt.penup()
                self.turt.goto(450,450)
                self.turt.write(f'{self.fuel} gallons of fuel remaining!', align='right')
                self.fuel -= 1
            else:
                self.turt.clear()
                self.turt.color('red')
                self.turt.hideturtle()
                self.turt.write('Out of Fuel!', align='right')
    def right_turn(self):
        if self.alive == True:
            if self.fuel != 0:
                self.right(15)
                self.turt.clear()
                self.turt.color('blue')
                self.turt.hideturtle()
                self.turt.penup()
                self.turt.goto(450,450)
                self.turt.write(f'{self.fuel} gallons of fuel remaining!', align='right')
                self.fuel -= 1
            else:
                self.turt.clear()
                self.turt.color('red')
                self.turt.hideturtle()
                self.turt.write('Out of Fuel!', align='right')
class obs(SpaceCraft):
    '''
    Purpose: creates obstacle for the player to avoid
    instance vars:
        self: initializing variable (the asteroid)
        self.xv = initial x val of asteroid
        self.xy = initial y val of asteroid
        self.yvel = velocity downwards of the asteroid, increasing over time
    Methods:
    init: initializes the variables
    move: moves the asteroid according to gravity, and resets it to the top if it goes off screen
    '''
    def __init__(self, x,y,):
        turtle.Turtle.__init__(self)
        SpaceCraft.end = False
        
        self.xv = x
        self.yv = y
        self.yvel = 0
        self.shape('circle')
        self.color('blue')
        self.turtlesize(0.6)
        self.penup()
        self.goto(self.xv,self.yv)
        self.speed = 0
    def move(self):
        self.yvel -= 0.0486
        x = self.xcor()
        y = self.ycor() + self.yvel
        self.goto(x, y)
        if y < 25:
            self.goto(self.xv,500)
            

class surf(turtle.Turtle):
    '''
    Purpose: creates the surface of the moon
    init vars: self = initializes the turtle
    methods: init: creates the surface of the moon
    '''
    def __init__(self):
      turtle.Turtle.__init__(self)
      self.hideturtle()
      self.fillcolor('gray')
      self.begin_fill()
      self.penup()
      self.goto(-20,20)
      self.pendown()
      self.goto(520,20)
      self.goto(520,-10)
      self.goto(-20,-10) 
      self.end_fill()
class star(turtle.Turtle):
    '''
    Purpose: creates a background of stars
    init vars: self, initializing var
    method: init, creates a star
    '''
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
    
        self.penup()
        self.shape('circle')
        self.color('yellow')
        self.turtlesize(0.4)
        self.goto(x,y)
        self.speed = 0
        
class explode(turtle.Turtle):
    '''
    Purpose: creates an explosion when the ship crashes
    init vars: boom 0-5, different shapes for the explosion
    method: init: creates the explosion
    '''
    def __init__(self, xcor, ycor):
        turtle.Turtle.__init__(self)
        boom = turtle.Turtle()
        boom2 = turtle.Turtle()
        boom3 = turtle.Turtle()
        boom4 = turtle.Turtle()
        boom5 = turtle.Turtle()

        boom2.penup()
        boom2.shape('triangle')
        boom2.color('orange')
        boom2.turtlesize(3.1,3)
        boom2.goto(xcor+5,ycor)

        boom3.penup()
        boom3.shape('triangle')
        boom3.color('yellow')
        boom3.turtlesize(3, 2)
        boom3.goto(xcor-6,ycor-3)

        boom4.penup()
        boom4.shape('triangle')
        boom4.color('red')
        boom4.turtlesize(3.3,4)
        boom4.left(30)
        boom4.goto(xcor,ycor)

        boom5.penup()
        boom5.shape('triangle')
        boom5.color('orange')
        boom5.turtlesize(3.3,3.5)
        boom5.right(120)
        boom5.goto(xcor-5,ycor+4)


        boom.penup()
        boom.shape('circle')
        boom.color('yellow')
        boom.turtlesize(2.7)
        boom.left(30)
        boom.goto(xcor-5,ycor+7)

        self.penup()
        self.shape('circle')
        self.color('red')
        self.turtlesize(3)
        self.goto(xcor,ycor)

        



if __name__ == '__main__':
    Game()