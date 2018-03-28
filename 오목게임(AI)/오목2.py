from tkinter import *
import time
import random

class Player :
     def __init__(self,x ,y) :
          self.x = x
          self.y = y


class PlayGame_Gomoku :
     def __init__(self, window) :
          self.blackstone = PhotoImage(file = 'black.png')
          self.whitestone = PhotoImage(file = 'white.png')
          self.stonelist = [([0]*19) for i in range(19)]
          self.frame = Frame(window).pack()
          self.canvas = Canvas(self.frame, width =1250, height = 850)
          self.canvas.pack()
          self.undo_button = Button(self.frame, text = '무르기', command = self.undo).place(x = 1035, y = 250)
          self.board = PhotoImage(file = '바둑판.gif')
          self.initBoard()
          self.blackPlayer = True
          self.is_stone_put = False
          self.whiteVictory = False
          self.blackVictory = False
          self.canvas.bind('<Button-1>', self.putStone)
          self.text = self.canvas.create_text(960, 200, anchor = NW, text = '흑의 차례입니다', fill = 'white', font = ('times', 20, 'bold')) 
          self.init_time = time.time()
          self.cur_time = 0
          self.turn_time = time.time()
          self.time = ''
          self.sec = ""
          self.pressed = False
          self.undoclick = False
          self.blackundo = 3
          self.whiteundo = 3
          self.b_count = self.canvas.create_text(950, 650, anchor = NW, text = self.blackundo , fill = 'white', font = ('times', 18, 'bold'))
          self.w_count = self.canvas.create_text(1140, 650, anchor = NW, text = self.whiteundo , fill = 'white', font = ('times', 18, 'bold'))
          self.indextuplelist = []
          self.elapsedTime()
          self.turnedTime()
          self.rule = self.canvas.create_text(950, 50, anchor = NW, text = '          고모쿠룰\n   특별한 제한 없이 \n5목을 완성하면 승리', fill = 'white', font = ('times', 18, 'bold')) 



     def initBoard(self) :
          self.canvas.create_image(0,0, anchor = NW, image = self.board)
          self.canvas.create_rectangle(850, 0, 1250, 850, fill = 'black')
          self.canvas.create_text(1000, 350, anchor = NW, text = '경과 시간', fill = 'white', font = ('time', 20))
          self.canvas.create_text(930, 450, anchor=NW, text='수읽기 제한시간(30초)', fill='white', font=('time', 20))
          self.canvas.create_text(870, 600, anchor = NW, text = '흑의 무르기 횟수', fill = 'white', font = ('times', 15, 'bold'))
          self.canvas.create_text(1070, 600, anchor = NW, text = '백의 무르기 횟수', fill = 'white', font = ('times', 15, 'bold'))
          

     def elapsedTime(self) :
          self.cur_time = time.time() - self.init_time
          self.canvas.delete(self.time)
          t = time.localtime(self.cur_time)
          self.time = self.canvas.create_text(1020, 400, anchor = NW, text = time.strftime("%M:%S", t), fill = 'white', font = ('time', 20))
          window.after(10, self.elapsedTime)

     def checkVictory_black(self) :
          for i in range(19) :
               for j in range(19) :
                    if j < 15 :
                         if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 :
                              self.blackVictory = True
                    if i < 15 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 :
                              self.blackVictory = True
                    if i < 15 and j < 15 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 :
                              self.blackVictory = True
                    if i < 15 and j < 15 :
                         if self.stonelist[i][j+4] == self.stonelist[i+1][j+3] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+1] == self.stonelist[i+4][j] == 1 :
                              self.blackVictory = True


     def checkVictory_white(self) :
          for i in range(19) :
               for j in range(19) :
                    if j < 15 :
                         if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 2 :
                              self.whiteVictory = True
                    if i < 15 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 2 :
                              self.whiteVictory = True
                    if i < 15 and j < 15 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 2 :
                              self.whiteVictory = True
                    if i < 15 and j < 15 :
                         if self.stonelist[i][j+4] == self.stonelist[i+1][j+3] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+1] == self.stonelist[i+4][j] == 2 :
                              self.whiteVictory = True


     def checkArea(self, x, y) :  
          for i in range(19) :
               for j in range(19) :
                    if (4 + 44.5*i < x < 44 + 44.5*i) and (4 + 44.5*j < y < 44 + 44.5*j) :
                         if self.stonelist[i][j] == 0 :
                              if self.blackPlayer:
                                   k = self.canvas.create_image(24 + 44.5*i, 24 + 44.5*j, anchor = CENTER, image = self.blackstone)
                                   self.stonelist[i][j] = 1
                                   self.indextuplelist.append((i,j,k))

                              else :
                                   k = self.canvas.create_image(24 + 44.5*i, 24 + 44.5*j, anchor = CENTER, image = self.whitestone)
                                   self.stonelist[i][j] = 2
                                   self.indextuplelist.append((i,j,k))

                              self.is_stone_put = True

     def changeText(self) :
          b = '흑의 차례입니다'
          w = '백의 차례입니다'
          if self.blackPlayer :
               self.text = self.canvas.create_text(960, 200, anchor = NW, text = b, fill = 'white', font = ('times', 20, 'bold'))

          else :
               self.text = self.canvas.create_text(960, 200, anchor = NW, text = w, fill = 'white', font = ('times', 20, 'bold'))
          self.canvas.delete(self.b_count)
          self.canvas.delete(self.w_count)
          self.b_count = self.canvas.create_text(950, 650, anchor = NW, text = self.blackundo , fill = 'white', font = ('times', 18, 'bold'))
          self.w_count = self.canvas.create_text(1140, 650, anchor = NW, text = self.whiteundo , fill = 'white', font = ('times', 18, 'bold'))

     def turnedTime(self) :
          self.cur_time = time.time() - self.turn_time
          t = time.localtime(self.cur_time)
          self.canvas.delete(self.sec)
          self.limit = 30-int(time.strftime("%S", t))
          if self.limit <= 0 :
              self.limit = 0
              self.blackPlayer = not self.blackPlayer
              self.is_stone_put = not self.is_stone_put
              self.putStone(Player(-10,-10))
              return
          self.sec = self.canvas.create_text(1020, 500, anchor = NW, text = str(self.limit) + '초', fill = 'white', font = ('time', 20))
          window.after(10, self.turnedTime)
          

     def putStone(self, event) :
          self.checkArea(event.x, event.y)
          if self.is_stone_put:
               self.turn_time = time.time()
               self.turnedTime()
               self.blackPlayer = not self.blackPlayer
               self.is_stone_put = not self.is_stone_put
               if event.x == -10 :
                    self.blackPlayer = not self.blackPlayer
                    self.s = Tk()
                    label = Label(self.s, text = '착수 시간이 초과되었습니다. 턴이 넘어갑니다').pack()
                    button = Button(self.s, text = '확인', command = self.turn_change).pack()                     
          self.undoclick = False
          self.canvas.delete(self.text)
          self.changeText()
          self.checkVictory_black()
          self.checkVictory_white()
          if self.blackVictory :
               self.w = Tk()
               label = Label(self.w, text = '흑의 승리입니다!').pack()
               b1 = Button(self.w, text = '종료', command = self.exit).pack(side = LEFT)
               b2 = Button(self.w, text = '다시하기', command = self.restart).pack(side = LEFT)
          if self.whiteVictory :
               self.w = Tk()
               label = Label(self.w, text = '백의 승리입니다!').pack()
               b1 = Button(self.w, text = '종료', command = self.exit).pack(side = LEFT)
               b2 = Button(self.w, text = '다시하기', command = self.restart).pack(side = LEFT)
          return

     

     def turn_change(self) :
          self.pressed = True
          self.s.destroy()

     def exit(self) :
          self.w.withdraw()
          global window
          window.destroy()

     def restart(self) :
          self.w.withdraw()
          global window
          window.destroy()
          window = Tk()
          window.withdraw()
          game = main()
          window.mainloop()

     def undo(self) :
          if not self.undoclick :
               if (self.blackundo > 0 and not self.blackPlayer) or (self.whiteundo > 0 and self.blackPlayer) :
                    self.blackPlayer = not self.blackPlayer
                    self.is_stone_put = not self.is_stone_put
                    i, j, k = self.indextuplelist[-1]
                    del self.indextuplelist[-1]
                    self.stonelist[i][j] = 0
                    self.canvas.delete(k)
                    if self.blackPlayer :
                         self.blackundo += -1
                    else :
                         self.whiteundo += -1
                    self.canvas.delete(self.text)
                    self.changeText()
          self.undoclick = True


class PlayGame_Renju(PlayGame_Gomoku) :
     def __init__(self, window) :
          super().__init__(window)
          self.renju = 0
          self.canvas.delete(self.rule)
          self.rule = self.canvas.create_text(930, 50, anchor = NW, text = '             렌주룰\n 흑은 33, 44, 장목 금지 \n백은 규칙에 제한 없음', fill = 'white', font = ('times', 18, 'bold'))
          


     def check33(self) :
          for i in range(19) :
               for j in range(19) :
                    if j < 15 :
                         if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == 1 and self.stonelist[i][j] == self.stonelist[i][j+4] == 0 :
                              self.renju += 1
                    if i < 15 :
                         if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == 1 and self.stonelist[i][j] == self.stonelist[i+4][j] == 0 :
                              self.renju += 1
                    if i < 15 and j < 15 :
                         if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == 1 and self.stonelist[i][j] == self.stonelist[i+4][j+4] == 0 :
                              self.renju += 1
                    if i < 15 and j < 15 :
                         if self.stonelist[i+1][j+3] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+1] == 1 and self.stonelist[i][j+4] == self.stonelist[i+4][j] == 0 :
                              self.renju += 1
                    if j < 14 :
                         if self.stonelist[i][j+1] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and (self.stonelist[i][j] == self.stonelist[i][j+5] == self.stonelist[i][j+2] == 0) :
                              self.renju += 1
                    if j < 14 :
                         if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+4] == 1 and (self.stonelist[i][j] ==  self.stonelist[i][j+5] ==  self.stonelist[i][j+3] == 0) :
                              self.renju += 1
                    if i < 14 :
                         if self.stonelist[i+1][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and (self.stonelist[i][j] ==  self.stonelist[i+5][j] ==  self.stonelist[i+2][j] == 0) :
                              self.renju += 1
                    if i < 14 :
                         if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+4][j] == 1 and (self.stonelist[i][j] ==  self.stonelist[i+5][j] ==  self.stonelist[i+3][j] == 0) :
                              self.renju += 1
                    if i < 14 and j < 14 :
                         if self.stonelist[i+1][j+1] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and (self.stonelist[i][j] == self.stonelist[i+5][j+5] ==  self.stonelist[i+2][j+2] == 0) :
                              self.renju += 1
                    if i < 14 and j < 14 :
                         if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+4][j+4] == 1 and (self.stonelist[i][j] == self.stonelist[i+5][j+5] ==  self.stonelist[i+3][j+3] == 0) :
                              self.renju += 1
                    if i < 14 and j < 14 :
                         if self.stonelist[i+1][j+4] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == 1 and (self.stonelist[i][j+5] == self.stonelist[i+5][j] ==  self.stonelist[i+2][j+3] == 0) :
                              self.renju += 1
                    if i < 14 and j < 14 :
                         if self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+4][j+1] == 1 and (self.stonelist[i][j+5] == self.stonelist[i+5][j] ==  self.stonelist[i+3][j+2] == 0) :
                              self.renju += 1
          if self.renju >= 2 :
               self.renju = 0
               return True
          self.renju = 0
          return False

     def check44(self) :
          for i in range(19) :
               for j in range(19) :
                    if j < 14 :
                         if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and not(self.stonelist[i][j] == 2 and self.stonelist[i][j+5] == 2) and not(self.stonelist[i][j] == 1 or self.stonelist[i][j+5] == 1) :
                              self.renju += 1
                    if j == 0 :
                        if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == 1 and (self.stonelist[i][j+4] == 0) :
                            self.renju += 1
                    if j == 18 :
                        if self.stonelist[i][j-3] == self.stonelist[i][j-2] == self.stonelist[i][j-1] == self.stonelist[i][j] == 1 and(self.stonelist[i][j-4] == 0) :
                            self.renju += 1
                    if i < 14 :
                         if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i][j] == 2 and self.stonelist[i+5][j] == 2) and not(self.stonelist[i][j] == 1 or self.stonelist[i+5][j] == 1) :
                              self.renju += 1
                    if i == 0 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == 1 and(self.stonelist[i+4][j] == 0) :
                              self.renju += 1
                    if i == 18 :
                         if self.stonelist[i-3][j] == self.stonelist[i-2][j] == self.stonelist[i-1][j] == self.stonelist[i][j] == 1 and(self.stonelist[i-4][j] == 0) :
                              self.renju += 1
                    if i < 14 and j < 14 :
                         if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and not(self.stonelist[i][j] == self.stonelist[i+5][j+5] == 2) and not(self.stonelist[i][j] == 1 or self.stonelist[i+5][j+5] == 1) :
                              self.renju += 1
                    if i == 0 and j == 0 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == 1 and(self.stonelist[i+4][j+4] == 0) :
                              self.renju += 1
                    if i == 18 and j == 18 :
                         if self.stonelist[i-3][j-3] == self.stonelist[i-2][j-2] == self.stonelist[i-1][j-1] == self.stonelist[i][j] == 1 and(self.stonelist[i-4][j-4] == 0) :
                              self.renju += 1
                    if i < 14 and j < 14 :
                         if self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == 1 and not(self.stonelist[i][j+5] == self.stonelist[i+5][j] == 2) and not(self.stonelist[i][j+5] == 1 and self.stonelist[i+5][j] == 1) :
                              self.renju += 1
                    if i == 0 and j == 18 :
                         if self.stonelist[i+3][j-3] == self.stonelist[i+2][j-2] == self.stonelist[i+1][j-1] == self.stonelist[i][j] == 1 and(self.stonelist[i+4][j-4] == 0) :
                              self.renju += 1
                    if i == 18 and j == 0 :
                         if self.stonelist[i][j] == self.stonelist[i-1][j+1] == self.stonelist[i-2][j+2] == self.stonelist[i-3][j+3] == 1 and(self.stonelist[i-4][j+4] == 0) :
                              self.renju += 1
          if self.renju >= 2 :
               self.renju = 0
               return True
          self.renju = 0
          return False

     def check6moku(self) :
          for i in range(19) :
               for j in range(19) :
                    if j < 14 :
                         if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4]== self.stonelist[i][j+5] == 1 :
                              return True
                    if i < 14 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == self.stonelist[i+5][j] == 1 :
                              return True
                    if i < 14 and j < 14 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == self.stonelist[i+5][j+5] == 1 :
                              return True
                    if i < 14 and j < 14 :
                         if self.stonelist[i][j+5] == self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == self.stonelist[i+5][j] == 1 :
                              return True
          return False

     def checkExact5moku(self) :
          for i in range(19) :
               for j in range(19) :
                    if j < 13 :
                         if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == self.stonelist[i][j+5] == 1 and not(self.stonelist[i][j] == 1 or self.stonelist[i][j+6] == 1) :
                              return True
                    if j == 0 :
                         if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and not(self.stonelist[i][j+5] == 1) :
                              return True
                    if j == 18 :
                         if self.stonelist[i][j-4] == self.stonelist[i][j-3] == self.stonelist[i][j-2] == self.stonelist[i][j-1] == self.stonelist[i][j] == 1 and not(self.stonelist[i][j-5] == 1) :
                              return True
                    if i < 13 :
                         if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == self.stonelist[i+5][j] == 1 and not(self.stonelist[i][j] == 1 or self.stonelist[i+6][j] == 1) :
                              return True
                    if i == 0 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+5][j] == 1) :
                              return True
                    if i == 18 :
                         if self.stonelist[i-4][j] == self.stonelist[i-3][j] == self.stonelist[i-2][j] == self.stonelist[i-1][j] == self.stonelist[i][j] == 1 and not(self.stonelist[i-5][j] == 1) :
                              return True
                    if i < 13 and j < 13 :
                         if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == self.stonelist[i+5][j+5] == 1 and not(self.stonelist[i][j] == 1 or self.stonelist[i+6][j+6] == 1) :
                              return True
                    if i == 0 and j == 0 :
                         if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and not(self.stonelist[i+5][j+5] == 1) :
                              return True
                    if i == 18 and j == 18 :
                         if self.stonelist[i-4][j-4] == self.stonelist[i-3][j-3] == self.stonelist[i-2][j-2] == self.stonelist[i-1][j-1] == self.stonelist[i][j] == 1 and not(self.stonelist[i-5][j-5] == 1) :
                              return True
                    if i < 13 and j < 13 :
                         if self.stonelist[i+1][j+5] == self.stonelist[i+2][j+4] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+2] == self.stonelist[i+5][j+1] == 1 and not(self.stonelist[i][j+6] == 1 or self.stonelist[i+6][j] == 1) :
                              return True
                    if i == 0 and j == 18 :
                         if self.stonelist[i+4][j-4] == self.stonelist[i+3][j-3] == self.stonelist[i+2][j-2] == self.stonelist[i+1][j-1] == self.stonelist[i][j] == 1 and not(self.stonelist[i+5][j-5] == 1) :
                              return True
                    if i == 18 and j == 0 :
                         if self.stonelist[i-4][j+4] == self.stonelist[i-3][j+3] == self.stonelist[i-2][j+2] == self.stonelist[i-1][j+1] == self.stonelist[i][j] == 1 and not(self.stonelist[i-5][j+5] == 1) :
                              return True
          return False

     def checkArea(self, x, y) :
          for i in range(19) :
               for j in range(19) :
                    if (4 + 44.5*i < x < 44 + 44.5*i) and (4 + 44.5*j < y < 44 + 44.5*j) :
                         if self.stonelist[i][j] == 0 :
                              if self.blackPlayer:
                                   k = self.canvas.create_image(24 + 44.5*i, 24 + 44.5*j, anchor = CENTER, image = self.blackstone)
                                   self.stonelist[i][j] = 1
                                   self.indextuplelist.append((i,j,k))
                                   self.i = i
                                   self.j = j

                                   if self.checkExact5moku() :
                                        self.blackVictory = True
                                   elif self.check33() :
                                        w = Tk()
                                        label = Label(w, text = '33입니다. 다른 곳에 착수하세요!').pack()
                                        b1 = Button(w, text = '확인', command = w.withdraw).pack()
                                        self.canvas.delete(k)
                                        self.stonelist[self.i][self.j] = 0
                                        return

                                   elif self.check6moku() :
                                        w = Tk()
                                        label = Label(w, text = '6목입니다. 다른 곳에 착수하세요!').pack()
                                        b1 = Button(w, text = '확인', command = w.withdraw).pack()
                                        self.canvas.delete(k)
                                        self.stonelist[self.i][self.j] = 0
                                        return

                                   elif self.check44() :
                                        w = Tk()
                                        label = Label(w, text = '44입니다. 다른 곳에 착수하세요!').pack()
                                        b1 = Button(w, text = '확인', command = w.withdraw).pack()
                                        self.canvas.delete(k)
                                        self.stonelist[self.i][self.j] = 0
                                        return

                              else :
                                   k = self.canvas.create_image(24 + 44.5*i, 24 + 44.5*j, anchor = CENTER, image = self.whitestone)
                                   self.stonelist[i][j] = 2
                                   self.indextuplelist.append((i,j,k))
                              self.is_stone_put = True

     def putStone(self, event) :
          self.checkArea(event.x, event.y)
          if self.is_stone_put:
               self.blackPlayer = not self.blackPlayer
               self.is_stone_put = not self.is_stone_put
          self.canvas.delete(self.text)
          self.changeText()
          self.turn_time = time.time()
          self.turnedTime()
          if event.x == -10 :
                    self.blackPlayer = not self.blackPlayer
                    self.s = Tk()
                    label = Label(self.s, text = '착수 시간이 초과되었습니다. 턴이 넘어갑니다').pack()
                    button = Button(self.s, text = '확인', command = self.turn_change).pack()
          self.canvas.delete(self.text)
          self.changeText()
          self.undoclick = False
          if self.blackPlayer :
               self.checkVictory_white()
          if self.blackVictory :
               self.w = Tk()
               label = Label(self.w, text = '흑의 승리입니다!').pack()
               b1 = Button(self.w, text = '종료', command = self.exit).pack(side = LEFT)
               b2 = Button(self.w, text = '다시하기', command = self.restart).pack(side = LEFT)
          if self.whiteVictory :
               self.w = Tk()
               label = Label(self.w, text = '백의 승리입니다!').pack()
               b1 = Button(self.w, text = '종료', command = self.exit).pack(side = LEFT)
               b2 = Button(self.w, text = '다시하기', command = self.restart).pack(side = LEFT)
          return

class Ai_Gomoku_White(PlayGame_Gomoku) :
     def __init__(self, window) :
          super().__init__(window)

     def checkArea(self, x, y) :  
          for i in range(19) :
               for j in range(19) :
                    if (4 + 44.5*i < x < 44 + 44.5*i) and (4 + 44.5*j < y < 44 + 44.5*j) :
                         if self.stonelist[i][j] == 0 :
                              if self.blackPlayer:
                                   k = self.canvas.create_image(24 + 44.5*i, 24 + 44.5*j, anchor = CENTER, image = self.blackstone)
                                   self.stonelist[i][j] = 1
                                   self.indextuplelist.append((i,j,k))

                              self.is_stone_put = True

     def ai_put(self, i, j) :
          k = self.canvas.create_image(24 + 44.5*i, 24 + 44.5*j, anchor = CENTER, image = self.whitestone)
          self.stonelist[i][j] = 2
          self.indextuplelist.append((i,j,k))

     def ai_algorithm(self) :
          if not self.blackPlayer :
               for i in range(19) :
                    for j in range(19) :
                         if j < 14 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 2 and not(self.stonelist[i][j] == 1 and self.stonelist[i][j+5] == 1) :
                                   if self.stonelist[i][j] == 0 and self.stonelist[i][j+5] == 1 :
                                        self.ai_put(i, j)
                                        return
                                   if self.stonelist[i][j] == 1 and self.stonelist[i][j+5] == 0 :
                                        self.ai_put(i, j+5)
                                        return
                                   if self.stonelist[i][j] == 0 and self.stonelist[i][j+5] == 0 :
                                        r = [(i,j), (i,j+5)]
                                        x, y = random.choice(r)
                                        self.ai_put(x,y)
                                        return
                              
                         if j == 0 :
                             if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == 2 and (self.stonelist[i][j+4] == 0) :
                                 self.ai_put(i, j+4)
                                 return

                         if j == 18 :
                             if self.stonelist[i][j-3] == self.stonelist[i][j-2] == self.stonelist[i][j-1] == self.stonelist[i][j] == 2 and(self.stonelist[i][j-4] == 0) :
                                 self.ai_put(i, j-4)
                                 return

                         if i < 14 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 2 and not(self.stonelist[i][j] == 1 and self.stonelist[i+5][j] == 1)  :
                                   if self.stonelist[i][j] == 0 and self.stonelist[i+5][j] == 1 :
                                        self.ai_put(i, j)
                                        return
                                   if self.stonelist[i][j] == 1 and self.stonelist[i+5][j] == 0 :
                                        self.ai_put(i+5, j)
                                        return
                                   if self.stonelist[i][j] == 0 and self.stonelist[i+5][j] == 0 :
                                        r = [(i,j), (i+5,j)]
                                        x, y = random.choice(r)
                                        self.ai_put(x,y)
                                        return
                         if i == 0 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == 2 and(self.stonelist[i+4][j] == 0) :
                                   self.ai_put(i+4, j)
                                   return

                         if i == 18 :
                              if self.stonelist[i-3][j] == self.stonelist[i-2][j] == self.stonelist[i-1][j] == self.stonelist[i][j] == 2 and(self.stonelist[i-4][j] == 0) :
                                   self.ai_put(i-4, j)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 2 and not(self.stonelist[i][j] == self.stonelist[i+5][j+5] == 1) :
                                   if self.stonelist[i][j] == 0 and self.stonelist[i+5][j+5] == 1 :
                                        self.ai_put(i, j)
                                        return
                                   if self.stonelist[i][j] == 1 and self.stonelist[i+5][j+5] == 0 :
                                        self.ai_put(i+5, j+5)
                                        return
                                   if self.stonelist[i][j] == 0 and self.stonelist[i+5][j+5] == 0 :
                                        r = [(i,j), (i+5,j+5)]
                                        x, y = random.choice(r)
                                        self.ai_put(x,y)
                                        return

                         if i == 0 and j == 0 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == 2 and(self.stonelist[i+4][j+4] == 0) :
                                   self.ai_put(i+4, j+4)
                                   return

                         if i == 18 and j == 18 :
                              if self.stonelist[i-3][j-3] == self.stonelist[i-2][j-2] == self.stonelist[i-1][j-1] == self.stonelist[i][j] == 2 and(self.stonelist[i-4][j-4] == 0) :
                                   self.ai_put(i-4, j-4)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == 2 and not(self.stonelist[i][j+5] == self.stonelist[i+5][j] == 1) :
                                   if self.stonelist[i][j+5] == 0 and self.stonelist[i+5][j] == 1 :
                                        self.ai_put(i, j+5)
                                        return
                                   if self.stonelist[i][j+5] == 1 and self.stonelist[i+5][j] == 0 :
                                        self.ai_put(i+5, j)
                                        return
                                   if self.stonelist[i][j+5] == 0 and self.stonelist[i+5][j] == 0 :
                                        r = [(i,j+5), (i+5,j)]
                                        x, y = random.choice(r)
                                        self.ai_put(x,y)
                                        return

                         if i == 0 and j == 18 :
                              if self.stonelist[i+3][j-3] == self.stonelist[i+2][j-2] == self.stonelist[i+1][j-1] == self.stonelist[i][j] == 2 and(self.stonelist[i+4][j-4] == 0) :
                                   self.ai_put(i+4, j-4)
                                   return

                         if i == 18 and j == 0 :
                              if self.stonelist[i][j] == self.stonelist[i-1][j+1] == self.stonelist[i-2][j+2] == self.stonelist[i-3][j+3] == 2 and(self.stonelist[i-4][j+4] == 0) :
                                   self.ai_put(i-4, j+4)
                                   return
               for i in range(19) :
                    for j in range(19) :

                         if j < 14 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and not(self.stonelist[i][j] == 2 and self.stonelist[i][j+5] == 2) :
                                   if self.stonelist[i][j] == 0 and self.stonelist[i][j+5] == 2 :
                                        self.ai_put(i, j)
                                        return
                                   if self.stonelist[i][j] == 2 and self.stonelist[i][j+5] == 0 :
                                        self.ai_put(i, j+5)
                                        return
                              
                         if j == 0 :
                             if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == 1 and (self.stonelist[i][j+4] == 0) :
                                 self.ai_put(i, j+4)
                                 return

                         if j == 18 :
                             if self.stonelist[i][j-3] == self.stonelist[i][j-2] == self.stonelist[i][j-1] == self.stonelist[i][j] == 1 and(self.stonelist[i][j-4] == 0) :
                                 self.ai_put(i, j-4)
                                 return

                         if i < 14 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i][j] == 2 and self.stonelist[i+5][j] == 2)  :
                                   if self.stonelist[i][j] == 0 and self.stonelist[i+5][j] == 2 :
                                        self.ai_put(i, j)
                                        return
                                   if self.stonelist[i][j] == 2 and self.stonelist[i+5][j] == 0 :
                                        self.ai_put(i+5, j)
                                        return

                         if i == 0 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == 1 and(self.stonelist[i+4][j] == 0) :
                                   self.ai_put(i+4, j)
                                   return

                         if i == 18 :
                              if self.stonelist[i-3][j] == self.stonelist[i-2][j] == self.stonelist[i-1][j] == self.stonelist[i][j] == 1 and(self.stonelist[i-4][j] == 0) :
                                   self.ai_put(i-4, j)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and not(self.stonelist[i][j] == self.stonelist[i+5][j+5] == 2) :
                                   if self.stonelist[i][j] == 0 and self.stonelist[i+5][j+5] == 2 :
                                        self.ai_put(i, j)
                                        return
                                   if self.stonelist[i][j] == 2 and self.stonelist[i+5][j+5] == 0 :
                                        self.ai_put(i+5, j+5)
                                        return

                         if i == 0 and j == 0 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == 1 and(self.stonelist[i+4][j+4] == 0) :
                                   self.ai_put(i+4, j+4)
                                   return

                         if i == 18 and j == 18 :
                              if self.stonelist[i-3][j-3] == self.stonelist[i-2][j-2] == self.stonelist[i-1][j-1] == self.stonelist[i][j] == 1 and(self.stonelist[i-4][j-4] == 0) :
                                   self.ai_put(i-4, j-4)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == 1 and not(self.stonelist[i][j+5] == self.stonelist[i+5][j] == 2) :
                                   if self.stonelist[i][j+5] == 0 and self.stonelist[i+5][j] == 2 :
                                        self.ai_put(i, j+5)
                                        return
                                   if self.stonelist[i][j+5] == 2 and self.stonelist[i+5][j] == 0 :
                                        self.ai_put(i+5, j)
                                        return

                         if i == 0 and j == 18 :
                              if self.stonelist[i+3][j-3] == self.stonelist[i+2][j-2] == self.stonelist[i+1][j-1] == self.stonelist[i][j] == 1 and(self.stonelist[i+4][j-4] == 0) :
                                   self.ai_put(i+4, j-4)
                                   return

                         if i == 18 and j == 0 :
                              if self.stonelist[i][j] == self.stonelist[i-1][j+1] == self.stonelist[i-2][j+2] == self.stonelist[i-3][j+3] == 1 and(self.stonelist[i-4][j+4] == 0) :
                                   self.ai_put(i-4, j+4)
                                   return

                         if j < 15 :
                              if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+4] == 1 and not(self.stonelist[i][j+3] == 2) :
                                   self.ai_put(i, j+3)
                                   return

                         if i < 15 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+3][j] == 2) :
                                   self.ai_put(i+3, j)
                                   return                         

                         if i < 15 and j < 15 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+4][j+4] == 1 and not(self.stonelist[i+3][j+3] == 2) :
                                   self.ai_put(i+3, j+3)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i][j+4] == self.stonelist[i+1][j+3] == self.stonelist[i+2][j+2] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+3][j+1] == 2) :
                                   self.ai_put(i+3, j+1)
                                   return


                         if j < 15 :
                              if self.stonelist[i][j] == self.stonelist[i][j+1] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and not(self.stonelist[i][j+2] == 2) :
                                   self.ai_put(i, j+2)
                                   return

                         if i < 15 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+2][j] == 2) :
                                   self.ai_put(i+2, j)
                                   return                         

                         if i < 15 and j < 15 :
                              if self.stonelist[i][j] == self.stonelist[i+1][j+1] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and not(self.stonelist[i+2][j+2] == 2) :
                                   self.ai_put(i+2, j+2)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i][j+4] == self.stonelist[i+1][j+3] == self.stonelist[i+3][j+1] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+2][j+2] == 2) :
                                   self.ai_put(i+2, j+2)
                                   return

                         if j < 15 :
                              if self.stonelist[i][j] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and not(self.stonelist[i][j+1] == 2) :
                                   self.ai_put(i, j+1)
                                   return

                         if i < 15 :
                              if self.stonelist[i][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+1][j] == 2) :
                                   self.ai_put(i+1, j)
                                   return                         

                         if i < 15 and j < 15 :
                              if self.stonelist[i][j] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and not(self.stonelist[i+1][j+1] == 2) :
                                   self.ai_put(i+1, j+1)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i][j+4] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+1] == self.stonelist[i+4][j] == 1 and not(self.stonelist[i+1][j+3] == 2) :
                                   self.ai_put(i+1, j+3)
                                   return                              


                              
               for i in range(19) :
                    for j in range(19) : 

                         if j < 15 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == 2 and self.stonelist[i][j] == self.stonelist[i][j+4] == 0 :
                                   r = [(i,j), (i,j+4)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 15 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == 2 and self.stonelist[i][j] == self.stonelist[i+4][j] == 0 :
                                   r = [(i,j), (i+4,j)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == 2 and self.stonelist[i][j] == self.stonelist[i+4][j+4] == 0 :
                                   r = [(i,j), (i+4,j+4)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i+1][j+3] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+1] == 2 and self.stonelist[i][j+4] == self.stonelist[i+4][j] == 0 :
                                   r = [(i,j+4), (i+4,j)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if j < 14 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 2 and (self.stonelist[i][j] == self.stonelist[i][j+5] == self.stonelist[i][j+2] == 0) :
                                   self.ai_put(i,j+2)
                                   return

                         if j < 14 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+4] == 2 and (self.stonelist[i][j] ==  self.stonelist[i][j+5] ==  self.stonelist[i][j+3] == 0) :
                                   self.ai_put(i,j+3)
                                   return
                                   
                         if i < 14 :
                              if self.stonelist[i+1][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 2 and (self.stonelist[i][j] ==  self.stonelist[i+5][j] ==  self.stonelist[i+2][j] == 0) :
                                   self.ai_put(i+2,j)
                                   return

                         if i < 14 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+4][j] == 2 and (self.stonelist[i][j] ==  self.stonelist[i+5][j] ==  self.stonelist[i+3][j] == 0) :
                                   self.ai_put(i+3,j)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 2 and (self.stonelist[i][j] == self.stonelist[i+5][j+5] ==  self.stonelist[i+2][j+2] == 0) :
                                   self.ai_put(i+2,j+2)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+4][j+4] == 2 and (self.stonelist[i][j] == self.stonelist[i+5][j+5] ==  self.stonelist[i+3][j+3] == 0) :
                                   self.ai_put(i+3,j+3)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+4] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == 2 and (self.stonelist[i][j+5] == self.stonelist[i+5][j] ==  self.stonelist[i+2][j+3] == 0) :
                                   self.ai_put(i+2,j+3)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+4][j+1] == 2 and (self.stonelist[i][j+5] == self.stonelist[i+5][j] ==  self.stonelist[i+3][j+2] == 0) :
                                   self.ai_put(i+3,j+2)
                                   return
               for i in range(19) :
                    for j in range(19) :

                         if j < 15 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+3] == 1 and self.stonelist[i][j] == self.stonelist[i][j+4] == 0 :
                                   r = [(i,j), (i,j+4)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 15 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+3][j] == 1 and self.stonelist[i][j] == self.stonelist[i+4][j] == 0 :
                                   r = [(i,j), (i+4,j)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+3] == 1 and self.stonelist[i][j] == self.stonelist[i+4][j+4] == 0 :
                                   r = [(i,j), (i+4,j+4)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 15 and j < 15 :
                              if self.stonelist[i+1][j+3] == self.stonelist[i+2][j+2] == self.stonelist[i+3][j+1] == 1 and self.stonelist[i][j+4] == self.stonelist[i+4][j] == 0 :
                                   r = [(i,j+4), (i+4,j)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if j < 14 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+3] == self.stonelist[i][j+4] == 1 and (self.stonelist[i][j] == self.stonelist[i][j+5] == self.stonelist[i][j+2] == 0) :
                                   self.ai_put(i,j+2)
                                   return

                         if j < 14 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == self.stonelist[i][j+4] == 1 and (self.stonelist[i][j] ==  self.stonelist[i][j+5] ==  self.stonelist[i][j+3] == 0) :
                                   self.ai_put(i,j+3)
                                   return
                                   
                         if i < 14 :
                              if self.stonelist[i+1][j] == self.stonelist[i+3][j] == self.stonelist[i+4][j] == 1 and (self.stonelist[i][j] ==  self.stonelist[i+5][j] ==  self.stonelist[i+2][j] == 0) :
                                   self.ai_put(i+2,j)
                                   return

                         if i < 14 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == self.stonelist[i+4][j] == 1 and (self.stonelist[i][j] ==  self.stonelist[i+5][j] ==  self.stonelist[i+3][j] == 0) :
                                   self.ai_put(i+3,j)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+3][j+3] == self.stonelist[i+4][j+4] == 1 and (self.stonelist[i][j] == self.stonelist[i+5][j+5] ==  self.stonelist[i+2][j+2] == 0) :
                                   self.ai_put(i+2,j+2)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == self.stonelist[i+4][j+4] == 1 and (self.stonelist[i][j] == self.stonelist[i+5][j+5] ==  self.stonelist[i+3][j+3] == 0) :
                                   self.ai_put(i+3,j+3)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+4] == self.stonelist[i+3][j+2] == self.stonelist[i+4][j+1] == 1 and (self.stonelist[i][j+5] == self.stonelist[i+5][j] ==  self.stonelist[i+2][j+3] == 0) :
                                   self.ai_put(i+2,j+3)
                                   return

                         if i < 14 and j < 14 :
                              if self.stonelist[i+1][j+4] == self.stonelist[i+2][j+3] == self.stonelist[i+4][j+1] == 1 and (self.stonelist[i][j+5] == self.stonelist[i+5][j] ==  self.stonelist[i+3][j+2] == 0) :
                                   self.ai_put(i+3,j+2)
                                   return

               for i in range(19) :
                    for j in range(19) :
                         if j < 16 :
                              if self.stonelist[i][j+1] == self.stonelist[i][j+2] == 2 and self.stonelist[i][j] == self.stonelist[i][j+3] == 0 :
                                   r = [(i,j), (i,j+3)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 16 :
                              if self.stonelist[i+1][j] == self.stonelist[i+2][j] == 2 and self.stonelist[i][j] == self.stonelist[i+3][j] == 0 :
                                   r = [(i,j), (i+3,j)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 16 and j < 16 :
                              if self.stonelist[i+1][j+1] == self.stonelist[i+2][j+2] == 2 and self.stonelist[i][j] == self.stonelist[i+3][j+3] == 0 :
                                   r = [(i,j), (i+3,j+3)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

                         if i < 16 and j < 16 :
                              if self.stonelist[i+1][j+2] == self.stonelist[i+2][j+1] == 2 and self.stonelist[i][j+3] == self.stonelist[i+3][j] == 0 :
                                   r = [(i+3,j), (i,j+3)]
                                   x, y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

               for i in range(19) :
                    for j in range(19) :

                         if i < 17 and j < 17 :
                              r = []
                              if self.stonelist[i+1][j+1] == 2 :
                                   for n in range(3) :
                                        for m in range(3) :
                                             if self.stonelist[i+n][j+m] == 0 :
                                                  r.append((i+n, j+m))
                              if r != [] :
                                   x,y = random.choice(r)
                                   self.ai_put(x,y)
                                   return

               for i in range(19) :
                    for j in range(19) :
                         n = 0
                         if self.stonelist[i][j] == 2 :
                              n = n + 1

               if n == 0 :
                    r = []
                    for a in range(4) :
                         for b in range(4) :
                              if self.stonelist[7+a][7+b] == 0 :
                                   r.append((7+a, 7+b))
                    
                    x, y = random.choice(r)
                    self.ai_put(x,y)
                    return

     def putStone(self, event) :
          self.checkArea(event.x, event.y)
          if self.is_stone_put:
               self.turn_time = time.time()
               self.turnedTime()
               self.blackPlayer = not self.blackPlayer
               self.is_stone_put = not self.is_stone_put
               if event.x == -10 :
                    self.blackPlayer = not self.blackPlayer
                    self.s = Tk()
                    label = Label(self.s, text = '착수 시간이 초과되었습니다. 턴이 넘어갑니다').pack()
                    button = Button(self.s, text = '확인', command = self.turn_change).pack()

          if event.x == -20 :
               self.ai_algorithm()
               self.blackPlayer = not self.blackPlayer
               self.is_stone_put = not self.is_stone_put
                    
          self.undoclick = False
          self.canvas.delete(self.text)
          self.changeText()
          self.checkVictory_black()
          self.checkVictory_white()
          if self.blackVictory :
               self.w = Tk()
               label = Label(self.w, text = '흑의 승리입니다!').pack()
               b1 = Button(self.w, text = '종료', command = self.exit).pack(side = LEFT)
               b2 = Button(self.w, text = '다시하기', command = self.restart).pack(side = LEFT)
          if self.whiteVictory :
               self.w = Tk()
               label = Label(self.w, text = '백의 승리입니다!').pack()
               b1 = Button(self.w, text = '종료', command = self.exit).pack(side = LEFT)
               b2 = Button(self.w, text = '다시하기', command = self.restart).pack(side = LEFT)
          if not self.blackPlayer :
               self.putStone(Player(-20,-20))
          return
                                                  































class main :
     def __init__(self) :
          self.window = Tk()
          self.label = Label(self.window, text = '규칙을 선택하세요')
          self.label.pack()
          self.b1 = Button(self.window, text = '렌주룰')
          self.b2 = Button(self.window, text = '고모쿠룰')
          self.b1.pack(side = LEFT)
          self.b2.pack(side = LEFT)
          self.b1.bind('<Button-1>', self.choose_Renju)
          self.b2.bind('<Button-1>', self.choose_Gomoku)
          self.window.mainloop()

     def choose_Renju(self, event) :
          window.deiconify()
          g = PlayGame_Renju(window)
          self.window.destroy()
          return

     def choose_Gomoku(self, event) :
          window.deiconify()
          #g = PlayGame_Gomoku(window)
          g = Ai_Gomoku_White(window)
          self.window.destroy()
          return

window = Tk()
window.withdraw()
game = main()
window.mainloop()







