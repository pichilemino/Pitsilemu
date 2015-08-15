##! /usr/bin/env python
# -*- coding: utf-8 -*-

# @c = http://en.wikinews.org/w/query.php?what=contribcounter&titles=User:MisterWiki
# @info = http://tools.wikimedia.de/~interiot/cgi-bin/count_edits?dbname=enwiki_p&user=MisterWiki

import os,sys,re,codecs
import threading,thread
import httplib,urllib,urllib2
import time,datetime
import string,math,random
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, nm_to_u
from orewikipedia import *
from funcions import *
from datetime import datetime
from relativedelta import *
import net,boca,config,abusos

def desaReg():
	dicts={'salutacions':dSalutacions,'definicions':dDefinicions,'marques':dMarques,'botops':dBotOps,'ignorats':ignorats, 'flags': flags}
	desaobj(dicts,'dicts.bin')

dicts={}
try:
    #items de dDefinicions:  {element: definicio}
    #items de dSalutacions: {usuari: salutació}
    #items de dMarques: {usuari: marques}
    dicts=lligobj("dicts.bin")
    if dicts:
        dSalutacions = dicts['salutacions']
        dDefinicions = dicts['definicions']
        dMarques = dicts['marques']
        dBotOps  = dicts['botops']
        ignorats= dicts['ignorats'] #argenz 29.12.07.
        flags= dicts['flags']

        print u"log loaded successfully"
except:
    print "log was not loaded successfully"
    dSalutacions={"janedoe": 'salve, oh Jane, doncella de Orlean',
                  "wiki_bot":'Qué tal socio cibernético, Â¿te apetece matar a unos humanoides?',
                  "yrithinnd":'aserejé yrithinnd',"maldoror":'Plegue al cielo que el lector, enardecido y momentáneamente feroz como lo que lee, halle, sin desorientarse, su abrupto y salvaje sendero por entre las desoladas ciénagas de estas páginas sombrías y llenas de veneno',
                  "kordas":'Komo tú por akí? cuerdas',
                  "kokoo":'koookoorookooooo dice el gallo',
                  "hispa":'Ave, magister militum! Bloqueaturi te salutant!',
                  "f-ar":'hola alhen. Dónde estabas vago? Ponte a trabajar condenao!! --> http://en.wikinews.org/wiki/Categor%C3%ADa:Wikipedia:Borrar%20%28definitivo%29',
                  "lourdes":'Bienvenida lourdes',
                  "monica":'Bienvenida monica',
                  "cookie":'Bienvenida cookie',
                  "dianai":'Bienvenida dianai',
                  "nuria":'Bienvenida nuria',
                  "marb":'Bienvenida marb',
                  "^julie^":'Bienvenida ^julie^',
                  "maria":'Bienvenida maria',
                  "eli22":'Bienvenida eli22',
                  "retama":'Bienvenida retama',
                  "isha":'Bienvenida isha',
                  "urumi":'Bienvenida urumi'}
    dDefinicions = {}
    dMarques = {}
    dBotOps={'wikipedia':   ['retama', 'siabef', 'racso', 'edmenb', 'txo', 'paintman', 'jorgechp', 'chabacano', 'gaeddal', 'platonides',
                            'gizmo-ii', 'taichi', 'ejmeza', 'orgullokmoore', 'angus', 'barcex', 'yrithinnd', 'iradigalesc', 'pasqual',
                            'tomatejc', 'gordonrox24', 'misterwiki', 'jamesofur', 'barras_', 'brian_s'],
            'wikimedia':    ['francogg', 'alhen'],
            'wikinews': ['tempodivalse', 'irunongames'],
            'wikia': ['cest-moi']}
    ignorats=[] #Argenz 29.12.07.
    flags={"yrithinnd": "God", "ctrl-z": "Dustman", "ctrl_z": "Dustman", "pasqual":"Allah","iradigalesc":"Botmaker","milo":"camarada",
           "Netito777":"maestro de Jimbo","racso":"War Machine","smp":"Wesnother","xtv":"Rex Gratia Dei","xtv-ca":"Rex Gratia Dei"}

    desaReg()

#variable tipus llista per ennlistar tots els botops del dict dBotOps, mes facil accedir facilment
lBotOps=[]
for proj in dBotOps:
	for op in dBotOps[proj]:
		lBotOps.append(op)

class art( threading.Thread ):

 def __init__ ( self, command, idioma='es', canal=config.canales[0]):
	self.c=command
	self.idioma=idioma
	self.chan = canal
	threading.Thread.__init__ ( self )

 def run ( self ):
	self.articulos(self.c,self.idioma)


 def articleCount(self,xx): #xx es el código de la wiki. Ejemplos - "es:", "en:", "de:"..
	crudo=net.pageText('http://'+xx+'.wikinews.org/w/index.php?title=Special:Statistics&action=raw')
	m=re.search(ur"good=(.*);views=",crudo)
	if m:
		return m.group(1)
	else:
		return 0


 def articulos(self,c,b):
	#if True:
	try:
		articulos=int(self.articleCount(b))
		if b!="es":
			articulos_es=int(self.articleCount("es"))
			if articulos_es < articulos :
				diferencia=str(articulos_es-articulos)+" over"
			elif articulos_es > articulos:
				diferencia=str(articulos-articulos_es)+" below"
			else:
				diferencia ="prepacked with"
			msg=u"http://%s.wikinews.org has %i articles (%s w:es)" %(b, articulos, diferencia)
			c.privmsg(self.chan, msg.encode("utf-8"))
		else:
			msg=u"We have $l%i$N articles... with better quality than the others!!! And now, wikify or I'll kill you!!!" % (articulos)
			msg=colors(msg)
			c.privmsg(self.chan,msg.encode("utf-8"))

			meta     = int(str(articulos)[0])+1
			potencia = len(str(articulos))-1
			meta     = meta*(10**potencia)
			faltan   = meta-articulos
			if faltan<500:
				url="http://en.wikinews.org/w/api.php?action=query&list=recentchanges&rctype=new&rcnamespace=0&rclimit=1&format=xmlfm"
				ultima=net.pageText(url)
				ultima=ultima.split("title=&quot;")[1].split("&quot;")[0]
				msg=u"We have to create $l%i$N to reach the %i articles" % (faltan,meta)
				msg=colors(msg).encode("utf-8")
				c.privmsg(self.chan,msg)
				msg="The article #%i has been: [[$b%s$n]] http://en.wikinews.org/wiki/%s $Bhttp://en.wikinews.org/wiki/Special:Newpages$n" % (articulos, ultima, trurl(ultima))
				msg=colorrs(msg).encode("utf-8")
				c.privmsg(self.chan,msg)
	except :
		boca.respuesta(boca.art_error,100,c,self.chan)


class TestBot(SingleServerIRCBot):
	def __init__(self, channel, nickname, server, port=6667):
		SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
		self.chans = config.canales
		self.channel = channel
		self.nickname = nickname
		self.abuso=abusos.Abuso()

	def on_error(self, c, e):
		#print e.target()
		self.die()

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")
		c.privmsg("NickServ",'GHOST '+self.nickname+' '+config.clave)
		c.nick(self.nickname)
		c.privmsg("NickServ",'IDENTIFY '+config.clave)


	def on_welcome(self, c, e):
		c.privmsg("NickServ",'GHOST '+self.nickname+' '+config.clave)
		c.privmsg("NickServ",'IDENTIFY '+config.clave)
		for canal in self.chans:
			c.join(canal)
		#c.join("#wikipedia-es-400000")

	def on_ctcp(self, c, e):
		if e.arguments()[0] == "VERSION":
			c.ctcp_reply(nm_to_n(e.source()),"VERSION This bot was originally developed as Orejotas by [[ca:Usuari:Pasqual]]. Translated to the English language by [[simple:User:MisterWiki]]")
		elif e.arguments()[0] == "PING":
			if len(e.arguments()) > 1:
				c.ctcp_reply(nm_to_n(e.source()),"PING " + e.arguments()[1])
			elif e.arguments()[0] == "ACTION":
				pass
			else:
				dado=random.randint(1,2)
				if dado==1:
					c.ctcp_reply(nm_to_n(e.source()),"No. Don't blame me.")
				elif dado==2:
					c.ctcp_reply(nm_to_n(e.source()),"Don't touch me.")

	def on_namreply(self, c, e):
		canal=e.arguments()[1]
		conn=self.connection
		if canal==self.channel:
			#conn.privmsg(canal,u"I'm here, don't be scared! :)".encode('utf-8'))
			#obtenim la llista d'usuaris connectats
			usuaris=e.arguments()[2]
			if usuaris.endswith(" "):
				usuaris=usuaris[:-1]
			usuaris=usuaris.split(" ")
			for usuari in usuaris:
				if usuari.startswith("&"):
					ops.append(usuari[1:])
					opmods.append(usuari[1:])
				elif usuari.startswith("+"):
					mods.append(usuari[1:])
					opmods.append(usuari[1:])

	def on_join(self, c, e):
		nick = nm_to_n(e.source())
		if nick.lower() not in [self.nickname, "alhen", "drini"]:
			time.sleep(random.randint(0,4))
			canal=e.target()
			#c.privmsg(self.channel,orefrases.saludo(nick))
			"""
			if nick.lower()=="janedoe":
		        	c.privmsg(self.channel,'salve, oh Jane, doncella de Orlean')
			elif nick.lower()=="wiki_bot":
				c.privmsg(self.channel,'Qué tal socio cibernético, Â¿te apetece matar a unos humanoides?')
			elif nick.lower()=="yrithinnd":
				c.privmsg(self.channel,'aserejé '+nick)
			elif nick.lower()=="maldoror":
				c.privmsg(self.channel,'Plegue al cielo que el lector, enardecido y momentáneamente feroz como lo que lee, halle, sin desorientarse, su abrupto y salvaje sendero por entre las desoladas ciénagas de estas páginas sombrías y llenas de veneno')
			elif nick.lower()=="kordas":
				c.privmsg(self.channel,'KOmo tú por aquí? cuerdas')
			elif nick.lower()=="kokoo":
				c.privmsg(self.channel,'koookoorookooooo dice el gallo')
			elif nick.lower()=="hispa":
				c.privmsg(self.channel,'Ave, magister militum! Bloqueaturi te salutant!')
			elif nick.lower()=="f-ar":
				c.privmsg(self.channel,'FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR FAR')
			elif nick.lower()=="alhen":
				c.privmsg(self.channel,'hola alhen. Dónde estabas vago? Ponte a trabajar condenao!! --> http://en.wikinews.org/wiki/Categor%C3%ADa:Wikipedia:Borrar%20%28definitivo%29')
			elif re.search("^(lourdes|monica|cookie|dianai|nuria|marb|\^juli[ae]\^|maria|eli22|retama|isha|urumi|mushii)$",nick.lower()):
				c.privmsg(self.channel,'Bienvenida '+nick)
			else:
			"""
			#boca.respuesta(boca.saludo, 10, c, canal,(nick,))
		print "%s ha entrat a %s"%(nick, e.target())

	def on_kick(self, c, e):
		nick = nm_to_n(e.source())
		kicked=e.arguments()[0]
		canal=e.target()
		if kicked==self.nickname:
			time.sleep(2)
			c.join(canal)
			c.privmsg(canal,nick+', I will smash your face!')
		else:
			if nick in opmods:
				opmods.remove(nick)
			if nick in ops:
				ops.remove(nick)
			if nick in mods:
				mods.remove(nick)

#	def on_ping(self, c, e):
#		c.privmsg(self.channel,'PING!')
#		c.join(self.channel)

	def on_quit(self,c,e):
		usuari = nm_to_n(e.source())
		if usuari in opmods:
			opmods.remove(usuari)
		if usuari  in ops:
			ops.remove(usuari)
		if usuari  in mods:
			mods.remove(usuari)

	def on_disconnect(self,c,e):
		#print "\n==",e.eventtype(),"\n",e.target(),"\n",e.source(),"\n",e.arguments(),"\n==\n"
		usuari = nm_to_n(e.source())
		if usuari in opmods:
			opmods.remove(usuari)
		if usuari  in ops:
			ops.remove(usuari)
		if usuari  in mods:
			mods.remove(usuari)

	def on_part(self, c, e):
		if e.target()==self.channel:
			usuari = nm_to_n(e.source())
			if usuari in opmods:
				opmods.remove(usuari)
			if usuari  in ops:
				ops.remove(usuari)
			if usuari  in mods:
				mods.remove(usuari)

	def on_mode(self, c, e):
		#print "\n==",e.eventtype(),"\n",e.target(),"\n",e.source(),"\n",e.arguments(),"\n==\n"
		if e.target()==self.channel:
			mode = e.arguments()[0]
			usuaris= e.arguments()[1:]
			for usuari in usuaris:
				if mode[0] =="+":
					if mode[1] == "o" and usuari not in opmods:
						opmods.append(usuari)
						ops.append(usuari)
					if mode[1] == "v" and usuari not in opmods:
						opmods.append(usuari)
						mods.append(usuari)
				else:
					if mode[1] == "o" and usuari in ops:
						opmods.remove(usuari)
						ops.remove(usuari)
					if mode[1] == "v" and usuari in mods:
						opmods.remove(usuari)
						mods.remove(usuari)

	def on_nick(self, c, e):
		#print "\n==",e.eventtype(),"\n",e.target(),"\n",e.source(),"\n",e.arguments(),"\n==\n"
		usuari = str(nm_to_u(e.source()))[2:]
		cloak = nm_to_h(e.source())
		usuariAbans = nm_to_n(e.source())
		usuariAra = e.target()
		canal=self.channel
		conn=self.connection
		#actualitzem llistes
		if usuariAbans in opmods:
			opmods.remove(usuariAbans)
			opmods.append(usuariAra)
		if usuariAbans in mods:
			mods.remove(usuariAbans)
			mods.append(usuariAra)
		if usuariAbans in ops:
			ops.remove(usuariAbans)
			ops.append(usuariAra)

	def on_notice(self, c, e):
		#print "\n==",e.eventtype(),"\n",e.target(),"\n",e.source(),"\n",e.arguments(),"\n==\n"
		pass

	def on_action(self, c, e):
		#print "\n==",e.eventtype(),"\n",e.target(),"\n",e.source(),"\n",e.arguments(),"\n==\n"
		pass

	def on_privmsg(self, c, e):
		nick = nm_to_n(e.source())
		cloak = nm_to_h(e.source())
		canal=self.channel
		a = e.arguments()[0]
		a=parseinput(a, c, nick, nick)
		print "["+time.strftime("%j_%H:%M:%S")+"] Private <"+nick+"> "+a

		if not reImmunes.search(cloak):
			self.abuso.creakey(nick)
			self.abuso.limpiacaducados(nick)
			if not self.abuso.puedehablar(nick):
				print "%s is blocked" % (nick)
				return
		try:
			if a[0]=='@':
				self.do_command(e, string.strip(a[1:]),nick)
			else:
				enlaces=re.finditer(ur"(?<!!)(?:\[\[(.*?)(?:\]\]|\|)|(\{\{(?:subst:|raw:)?(?P<pl>.*?)(?:\|(?P<arg>.*?))?\}\}))",a)
				tope=0
				for i in enlaces:
					argplant=False
					if i.group(2):
						if re.search(ur"\{\{\{|\}\}\}", i.group(2).decode('utf-8', 'replace')):
							argplant=True
					#simulación de enlaces wiki, devuelve la url
					if i.group(1) and not argplant:
						if tope<3:
							c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/"+trurl(i.group(1)).encode('utf-8'))
							self.abuso.registracomando(nick,"enlace "+trurl(i.group(1)),2)
					#simulación de código para plantillas y 'transclusions'
					elif i.group(3) and not argplant:
						if tope<3:
							#convierte {{NAMESPACE:...}} en un enlace a la página indicada, no en un enlace a una página.
							if ":" in i.group('pl'):
								ns=i.group('pl').split(":")[0]
								if re.search(r"us(uario|er)|plantilla|template|mediawiki|categor(ia|ía|y)|imagen?|ayuda|help|wikipedia|project|portal|wikiproyecto|anexo", ns.lower()):
									pag=i.group('pl')
								else:
									pag="Template:"+i.group('pl')
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/"+trurl(pag).encode('utf-8'))
							#{{u|Xxxx}} equivale a [[Usuario:Xxxx]]
							elif i.group('pl')=="u" and i.group('params'):
								usr=i.group('arg')
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/User:"+trurl(usr).encode('utf-8'))
							#{{u|Xxxx}} equivale a [[Usuario Discusión:Xxxx]]
							elif i.group('pl')=="ud" and i.group('params'):
								usr=i.group('arg')
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/User_talk:"+trurl(usr).encode('utf-8'))
							#{{done}}
							elif i.group('pl')=="done":
								c.privmsg(canal, u"how efficient are you!".encode('utf-8'))
							#se supone que es una plantilla...
							else:
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/Template:"+trurl(i.group('pl')).encode('utf-8'))
							self.abuso.registracomando(nick,"plantilla "+trurl(i.group(3)),2)
					tope+=1

		except UnicodeEncodeError, ue:
			print time.strftime("%m-%d %H:%M:%S"), ue

	def on_pubmsg(self, c, e):
		a = e.arguments()[0]
		nick = nm_to_n(e.source())
		canal=e.target()
		a=parseinput(a, c, canal, nick)
		if canal!="#wikipedia-es-sysop":
			print "[%s] {%s} <%s> %s" % (time.strftime("%m-%d %H:%M:%S"),canal,nick, a)
		cloak= nm_to_h(e.source())
		boss = reAutoritzats.search(cloak.lower())

		if canal== "#wikipedia-es-400000":
			if nick == "NumArtics" and "Nuevo articulo" in a:
				arts=art(c, "es")
				arts = arts.articleCount("es")
				arts = int(arts)
				if arts % 5 == 0:
					url="http://en.wikinews.org/w/api.php?action=query&list=recentchanges&rctype=new&rcnamespace=0&rclimit=1&format=xmlfm"
					ultima=net.pageText(url)
					ultima=ultima.split("title=&quot;")[1].split("&quot;")[0]
					msg="The article #%i has been: [[$r%s$n]] http://en.wikinews.org/wiki/%s We have to write $r$N%i$n to reach the 400K $Bhttp://en.wikinews.org/wiki/Special:Newpages$n" % (arts, ultima, trurl(ultima), 450000-arts)
					msg=msg.replace("$r",RED).replace("$B",BLACK).replace("$n",NORMAL).replace("$N",BOLD)
					c.privmsg(config.canales[0],msg)
					return
			else: return

		if not reImmunes.search(cloak):
			self.abuso.creakey(nick)
			self.abuso.limpiacaducados(nick)
			if not self.abuso.puedehablar(nick):
				print "%s está bloqueado" % (nick)
				return
		try:
			for bandejat in ignorats:
				if not boss and re.search("\?|\*",bandejat) and bandejat != "*":
					bandejat=bandejat.replace("?",".?").replace("*",".*")
					if re.search(r""+bandejat.lower(),nick.lower()):
						return
				elif not boss and bandejat.lower() == nick.lower():
					return
			if a[0]=='@' and len(a)>1:
				self.do_command(e, string.strip(a[1:]))
			else:
				enlaces=re.finditer(ur"(?<!!)(?:\[\[(.*?)(?:\]\]|\|)|(\{\{(?:subst:|raw:)?(?P<pl>.*?)(?:\|(?P<arg>.*?))?\}\}))",a)
				#if canal in ("#wikinews","#wikinews-en"): enlaces=[]
				tope=0
				for i in enlaces:
					argplant=False
					if i.group(2):
						if re.search(ur"\{\{\{|\}\}\}", i.group(2)):
							argplant=True
					#simulación de enlaces wiki, devuelve la url
					if i.group(1) and not argplant:
						if tope<3:
							c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/"+trurl(i.group(1)).encode('utf-8'))
							self.abuso.registracomando(nick,"enlace "+trurl(i.group(1)),2)
					#simulación de código para plantillas y 'transclusions'
					elif i.group(3) and not argplant:
						if tope<3:
							#convierte {{NAMESPACE:...}} en un enlace a la página indicada, no en un enlace a una página.
							if ":" in i.group('pl'):
								ns=i.group('pl').split(":")[0]
								if re.search(r"us(uario|er)|plantilla|template|mediawiki|categor(ia|ía|y)|imagen?|ayuda|help|wikipedia|project|portal|wikiproyecto|anexo", ns.lower()):
									pag=i.group('pl')
								else:
									pag="Template:"+i.group('pl')
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/"+trurl(pag).encode('utf-8'))
							#{{u|Xxxx}} equivale a [[Usuario:Xxxx]]
							elif i.group('pl')=="u":
								usr=i.group('arg')
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/User:"+trurl(usr).encode('utf-8'))
							#{{u|Xxxx}} equivale a [[Usuario Discusión:Xxxx]]
							elif i.group('pl')=="ud":
								usr=i.group('arg')
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/User_talk:"+trurl(usr).encode('utf-8'))
							#{{done}}
							elif i.group('pl')=="done":
								c.privmsg(canal, u"how efficient are you!".encode('utf-8'))
							#se supone que es una plantilla...
							else:
								c.privmsg(canal, u"http://"+config.idi+"."+wikipro[config.pro]+".org/wiki/Template:"+trurl(i.group('pl')).encode('utf-8'))
							self.abuso.registracomando(nick,"plantilla "+trurl(i.group('pl')),2)
					tope+=1
				if a=="mola":
					self.abuso.registracomando(nick,"mola",3)
					c.privmsg(canal, u"Ey tio")
				elif a.lower()=="ey tio" or a.lower()==u"ey tyo":
					self.abuso.registracomando(nick,"mola",3)
					c.privmsg(canal, "mola")
				elif a==u"melon":
					self.abuso.registracomando(nick,"melon",3)
					c.privmsg(canal, "XDDDDDD")
				elif a=="heh":
					self.abuso.registracomando(nick,"heh",3)
					if random.randint(1,2)==1:
						c.privmsg(canal, "lol")
					else:
						pass
				elif re.search("^(?:%s:)? *ping$" % self.nickname, a, re.I):
					self.abuso.registracomando(nick,"ping",3)
					c.privmsg(canal, "%s: PONG"%nick)
				elif re.search(ur"\W"+self.nickname+"\W", a, re.I):# and not boss:
					if boss:
						#para que algunos callen, y no quiero senyalar  a alhen -23-4-08-
						#time.sleep(random.randint(0,3))
						#boca.respuesta(boca.flatter,100,c,canal,(nick),))
						pass
					else:
						self.abuso.registracomando(nick,"orejotas",1)
						time.sleep(random.randint(0,6))
						#boca.respuesta(boca.reply,60,c,canal,(nm_to_n(e.source()),))
				elif re.search("^re(?:load|boot)!?$",a.lower()):
					if boss:
						self.die("Coming back soon, my friends :)")
					else:
						c.privmsg(canal, "... I'll think about it")

		except UnicodeEncodeError, ue:
			print ue

	def do_command(self, e, cmd, canal=0):
		global ops
		global mods
		global flags
		if canal==0:
			canal=	e.target()
		nick = nm_to_n(e.source())
		c = self.connection
		cloak= nm_to_h(e.source())
		boss = re.search(reAutoritzats,cloak.lower())
		isBotOp=False
		prefcloak=cloak.split("/")[0]
		if prefcloak in dBotOps:
			if cloak.split("/")[1].lower() in dBotOps[prefcloak]:
				isBotOp=True
		if not isBotOp and nick in ops:
			isBotOp=True
		ordre=cmd.split(" ")[0].lower()
		args=""
		if " " in cmd:
			args=cmd.split(" ",1)[1]

##Cosas del IRC
		if ordre == "disconnect":
			pass
		elif ordre == "die":
			self.abuso.registracomando(nick,"die",3)
			if boss:
				self.die("i'll be coming back soon...")
			dado=random.randint(1,3)
			if dado==1:
				c.privmsg(canal, "You die, disloyal!")
			elif dado==2:
				c.privmsg(canal, "Aggghhh i dieeeee")
				c.privmsg(canal, "Exception: self.die() Operation impossible to realize :Ã¾")
			elif dado==3:
				c.privmsg(canal, "Oh, yeah, I'm so scared... die you!")
		elif ordre == "stats":
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			self.abuso.registracomando(nick,"stats",9)
			page="Special:Statistics"
			code="es"
			if args:
				code=args
				if code[-1]==":":
					code=code[:-1]
			page=code+":"+page
			data=fetch(page)
			c.privmsg(canal, data)
		elif ordre == "ping":
			self.abuso.registracomando(nick,"ping",3)
			c.privmsg(canal, "%s: PONG"%nick)


##Cosas de la WIKIPEDIA
		elif ordre in ["ip", "whois"] and args:
			self.abuso.registracomando(nick,"whois",9)
			ip=re.search("^(\d{1,3}\.){3}\d{1,3}$",args)
			msg=u"not valid IP"
			if ip:
				#url="http://www.dnsstuff.com/tools/ipall.ch?domain="+args
				url="http://private.dnsstuff.com/tools/ipall.ch?domain=%s"%args
				try:
					txt=net.pageText(url)
					txt=txt.split("<pre>")[1].split("</pre>")[0]
					reverseDSN = re.search("Reverse DNS: +(.*)",txt)
					if reverseDSN:
						reverseDSN=reverseDSN.group(1)
					city = re.search("City \(per outside source\):\s+(.*)",txt)
					city=city.group(1) if city else "???"
					iprange = re.search("Country IP Range:\s+(.*) to (.*)",txt)
					iprange=[iprange.group(1), iprange.group(2)] if iprange else "???"
					country = re.search("Country \(per IP registrar\):\s+(.*)",txt)
					country=country.group(1) if country else "???"
					proxy = re.search("Known Proxy\?\s+(.*)",txt)
					proxy=proxy.group(1) if proxy else "???"
					proxyClr = ""
					if "No" in proxy: proxyClr = "$e"
					if "Yes" in proxy: proxyClr = "$r"
					proxy = proxyClr+proxy
					msg="reverseDSN: $l%s$N - range: $l%s$N / $l%s$N - city: $l%s$N - country: $l%s$N - known proxy: %s$N - $b%s$N" % (reverseDSN, iprange[0], iprange[1], city, country, proxy, url)
					msg=colors(msg)
					msg=msg.replace("\n","").replace("\r","")
					c.privmsg(canal, msg.encode("utf-8"))
				except:
					c.privmsg(canal, url.encode("utf-8"))
		elif ordre == "whois2":
			self.abuso.registracomando(nick,"whois",9)
			if re.search("^(?:\d{1,3}\.){3}\d{1,3}$",args):
				url = "http://toolserver.org/~chm/whois.php?ip="+args
				c.privmsg(canal, url)
		elif ordre == "info":
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			m=re.search(ur"(?us)info\s*(?:(?P<pro>wikispecies|commons|meta|w|b|q|n|s|v|wikt):)?(?:(?P<idi>\w{2,6}):)?(?P<user>.*)",cmd)
			#print "orejotas #617",m.groups()
			usr=""
			if m:
				usr = nick if not m.group('user') else m.group('user')
				silent = True if re.search(ur"Â·Â·|::", usr) else False
				usr = usr.replace(u"Â·Â·","")
				usr = usr.replace("::","")
				usr = nomVP(usr)
				usr0 = usr[0].upper()
				if len(usr) > 1: usr=usr0+usr[1:]
				if "|" in usr: usr=usr.split("|")[0]
				ap=net.ap(c,usr,l=m.group('idi'),p=m.group('pro'),flags=flags,ch=canal,q=silent)
				thread.start_new_thread(ap.start,())
				if 5 > int(time.strftime("%d")) > 0:
					c.privmsg(canal, "processing... this can take some minutes ;) ...")
			self.abuso.registracomando(nick,"info "+usr,5)
		elif ordre == "art":
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			w="en"
			b=p=""
			if args:
				b=args.replace(" ","")
				b=b.replace(":","")
				b=b.replace(".","")
				art(c,b).start()
				p=" "+b
			else:
				art(c,"en", canal).start()
			self.abuso.registracomando(nick,"art"+p,3)
		elif ordre == "size":
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			thread.start_new_thread(c.privmsg,(canal, tam(trurl(args).encode('utf-8'))))
			self.abuso.registracomando(nick,"size "+args,3)
		elif ordre == "fetch":
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			c.privmsg(canal, fetch(trurl(args)))
			self.abuso.registracomando(nick,"fetch "+args,6)
		elif re.search("^(?:wiki)?concurso$",ordre):
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			data = net.pageWiki("Wikipedia:Wikiconcurso")
			m=re.search("(?us)=== Edición en curso ===.*edición (\d*)\|.*=== Ediciones realizadas ===",data)
			if m:
				c.privmsg(canal, "http://en.wikinews.org/wiki/Wikipedia:Wikiconcurso/edici%C3%B3n_"+m.group(1))
			else:
				c.privmsg(canal, "http://en.wikinews.org/wiki/Wikipedia:Wikiconcurso")
			self.abuso.registracomando(nick,"wikiconcurso",5)
		elif ordre in ["b", "block","bloquea"] and args:
			self.abuso.registracomando(nick,"block",5)
			msg=u"http://en.wikinews.org/wiki/Special:Blockip/"+trurl(args)
			c.privmsg(canal, msg.encode("utf-8"))
		elif ordre in  ["cb", "bc"] and args:
			self.abuso.registracomando(nick,"block",5)
			msg=u"http://en.wikinews.org/wiki/Special:$sp$/%s"%trurl(args)
			msg=msg.encode("utf-8")
			for l in ordre:
				if l == "c":
					c.privmsg(canal, msg.replace("$sp$","Contributions"))
				else:
					c.privmsg(canal, msg.replace("$sp$","BlockIP"))
		elif re.search("^b(?:lock)?l(?:og)?$", ordre) and args:
			url="http://en.wikinews.org/w/api.php?action=query&list=blocks"
			if args:
				user=trurl(args)
				url+="&bkusers=%s" % user
			url+="&format=xmlfm"
			txt=net.pageText(url)

			logs=re.search('<span style="color:blue;">&lt;block id=&quot;(?P<id>\d*)&quot; (?:user=&quot;(?P<blocked>.*)&quot; )?' + \
					'by=&quot;(?P<sysop>.*)&quot; timestamp=&quot;(?P<since>.*)&quot; expiry=&quot;(?P<till>.*)&quot; ' + \
					'reason=&quot;(?P<reason>.*?)&quot; (?P<anononly>anononly=&quot;&quot; )?(?P<automatic>automatic=&quot;&quot; )?' + \
					'(?P<nocreate>nocreate=&quot;&quot; )?(?P<autoblock>autoblock=&quot;&quot; )?(?P<noemail>noemail=&quot;&quot; )?/&gt;</span>',txt)
			if logs:
				#print "  ::", logs.groups()
				id=logs.group('id')
				usr=logs.group('blocked')
				sysop=logs.group('sysop')
				ts=logs.group('since')
				exp=logs.group('till')
				expstr=exp
				ts=apiTime(ts)
				ts1=" (desde: %s) " % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts[0]))
				ts2=ts[1]
				exp1=exp2=tmst=""
				if exp!="infinity":
					exp=apiTime(exp)
					exp1=" (hasta: %s) " % time.strftime("%Y-%m-%d %H:%M: %S", time.localtime(exp[0]))
					exp2=exp[1]
					diff=relativedelta(exp2,ts2)
					diff={"years":diff.years, "months":diff.months, "days": diff.days, "hours": diff.hours, "minutes": diff.minutes, "seconds": diff.seconds}
					#print diff
					exp=[]
					for e in diff:
						if diff[e]>1:
							exp.append(str(diff[e])+" "+e)
						elif diff[e]==1:
							exp.append(str(diff[e])+" "+e[:-1])
					if len(exp)>1:
						expstr=", ".join(exp[:-1])
						expstr+=" y "+exp[-1]
					elif exp:
						expstr=exp[-1]
					else:
						expstr="<desconocido>"
					tmst=exp1
				elif exp=="infinity":
					expstr="indefinetely"
					tmst=ts1
				reason=logs.group('reason')
				anononly=logs.group('anononly')
				automatic=logs.group('automatic')
				nocreate=logs.group('nocreate')
				autoblock=logs.group('autoblock')
				noemail=logs.group('noemail')
				apiflags={"anon only.": anononly, "automatic":automatic,"no acc. create.":nocreate,"autoblock":autoblock,"no email":noemail}
				f=[]
				ftxt=" bloqueos: "
				for flag in apiflags:
					if apiflags[flag]:
						f.append(flag)
				if len(f)>1:
					ftxt+="%s." % ", ".join(f)
				elif f:
					ftxt+="%s." % f[0]
				txt="id: $%g#"+id+"$N $l"+sysop+"$N blocked $r"+usr+"$N during $o"+expstr+"$N"+tmst
				txt+="("+reason+")"
				txt=txt+ftxt
				txt=colors(txt.decode("utf-8"))
				c.privmsg(canal, txt.encode("utf-8"))
			c.privmsg(canal, "http://en.wikinews.org/wiki/Special:IPBlockList?ip="+user)
			self.abuso.registracomando(nick,"block",5)

##Utilidades
		elif re.search("^ran(?:dom)?$",ordre):
			self.abuso.registracomando(nick,cmd,19)
			if args:
				b=[]
				if ", " in args:
					b=args.split(", ")
				elif "," in args:
					b=args.split(",")
				if len(b)==2 and b[0].isdigit() and b[1].isdigit():
					#random numbers are generated by decimal number, obviously a @ran 0,1 always gets 1
					#add 1 always and later substract it
					b=[int(b[0])+1,int(b[1])+1]
					if b[0]>b[1]:
						b=[b[1],b[0]]
					b=random.randint(b[0],b[1])-1
					c.privmsg(canal,b)
				elif len(b)>1:
					tria=random.randint(1,len(b))-1
					c.privmsg(canal,b[tria].encode("utf-8"))
				else:
					c.privmsg(canal,"the number of options is insufficient.")

			else:
				b=random.randint(1,2)
				if b==1:
					b="nones"
				else:
					b="pares"
				c.privmsg(canal,b)

		elif ordre == "en-es":
			self.abuso.registracomando(nick,"enes "+args,4)
			#/usr/bin/sh ~/i2e-0.5.1/i2e-cli
			llamada="~/i2e-0.5.1/i2e.sh "+args.encode('latin-1')
			if isAlpha(args.encode('utf-8')):
				a=os.popen(llamada)
				quid=a.readlines()
				a.close()
				salida=""
				for i in quid[1:4]:
					c.privmsg(canal, i)
		elif ordre == "es-en":
			self.abuso.registracomando(nick,"esen "+args,4)
			llamada="~/i2e-0.5.1/i2e.sh -r "+args.encode('latin-1')
			if isAlpha(args.encode('utf-8')):
				a=os.popen(llamada)
				quid=a.readlines()
				a.close()
				salida=""
				for i in quid[1:9]:
					c.privmsg(canal, i)
		elif ordre in ["es-en","en-es"] and args:
			word=args
			number, result = dictorg(word,"*",ordre)
			msg=u"%i resultados. %s"%(number, result)
			c.privmsg(canal, msg.encode('utf-8'))
		##  enlaza a la EL
		elif ordre == "el":
			self.abuso.registracomando(nick,"sino "+args,3)
			c.privmsg(canal, "http://enciclopedia.us.es/index.php/"+urllib.quote(args.encode('utf-8')))
		elif ordre == "search-co":
			self.abuso.registracomando(nick,cmd,3)
			args=args.replace(" ","+")
			args=args.replace("\"","%22")
			c.privmsg(canal, "http://www.google.es/search?hl=en&q="+args.encode('utf-8')+"+site:commons.wikimedia.org")
		elif ordre == "search-me":
			self.abuso.registracomando(nick,cmd,3)
			args=args.replace(" ","+")
			args=args.replace("\"","%22")
			c.privmsg(canal, "http://www.google.com/search?hl=en&q="+args.encode('utf-8')+"+site:meta.wikimedia.org")
		elif ordre == "search-go":
			self.abuso.registracomando(nick,cmd,3)
			args=args.replace(" ","+")
			args=args.replace("\"","%22")
			c.privmsg(canal, "http://www.google.com/search?hl=en&q="+args.encode('utf-8'))
		elif ordre[0:6] == "search-":
			self.abuso.registracomando(nick,cmd,3)
			wiki=cmd[6:cmd.find(" ")]
			if wikimap.has_key(wiki):
				args=args.replace(" ","+")
				args=args.replace("\"","%22")
				c.privmsg(canal, "http://www.google.com/search?hl=en&q="+args.encode('utf-8')+"+site:"+wiki+".wikinews.org")
			if wikimap2.has_key(wiki):
				args=args.replace(" ","+")
				args=args.replace("\"","%22")
				c.privmsg(canal, "http://www.google.com/search?hl=en&q="+args.encode('utf-8')+"+site:"+wiki+".wikinews.org")
			else:
				c.privmsg(canal,"Lameruzooo, that wiki doesn't exists")
		elif ordre == "wikinews":
			self.abuso.registracomando(nick,cmd,3)
			if cmd == "wikinews":
				c.privmsg(canal, "Are you idiot or what? We are on this channel! .  --> http://www.wikinews.org/ <--")
			else:
				busqueda=args.replace("\"","%22")
				busqueda=urllib.quote(busqueda.encode("utf-8"))
				c.privmsg(canal, "http://www.google.com/search?hl=en&q="+busqueda+"+site:wikinews.org")
		elif ordre == "google":
			self.abuso.registracomando(nick,cmd,3)
			if cmd == "google":
				c.privmsg(canal, "http://www.google.com")
			else:
				busqueda=args.replace(" ","+")
				busqueda=busqueda.replace("\"","%22")
				c.privmsg(canal, "http://www.google.com/search?hl=en&q="+busqueda)
		elif ordre == "define":
			self.abuso.registracomando(nick,cmd,3)
			busqueda=args.replace(" ","+")
			busqueda=busqueda.replace("\"","%22")
			c.privmsg(canal, "http://www.google.com/search?hl=en&q=define:"+busqueda)
		elif ordre == "flickr":
			self.abuso.registracomando(nick,cmd,4)
			if cmd == "flickr":
				c.privmsg(canal, "http://www.flickr.com")
			else:
				busqueda=args.replace(" ","+")
				busqueda=busqueda.replace("\"","%22")
				c.privmsg(canal, "http://www.flickr.com/search/?q="+busqueda+"&l=commderiv")
		elif ordre == "youtube":
			self.abuso.registracomando(nick,cmd,4)
			if cmd == "youtube":
				c.privmsg(canal, "http://www.youtube.com")
			else:
				busqueda=args.replace(" ","+")
				busqueda=busqueda.replace("\"","%22")
				c.privmsg(canal, "http://youtube.com/results?search_query="+busqueda+"&search=Search")
		elif ordre == "wname" :
			self.abuso.registracomando(nick,cmd,3)
			code=args.replace(":","")
			if wikimap.has_key(code):
				c.privmsg(canal, "Language: %s" % unicode(wikimap[cmd[6:]]).encode('utf-8','replace'))
			if wikimap2.has_key(code):
				c.privmsg(canal, "Language: %s" % unicode(wikimap2[cmd[6:]]).encode('utf-8','replace'))
			else:
				c.privmsg(canal, u"That language doesn't exists.")
		elif ordre=="conv" and args:
			if " " in args:
				import numbers
				conv=args.split(" ",1)
				convtype=conv[0].upper()
				n=0
				if convtype in ["R", "D>R"]:
					n=numbers.dec2rom(conv[1])
				elif convtype in ["B", "D>B"]:
					n=numbers.dec2bin(conv[1])
				elif convtype=="R>D":
					n=numbers.rom2dec(conv[1])
				elif convtype=="B>D":
					n=numbers.bin2dec(conv[1])
				if n:
					c.privmsg(canal,n)


#JUGUETES
		elif ordre == "idiocy" or ordre == u"idiocies":
			self.abuso.registracomando(nick,"tonteria",10)
			llamada="cowthink -f sodomized "+args.encode('latin-1')
			if isAlpha(args.encode('utf-8')):
				a=os.popen(llamada)
				kaka=a.readlines()
				a.close()
				salida=""
				for i in kaka:
					c.privmsg(canal, i)
					time.sleep(2.0)
			#c.privmsg(self.channel, "You are a moron!!")
		elif ordre == "month":
			mesos={1:"january", 2:"february",3:"march",4:"april",5:"may",6:"june",7:"july",8:"august",9:"september",10:"october",11:"november",12:"december"}
			mes=int(time.strftime("%m",time.localtime(time.time()+3600*2)))
			mes=mesos[mes]
			c.privmsg(canal, mes)
		elif ordre == "wtf":
			self.abuso.registracomando(nick,"wtf "+args,4)
			if canal[0]!="#":
				c.privmsg(canal, "Command not available in private")
				return
			llamada="wtf "+args.encode('latin-1')
			if isAlpha(args.encode('utf-8')):
				a=os.popen(llamada)
				kaka=a.readlines()
				a.close()
				salida=""
				for i in kaka:
					c.privmsg(canal, i)
					time.sleep(1.0)
		elif ordre == "pi":
			self.abuso.registracomando(nick,"pi",3)
			c.privmsg(canal, "aprox: %s, see also: %s" % (math.pi, "http://www.piday.org/includes/pi_to_1million_digits_v2.html"))
		elif cmd.lower() == "e":
			self.abuso.registracomando(nick,"e",3)
			c.privmsg(canal, math.e)
#### AYUDA
		elif ordre == "help" or ordre == "ayuda":
			self.abuso.registracomando(nick,"help",3)
			c.privmsg(canal, "My manual: http://pitsilemu.wikia.com")
		elif ordre == "all":
			self.abuso.registracomando(nick,"all",4)
			cmds="Available functions: die, stats, ip, whois, whois2, info, size, fetch, block, cb, bc, random, en-es, es-en, el, search-co, search-me, search-go, search-xx, wikipedia, google, define, flickr, youtube, wname, conv, month, pi, help, all, _@, time, sug"
			if isBotOp:
				cmds+=", ign *, unign *, igns, addop *, removeop *"
			c.privmsg(canal, cmds)
			time.sleep(.5)
			cmds="new: @conv (D>R|D>B|R>D|B>D) *, @bl(ocklog) *"
			c.privmsg(canal, cmds)
		elif ordre =="_@":
			self.abuso.registracomando(nick,"@_@",3)
			c.privmsg(canal, "^_^")
		elif ordre == "time":
			self.abuso.registracomando(nick,"time",3)
			c.privmsg(canal, time.strftime("%d-%m-%y %H:%M:%S UTC"))
		elif ordre in ["sug", "sugus"]:
			self.abuso.registracomando(nick,"sug",3)
			if " " not in cmd or cmd == "sug ":
				c.privmsg(canal, "Use this command to suggest new functions, et cetera.")
				return
			sugerencia=cmd.split(" ",1)[1]
			#print "orejotas_vell {orejotas.bot.py} @sug #1067"
			try:
				file=config.sug
				print file
				sug=codecs.open(file, mode='a', errors='strict', encoding='utf-8',  buffering=1)
			except:
				print "Asegurese de incluir el nombre del fichero para sugerencias en el archivo config y que tiene permisos de escritura"
				return
			try:
				mytime=time.strftime("%d/%m/%y - %H:%M:%S",time.localtime(time.time()+3600*2))
				newline=u"\n\n=======================\nFecha: %s\nUsuario: %s\nSugerencia: %s" %(mytime, nick, sugerencia)
				sug.write(newline)
				sug.close()
				boca.respuesta(boca.sugerencias,100,c,canal)
			except:
				c.privmsg(canal, "suggestion not accepted")

#### TONTERIAS, Huevos de pascua
		elif ordre ==u"coffee" or cmd.lower()=="cafe":
			self.abuso.registracomando(nick,"cafe",4)
			boca.respuesta(boca.cafe,100,c,canal)
		elif ordre =="tobacco" :
			self.abuso.registracomando(nick,"tabaco",4)
			boca.respuesta(boca.tabaco,100,c,canal)
		elif ordre =="porro" :
			self.abuso.registracomando(nick,"porro",4)
			boca.respuesta(boca.porro,100,c,canal)
		elif ordre =="beer" or ordre =="duff" or ordre =="cerveza":
			self.abuso.registracomando(nick,"birra",4)
			boca.respuesta(boca.litrona,100,c,canal)
		elif ordre.startswith("beauty") :
			self.abuso.registracomando(nick,"guapo",4)
			boca.respuesta(boca.guapo,100,c,canal)
		elif ordre.startswith("sexy") :
			self.abuso.registracomando(nick,"sexy",4)
			boca.respuesta(boca.sexy,100,c,canal)
		elif ordre.startswith("intelligent") or ordre.startswith("intel"):
			self.abuso.registracomando(nick,"listo",4)
			boca.respuesta(boca.listo,100,c,canal)
		elif ordre.startswith("font"):
			self.abuso.registracomando(nick,"fuente",4)
			boca.respuesta(boca.fuentes,100,c,canal)
		elif ordre in ["selfabuse","check"]:
			if not boss or not re.search("^yrithinnd|^pas(?:qu|kw)al", nick, re.I): #canal.lower() not in ["yrithinnd","pasqual"]:
				return
			if canal != nick:
				canal=nick
			if not self.abuso.abuse:
				c.privmsg(canal,"no logs")
				return
			if not args:
				ab_items=str(len(self.abuso.abuse.keys()))
				c.privmsg(canal,"total number of logs: "+ab_items)
				abuses=self.abuso.abuse.keys()
				abuses.sort()
				for i in abuses:
					s=i+str(self.abuso.abuse[i])
					c.privmsg(canal,s)
					time.sleep(len(s)/20)
			else:
				el = args.replace("*",".*").replace("?",".?")
				el = "^(?:%s)$" % el
				i=0
				for itm in self.abuso.abuse.keys():
					if re.search(el, itm, re.I):
						i+=1
						s=itm+str(self.abuso.abuse[itm])
						c.privmsg(canal,s)
						time.sleep(len(s)/20)
				c.privmsg(canal,"Results: %i. @check end" % i)
		elif ordre == "bans" and boss:
				i=0
				for itm in self.abuso.abuse.keys():
					if not self.abuso.puedehablar(itm):
						i+=1
						s=itm + " is blocked"
						c.privmsg(canal,s)
						time.sleep(len(s)/20)
				if i:
					msg = "%i blocked." % i
				else:
					msg = "no bans"
				c.privmsg(canal,msg)
		elif ordre == "opmods":
			msg=""
			if "ChanServ" in ops:
				ops=ops.remove("ChanServ")
			if ops:
				msg+="ops: "

				if len(ops) > 1:
						for op in ops[:-1]:
							op=op[0]+u"Ã·"+op[1:]
							msg+= op+", "
						msg+= " y "+ops[-1]
				else:
					msg+= ops[-1]
			if mods:
				if ops:
					msg+="; "
				if len(mods) > 1:
						for mod in mods[:-1]:
							mod=mod[0]+u"Ã·"+mod[1:]
							msg+= mod+", "
						msg+= " y "+mods[-1]
				else:
					msg+= ops[-1]
			if msg:
				c.privmsg(canal, msg)
#
#		elif cmd[0:4].lower() == "test" :
#			c.privmsg(canal, "Ã±Ã±áéíóú")
#### XAT
		elif ordre == "flags":
			if not boss:
				self.abuso.registracomando(nick,"flags",9)
				c.privmsg(canal, "you don't have enough permissions")
				return
			if args:
				usr=""
				flag=""
				if ":" in args:
					usr=args.split(":",1)[0].lower()
					flag=args.split(":",1)[1]
				else:
					usr=args.lower()
				if usr and flag:
					if usr not in flags:
						flags[usr]=flag
						c.privmsg(canal, "accepted flags.")
					else:
						flags[usr]=flag
						c.privmsg(canal, "modified flags.")
					desaReg()
				elif usr and not flag:
					if usr in flags:
						del flags[usr]
						c.privmsg(canal, "deleted flags.")
						desaReg()
				else:
						c.privmsg(usuario, u"wrong parameters.")

		elif isBotOp and re.search(r"^(?:igns?|unign|addop|removeop|add|rem)",cmd):
			global ignorats
			if  ordre == "ign" and args:
				els=[]
				nousigns=[]
				if ", " in args:
					els=args.split(", ")
				else:
					els=[args]
				for el in els:
					if el.lower() == "MisterWiki":
						if cloak.lower() != "wikipedia/MisterWiki":
							el=nick
						else:
							c.privmsg(nick, "Heyo!")
							return
					if el not in ignorats and el != "*":
						ignorats.append(el)
						nousigns.append(el)
				desaReg()
				if len(nousigns)==1:
					els="the following nick"
				else:
					els="the following nicks"
				if nousigns:
					msg=u"has been added to the ignored list: %s"%(els,', '.join(nousigns))
					msg=msg.encode("utf-8")
					c.privmsg(nick, msg)
					time.sleep(len(msg)/10)
				else:
					igns=', '.join(ignorats).encode("utf-8")
					c.privmsg(nick, "the bot will ignore: %s"%igns)
			elif " " in cmd and ordre == "unign":
				el = cmd[cmd.find(" ")+1:]
				els=[]
				elim=[]
				if el=="*":
					ignorats=[]
					c.privmsg(nick, "log deleted")
				if ", " in el:
					els=el.split(", ")
				else:
					els=[el]
				for el in els:
					if re.search("\*|\?",el):
						el0=el.replace(".*","*").replace(".?","?").replace("*",".*").replace("?",".?")
						for el1 in ignorats:
							if re.search(r"("+el0+")",el1,re.I):
								el2=re.search(r"("+el0+")",el1,re.I).group(1)
								if el1.lower() == el2.lower():
									elim.append(el1)
					else:
						for el1 in ignorats:
							if el1.lower() == el.lower():
								elim.append(el1)
				for el in elim:
					ignorats.remove(el)
				if elim:
					msg="deleted things: %s"%(', '.join(elim))
					c.privmsg(nick, msg)
					time.sleep(len(msg)/10)
					c.privmsg(nick, "left: %s"%(', '.join(ignorats)))
					desaReg()
				else:
					c.privmsg(nick, "no coincidences found")
			elif ordre=="igns":
				if ignorats:
					users=', '.join(ignorats)
					c.privmsg(nick, users)
			elif ordre == "addop" and args:
				noucloak=args
				if noucloak.count("/")>1:
					c.privmsg(nick, "too many '/'!")
					return
				if "/" in noucloak:
					prefcloak=noucloak.split("/")[0]
					postcloak=noucloak.split("/")[1].lower()
					if dBotOps.has_key(prefcloak):
						if postcloak not in dBotOps[prefcloak]:
							dBotOps[prefcloak].append(postcloak)
						else:
							c.privmsg(nick, "there's already registered.")
							return
					else:
						dBotOps[prefcloak]=[postcloak]
					lBotOps.append(postcloak)
					#print dBotOps
					desaReg()
					c.privmsg(nick, "operator and cloak added!")
				else:
					c.privmsg(nick, "invalid entry: for \"nick!name@project/user\" type \"@addop project/user\"")
			elif " " in cmd and ordre == "removeop":
				vellcloak=args
				if vellcloak.count("/")>1:
					c.privmsg(nick, "demasiados '/'!")
					return
				if "/" in vellcloak:
					prefcloak=vellcloak.split("/")[0]
					postcloak=vellcloak.split("/")[1].lower()
					if postcloak=="pasqual" and "pasqual" not in cloak.lower():
						c.privmsg(nick, "o_o")
						return
					if dBotOps.has_key(prefcloak):
						if postcloak in dBotOps[prefcloak]:
							dBotOps[prefcloak].remove(postcloak)
							lBotOps.remove(postcloak)
							c.privmsg(nick, "operator and cloak deleted!")
							#print dBotOps
							desaReg()
						else:
							c.privmsg(nick, "no coincidences found")
					else:
						c.privmsg(nick, "no coincidences found")
				else:
					c.privmsg(nick, "not valid entry: for \"nick!name@project/user\" type \"@remove project/user\"")
			elif ordre == "add" and args and canal in self.chans[1:]:
				cloak=args
				cloak=cloak.replace("wp/","wikipedia/")
				cloak=cloak.replace("wm/","wikimedia/")
				cloak=cloak.replace("uf/","unaffiliated/")
				c.privmsg("ChanServ","OP %s %s"%(canal,self.nickname))
				time.sleep(1)
				c.mode(canal,"+I *!*@%s"%cloak)
				time.sleep(1)
				c.privmsg("ChanServ","OP %s -%s"%(canal,self.nickname))
			elif ordre == "rem" and args and canal in self.chans[1:]:
				cloak=args
				cloak=cloak.replace("wp/","wikipedia/")
				cloak=cloak.replace("wm/","wikimedia/")
				cloak=cloak.replace("uf/","unaffiliated/")
				c.privmsg("ChanServ","OP %s %s"%(canal,self.nickname))
				time.sleep(1)
				c.mode(canal,"-I *!*@%s"%cloak)
				time.sleep(1)
				c.privmsg("ChanServ","OP %s -%s"%(canal,self.nickname))

		elif ordre == "botops":
			msg=""
			if "ChanServ" in ops:
				ops=ops.remove("ChanServ")
			for cl in dBotOps:
				msg=cl+": "
				for usr in dBotOps[cl]:
					usr=usr[0]+u"Ã·"+usr[1:]
					msg+=usr+", "
				msg=msg[:-2]+"."
				c.privmsg(nick, msg.encode("utf-8","replace"))
				time.sleep(.5)
			msg=""
			if ops:
				msg+="ops: "
				if len(ops) > 1:
					msg+= ", ".join(ops[:-2])
					msg+= " y "+ops[-1]
				else:
					msg+= ops[-1]
			if mods:
				if msg:
					msg+="; "
				msg+="mods: "
				if len(ops) > 1:
					msg+= ", ".join(ops[:-2])
					msg+= " y "+ops[-1]
				else:
					msg+= ops[-1]
			if msg:
				c.privmsg(nick, msg.encode("utf-8","replace"))
		else:
			self.abuso.registracomando(nick,"#err",4)
			c.privmsg(canal, "o_O I don't understand. Try again.")

output_lock = threading.Lock()
input_lock = threading.Lock()
output_cache = []

def output(text):
    output_lock.acquire()
    try:
        if type(text) is not unicode:
            try:
                text = unicode(text, 'utf-8')
            except UnicodeDecodeError:
                text = unicode(text, 'iso8859-1')
        if input_lock.locked():
            cache_output(text, toStdout = False)
        else:
            ui.output(text, toStdout = False)
    finally:
        output_lock.release()

def cache_output(*args, **kwargs):
    output_cache.append((args, kwargs))



def main():
	import sys

	channel  = config.canales[0]
	nickname = config.nombre
	bot = TestBot(channel, nickname, "irc.freenode.net", 6667)
	bot.start()

if __name__ == "__main__":
	main()
