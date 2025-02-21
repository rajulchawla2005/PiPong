import pygame

# rect tuple (x-axis, y-axis, width, height)

max_width = 1280
max_height = 720
bar_height = 60
player_score = 0
computer_score = 0

global running
running = True

# pygame setup
pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()



def initialise():

	# initialise the display
	screen.fill("black")
	#top bar
	pygame.draw.rect(screen, "white", (0, 0, max_width, bar_height))
	
	#bottom bar
	pygame.draw.rect(screen, "white", (0, max_height-bar_height, max_width, bar_height))
	
	my_font = pygame.font.SysFont('Comic Sans MS', 100, bold=True)
	
	update_score()
	

def update_score():
	player_score_text_surface = my_font.render(str(player_score), True, "white")
	screen.blit(player_score_text_surface, (420, 100))
	computer_score_text_surface = my_font.render(str(computer_score), True, "white")
	screen.blit(computer_score_text_surface, (850, 100))

def update():
	pass


def main():
	initialise()
	# while the game is running
	global running
	while running:
		# check if the close button has been pressed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		# start of render (figure out what to update)
		update()
		# end of render (send updates to screen)
		pygame.display.flip()
		
		clock.tick(60)

if __name__ == "__main__":
	main()
	
pygame.quit()
