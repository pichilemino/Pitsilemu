# -*- coding: utf-8 -*-
import random,time

class Boca:
	def __init__(self):
		#self.saludo=[
		#	[('M',u"Welcome back %s",1,0)],
		#	[('M',u"Hey %s",1,0)],
		#	[('M',u"Hi %s",1,0)],
		#	[('M',u"Ohai",0,0)],
		#	[('M',u"Hallo ",0,0)],
		#	[('M',u"wop wop",0,0)],
		#	[('M',u"Wassap neeeeeeeeeeeeengg",0,0)],
		#	[('M',u"Hola %s",1,0)],
		#	[('M',u"Hi %s, what's up?",1,0)],
		#	[('M',u"Konnichiwa",0,0)],
		#	[('M',u"wazzaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaap",0,0)],
		#	[('M',u"salâm",0,0)],
		#]
		self.reply=[
			[('M',u"Never gonna give you up! Never gonna let you down!",0,0)],
			[('M',u"Yes, my love?",0,0)],
			[('M',u"You talking about me?",0,0)],
			[('M',u"Don't talk about me!",0,0)],
			[('M',u"Bah",0,0)],
			[('M',u"%s, why do you say that?",1,0)],
			[('M',u"%s, the last person that said that, is underground and is not a mole, or a miner, or is on the subway.",1,0)],
			[('M',u"Yes?",0,0)],
			[('M',u"Puff!",0,0)],
			[('M',u"pssssss",0,0)],
			[('M',u"heyo!",0,0)],
			[('M',u"Later I'll answer, I'm busy ATM",0,0)],
			[('M',u"%s, that' makes me exasperate! >:D",1,0)],
			[('M',u"mmmmm",0,0)],
			[('M',u"Do you think?",0,0)],
			[('M',u"a mo",0,0)],
			[('M',u"haha",0,0)],
			[('M',u":-D",0,0)],
			[('M',u":-(",0,0)],
			[('M',u"I'm Johnny Knoxville, welcome to Jackass",0,0)],
			[('M',u"¬¬'",0,0)],
			[('M',u"%s, shut up, please.",1,0)],
			[('M',u"%s, when the cows fly, let me know, please.",1,0)],
			[('M',u"¡¡¡%s!!! Clean your mouth before pronouncing my glorious name, insignificant mortal.",1,0)],
			[('M',u"wait a moment, I'm writing a stub about me :D",0,0)],
			[('M',u"You're not good, can't you see, Brother Louie Louie Louie!",0,0)],
			[('M',u"STOP! I'm playing Counter-Strike",0,0)],
			[('M',u"Ahhhh! %s came too late!",1,0)],
			[('M',u"I'm not listening to YOU!",0,0)],
			[('M',u"Wikipedia is vandalized, who will unvandalize it?, the person that unvandalize it, a good unvandalizer is. IN YOUR FACE!",0,0)],
			[('M',u"Lemme think about it.",0,0)],
			[('M',u":-O %s SHUT UP OR I WILL RICKROLL YOU!!!",1,0)],
			[('M',u"Shut up, or you will end just like MisterWiki, calling admins nazis...",0,0)],
			[('M',u"I don't know why I'm still here :p",0,0)],
			[
				('M',u"%s, Can I ask you something?",1,20),
				('M',u"Can I vandalize Wikipedia?",0,0)
			],
			[('A',u"is thinking how to kill the human race",0,0)],
			[('A',u"kicks %s",1,0)],
			[('N',u"ATENTION: Wikipedia in short will close his doors.",0,0)],
			[('N',u"WARNING: Talking with %s can be maddening.",1,0)],
			[('M',u"Yes, of course.",0,0)],
			[('M',u"Well, yes",0,0)],
			[('M',u"No.",0,0)],
			[('M',u"Why don't you go to kick dogs in the street and leave me alone?",0,0)],
			[('M',u"I'm noting certain ironic tone",0,0)],
			[('M',u"You make me doubt, %s",1,0)],
			[('M',u"%s What are you doing?",1,0)],
			[('M',u"%s, are you sure? ",1,0)],
			[('A',u"is falling in love",0,0)],
			[('M',u"I think I have broken something",0,0)],
			[('M',u"Ouch !",0,0)],
			[('M',u"D'oh !",0,0)],
			[('M',u"%s, if you don't bother, shut up!",1,0)],
			[('A',u"%s, I'm busy ATM",1,0)],
			[('M',u"Oh big yellow taxi, come take me home, my girl is waiting just for me, don't tell me a story!",0,0)],
			[('M',u"Depends.",0,0)],
			[('M',u"I just have to say one more thing, a big thing for Pitsilemu and the Artifficial Inteligence",0,0)],
			[('A',u"hates you",0,0)],
			[('A',u"yawns",0,0)],
			[('M',u"beep beep",0,0)],
		]
		self.flatter=[		
			[('M',u"Maybe",0,0)],
			[('M',u"Yes, sir.",0,0)],
			[('M',u"Whatever, sir",0,0)],
			[('M',u"Whatever The Sir says, goes to mass",0,0)],
			[('M',u":)",0,0)],
			[('M',u"Thanks forever",0,0)],
			[('M',u"His Excellency, in your voice, my name is as beautiful as your infinite kindness",0,0)],
			[('M',u"OK",0,0)],
			[('M',u"I'll never gonna give you up ;)",0,0)],
			[('M',u"Anytime.",0,0)],
			[('M',u"Sir.",0,0)],
			[('M',u"Sir, I love to hear my name from your mouth",0,0)],
			[('M',u":)",0,0)],
			[('M',u"Nobody is like my goodlooking and beloved MisterWiki",0,0)],
			[('M',u"I love you, Sir.",0,0)],
			[('M',u"Sorry sir, %s",1,0)],
			[('M',u"Oh, %s, evidently you'll have my support anywhere",1,0)],
			[('M',u"Sir, I love to hear my name from your mouth",1,0)],
			[('M',u"%s, anytime.",1,0)],
			[('M',u"MisterWiki is a sucker, OPs please kick him from this channel!!! >:D",0,0)],
			[
				('M',u"how powerful is the voice of my Sir",0,20),
				('M',u"just one thing: shut up moron :P",0,0),
			],
			[('M',u"%s, I can't help you now, please catch me later",0,0)],
			[('M',u"What does he wants now!",0,0)],
		]
		self.art_error=[		
			[('M',u"Never gonna give you up!",0,0)],
			[('M',u"I will not let you down.",0,0)],
			[('M',u"Look it by yourself, you don't hate it?...",0,0)],
			[('M',u"Hey!! I'm stressed",0,0)],
			[('M',u"La cagaste, conchetumare >:D",0,0)],
			[('M',u"Qui pa' loco chuchetumare!",0,0)],
			[('M',u"Cabeza de resbalin conchetumare",0,0)],
			[('M',u"Do you think I'm your slave?",0,0)],
			[('M',u"Hey!! i'm not jefry mammmmmonaas@",0,0)],
			[('M',u"I think that the Spanish Wikipedia is the worst Wikipedia ever.",0,0)],
			[('M',u"Oops, I can't help you",0,0)],
			[('M',u"There's something going wrong.",0,0)],
		]
		self.sugerencias=[
			[('M',u"Suggestion ignored successfully",0,0)],
			[('M',u"Idiocy archived at /dev/null",0,0)],
			[('M',u"Omai!",0,0)],
			[('M',u"I just called... to say... that your suggestion sucks.",0,0)],
			[('M',u"You can win if you want, if you want it you will win!",0,0)],
			[('A',u"Error 404: File Not Found. Your suggestion was not saved. Sorry ;-) (j/k)",0,0)],
			[('M',u"Be a man!",0,0)],
			[('A',u"suggest you to write your suggestion in a paper, because he'll later smoke it.",0,0)],
			[('A',u'pisses your suggestion',0,0)],
		]
		self.fuentes=[
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/e/eb/Vilaflorbrunnen2.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/3/3e/View_of_Paseo_del_Pr%C3%ADncipe_de_Vergara_%28El_Espol%C3%B3n%29_in_Logro%C3%B1o.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/e/e7/Spain.Santiago.de.Compostela.Plaza.Toural.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/e/e6/Spain.Barcelona.Plaza.Catalunya.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/1/1b/Santiago_Alameda_Fonte_Ferradura_GDFL.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/e/e9/Plaza-de-cibeles.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/2/22/Priego.JPG",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/a/ae/Padr%C3%B3n_Galicia_Xullo_2006_05.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/7/71/Murrieta_Fountain_in_Logro%C3%B1o.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/d/d4/Madrid_18.JPG",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/c/c5/Granada_plaza_isabel_la_catolica.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/4/4d/Fuente_de_las_Batallas.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/4/4c/Fuente_de_H%C3%A9rcules.JPG",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/a/a0/Grenada1.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/c/c0/Bratislava_Presidents_Garden.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/d/d8/BuckinghamFountainCloseUp.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/b/b5/Belarus-Minsk-Kupalinki_Sculpture-1.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/6/60/Fountain_sergels_torg_stockholm_sweden_20040506.jpg",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/4/4b/Grifo_m%C3%A1gico.JPG",0,0)],
			[('M',u"http://upload.wikimedia.org/wikipedia/commons/4/44/Miko%C5%82%C3%B3w_-_Fontanna_na_rynku1.jpg",0,0)],
		]
		self.cafe=[
			[('M',u"No thanks",0,0)],
			[('M',u"A milk, please!",0,0)],
			[('M',u"Yes, please",0,0)],
		]
		self.tabaco=[
			[('M',u"No thanks, I don't smoke",0,0)],
			[('M',u"It's a bad day to stop smoking",0,0)],
			[('M',u"Gimme 2",0,0)],
			[('M',u"Venga!",0,0)],
		]
		self.porro=[
			[('M',u"I don't want to say that.",0,0)],
			[('M',u"Stop!",0,0)],
			[('A',u"imposses this song: Rick Astley - Never Gonna Give You Up",0,0)],
			[('M',u"Uff, I'm too lazy >:D",0,0)],
		]
		self.litrona=[
			[('M',u"No.",0,0)],
			[('M',u"Don't tell me are you blind to see?",0,0)],
			[('M',u"We're no strangers to love!",0,0)],
			[('M',u"I will oxidize if I don't take some beer",0,0)],
			[('M',u"Take it.",0,0)],
		]
		self.guapo=[
			[('M',u"thanks",0,0)],
			[('M',u"i'm beautiful",0,0)],
			[('M',u"more than you, i know",0,0)],
		]
		self.sexy=[
			[('M',u"thanks",0,0)],
			[('M',u"^_^",0,0)],
			[('M',u"oh yeah baby !",0,0)],
		]
		self.listo=[
			[('M',u"you don't",0,0)],
			[('M',u"yo yo",0,0)],
			[('M',u"thanks",0,0)],
			[('A',u"reverences you",0,0)],
		]
		
	def respuesta(self,frases, prob, con, canal, param=(1,2,3,4,5)):
		"""
		Elige una frase de las que le pasemos y la dice con probabilidad que le digamos, las frases permiten respuestas dirigidas.
		TODO: Que funcione con múltiples parámetros
		"""
		dado=random.randint(0,100)
		if dado>prob:
			return "" #No devuelvo None para evitar que aparezca "None" en el canal
		dado=random.randint(0,len(frases)-1)
		for i in frases[dado]:
			if i[2]==0: #La frase no tiene parámetros
				if i[0]=='M': #Mensaje
					#con.send_raw("PRIVMSG %s :%s" % (config.canal,i[1]))
					con.privmsg(canal,i[1].encode('utf-8'))
				elif i[0]=='A': #Action (/me(
					#con.send_raw("PRIVMSG %s :\001ACTION %s\001" % (config.canal,i[1]))
					con.action(canal,i[1].encode('utf-8'))
				elif i[0]=='N': #Notice
					#con.send_raw("NOTICE %s :%s" % (config.canal,i[1]))
					con.notice(canal,i[1].encode('utf-8'))
			else:
				if i[0]=='M': #Mensaje
					con.privmsg(canal,(i[1] % param).encode('utf-8'))
				elif i[0]=='A': #Action (/me)
					con.action(canal,(i[1] % param).encode('utf-8'))
				elif i[0]=='N': #Notice
					con.notice(canal,(i[1] % param).encode('utf-8'))
			time.sleep(i[3])


#Creo una instancia de los métodos públicos para que puedan ser llamados sin necesidad de instanciar la clase. 
_inst = Boca()
respuesta = _inst.respuesta
# Variables
#saludo = _inst.saludo
reply = _inst.reply
art_error = _inst.art_error
fuentes = _inst.fuentes
cafe = _inst.cafe
tabaco = _inst.tabaco
porro = _inst.porro
litrona = _inst.litrona
guapo = _inst.guapo
sexy = _inst.sexy
listo = _inst.listo
flatter = _inst.flatter
sugerencias = _inst.sugerencias

if __name__ == '__main__':
    print "Clase "+__name__