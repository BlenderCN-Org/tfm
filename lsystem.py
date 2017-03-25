from math import pi
from random import random
import sys


##################################################
#        L-system Grammar implementation         #
##################################################

class Grammar(object):
   productions={}
   intialSymbol=''
   roomsL=1
   roomsR=0
   meeting=1
   bathroom=1
   noise = [0.0]

   def getProductions(self, left, rightstr):
      self.productions[left]=[] 
      index=0
      while(index<len(rightstr)):
         index=rightstr.find("(",index) 
         if(index==-1): 
             return
         index+=1 
         while(rightstr[index]==' '): 
            index+=1
         prob=float(rightstr[index:rightstr.find(' ',index+1)])
         index=rightstr.find(' ',index)
         right=rightstr[index:rightstr.find(')',index+1)].strip()
         self.productions[left].append([right,prob])
          
   def __init__(self,filename):
      #print("filename = ", filename)
      f = open(filename, "r")
      line=f.readline()
      params = [int(x.strip()) for x in line.split(',')]
      self.meeting = params[0]
      self.bathroom = params[1]
      self.roomsL = params[2]
      self.roomsR = params[3]
      line = f.readline()
      # The second line is the initial symbol
      self.initialSymbol=line.rstrip()
      line=f.readline()
      while (line!="" and "->" in line):
         left=line[:line.find("->")].strip()
         self.getProductions(left,line[line.find("->")+2:])
         line=f.readline()

      if self.roomsL < 0 or self.roomsR < 0:
         sys.exit("\n### ERROR: Office room number can only be either zero or positive. Program terminated.\n")
      if self.roomsL == 0 and self.roomsR == 0 and (self.meeting == 1 or self.bathroom == 1):
         print("\n### WARNING: No office rooms to generate.\n")
      if self.roomsL == 0 and self.roomsR == 0 and self.meeting == 0 and self.bathroom == 0:
         sys.exit("\n### ERROR: No rooms to generate at all. Program terminated.\n")
      if (line != ""):
         noises = line
         self.noise = [float(x.strip()) for x in noises.split(',')]
         if len(self.noise) != (self.roomsL + self.roomsR + self.meeting + self.bathroom) and len(self.noise) != 1:
            sys.exit("\n### ERROR: Noise list length does not match the number of office rooms to generate. Program terminated.\n")


   def applyProductions(self,axiom):
      res = ""
      for s in axiom:
         if(s in self.productions):
            # If the axiom is in a left part of a rule
            # we have to decide which right part to follow
            # according to the probability distribution
            # Let's roll the dice ! 
            r=random()            
            i=0
            acum=self.productions[s][0][1]
            while(acum<r and i<len(self.productions[s])): 
               i+=1
               acum+=self.productions[s][i][1]                  
            res=res+self.productions[s][i][0] 
         else:
            res = res + s
      return res

   def deriveString(self,level):
      # Generates a string from the grammar by iteratively applying productions
      # until the number of iterations reachs "level"

      res = self.initialSymbol
      for n in range(level):
         res=self.applyProductions(res)
      return res
