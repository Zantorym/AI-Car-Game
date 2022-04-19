import pygame
from src.game import Game
from src.aigame import AIGame
from src.game_train import GameTrain


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 100, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text('X', 20, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.playaix, self.playaiy = self.mid_w, self.mid_h + 60
        self.trainaix, self.trainaiy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(
                'Main Menu', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text('Play Game', 30, self.startx, self.starty)
            self.game.draw_text('AI Plays Game', 30, self.playaix, self.playaiy)
            self.game.draw_text('Train AI', 30,
                                self.trainaix, self.trainaiy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (
                    self.playaix + self.offset, self.playaiy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.trainaix + self.offset, self.trainaiy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (
                    self.trainaix + self.offset, self.trainaiy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.playaix + self.offset, self.playaiy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.track_menu
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class TrackMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Track 1'
        self.track0x, self.track0y = self.mid_w, self.mid_h - 30
        self.track1x, self.track1y = self.mid_w, self.mid_h
        self.track2x, self.track2y = self.mid_w, self.mid_h + 30
        self.cursor_rect.midtop = (self.track0x + self.offset, self.track0y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text(
                'Select Track', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 60)
            self.game.draw_text('Track 1', 30, self.track0x, self.track0y)
            self.game.draw_text('Track 2', 30, self.track1x, self.track1y)
            self.game.draw_text('Track 3', 30, self.track2x, self.track2y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Track 1':
                self.cursor_rect.midtop = (
                    self.track1x + self.offset, self.track1y)
                self.state = 'Track 2'
            elif self.state == 'Track 2':
                self.cursor_rect.midtop = (
                    self.track2x + self.offset, self.track2y)
                self.state = 'Track 3'
            elif self.state == 'Track 3':
                self.cursor_rect.midtop = (
                    self.track0x + self.offset, self.track0y)
                self.state = 'Track 1'
        elif self.game.UP_KEY:
            if self.state == 'Track 1':
                self.cursor_rect.midtop = (
                    self.track2x + self.offset, self.track2y)
                self.state = 'Track 3'
            elif self.state == 'Track 2':
                self.cursor_rect.midtop = (
                    self.track0x + self.offset, self.track0y)
                self.state = 'Track 1'
            elif self.state == 'Track 3':
                self.cursor_rect.midtop = (
                    self.track1x + self.offset, self.track1y)
                self.state = 'Track 2'

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Track 1':
                game = Game(0)
                game.start()
            elif self.state == 'Track 2':
                game = Game(1)
                game.start()
            elif self.state == 'Track 3':
                game = Game(2)
                game.start()
            self.run_display = False


class AIMenu(TrackMenu):
    def __init__(self, game):
        TrackMenu.__init__(self, game)

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            if self.state == 'Track 1':
                game = AIGame(0)
                game.start()
            elif self.state == 'Track 2':
                game = AIGame(1)
                game.start()
            elif self.state == 'Track 3':
                game = AIGame(2)
                game.start()
            self.run_display = False


class AITrainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(
                'Train AI', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text(
                'Start', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 20)
            self.blit_screen()

    def check_input(self):
        # if self.game.START_KEY or self.game.BACK_KEY:
        #     self.game.curr_menu = self.game.main_menu
        #     self.run_display = False

        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            trainer = GameTrain()
            trainer.start()
