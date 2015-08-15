#! /usr/bin/env python
# -*- coding: utf-8 -*-

import bz2, codecs, pickle, re, time, urllib, urllib2
import net
from datetime import datetime

def desaobj(obj,file): #Guarda un objeto en un fichero
	f = bz2.BZ2File(file, 'w')
	pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
	f.close()

def lligobj(file): #Lee un fichero y devuelve el objeto
	f = bz2.BZ2File(file, 'r')
	obj = pickle.load(f)
	f.close()
	return obj

reAutoritzats= re.compile(r"pasqual|iradigalesc|misterwiki|yrithinnd",re.I)
reImmunes=re.compile(r"pasqual|iradigalesc|cestmoi|yrithinnd|drini|misterwiki|gustavo86")
opmods=[] #operadors i moderadors (usuaris autoritzats)
ops=[]
mods=[]
tz=7200
chanlog=codecs.open("chanlog.log","a","utf-8")

BLACK=u"\x0301"
BLUE=u"\x0312"
BOLD=u"\x02"
BROWN=u"\x0305"
CYAN=u"\x0311"
DARK_BLUE=u"\x0302"
DARK_GRAY=u"\x0314"
DARK_GREEN=u"\x0303"
GREEN=u"\x0309"
LIGHT_GRAY=u"\x0315"
MAGENTA=u"\x0313"
NORMAL=u"\x0f"
OLIVE=u"\x0307"
PURPLE=u"\x0306"
RED=u"\x0304"
REVERSE=u"\x16"
TEAL=u"\x0310"
UNDERLINE=u"\x1f"
WHITE=u"\x0300"
YELLOW=u"\x0308"

def colors(txt):
        txt=txt.replace("$b",BLACK)
        txt=txt.replace("$l",BLUE)
        txt=txt.replace("$B",BOLD)
        txt=txt.replace("$r",BROWN)
        txt=txt.replace("$c",CYAN)
        txt=txt.replace("$%l",DARK_BLUE)
        txt=txt.replace("$%g",DARK_GRAY)
        txt=txt.replace("$%v",DARK_GREEN)
        txt=txt.replace("$e",GREEN)
        txt=txt.replace("$g",LIGHT_GRAY)
        txt=txt.replace("$m",MAGENTA)
        txt=txt.replace("$N",NORMAL)
        txt=txt.replace("$o",OLIVE)
        txt=txt.replace("$p",PURPLE)
        txt=txt.replace("$r",RED)
        txt=txt.replace("$I",REVERSE)
        txt=txt.replace("$t",TEAL)
        txt=txt.replace("$U",UNDERLINE)
        txt=txt.replace("$w",WHITE)
        txt=txt.replace("$y",YELLOW)
        return txt
        

def parseinput(txt, c, chan, nick):
	a=""
	try:
		a=unicode(txt, 'utf-8')
	except UnicodeError:
		try:
			a=unicode(txt, 'latin-1')
		except UnicodeError:
			c.privmsg(chan, "Please use utf-8")
			print u"Indetermined codification."
	return a

def nomVP(usr):
	"""
	facilita el nom que té l'usuari a la viquipèdia, qualsevol altre que puga posar-se
	per fer-los conicidir amb les dades del registre d'usuaris.
	"""
	usuari=usr
	if usr.lower()=="iradi":
		usuari="Iradigalesc"
	if usr.lower()=="misterwiki":
		usuari="MisterWiki"
	elif usr.lower() == "jordicc":
		usuari="Jordicollcosta"
	elif usr.lower()=="krls-ca":
		usuari = "KRLS"
	elif usr.lower() =="lohen":
		usuari = "Lohen11"
	elif usr.lower() =="lepti":
		usuari = "Leptictidium"
	elif "pasqual|" in usr.lower():
		usuari="Pasqual"
	elif usr.lower() =="smp_ca" or usr.lower() =="smp-ca":
		usuari = "SMP"
	elif usr.lower() =="xtv-ca":
		usuari="Xtv"
	elif usr.lower() =="davidian":
		usuari="Schizodelight"
	elif usr.lower() in ["xpoferens", "xpofol"]:
		usuari="XpoferenS"
	elif usr.lower() == "mafoto":
		usuari="MiguelAngel fotografo"
	elif usr.lower() == "terere":
		usuari=u"Góngora"
	elif usr.lower() == "innat":
		usuari="InNaT"
	elif usr.lower() == "pericallis":
		usuari="Alvaro_qc"
	elif usr.lower() == "hub_es":
		usuari="HUB"
	return usuari

def tam(pagina):
	t1=time.time()
	data = net.pageWiki(pagina)
	salida = net.pageURL(pagina)
	if len(data)>1024:
		salida+= " is %i bytes (%iKb) long." % (len(data), len(data)/1024)
	else:
		salida+= " is %i bytes long." % (len(data))
	salida+= "Took %f seconds." % (time.time()-t1)
	return salida

def size(data): #in contruction
	m=re.search("(.*?:)?(.*?)",data)
	if m:
		langs=m.group(1)
		if langs:
				langs=langs.split("|")
		titles=m.group(2)
		if len(langs)>3:
			langs=langs[0:2]
		for lang in langs:
			urllib.quote(titles,safe=":")
			url="http://%s.wikinews.org/w/api.php?action=query&prop=info&titles=%s" % (lang,trurl(title))
			size = net.api_size(url)
			return size

def fetch(pagina):
	data=net.pageWiki(pagina)
	if not data:
		return "\x0304Page not found.\x0f"
	data=data.replace("\r", "·")
	data=data.replace("\n", "·")
	data=re.sub("\[\[[Ii]mage?:.*?\]\]","",data)
	data=re.sub("'''(.*?)'''","\x02\x0301\g<1>\x0f",data)
	data=re.sub("\[\[([^\]]*?)\|(.*?)\]\]","\x0312\g<2>\x0f",data)
	data=re.sub("\[\[(.*?)\]\]","\x0312\g<1>\x0f",data)
	if re.search("^(?:.*:)?special:statistics$", pagina.lower()):
		#cawiki 11-10-08 +/-18:00 CEST   total=321076;good=135139;views=171;edits=2748283;users=19445;activeusers=1108;admins=19;images=3985;jobs=20
		data = data.replace("good","articles").replace("views","views").replace("edits","edits").replace("activeusers","active users").replace("users","users")\
			.replace("images","images").replace("jobs","jobs").replace("admins","admins")
		data=data
		data=data.replace("=",": $l")
		data=data.replace(";","$N, ")
		data=data.decode("utf-8")
		data=data[:-1]+"$N."
		data=colors(data)
		data=data.encode("utf-8")
	elif "Wikipedia:" in pagina:
		pass
	elif " " in data:
		if len(data)>350:
			data=data[:350]
			data=data.split(" ")[:-1]
			data=" ".join(data)
			data=data+"..."
		if data.startswith("#REDIRECT \x0312"):
			link = net.pageURL(pagina).split("/wiki/")[0]+"/wiki/"
			link = link+data[13:-1].replace(" ","_")
			data += " ( %s )." % link
	return data[0:350]
	
def isAlpha(txt):
	test=re.search(r"^[a-záéíóúüñ]+$", txt.lower())
	if test: 
		return True
	return False

def isCalculable(txt):
	test = re.search("^[\d\(\)\+\*\-/^]+$", txt)
	if test: return True
	return False

def trurl(userinput):
	try:
		userinput=urllib.quote(userinput.encode('utf-8', 'replace'))
	except:
		userinput=urllib.quote(userinput)
	userinput=userinput.replace('%2F', '/')
	userinput=userinput.replace("%3A",":")
	userinput=userinput.replace("%20","_")
	return userinput

def apiTime(txt):
        tz=7200
        t=re.search('(?P<y>\d+)-(?P<m>\d+)-(?P<d>\d+)T(?P<h>\d+):(?P<n>\d+):(?P<s>\d+)Z',txt)
        ts=time.mktime((0, 0, 0, 0, 0, 0, 0, 0, 0))
        if txt:
		ts1=time.mktime((int(t.group('y')), int(t.group('m')), int(t.group('d')), int(t.group('h')), int(t.group('n')), int(t.group('s')),0,0,0))
		ts2=datetime(int(t.group('y')), int(t.group('m')), int(t.group('d')), int(t.group('h')), int(t.group('n')), int(t.group('s')))
        return [ts1,ts2]
		

def f_seen(self, origin, match, args): 
   """.seen <nick> - Reports when <nick> was last seen."""
   if origin.sender == '#talis': return
   nick = match.group(2).lower()
   if not hasattr(self, 'seen'): 
      return self.msg(origin.sender, '?')
   if self.seen.has_key(nick): 
      channel, t = self.seen[nick]
      t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))

      msg = "I last saw %s at %s on %s" % (nick, t, channel)
      self.msg(origin.sender, str(origin.nick) + ': ' + msg)
   else: self.msg(origin.sender, "Sorry, I haven't seen %s around." % nick)
f_seen.rule = (['seen'], r'(\S+)')

def f_note(self, origin, match, args): 
   def note(self, origin, match, args): 
      if not hasattr(self.bot, 'seen'): 
         self.bot.seen = {}
      if origin.sender.startswith('#'): 
         # if origin.sender == '#inamidst': return
         self.seen[origin.nick.lower()] = (origin.sender, time.time())

      # if not hasattr(self, 'chanspeak'): 
      #    self.chanspeak = {}
      # if (len(args) > 2) and args[2].startswith('#'): 
      #    self.chanspeak[args[2]] = args[0]

   try: note(self, origin, match, args)
   except Exception, e: print e
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
