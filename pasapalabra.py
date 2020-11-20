import sys, pygame, os, random, math, time

pygame.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()


# =================
# === VARIABLES ===
# =================
screen_width, screen_height = 1320, 700
pausa = True
game_end = False
winner = None

music = False

CT = 60
start_ticks = pygame.time.get_ticks()

screen = pygame.display.set_mode((screen_width, screen_height))

abecedario = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'

rosco_width, rosco_height = 700, 700
rosco_x, rosco_y = screen_width/4-20, 3

letter_width, letter_height=69, 69
radius_letter = letter_width/2

pasapalabra_width, pasapalabra_height = 300, 150
pasapalabra_x, pasapalabra_y = 50, 550

score_rectangle_width, score_rectangle_height = 250, 400
score_rectangle_x, score_rectangle_y = 75, 200

button_state = 0

max_time = 15
time_spent = 0

# ==============
# === COLORS ===
# ==============
black = 0,0,0
white = 255, 255, 255


# ====================
# === FONTS & TEXT ===
# ====================
pasapalabra_font = pygame.font.Font("Fonts/Golden_Metafor_Regular.ttf", 30)
pasapalabra_text = pasapalabra_font.render("Pasapalabra", False, white)

time_font = pygame.font.Font("Fonts/MEDIO_VINTAGE.otf", 50)
time_text = time_font.render("TIEMPO", False, white)

time_font_75 = pygame.font.Font("Fonts/MEDIO_VINTAGE.otf", 75)


# ===================
# === MUSIC & SFX ===
# ===================
pygame.mixer.music.load("Sounds/Layton_puzzle_theme.mp3")
pygame.mixer.music.set_volume(0.5)

correct_sfx = pygame.mixer.Sound("Sounds/correct.wav")
wrong_sfx = pygame.mixer.Sound("Sounds/wrong.wav")


# ==============
# === IMAGES ===
# ==============
fondo_azul = pygame.transform.scale( pygame.image.load('Images/fondo_azul_2.jpg'),   (screen_width, screen_height))
# fondo_naranja = pygame.transform.scale( pygame.image.load('Images/fondo_naranja.jpg'),   (screen_width, screen_height))

unpressed_blue_button = pygame.transform.scale( pygame.image.load('Images/blue_button.png'), (pasapalabra_width, pasapalabra_height))
pressed_blue_button = pygame.transform.scale( pygame.image.load('Images/pressed_blue_button.png'), (pasapalabra_width, pasapalabra_height))
unpressed_orange_button = pygame.transform.scale( pygame.image.load('Images/orange_button.png'), (pasapalabra_width, pasapalabra_height))
pressed_orange_button = pygame.transform.scale( pygame.image.load('Images/pressed_orange_button.png'), (pasapalabra_width, pasapalabra_height))

rosco_azul = pygame.transform.scale( pygame.image.load('Images/rosco_azul.png'),   (rosco_width, rosco_height))
# rosco_naranja = pygame.transform.scale( pygame.image.load('Images/rosco_naranja.png'),   (rosco_width, rosco_height))

blue_rectangle = pygame.transform.scale( pygame.image.load('Images/blue_rectangle.png'),   (score_rectangle_width, score_rectangle_height))
orange_rectangle = pygame.transform.scale( pygame.image.load('Images/orange_rectangle.png'),   (score_rectangle_width, score_rectangle_height))
red_rectangle = pygame.transform.scale( pygame.image.load('Images/red_rectangle.png'),   (score_rectangle_width, score_rectangle_height))

jaume_image = pygame.transform.scale( pygame.image.load('Images/jaume.png'), (350, 350))
nuria_image = pygame.transform.scale( pygame.image.load('Images/nuria.png'), (350, 350))

verde_letter2image = {}
rojo_letter2image  = {}
for letter in abecedario:
    verde_letter2image["verde_{}".format(letter)] = pygame.transform.scale(pygame.image.load("Images/Verde/verde_{}.png".format(letter)), (letter_width, letter_height))
    rojo_letter2image["rojo_{}".format(letter)] = pygame.transform.scale(pygame.image.load("Images/Rojo/rojo_{}.png".format(letter)),(letter_width, letter_height))

congratulations = pygame.transform.scale( pygame.image.load('Images/congratulations.png'), (screen_width//2, screen_height//3))

# (width, height)
letter2coord = {
    "A": (621,2),
    "B": (690,10),
    "C": (758,30),
    "D": (820,70),
    "E": (870,120),
    "F": (910,185),
    "G": (932,253),
    "H": (940,325),
    "I": (930,396),
    "J": (903,462),
    "K": (865,520),
    "L": (815,570),
    "M": (755,605),
    "N": (690,625),
    "Ñ": (619,630),
    "O": (547,620),
    "P": (477,595),
    "Q": (412,550),
    "R": (365,495),
    "S": (330,429),
    "T": (310,358),
    "U": (312,285),
    "V": (327,210),
    "W": (363,145),
    "X": (413,80),
    "Y": (477,35),
    "Z": (547,10),
    
}

# ===============
# === CLASSES ===
# ===============

class Image:
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height


class Player:
    def __init__(self, color, image):
        self.letters2state = {}
        for letter in abecedario:
            self.letters2state[letter] = 0        # 0: not answered | 1: Verde | 2: Rojo
        if color == "azul":
            self.rectangle = blue_rectangle
            self.unpressed_button = unpressed_blue_button
            self.pressed_button = pressed_blue_button
        else:
            self.rectangle = orange_rectangle
            self.unpressed_button = unpressed_orange_button
            self.pressed_button = pressed_orange_button
        self.fondo = fondo_azul
        self.rosco = rosco_azul
        self.image = image
        self.end = False
        


# ==============
# === PLAYER ===
# ==============

Jaume, Nuria = Player("naranja", jaume_image), Player("azul", nuria_image)
current_player = random.randint(1,2)
if current_player==1:
    current_player = Jaume
else:
    current_player = Nuria
# current_player = Nuria


# =================
# === FUNCTIONS ===
# =================

def close_game():
    pygame.display.quit()
    sys.exit()

def click_letter(m_x, m_y):
    global letter2coord
    for letter in letter2coord.keys():
        center_letter = (letter2coord[letter][0] + radius_letter , letter2coord[letter][1] + radius_letter)
        sqx = (m_x - center_letter[0])**2
        sqy = (m_y - center_letter[1])**2

        if math.sqrt(sqx+sqy) < radius_letter:
            return letter

def draw_all(end_f):
    global current_player, time_left, winner
    screen.blit(current_player.fondo, (0,0))

    if not end_f:
        screen.blit(current_player.image, (500, 175))

        if button_state == 0:
            screen.blit(current_player.unpressed_button, (pasapalabra_x, pasapalabra_y))
        else:
            screen.blit(current_player.pressed_button, (pasapalabra_x, pasapalabra_y))
            
        screen.blit(pasapalabra_text, (pasapalabra_x+48, pasapalabra_y+55))

        if time_left>5:
            screen.blit(current_player.rectangle, (score_rectangle_x, score_rectangle_y))
        else:
            screen.blit(red_rectangle, (score_rectangle_x, score_rectangle_y))
        screen.blit(time_text, (score_rectangle_x+40, score_rectangle_y+65))

        time_left_text = time_font_75.render(str(time_left), False, white)
        screen.blit(time_left_text, (score_rectangle_x+80, score_rectangle_y+170))

        screen.blit(current_player.rosco, (rosco_x, rosco_y))


        for letter in current_player.letters2state.keys():
            if current_player.letters2state[letter]  ==1:
                screen.blit(verde_letter2image["verde_{}".format(letter)], letter2coord[letter]) 
            elif current_player.letters2state[letter]==2:
                screen.blit(rojo_letter2image["rojo_{}".format(letter)], letter2coord[letter])
        

    else:
        screen.blit(winner.image, (500, 200))
        screen.blit(congratulations, (screen_width//4, 10))

    pygame.display.flip()



# ============
# === MAIN ===
# ============
while True:
    clock.tick(CT)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    time_left= max_time - time_spent


    if not pausa:
        if not music:
            music = True
            pygame.mixer.music.play(loops=-1)
        if time_left == 0:
            pausa = True
            wrong_sfx.play()
            pygame.mixer.music.stop()
        time_spent = (pygame.time.get_ticks()-start_ticks)//1000

    isAny0_jaume = True
    isAny0_nuria = True

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            close_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            possible_letter = click_letter(mouse_x, mouse_y)
            if possible_letter != None:
                isAny0_jaume = False
                isAny0_nuria = False

                if event.button == 1:       # Turn green
                    current_player.letters2state[possible_letter] = 1
                    time_spent = 0
                    correct_sfx.play()
                elif event.button == 3:     # Turn red
                    current_player.letters2state[possible_letter] = 2
                    pausa = True
                    pygame.mixer.music.stop()
                    music = False
                    wrong_sfx.play()

                elif event.button == 2:     # Turn blue
                    current_player.letters2state[possible_letter] = 0
                
                for letter in abecedario:
                    if Jaume.letters2state[letter]==0:
                        isAny0_jaume = True
                    if Nuria.letters2state[letter]==0:
                        isAny0_nuria = True
                

            else:
                if time_left != 0:
                    pausa = False
                else:
                    start_ticks = pygame.time.get_ticks()
                    time_spent = 0
                    pausa = True
            if time_spent == 0:
                start_ticks = pygame.time.get_ticks()
            if pasapalabra_x < mouse_x < pasapalabra_x+pasapalabra_width and pasapalabra_y < mouse_y < pasapalabra_y+pasapalabra_height:
                button_state = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            button_state = 0
            if pasapalabra_x < mouse_x < pasapalabra_x+pasapalabra_width and pasapalabra_y < mouse_y < pasapalabra_y+pasapalabra_height:
                if current_player == Jaume:
                    if not Nuria.end:
                        current_player = Nuria
                        pausa = True
                        pygame.mixer.music.stop()
                        music = False

                else:
                    if not Jaume.end:
                        current_player = Jaume
                        pausa = True
                        pygame.mixer.music.stop()
                        music = False
                
                start_ticks = pygame.time.get_ticks()
                time_spent = 0
    if Jaume.end:
        current_player=Nuria
    if Nuria.end:
        current_player=Jaume
    # END GAME
    if Jaume.end and Nuria.end:
        game_end = True
        jaume_fallos, nuria_fallos = 0, 0
        for letter in abecedario:
            if Jaume.letters2state[letter]==2:
                jaume_fallos+=1
            if Nuria.letters2state[letter]==2:
                nuria_fallos+=1
        if jaume_fallos<nuria_fallos:
            winner = Jaume
        elif jaume_fallos>nuria_fallos:
            winner = Nuria
    
    draw_all(game_end)
    if not isAny0_jaume:
        Jaume.end=True
    if not isAny0_nuria:
        Nuria.end=True
        