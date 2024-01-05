import math

file_name_csv = "Data/N=10_W=10_H=8_normal_0.csv"

N = 10  # number of targets
W = 10  # width
H = 8   # height
R = 3  # radius of sensor

def read_data(path):
    coordinates = []
    demand = []
    with open(path, 'r') as f:
        # Read the header line
        header = f.readline()

        for _ in range(N):
            line = f.readline().strip().split(',')
            x, y, q = map(float, line)
            coordinates.append((x, y))
            demand.append(int(q))

    return coordinates, demand

def get_distances(X, Y):
    return math.sqrt(pow(X[0]-Y[0], 2)+pow(X[1]-Y[1], 2))

def find_positions(coordinates):
    unique_positions = set()
    targetted = []
    check = [0]*N
    isolation = []
    for i in range(len(coordinates)-1):
        for j in range(i+1, len(coordinates)):
            if get_distances(coordinates[i], coordinates[j]) <= 2*R:
                check[i]+=1
                check[j]+=1
                
                midpoint = ((coordinates[i][0] + coordinates[j][0]) / 2, (coordinates[i][1] + coordinates[j][1]) / 2)
                angle = math.atan2(coordinates[j][1] - coordinates[i][1], coordinates[j][0] - coordinates[i][0])

                x_p1 = round(midpoint[0] + R * math.cos(angle + math.pi/2), 6)
                y_p1 = round(midpoint[1] + R * math.sin(angle + math.pi/2), 6)

                x_p2 = round(midpoint[0] - R * math.cos(angle + math.pi/2), 6)
                y_p2 = round(midpoint[1] - R * math.sin(angle + math.pi/2), 6)

                if 0 <= x_p1 <= W and 0 <= y_p1 <= H:
                    unique_positions.add((x_p1, y_p1))
                    targetted.append([i, j])
                if 0 <= x_p2 <= W and 0 <= y_p2 <= H:
                    unique_positions.add((x_p2, y_p2))
                    targetted.append([i, j])
    for i in range(len(coordinates)):
        if check[i] == 0: isolation.append(i)

    for i in range(len(list(unique_positions))):
        for j in range(len(coordinates)):
            if j not in targetted[i] and j not in isolation: 
                if get_distances(list(unique_positions)[i], coordinates[j]) <= R:
                    targetted[i].append(j)
    
    a = []
    for j in range(len(coordinates)):
        temp = [0]*len(list(unique_positions))
        a.append(temp)
        for i in range(len(list(unique_positions))):
            if j in targetted[i]:
                a[j][i] = 1
    
    return list(unique_positions), a, isolation

