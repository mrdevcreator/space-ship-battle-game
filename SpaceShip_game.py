from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
from midpoint import *


class Game:
    WINDOW_WIDTH, WINDOW_HEIGHT = 600, 800
    PLAYER_WIDTH, PLAYER_HEIGHT = 35, 56
    SHIP_SIZE = 80
    POINTS =  [(random.uniform(0,600), random.uniform(0,800)) for _ in range(100)]
    def __init__(self):
        self.boss = False        
        self.Boss1right = False
        self.hit_count_ship1 = 0
        self.hit_count_ship2 = 0
        self.hit_count_ship3 = 0
        self.hit_count_ship6 = 0
        self.hit_count_ship8 = 0
        self.hit_count_ship4 = 0

        self.player_x = (self.WINDOW_WIDTH - self.PLAYER_WIDTH) // 2
        self.player_y = 150
        self.ship1_x, self.ship1_y = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE ), (
                    self.WINDOW_HEIGHT - 100) 
        if ((self.WINDOW_WIDTH//2)-50 <= self.ship1_x <= (self.WINDOW_WIDTH//2)+50) or (self.ship1_x == (self.WINDOW_WIDTH//2 )):
            self.ship2_x  = random.choice([self.SHIP_SIZE+10, self.WINDOW_WIDTH-(self.SHIP_SIZE+10)])
        else:
            if self.ship1_x< (self.WINDOW_WIDTH//2):
                self.ship2_x = random.randint((self.WINDOW_WIDTH//2+10 - self.SHIP_SIZE), (self.WINDOW_WIDTH - self.SHIP_SIZE ))
            else:
                self.ship2_x = random.randint(0, self.WINDOW_WIDTH//2 - self.SHIP_SIZE)
        self.ship2_y = (self.WINDOW_HEIGHT - 100)

        self.ship3_x, self.ship3_y = random.randint(self.SHIP_SIZE, self.WINDOW_WIDTH - self.SHIP_SIZE ), (
                    self.WINDOW_HEIGHT - 100) 
        self.ship6_x, self.ship6_y = random.randint(self.SHIP_SIZE, self.WINDOW_WIDTH - self.SHIP_SIZE ), (
                    self.WINDOW_HEIGHT - 100)

        self.ship2_speed = 1.2
        self.ship1_speed = 1.0
        self.ship6_speed = 1.0
        self.score = 0
        self.game_over = False
        self.paused = False
        self.collision = 0
        self.life = 5
        self.bullets = []
        self.space_pressed = False
        x_center, y_center = self.ship3_x, self.ship3_y - self.SHIP_SIZE // 4
        self.bomb = [self.ship3_x, self.ship3_y]
        self.color_offset = 0
        self.level = 1
        self.hitpoint = {'l1':1,'l2':2,'l3':3}
        self.lv = [1,1,1]
        self.highest_score = 0


    def resetAll(self):
        self.boss = False        
        self.Boss1right = False
        self.hit_count_ship1 = 0
        self.hit_count_ship2 = 0
        self.hit_count_ship3 = 0
        self.hit_count_ship6 = 0
        self.hit_count_ship8 = 0
        self.hit_count_ship4 = 0

        self.player_x = (self.WINDOW_WIDTH - self.PLAYER_WIDTH) // 2
        self.player_y = 150
        self.ship1_x, self.ship1_y = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE ), (
                    self.WINDOW_HEIGHT - 100) 
        if ((self.WINDOW_WIDTH//2)-50 <= self.ship1_x <= (self.WINDOW_WIDTH//2)+50) or (self.ship1_x == (self.WINDOW_WIDTH//2 )):
            self.ship2_x  = random.choice([self.SHIP_SIZE+10, self.WINDOW_WIDTH-(self.SHIP_SIZE+10)])
        else:
            if self.ship1_x< (self.WINDOW_WIDTH//2):
                self.ship2_x = random.randint((self.WINDOW_WIDTH//2+10 - self.SHIP_SIZE), (self.WINDOW_WIDTH - self.SHIP_SIZE ))
            else:
                self.ship2_x = random.randint(0, self.WINDOW_WIDTH//2 - self.SHIP_SIZE)
        self.ship2_y = (self.WINDOW_HEIGHT - 100)

        self.ship3_x, self.ship3_y = random.randint(self.SHIP_SIZE, self.WINDOW_WIDTH - self.SHIP_SIZE ), (
                    self.WINDOW_HEIGHT - 100) 
        self.ship6_x, self.ship6_y = random.randint(self.SHIP_SIZE, self.WINDOW_WIDTH - self.SHIP_SIZE ), (
                    self.WINDOW_HEIGHT - 100)


        self.ship2_speed = 1.2
        self.ship1_speed = 1.0
        self.ship6_speed = 1.0
        self.score = 0
        self.game_over = False
        self.paused = False
        self.collision = 0
        self.life = 5
        self.bullets = []
        
        self.space_pressed = False

        
        x_center, y_center = self.ship3_x, self.ship3_y - self.SHIP_SIZE // 4
        self.bomb = [self.ship3_x, self.ship3_y]


        self.color_offset = 0
        self.level = 1

        self.hitpoint = {'l1':1,'l2':2,'l3':3}

        self.lv = [0,0,0]
    def is_point_inside(self,x, y,button_type):
        if button_type == "x":
            x2,y2 = (self.WINDOW_WIDTH-30),25
            if ((x-x2)**2)+((y-y2)**2) <= (22**2):
                return True
            else:
                return False
        elif button_type == "||":
            x2,y2 = (self.WINDOW_WIDTH//2),25
            if ((x-x2)**2)+((y-y2)**2) <= (22**2):
                return True
            else:
                return False
        elif button_type == "<-":
            x2,y2 = 20,25
            if ((x-x2)**2)+((y-y2)**2) <= (22**2):
                return True
            else:
                return False
        elif button_type == ".":
            x2,y2 = self.player_x+16, self.player_y-53
            if ((x-x2)**2)+((y-y2)**2) <= (54**2):
                return True
            else:
                return False
        else:
            x2,y2 = self.player_x+16, self.player_y-56
            if ((x-x2)**2)+((y-y2)**2) <= (52**2):
                return True
            else:
                return False

    def MoveFire1Points(self):
        for i in range(len(self.bullets)):
            self.bullets[i] = (self.bullets[i][0], self.bullets[i][1] + 10)
       
        fire2 = []
        i = 0
        while True:
            if i == len(self.bullets):
                break
            if self.bullets[i][1] < self.WINDOW_HEIGHT:  
                fire2.append(self.bullets[i])
            i += 1

        self.bullets = fire2.copy()

    def Player1Fire(self):
        if len(self.bullets) < 300:
            self.bullets.append((self.player_x + self.PLAYER_WIDTH // 2, self.player_y + self.PLAYER_HEIGHT))
        else:
            self.bullets = [(self.player_x + self.PLAYER_WIDTH // 2, self.player_y + self.PLAYER_HEIGHT)]
        self.MoveFire1Points() 
 
    def Boss1Fire(self):
        if not self.paused and not self.game_over:
            self.draw_bomb()
            if self.level == 1:
                self.bomb[1] -= 3
            elif self.level == 2:
                self.bomb[1] -= 4
            else:
                self.bomb[1] -= 5

    def draw_bomb(self):
        self.bomb[0] = self.ship3_x
        if self.bomb[1] <= 0:
            self.bomb[1] = self.ship3_y - self.SHIP_SIZE // 4
        
        x,y = self.bomb[0]+40,self.bomb[1]

        midpoint_cir = MidpointCircle()
        midpoint_line = MidpointLine()
        midpoint_line.midpoint(x,y+18,x,y+21,[1.0,1.0,0.0],3)
        self.draw_oval(x,y+12,6,6,midpoint_line,[1.0,0.0,0.0],0,180)
        midpoint_cir.filled_circle(12,x,y)
        
    def draw_bullets(self,color,size):
        glPointSize(size)
        glBegin(GL_POINTS)
        glColor3f(*color) 
        for bullet in self.bullets:
            x, y = bullet
            if y > self.WINDOW_HEIGHT + 50:
                if len(self.bullets) != 0:
                  self.bullets.remove(bullet)
            else:
                glVertex2f(x, y)
        glEnd()
        self.MoveFire1Points()

    def drawBackground(self):
        glColor3f(0.7,0.7,0.7)
        glPointSize(2)
        glBegin(GL_POINTS)
        for x,y in self.POINTS:
            glVertex2f(x, y)  
        
        glEnd()

    def draw_x(self, midpoint_line):
        color = [1.0, 0.0, 0.0]

        x1, y1 = self.WINDOW_WIDTH - 35, self.WINDOW_HEIGHT - 35
        x2, y2 = self.WINDOW_WIDTH - 8, self.WINDOW_HEIGHT - 8
        midpoint_line.midpoint(x1, y1, x2, y2, color,1)

        x3, y3 = self.WINDOW_WIDTH - 35, self.WINDOW_HEIGHT - 8
        x4, y4 = self.WINDOW_WIDTH - 8, self.WINDOW_HEIGHT - 35
        midpoint_line.midpoint(x3, y3, x4, y4, color,1)

    def draw_arrow(self, midpoint_line):
        color = [0.0, 1.0, 0.0]
        x1, y1 = self.WINDOW_WIDTH - (self.WINDOW_WIDTH - 25), self.WINDOW_HEIGHT - 9
        x2, y2 = self.WINDOW_WIDTH - (self.WINDOW_WIDTH - 25), self.WINDOW_HEIGHT - 35

        x3, y3 = self.WINDOW_WIDTH - (self.WINDOW_WIDTH - 8), self.WINDOW_HEIGHT - 22
        midpoint_line.midpoint(x1, y1, x3, y3, color,1)
        midpoint_line.midpoint(x3 - 0.2, y3 - 0.2, x2, y2, color,1)
        midpoint_line.midpoint(x3, y3, x2 + 20, y3, color,1)

    def draw_button(self, midpoint_line, is_play):
        color = [0.9, 0.5, 0.3]

        if not is_play:
            x1, y1 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) - 6), self.WINDOW_HEIGHT - 8
            x2, y2 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) - 6), self.WINDOW_HEIGHT - 35
            midpoint_line.midpoint(x1, y1, x2, y2, color,1)

            x3, y3 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 6), self.WINDOW_HEIGHT - 8
            x4, y4 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 6), self.WINDOW_HEIGHT - 36
            midpoint_line.midpoint(x3, y3, x4, y4, color,1)
        else:
            x1, y1 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 15), self.WINDOW_HEIGHT - 8
            x2, y2 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) + 15), self.WINDOW_HEIGHT - 36
            midpoint_line.midpoint(x1, y1, x2, y2, color,1)

            x3, y3 = self.WINDOW_WIDTH - ((self.WINDOW_WIDTH // 2) - 15), self.WINDOW_HEIGHT - 22
            midpoint_line.midpoint(x1, y1, x3, y3, color,1)
            midpoint_line.midpoint(x3, y3, x2 - 0.5, y2 - 0.5, color,1)

    def draw_oval(self,x_center,y_center,radius_x,radius_y,midpoint_line,color_body,start_degree, end_degree):
        angle = start_degree
        while angle <= end_degree:
            x = int(x_center + radius_x * math.cos(math.radians(angle)))
            y = int(y_center + radius_y * math.sin(math.radians(angle)))
            midpoint_line.midpoint(x, y, x, y, color_body,1)
            angle += 1

    def draw_enemy_ship(self, midpoint_line,midpoint_cir):
        
        color_body = [1.0, 0.9, 0.0]
        color_window = [1.0, 0.0, 0.0]
        x_center, y_center = self.ship1_x + self.SHIP_SIZE // 2, self.ship1_y - self.SHIP_SIZE // 4
        radius_x, radius_y = self.SHIP_SIZE // 2, self.SHIP_SIZE // 4

        #Head
        self.draw_oval(x_center,y_center+15,radius_x-18,radius_y+24,midpoint_line,color_window,10,170)

        #Body
        self.draw_oval(x_center,y_center+7,radius_x+7,radius_y-5,midpoint_line,color_body,192,348)
        self.draw_oval(x_center,y_center,radius_x+7,radius_y-1,midpoint_line,color_body,178,362)
        midpoint_line.midpoint(x_center + 46, y_center+3, x_center + 25, y_center + 20, color_body,2)
        midpoint_line.midpoint(x_center - 46, y_center+3, x_center - 25, y_center + 20, color_body,2)
        midpoint_line.midpoint(x_center - 25, y_center + 20,x_center + 25, y_center + 20, color_body,2)

        # Window
        midpoint_cir.filled_circle(5, x_center-21, y_center+6 )
        midpoint_cir.filled_circle(5, x_center+21, y_center+6 )
        midpoint_cir.filled_circle(5, x_center, y_center+5)

        # Legs
        midpoint_line.midpoint(x_center - 15, y_center - 14, x_center - 21, y_center - 30, color_window,2)
        midpoint_line.midpoint(x_center + 15, y_center - 14, x_center + 21, y_center - 30, color_window,2)

        midpoint_line.midpoint(x_center - 25, y_center - 12, x_center - 38, y_center - 32, color_window,2)
        midpoint_line.midpoint(x_center + 25, y_center - 12, x_center + 38, y_center - 32, color_window,2)

    def draw_enemy_ship2(self, midpoint_line,midpoint_cir):
        color_body = [1.0, 0.9, 0.0]
        color_window = [1.0, 0.0, 0.0]
        x_center, y_center = self.ship2_x + self.SHIP_SIZE // 2, self.ship2_y - self.SHIP_SIZE // 4
        radius_x, radius_y = self.SHIP_SIZE // 2, self.SHIP_SIZE // 4

        for i in range(2):
          self.draw_oval(x_center,y_center-i,radius_x+7,radius_y-3,midpoint_line,color_body,0,360)
        self.draw_oval(x_center,y_center-15,radius_x-7,radius_y-8,midpoint_line,color_body,0,180)
        midpoint_cir.filled_circle(5, x_center , y_center+5 )
        midpoint_cir.filled_circle(5, x_center-20, y_center+5 )
        midpoint_cir.filled_circle(5, x_center+20, y_center+5 )
        midpoint_cir.filled_circle(5, x_center-37, y_center+1 )
        midpoint_cir.filled_circle(5, x_center+37, y_center+1 )
        
        
        self.draw_oval(x_center,y_center+16,radius_y,radius_y+5,midpoint_line,color_window,0,180)
        self.draw_oval(x_center,y_center+15,radius_y,radius_y+5,midpoint_line,color_window,0,180)

        # Legs
        midpoint_line.midpoint(x_center - 15, y_center - 14, x_center - 21, y_center - 30, color_window,2)
        midpoint_line.midpoint(x_center + 15, y_center - 14, x_center + 21, y_center - 30, color_window,2)

        midpoint_line.midpoint(x_center - 25, y_center - 12, x_center - 38, y_center - 32, color_window,2)
        midpoint_line.midpoint(x_center + 25, y_center - 12, x_center + 38, y_center - 32, color_window,2)

    def draw_enemy_ship3(self, midpoint_line,midpoint_cir):
        color_body = [0.2, 0.5, 0.1]
        color_window = [0.7, 0.3, 1.0]
        color_leg = [1, 1, 1]
        x_center, y_center = self.ship3_x + self.SHIP_SIZE // 2, self.ship3_y - self.SHIP_SIZE // 4
        radius_x, radius_y = self.SHIP_SIZE, self.SHIP_SIZE // 2  # Adjusted ship size

        # Head
        self.draw_oval(x_center, y_center + 30, radius_x - 36, radius_y + 48, midpoint_line, color_window, 10, 170)
        midpoint_line.midpoint(x_center - 40, y_center + 42, x_center + 40, y_center + 42, color_window, 3)

        # Body
        midpoint_line.midpoint(x_center - 40, y_center + 42, x_center + 40, y_center + 42, color_body, 3)
        midpoint_line.midpoint(x_center - 40, y_center + 42, x_center - 70, y_center, color_body, 3)
        midpoint_line.midpoint(x_center + 40, y_center + 42, x_center + 70, y_center, color_body, 3)
        midpoint_line.midpoint(x_center - 70, y_center, x_center + 70, y_center, color_body, 3)
        midpoint_line.midpoint(x_center - 40, y_center, x_center - 40, y_center - 20, color_body, 3)
        midpoint_line.midpoint(x_center + 40, y_center, x_center + 40, y_center - 20, color_body, 3)
        midpoint_line.midpoint(x_center - 40, y_center, x_center + 70, y_center, color_body, 3)
        midpoint_line.midpoint(x_center - 36, y_center - 20, x_center + 36, y_center - 20, color_body, 3)

        # Leg
        midpoint_line.midpoint(x_center - 36, y_center - 28, x_center - 60, y_center - 70, color_leg, 4)
        midpoint_line.midpoint(x_center + 36, y_center - 28, x_center + 60, y_center - 70, color_leg, 4)

        midpoint_line.midpoint(x_center - 20, y_center - 24, x_center - 20, y_center - 64, color_leg, 4)
        midpoint_line.midpoint(x_center + 20, y_center - 24, x_center + 20, y_center - 64, color_leg, 4)

    def ship6(self,midpoint_line, midpoint_cir):

        color_window = [1.0, 0.8, 0.4]
        color_leg = [1, 0, 1]
        x_center, y_center = self.ship6_x + self.SHIP_SIZE // 2, self.ship6_y - self.SHIP_SIZE-30 // 4
        radius_x, radius_y = self.SHIP_SIZE // 2, self.SHIP_SIZE // 4

        #head
        self.draw_oval(x_center, y_center + 35, radius_x - 36, radius_y + 45, midpoint_line, color_window, 10, 170)
        self.draw_oval(x_center, y_center + 45, radius_x - 18, radius_y + 34, midpoint_line, color_window, 10, 170)
        midpoint_line.midpoint(x_center - 45, y_center + 50, x_center - 60, y_center + 55, color_leg, 2)
        midpoint_line.midpoint(x_center+45, y_center+50, x_center+60, y_center+55, color_leg, 2)

        #Body
        midpoint_line.midpoint(x_center-60, y_center+55, x_center, y_center-10, color_leg, 2)
        midpoint_line.midpoint(x_center+60, y_center+55, x_center, y_center-10, color_leg, 2)
        midpoint_line.midpoint(x_center-45, y_center+50, x_center, y_center, color_leg, 2)
        midpoint_line.midpoint(x_center+45, y_center+50, x_center, y_center, color_leg, 2)
        self.draw_oval(x_center, y_center, radius_x , radius_y+30, midpoint_line, color_window, 60, 120)
        self.draw_oval(x_center, y_center, radius_x , radius_y+20, midpoint_line, color_window, 60, 120)
        self.draw_oval(x_center, y_center, radius_x , radius_y+10, midpoint_line, color_window, 60, 120)
        self.draw_oval(x_center, y_center, radius_x , radius_y, midpoint_line, color_window, 65, 115)
        self.draw_oval(x_center, y_center, radius_x , radius_y-10, midpoint_line, color_window, 70, 110)

    def Player1(self, midpoint_line,color,size,no):
      # Body
      x1, y1 = self.player_x + self.PLAYER_WIDTH // 2, self.player_y + 5

      x2, y2 = self.player_x, self.player_y - self.PLAYER_WIDTH // 2
      midpoint_line.midpoint(x1, y1, x2, y2, color,size)

      x3, y3 = self.player_x + self.PLAYER_WIDTH // 2, self.player_y - (self.PLAYER_WIDTH + 5)
      midpoint_line.midpoint(x2, y2, x3, y3, color,size)

      x4, y4 = self.player_x + self.PLAYER_WIDTH, self.player_y - self.PLAYER_WIDTH // 2
      midpoint_line.midpoint(x3, y3, x4, y4, color,size)

      midpoint_line.midpoint(x4, y4, x1, y1, color,size)

      

      x6, y6 = self.player_x, self.player_y-self.PLAYER_HEIGHT - self.PLAYER_WIDTH // 2
      midpoint_line.midpoint(x6, y6, x2, y2, color,size)
      

      x7, y7 = self.player_x + self.PLAYER_WIDTH // 2, self.player_y-self.PLAYER_HEIGHT - (self.PLAYER_WIDTH + 5)
      midpoint_line.midpoint(x6, y6, x7, y7, color,size)

      x8, y8 = self.player_x + self.PLAYER_WIDTH, self.player_y-self.PLAYER_HEIGHT - self.PLAYER_WIDTH // 2
      midpoint_line.midpoint(x7, y7, x8, y8, color,size)
      # mibble and body right
      midpoint_line.midpoint(x8, y8, x4, y4, color,size)
      midpoint_line.midpoint(x7, y7, x3, y3, color,size)


      x9, y9 = self.player_x - 27, self.player_y-self.PLAYER_HEIGHT -50- self.PLAYER_WIDTH // 2
      x10, y10 = self.player_x - 14, self.player_y-self.PLAYER_HEIGHT -60- self.PLAYER_WIDTH // 2
      midpoint_line.midpoint(x6, y6, x9, y9, color,size)
      # bottom left tail
      if no == 3 :
        midpoint_line.midpoint(x6, y6, x10, y10, color,size)
        midpoint_line.midpoint(x9, y9, x10, y10, color,size)

      x11, y11 = self.player_x + 59, self.player_y-self.PLAYER_HEIGHT -50- self.PLAYER_WIDTH // 2
      x12, y12 = self.player_x + 48, self.player_y-self.PLAYER_HEIGHT -60- self.PLAYER_WIDTH // 2
      midpoint_line.midpoint(x8, y8, x11, y11, color,size)
      # bottom right tail
      if no == 3 :
        midpoint_line.midpoint(x8, y8, x12, y12, color,size)
        midpoint_line.midpoint(x12, y12, x11, y11, color,size)
   
      x5, y5 = self.player_x-41 + self.PLAYER_WIDTH // 2, self.player_y-self.PLAYER_HEIGHT 
      x13, y13 = self.player_x-28 + self.PLAYER_WIDTH // 2, self.player_y-self.PLAYER_HEIGHT - 2
      midpoint_line.midpoint(x2, y2, x5, y5, color,size)
      # up left tail
      if no != 1 :
        midpoint_line.midpoint(x2, y2, x13, y13, color,size)
        midpoint_line.midpoint(x5, y5, x13, y13, color,size)
      x14,x15 = self.player_x + 61 , self.player_x + 49

      midpoint_line.midpoint(x4, y4, x14, y5, color,size)
      # up right tail
      if no != 1 :
        midpoint_line.midpoint(x4, y4, x15, y13, color,size)
        midpoint_line.midpoint(x14, y5, x15, y13, color,size)

    def has_collided(self, box1, box2):
        return box1[0] < box2[0] + box2[2] and \
               box1[0] + box1[2] > box2[0] and \
               box1[1] < box2[1] + box2[3] and \
               box1[1] + box1[3] > box2[1]
    
    def theme(self):
        if not self.paused and not self.game_over:
            glClearColor(self.color_offset,self.color_offset,self.color_offset,self.color_offset)
        
            if self.color_offset >= 0.15:
                self.color_offset = 0
            else:
                self.color_offset += 0.0001
            
    def display(self):
        self.theme()
        for bullet in self.bullets:
            # Check collision with the first enemy ship
            if not self.boss:
                if self.has_collided([bullet[0], bullet[1], 0, 0],
                                [self.ship1_x, self.ship1_y - self.SHIP_SIZE, self.SHIP_SIZE, self.SHIP_SIZE]):
                
                    self.hit_count_ship1 += 1
                    if len(self.bullets) != 0:
                      self.bullets.remove(bullet)

                    if self.hit_count_ship1 == 20:
                        self.score += 1
                        print("Score:", self.score)
                        self.hit_count_ship1 = 0
                        self.ship1_y = (self.WINDOW_HEIGHT - 20)
                        self.ship1_x = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE)
                        self.ship1_speed += 0.2
            # Check collision with the second enemy ship
            if not self.boss:
                if self.has_collided([bullet[0], bullet[1], 0, 0],
                                    [self.ship2_x, self.ship2_y - self.SHIP_SIZE, self.SHIP_SIZE, self.SHIP_SIZE]):
                    self.hit_count_ship2 += 1
                    if len(self.bullets) != 0:
                      self.bullets.remove(bullet)
                    

                    if self.hit_count_ship2 == 20:
                        self.score += 1
                        print("Score:", self.score)
                        self.hit_count_ship2 = 0
                        if ((self.WINDOW_WIDTH//2)-50 <= self.ship1_x <= (self.WINDOW_WIDTH//2)+50) or (self.ship1_x == (self.WINDOW_WIDTH//2 )):
                            self.ship2_x  = random.choice([self.SHIP_SIZE+10, self.WINDOW_WIDTH-(self.SHIP_SIZE+10)])
                        else:
                            if self.ship1_x< (self.WINDOW_WIDTH//2):
                                self.ship2_x = random.randint((self.WINDOW_WIDTH//2+10 - self.SHIP_SIZE), (self.WINDOW_WIDTH - self.SHIP_SIZE ))
                            else:
                                self.ship2_x = random.randint(0, self.WINDOW_WIDTH//2 - self.SHIP_SIZE)   
                        self.ship2_y = (self.WINDOW_HEIGHT - 20)
                        self.ship2_speed += 0.2

            # Check collision with the third enemy ship
            if self.boss:
                if self.has_collided([bullet[0], bullet[1], 0, 0],
                                [self.ship3_x, self.ship3_y - self.SHIP_SIZE, self.SHIP_SIZE, self.SHIP_SIZE]):
                    self.hit_count_ship3+= 1
                    if len(self.bullets) != 0:
                      self.bullets.remove(bullet)
                    if self.level == 1:
                        a = 450
                    elif self.level == 2:
                        a = 480
                    elif self.level >= 3:
                        a = 500

                    if self.hit_count_ship3 == a: 
                       self.score += 20
                       print("Score:" ,self.score)
                       self.hit_count_ship3 = 0
                       self.boss = False

            # Check collision with the 6th enemy ship
            if not self.boss:
                if self.has_collided([bullet[0], bullet[1], 0, 0],
                                    [self.ship6_x, self.ship6_y - self.SHIP_SIZE, self.SHIP_SIZE, self.SHIP_SIZE]):

                    self.hit_count_ship6 += 1
                    if len(self.bullets) != 0:
                      self.bullets.remove(bullet)
                    a = 200
                    if self.level == 1:
                        a = 200
                    elif self.level == 2:
                        a = 220
                    elif self.level >= 3:
                        a = 230
                    if self.hit_count_ship6 == a:
                        self.score += 3
                        print("Score:", self.score)
                        self.hit_count_ship6 = 0
                        self.ship6_y = (self.WINDOW_HEIGHT - 20)
                        self.ship6_x = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE)
                        self.ship6_speed += 0.2
        
        if self.boss:
            if self.is_point_inside(self.bomb[0], self.bomb[1], ".."):
                    self.collision += 1
                    print(f'Life left - {self.life-self.collision}')
                    self.bomb[0] = self.ship3_x
                    self.bomb[1] = self.ship3_y - self.SHIP_SIZE // 4
                    
                
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.reshape()
        
        if not self.game_over and not self.paused:
            self.ship1_y -= self.ship1_speed
            self.ship2_y -= self.ship2_speed
            self.ship6_y -= self.ship6_speed


            if self.ship3_x <= 0 and self.score > 6:
                self.Boss1right = True
                
            elif self.ship3_x >= self.WINDOW_WIDTH- self.SHIP_SIZE and self.score > 6:
                self.Boss1right = False 
            if self.Boss1right and self.score > 6:
                self.ship3_x += 1
            elif not self.Boss1right and self.score > 6:
                self.ship3_x -= 1

            if self.collision== 5:
                self.game_over = True
                print(f"Game over!! Your Score = {self.score}")
                if self.highest_score <= self.score:
                    self.highest_score = self.score
                    print('New Highest Score !!!')
            else:
                x_center, y_center = self.ship2_x + self.SHIP_SIZE // 2, self.ship2_y - self.SHIP_SIZE // 4
                x1_center, y1_center = self.ship1_x + self.SHIP_SIZE // 2, self.ship1_y - self.SHIP_SIZE // 4
                x3_center, y3_center = self.ship6_x + self.SHIP_SIZE // 2, self.ship6_y - self.SHIP_SIZE-30 // 4
                
                ax = 42
                ay = 16
                if not self.boss and (self.is_point_inside(x_center-ax,y_center-ay,".") or self.is_point_inside(x_center+ax,y_center-ay,".") or self.is_point_inside(x_center,y_center-ax,".") or self.is_point_inside(x1_center-ax,y1_center-ay,".") or self.is_point_inside(x1_center+ax,y1_center-ay,".") or self.is_point_inside(x1_center,y1_center-ay,".") or (self.is_point_inside(x3_center-15,y3_center-8,".") or self.is_point_inside(x3_center+15,y3_center-8,"." or self.is_point_inside(x3_center,y3_center-14,".")))):

                    self.collision+=1
                    print(f'Life left - {self.life-self.collision}')
                    # Regenatrating the ships when has any collision
                    self.ship1_y = (self.WINDOW_HEIGHT - 20)
                    self.ship2_y = (self.WINDOW_HEIGHT - 20)
                    self.ship1_x = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE )
                    self.ship6_y = (self.WINDOW_HEIGHT - 20)
                    self.ship6_x = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE)
                    if ((self.WINDOW_WIDTH//2)-50 <= self.ship1_x <= (self.WINDOW_WIDTH//2)+50) or (self.ship1_x == (self.WINDOW_WIDTH//2 )):
                        self.ship2_x  = random.choice([self.SHIP_SIZE+10, self.WINDOW_WIDTH-(self.SHIP_SIZE+10)])
                    else:
                        if self.ship1_x< (self.WINDOW_WIDTH//2):
                            self.ship2_x = random.randint((self.WINDOW_WIDTH//2+10 - self.SHIP_SIZE), (self.WINDOW_WIDTH - self.SHIP_SIZE ))
                        else:
                            self.ship2_x = random.randint(0, self.WINDOW_WIDTH//2 - self.SHIP_SIZE)

                # Regenatrating the ship 1 and 2 when leaves the window         
                elif ((self.ship1_y+self.SHIP_SIZE ) <= 0) or  ((self.ship2_y+self.SHIP_SIZE ) <= 0):
                    self.ship1_y = (self.WINDOW_HEIGHT - 20)
                    self.ship2_y = (self.WINDOW_HEIGHT - 20)
                    self.ship1_x = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE )
                    if ((self.WINDOW_WIDTH//2)-50 <= self.ship1_x <= (self.WINDOW_WIDTH//2)+50) or (self.ship1_x == (self.WINDOW_WIDTH//2 )):
                        self.ship2_x  = random.choice([self.SHIP_SIZE+10, self.WINDOW_WIDTH-(self.SHIP_SIZE+10)])
                    else:
                        if self.ship1_x< (self.WINDOW_WIDTH//2):
                            self.ship2_x = random.randint((self.WINDOW_WIDTH//2+10 - self.SHIP_SIZE), (self.WINDOW_WIDTH - self.SHIP_SIZE ))
                        else:
                            self.ship2_x = random.randint(0, self.WINDOW_WIDTH//2 - self.SHIP_SIZE)
                # Regenatrating the ship 3 when leaves the window
                elif ((self.ship6_y+self.SHIP_SIZE ) <= 0):
                    self.ship6_y = (self.WINDOW_HEIGHT - 20)
                    self.ship6_x = random.randint(1, self.WINDOW_WIDTH - self.SHIP_SIZE)
            
        midpoint_line = MidpointLine()
        midpoint_cir = MidpointCircle()

        if self.space_pressed and not self.paused and not self.game_over:
            self.Player1Fire()
        
        if not self.boss:
          self.draw_enemy_ship(midpoint_line,midpoint_cir)
          self.draw_enemy_ship2(midpoint_line,midpoint_cir) 
 
        if not self.boss and (self.score!= 0  and (self.score % 20 == 0 or self.score % 20 == 1 or self.score % 20 == 2)):
            self.ship6(midpoint_line,midpoint_cir)

        
        if (self.score > 7 and  (self.score % 25 == 0 or self.score % 25 == 1)) :
            self.boss = True
            self.draw_enemy_ship3(midpoint_line,midpoint_cir)
            self.Boss1Fire()

        if self.lv[0] == 1:
              print('Level 1 started!')
              self.lv[0] = 0

        if self.score <= 30:
          self.Player1(midpoint_line,[1.0, 1.0, 1.0],3,1)
          self.draw_bullets([1.0, 0.0, 0.0],5)
          self.level = 1
        elif self.score <= 60:
          self.Player1(midpoint_line,[1.0, 1.0, 0.0],4,2)
          self.draw_bullets([1.0, 1.0, 1.0],6)
          self.level = 2
          if self.lv[1] == 1:
              print('Level 2 started!')
              self.lv[1] = 0
         
        elif self.score  > 60:
          self.Player1(midpoint_line,[0.0, 1.0, 1.0],5,3)
          self.draw_bullets([0.0, 0.0, 1.0],9)
          self.level = 3
          if self.lv[2] == 1:
              print('Level 3 started!')
              self.lv[2] = 0
        
        self.draw_x(midpoint_line)
        self.draw_button(midpoint_line, self.paused)
        self.draw_arrow(midpoint_line)
        self.drawBackground()

        glutSwapBuffers()

    def reshape(self):
        glViewport(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.WINDOW_WIDTH, 0,self.WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def special_keys(self, key, x, y):
        speed = 12
        if key == GLUT_KEY_LEFT and self.player_x > 0 and not self.game_over and not self.paused:
            self.player_x -= speed
        elif key == GLUT_KEY_RIGHT and self.player_x < self.WINDOW_WIDTH - self.PLAYER_WIDTH and not self.game_over and not self.paused:
            self.player_x += speed
        elif key == GLUT_KEY_UP and self.player_y < self.WINDOW_HEIGHT//2 and not self.game_over and not self.paused:
            self.player_y += speed
        elif key == GLUT_KEY_DOWN and self.player_y > self.WINDOW_HEIGHT-(self.WINDOW_HEIGHT - 100) - self.PLAYER_HEIGHT and not self.game_over and not self.paused:
            self.player_y -= speed

    def update(self, value):
        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0) 

    def mouse_callback(self,button, state, x, y):
      if (state == GLUT_DOWN):
        if self.is_point_inside(x,y,"x"):
          glutDestroyWindow(glutGetWindow())
          print(f"Goodbye")
        elif self.is_point_inside(x,y,"||"):
            self.paused = not self.paused
        elif self.is_point_inside(x,y,"<-"):
            print("Starting Over !")
            self.resetAll()

    def keyboardListener(self,key,x,y):
        if key==b' ':
           self.space_pressed = True

    def keyboardUpListener(self, key, x, y):
        if key == b' ':
           self.space_pressed = False

    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow(b"Catch the Diamonds!")  
        glutDisplayFunc(self.display) 
        glutSpecialFunc(self.special_keys)  
        glutMouseFunc(self.mouse_callback) 
        glutKeyboardFunc(self.keyboardListener)
        glutKeyboardUpFunc(self.keyboardUpListener)
        glutTimerFunc(25, self.update, 0)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glutMainLoop()        

if __name__ == "__main__":
    game_instance = Game()
    game_instance.main()