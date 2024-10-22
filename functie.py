prio = {'+' : 0, '-' : 0, '*' : 1, '/' : 1, '^' : 2, '(' : -1, '-u': 0}

def is_close_to_zero(number, tolerance = 1e-8):
    return abs(number) <= tolerance

operands = []
operators = []
e = 2.7182

def translate_function(line):

    line = line.replace(' ', '')

    for i, c in enumerate(line):
        if c in 'xe.' or c.isdigit():
            if i != 0 and (c.isdigit() or c == '.'):
                if line[i - 1].isdigit() or line[i - 1] == '.':
                    operands[-1]['value'] += c
                else:
                    operands.append({'value' : c})
            else:
                operands.append({'value' : c})
        if c in '^*/+-':
            isunar = False
            if c == '-':
                if i == 0 or line[i - 1] == '(':
                    operators.append('-u')
                    operands.append({'value' : '0'})
                    isunar = True
            if operators != [] and (not isunar):
                while prio[c] <= prio[operators[-1]]:
                    d = {}
                    d['node'] = operators.pop()
                    d['right'] = operands.pop()
                    d['left'] = operands.pop()
                    operands.append(d)
                    if operators == []:
                        break
            if not isunar:
                operators.append(c)
        if c == '(':
            operators.append(c)
        if c == ')':
            while operators[-1] != '(':
                d = {}
                d['node'] = operators.pop()
                d['right'] = operands.pop()
                d['left'] = operands.pop()
                operands.append(d)
            operators.pop()

    while operators != []:
        d = {}
        d['node'] = operators.pop()
        d['right'] = operands.pop()
        d['left'] = operands.pop()
        operands.append(d)

def prec(d, level):
    print(" " * level, d['node'] if 'node' in d else d['value'])
    if 'left' in d:
        prec(d['left'], level + 1)
    if 'right' in d:
        prec(d['right'], level + 1)

def vale(d, value):
    if 'value' in d:
        if d['value'][0].isdigit():
            return float(d['value'])
        if d['value'][0] == 'x':
            return value
        if d['value'][0] == 'e':
            return e
    val_l = vale(d['left'], value)
    val_r = vale(d['right'], value)
    try:
        if d['node'] == '+':
            return val_l + val_r
        if d['node'] == '-' or d['node'] == '-u':
            return val_l - val_r
        if d['node'] == '/':
            if is_close_to_zero(val_r):
                return None
            return val_l / val_r
        if d['node'] == '^':
            if val_l < 0 and int(val_r) != float(val_r):
                return None
            return val_l ** val_r
        if d['node'] == '*':
            return val_l * val_r
    except:
        return None

#print("Introduce o valoare in care sa evaluezi functia: ", functie)
'''val = input()
nval = ''
if 'sqrt' in val:
    for c in val:
        if c.isdigit():
            nval += c
    val = float(nval) ** 0.5
print(val)'''

#print("Valoarea lui f(x) in: ", val, " este ", vale(operands[-1], float(val)))
    


#print(d['left']['left'])
#print(d)

#print(operands[-1])
#prec(operands[-1], 0)
        

        
    