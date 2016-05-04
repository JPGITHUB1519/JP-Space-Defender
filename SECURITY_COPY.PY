import pygame
import random
import time

# it going to inherit from sprite

class Player(pygame.sprite.Sprite) :

	#constructor
	def __init__ (self, imagen) :

		self.imagen = imagen
		self.rect = self.imagen.get_rect()
		self.rect.left = 300
		self.rect.top = 200

	def mover(self, vx, vy) :

		self.rect.move_ip(vx,vy)
		

	# it going to draw in a surface the player
	def update(self, superficie) :

		superficie.blit(self.imagen, self.rect)

class Recs(object) :

	def __init__(self, numeroinicial) :

		# generating random recs
		self.lista = []

		for x in range(numeroinicial) :

			leftrandom = random.randrange(2,560)
			toprandom = random.randrange(-580,10)
			width = random.randrange(10,30)
			height = random.randrange(15,30)

			self.lista.append(pygame.Rect(leftrandom,toprandom,width,height))

	def reagregar(self) :

		for x in range (len(self.lista)) :

			# si el rectangulo se pasa de la pantalla

			if self.lista[x].top > 482 :

				leftrandom = random.randrange(2,560)
				toprandom = random.randrange(-580,10)
				width = random.randrange(10,30)
				height = random.randrange(15,30)

				#replace the list with another rec 
				self.lista[x] = pygame.Rect(leftrandom,toprandom,width,height)




		

	def agregarotro(self) :

		pass

	def mover(self) :

		#move the recs to down

		for rectangulo in self.lista :

			rectangulo.move_ip(0,2)

	def pintar(self, superficie) :

		# pain all Recs

		for rectangulo in self.lista :

			pygame.draw.rect(superficie, (255,0,0),rectangulo)


def colision(player, recs) :

	for rec in recs.lista :

		if player.rect.colliderect(rec) :

			return True

	return False

def check_sound(sonido, cond) :

	if cond == True :

		sonido.play()

	cond = False

	return cond

def get_max_score(filename) :

	file = open(filename,"r")
	content = file.readline()
	return content

def save_max_score(filename,score) :

	file = open(filename, "r+")
	file.write(score)


def main() :

	pygame.init()
	pantalla = pygame.display.set_mode([600,480])
	pygame.display.set_caption("JP Space Defender")

	clock = pygame.time.Clock()
	salir = False

	# imagenes

	imagen_ship = pygame.image.load("imagenes/ship.png").convert_alpha()
	imagen_fondo = pygame.image.load("imagenes/space.jpg")
	imagen_explosion = pygame.image.load("imagenes/explosion.png")
	
	# sonidos

	sonido_game_over = pygame.mixer.Sound("sonidos/game_over.wav")
	sonido_game_over_cond = True

	sonido_congratulation = pygame.mixer.Sound("sonidos/max_score.wav")
	sonido_congratulation_cond = True

	#musica de fondo

	pygame.mixer.music.load("sonidos/fondo.mp3")

	# textos

	fuente1 = pygame.font.SysFont("Arial",50)
	fuente2 = pygame.font.SysFont("Courier",20,True)
	fuente3 = pygame.font.SysFont("Arial",30)
	game_over_text = fuente1.render("Game Over", 0,(255,255,254))
	jugador = Player(imagen_ship)
	recs1 = Recs(25)
	# variables aux
	vx = 0
	vy = 0
	velocidad = 10
	colisiono = False
	score = 0
	max_score = get_max_score("data.txt")
	max_score = int(max_score)
	# variables to check if the key is hold
	downsigueapretada = False
	upsigueapretada = False
	leftsigueapretada = False
	rightsigueapretada = False

	# sonar musica
	# param -> loop -1 -> play infinitely

	pygame.mixer.music.play(-1)

	while salir != True :
	
		for event in pygame.event.get() :

			if event.type == pygame.QUIT :

				salir = True

			# si colisiono se bloquea todo

			if  colisiono == False :

				if event.type == pygame.KEYDOWN :

					if event.key == pygame.K_LEFT :

						leftsigueapretada = True
						vx = -velocidad

					if event.key == pygame.K_RIGHT :

						rightsigueapretada = True
						vx =  velocidad

					if event.key == pygame.K_UP :

						upsigueapretada = True
						vy = - velocidad

					if event.key == pygame.K_DOWN :

						downsigueapretada = True
						vy = velocidad

				if event.type == pygame.KEYUP :

					if event.key == pygame.K_LEFT :

						leftsigueapretada = False

						if rightsigueapretada :
							vx = velocidad
						else :
							vx = 0

					if event.key == pygame.K_RIGHT :

						rightsigueapretada = False

						if leftsigueapretada :
							vx = - velocidad
						else :
							vx = 0

					if event.key == pygame.K_UP :

						upsigueapretada = False

						if downsigueapretada :
							vy = velocidad
						else :
							vy = 0

					if event.key == pygame.K_DOWN :

						downsigueapretada = False

						if upsigueapretada :
							vy = - velocidad
						else :
							vy = 0


		clock.tick(20)
		#print pygame.time.get_ticks() /1000		
		# si colisiona se hace lo sig...
		if colision(jugador, recs1) :
			colisiono = True
			sonido_game_over_cond = check_sound(sonido_game_over, sonido_game_over_cond)
			imagen_fondo.blit(game_over_text, (210,175))
			jugador.imagen = imagen_explosion
			pygame.mixer.music.stop()

			# save the new max score
			if score > max_score :

				save_max_score("data.txt", str(score))
				congratulations_text = fuente3.render("Congratulations, You Get The Max Score",0,(255,250,205))
				imagen_fondo.blit(congratulations_text,(100,250))
				sonido_congratulation_cond = check_sound(sonido_congratulation, sonido_congratulation_cond)

		# se mueve todo si no colisiona
		if colisiono == False :
			recs1.mover()
			score = pygame.time.get_ticks() / 1000
			jugador.mover(vx,vy)

			# fix the player out the screen

			# fix left
			if jugador.rect.left < 0 :
				
				jugador.rect.move_ip(10,0)

			#top
			if jugador.rect.top < 0 :

				jugador.rect.move_ip(0,10)

			if jugador.rect.top > 410 :

				jugador.rect.move_ip(0,-10)

			if jugador.rect.left > 540 :

				jugador.rect.move_ip(-10,0)


		pantalla.blit(imagen_fondo, (0,0))
		actual_score_text = fuente2.render("Score : " + str(score),0,(255,255,255))
		max_score_text = fuente2.render("Max Score : " + str(max_score), 0,(255,255,255))
		pantalla.blit(actual_score_text,(470,0))
		pantalla.blit(max_score_text,(435,25))
		recs1.pintar(pantalla)
		jugador.update(pantalla)
		
		pygame.display.update()

		recs1.reagregar()

	pygame.quit()

main()