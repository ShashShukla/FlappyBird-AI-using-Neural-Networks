import pygame as game
from random import randint
from pygame.locals import *
from collections import deque
from ai import Net

BIRD_SPRITE = game.image.load("bird.png")
g = 0.001
BIRD_HEIGHT = 80
BIRD_WIDTH = 80
BIRD_VELOCITY = 0.1
''' Start at the Center '''
INIT_X = 100
INIT_Y = 200
PIPE_WIDTH = 80
PIPE_PIECE_HEIGHT = 30
PIPE_ADD_RATE = 1750
PIPE_SCROLL_SPEED = .2
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
game.init()
screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
myfont = game.font.SysFont("monospace", 32)


# def init_setting:
	# SCREEN_WIDTH = 500
	# SCREEN_HEIGHT = 600
	# game.init()
	# screen = game.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Bird(game.sprite.Sprite):

	def __init__(self):	
		game.sprite.Sprite.__init__(self)
		self.x = INIT_X
		self.y = INIT_Y
		self.sprite = game.transform.scale(BIRD_SPRITE,(BIRD_HEIGHT,BIRD_WIDTH))
		self.velocity = BIRD_VELOCITY
		self.mask = game.mask.from_surface(self.sprite)


	def update_no_flap(self):
		self.velocity += g
		self.y += self.velocity

	def update_flap(self):
		self.velocity -= BIRD_VELOCITY * 10
		if self.velocity < -BIRD_VELOCITY * 5:
			self.velocity = -BIRD_VELOCITY * 5


	@property
	def rect(self):
	    return Rect(self.x, self.y, BIRD_HEIGHT, BIRD_WIDTH)
	
class Pipe(game.sprite.Sprite):

	def __init__(self):
		self.x = SCREEN_WIDTH - 2
		self.passed_flag = False
		self.sprite = game.Surface((PIPE_WIDTH, SCREEN_HEIGHT), SRCALPHA)
		self.sprite.convert()
		self.sprite.fill((0,0,0,0))
		total_pipe_body_pieces = int((SCREEN_HEIGHT - 3 * BIRD_HEIGHT - 3 * PIPE_PIECE_HEIGHT) / PIPE_PIECE_HEIGHT)
		self.bottom_pieces = randint(1, total_pipe_body_pieces)
		self.top_pieces = total_pipe_body_pieces - self.bottom_pieces

		pipe_sprite =game.image.load("pipe.png")
		pipe_sprite = game.transform.scale(pipe_sprite, (PIPE_WIDTH, 80))

		# bottom pipe
		for i in range(1, self.bottom_pieces + 1):
			piece_pos = (0, SCREEN_HEIGHT - i*PIPE_PIECE_HEIGHT)
			self.sprite.blit(pipe_sprite, piece_pos)

		# top pipe
		for i in range(self.top_pieces):
			self.sprite.blit(pipe_sprite, (0, i * PIPE_PIECE_HEIGHT))

		self.top_pieces += 1
		self.bottom_pieces += 1
		self.bot_height = self.bottom_pieces * PIPE_PIECE_HEIGHT
		self.mask = game.mask.from_surface(self.sprite)
		
	@property
	def rect(self):
		return Rect(self.x, 0, PIPE_WIDTH, PIPE_PIECE_HEIGHT)

	@property
	def visible(self):
		return -PIPE_WIDTH < self.x < SCREEN_WIDTH

	def update(self):
		self.x -= PIPE_SCROLL_SPEED 

	def collides_with(self, bird):
		return game.sprite.collide_mask(self, bird)

def play(headless=False, ai=None):
	bird = Bird()
	pipes = deque()
	frame = 0
	score = 0
	done = False

	while True:
		# draw bird
		bird.update_no_flap()
		# print "YO"
		if not headless:
			screen.fill((0, 255, 255))
			screen.blit(bird.sprite, (bird.x, bird.y))

		if frame %PIPE_ADD_RATE == 0:
			p = Pipe()
			pipes.append(p)

		collision_detected = any(p.collides_with(bird) for p in pipes)

		# check bounds
		if bird.y > 600 or bird.y < 0 or collision_detected:
			break

		while pipes and not pipes[0].visible:
			pipes.popleft()

		for p in pipes:
			if p.x + PIPE_WIDTH/2 < bird.x and not p.passed_flag:
				p.passed_flag = True
				score += 1
                                #print score
			p.update()
			if not headless:
				screen.blit(p.sprite, (p.x, 0))

		if not ai:
			for event in game.event.get():
				if event.type == game.QUIT:
					break

				if event.type == game.KEYDOWN and event.key == game.K_SPACE:
					bird.update_flap()

		elif ai.forward([bird.x - pipes[0].x,SCREEN_HEIGHT - bird.y - pipes[0].bot_height]) > 0.5:
			bird.update_flap()
		label = myfont.render("Score =" + str(score), 1, (255,100,0))
		screen.blit(label, (316, 40))

		# update screen
		if not headless:
			game.display.flip()
		frame += 1

	print 'Score: ' + str(score)
	return score

