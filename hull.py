#! /usr/bin/python

import math
import sys

def set_correct_normal(possible_internal_points,plane): #Make the orientation of Normal correct
	for point in possible_internal_points:
		dist = dotProduct(plane.normal,point - plane.pointA)
		if(dist != 0) :
			if(dist > 10**-10):
				plane.normal.x = -1*plane.normal.x
				plane.normal.y = -1*plane.normal.y
				plane.normal.z = -1*plane.normal.z
				return         

def printV(vec): # Print points
	print vec.x, vec.y, vec.z

def cross(pointA, pointB): # Cross product
	x = (pointA.y*pointB.z) - (pointA.z*pointB.y)
	y = (pointA.z*pointB.x) - (pointA.x*pointB.z)
	z = (pointA.x*pointB.y) - (pointA.y*pointB.x)
	return Point(x, y, z)

def dotProduct(pointA, pointB): # Dot product
	return (pointA.x*pointB.x + pointA.y*pointB.y + pointA.z*pointB.z)

def checker_plane(a, b): #Check if two planes are equal or not

	if ((a.pointA.x == b.pointA.x) and (a.pointA.y == b.pointA.y) and (a.pointA.z == b.pointA.z)):
		if ((a.pointB.x == b.pointB.x) and (a.pointB.y == b.pointB.y) and (a.pointB.z == b.pointB.z)):	
			if ((a.pointC.x == b.pointC.x) and (a.pointC.y == b.pointC.y) and (a.pointC.z == b.pointC.z)):	
				return True

		elif ((a.pointB.x == b.pointC.x) and (a.pointB.y == b.pointC.y) and (a.pointB.z == b.pointC.z)):	
			if ((a.pointC.x == b.pointB.x) and (a.pointC.y == b.pointB.y) and (a.pointC.z == b.pointB.z)):	
				return True
				
	if ((a.pointA.x == b.pointB.x) and (a.pointA.y == b.pointB.y) and (a.pointA.z == b.pointB.z)):
		if ((a.pointB.x == b.pointA.x) and (a.pointB.y == b.pointA.y) and (a.pointB.z == b.pointA.z)):	
			if ((a.pointC.x == b.pointC.x) and (a.pointC.y == b.pointC.y) and (a.pointC.z == b.pointC.z)):	
				return True

		elif ((a.pointB.x == b.pointC.x) and (a.pointB.y == b.pointC.y) and (a.pointB.z == b.pointC.z)):	
			if ((a.pointC.x == b.pointA.x) and (a.pointC.y == b.pointA.y) and (a.pointC.z == b.pointA.z)):	
				return True

	if ((a.pointA.x == b.pointC.x) and (a.pointA.y == b.pointC.y) and (a.pointA.z == b.pointC.z)):
		if ((a.pointB.x == b.pointA.x) and (a.pointB.y == b.pointA.y) and (a.pointB.z == b.pointA.z)):	
			if ((a.pointC.x == b.pointB.x) and (a.pointC.y == b.pointB.y) and (a.pointC.z == b.pointB.z)):	
				return True

		elif ((a.pointB.x == b.pointC.x) and (a.pointB.y == b.pointC.y) and (a.pointB.z == b.pointC.z)):	
			if ((a.pointC.x == b.pointB.x) and (a.pointC.y == b.pointB.y) and (a.pointC.z == b.pointB.z)):	
				return True			
			
	return False

def checker_edge(a, b): # Check if 2 edges have same 2 vertices

	if ((a.pointA == b.pointA)and(a.pointB == b.pointB)) or ((a.pointB == b.pointA)and(a.pointA == b.pointB)):
		return True

	return False
		
class Edge: # Make a object of type Edge which have two points denoting the vertices of the edges
	def __init__(self,pointA,pointB):
		self.pointA = pointA
		self.pointB = pointB

	def __str__(self):
		string = "Edge"
		string += "\n\tA: "+ str(self.pointA.x)+","+str(self.pointA.y)+","+str(self.pointA.z)
		string += "\n\tB: "+ str(self.pointB.x)+","+str(self.pointB.y)+","+str(self.pointB.z)
		return string

	def __hash__(self):
		return hash((self.pointA,self.pointB))

	def __eq__(self,other):
		# print "comparing Edges"
		return checker_edge(self,other)

class Point: #Point class denoting the points in the space
	def __init__(self, x=None, y=None, z=None):
		self.x = x
		self.y = y
		self.z = z

	def __sub__(self, pointX):
		return	Point(self.x - pointX.x, self.y - pointX.y, self.z - pointX.z)

	def __add__(self, pointX):
		return	Point(self.x + pointX.x, self.y + pointX.y, self.z + pointX.z)		

	def length(self):
		return math.sqrt(self.x**2 + self.y**2 + self.z**2) 

	def __str__(self):
		return str(self.x)+","+str(self.y)+","+str(self.z)

	def __hash__(self):
		return hash((self.x,self.y,self.z))

	def __eq__(self,other):
		# print "Checking equality of Point"
		return (self.x==other.x) and(self.y==other.y) and(self.z==other.z) 	

class Plane: # Plane class having 3 points for a triangle
	def __init__(self, pointA, pointB, pointC):
		self.pointA = pointA
		self.pointB = pointB
		self.pointC = pointC
		self.normal = None
		self.distance = None
		self.calcNorm()
		self.to_do = set()	
		self.edge1 = Edge(pointA, pointB)
		self.edge2 = Edge(pointB, pointC)
		self.edge3 = Edge(pointC, pointA)

	def calcNorm(self):
		point1 = self.pointA - self.pointB
		point2 = self.pointB - self.pointC
		normVector = cross(point1,point2)
		length = normVector.length()
		normVector.x = normVector.x/length
		normVector.y = normVector.y/length
		normVector.z = normVector.z/length
		self.normal = normVector
		self.distance = dotProduct(self.normal,self.pointA)

	def dist(self, pointX):
		return (dotProduct(self.normal,pointX - self.pointA))

	def get_edges(self):
		return [self.edge1, self.edge2, self.edge3]

	def calculate_to_do(self, temp=None):    
		if (temp != None):
			for p in temp:
				dist = self.dist(p)
				if dist > 10**(-10):
					self.to_do.add(p)

		else:	
			for p in points:
				dist = self.dist(p)
				if dist > 10**(-10):
					self.to_do.add(p)

	def __eq__(self,other):
		# print 'Checking Plane Equality'
		return checker_plane(self,other)

	def __str__(self):
		string =  "Plane : "
		string += "\n\tX: "+str(self.pointA.x)+","+str(self.pointA.y)+","+str(self.pointA.z)
		string += "\n\tY: "+str(self.pointB.x)+","+str(self.pointB.y)+","+str(self.pointB.z)
		string += "\n\tZ: "+str(self.pointC.x)+","+str(self.pointC.y)+","+str(self.pointC.z)
		string += "\n\tNormal: "+str(self.normal.x)+","+str(self.normal.y)+","+str(self.normal.z)
		return string

	def __hash__(self):
		return hash((self.pointA,self.pointB,self.pointC))

def calc_horizon(visited_planes,plane,eye_point,edge_list): # Calculating the horizon for an eye to make new faces
	if (plane.dist(eye_point) > 10**-10):
		visited_planes.append(plane)
		edges = plane.get_edges()
		for edge in edges:
			neighbour = adjacent_plane(plane,edge)
			if (neighbour not in visited_planes):
				result = calc_horizon(visited_planes,neighbour,eye_point,edge_list)
				if(result == 0):
					edge_list.add(edge)

		return 1
	
	else:
		return 0
				
def adjacent_plane(main_plane,edge): # Finding adjacent planes to an edge
	for plane in list_of_planes:
		edges = plane.get_edges()
		if (plane != main_plane) and (edge in edges):
			return plane


def distLine(pointA, pointB, pointX): #Calculate the distance of a point from a line
	vec1 = pointX - pointA
	vec2 = pointX - pointB
	vec3 = pointB - pointA
	vec4 = cross(vec1, vec2)
	if vec3.length() == 0:
		return None

	else:
		return vec4.length()/vec3.length()

def max_dist_line_point(pointA, pointB): #Calculate the maximum distant point from a line for initial simplex
	maxDist = 0;
	for point in points:
		if (pointA != point) and (pointB != point):
			dist = abs(distLine(pointA,pointB,point))
			if dist>maxDist:
				maxDistPoint = point
				maxDist = dist

	return maxDistPoint

def max_dist_plane_point(plane): # Calculate the maximum distance from the plane
	maxDist = 0
	
	for point in points:
		dist = abs(plane.dist(point))
		if (dist > maxDist):
			maxDist = dist
			maxDistPoint = point

	return maxDistPoint

def find_eye_point(plane, to_do_list): # Calculate the maximum distance from the plane
	maxDist = 0
	for point in to_do_list:
		dist = plane.dist(point)
		if (dist > maxDist):
			maxDist = dist
			maxDistPoint = point

	return maxDistPoint    

def initial_dis(p, q): # Gives the Euclidean distance
	return math.sqrt((p.x-q.x)**2+(p.y-q.y)**2+(p.z-q.z)**2)

def initial_max(now): # From the extreme points calculate the 2 most distant points
	maxi = -1
	found = [[], []]
	for i in xrange(6):
		for j in xrange(i+1, 6):	
			dist = initial_dis(now[i], now[j])
			if dist > maxi:
				found = [now[i], now[j]]

	return found	

def initial(): # To calculate the extreme points to make the initial simplex

	x_min_temp = 10**9
	x_max_temp = -10**9
	y_min_temp = 10**9
	y_max_temp = -10**9
	z_min_temp = 10**9
	z_max_temp = -10**9
	for i in xrange(num): 
		if points[i].x > x_max_temp:
			x_max_temp = points[i].x
			x_max = points[i]

		if points[i].x < x_min_temp:
			x_min_temp = points[i].x
			x_min = points[i]

		if points[i].y > y_max_temp:
			y_max_temp = points[i].y
			y_max = points[i]

		if points[i].y < y_min_temp:
			y_min_temp = points[i].y
			y_min = points[i]

		if points[i].z > z_max_temp:
			z_max_temp = points[i].z
			z_max = points[i]

		if points[i].z < z_min_temp:
			z_min_temp = points[i].z
			z_min = points[i]	

	return (x_max, x_min, y_max, y_min, z_max, z_min)						

points = [] # List to store the points

if len(sys.argv) < 2:
	print "Few arguments. See README for help"
	sys.exit()

try: # Open the input and store it in points list
	data = open(sys.argv[1], "r")
	num = int(data.readline())
	for line in data:
		a = map(float, line.split())
		points.append(Point(a[0], a[1], a[2]))

	if num < 4:
		print "Less than 4 points so 1D or 2D"
		sys.exit()

finally:
	data.close()	

try:
	extremes = initial() # calculate the extreme points for every axis.
	initial_line = initial_max(extremes) # Make the initial line by joining farthest 2 points
	third_point = max_dist_line_point(initial_line[0], initial_line[1]) # Calculate the 3rd point to make a plane
	first_plane = Plane(initial_line[0], initial_line[1], third_point) # Make the initial plane by joining 3rd point to the line

	fourth_point = max_dist_plane_point(first_plane) # Make the fourth plane to make a tetrahedron
except:
	print "Figure either in 2D or 3D"
	sys.exit()

possible_internal_points = [initial_line[0],initial_line[1],third_point,fourth_point] # List that helps in calculating orientation of point

second_plane = Plane(initial_line[0], initial_line[1], fourth_point) # The other planes of the tetrahedron
third_plane = Plane(initial_line[0], fourth_point, third_point)
fourth_plane = Plane(initial_line[1], third_point, fourth_point)

set_correct_normal(possible_internal_points,first_plane) # Setting the orientation of normal correct
set_correct_normal(possible_internal_points,second_plane)
set_correct_normal(possible_internal_points,third_plane)
set_correct_normal(possible_internal_points,fourth_plane)

first_plane.calculate_to_do() # Calculating the to_do list which stores the point for which  eye_point have to be found
second_plane.calculate_to_do()
third_plane.calculate_to_do()
fourth_plane.calculate_to_do()

list_of_planes = [] # List containing all the planes
list_of_planes.append(first_plane)
list_of_planes.append(second_plane)
list_of_planes.append(third_plane)
list_of_planes.append(fourth_plane)

any_left = True # Checking if planes with to do list is over

while any_left:
	any_left = False
	for working_plane in list_of_planes:
		if len(working_plane.to_do) > 0:
			any_left = True
			eye_point = find_eye_point(working_plane, working_plane.to_do) # Calculate the eye point of the face

			edge_list = set()
			visited_planes = []
			
			calc_horizon(visited_planes, working_plane, eye_point, edge_list)  # Calculate the horizon
			
			for internal_plane in visited_planes: # Remove the internal planes
				list_of_planes.remove(internal_plane)

			for edge in edge_list:	# Make new planes
				new_plane = Plane(edge.pointA, edge.pointB, eye_point)
				set_correct_normal(possible_internal_points,new_plane)

				temp_to_do = set()
				for internal_plane in visited_planes:
					temp_to_do = temp_to_do.union(internal_plane.to_do)

				new_plane.calculate_to_do(temp_to_do)
				
				list_of_planes.append(new_plane)

final_vertices = set()
for plane in list_of_planes:
	final_vertices.add(plane.pointA)
	final_vertices.add(plane.pointB)
	final_vertices.add(plane.pointC)

try: # Open the output file
	data1 = open("data/"+sys.argv[1].split('.')[0]+".out", "w")
	data1.write(str(len(final_vertices)) + '\n')
	for point in final_vertices:
		data1.write(str(point.x) +' '+ str(point.x) +' '+ str(point.x) + '\n')

finally:
	data1.close()	
