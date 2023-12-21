from aocd import get_data
import re

data = get_data(day=19,year=2023)
example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

def parse_workflow(workflow):
    workflow_regex = r'([a-z]{1,})\{(.{1,})\}'
    name, rules = re.match(workflow_regex, workflow).groups()
    rules = rules.split(',')
    return name, rules

def parse_part(part):
    part_regex = '\{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)\}'
    x,m,a,s = re.match(part_regex,part).groups()
    return x,m,a,s

def check_action(action):
    if action == 'A':
        next_action = 'accept'
    elif action == 'R':
        next_action = 'reject'
    else:
        next_action = 'workflow'
    return next_action

#['a<2006:qkq', 'm>2090:A', 'rfg']
def apply_workflow(workflow, part):
    next_action = None
    for rule in workflow:
        if ':' in rule:
            condition, next = rule.split(':')
            pass_check = eval(condition, None, part)
            if pass_check:
                next_action = check_action(next)
                return next, next_action
        else:
            next_action = check_action(rule)
            return rule, next_action

def parse_data(data):
    all_workflows = {}
    workflows, ratings = data.split('\n\n')
    for workflow in workflows.split('\n'):
        name, rules = parse_workflow(workflow)
        all_workflows[name] = rules
    all_parts = []
    for part in ratings.split('\n'):
        x,m,a,s = parse_part(part)
        p = {'x':int(x),'m':int(m),'a':int(a),'s':int(s)}
        all_parts.append(p)
    return all_workflows, all_parts

def run_all_workflows(all_workflows, part):
    finished = False
    workflow = all_workflows['in']
    while not finished:
        next_rule, next_action = apply_workflow(workflow, part)
        if next_action in ('accept','reject'):
            finished = True
            return next_action
        else:
            workflow = all_workflows[next_rule]

def part_one(data):
    all_workflows, all_parts = parse_data(data)
    answer = 0
    for p in all_parts:
        if run_all_workflows(all_workflows, p) == 'accept':
            answer += sum(list(p.values()))
    return answer

part_one_example_answer = part_one(example)
part_one_answer = part_one(data)

from collections import deque

def new_range(op, n, lo, hi):
  if op=='>':
    lo = max(lo, n+1)
  elif op=='<':
    hi = min(hi, n-1)
  elif op=='>=':
    lo = max(lo, n)
  elif op=='<=':
    hi = min(hi, n)
  else:
    assert False
  return (lo,hi)

def new_ranges(var, op, n, xl,xh,ml,mh,al,ah,sl,sh):
  if var=='x':
    xl,xh = new_range(op, n, xl, xh)
  elif var=='m':
    ml,mh = new_range(op, n, ml, mh)
  elif var=='a':
    al,ah = new_range(op, n, al, ah)
  elif var=='s':
    sl,sh = new_range(op, n, sl, sh)
  return (xl,xh,ml,mh,al,ah,sl,sh)

def part_two(data):
    all_workflows, _ = parse_data(data)
    ans = 0
    Q = deque([('in', 1, 4000, 1, 4000, 1, 4000, 1,4000)])
    while Q:
      state, xl,xh,ml,mh,al,ah,sl,sh = Q.pop()
      #print(state, xl, xh, ml, mh, al, ah, sl, sh, ans)
      if xl>xh or ml>mh or al>ah or sl>sh:
        continue
      if state=='A':
        score = (xh-xl+1)*(mh-ml+1)*(ah-al+1)*(sh-sl+1)
        #print(state, xl, xh, ml, mh, al, ah, sl, sh, ans, score)
        ans += score
        continue
      elif state=='R':
        continue
      else:
        rules = all_workflows[state]
        for cmd in rules:
          applies = True
          res = cmd
          if ':' in cmd:
            cond,res = cmd.split(':')
            var = cond[0]
            op = cond[1]
            n = int(cond[2:])
            #print(state, var, op, n, *new_ranges(var, op, n, xl, xh, ml, mh, al, ah,sl, sh))
            Q.append((res, *new_ranges(var, op, n, xl, xh, ml, mh, al, ah,sl, sh)))
            xl,xh,ml,mh,al,ah,sl,sh = new_ranges(var, '<=' if op=='>' else '>=', n, xl, xh, ml, mh, al, ah,sl, sh)
            #print(xl,xh,ml,mh,al,ah,sl,sh)
          else:
            Q.append((res, xl, xh, ml, mh, al, ah, sl, sh))
            break
    print(ans)

part_two_example_answer = part_two(example)
part_two_answer = part_two(data)