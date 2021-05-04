
def punto_rectangulo(punto, abajo_izquierda, arriba_derecha):
  return punto.x > abajo_izquierda.x and \
         punto.x < arriba_derecha.x and \
         punto.y > abajo_izquierda.y and \
         punto.y < arriba_derecha.y

class Punto:
  def __init__(self, x, y, value = None):
    self.x = x
    self.y = y
    self.value = value

class QuadTree:
  def __init__(self, capacidad = 5, abajo_izquierda = Punto(-200, -200, None), arriba_derecha = Punto(200, 200, None)):
    self.noroeste = None
    self.noreste = None
    self.suroeste = None
    self.sureste = None
    self.abajo_izquierda = abajo_izquierda
    self.arriba_derecha = arriba_derecha
    self.puntos = []
    self.capacidad = capacidad

  def add_punto(self, punto):
    if self.esta_dentro(punto):
      if self.es_hoja(): 
        if len(self.puntos) < self.capacidad: 
          self.puntos.append(punto)
        
        else:
          self.split()
          for p in self.puntos:
            self.noroeste.add_punto(p)
            self.noreste.add_punto(p)
            self.suroeste.add_punto(p)
            self.sureste.add_punto(p)

          self.noroeste.add_punto(punto)
          self.noreste.add_punto(punto)
          self.suroeste.add_punto(punto)
          self.sureste.add_punto(punto)
          self.puntos = []

      else:
        self.noroeste.add_punto(punto)
        self.noreste.add_punto(punto)
        self.suroeste.add_punto(punto)
        self.sureste.add_punto(punto)

  def get_punto_rectan(self, abajo_izquierda, arriba_derecha):
    if not self.sobrepuesto(abajo_izquierda, arriba_derecha):
      return []
    result = []
    if self.es_hoja():
      for p in self.puntos:
        if punto_rectangulo(p, abajo_izquierda, arriba_derecha):
          result.append(p)
    
    else:
      result.extend(self.noroeste.get_punto_rectan(abajo_izquierda, arriba_derecha))
      result.extend(self.noreste.get_punto_rectan(abajo_izquierda, arriba_derecha))
      result.extend(self.suroeste.get_punto_rectan(abajo_izquierda, arriba_derecha))
      result.extend(self.sureste.get_punto_rectan(abajo_izquierda, arriba_derecha))
    return result

  def sobrepuesto(self, abajo_izquierda, arriba_derecha):
    if self.abajo_izquierda.x > arriba_derecha.x or abajo_izquierda.x > self.arriba_derecha.x:
      return False
    if self.abajo_izquierda.y > arriba_derecha.y or abajo_izquierda.y > self.arriba_derecha.y:
      return False
    return True

  def split(self):
    x_low = self.abajo_izquierda.x
    y_low = self.abajo_izquierda.y
    x_high = self.arriba_derecha.x
    y_high = self.arriba_derecha.y
    x_mid = self.abajo_izquierda.x + (self.arriba_derecha.x - self.abajo_izquierda.x) / 2
    y_mid = self.abajo_izquierda.y + (self.arriba_derecha.y - self.abajo_izquierda.y) / 2
    self.noroeste = QuadTree(capacidad=self.capacidad, abajo_izquierda=Punto(x_low, y_mid), arriba_derecha=Punto(x_mid, y_high))
    self.noreste = QuadTree(capacidad=self.capacidad, abajo_izquierda=Punto(x_mid, y_mid), arriba_derecha=Punto(x_high, y_high))
    self.suroeste = QuadTree(capacidad=self.capacidad, abajo_izquierda=Punto(x_low, y_low), arriba_derecha=Punto(x_mid, y_mid))
    self.sureste = QuadTree(capacidad=self.capacidad, abajo_izquierda=Punto(x_mid, y_low), arriba_derecha=Punto(x_high, y_mid))

  def es_hoja(self):
    return self.noroeste is None and \
           self.noreste is None and \
           self.suroeste is None and \
           self.sureste is None 
  
  def esta_dentro(self, punto):
    return punto.x > self.abajo_izquierda.x and \
           punto.y > self.abajo_izquierda.y and \
           punto.x < self.arriba_derecha.x and \
           punto.y < self.arriba_derecha.y

from matplotlib import pyplot as plt
import random
import time
import pandas as pd 
def draw_quadtree(ax, qt):
  nodes = [qt]
  x1 = qt.abajo_izquierda.x
  x2 = qt.arriba_derecha.x
  y1 = qt.abajo_izquierda.y
  y2 = qt.arriba_derecha.y
  ax.plot([x1, x2], [y1, y1], '-k')
  ax.plot([x1, x2], [y2, y2], '-k')
  ax.plot([x1, x1], [y1, y2], '-k')
  ax.plot([x2, x2], [y1, y2], '-k')
  while nodes: 
    node = nodes.pop()
    if node.es_hoja():
      continue
    x1 = node.abajo_izquierda.x
    x2 = node.arriba_derecha.x
    y1 = node.abajo_izquierda.y
    y2 = node.arriba_derecha.y
    ax.plot([(x1+x2) / 2, (x1+x2) / 2], [y1, y2], '-k')
    ax.plot([x1, x2], [(y1+y2) / 2, (y1+y2) / 2], '-k')
    nodes.append(node.noroeste)
    nodes.append(node.noreste)
    nodes.append(node.suroeste)
    nodes.append(node.sureste)


puntos=[]
qt = QuadTree(2)
df = pd.read_csv("points.tsv", sep='\t' ,header=None)
puntos = [Punto(float(df.iloc[x,0]), float(df.iloc[x,1])) for x in range(100)]
fig, ax = plt.subplots()  #create figure and axes
ax.plot([p.x for p in puntos], [p.y for p in puntos], 'r.', label="Puntos") # Plot puntos
print("Termino de agrregar al arreglo")
# Add puntos to quadtree
for p in puntos:
    qt.add_punto(p)

# Plot the quadtree
draw_quadtree(ax, qt)

plt.legend()
plt.show()
