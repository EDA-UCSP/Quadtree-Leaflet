
def is_point_in_rect(point, bottomLeft, topRight):
  return point.x > bottomLeft.x and \
         point.x < topRight.x and \
         point.y > bottomLeft.y and \
         point.y < topRight.y

def is_point_in_circle(point, circle):
  dst_x = point.x - circle.x
  dst_y = point.y - circle.y
  return dst_x * dst_x + dst_y * dst_y < circle.value * circle.value

class Point:
  def __init__(self, x, y, value = None):
    self.x = x
    self.y = y
    self.value = value

# The QuadTree
class QuadTree:
  def __init__(self, capacity = 5, bottomLeft = Point(-200, -200, None), topRight = Point(200, 200, None)):
    self.northWest = None
    self.northEast = None
    self.southWest = None
    self.southEast = None
    self.bottomLeft = bottomLeft
    self.topRight = topRight
    self.points = []
    self.capacity = capacity

  def add_point(self, point):
    if self.is_inside(point):
      if self.is_leaf(): 
        if len(self.points) < self.capacity: 
          self.points.append(point)
        
        else:
          self.split()
          for p in self.points:
            self.northWest.add_point(p)
            self.northEast.add_point(p)
            self.southWest.add_point(p)
            self.southEast.add_point(p)

          self.northWest.add_point(point)
          self.northEast.add_point(point)
          self.southWest.add_point(point)
          self.southEast.add_point(point)
          self.points = []

      else:
        self.northWest.add_point(point)
        self.northEast.add_point(point)
        self.southWest.add_point(point)
        self.southEast.add_point(point)

  def get_points_in_rect(self, bottomLeft, topRight):
    if not self.is_overlapping(bottomLeft, topRight):
      return []
    result = []
    if self.is_leaf():
      for p in self.points:
        if is_point_in_rect(p, bottomLeft, topRight):
          result.append(p)
    
    else:
      result.extend(self.northWest.get_points_in_rect(bottomLeft, topRight))
      result.extend(self.northEast.get_points_in_rect(bottomLeft, topRight))
      result.extend(self.southWest.get_points_in_rect(bottomLeft, topRight))
      result.extend(self.southEast.get_points_in_rect(bottomLeft, topRight))
    return result

  def is_overlapping(self, bottomLeft, topRight):
    if self.bottomLeft.x > topRight.x or bottomLeft.x > self.topRight.x:
      return False
    if self.bottomLeft.y > topRight.y or bottomLeft.y > self.topRight.y:
      return False
    return True

  def split(self):
    x_low = self.bottomLeft.x
    y_low = self.bottomLeft.y
    x_high = self.topRight.x
    y_high = self.topRight.y
    x_mid = self.bottomLeft.x + (self.topRight.x - self.bottomLeft.x) / 2
    y_mid = self.bottomLeft.y + (self.topRight.y - self.bottomLeft.y) / 2
    self.northWest = QuadTree(capacity=self.capacity, bottomLeft=Point(x_low, y_mid), topRight=Point(x_mid, y_high))
    self.northEast = QuadTree(capacity=self.capacity, bottomLeft=Point(x_mid, y_mid), topRight=Point(x_high, y_high))
    self.southWest = QuadTree(capacity=self.capacity, bottomLeft=Point(x_low, y_low), topRight=Point(x_mid, y_mid))
    self.southEast = QuadTree(capacity=self.capacity, bottomLeft=Point(x_mid, y_low), topRight=Point(x_high, y_mid))

  def is_leaf(self):
    return self.northWest is None and \
           self.northEast is None and \
           self.southWest is None and \
           self.southEast is None 
  
  def is_inside(self, point):
    return point.x > self.bottomLeft.x and \
           point.y > self.bottomLeft.y and \
           point.x < self.topRight.x and \
           point.y < self.topRight.y

from matplotlib import pyplot as plt
import random
import time
import pandas as pd 
def draw_quadtree(ax, qt):
  nodes = [qt]
  x1 = qt.bottomLeft.x
  x2 = qt.topRight.x
  y1 = qt.bottomLeft.y
  y2 = qt.topRight.y
  ax.plot([x1, x2], [y1, y1], '-k')
  ax.plot([x1, x2], [y2, y2], '-k')
  ax.plot([x1, x1], [y1, y2], '-k')
  ax.plot([x2, x2], [y1, y2], '-k')
  while nodes: 
    node = nodes.pop()
    if node.is_leaf():
      continue
    x1 = node.bottomLeft.x
    x2 = node.topRight.x
    y1 = node.bottomLeft.y
    y2 = node.topRight.y
    ax.plot([(x1+x2) / 2, (x1+x2) / 2], [y1, y2], '-k')
    ax.plot([x1, x2], [(y1+y2) / 2, (y1+y2) / 2], '-k')
    nodes.append(node.northWest)
    nodes.append(node.northEast)
    nodes.append(node.southWest)
    nodes.append(node.southEast)


points=[]
qt = QuadTree(10000)
df = pd.read_csv("points.tsv", sep='\t' ,header=None)
points = [Point(float(df.iloc[x,0]), float(df.iloc[x,1])) for x in range(1000000)]
fig, ax = plt.subplots()  #create figure and axes
ax.plot([p.x for p in points], [p.y for p in points], 'r.', label="Points") # Plot points
print("Termino de agrregar al arreglo")
# Add points to quadtree
for p in points:
    qt.add_point(p)

# Plot the quadtree
draw_quadtree(ax, qt)

plt.legend()
plt.show()
