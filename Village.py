import pygame
import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

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
nationality_set = ('Chinese', 'American', 'British')
count = 0

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
    None: COLOR_DEFINITIONS["light_grey"]
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
        self.age_classifier = "kid" if self.age < 18 else "adult" if self.age < 60 else "elder"
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
        self.x += self.dx
        self.y += self.dy

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

    def change_health(self, amount):
        self.health += amount
        self.health = max(0, min(self.health, 100))

    def change_happiness(self, amount):
        self.happiness += amount
        self.happiness = max(0, min(self.happiness, 100))

    def age_up(self):
        self.age += 1/365
        if self.age > 80:
            self.change_health(-random.randint(0, 15)/100)
        if self.age > 60:
            self.change_health(-random.randint(0, 12)/100)

    def work(self):
        return

    def reproduction(self):
        self.health -= 30

        new_person = Person(x=self.x, y=self.y, age=0)
        village.population.append(new_person)
        village.INFO["Population Size"] += 1

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
            "population change": 0,
            "Press to M show Detail": "(English Input Method)"
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
        self.INFO["year"] += 1/365
        self.INFO["year"] = round(self.INFO["year"], 3)
        self.update_grid()
        self.show_stats()

    def show_stats(self):
        for i, (info, count) in enumerate(self.INFO.items()):
            text = f"{info}: {count}"
            font = pygame.font.Font(None, 36)
            text = font.render(text, True, COLORS["info"])
            SCREEN.blit(text, (10, 10 + 40 * i))

    def get_age_distribution(self):
        age_bins_male = [0] * 10
        age_bins_female = [0] * 10
        for person in self.population:
            age_bin = int(person.age // 10)
            if age_bin >= 10:
                age_bin = 9
            if person.sex == 'male':
                age_bins_male[age_bin] -= 1
            else:
                age_bins_female[age_bin] += 1
        return age_bins_male, age_bins_female

class DynamicChart:
    def __init__(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))

    def create_chart(self):
        self.x_data = []
        self.y_data = []
        self.ax1.set_xlim(0, 50)
        self.ax1.set_ylim(50,800)
        self.line1, = self.ax1.plot([], [], 'r-', animated=True)
        self.ax1.set_xlabel('Year')
        self.ax1.set_ylabel('Population Size')

        self.bar_rects_male = self.ax2.barh(range(10), [0] * 10, align='center', height=0.5, color='blue', alpha=0.6, label='Males')
        self.bar_rects_female = self.ax2.barh(range(10), [0] * 10, align='center', height=0.5, color='green', alpha=0.6, label='Females')
        self.ax2.set_xlim(-50, 50)
        self.ax2.legend()
        self.ax2.set_yticks(range(10))
        self.ax2.set_yticklabels([f'{i*10}-{i*10+9}' for i in range(10)])
        self.ax2.set_xlabel('Population')
        self.ax2.set_title('Age Distribution')

        return self.line1, *self.bar_rects_male, *self.bar_rects_female

    def update(self, frame):
        self.x_data.append(village.INFO["year"])
        self.y_data.append(village.INFO["Population Size"])
        self.line1.set_data(self.x_data, self.y_data)

        age_distribution_male, age_distribution_female = village.get_age_distribution()
        for rect, h in zip(self.bar_rects_male, age_distribution_male):
            rect.set_width(h)
        for rect, h in zip(self.bar_rects_female, age_distribution_female):
            rect.set_width(h)

        return self.line1, *self.bar_rects_male, *self.bar_rects_female

    def show(self):
        plt.show(block=False)

# 初始化村庄
village = Village(100)
current_year_info = dict(village.INFO)
last_year_info = None


# pygame loop
animating = True
while animating:
    year = f"{village.INFO['year']:.3f}"

    if year[-3:] in ["999", "000", "001"]:  # 每年更新一次
        last_year_info = current_year_info
        current_year_info = dict(village.INFO)
        village.INFO["population change"] = current_year_info["Population Size"] - last_year_info["Population Size"]

    SCREEN.fill(COLORS["background"])

    village.stimulate_day()

    for p in village.population:
        p.age_up()
        p.work()
        p.move()
        p.show()

    for p in village.population:
        if p.health <= 0:
            village.population.remove(p)
            village.INFO["Population Size"] -= 1
            village.INFO["dead"] += 1

        nearby_people = village.get_nearby_people(p)
        for other in nearby_people:
            if math.sqrt((p.x - other.x)**2 + (p.y - other.y)**2) < 5 and p != other:
                if p.health > 60 and p.age >= 18 and other.age >= 18 and p.age <= 60 and other.age <= 60:
                    if p.sex == "female":
                        if other.sex == "male":
                            if p.last_reproduce is not None:
                                if random.random() < 0.1 and village.INFO["year"] - p.last_reproduce > 1:
                                    p.reproduction()
                                    p.last_reproduce = village.INFO["year"]
                                    if random.random() < 0.01:
                                        p.change_health(-100)
                                        village.INFO["dead"] += 1
                            if p.last_reproduce is None:
                                random.random() < 0.1
                                p.reproduction()
                                p.last_reproduce = village.INFO["year"]
                                if random.random() < 0.01:
                                    p.change_health(-100)
                                    village.INFO["dead"] += 1

        p.health += 0.05

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            animating = False
        if event.type == pygame.KEYDOWN:
            # if press key m show dynamic chart
            if event.key == pygame.K_m:
                count += 1

                if count % 2 == 1:
                    # 创建动态图表
                    chart = DynamicChart()
                    anim = animation.FuncAnimation(chart.fig, chart.update, init_func=chart.create_chart, blit=True)
                    chart.show()

                else:
                    plt.close()


pygame.quit()
plt.close()
