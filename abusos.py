# -*- coding: utf-8 -*-
import time

class Abuso:
 def __init__(self):
  '''
  {'nick': ['nick', nivel_de_aviso, hasta que epoch no puede hablar, (epoch, 'comando', antikarma)]}
  {'yrithinnd': ['yrithinnd', 2, 1162853279, (1162853158, 'mant', 6), (1162853158, 'mant', 6), (1162853159, 'mant', 6)]}
  '''
  self.abuse = {}
 
 def creakey(self,nick):
  if not self.abuse.has_key(nick):
   self.abuse[nick]=[nick,1,0]

 def puedehablar(self,nick):
  '''
  Devuelve si el usuario puede hablar
  '''
  if not self.abuse.has_key(nick): #si no está registrado es porqué es inmune
	return
  return self.abuse[nick][2]<int(time.time())

 def limpiacaducados(self,nick):
  '''
  Borra los comandos obsoletos (1 minuto de memoria)
  '''
  for i in self.abuse[nick][3:]:
   if i[0]<(int(time.time())-60):
    self.abuse[nick].pop(3)

 def registracomando(self,nick,comando,valor):
  '''
  Añade el último comando al hash
  '''
  if not self.abuse.has_key(nick): #si no está registrado es porqué es inmune
	return
  self.abuse[nick].append((int(time.time()),comando,valor))
  self.abuso1(nick)
  self.abuso2(nick)

 def abuso1(self,nick):
  '''19 puntos en < 1 minuto'''
  cuenta=0
  for i in self.abuse[nick][3:len(self.abuse)]:
   cuenta+=i[2]
   if cuenta >19:
    self.abuse[nick][2]=int(time.time())+((2**self.abuse[nick][1])*60)
    self.abuse[nick][1]+=1
    if self.abuse[nick][1]>6:
     self.abuse[nick][1]=6
    return True
  return False

 def abuso2(self,nick):
  '''19 puntos en < 1 minuto'''
  cuenta=0
  for i in self.abuse[nick][3:len(self.abuse)]:
   cuenta+=i[2]
   if cuenta >19:
    self.abuse[nick][2]=int(time.time())+((2**self.abuse[nick][1])*60)
    self.abuse[nick][1]+=1
    if self.abuse[nick][1]>6:
     self.abuse[nick][1]=6
    return True
  return False
