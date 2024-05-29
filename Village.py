import pygame
import random
import math

pygame.init()

WIDTH = 1000
HEIGHT = 800
SCREEN =pygame.display.set_mode((WIDTH, HEIGHT))
max_speed = 1
num_of_people = 100
map_path = "./resource/map_HongKong.png"
sex_set = ('male', 'female')
occupation_set = ('worker', 'farmer', 'leader', 'soldier')
skills_set = ('building', 'farming', 'fighting', 'leading')
special_status_set = ('sick', 'injured', 'pregnant')
nationality_set = ('Chinese', 'American', 'British')

STATE_COUNTS = {
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
    None: COLOR_DEFINITIONS["light_grey"]
}

class Person:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.dx = 0
        self.dy = 0
        self.health = 100
        self.happiness = random.randint(0, 100)
        self.age = random.randint(0, 100)
        self.sex = random.choice(sex_set)
        self.occupation = random.choice(occupation_set)
        self.skills = random.choice(skills_set)
        self.special_status = None  # e.g., 'sick', 'injured'
        self.nationality = None
        self.IQ = random.randint(60, 180)
        self.intelligence = random.randint(0, 100)


    def show(self, size = 10):
        pygame.draw.circle(SCREEN, COLORS[self.nationality], (self.x, self.y), size)

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

    # -----------------------Change Attribute------------------------------
    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, 100))

    def change_happiness(self, amount):
        self.happiness += amount
        self.happiness = max(0, min(self.happiness, 100))

    def age_up(self):
        self.age += 1
        if self.age > 80:
            self.change_health(-10)

    def work(self):
        if self.occupation == "worker":
            # to be added
            print("worker")
        elif self.occupation == "farmer":
            # to be added
            print("farmer")

    # -----------------------Interact with other people-------------------
    def reproduction(self, other):
        # to be added
        print("reproduction")

    # -----------------------get stats------------------------------------
    def get_status(self):
        return {
            'health': self.health,
            'happiness': self.happiness,
            'age': self.age,
            'sex': self.sex,
            'occupation': self.occupation,
            'skills': self.skills,
            'special_status': self.special_status,
            'nationality': self.national,
            'IQ': self.IQ,
            'intelligence': self.intelligence
    }


# class Village:
    # may be consider to add?


# initialize people
people = [Person() for i in range(num_of_people)]

# pygame loop
animating = True
while animating:

    # set background color
    SCREEN.fill(COLORS["background"])
    # # add the map on to the background
    # map = pygame.image.load(map_path)
    # SCREEN.blit(map, (0, 0))

    # pygame draws things to the screen
    for p in people:
        # random movement
        p.move()
        p.show()

    # do actions for people
    for p in people:
        print("some actions")

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