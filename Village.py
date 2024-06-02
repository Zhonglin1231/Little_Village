import pygame
import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict, deque

pygame.init()

WIDTH = 1000
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
max_speed = 1
num_of_people = 100
grid_size = 50
map_path = "./resource/map_HongKong.png"
sex_set = ('male', 'female')
occupation_set = ('worker', 'farmer', 'leader', 'soldier')
skills_set = ('building', 'farming', 'fighting', 'leading')
special_status_set = ('sick', 'injured', 'pregnant')
nationality_set = ('Chinese', 'American', 'British', 'new', 'newnew')


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
    "info": COLOR_DEFINITIONS["white"],
    None: COLOR_DEFINITIONS["light_grey"],
    "new": COLOR_DEFINITIONS["red"],
    "newnew": COLOR_DEFINITIONS["blue"]
}

class Person:
    def __init__(self, x=None, y=None, nationality=None, age=None):
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.dx = 0
        self.dy = 0
        self.health = 100
        self.happiness = random.randint(0, 100)
        self.age = age if age is not None else random.randint(0, 100)
        self.sex = random.choice(sex_set)
        self.occupation = random.choice(occupation_set)
        self.skills = random.choice(skills_set)
        self.special_status = None  # e.g., 'sick', 'injured'
        self.nationality = nationality if nationality is not None else None
        self.IQ = random.randint(60, 180)
        self.intelligence = random.randint(0, 100)
        self.last_reproduce = None

    def show(self, size=10):
        pygame.draw.circle(SCREEN, COLORS[self.nationality], (self.x, self.y), size)

    def move(self, speed=0.75):
        # adjust position vector
        self.x += self.dx
        self.y += self.dy

        # avoid going out of bounds
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
        self.age += 1/365
        if self.age > 80:
            self.change_health(-0.1)

    def work(self):
        # if self.occupation == "worker":
        #     # to be added
        #     print("worker")
        # elif self.occupation == "farmer":
        #     # to be added
        #     print("farmer")
        return

    # -----------------------Interact with other people-------------------
    def reproduction(self):
        self.health -= 30

        # create a new person and add to the population
        if self.nationality == None:
            new_person = Person(x=self.x, y=self.y, nationality="new", age=0)
        elif self.nationality == "new":
            new_person = Person(x=self.x, y=self.y, nationality="newnew", age=0)
        else:
            new_person = Person(x=self.x, y=self.y, age=0)
        village.population.append(new_person)
        village.INFO["Population Size"] += 1

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
            'nationality': self.nationality,
            'IQ': self.IQ,
            'intelligence': self.intelligence
        }


class Village:
    def __init__(self, num_of_people):
        self.population = [Person() for _ in range(num_of_people)]
        self.grid = defaultdict(list)
        self.INFO = {
            "Population Size": num_of_people,
            "GDP": 0,
            "dead": 0,
            "year": 0,
            "population change": 0
        }

    def update_grid(self):
        self.grid = defaultdict(list)
        for person in self.population:
            grid_x = person.x // grid_size
            grid_y = person.y // grid_size
            self.grid[(grid_x, grid_y)].append(person)

    def get_nearby_people(self, person):
        grid_x = person.x // grid_size
        grid_y = person.y // grid_size
        nearby_people = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nearby_people.extend(self.grid[(grid_x + dx, grid_y + dy)])
        return nearby_people

    def stimulate_day(self):
        # update data
        self.INFO["year"] += 1/365
        self.INFO["year"] = round(self.INFO["year"], 3)
        self.update_grid()
        self.show_stats()

    def show_stats(self):
        # show stats
        for i, (info, count) in enumerate(self.INFO.items()):
            text = f"{info}: {count}"
            font = pygame.font.Font(None, 36)
            text = font.render(text, True, COLORS["info"])
            SCREEN.blit(text, (10, 10 + 40 * i))


class DynamicChart:

    def __init__(self) :
        self.fig, self.ax = plt.subplots()
        self.x_data = deque(maxlen=1000)
        self.y_data = deque(maxlen=1000)
        self.line, = plt.plot([], [], 'r-', animated=True)

    def create_chart(self):
        self.ax.set_xlim(0, 50)
        self.ax.set_ylim(50, 800)
        return self.line,

    def update(self, frame):
        self.x_data.append(village.INFO["year"])
        self.y_data.append(village.INFO["Population Size"])
        self.line.set_data(self.x_data, self.y_data)
        return self.line,

    def show(self):
        plt.show(block=False)


# initialize village
village = Village(100)
current_year_info = dict(village.INFO)
last_year_info = None

# create dynamic chart
chart = DynamicChart()
anim = animation.FuncAnimation(chart.fig, chart.update, frames=range(200), init_func=chart.create_chart, blit=True)
chart.show()
 
# pygame loop
animating = True
while animating:
    # parameter calculation part
        # calculate yearly rate
    year = f"{village.INFO['year']:.3f}"
    if year[-3:] in ["000", "999", "001"]:
        last_year_info = current_year_info
        current_year_info = dict(village.INFO)
        print(current_year_info["Population Size"], last_year_info["Population Size"])
        # calculate change of population
        village.INFO["population change"] = current_year_info["Population Size"] - last_year_info["Population Size"]
        print(village.INFO["population change"])

    # set background color
    SCREEN.fill(COLORS["background"])
    # # add the map on to the background
    # map = pygame.image.load(map_path)
    # SCREEN.blit(map, (0, 0))

    # pygame draws things to the screen
    village.stimulate_day()

    # people movement
    for p in village.population:
        p.age_up()
        p.work()
        p.move()
        p.show()

    # do actions for people
    for p in village.population:

        if p.health <= 0:
            village.population.remove(p)
            village.INFO["Population Size"] -= 1
            village.INFO["dead"] += 1

        # the action with others
        nearby_people = village.get_nearby_people(p)
        for other in nearby_people:
            # make sure distance is close to interact
            if math.sqrt((p.x - other.x)**2 + (p.y - other.y)**2) < 20 and p != other:
                # action for high health people
                if p.health > 60 and p.age >= 18 and other.age >= 18 and p.age <= 60 and other.age <= 60:
                    # action for female
                    if p.sex == "female":
                        # action for diff gender
                        if other.sex == "male":
                            # reproduction
                            # possibility of 0.1 to reproduce and pass 1 year didn't reproduce
                            if p.last_reproduce is not None:
                                if random.random() < 0.1 and village.INFO["year"] - p.last_reproduce > 1:
                                    p.reproduction()
                                    p.last_reproduce = village.INFO["year"]
                                    # possibility of 0.01 to die after reproduce
                                    if random.random() < 0.01:
                                        p.change_health(-100)
                                        village.INFO["dead"] += 1
                            if p.last_reproduce is None:
                                random.random() < 0.1
                                p.reproduction()
                                p.last_reproduce = village.INFO["year"]
                                # possibility of 0.01 to die after reproduce
                                if random.random() < 0.01:
                                    p.change_health(-100)
                                    village.INFO["dead"] += 1

        p.health += 0.1



    # update the display
    # plt.pause(0.01)
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

pygame.quit()
plt.close()
