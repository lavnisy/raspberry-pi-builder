import pygame as pg

from random import choice
#build a raspberry pi!🍓

pg.init()

width = 1300
height = 1000
screen = pg.display.set_mode((width, height))

#posição dos componentes 
p_cpu = (471,298)
t_cpu = (130,100)
p_ram =  (598,298)
t_ram = (100,100)
p_fonte = (353,495)
t_fonte = (80,43)
p_usb2 =  (850,445)
t_usb2 = (150,85)
p_usb3 = (847,338)
t_usb3 = (150,85)
p_audio = (690,450)
t_audio = (70,100)
p_ethernet = (823,218)
t_ethernet = (170,100)
p_w_b = (350,244)
t_w_b = (93,85)

#imagens e áudios
bg = load("img", False, "media/bg.png", width, height)

tittle = load("img", False, "media/text.png", 600,190)

board_img = load("img",False, "media/board.png", 800,600)

join_audio = pg.mixer.Sound("media/put.mp3")

join_audio.set_volume(1.0)

isso_bb = pg.mixer.Sound("media/eita bb (1).mp3")

nao_bb = pg.mixer.Sound("media/aí não bb.mp3")

nao_bb.set_volume(1.0)

isso_bb.set_volume(1.0)

aê = pg.mixer.Sound("media/aplausos.mp3")

aê.set_volume(0.7)

components_img = {"cpu" : load("img", False, "media/cpu.png", 130, 100), 
"ram" : load("img", False, "media/ram.png", 100,100), 
"fonte" : load("img", False, "media/fonte.png", 80,43), 
"usb2" : load("img", False, "media/usb2.png", 150,85), 
"usb3" : load("img", False, "media/usb3.png", 150,85), 
"w&b" : load("img", False, "media/wifi&blue.png", 93,85), 
"audio" : load("img", False, "media/audio.png", 70,100), 
"ethernet" : load("img", False, "media/ethernet.png", 170,100)
}

#contador
ok = 0

#função para carregar imagens e áudios.

def load(type,sound,img,width, height):

	if type == "sound":
		s = pg.mixer.Sound(sound)

		return s

		

	elif type == "img":

		i = pg.image.load(img)

		i = pg.transform.scale(i,(width,height))

		return i		

		
#classes
class Board(pg.sprite.Sprite):
	
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		self.image = board_img
		self.rect = self.image.get_rect()
		self.rect[0] = width / 2 - 400
		self.rect[1] = 80

#classe que irá dar vida aos objetos componentes 
class Components(pg.sprite.Sprite):
	
	#argumentos imagem, esquerda, direita, tamanho do rect que vai ser utilizado para definir o local do componente e a sua posição. 
	def __init__(self, img, left,top,rw_rh, rl_rr):
		
		pg.sprite.Sprite.__init__(self)
		self.myplace = pg.Rect(rl_rr,(rw_rh[0] / 2,rw_rh[1] / 2)) 
		self.myplace.top += 20
		self.myplace.left += 30
		self.pos = rl_rr
		self.image = img
		self.rect = self.image.get_rect()
		self.rect[0] = left
		self.rect[1] = top
		self.touched = False
		self.rect[2], self.rect[3] = rw_rh
		self.joined = False
		self.mouse = 0
		self.state = [1,2,3]
		self.state[0] = "parado"
		
	def update(self):
		if self.touched and self.joined == False:
			#se o touched for verdadeiro o obj vai se mover de acordo com o movimento do cursor do mouse/dedo
			self.rect.move_ip(pg.mouse.get_rel()) 
			self.state[0] = "em movimento"
	
	#testa se a posição do cursor e a do objeto estão se colidindo		
	def touch(self, mouse):
		self.mouse = mouse
		if self.rect.collidepoint(mouse.pos):
			self.touched = True
		

	#testa se o componente está na sua posição de origem e o fixa		
	def join(self, effect):
		if self.state[0] == "em movimento":
			self.state[1] = "solto"
			
		my_audio_choice = (isso_bb, effect)
		my_audio_choice = choice(my_audio_choice)
		
		if self.rect.colliderect(self.myplace) and self.joined == False:
			self.state[1] = "no lugar de origem"
			my_audio_choice.play()
			self.rect[0], self.rect[1] = self.pos
			self.joined = True
					
		if self.state[1] == "solto" and self.joined == False:
			nao_bb.play()
			self.state = [1,2,3]
			
	def notjoin(self):
		pass


		




#criando os objetos

MotherBoard = Board()

cpu = Components(components_img["cpu"], 1050,400, t_cpu, p_cpu)

ram = Components(components_img["ram"], 10,500, t_ram, p_ram)

fonte = Components(components_img["fonte"], 100,300,(t_fonte[0] + 30,t_fonte[1] + 10), p_fonte)

usb2 = Components(components_img["usb2"], 100,100, t_usb2, p_usb2)

usb3 = Components(components_img["usb3"], 1100,200, t_usb3, p_usb3)

w_b = Components(components_img["w&b"], 750,600, t_w_b, p_w_b)

audio = Components(components_img["audio"], 1150,600, t_audio, p_audio)

ethernet = Components(components_img["ethernet"], 380,590, t_ethernet, p_ethernet)

#grupo de sprites
group = pg.sprite.Group()
group.add(MotherBoard, cpu, ram, fonte, usb2, usb3, w_b, ethernet, audio)	

#for tests
myfont = pg.font.SysFont("Arial", 34)
blit = False
label = myfont.render(f"{cpu.rect.colliderect(cpu.myplace)} ", 1, (0,0,0))
while True:

	for ev in pg.event.get():
		if ev.type == quit:
			pg.quit()
			
		elif ev.type == pg.MOUSEBUTTONDOWN:
		
			cpu.touch(ev)
			ram.touch(ev)
			fonte.touch(ev)
			usb2.touch(ev)
			usb3.touch(ev)
			w_b.touch(ev)
			audio.touch(ev)
			ethernet.touch(ev)
			
		elif ev.type == pg.MOUSEBUTTONUP:
			
			cpu.touched = False
			ram.touched = False
			fonte.touched = False
			usb2.touched = False
			usb3.touched = False
			w_b.touched = False
			audio.touched = False
			ethernet.touched = False
			cpu.join(isso_bb)
			cpu.notjoin()
			ram.join(join_audio)
			ram.notjoin()
			fonte.join(isso_bb)
			usb2.join(join_audio)
			usb3.join(join_audio)
			w_b.join(join_audio)
			audio.join(join_audio)
			ethernet.join(join_audio)
			
			blit == True
	
	#se todas as peças estiverem no seu devido local e o contador ser menor que 1 o áudio de aplausos será ativado e o cont irá receber +1.		
	if cpu.joined and ram.joined and usb2.joined and usb3.joined and fonte.joined and ethernet.joined and audio. joined and w_b.joined and ok < 1:
		aê.play()
		ok+= 1
							
	screen.blit(bg, (0,0))
	screen.blit(tittle,(320,0))
		
	group.draw(screen)
	
	cpu.update()
	ram.update()
	fonte.update()
	usb2.update()
	usb3.update()
	w_b.update()
	audio.update()
	ethernet.update()
	pg.display.update()

