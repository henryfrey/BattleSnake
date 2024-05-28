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
      self.food : List= [] #[x,y]
      self.head = [0,0]

    def distanceToPoint(self,pointHead, pointDesirable):
      return abs(pointHead[0] - pointDesirable[0]) + abs(pointHead[1] - pointDesirable[1])

    def fillMap(self, request):
      self.turn = request['turn']
      board = request['board']
      mySnake = request['you']
      self.size = mySnake['length']
      self.health = mySnake['health']
      body = mySnake['body']
      self.head  = [body[0]['x'], body[0]['y']]
      for i in range(len(body)):
        self.array[body[i]['x']][body[i]['y']] = -1000

      
      snakes = board['snakes']
      for i in range(1,len(snakes)):
        body = snakes[i]['body']
        head = body[0]
        self.snakeInfo += [([head['x'], head['y']], snakes[i]['length'])]
        for j in range(len(body)-1):
          self.array[body[j]['x']][body[j]['y']] = -1000
        if snakes[i]['length'] >= self.size:
          self.array[head['x']+1][head['y']] = -1000
          self.array[head['x']-1][head['y']] = -1000
          self.array[head['x']][head['y']+1] = -1000
          self.array[head['x']][head['y']-1] = -1000

      food = board['food']
      for i in range(len(food)):
        closest = True
        point = [food[i]['x'], food[i]['y']]
        for i in self.snakeInfo:
          if self.distanceToPoint(i[0], point) < self.distanceToPoint(self.head, point):
            closest = False
            break
          if self.distanceToPoint(i[0], point) == self.distanceToPoint(self.head, point) and self.size <= i[1]:
            closest = False
            break
        if closest:
          self.array[point[0]][point[1]] = 10
          self.food += [(point[0], point[1])]
        
    def spread(self, point):
      x, y = point
      if self.dimension >= x >= 0 == self.array[x][y] and 0 <= y <= self.dimension:
        self.array[x+1][y] += self.array[x][y]-1
        self.array[x-1][y] += self.array[x][y]-1
        self.array[x][y+1] += self.array[x][y]-1
        self.array[x][y+1] += self.array[x][y]-1
        self.spread((x+1, y))
        self.spread((x-1, y))
        self.spread((x, y+1))
        self.spread((x, y-1))
  
    def evaluateMap(self):
      if not(len(self.food) > 0):
        for i in self.food:
          self.spread(i)
      