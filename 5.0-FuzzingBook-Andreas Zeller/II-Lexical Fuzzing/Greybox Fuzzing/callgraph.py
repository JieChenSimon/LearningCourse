
def print_maze(out, row, col):
    output  = out +"\n"
    c_row = 0
    c_col = 0
    for c in list("""
+-+-----+
|X|     |
| | --+ |
| |   | |
| +-- | |
|     |#|
+-----+-+
"""):
        if c == '\n':
            c_row += 1
            c_col = 0
            output += "\n"
        else:
            if c_row == row and c_col == col: output += "X"
            elif c == "X": output += " "
            else: output += c
            c_col += 1
    return output

def tile_1_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 0)

def tile_1_1(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 1)

def tile_1_2(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 2)

def tile_1_3(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 3)

def tile_1_4(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 4)

def tile_1_5(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 5)

def tile_1_6(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 6)

def tile_1_7(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 7)

def tile_1_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 1, 8)

def tile_2_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 2, 0)

def tile_2_1(input, index):
    if (index == len(input)): return print_maze("VALID", 2, 1)
    elif input[index] == 'L': return tile_2_0(input, index + 1)
    elif input[index] == 'R': return tile_2_2(input, index + 1)
    elif input[index] == 'U': return tile_1_1(input, index + 1)
    elif input[index] == 'D': return tile_3_1(input, index + 1)
    else : return tile_2_1(input, index + 1)

def maze(input):
    return tile_2_1(list(input), 0)

def tile_2_2(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 2, 2)

def tile_2_3(input, index):
    if (index == len(input)): return print_maze("VALID", 2, 3)
    elif input[index] == 'L': return tile_2_2(input, index + 1)
    elif input[index] == 'R': return tile_2_4(input, index + 1)
    elif input[index] == 'U': return tile_1_3(input, index + 1)
    elif input[index] == 'D': return tile_3_3(input, index + 1)
    else : return tile_2_3(input, index + 1)

def tile_2_4(input, index):
    if (index == len(input)): return print_maze("VALID", 2, 4)
    elif input[index] == 'L': return tile_2_3(input, index + 1)
    elif input[index] == 'R': return tile_2_5(input, index + 1)
    elif input[index] == 'U': return tile_1_4(input, index + 1)
    elif input[index] == 'D': return tile_3_4(input, index + 1)
    else : return tile_2_4(input, index + 1)

def tile_2_5(input, index):
    if (index == len(input)): return print_maze("VALID", 2, 5)
    elif input[index] == 'L': return tile_2_4(input, index + 1)
    elif input[index] == 'R': return tile_2_6(input, index + 1)
    elif input[index] == 'U': return tile_1_5(input, index + 1)
    elif input[index] == 'D': return tile_3_5(input, index + 1)
    else : return tile_2_5(input, index + 1)

def tile_2_6(input, index):
    if (index == len(input)): return print_maze("VALID", 2, 6)
    elif input[index] == 'L': return tile_2_5(input, index + 1)
    elif input[index] == 'R': return tile_2_7(input, index + 1)
    elif input[index] == 'U': return tile_1_6(input, index + 1)
    elif input[index] == 'D': return tile_3_6(input, index + 1)
    else : return tile_2_6(input, index + 1)

def tile_2_7(input, index):
    if (index == len(input)): return print_maze("VALID", 2, 7)
    elif input[index] == 'L': return tile_2_6(input, index + 1)
    elif input[index] == 'R': return tile_2_8(input, index + 1)
    elif input[index] == 'U': return tile_1_7(input, index + 1)
    elif input[index] == 'D': return tile_3_7(input, index + 1)
    else : return tile_2_7(input, index + 1)

def tile_2_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 2, 8)

def tile_3_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 3, 0)

def tile_3_1(input, index):
    if (index == len(input)): return print_maze("VALID", 3, 1)
    elif input[index] == 'L': return tile_3_0(input, index + 1)
    elif input[index] == 'R': return tile_3_2(input, index + 1)
    elif input[index] == 'U': return tile_2_1(input, index + 1)
    elif input[index] == 'D': return tile_4_1(input, index + 1)
    else : return tile_3_1(input, index + 1)

def tile_3_2(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 3, 2)

def tile_3_3(input, index):
    if (index == len(input)): return print_maze("VALID", 3, 3)
    elif input[index] == 'L': return tile_3_2(input, index + 1)
    elif input[index] == 'R': return tile_3_4(input, index + 1)
    elif input[index] == 'U': return tile_2_3(input, index + 1)
    elif input[index] == 'D': return tile_4_3(input, index + 1)
    else : return tile_3_3(input, index + 1)

def tile_3_4(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 3, 4)

def tile_3_5(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 3, 5)

def tile_3_6(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 3, 6)

def tile_3_7(input, index):
    if (index == len(input)): return print_maze("VALID", 3, 7)
    elif input[index] == 'L': return tile_3_6(input, index + 1)
    elif input[index] == 'R': return tile_3_8(input, index + 1)
    elif input[index] == 'U': return tile_2_7(input, index + 1)
    elif input[index] == 'D': return tile_4_7(input, index + 1)
    else : return tile_3_7(input, index + 1)

def tile_3_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 3, 8)

def tile_4_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 4, 0)

def tile_4_1(input, index):
    if (index == len(input)): return print_maze("VALID", 4, 1)
    elif input[index] == 'L': return tile_4_0(input, index + 1)
    elif input[index] == 'R': return tile_4_2(input, index + 1)
    elif input[index] == 'U': return tile_3_1(input, index + 1)
    elif input[index] == 'D': return tile_5_1(input, index + 1)
    else : return tile_4_1(input, index + 1)

def tile_4_2(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 4, 2)

def tile_4_3(input, index):
    if (index == len(input)): return print_maze("VALID", 4, 3)
    elif input[index] == 'L': return tile_4_2(input, index + 1)
    elif input[index] == 'R': return tile_4_4(input, index + 1)
    elif input[index] == 'U': return tile_3_3(input, index + 1)
    elif input[index] == 'D': return tile_5_3(input, index + 1)
    else : return tile_4_3(input, index + 1)

def tile_4_4(input, index):
    if (index == len(input)): return print_maze("VALID", 4, 4)
    elif input[index] == 'L': return tile_4_3(input, index + 1)
    elif input[index] == 'R': return tile_4_5(input, index + 1)
    elif input[index] == 'U': return tile_3_4(input, index + 1)
    elif input[index] == 'D': return tile_5_4(input, index + 1)
    else : return tile_4_4(input, index + 1)

def tile_4_5(input, index):
    if (index == len(input)): return print_maze("VALID", 4, 5)
    elif input[index] == 'L': return tile_4_4(input, index + 1)
    elif input[index] == 'R': return tile_4_6(input, index + 1)
    elif input[index] == 'U': return tile_3_5(input, index + 1)
    elif input[index] == 'D': return tile_5_5(input, index + 1)
    else : return tile_4_5(input, index + 1)

def tile_4_6(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 4, 6)

def tile_4_7(input, index):
    if (index == len(input)): return print_maze("VALID", 4, 7)
    elif input[index] == 'L': return tile_4_6(input, index + 1)
    elif input[index] == 'R': return tile_4_8(input, index + 1)
    elif input[index] == 'U': return tile_3_7(input, index + 1)
    elif input[index] == 'D': return tile_5_7(input, index + 1)
    else : return tile_4_7(input, index + 1)

def tile_4_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 4, 8)

def tile_5_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 5, 0)

def tile_5_1(input, index):
    if (index == len(input)): return print_maze("VALID", 5, 1)
    elif input[index] == 'L': return tile_5_0(input, index + 1)
    elif input[index] == 'R': return tile_5_2(input, index + 1)
    elif input[index] == 'U': return tile_4_1(input, index + 1)
    elif input[index] == 'D': return tile_6_1(input, index + 1)
    else : return tile_5_1(input, index + 1)

def tile_5_2(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 5, 2)

def tile_5_3(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 5, 3)

def tile_5_4(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 5, 4)

def tile_5_5(input, index):
    if (index == len(input)): return print_maze("VALID", 5, 5)
    elif input[index] == 'L': return tile_5_4(input, index + 1)
    elif input[index] == 'R': return tile_5_6(input, index + 1)
    elif input[index] == 'U': return tile_4_5(input, index + 1)
    elif input[index] == 'D': return tile_6_5(input, index + 1)
    else : return tile_5_5(input, index + 1)

def tile_5_6(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 5, 6)

def tile_5_7(input, index):
    if (index == len(input)): return print_maze("VALID", 5, 7)
    elif input[index] == 'L': return tile_5_6(input, index + 1)
    elif input[index] == 'R': return tile_5_8(input, index + 1)
    elif input[index] == 'U': return tile_4_7(input, index + 1)
    elif input[index] == 'D': return tile_6_7(input, index + 1)
    else : return tile_5_7(input, index + 1)

def tile_5_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 5, 8)

def tile_6_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 6, 0)

def tile_6_1(input, index):
    if (index == len(input)): return print_maze("VALID", 6, 1)
    elif input[index] == 'L': return tile_6_0(input, index + 1)
    elif input[index] == 'R': return tile_6_2(input, index + 1)
    elif input[index] == 'U': return tile_5_1(input, index + 1)
    elif input[index] == 'D': return tile_7_1(input, index + 1)
    else : return tile_6_1(input, index + 1)

def tile_6_2(input, index):
    if (index == len(input)): return print_maze("VALID", 6, 2)
    elif input[index] == 'L': return tile_6_1(input, index + 1)
    elif input[index] == 'R': return tile_6_3(input, index + 1)
    elif input[index] == 'U': return tile_5_2(input, index + 1)
    elif input[index] == 'D': return tile_7_2(input, index + 1)
    else : return tile_6_2(input, index + 1)

def tile_6_3(input, index):
    if (index == len(input)): return print_maze("VALID", 6, 3)
    elif input[index] == 'L': return tile_6_2(input, index + 1)
    elif input[index] == 'R': return tile_6_4(input, index + 1)
    elif input[index] == 'U': return tile_5_3(input, index + 1)
    elif input[index] == 'D': return tile_7_3(input, index + 1)
    else : return tile_6_3(input, index + 1)

def tile_6_4(input, index):
    if (index == len(input)): return print_maze("VALID", 6, 4)
    elif input[index] == 'L': return tile_6_3(input, index + 1)
    elif input[index] == 'R': return tile_6_5(input, index + 1)
    elif input[index] == 'U': return tile_5_4(input, index + 1)
    elif input[index] == 'D': return tile_7_4(input, index + 1)
    else : return tile_6_4(input, index + 1)

def tile_6_5(input, index):
    if (index == len(input)): return print_maze("VALID", 6, 5)
    elif input[index] == 'L': return tile_6_4(input, index + 1)
    elif input[index] == 'R': return tile_6_6(input, index + 1)
    elif input[index] == 'U': return tile_5_5(input, index + 1)
    elif input[index] == 'D': return tile_7_5(input, index + 1)
    else : return tile_6_5(input, index + 1)

def tile_6_6(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 6, 6)

def tile_6_7(input, index):
    return print_maze("SOLVED", 6, 7)

def target_tile():
    return "tile_6_7"

def tile_6_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 6, 8)

def tile_7_0(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 0)

def tile_7_1(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 1)

def tile_7_2(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 2)

def tile_7_3(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 3)

def tile_7_4(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 4)

def tile_7_5(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 5)

def tile_7_6(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 6)

def tile_7_7(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 7)

def tile_7_8(input, index):
    try: HTMLParser().feed(input)
    except: pass
    return print_maze("INVALID", 7, 8)
