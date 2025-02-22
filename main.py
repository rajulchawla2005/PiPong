import pygame
import time
import random

# rect tuple (x-axis, y-axis, width, height)

max_width = 1280
max_height = 720
bar_height = 60
bounces = []
borders = []
speed = 3


global running, player_score, computer_score, player_rect, computer_rect, ball, ball_direction, interrupt
running = True
player_score = 0
computer_score = 0
player_rect = None
computer_rect = None
ball = None
# an int, either 0 (bottom left), 1 (bottom right), 2 (top left), 3 (top right)
ball_direction = None
interrupt = None

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
	global player_rect, computer_rect, ball, ball_direction, interrupt
	player_rect = pygame.draw.rect(screen, "white", ((bar_height/2), 285, bar_height/2, 150))
	
	computer_rect = pygame.draw.rect(screen, "white", ((max_width-bar_height), 285, bar_height/2, 150))
	
	# draw the ball in the center (x=max_width/2-ball_length/2, y=max_height/2-ball_length/2, ball_length, ball_length)
	ball = pygame.draw.rect(screen, "white", (615, 335, 50, 50))
	# start off random
	ball_direction = random.randint(0,3)
	
	# put both scores down
	update_score()
	interrupt = False
	
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
	
# increases the computer score, then update the scores
def computer_score_increase():
	global computer_score
	computer_score += 1
	
def player_up():
	global player_rect
	# get a copy of the current player rectangle
	new_player_rect = player_rect.copy()
	# move that copy up
	new_player_rect.move_ip(0, -5)
	# check if up movement is valid, does it intersect the top bar
	if new_player_rect.colliderect(bounces[0]):
		# if so, don't update anything
		return
	# draw the old rectangle as black (blends in)
	pygame.draw.rect(screen, "black", player_rect)
	# draw the new rectangle as white
	pygame.draw.rect(screen, "white", new_player_rect)
	# update the player rectangle to this new one
	player_rect = new_player_rect
	
	
def player_down():
	global player_rect
	# get a copy of the current player rectangle
	new_player_rect = player_rect.copy()
	# move that copy down
	new_player_rect.move_ip(0, 5)
	# check if down movement is valid, does it intersect the bottom bar
	if new_player_rect.colliderect(bounces[1]):
		# if so, don't update anything
		return
	# draw the old rectangle as black (blends in)
	pygame.draw.rect(screen, "black", player_rect)
	# draw the new rectangle as white
	pygame.draw.rect(screen, "white", new_player_rect)
	# update the player rectangle to this new one
	player_rect = new_player_rect

def check_player_input():
	# get user input
	keys = pygame.key.get_pressed()
	# if the up key has been pressed
	if keys[pygame.K_UP]:
		player_up()
		# don't check for a different input
		return
	# if the down key has been pressed
	if keys[pygame.K_DOWN]:
		player_down()
		# don't check for a different input
		return
		
def ball_collision_check(ball):
	global ball_direction
	# if the ball collides with the bottom bar
	if ball.colliderect(bounces[1]):
		# if ball direction is bottom left (0), it is now top left (2)
		# if ball direction is bottom right (1), it is now top right (3)
		match ball_direction:
			case 0:
				ball_direction = 2
			case 1:
				ball_direction = 3
		return True
		
	# if the ball collides with the top bar
	if ball.colliderect(bounces[0]):
		# if ball direction is top left (2), it is now bottom left (0)
		# if ball direction is top right (3), it is now bottom right (1)
		match ball_direction:
			case 2:
				ball_direction = 0
			case 3:
				ball_direction = 1
		return True
		
	# if the ball collides with the player
	if ball.colliderect(player_rect):
		# if ball direction is bottom left (0), it is now bottom right (1)
		# if ball direction is top left (2), it is now top right (3)
		match ball_direction:
			case 0:
				ball_direction = 1
			case 2:
				ball_direction = 3
		return True
				
	# if the ball collides with the computer
	if ball.colliderect(computer_rect):
		# if ball direction is bottom right (1), it is now bottom left (0)
		# if ball direction is top right (3), it is now top left (2)
		match ball_direction:
			case 1:
				ball_direction = 0
			case 3:
				ball_direction = 2
		return True
				
	# if the ball collides with the players border
	if ball.colliderect(borders[0]):
		interrupt = True
		computer_score_increase()
		initialise()
		return True
		
	# if the ball collides with the computers border
	if ball.colliderect(borders[1]):
		interrupt = True
		player_score_increase()
		initialise()
		return True
				
		
	return False
	
		
def ball_bottom_left():
	global ball
	# get a copy of the ball
	new_ball = ball.copy()
	# move that copy bottom left
	new_ball.move_ip(-1*speed, speed)
	# check if down-left movement collides with anything, if it does then return
	if ball_collision_check(new_ball):
		return
	# draw the old ball as black (blends in)
	pygame.draw.rect(screen, "black", ball)
	# draw the new ball as white
	pygame.draw.rect(screen, "white", new_ball)
	# update the ball to this new one
	ball = new_ball		
	
def ball_bottom_right():
	global ball
	# get a copy of the ball
	new_ball = ball.copy()
	# move that copy bottom right
	new_ball.move_ip(speed, speed)
	# check if down-right movement collides with anything, if it does then return
	if ball_collision_check(new_ball):
		return
	# draw the old ball as black (blends in)
	pygame.draw.rect(screen, "black", ball)
	# draw the new ball as white
	pygame.draw.rect(screen, "white", new_ball)
	# update the ball to this new one
	ball = new_ball	
	
def ball_top_left():
	global ball
	# get a copy of the ball
	new_ball = ball.copy()
	# move that copy top left
	new_ball.move_ip(-1*speed, -1*speed)
	# check if up-left movement collides with anything, if it does then return
	if ball_collision_check(new_ball):
		return
	# draw the old ball as black (blends in)
	pygame.draw.rect(screen, "black", ball)
	# draw the new ball as white
	pygame.draw.rect(screen, "white", new_ball)
	# update the ball to this new one
	ball = new_ball	
	
def ball_top_right():
	global ball
	# get a copy of the ball
	new_ball = ball.copy()
	# move that copy top right
	new_ball.move_ip(speed, -1*speed)
	# check if up-right movement collides with anything, if it does then return
	if ball_collision_check(new_ball):
		return
	# draw the old ball as black (blends in)
	pygame.draw.rect(screen, "black", ball)
	# draw the new ball as white
	pygame.draw.rect(screen, "white", new_ball)
	# update the ball to this new one
	ball = new_ball	

def update_ball():
	match ball_direction:
		case 0:
			ball_bottom_left()
		case 1:
			ball_bottom_right()
		case 2:
			ball_top_left()
		case 3:
			ball_top_right()
	return
	
def move_computer_up():
	global computer_rect
	# get a copy of the computer rectangle
	new_computer_rect = computer_rect.copy()
	# move the computer up
	new_computer_rect.move_ip(0, -1*speed)
	# check if it intersects the top bar
	if new_computer_rect.colliderect(bounces[0]):
		# if so, don't update anything
		return
	# draw the old rectangle as black (blends in)
	pygame.draw.rect(screen, "black", computer_rect)
	# draw the new rectangle
	pygame.draw.rect(screen, "white", new_computer_rect)
	# update the computer rectangle to this new one
	computer_rect = new_computer_rect
	
def move_computer_down():
	global computer_rect
	# get a copy of the computer rectangle
	new_computer_rect = computer_rect.copy()
	# move the computer down
	new_computer_rect.move_ip(0, speed)
	# check if it intersects the bottom bar
	if new_computer_rect.colliderect(bounces[1]):
		# if so, don't update anything
		return
	# draw the old rectangle as black (blends in)
	pygame.draw.rect(screen, "black", computer_rect)
	# draw the new rectangle
	pygame.draw.rect(screen, "white", new_computer_rect)
	# update the computer rectangle to this new one
	computer_rect = new_computer_rect
	
def update_computer():
	# generate a random value between 0 and 10
	rng_value = random.randint(0,10)
	# store the current y coordinate of the computer and ball
	current_y_coord = computer_rect.y
	current_ball_y_coord = ball.y
	# chance of doing nothing
	if rng_value < 3:
		return
		
	# computer is below ball
	if current_y_coord > current_ball_y_coord:
		move_computer_up()
		return
	# computer is above ball
	elif current_y_coord < current_ball_y_coord:
		move_computer_down()
		return
	# computer is at the same level
	else:
		return
	

def update():
	# see what the user is doing
	check_player_input()
	# update the ball
	update_ball()
	# move computer
	update_computer()

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
		if not interrupt:
			update()
		# end of render (send updates to screen)
		pygame.display.flip()
		
		clock.tick(60)

if __name__ == "__main__":
	main()
	
pygame.quit()
