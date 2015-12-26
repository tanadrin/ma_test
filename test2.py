import pyglet
import sys
import random

#Images for displaying the grid of cells
square0 = pyglet.resource.image('square0.jpg')
square1 = pyglet.resource.image('square1.jpg')
square2 = pyglet.resource.image('square2.jpg')
square3 = pyglet.resource.image('square3.jpg')
square4 = pyglet.resource.image('square4.jpg')
square5 = pyglet.resource.image('square5.jpg')
sol_tracker_5000 = 1
dying_sols = {}
spawning_sols = {}
moving_sols = {}

window = pyglet.window.Window()

class MapCell:
	def __init__(self, x, y, pop_size):
		self.x = x
		self.y = y
		self.pop_size = 0
		self.population = {}
	def MoveSol(self, sol, destination):
		self.population.pop(sol.name, None)
		destination.population[sol.name] = sol
		self.pop_size = len(self.population)
		destination.pop_size = len(destination.population)
		
		
	
class Sol:
	def __init__ (self, age, location, name):
		self.age = age
		self.location = location
		self.name = name
		world_map[location].population[self.name] = self
		world_population[self.name] = self
	def do_something(self):
		choice = random.randint(1,3)
		if choice == 1:
			self.schedule_move()
		elif choice == 2:
			if self.age > 3:
				if self.age < 12:
					self.schedule_spawn()
		elif choice == 3:
			if self.age > 12:
				self.schedule_death()
	def schedule_move(self):
		global moving_sols
		moving_sols[self.name] = self
	def move_random (self):
		current_cell = world_map[self.location]
		target_cell = None
		target_x = 0
		target_y = 0
		target_location = ()
		while target_cell is None:
			target_x = random.randint(-1,1)
			target_y = random.randint(-1,1)
			target_location = (self.location[0]+target_x,self.location[1]+target_y)
			target_cell = world_map.get((self.location[0]+target_x,self.location[1]+target_y))
		current_cell.MoveSol(self, target_cell)
		self.location = target_location
	def schedule_spawn(self):
		global spawning_sols
		spawning_sols[self.name] = self
	def spawn_sol(self):
		global sol_tracker_5000
		new_name = str(sol_tracker_5000)
		new_location = self.location
		new_age = 0
		if world_map[self.location].pop_size < 5:
			new_sol = Sol(new_age,new_location,new_name)
			sol_tracker_5000 = sol_tracker_5000 + 1
			world_map[self.location].pop_size = len(world_map[self.location].population)
	def schedule_death(self):
		global dying_sols
		dying_sols[self.name] = self
	def die(self):
		world_population.pop(self.name, None)
		world_map[self.location].population.pop(self.name, None)
		world_map[self.location].pop_size = len(world_map[self.location].population)

		
def create_map():
	for i in range(0, size_x):
		for j in range(0, size_y):
			world_map[(i,j)] = MapCell(i,j,0)
	return world_map
			
def main():
	global world_population
	world_population = {}
	global world_map 
	world_map = {}
	global size_x 
	size_x = int(sys.argv[1])
	global size_y 
	size_y = int(sys.argv[2])
	world_map = create_map()
	
def printmap():
	for x in range(0, size_x):
		for y in range (0, size_y):
			index = (x,y)
			print(index, world_map[index].pop_size)
			
@window.event
def on_draw():
	window.clear()
	for x in range(0, size_x):
		for y in range(0, size_y):
			index = (x,y)
			current_cell = world_map[index]
			if current_cell.pop_size == 0:
				square0.blit(x*30, y*30)
			elif current_cell.pop_size == 1:
				square1.blit(x*30, y*30)
			elif current_cell.pop_size == 2:
				square2.blit(x*30, y*30)
			elif current_cell.pop_size == 3:
				square3.blit(x*30, y*30)
			elif current_cell.pop_size == 4:
				square4.blit(x*30, y*30)
			elif current_cell.pop_size > 4:
				square5.blit(x*30, y*30)
				
def update(dt):
	global dying_sols
	global spawning_sols
	global moving_sols
	for s in world_population:
		world_population[s].do_something()
		world_population[s].age = world_population[s].age + 1
	for s in dying_sols:
		dying_sols[s].die()
	for s in spawning_sols:
		spawning_sols[s].spawn_sol()
	for s in moving_sols:
		moving_sols[s].move_random()
	dying_sols = {}
	spawning_sols = {}
pyglet.clock.schedule_interval(update, 1)
				
main()
test_sol = Sol(0,(1,1), "0")
pyglet.app.run()
