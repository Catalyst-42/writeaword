import curses, os, os.path, random, time

myscreen = curses.initscr()
y, x = myscreen.getmaxyx()

curses.start_color()
curses.noecho()
curses.cbreak()

# initializing all things
out = ''
code = 0
speed = 0
speed_keys = 0
i = 0
keys =  0
mistakes = 0
log_mistakes =  0
color_error = 0
code = 0
scoreboard =  0
all_runs = 0
speed_median = 0
mistakes_median = 0
speed_record = 0
line = 0
now_line = 0
local_line = x
j = x
all_speed_log = []
all_mistakes_log = []
scoreboard = '|        Пусто       |'
scoreboard_m = '|        Пусто       |'
bg = '|' + ' ' * (x - 26) + '|'
texts = ''
text = ''
void = ' ' * x

# language
lang = 0
lang_name_set = ['Русский', 'Английский', 'Цифры']
lang_score_s_set = ['ru-score-s.txt', 'en-score-s.txt', 'nl-score-s.txt']
lang_score_m_set = ['ru-score-m.txt', 'en-score-m.txt', 'nl-score-m.txt']
lang_text_set = ['ru-text.txt', 'en-text.txt', 'nl-text.txt']

def load_stats():
    global scoreboard, all_runs, speed_median, scoreboard_m, mistakes_median, speed_record

    speed_median = 0
    mistakes_median = 0
    all_runs = 0
    speed_record = 0
    scoreboard = '|        Пусто       |'
    scoreboard_m = '|        Пусто       |'

    if os.path.exists(lang_score_s_set[lang]):
        with open(lang_score_s_set[lang], 'r') as f:
            scoreboard = f.read().splitlines()
            all_runs = len(scoreboard)
            
            # all speed median
            speed_median = 0
            for _ in range(len(scoreboard)):
                speed_median += float(scoreboard[_])

            speed_median = round(speed_median / len(scoreboard), 2)

            # the record
            speed_record = 0
            for _ in range(len(scoreboard)):
                if float(scoreboard[_]) > speed_record:
                    speed_record = float(scoreboard[_])

            damp = ''
            size = len(scoreboard) - 1
            p = 0
            while size >= 0 and p < 5:
                damp += '|       ' + scoreboard[size] + ' ' * (len('| Последние скорости |') - 9 - len(scoreboard[size])) + '|\n'
                size -= 1
                p += 1

            scoreboard = damp
    
        f.close()

    if os.path.exists(lang_score_m_set[lang]):
        with open(lang_score_m_set[lang], 'r') as f:
            scoreboard_m = f.read().splitlines()

            # all mistakes median
            mistakes_median = 0
            for _ in range(len(scoreboard_m)):
                mistakes_median += float(scoreboard_m[_].replace('%', ' '))

            mistakes_median = round(mistakes_median / len(scoreboard_m), 2)

            damp = ''
            size = len(scoreboard_m) - 1
            p = 0
            while size >= 0 and p < 5:
                damp += '|       ' + scoreboard_m[size] + ' ' * (len('|  Последние ошибки  |') - 9 - len(scoreboard_m[size])) + '|\n'
                size -= 1
                p += 1

            scoreboard_m = damp
        
        f.close()


def open_text():
    global texts, text, lang_text_set, lang, line, now_line, local_line, j, x, i, line, out, mistakes

    if os.path.exists(lang_text_set[lang]):
        with open(lang_text_set[lang], 'r') as f:
            texts = f.read().splitlines()

        f.close()

    for _ in range(len(texts)):
        texts[_] += ' '

    #  end of typing text line
    myscreen.clear()
    out, i = '', 0

    mistakes = 0

    line, now_line, local_line, j = random.randint(0, len(texts) - 1), 0, x, x
    text = texts[line]

    if len(text) >= x:
        while j > 0:
            j -= 1
            if text[j] == ' ':
                text = text[:j] + ' '
                break

    now_line += len(text)


def main(myscreen):
    global text, texts, out, speed, i, keys, mistakes, y, x, void, speed_keys, line, now_line, log_mistakes, all_speed_log, all_mistakes_log, color_error, code, lang
    
    # init common clear colors
    curses.init_color(10, 900, 900, 900)
    curses.init_color(11, 1000, 0, 1000)
    curses.init_color(12, 500, 500, 500)
    curses.init_color(13, 0, 1000, 1000)
    curses.init_pair(1, 10, curses.COLOR_BLACK) # stats    
    curses.init_pair(2, 10, curses.COLOR_BLACK) # comon color
    curses.init_pair(3, 11, curses.COLOR_BLACK) # error color
    curses.init_pair(4, 12, curses.COLOR_BLACK) # already typed
    curses.init_pair(5, 11, curses.COLOR_BLACK) # logo color
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLACK) # bg color

    while 1:
        # stats
        speed_out, mistakes_out = 0, 0

        myscreen.bkgd(curses.color_pair(6))

        if all_speed_log:
            for _ in range(len(all_speed_log)):
                speed_out += all_speed_log[_]
            
            speed_out = round(speed_out / len(all_speed_log), 2)

            for _ in range(len(all_mistakes_log)):
                mistakes_out += all_mistakes_log[_]
            
            mistakes_out = round(mistakes_out / len(all_mistakes_log), 2)
        
        if color_error == 0:
            myscreen.addstr(1, 0, text, curses.color_pair(2))

        else:
            myscreen.addstr(1, 0, text, curses.color_pair(3))

        # complete text
        myscreen.addstr(1, 0, text[:i], curses.color_pair(4))

        # scoreboarding
        myscreen.addstr(4, 0, '| Последние скорости |', curses.color_pair(1))
        myscreen.addstr(5, 0, str(scoreboard), curses.color_pair(1))
        myscreen.addstr(11, 0, '|  Последние ошибки  |', curses.color_pair(1))
        myscreen.addstr(12, 0, str(scoreboard_m), curses.color_pair(1))

        # stats
        for _ in range(11, 17):
            myscreen.addstr(_, 24, bg, curses.color_pair(1))

        myscreen.addstr(11, 24, '| Глобальная статистика: ', curses.color_pair(1))
        myscreen.addstr(12, 24, '| Рекорд скорости: ' + str(speed_record), curses.color_pair(1))
        myscreen.addstr(13, 24, '| Всего строк: ' + str(all_runs), curses.color_pair(1))
        myscreen.addstr(14, 24, '|', curses.color_pair(1))
        myscreen.addstr(15, 24, '| Средняя скорость всех попыток: ' + str(speed_median), curses.color_pair(1))
        myscreen.addstr(16, 24, '| Средние ошибки всех попыток: ' + str(mistakes_median) + ' %', curses.color_pair(1))

        # bg for session
        for _ in range(4, 9):
            myscreen.addstr(_, 24, bg, curses.color_pair(1))
        
        myscreen.addstr(0, 0, void, curses.color_pair(1))

        if speed == 0:
            myscreen.addstr(4, 24, '| Средние значения сеанса:', curses.color_pair(1))
            myscreen.addstr(5, 24, '| Символов в минуту: -- ', curses.color_pair(1))
            myscreen.addstr(6, 24, '| Ошибки: --', curses.color_pair(1)) 
            myscreen.addstr(7, 24, '| Время: -- ', curses.color_pair(1))

        else:
            myscreen.addstr(4, 24, '| Средние значения сеанса:', curses.color_pair(1))
            myscreen.addstr(5, 24, '| Символов в минуту: ' + str(speed_out), curses.color_pair(1))
            myscreen.addstr(6, 24, '| Ошибки: ' + str(mistakes_out) + ' % ', curses.color_pair(1))
            myscreen.addstr(7, 24, '| Время: ' + str(round(speed, 2)), curses.color_pair(1)) 

        # exit
        myscreen.addstr(9, 24, bg, curses.color_pair(1))
        myscreen.addstr(9, 24, '| Язык: ' + lang_name_set[lang], curses.color_pair(1))

        # outlite the text input and give cursor to it 
        myscreen.addstr(3, 0, '‾' * x, curses.color_pair(2))
        myscreen.addstr(0, 0, 'Writeaword by Catalyst', curses.color_pair(5))
        myscreen.addstr(2, 0, ' ' * x, curses.color_pair(2))
        myscreen.addstr(2, 0, out, curses.color_pair(2))

        code = myscreen.get_wch()

        if out == '':
            start_time = time.time()

        if code == '\x1b': # escape key
            break

        elif code == '\x7f': # delete key
            out = out[:-1]
        
        elif code == 260: # left arrow
            if lang > 0:
                lang -= 1

            else:
                lang = 2

            j = 0
            open_text()
            load_stats()
            
        elif code == 261: # right arrow
            if lang < 2:
                lang += 1

            else: 
                lang = 0

            j = 0
            open_text()
            load_stats()
        
        else:
            try:
                out += code

            except TypeError:
                pass

        if out == text[:len(out)]:
            i = len(out)
            color_error = 0

            if len(out) >= len(text):
                #  end of typing text line
                myscreen.clear()
                out, i, speed_keys, speed = '', 0, len(text), time.time() - start_time
                keys += len(text)
                log_mistakes += mistakes

                # global stats
                all_speed_log.append(round(speed_keys / speed * 60, 2))
                all_mistakes_log.append(round(mistakes / (len(text) - 1) * 100, 2))

                with open(lang_score_s_set[lang], 'a') as f:
                    f.write(str(round(speed_keys / speed * 60, 2)) + '\n')
                f.close()

                with open(lang_score_m_set[lang], 'a') as f:
                    f.write(str(round(mistakes / (len(text) - 1) * 100, 2)) +' % \n')
                f.close()

                load_stats()
                mistakes = 0

                if now_line == len(texts[line]):
                    line, now_line, local_line, j = random.randint(0, len(texts) - 1), 0, x, x
                    text = texts[line][:x]

                    if len(text) >= x:
                        while j > 0:
                            j -= 1
                            if text[j] == ' ':
                                text = text[:j] + ' '
                                break

                    now_line += len(text)
                
                else:
                    # new part of old text
                    page, j = now_line, now_line + x
                    text = texts[line][page:j]
                    j = len(text)
                    
                    if len(text) >= x:
                        while j > 0:
                            j -= 1
                            if text[j] == ' ':
                                text = text[:j] + ' '
                                break

                    now_line += len(text)

        else:
            if out[:-1] == text[:len(out) - 1]:
                mistakes += 1

            color_error = 1

        myscreen.refresh()

load_stats()
open_text()
curses.wrapper(main)
