from tkinter import *
import time
import math

class Unit :
     def __init__(self, x,y,image,game) :
          self.hp = 0
          self.hpBar = 0
          self.x = x
          self.y = y
          self.image = image
          self.game = game

     def death(self,game) :
          if self.hp <= 0 :
               self.game.endgame()
               self.game.removeunit(self)

     def draw(self, game) :
          game.canvas.create_image(self.x, self.y, anchor = NW, image = self.image)

     def getWidth(self) :
          return self.image.width()

     def getHeight(self) :
          return self.image.height()

     def collision(self, other) :
          p1x = self.x
          p1y = self.y
          p2x = self.x + self.getWidth()
          p2y = self.y + self.getHeight()
          p3x = other.x
          p3y = other.y
          p4x = other.x + other.getWidth()
          p4y = other.y + other.getHeight()
          overlapped = not (p1x>p4x or p2x > p3x or p1y>p4y or p2y<p3y)
          return overlapped

     def handlecollision(self, other) :
          pass

     def move(self, game):
          pass

class Marine(Unit) :
     def __init__(self, x,y,image, game, enemy) :
          super().__init__(x, y, image, game)
          self.attackDamage = 6
          self.attackSpeed = 10
          self.speed = 10
          self.dx = 0
          self.dy = 0
          self.enemy = enemy
          self.hp = 40
          self.armor = 0
          self.movingstate = False
          

     def setDx(self, dx) :
          self.dx = dx

     def setDy(self, dy) :
          self.dy = dy
          
     def getSpeed(self) :
          return self.speed
     
     def steampack(self) :
          time = time.time()
          self.hp = self.hp-10
          while time.time() - time <= 10 :
               self.speed = 20
               self.attackSpeed = 20


     def move(self, game) :
          movingstate = True
          ux,uy = game.x, game.y
          vx = ux - self.x
          vy = uy - self.y
          total = vx**2 + vy**2
          if total != 0 :
               self.dx = self.speed*vx/math.sqrt(total)
               self.dy = self.speed*vy/math.sqrt(total)
          

     def shot(self, other) :
          if not self.movingstate :
               self.enemy.hp = self.enemy.hp - (self.attackDmage-other.armor)

     def ready_to_attack(self) :
          return True

     def attack(self,other,window) :
          distance = math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
          if distance <= 60 :
               self.movingstate = False
               self.shot()
          else :
               if self.ready_to_attack() :
                    movingstate = True
                    ux,uy = game.mouseclick(event)
                    vx = ux - self.x
                    vy = uy - self.y
                    total = vx**2 + vy**2
                    self.dx = self.speed*vx/math.sqrt(total)
                    self.dy = self.speed*vy/math.sqrt(total)
          window.after(100/self.attackSpeed, self.shot)

     def handlecollision(self, other) :
          if type(other) is Spine :
               self.hp = self.hp - (other.attackDmage - self.armor)
          


class Lurker(Unit) :
     def __init__(self, x, y, image, game) :
          super().__init__(x, y, image, game)
          self.hp = 125
          self.armor = 1
          self.attackSpeed = 5
          self.attackstate = False

     def attack(self, other, window) :
          if math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2) <= 100 :
               self.attackstate = True
               spine.generate()
          window.after(100/self.attackSpeed, self.attack)


class Spine(Unit) :
     def __init__(self, x, y , image, game) :
          super().__init__(x, y, image, game)
          self.attackDamage = 20

class Gameplay :

     def endgame(self) :
          self.running = False
          pass

     def removeunit(self, unit) :
          if unit in self.unitlist :
               self.unitlist.remove(unit)
               del unit
          
     def __init__(self, window) :
          self.window = window
          self.running = True
          self.unitlist = []
          self.marineimage = PhotoImage(file = 'battle.gif')
          self.lurkerimage = PhotoImage(file ='오버로드.gif')
          self.spineimage = PhotoImage(file ='미사일.png')
          self.canvas = Canvas(window, width = 800,height = 600)
          self.canvas.pack()
          self.running = True
          self.initunit()
          self.x, self.y = 400, 550
          window.bind('<Button-3>', self.mouseclick)
          window.bind('t', self.presst)
          window.bind('a', self.pressa)
          window.bind('<Button-1>', self.mouseclickl)

     def initunit(self) :
          self.lurker = Lurker(400,50, self.lurkerimage,self)
          self.marine = Marine(400,550,self.marineimage,self, self.lurker)
          self.unitlist.append(self.marine)
          self.unitlist.append(self.lurker)
          
     def mouseclick(self, event) :
          self.x, self.y = event.x, event.y
          return

     def presst(self, event) :
          self.marine.steampack()
          return

     def pressa(self, event) :
          self.marine.ready_to_attack()
          return

     def mouseclickl(self, event) :
          return event.x, event.y

     def paint(self,) :
          self.canvas.delete(ALL)
          self.canvas.create_rectangle(0,0,800,600, fill = 'white')
          for unit in self.unitlist :
               unit.draw(self)

     def gameloop(self) :
          for unit in self.unitlist :
               unit.move(self)

          for me in self.unitlist :
               for other in self.unitlist :
                    if me != other :
                         if (me.collision(other)) :
                              me.handlecollision(other)
                              other.handlecollision(me)
          self.paint()
          if self.running :
               self.window.after(10, self.gameloop)

          
          
window = Tk()
game = Gameplay(window)
window.after(10, game.gameloop())
window.mainloop()








               
               

     
          
               

          
          

     
          
          
          
          
