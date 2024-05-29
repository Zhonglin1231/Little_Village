import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 800
SCREEN =pygame.display.set_mode((WIDTH, HEIGHT))
max_speed = 2
num_of_people = 100
map_path = "./resource/map_HongKong.png"

STATE_COUNTS = {
    "healthy": 0,
    "infected": 0,
    "immune": 0,
    "dead": 0
}

COLOR_DEFINITIONS = {
    "grey": (35, 35, 40),
    "light_grey": (70, 70, 90),
    "white": (255, 248, 240),
    "red": (239, 71, 111),
    "blue": (72, 133, 237),
    "green": (0, 255, 0)
}

COLORS = {
    "background": COLOR_DEFINITIONS["grey"],
    "healthy": COLOR_DEFINITIONS["green"],
    "infected": COLOR_DEFINITIONS["red"],
    "immune": COLOR_DEFINITIONS["blue"],
    "dead": COLOR_DEFINITIONS["light_grey"]
}

class Person:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.dx = 0
        self.dy = 0
        self.state = "healthy"

    def show(self, size = 10):
        pygame.draw.circle(SCREEN, COLORS[self.state], (self.x, self.y), size)

    def move(self, speed = 0.75):

        # adjust position vector
        self.x += self.dx
        self.y += self.dy

        # aviod going out of bounds
        if self.x >= WIDTH:
            self.x = WIDTH - 1
            self.dx *= -1
        if self.y >= HEIGHT:
            self.y = HEIGHT - 1
            self.dy *= -1
        if self.x < 0:
            self.x = 1
            self.dx *= -1
        if self.y < 0:
            self.y = 1
            self.dy *= -1

        # set the maximum speed
        if self.dx > max_speed:
            self.dx -= 0.05
        if self.dy > max_speed:
            self.dy -= 0.05
        if self.dx < max_speed * -1:
            self.dx += 0.05
        if self.dy < max_speed * -1:
            self.dy += 0.05

        self.dx += random.uniform(-speed, speed)
        self.dy += random.uniform(-speed, speed)

    def get_infected(self):
        self.state = "infected"

def show_stats():
    # show stats
    for i, (state, count) in enumerate(STATE_COUNTS.items()):
        text = f"{state}: {count}"
        font = pygame.font.Font(None, 36)
        text = font.render(text, True, COLORS[state])
        SCREEN.blit(text, (10, 10 + 40 * i))

# initialize people
people = [Person() for i in range(num_of_people)]
myself = people[-1]
myself.state = "infected"
STATE_COUNTS["healthy"] = num_of_people
# people[0].state = "infected"
STATE_COUNTS["infected"] += 1
STATE_COUNTS["healthy"] -= 1
people[1].state = "immune"
STATE_COUNTS["immune"] += 1
STATE_COUNTS["healthy"] -= 1

# pygame loop
animating = True
while animating:

    # set background color
    SCREEN.fill(COLORS["background"])
    # add the map on to the background
    map = pygame.image.load(map_path)
    SCREEN.blit(map, (0, 0))

    # pygame draws things to the screen
    for p in people[:-1]:
        p.move()
        p.show()
        
    myself.x, myself.y = pygame.mouse.get_pos()
    people[-1].show()
    

    for p in people:

        if p.state == "infected":
            # infect people
            for other in people:
                if p != other and other.state == "healthy":
                    dist = math.sqrt((p.x - other.x)**2 + (p.y - other.y)**2)
                    if dist < 7.5:
                        # infect the other person, the possibility of infection is 0.2
                        if random.random() < 0.2:
                            other.get_infected()
                            STATE_COUNTS["healthy"] -= 1
                            STATE_COUNTS["infected"] += 1

            # self recovery
            if random.random() < 0.001:
                p.state = "immune"
                STATE_COUNTS["infected"] -= 1
                STATE_COUNTS["immune"] += 1

            # dead people
            if random.random() < 0.0001:
                p.state = "dead"
                STATE_COUNTS["infected"] -= 1
                STATE_COUNTS["dead"] += 1

        # immune people return healthy
        if p.state == "immune":
            if random.random() < 0.0002:
                p.state = "healthy"
                STATE_COUNTS["immune"] -= 1
                STATE_COUNTS["healthy"] +=1

        # remove dead people
        if p.state == "dead":
            people.remove(p)

    # show state counts
    show_stats()

    # update the display
    pygame.display.flip()

    # track user interaction
    for event in pygame.event.get():

        # user closes the window
        if event.type == pygame.QUIT:
            animating = False

        # users presses a key
        if event.type == pygame.KEYDOWN:
            
            # escape key closes the animation
            if event.key == pygame.K_ESCAPE:
                animating = False


            # if event.key == pygame.K_UP:
            #     myself.y -= 10
            # if event.key == pygame.K_DOWN:
            #     myself.y += 10
            # if event.key == pygame.K_LEFT:
            #     myself.x -= 10
            # if event.key == pygame.K_RIGHT:
            #     myself.x += 10


                
