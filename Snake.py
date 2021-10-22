import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
  rows = 20
  w = 500
  def __init__(self, start, dx = 1, dy = 0, color = (255, 0, 0)):
    self.pos = start
    self.dx = 1
    self.dy = 0
    self.color = color

  def move(self, dx, dy):
    self.dx = dx
    self.dy = dy

    self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

  def draw(self, surface, eyes = False):
    dist = self.w // self.rows

    i = self.pos[0]
    j = self.pos[1]

    pygame.draw.rect(surface, self.color, (i * dist + 1, j * dist + 1, dist - 2, dist - 2))

    if eyes:
      center = dist // 2
      radius = 3
      circleMid = (i * dist + center - radius, j * dist + 8)
      circleMid2 = (i * dist + dist - radius * 2, j * dist + 8)
      pygame.draw.circle(surface, (0, 0, 0), circleMid, radius)
      pygame.draw.circle(surface, (0, 0, 0), circleMid2, radius)


class snake(object):
  body = []
  turns = {}

  def __init__(self, color, pos):
    self.color = color
    self.head = cube(pos)
    self.body.append(self.head)
    self.dx = 0
    self.dy = 1

  def move(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      keys = pygame.key.get_pressed()

      for key in keys:
        if keys[pygame.K_LEFT]:
          self.dx = -1
          self.dy = 0
          self.turns[self.head.pos[:]] = [self.dx, self.dy]
        elif keys[pygame.K_RIGHT]:
          self.dx = 1
          self.dy = 0
          self.turns[self.head.pos[:]] = [self.dx, self.dy]
        elif keys[pygame.K_UP]:
          self.dy = -1
          self.dx = 0
          self.turns[self.head.pos[:]] = [self.dx, self.dy]
        elif keys[pygame.K_DOWN]:
          self.dy = 1
          self.dx = 0
          self.turns[self.head.pos[:]] = [self.dx, self.dy]
    for i, c in enumerate(self.body):
      p = c.pos[:]
      if p in self.turns:
        turn = self.turns[p]
        c.move(turn[0], turn[1])
        if i == len(self.body) - 1:
          self.turns.pop(p)
      else:
        if c.dx == -1 and c.pos[0] <= 0:
          c.pos = (c.rows - 1, c.pos[1])
        elif c.dx == 1 and c.pos[0] >= c.rows - 1:
          c.pos = (0, c.pos[1])
        elif c.dy == 1 and c.pos[1] >= c.rows - 1:
          c.pos = (c.pos[0], 0)
        elif c.dy == -1 and c.pos[1] <= 0:
          c.pos = (c.pos[0], c.rows - 1)
        else:
          c.move(c.dx, c.dy)

  def reset(self, pos):
    self.head = cube(pos)
    self.body = []
    self.body.append(self.head)
    self.turns = {}
    self.dx = 0
    self.dy = 0

  def addCube(self):
    tail = self.body[-1]
    dx, dy = tail.dx, tail.dy

    if dx == 1 and dy == 0:
      self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
    elif dx == -1 and dy == 0:
      self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
    elif dx == 0 and dy == 1:
      self.body.append(cube((tail.pos[0], tail.pos[1] -1)))
    elif dx == 0 and dy == -1:
      self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

    self.body[-1].dx = dx
    self.body[-1].dy = dy

  def draw(self, surface):
    for i, c in enumerate(self.body):
      if i == 0:
        c.draw(surface, True)
      else:
        c.draw(surface)

def drawGrid(w, rows, surface):
  sizeBetween = w // rows
  x = 0
  y = 0

  for l in range(rows):
    x += sizeBetween
    y += sizeBetween

    pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
    pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
  global rows, width, s, snack
  surface.fill((0, 0, 0))
  s.draw(surface)
  snack.draw(surface)
  drawGrid(width, rows, surface)
  pygame.display.update()

def ranSnack(rows, item):
  positions = item.body

  while True:
    x = random.randrange(rows)
    y = random.randrange(rows)

    if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0:
      continue
    else:
      break

  return (x,y)

def message_box(subject, content):
  root = tk.Tk()
  root.attributes("-topmost", True)
  root.withdraw()
  messagebox.showinfo(subject, content)
  try:
    root.destroy()
  except:
    pass

def main():
  global width, rows, s, snack
  width = 500
  rows = 20
  win = pygame.display.set_mode((width, width))
  s = snake((255, 0, 0), (10, 10))
  snack = cube(ranSnack(rows, s), color = (0, 255, 0))
  
  clock = pygame.time.Clock()

  flag = True
  while flag:
    pygame.time.delay(50)
    clock.tick(10)
    s.move()
    if s.body[0].pos == snack.pos:
      s.addCube()
      snack = cube(ranSnack(rows, s), color = (0, 255, 0))

    for x in range(len(s.body)):
      if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
        print("Score", len(s.body))
        message_box("You Lose!", f"Score: {len(s.body)}")
        s.reset((10, 10))
        break

    redrawWindow(win)

main()
