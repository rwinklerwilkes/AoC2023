from aocd import get_data
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
        self.m,self.b = find_slope_intercept(x,y,z,dx,dy,dz)

    def __repr__(self):
        return f'{self.x}, {self.y}, {self.z} @ {self.dx}, {self.dy}, {self.dz}'

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

def find_slope_intercept(x,y,z,dx,dy,dz):
    m = dy/dx
    b = y-m*x
    return m,b

def find_intersection(line1, line2, xlims, ylims):
    if line1.m==line2.m:
        return False
    x = (line2.b-line1.b)/(line1.m-line2.m)
    y = line1.m*x + line1.b
    #Backtest
    t1 = (x-line1.x)/line1.dx
    t2 = (x - line2.x) / line2.dx
    if x >= xlims[0] and x <= xlims[1] and y >= ylims[0] and y <= ylims[1] and t1 >= 0 and t2 >= 0:
        return True
    else:
        return False

def part_one(data, xlims, ylims):
    parsed_data = parse_data(data)
    answer = 0
    for i in parsed_data:
        for j in parsed_data:
            if i == j:
                continue
            else:
                if find_intersection(i,j,xlims,ylims):
                    answer += 1
                    # print(i, j)
    answer /= 2
    return answer

part_one_example_answer = part_one(example, (7,27), (7,27))
part_one_answer = part_one(data, (200000000000000, 400000000000000), (200000000000000, 400000000000000))