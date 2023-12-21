from aocd import get_data
from collections import defaultdict

data = get_data(day=20,year=2023)
example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

class Module:
    def __init__(self, name, debug):
        self.name = name
        self.connections = []
        self.pulses_sent = {'low':0, 'high':0}
        self.debug = debug

    def __repr__(self):
        return self.name

    def add_connection(self, connection):
        self.connections.append(connection)

    def receive(self, connection, pulse):
        if self.debug:
            print(f'Received {pulse} from {connection}')
        return []

class FlipFlop(Module):
    def __init__(self, name,debug):
        super().__init__(name,debug)
        self.on = False

    def __repr__(self):
        return f'{self.name}, {self.on}'

    def receive(self, connection, pulse):
        to_process = []
        if pulse == 'low':
            return_pulse = 'low' if self.on else 'high'
            self.on = not self.on
            for c in self.connections:
                if self.debug:
                    print(self, '-', return_pulse, '->', c)
                self.pulses_sent[return_pulse] += 1
                to_process.append([self, c, return_pulse])
        return to_process

class Conjunction(Module):
    def __init__(self, name,debug):
        super().__init__(name,debug)
        self.last_received = {}

    def add_connection(self, connection):
        self.connections.append(connection)

    def receive(self, connection, pulse):
        to_process = []
        self.last_received[connection.name] = pulse
        if all([v == 'high' for v in self.last_received.values()]):
            return_pulse = 'low'
        else:
            return_pulse = 'high'
        for c in self.connections:
            if self.debug:
                print(self, '-', return_pulse, '->', c)
            self.pulses_sent[return_pulse] += 1
            to_process.append([self, c, return_pulse])
        return to_process

class Broadcast(Module):
    def __init__(self, name,debug):
        super().__init__(name,debug)

    def receive(self, connection, pulse):
        to_process = []
        for c in self.connections:
            if self.debug:
                print(self, '-', pulse, '->', c)
            self.pulses_sent[pulse] += 1
            to_process.append([self, c, pulse])
        return to_process

def parse_input(data,debug=False):
    modules = {}
    connections = defaultdict(list)
    for row in data.split('\n'):
        module, rconn = row.split(' -> ')
        if module == 'broadcaster':
            name = module
            modules[name] = Broadcast(name,debug)
        elif module[0] == '%':
            name = module[1:]
            modules[name] = FlipFlop(name,debug)
        elif module[0] == '&':
            name = module[1:]
            modules[name] = Conjunction(name,debug)
        else:
            name = module
            modules[name] = Module(name,debug)
        connections[name] += rconn.split(', ')
    for name, conns in connections.items():
        for conn in conns:
            cur_mod = modules.get(conn)
            if cur_mod is None:
                modules[conn] = Module(conn,debug)
            cur_mod = modules[conn]
            modules[name].add_connection(modules[conn])
            if isinstance(cur_mod, Conjunction):
                cur_mod.last_received[name] = 'low'
    return modules

def part_one(data,cycle_length=1000,debug=False):
    modules = parse_input(data,debug=debug)
    pulses_sent = {'low': 0, 'high': 0}
    for c in range(cycle_length):
        to_process = [[None, modules['broadcaster'], 'low']]
        pulses_sent['low'] += 1
        while to_process:
            src, dest, pulse = to_process.pop(0)
            next_steps = dest.receive(src, pulse)
            to_process += next_steps

    for m in modules.values():
        for p, n in m.pulses_sent.items():
            pulses_sent[p] += n
    answer = pulses_sent['low']*pulses_sent['high']
    return answer, pulses_sent

example_two = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

part_one_example_answer, pulses_sent = part_one(example,1000,False)
part_one_example_two_answer, pulses_sent = part_one(example_two,1000,False)
part_one_answer, _ = part_one(data,1000,False)