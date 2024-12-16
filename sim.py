from mesa import Agent, Model
import random

def clamp(value, min_val, max_value):
    return round(max(min_val, min(max_value, value)), 2)

class LifeForm(Agent):
    health = 100
    q_values = {
        "healthy_food": 0.5,
        "poisened_food": 0.5,
            }
    learning_rate = 0.01

    def __init__(self, model):
        super().__init__(model)

    def mod_health(self, value: int):
        self.health = clamp(self.health + value, 0, 100)

    @property
    def alive(self):
        return self.health > 0

    def step(self):
        choice, reward = self.pick_food()

        if reward == 1:
            self.q_values[choice] = clamp(self.q_values[choice] + self.learning_rate, 0, 1)
        elif reward == -1:
            self.q_values[choice] = clamp(self.q_values[choice] - self.learning_rate, 0, 1)

        print(self.health, self.q_values)

        if not self.alive:
            self.remove()

    def pick_food(self):
        choice = random.choices(["healthy_food", "poisened_food"],
                                list(self.q_values.values()), k=1)[0]

        if choice == "healthy_food":
            self.mod_health(10)
            return choice, 1
        elif choice == "poisened_food":
            self.mod_health(-10)
            return choice, -1



class World(Model):
    def __init__(self):
        super().__init__()
        life = LifeForm(self)
        self.agents.add(life)

    def step(self):
        self.agents.shuffle_do("step")


world = World()

i = 0

while True:
    i += 1
    world.step()
    population = len(world.agents)
    print(f"day {i} populaiton {population}")

    if i == 20 or population == 0:
        break
