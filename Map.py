import math as m
from os import supports_follow_symlinks
from typing import List
import numpy as np

class Map:
    def __init__(self, length):
      self.array = np.zeros((length, length)).astype(int)
      self.dimension = length
      self.turn = 0
      self.health = 100
      self.size = 3
      self.snakeData : List = [] #[[(x0,y0),...,(xn,yn)],length, health] excluding own snake
      self.food : List= [] #[[x0,y0], ...,[xn,yn]]
      self.body = [] # [[x0,y0], ...,[xn,yn]]

    def fillMapData(self, request):
      self.turn = request['turn']
      mySnake = request['you']
      for i in range(len(mySnake['body'])):
        self.body.append([mySnake['body'][i]['x'], mySnake['body'][i]['y']])
      self.size = mySnake['length']
      self.health = mySnake['health']
      board = request['board']
      food = board['food']
      for i in range(len(food)):
        self.food.append([food[i]['x'], food[i]['y']])
        
      snakes = [x for x in board['snakes'] if x['id'] != mySnake['id']]
      for i in range(len(snakes)):
        snakeBody = []
        body = snakes[i]['body']
        for j in range(len(body)):
          snakeBody.append((body[j]['x'], body[j]['y']))
        self.snakeData.append([snakeBody, snakes[i]['length'], snakes[i]['health']])

    def sizeMaxEnemy(self):
      if len(self.snakeData) == 0:
        return 0
      maxEnemy = self.snakeData[0]
      for i in range(1,len(self.snakeData)):
        if self.snakeData[i][1] > maxEnemy[1]:
          maxEnemy = self.snakeData[i]
      return maxEnemy[1]
  #potential strats:
  # need Food
  # stay save 
  # attack 
  # Endgame 
    def findStrat(self):
      if self.health < 50:
          self.needFood()
      elif self.sizeMaxEnemy()+2 < self.size:
          self.attack()
      elif len(self.snakeData) > 1:
          self.staySafe()
      else:
        self.endGame()
  
    def needFood(self):
      for i in range(len(self.body)-1):
        self.array[self.body[i][0]][self.body[i][1]] = -1000
      for i in range(len(self.snakeData)):
        x,y = self.snakeData[i][0][0]
        if x > 0:
          self.array[x-1][y] = -500
        if x < self.dimension-1:
          self.array[x+1][y] = -500
        if y > 0:
          self.array[x][y-1] = -500
        if y < self.dimension-1:
          self.array[x][y+1] = -500
        for j in range(len(self.snakeData[i][0])-1):
          x,y = self.snakeData[i][0][j]
          self.array[x][y] = -1000
    
      for i in range(len(self.food)):
        if self.array[self.food[i][0]][self.food[i][1]] >= 0:
          self.array[self.food[i][0]][self.food[i][1]] = 11
          self.spreadPositive((self.food[i][0],self.food[i][1]), self.array[self.food[i][0]][self.food[i][1]])
      
    def staySafe(self):
      for i in range(len(self.body)-1):
        self.array[self.body[i][0]][self.body[i][1]] = -1000
      for i in range(len(self.snakeData)):
        x,y = self.snakeData[i][0][0]
        if x > 0:
          self.array[x-1][y] = -11
        if x < self.dimension-1:
          self.array[x+1][y] = -11
        if y > 0:
          self.array[x][y-1] = -11
        if y < self.dimension-1:
          self.array[x][y+1] = -11
        for j in range(len(self.snakeData[i][0])-1):
          x,y = self.snakeData[i][0][j]
          self.array[x][y] = -1000
      for i in range(self.dimension):
        for j in range(self.dimension):
          if self.array[i][j] == -11:
            self.spreadNegative((i,j), self.array[i][j])
    
    def attack(self):
      for i in range(len(self.body)-1):
        self.array[self.body[i][0]][self.body[i][1]] = -1000
      for i in range(len(self.snakeData)):
        x,y = self.snakeData[i][0][0]
        if x > 0:
          self.array[x-1][y] = 11
        if x < self.dimension-1:
          self.array[x+1][y] = 11
        if y > 0:
          self.array[x][y-1] = 11
        if y < self.dimension-1:
          self.array[x][y+1] = 11
        for j in range(len(self.snakeData[i][0])-1):
          x,y = self.snakeData[i][0][j]
          self.array[x][y] = -1000
      for i in range(self.dimension):
        for j in range(self.dimension):
          if self.array[i][j] > 0:
            self.spreadPositive((i,j), self.array[i][j])

    def endGame(self):
      if self.size <= 1+self.snakeData[0][1]:
        self.needFood()
      else:
        self.attack()

    def finalMapAdjustment(self):
      if self.dimension % 2 == 1:
        center = self.dimension//2
        for offset in range(center+1):
          value = offset
          for i in range(-offset, offset+1):
              self.array[i+center][center + offset] -= value
              self.array[i+center][center - offset] -= value
          for i in range(-offset+1, offset):
              self.array[center + offset][center + i] -= value
              self.array[center - offset][center + i] -= value
      else:
        pass
        
    def spreadPositive(self, point, value):
      x, y = point
      if value > 0 and self.array[x][y] == value:
        if x < self.dimension -1:
          if 0 <= self.array[x+1][y] < value-1:
            self.array[x+1][y] = self.array[x][y]-1
            self.spreadPositive((x+1, y), value-1)
        if x > 0:
          if 0 <= self.array[x-1][y] < value -1:
            self.array[x-1][y] = self.array[x][y]-1
            self.spreadPositive((x-1, y), value-1)
        if y < self.dimension -1:
          if 0 <= self.array[x][y+1] < value-1:
            self.array[x][y+1] = self.array[x][y]-1
            self.spreadPositive((x, y+1), value-1)
        if y > 0:
          if 0 <= self.array[x][y-1] < value -1:
            self.array[x][y-1] = self.array[x][y]-1
            self.spreadPositive((x, y-1), value-1)
    
    def spreadNegative(self, point, value):
      x, y = point
      if value < 0 and self.array[x][y] == value:
        if x < self.dimension -1:
          if value+1 <= self.array[x+1][y] <= 0:
            self.array[x+1][y] = self.array[x][y]+1
            self.spreadNegative((x+1, y), value+1)
        if x > 0:
          if value+1 <= self.array[x-1][y] <= 0:
            self.array[x-1][y] = self.array[x][y]+1
            self.spreadNegative((x-1, y), value+1)
        if y < self.dimension -1:
          if value+1 <= self.array[x][y+1] <= 0:
            self.array[x][y+1] = self.array[x][y]+1
            self.spreadNegative((x, y+1), value+1)
        if y > 0:
          if value+1 <= self.array[x][y-1] <= 0:
            self.array[x][y-1] = self.array[x][y]+1
            self.spreadNegative((x, y-1), value+1)