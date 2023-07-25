import pygame
import os
from random import randint

pygame.init()

WIDTH, HEIGHT = 960, 540
#ekraan jaguneb BOXCOUNTks 96 pix ja 54 pix suuruseks ruuduks
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snake game")

GREEN = 50, 200, 50
BOXCOLOUR = 0, 0, 0
BOXSIZE = 36
BOXCOUNT = int(HEIGHT / BOXSIZE)
FPS = 60
TEMPO = 150 # aja intervall millisekundites
clock = pygame.time.Clock()


apple_img = pygame.image.load(
    os.path.join("assets", "apple.png")).convert_alpha()

restart_img = pygame.image.load(
    os.path.join("assets", "apple.png")).convert_alpha()

apple_img = pygame.transform.scale(apple_img, (BOXSIZE * 4/5, BOXSIZE * 4/5))


def draw_window():
    # draws the background and grid
    WIN.fill(GREEN)
    for i in range(BOXCOUNT):
        for j in range(BOXCOUNT):
            pygame.draw.rect(WIN, BOXCOLOUR, pygame.Rect(i * BOXSIZE, j * BOXSIZE, BOXSIZE, BOXSIZE), 2)

    #drawing score text
    global score
    text = "Score: "
    text += str(score)
    font = pygame.font.SysFont(None, 48)
    text_img = font.render(text, True, "BLACK")
    text_rect = text_img.get_rect(center = (700, 270))
    WIN.blit(text_img, text_rect)
    WIN.blit(apple_img, apple_rect)


def collision_with_tail():
    for tail in tail_list[:-1]:
        tail_rect = tail.tail_rect
        if snake_head.head == tail_rect:
            return True


def out_of_borders():
    head_rect = snake_head.head
    outer_border = BOXSIZE * BOXCOUNT - BOXSIZE
    if head_rect.x < 0 or head_rect.y < 0 or head_rect.x > outer_border or head_rect.y > outer_border:
        return True


def spawn_apple():
    while True:

        global apple_rect
        apple_rect = apple_img.get_rect(center = (randint(1, BOXCOUNT) * BOXSIZE - BOXSIZE / 2, randint(1, BOXCOUNT) * BOXSIZE - BOXSIZE / 2))
        
        is_available = True

        for obj in tail_list:
            rect = obj.tail_rect
            if rect.colliderect(apple_rect):
                is_available = False
        
        if is_available is True: #If the coordinates are not on the tail
            WIN.blit(apple_img, apple_rect)
            break
        else: continue

def apple_eaten():
    if snake_head.head.colliderect(apple_rect):
        global score
        score += 1
        
        tail_list.append(Snake_tail(pygame.Rect(tail_list[-1].tail_rect)))
        tail_list[-1].move(head_rect) # moves the last rect in the list to the coordinates where the head was
        tail_list.insert(0, tail_list[-1]) # puts the list in the right order
        tail_list.pop(-1)
        return True
  
class Snake_head: 
    def __init__(self, rect): # snake_head.head tähistab ruutu, mis asub pea koha peal
        self.head = rect
  
    def move(self, direction):
        if direction == "right":
            self.head.x += BOXSIZE
        elif direction == "left":
            self.head.x -= BOXSIZE
        elif direction == "up":
            self.head.y -= BOXSIZE
        elif direction == "down":
            self.head.y += BOXSIZE

class Snake_tail: #self.tail_rect tähistab ruutu, mis on saba koha peal
    def __init__(self, rect):
        self.tail_rect = rect
    
    def move(self, newrect): # !!!!!!!!!!!!!!! maybe something could be done !!!!!!
        self.tail_rect.x = newrect.x
        self.tail_rect.y = newrect.y



def main():

    #setting the starting position
    tail_length = 3
    global tail_list
    tail_list = list() # tail_listis contains objects with the tail rectangles
    for i in range(-1, -tail_length-1, -1):
        tail_list.append(Snake_tail(pygame.Rect(i*BOXSIZE, 0, BOXSIZE, BOXSIZE)))
    
    global snake_head
    snake_head = Snake_head(pygame.Rect(0, 0, BOXSIZE, BOXSIZE))
    global score
    score = 0
 
    
    
    spawn_apple()
    apple_eaten()
    draw_window() # draws the grid

    head_direction = "right"
    
    run = True
    moving = False
    key_pressed = False
    end = False
    won = False

    last_time = pygame.time.get_ticks()

    pygame.draw.rect(WIN, "RED", snake_head.head)
    while run:
        global clock
        clock.tick(FPS) # the code doesn't run more than FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
                


            if event.type == pygame.KEYDOWN and key_pressed is False and end == False: # if a key is pressed moving value is set to True and direction is changed
                moving = True
                if event.key == pygame.K_RIGHT:
                    if head_direction != "left":
                        head_direction = "right"
                        key_pressed = True

                elif event.key == pygame.K_LEFT:
                    if head_direction != "right":
                        head_direction = "left"
                        key_pressed = True

                elif event.key == pygame.K_UP:
                    if head_direction != "down":
                        head_direction = "up"
                        key_pressed = True

                elif event.key == pygame.K_DOWN:
                    if head_direction != "up":
                        head_direction = "down"
                        key_pressed = True
            
            if end == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                main()
                run = False

        current_time = pygame.time.get_ticks()
        

        if current_time - last_time >= TEMPO:
            if moving:
                draw_window()

                global head_rect
                head_rect = pygame.Rect(snake_head.head)

                snake_head.move(head_direction)
                if apple_eaten() is True:
                    spawn_apple()

                elif collision_with_tail() is not True and out_of_borders() is not True:
                    tail_list[-1].move(head_rect) # moves the last rect in the list to the coordinates where the head was
                    tail_list.insert(0, tail_list[-1]) # puts the list in the right order
                    tail_list.pop(-1)

                elif collision_with_tail() is True or out_of_borders() is True:
                    end = True
                
                elif len(tail_list) == 224:
                    won = True


                for obj in tail_list:
                    pygame.draw.rect(WIN, BOXCOLOUR, obj.tail_rect)

                if end == False:
                    pygame.draw.rect(WIN, "RED", snake_head.head)  
                key_pressed = False

            if end or won:
                moving = False
        
                snake_head.head = pygame.Rect(head_rect)
                pygame.draw.rect(WIN, "RED", snake_head.head)

                if end:
                    big_text = "GAME OVER!!!"
                elif won:
                    big_text = "YOU WON!!!"
                
                small_text = "Press space to restart."

                font = pygame.font.SysFont(None, 100)
                text_img = font.render(big_text, True, "YELLOW")
                text_rect = text_img.get_rect(center=(270, 270))
                WIN.blit(text_img, text_rect)

                font = pygame.font.SysFont(None, 26)
                text_img = font.render(small_text, True, "YELLOW")
                text_rect = text_img.get_rect(center=(270, 310))
                WIN.blit(text_img, text_rect)


            last_time += TEMPO # tempo = the pace with which the snake moves
        
        pygame.display.update()
       

if __name__ == "__main__":
    main()