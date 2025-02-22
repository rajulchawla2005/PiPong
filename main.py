import pygame
import time

# rect tuple (x-axis, y-axis, width, height)

max_width = 1280
max_height = 720
bar_height = 60
bounces = []
borders = []

global running, player_score, computer_score, player_rect, computer_rect
running = True
player_score = 0
computer_score = 0
player_rect = None
computer_rect = None

# pygame setup
pygame.init()
my_font = pygame.font.SysFont('Comic Sans MS', 100)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()



def initialise():

	# initialise the display
	screen.fill("black")
	# top bar (x=0, y=0, width=max_width, height=bar_height)
	top_rect = pygame.draw.rect(screen, "white", (0, 0, max_width, bar_height))
	# bottom bar (x=0, y=max_height-bar_height, width=max_width, height=bar_height
	bottom_rect = pygame.draw.rect(screen, "white", (0, max_height-bar_height, max_width, bar_height))
	# left bar (x=0, y=0, width=bar_height/2, height=max_height)
	left_rect = pygame.draw.rect(screen, "grey", (0, 0, bar_height/2, max_height))
	# right bar (x=max_width-(bar_height/2), y=0, width=bar_height/2, height=max_height)
	right_rect = pygame.draw.rect(screen, "grey", ((max_width-(bar_height/2)), 0, bar_height/2, max_height))
	# put all the rectangles into either a bounce category or a lose category
	bounces.append(top_rect)
	bounces.append(bottom_rect)
	borders.append(left_rect)
	borders.append(right_rect)
	
	# draw the player (x=bar_height/2, y=max_width/2-player_height/2, width=bar_height/2, height=150)
	player_rect = pygame.draw.rect(screen, "white", ((bar_height/2), 285, bar_height/2, 150))
	
	# put both scores down
	update_score()
	print(borders, bounces)
	
# will update the score to the global values, updating the screen
def update_score():
	# get the top rectangle (background of scores
	top_rect = bounces.pop(0)
	# redraw the top rectangle
	top_rect = pygame.draw.rect(screen, "white", (0, 0, max_width, bar_height))
	# put the rectangle back in the bounces
	bounces.insert(0, top_rect)
	# draw the scores 
	player_score_text_surface = my_font.render(str(player_score), True, "black")
	screen.blit(player_score_text_surface, (426, 0))
	computer_score_text_surface = my_font.render(str(computer_score), True, "black")
	screen.blit(computer_score_text_surface, (853, 0))
	
# increases the player score, then update the scores
def player_score_increase():
	global player_score
	player_score += 1
	update_score()
	
# increases the computer score, then update the scores
def computer_score_increase():
	global computer_score
	computer_score += 1
	update_score()

def check_player_input():
	# get user input
	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP]:
		print("up key has been pressed")
	if keys[pygame.K_DOWN]:
		print("down key has been pressed")
				

def update():
	check_player_input()

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
