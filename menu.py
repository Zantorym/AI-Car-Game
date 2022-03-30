import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('X', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 60
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text('Start Game', 30, self.startx, self.starty)
            self.game.draw_text('Options', 30, self.optionsx, self.optionsy)
            self.game.draw_text('Credits', 30, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Track'
        self.trackx, self.tracky = self.mid_w, self.mid_h + 30
        self.obsticlesx, self.obsticlesy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.trackx + self.offset, self.tracky)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0,0,0))
            self.game.draw_text('Options', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text('Select obsticles', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10)
            self.draw_cursor()
            self.blit_screen()
        
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Track':
                self.state = 'Obsticles'
                self.cursor_rect.midtop = (self.obsticlesx + self.offset, self.obsticlesy)
            elif self.state == 'Obsticles':
                self.state = 'Track'
                self.cursor_rect.midtop = (self.trackx + self.offset, self.tracky)
        elif self.game.START_KEY:
            # Have to create menu for track and obsticle selection
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def display_menu(self):
       self.run_display = True
       while self.run_display:
           self.game.check_events()
           self.check_input()
           self.game.display.fill(self.game.BLACK)
           self.game.draw_text('Credits', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
           self.game.draw_text('(names)', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 20)
           self.blit_screen()
           
    def check_input(self):
        if self.game.START_KEY or self.game.BACK_KEY:
               self.game.curr_menu = self.game.main_menu
               self.run_display = False