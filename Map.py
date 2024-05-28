import math as m
import numpy as num

class Map:
    def __init__(self, length):
      self.array = num.zeros((length, length))
      self.turn = 0
      self.health = 100
      self.size = 3
      
    def fillMap(self, request):
      self.turn = request['turn']
      board = request['board']
      food = board['food']
      for i in range(len(food)):
        self.array[food[i]['x']][food[i]['y']] = 10
      mySnake = request['you']
      self.size = mySnake['length']
      self.health = mySnake['health']
      body = mySnake['body']
      for i in range(len(body)):
        self.array[body[i]['x']][body[i]['y']] = -m.inf
      snakes = board['snakes']
      for i in range(len(snakes)):
        body = snakes[i]['body']
        head = body[0]
        if snakes[i]['length'] >= self.size:
          for j in range(len(body)-1):
            self.array[body[i]['x']][body[i]['y']] = -m.inf
          self.array[head['x']+1][head['y']] = -m.inf
          self.array[head['x']-1][head['y']] = -m.inf
          self.array[head['x']][head['y']+1] = -m.inf
          self.array[head['x']][head['y']-1] = -m.inf

    def evaluateMap(self):

    def distanceToPoint(pointHead, pointDesirable):
      return abs(pointHead[0] - pointDesirable[0]) + abs(pointHead[1] - pointDesirable[1])
      
      
      