import math as m
from typing import List
import numpy as num

class Map:
    def __init__(self, length):
      self.array = num.zeros((length, length)).astype(int)
      self.dimension = length
      self.turn = 0
      self.health = 100
      self.size = 3
      self.snakeInfo : List = [] #[[x,y],length]
      self.food : List= [] #(x,y)
      self.head = [0,0]

    def fillMap(self, request):
      self.turn = request['turn']
      board = request['board']
      mySnake = request['you']
      self.head = [mySnake['head']['x'],mySnake['head']['y']]
      self.size = mySnake['length']
      self.health = mySnake['health']
      
      food = board['food']
      for i in range(len(food)):
        self.food.append((food[i]['x'], food[i]['y']))
        self.array[food[i]['x']][food[i]['y']] = 100

      snakes = board['snakes']
      for i in range(len(snakes)):
        body = snakes[i]['body']
        head = body[0]
        x = head['x']
        y = head['y']
        self.snakeInfo += [([x, y], snakes[i]['length'])]
        if snakes[i]['length'] >= self.size and [x,y] != self.head:
          if x < self.dimension -1:
            self.array[x+1][y] = -500
          if x > 0:
            self.array[x-1][y] = -500
          if y < self.dimension -1:
            self.array[x][y+1] = -500
          if y > 0:
            self.array[x][y-1] = -500
        for j in range(len(body)-1):
          self.array[body[j]['x']][body[j]['y']] = -1000
      
      
        
    def spread(self, point, value):
      x, y = point
      if self.array[x][y] == 0 or self.array[x][y] == value:
        if x < self.dimension -1:
          if self.array[x+1][y] == 0 or self.array[x+1][y] == value:
            self.array[x+1][y] += self.array[x][y]-1
            self.spread((x+1, y), value-1)
        if x > 0:
          if self.array[x-1][y] == 0 or self.array[x-1][y] == value:
            self.array[x-1][y] += self.array[x][y]-1
            self.spread((x-1, y), value-1)
        if y < self.dimension -1:
          if self.array[x][y+1] == 0 or self.array[x][y+1] == value:
            self.array[x][y+1] += self.array[x][y]-1
            self.spread((x, y+1), value-1)
        if y > 0:
          if self.array[x][y-1] == 0 or self.array[x][y-1] == value:
            self.array[x][y-1] += self.array[x][y]-1
            self.spread((x, y-1), value-1)
            
  
    def evaluateMap(self):
      if len(self.food) > 0:
        for i in range (len(self.food)):
          self.spread(self.food[i], 100)
      