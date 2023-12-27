from aocd import get_data
import numpy as np
import re

data = get_data(day=24, year=2023)
example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""

class Line:
    def __init__(self, x,y,z,dx,dy,dz):
        self.x = x
        self.y =y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.m,self.b = self.find_slope_intercept()
        self.ax, self.ay, self.az = 0,0,0

    def __repr__(self):
        return f'{self.x}, {self.y}, {self.z} @ {self.dx}, {self.dy}, {self.dz}'

    def find_slope_intercept(self):
        if self.dx != 0:
            m = self.dy / self.dx
        else:
            m = np.inf
        b = self.y - m * self.x
        return m, b

    def change_acc(self, axx, ayy, azz):
        #Express velocity and acceleration in window defined by other rock
        #So, if other rock is traveling at 3 mph and this at 2 mph, we account for this in relation to velocity here
        #And then use new acceleration in place of existing - now velocity and acceleration in frame of reference
        #to other acceleration
        self.dx -= axx - self.ax
        self.dy -= ayy - self.ay
        self.dz -= azz - self.az
        self.m, self.b = self.find_slope_intercept()
        self.ax, self.ay, self.az = axx, ayy, azz

    def find_intersection(self, other, xlims=(-np.inf,np.inf), ylims=(-np.inf,np.inf)):
        if self.m == other.m:
            return False, None, None
        if self.m == np.inf:
            x = self.x
            y = other.m * (x - other.x) + other.y
        elif other.m == np.inf:
            x = other.x
            y = self.m * (x - self.x) + self.y
        else:
            x = (other.b - self.b) / (self.m - other.m)
            y = self.m * x + self.b
        # Backtest
        t1 = np.sign(x-self.x) == np.sign(self.dx)
        t2 = np.sign(x - other.x) == np.sign(other.dx)
        if x >= xlims[0] and x <= xlims[1] and y >= ylims[0] and y <= ylims[1] and t1 and t2:
            return True, x, y
        else:
            return False, None, None

    def get_time(self,p):
        ret_val = 0
        if self.dx == 0:
            ret_val = (p[1] - self.y)/self.dy
        else:
            ret_val = (p[0] - self.x) / self.dx
        return ret_val

    def get_z(self, other, intersection_point):
        t_this = self.get_time(intersection_point)
        t_other = other.get_time(intersection_point)
        if t_this == t_other:
            return None
        else:
            return (self.z - other.z + t_this*self.dz - t_other*other.dz)/(t_this-t_other)


def parse_data(data):
    parsed_data = []
    for row in data.split('\n'):
        row_out = []
        for match in re.finditer('[\d\-]+', row):
            s,e = match.start(),match.end()
            row_out.append(int(row[s:e]))
        l = Line(*row_out)
        parsed_data.append(l)
    return parsed_data

def part_one(data, xlims, ylims):
    parsed_data = parse_data(data)
    answer = 0
    for i in parsed_data:
        for j in parsed_data:
            if i == j:
                continue
            else:
                inter, _, _ = i.find_intersection(j,xlims,ylims)
                if inter:
                    answer += 1
                    # print(i, j)
    answer /= 2
    return int(answer)

part_one_example_answer = part_one(example, (7,27), (7,27))
part_one_answer = part_one(data, (200000000000000, 400000000000000), (200000000000000, 400000000000000))


def part_two(data, debug=False):
    parsed_data = parse_data(data)
    N = 0
    while True:
        for X in range(N + 1):
            Y = N - X
            for negX in (-1, 1):
                for negY in (-1, 1):
                    dX = X * negX
                    dY = Y * negY
                    l1 = parsed_data[0]
                    l1.change_acc(dX, dY, 0)
                    inter = None
                    for l2 in parsed_data[1:]:
                        l2.change_acc(dX, dY, 0)
                        intersects, px, py = l1.find_intersection(l2)
                        pt = (px, py)
                        if pt is None:
                            break
                        if inter is None:
                            inter = pt
                            continue
                        if pt != inter:
                            # if debug: print(f'v {H2} — NOT SAME P {p}')
                            break
                        # if debug: print(f'v {H2} — continuing{p}')
                    if pt is None or pt != inter:
                        continue
                    # if debug: print(f'FOUND COMMON INTERSECTION {p}')
                    # we escaped intersecting everything with H1 with a single valid XY point!
                    print(f'potential intersector found with v=<{dX},{dY},?>' \
                          + f', p=<{inter[0]},{inter[1]},?>')
                    dZ = None
                    l1 = parsed_data[0]
                    # print(f'v {H1}')
                    for l2 in parsed_data[1:]:
                        nZ = l1.get_z(l2, inter)
                        if dZ is None:
                            # print(f'first aZ is {aZ} from {H2}')
                            dZ = nZ
                            continue
                        elif nZ != dZ:
                            print(f'invalidated! by {nZ} from {H1}')
                            return
                    if dZ == nZ:
                        l = parsed_data[0]
                        Z = l.z + l.get_time(inter) * (l.dz - dZ)
                        print(
                            f'found solution :) v=<{dX},{dY},{dZ}>, p=<{inter[0]},{inter[1]},{Z}>, s = {Z + inter[0] + inter[1]}')
                        return

        N += 1

part_two(example)
part_two(data)