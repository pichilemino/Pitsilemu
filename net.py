# -*- coding: utf-8 -*-

import urllib,urllib2,httplib,re,threading,time,string
import config
from orewikipedia import *
from datetime import datetime
from relativedelta import *

#__all__ = ["pageText","pageTextPost","pageWiki"]

class Net:	
	def __init__(self):
		#self.user_agent=u'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7'
		self.user_agent=u'PyBot 0.1 misterwiki@hotmail.com'
		self.cache_control=u'no-cache'
		self.pragma=u'no-cache'
		self.accept_charset='utf-8'
	
	def pageTextPost(self,url,postinfo,user_agent=None,nocache=False,encoding=None):
		m=re.search(ur'http://(.*?)(/.*)',url)
		if m==None:
			return
		else:
			domain=m.group(1)
			path=m.group(2)
		h = httplib.HTTP(domain)
		h.putrequest('POST', path)
		h.putheader('Host', domain)
		if user_agent==None:
			h.putheader('User-Agent', self.user_agent)
		if nocache:
			h.putheader('Cache-Control',self.cache_control)
			h.putheader('Pragma',self.pragma)
		if encoding==None:
			h.putheader('Accept-Charset',self.accept_charset)
		h.putheader('Content-Type', 'application/x-www-form-urlencoded')
		h.putheader('Content-Length', str(len(postinfo)))
		h.endheaders()
		h.send(postinfo)
		errcode, errmsg, headers = h.getreply()
		data = h.getfile().read() # Obtener el HTML en bruto
		return data
		
	def pageText(self,url,user_agent=None,nocache=False,encoding=None):
		"""
		TODO: Arreglar 404 (y demás errores)  urllib2.HTTPError: HTTP Error 404: Not Found
		""" 
		try:
			request=urllib2.Request(url)
			if user_agent==None:
				request.add_header('User-Agent', self.user_agent)
			if nocache:
				request.add_header('Cache-Control',self.cache_control)
				request.add_header('Pragma',self.pragma)
			if encoding==None:
				coding=self.accept_charset
			else:
				coding=encoding
			request.add_header('Accept-Charset',coding)
			response=urllib2.urlopen(request)
			text=response.read()
			response.close()
			return text
		except:
			return ""
		
	def pageWiki(self,wikilink):
		"""
		Casos
		*enlace
		*proyecto:enlace
		*proyecto:idioma:enlace
		*proyecto:otro:enlace
		*idioma:enlace
		*otro:enlace
		"""
		m=re.search(ur"(.*?):(.*)",wikilink) #Determinamos si no es un enlace al proyecto principal
		if m==None:
			url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[config.pro],wikilink)
		else:
			if wikipro.has_key(m.group(1)): # Nos indican el proyecto en el wikienlace
				if specialwikipro.has_key(wikipro[m.group(1)]): #Si es un proyecto especial
					url='http://%s/w/index.php?title=%s&action=raw' % (specialwikipro[wikipro[m.group(1)]],m.group(2))
				else: #Es un proyecto con internacionalizacion
					m2=re.search(ur"(.*?):(.*)",m.group(2)) #Determinamos el idioma
					if m2==None: #No hay más :, corresponde al idioma por defecto
						url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[m.group(1)],m.group(2))
					else: #Veamos si es un idioma válido
						if wikimap.has_key(m2.group(1)): #Idioma válido
							url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (m2.group(1),wikipro[m.group(1)],m2.group(2))
						else: #No es un idioma válido, será otra cosa
							url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[m.group(1)],m2.group(1)+":"+m2.group(2))
			elif wikimap.has_key(m.group(1)): #No es un ningún wikiproyecto, detectemos si corresponde a algun idioma del proyecto por defecto
				url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (m.group(1),wikipro[config.pro],m.group(2))
			else: #No corresponde a ningún otro dioma
				url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[config.pro],m.group(1)+":"+m.group(2))
		#print url
		return self.pageText(url,nocache=True)
			
	def pageURL(self,wikilink):
		"""
		Casos
		*enlace
		*proyecto:enlace
		*proyecto:idioma:enlace
		*proyecto:otro:enlace
		*idioma:enlace
		*otro:enlace
		"""
		m=re.search(ur"(.*?):(.*)",wikilink) #Determinamos si no es un enlace al proyecto principal
		if m==None:
			url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[config.pro],wikilink)
		else:
			if wikipro.has_key(m.group(1)): # Nos indican el proyecto en el wikienlace
				if specialwikipro.has_key(wikipro[m.group(1)]): #Si es un proyecto especial
					url='http://%s/w/index.php?title=%s&action=raw' % (specialwikipro[wikipro[m.group(1)]],m.group(2))
				else: #Es un proyecto con internacionalizacion
					m2=re.search(ur"(.*?):(.*)",m.group(2)) #Determinamos el idioma
					if m2==None: #No hay más :, corresponde al idioma por defecto
						url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[m.group(1)],m.group(2))
					else: #Veamos si es un idioma válido
						if wikimap.has_key(m2.group(1)): #Idioma válido
							url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (m2.group(1),wikipro[m.group(1)],m2.group(2))
						else: #No es un idioma válido, será otra cosa
							url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[m.group(1)],m2.group(1)+":"+m2.group(2))
			elif wikimap.has_key(m.group(1)): #No es un ningún wikiproyecto, detectemos si corresponde a algun idioma del proyecto por defecto
				url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (m.group(1),wikipro[config.pro],m.group(2))
			else: #No corresponde a ningún otro dioma
				url='http://%s.%s.org/w/index.php?title=%s&action=raw' % (config.idi,wikipro[config.pro],m.group(1)+":"+m.group(2))
		url=url.replace("w/index.php?title=","wiki/")
		url=url.replace("&action=raw","")
		return url

#Creo una instancia de los métodos públicos para que puedan ser llamados sin necesidad de instanciar la clase. 
_inst = Net()
pageTextPost = _inst.pageTextPost
pageText = _inst.pageText
pageWiki = _inst.pageWiki
pageURL = _inst.pageURL

def api_size(url=""): #in contruction (28-07-08)
    #print url
    if not url:
       return ""
    url="http://%s.wikinews.org/w/api.php?action=query&prop=info&titles=%s" % (lang,titles)
    content=pageText(url)
    content=content.decode("utf-8","replace")
    try:
        c=content.split('length=&quot;')[1].split('&quot;')[0]
    except IndexError:
        c=""
    except:
        c=content

    return c

def whowhere(nick,args):
	site=user=""
	if ":" in args:
		params=args.split(":")
		if args.count(":")==2:
			if wikimap.has_key(params[0]) and wikipro.has_key(params[1].lower()):
				site= u"%s.%s.org" % (params[0], wikipro[params[1]].lower())
			elif wikimap.has_key(params[1]) and wikipro.has_key(params[0].lower()):
				site= u"%s.%s.org" % (params[1], wikipro[params[0]])
			user = params[2]
		elif args.count(":")==1:
			if wikimap.has_key(params[0]):
				site= u"%s.wikinews.org" % (params[0])
			elif wikipro.has_key(params[0]) and not specialwikipro.has_key(wikipro[params[0].lower()]):
				site=u"es.%s.org" % wikipro[params[0]]
			elif wikipro.has_key(params[0]) and specialwikipro.has_key(wikipro[params[0].lower()]):
				site= specialwikipro[wikipro[params[0]]]
			user=params[1]						
	else:
		user=args.split("|")[0]
	if not user:
		user=nick.split("|")[0]
	if not site:
		site="%s.%s.org" % (config.idi, wikipro[config.pro])
	#print site, user
	return user, site

class ap( threading.Thread ):

 def __init__ ( self, c, u, l, p, flags="", ch=config.canales[0], q=False):
	self.conexion=c
	self.user=u
	self.lang=l
	self.proj=p
	self.flags=flags
	self.chan=ch
	self.quiet=q
	if l==None:
		self.lang=config.idi
	if p==None:
		self.proj=config.pro
	threading.Thread.__init__ ( self )

 def run ( self ):
	self.aportaciones()


 def aportaciones(self):
	if self.proj=="commons":
		dbname="commonswiki_p"
	elif self.proj=="meta":
		dbname="metawiki_p"
	elif wikipro[self.proj]=="wikipedia":
		dbname=self.lang+"wiki_p"
	elif wikipro[self.proj]=="wikibooks":
		dbname=self.lang+"wikibooks_p"
	elif wikipro[self.proj]=="wikiquote":
		dbname=self.lang+"wikiquote_p"
	elif wikipro[self.proj]=="wikinews":
		dbname=self.lang+"wikinews_p"
	elif wikipro[self.proj]=="wikisource":
		dbname=self.lang+"wikisource_p"
	elif wikipro[self.proj]=="wikiversity":
		dbname=self.lang+"wikiversity_p"
	elif wikipro[self.proj]=="wiktionary":
		dbname=self.lang+"wiktionary_p"
	else:
		#print "[net.py #222] Proyecto erroneo"
		return

	user=self.user
	user=urllib.quote(user.encode('utf-8','replace'))

	t=pageText('http://tools.wikimedia.de/~interiot/cgi-bin/count_edits?user='+user+'&dbname='+dbname)
	#t=pageText('http://tools.wikimedia.de/~kate/cgi-bin/count_edits?user='+urllib.quote(self.user.encode('utf-8'))+'&dbname='+dbname)
	general=ur"(?us)Username</th><td colspan='2'>(?P<user>.*?)<.*?Total edits</th><td colspan='2'>(?P<total>.*?)<.*?User groups</a><td colspan=2>(?P<flags>.*?)\s*<.*?Image uploads</th><td colspan='2'>(?P<images>.*?) \(.*?Distinct pages edited</th><td colspan='2'>(?P<distinct>.*?)<.*?Deleted edits</th><td colspan='2'>(?P<delete1>.*?)\s*<.*?First edit</th><td colspan='2'>(?P<first>.*?)<.*?"
	namespaces=ur"(?us)<tr class='nsn'><td class='nsname'><.*?class='nedits'.*?namespace=(?P<ns>\d*).*?>(?P<cuantas>\d*)<"
	logging=ur"(?us)<tr class='nsn'><td class='nsname'><.*?(?P<action>Delete|Restore|Block|Unblock|Protect|Unprotect|Move)</a></td><td class='nedits'><a.*?>(?P<cuantas>\d*)</a>"
	mg=re.search(general,t)
	mn=re.findall(namespaces,t)
	ml=re.findall(logging,t)
	apor = u""
	nick = u"%s:%s:User:%s" % (str(self.proj),str(self.lang),self.user) if not self.quiet else "the user"
	if mg:
		#apor=u"%s:%s:User:%s has made " % (str(self.proj),str(self.lang),str(urllib.quote(self.user.encode('utf-8'))))
		apor=u"%s has made " % nick
		apor+=u"%s edits. " % (mg.group('total'))
		apor+=u"%s in different pages. " % (mg.group('distinct'))
		for i in mn:
			if int(i[0])==0:
				apor+=u"%s in articles. " % (str(i[1]))
				break
		mf=re.search(ur"(?P<ano>\d{4})/(?P<mes>\d{2})/(?P<dia>\d{2}) (?P<hora>\d{2}):(?P<min>\d{2}):(?P<sec>\d{2})", mg.group('first'))
		if mf:
			firstedit_date=datetime(int(mf.group("ano")),int(mf.group("mes")),int(mf.group("dia")),int(mf.group("hora")),int(mf.group("min")),int(mf.group("sec")))
			diff = relativedelta(datetime.now(),firstedit_date)
			diff={u"years": diff.years, "months": diff.months, u"days": diff.days}
			sq=[]
			sorted=[u"years","months",u"days"]
			for txt in sorted:
				if diff[txt] > 1:
					sq.append("%d %s" % (diff[txt], txt))
				elif diff[txt] == 1:
					sing={u"years": u"year", "months": "month", u"days": u"day"}
					sq.append("%d %s" % (diff[txt], sing[txt]))
			if len(sq)>1:
				txt=", ".join(sq[:-1])
				txt+=" and %s" % sq[-1]
				apor+=txt
			elif sq:
				apor+=sq[0]
			apor+=u" old (%s/%s/%s %s:%s:%s). " % (mf.group("dia"),mf.group("mes"), mf.group("ano"), mf.group("hora"),mf.group("min"),mf.group("sec"))
		if int(mg.group('images'))>0:
			apor+=u"%s uploaded images. " % (mg.group('images'))
		if mg.group('flags'):
			if user.lower() in self.flags:
				flags=self.flags[user.lower()]
			else:
				flags=mg.group('flags')
			apor+=u"Flags: %s. " % flags
		apor+=u"%s deleted contributions. " % (mg.group('delete1'))
		for i in ml:
			if i[0]=='Delete':
				apor+=u"%s deletions. " % (str(i[1]))
				break
	else:
		pass #print "No"


	if not self.quiet: 
		if specialwikipro.has_key(wikipro[self.proj]): #Si es un proyecto especial
			apor+=u"\u000315".encode('utf-8')+"(http://"+specialwikipro[wikipro[self.proj]]
		else:
			apor+=u"\u000315".encode('utf-8')+"(http://"+str(self.lang)+"."+wikipro[self.proj]+".org"
		
		apor+=u"/wiki/Special:Contributions/"+user+")"
	self.conexion.privmsg(self.chan,apor.encode('utf-8'))

def estatVP(user,lang,family):
	months={#ca!
		"gen":1, "feb":2, "febr":2, "març":3, "abr": 4, "maig": 5, "juny": 6, "jul": 7, "ag":8, "ago": 8, "set": 9, "oct": 10, "nov":11, "des": 12
    	}
	def conv(n):
		n=str(n)
		if len(n)==1:
			n="0"+n
		return n

	text=pageText("http://%s.%s.org/w/index.php?title=Especial:Contributions&limit=20&target=%s&limit=10&uselang=ca"%(lang,family,user))
	text=text.split('<!-- start content -->')[1].split('<!-- end content -->')[0]
	text=text.decode('utf-8','replace')
	last=re.search(ur'\<ul>\s*<li>(?P<hour>..):(?P<min>..), (?P<day>..?) (?P<month>.*?) (?P<year>....).*?</li>',text)
	if last:
		hour_ts=str(last.group('hour'))
		min_ts=str(last.group('min'))
		day_ts=conv(last.group('day'))
		month_ts=str(last.group('month'))
		if not month_ts.isdigit():
			month_ts=conv(months[last.group('month')])
		year_ts=str(last.group('year'))
		last_edit=time.mktime((int(year_ts),int(month_ts),int(day_ts),int(hour_ts),int(min_ts),0,0,0,0))
		return last_edit
	else:
		return -1

if __name__ == '__main__':
    print "cuac"


