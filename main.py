import copy
import random
import matplotlib.pyplot as plt


# to random create N points within X and Y limits
def createPoints(n,maxX,maxY):
    points = [[0 for _ in range(2)] for _ in range(n)]
    # first point is 0 , 0
    # the rest are randoms
    for i in range(1,n):
        while True:
            point = [random.randrange(maxX), random.randrange(maxY)]
            if point not in points:
                points[i] = point
                break
    return points

# to random create a path of N numbers
def createPath(n):
    path = []
    # we start a the 0,0 block
    path.append(0)
    for i in range(1,n):
        path.append(i)
    random.shuffle(path[1:])
    return path

# the 2d distance of 2 points
def distanceOfPoints(x,y):
    d = (x[0] - y[0])**2 + (x[1] - y[1])**2
    return d ** 0.5

# the distance of the path
def distanceOfPath(n, path, points):
    d =0.0
    for i in range(n-1):
        d = d + distanceOfPoints(points[path[i]] , points[path[i+1]])
    return d

# to find the M percentege of the paths with the least distance
def calculateBestPaths(m,paths,distance):
    # sort the paths and the distances according to min distance
    for i in range(n):
        mid = i
        for j in range(i+1,n):
            if distance[mid] > distance[j]:
                mid = j
        # swap the distances and the paths
        distance[i] , distance[mid] = distance[mid] , distance[i]
        paths[i] , paths[mid] = paths[mid] , paths[i]

    # return the M*N best paths
    return paths[:int(m*n)]

# 2 points swap path mutation
def swapMutation(path,p1,p2):
    temp = path[p1]
    path[p1] = path[p2]
    path[p2] = temp
    return path

# 4 points swap path mutation
def swapMutation2(path,p1,p2,p3,p4):
    temp = path[p1]
    path[p1] = path[p2]
    path[p2] = temp
    temp = path[p3]
    path[p3] = path[p4]
    path[p4] = temp

    return path

# it will compute from M*K paths a set of K paths
def mutatePaths(k,paths):
    newPaths = []

    while len(newPaths) < k:
        x1 = random.randrange(n-1)+1 # 1-9
        x2 = random.randrange(n-1) + 1  # 1-9
        # we will create 4 paths from swapping the x1 and x2 points from the original paths
        for i in range(len(paths)):
            newPaths.append(swapMutation(copy.deepcopy(paths[i]), x1, x2))

        x1 = random.randrange(n - 1) + 1
        x2 = random.randrange(n - 1) + 1
        x3 = random.randrange(n - 1) + 1
        x4 = random.randrange(n - 1) + 1
        # we will create 4 paths from swapping the x1,x2 and x3,x4 points from the original paths
        for i in range(len(paths)):
            newPaths.append(swapMutation2(copy.deepcopy(paths[i]), x1, x2, x3, x4))

    # return the K new paths
    return newPaths[:k]






# the number of points the salesman wants to visit
n = 10

# the max X and Y of the coordinates
maxX = 10
maxY = 10

#points = createPoints(n,maxX,maxY)

# we will use a standard set of points for example
points = [[0,0],[7,4],[2,7],[3,6],[1,5],[6,3],[2,7],[8,7],[4,6],[6,4]]
#points = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7],[8,8],[9,9]]



# we want to visit each of these points starting from 0 0 with the least distance possible
# normally this problem needs O(n!) to be solved
# We will use a genetic algorithm
# We will create K random paths, we will keep the M percentege of them who have the best distance
# from this paths we will mutate them to have another set of K paths and repeat
# We save the best path each time so after some iterations we can be pretty close to a good solution

# the number K of paths we will have at each set
k = 20

# the percentege M of the fittest path we will use for mutations
m = 0.4

# the array of paths and their distances
paths = []
distances = []

# create the K paths and computing their distances
for i in range(k):
    paths.append(createPath(n))
    distances.append(distanceOfPath(n,paths[i],points))

# number of iterations we want
iterations = 500

# the best path and it's distance, we start from the first path
minPath = paths[0]
minDistance = distanceOfPath(n,paths[0],points)



# we start the iterations
for _ in range(iterations):
    # find the best paths
    bestPaths = calculateBestPaths(m, copy.deepcopy(paths), distances)
    # from best paths calculate the mutations
    paths = mutatePaths(k,copy.deepcopy(bestPaths))
    #calculate the distance and compare to the min distance
    for i in range(k):
        distances[i] = distanceOfPath(n, paths[i], points)
        if distances[i] < minDistance:
            minDistance = distances[i]
            minPath = paths[i]

# the complexity of the genetic algorithm iterations *( n^2 (to find best paths) + k (to mutate) + k(to find min distance))
# for n = 10 and iterations = 500 we have a complexity of O(5.000)
# which is better compared to n! for n > 6

print("The optimal path is ")
for i in range(n):
    print(points[minPath[i]])

print("and the minimum distance ",minDistance)

x=[]
y=[]

for i in range(n):
    x.append(points[minPath[i]][0])
    y.append(points[minPath[i]][1])

# plot the path
plt.plot(x,y,linewidth=2)

x=[]
y=[]
# plot the points
for i in range(n):
    x.append(points[i][0])
    y.append(points[i][1])

plt.scatter(x,y,c='red')

plt.title("Shortest path according to the genetic algorithm")
plt.grid(True)
plt.show()
