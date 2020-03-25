import curses
import random
from curses import textpad
menu = ['PLAY', 'LEADERBOARD', 'EXIT']


def print_menu(screen, selected_row_idx):
    screen.clear()
    h, w = screen.getmaxyx()
    for idx, row in enumerate(menu):  # enumerate return the index with value
        x = w//2-len(row)//2
        y = (h//2-len(menu)//2)+idx
        if idx == selected_row_idx:
            screen.attron(curses.color_pair(1))
            screen.addstr(y, x, row)
            screen.attroff(curses.color_pair(1))
        else:
            screen.addstr(y, x, row)
    screen.refresh()


def leader(screen):
    screen.clear()
    f2 = open('k.txt')
    lis = f2.readlines()
    f2.close()
    sk = []
    for i in range(len(lis)):
        sc = lis[i].split(";")
        sc[1] = sc[1].strip()
        sk.append(sc)
    sk.sort(key=lambda x: x[1])
    for i in range(len(lis)):
        screen.addstr(3+i, 3, sk[i][0])
        screen.addstr(3+i, 30, sk[i][1])
        screen.refresh()
    print(sk)
    screen.getch()


def create_food(snake, w, h):
    food = None
    while food is None:
        food_x = random.randint(3, w-3)
        food_y = random.randint(3, h-3)
        food = [food_x, food_y]
        if food in snake:
            food = None
    return list(food)


def player(screen, h, w):
    screen.addstr(h//2, w//2, "Enter Player's Name")
    curses.echo()
    screen.move(h//2+1, w//2)
    p = screen.getstr().decode('utf8')
    return p


def disp_score(screen, score):
    screen.addstr(1, 1, "SCORE :"+str(score))


def snake(screen, name):
    score = 0
    disp_score(screen, score)
    h, w = screen.getmaxyx()
    curses.curs_set(0)
    screen.clear()
    screen.nodelay(1)
    screen.timeout(300)
    box = [[2, 2], [h-2, w-2]]
    textpad.rectangle(screen, box[0][0], box[0][1], box[1][0], box[1][1])
    snake = [[w//2+1, h//2], [w//2, h//2], [w//2-1, h//2]]
    for x, y in snake:
        screen.addch(y, x, '*')
    food = create_food(snake, w, h)
    screen.addch(food[1], food[0], '*')
    dir = 1
    prev_dir = 1
    key = curses.KEY_RIGHT
    key_set = [curses.KEY_RIGHT, curses.KEY_DOWN,
               curses.KEY_UP, curses.KEY_LEFT]
    while 1:
        next_key = screen.getch()
        head = snake[0]
        if (next_key in key_set):
            key = next_key
        if key == curses.KEY_RIGHT and prev_dir != 0:
            dir = 1
        if key == curses.KEY_LEFT and prev_dir != 1:
            dir = 0
        if key == curses.KEY_UP and prev_dir != 2:
            dir = 3
        if key == curses.KEY_DOWN and prev_dir != 3:
            dir = 2
        prev_dir = dir
        if dir == 1:
            new_head = [head[0]+1, head[1]]
        elif dir == 0:
            new_head = [head[0]-1, head[1]]
        elif dir == 2:
            new_head = [head[0], head[1]+1]
        elif dir == 3:
            new_head = [head[0], head[1]-1]
        snake.insert(0, new_head)
        screen.addch(new_head[1], new_head[0], '*')
        if(snake[0] == food):
            food = create_food(snake, w, h)
            score += 1
            disp_score(screen, score)
            screen.addch(food[1], food[0], '*')
        else:
            screen.addch(snake[-1][1], snake[-1][0], ' ')
            snake.pop()
        if(box[0][0] == new_head[0]or box[1][1] == new_head[0] or
           box[0][1] == new_head[1]or box[1][0] == new_head[1]or
           snake[0]in snake[1:]):
            screen.addstr(h//2, w//2, "game over")
            f = open('k.txt', 'a+')
            non_emp = f.read(2)
            if len(non_emp) > 0:
                f.write("\n")
            f.write(name+";"+str(score))
            f.write("\n")
            f.close()
            screen.nodelay(0)
            screen.timeout(10000)
            break


def main(screen):
    h, w = screen.getmaxyx()
    name = str(player(screen, h, w))
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    current_row_idx = 0
    print_menu(screen, current_row_idx)
    while 1:

        key = screen.getch()
        screen.clear()
        if(key == curses.KEY_UP and current_row_idx > 0):
            current_row_idx -= 1
        if(key == curses.KEY_DOWN and current_row_idx < len(menu)-1):
            current_row_idx += 1
        if(key == curses.KEY_ENTER or key in[10, 13]):
            if(current_row_idx == len(menu)-1):
                break
            elif(current_row_idx == 0):
                snake(screen, name)
            elif(current_row_idx == 1):
                leader(screen)
        print_menu(screen, current_row_idx)
    screen.refresh()


curses.wrapper(main)
