import pygame
import button
import csv


pygame.init()


#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Lygiai')

#apibrėžti žaidimo kintamuosius
EILES = 16
MAX_STULP = 150
TILE_SIZE = SCREEN_HEIGHT // EILES
TILE_TYPES = 20
level = 0 
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


#load images
klase_img = pygame.image.load('img/background/klase.jpg').convert_alpha()
#ikelti kbadratus i sarasa
img_list = []
for x in range (TILE_TYPES):
	img = pygame.image.load(f'img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

#splavos
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)


#sukurti empty tile sarasa
world_data = []
for eile in range(EILES):
	r = [-1] * MAX_STULP
	world_data.append(r)

for tile in range(0,150):
	world_data[EILES - 1][tile] = 14

#funkcija uzrasyti teksta
def draw_text (text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#create funvtion for drawing background
def draw_bg():
	screen.fill(GREEN)
	width = klase_img.get_width()
	for x in range(4):
		screen.blit(klase_img, ((x * width) - scroll * 0.5,-50))


#nupiesti tinkla/ grid
def draw_grid():
	#vertikalios linijos
	for c in range(MAX_STULP + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#Horizontalios linijos
	for c in range(EILES + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


def draw_world():
	for y, eile in enumerate(world_data):
		for x, tile in enumerate(eile):
			if tile >= 0:
					screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#sukurti mygtukus
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 60, save_img, 0.5)
load_button = button.Button(SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT + LOWER_MARGIN - 60, load_img, 0.5)
#sukurti mygtuku sarasa
button_list = []
button_stulp = 0
button_eil = 0
for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (75 * button_stulp) + 50, 75 * button_eil + 50, img_list[i],1)
	button_list.append(tile_button)
	button_stulp += 1
	if button_stulp == 3:
		button_eil += 1
		button_stulp = 0



run = True 
while run:

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Spausti rodykles keiciant lygius', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save ir load data
	if save_button.draw(screen):
		#save level data
		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for eile in world_data:
				writer.writerow(eile)
	if load_button.draw(screen):
		#ikelti leveli data
		#resetinti scroll atgal i pradzia lygio
		scroll = 0
		with open(f'level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate (reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)

				

	#nupiesti mygtuku skyda
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
	
	#pasirinkti bloka
	butten_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)
	
	
	
	#eiti po zemelapi
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_STULP * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	
	#pridet nauju tiles ant mapo
	#gauti pelytes pozicija
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE 
	y = pos[1] // TILE_SIZE

	#tikrinti ar koordinates yra viduje tilesu
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#updatinti tile verte
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#klaviaturos paspaudimai
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 2

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1

			


	pygame.display.update()

pygame.quit()