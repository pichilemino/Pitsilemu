#! /usr/bin/env python
# -*- coding: utf-8 -*-
#10-10-08 Pasqual

import random, re

def dec2bin(num):
	if not re.search("^\d+$", num):
		return "nops"
	num=int(num)
	next=num
	bin=[]
	while next != 0:
		bin.append(str(next%2))
		next = int(next) / 2
	bin.reverse()
	bin ="".join(bin) if bin else 0
	return bin

def bin2dec(num):
	if re.search("^[10]+$",num):
		splitted=[]
		for n in num:
			splitted.append(int(n))
		splitted.reverse()
		p=0
		n=0
		for i in splitted:
			n+=i*2**p
			p+=1
		return n

#based on http://code.activestate.com/recipes/81611/
def dec2rom(num):
   """
   Convert an integer to Roman numerals.
   """
   if type(num) == int:
	num=str(num)
   if not re.search("^\d+$", num):
       return
   num = int(num)
   #print "numbers.py num:",type(num), num
   if not 0 < num < 4000:
      return "l'argument ha d'estar entre 1 i 3999" #raise ValueError, "Argument must be between 1 and 3999"   
   ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
   result = ""
   for i in range(len(ints)):
      count = int(num / ints[i])
      result += nums[i] * count
      num -= ints[i] * count
   return result

def rom2dec(num):
   """
   Convert a roman numeral to an integer.
   """

   if not re.search("[MDCLXVI]+",num, re.I):
      return ""
   num = num.upper()
   nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
   ints = [1000, 500, 100, 50,  10,  5,   1]
   places = []

   for i in range(len(num)):
      c = num[i]
      value = ints[nums.index(c)]
      # If the next place holds a larger number, this value is negative.
      try:
         nextvalue = ints[nums.index(num[i +1])]
         if nextvalue > value:
            value *= -1
      except IndexError:
         # there is no next place.
         pass
      places.append(value)
   sum = 0
   for n in places: sum += n
   # Easiest test for validity...
   if dec2rom(sum) == num:
      return sum
   else:
      return 'los datos no son correctos: %s' % num

#test
def call_d2b():	
        dec_num=True
        i=0
        p=False
        sortejats=[]
        repes=[]
        while i<=5000:
            i+=1
            dec_num=random.randint(0,2000)
            bin_num=dec2bin(dec_num)
            if dec_num in sortejats:
                p=True
                repes.append(dec_num)
                continue
            else:
                sortejats.append(dec_num)
            if dec_num<=10:
                p=True
                break
            print dec_num, "<:>", bin_num

        if p: print dec_num, "<:>", bin_num
        print "nombre de tirs:",i
        print len(repes),"repes:", repes

def call_dec_to_roman():
	for i in range(1, 21): print dec2rom(i)

if __name__ == "__main__":
	#call_d2b()
	#print dec2rom(1329)
	print bin2dec("110010101101")
	print dec2bin("3245")
	
