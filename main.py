import arcade
import time
from arcade.gui import *
import os
import sys


"""
Python Arcade Library 2.3.15
Character image from kenney.nl

"""

PIXEL_SIZE = 50
MAP_WIDTH = 20
MAP_HEIGHT = 12
WIDTH = PIXEL_SIZE * MAP_WIDTH
HEIGHT = PIXEL_SIZE * MAP_HEIGHT
TITLE  = ""
SPEED = 3
JUMP = 7
GRAVITATION = 0.3
CHARACTER_SIZE = 1
CHARACTER_START_POSITION_X = 300
CHARACTER_START_POSITION_Y = 200
WATER = 0
TIMER = 50
RIGHT_SCROLL = WIDTH//2
TOP_SCROLL = 0


#obrazovka při výhře
class End_win(arcade.View):
    def __init__(self):
        super().__init__()
        self.end_win_picture = arcade.load_texture('levels\\win.png')
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.end_win_picture.draw_sized(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.start_game()
        self.window.show_view(game_view)


#obrazovka při prohře
class End_lose(arcade.View):
    def __init__(self):
        super().__init__()
        self.end_lose_picture = arcade.load_texture("levels\\lose.png")
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.end_lose_picture.draw_sized(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.start_game()
        self.window.show_view(game_view)
        

#obrazovka při načtení hry
class Start_view(arcade.View):
    def __init__(self):
        super().__init__()
        self.end_lose_picture = arcade.load_texture('levels\\start.png')
        arcade.set_viewport(0, WIDTH, 0, HEIGHT)
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.end_lose_picture.draw_sized(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.start_game()
        self.window.show_view(game_view)


class Game(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_list = None
        self.physics_engine = None
        self.ground_list = None
        self.count_score = 0
        self.time = TIMER
        self.view_bottom = 0
        self.view_left = 0
        self.level = 1
        self.theme = None

        #zvuky
        self.jump_sound = arcade.load_sound("resources:sounds/coin1.wav")
        arcade.play_sound(self.jump_sound)
        self.start_game()
        

    def start_game(self):

        self.player_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()

        #nastavení animací
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture('images\\robot_walk0.png'))

        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture('images\\robot_walk0.png', mirrored=True))

        self.player.walk_right_textures = []
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk0.png'))
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk1.png'))
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk2.png'))
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk3.png'))
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk4.png'))
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk6.png'))
        self.player.walk_right_textures.append(arcade.load_texture('images\\robot_walk7.png'))

        self.player.walk_left_textures = []
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk0.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk1.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk2.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk3.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk4.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk5.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk6.png', mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture('images\\robot_walk7.png', mirrored=True))

        #velikost postavy
        self.player.scale = CHARACTER_SIZE

        #pořáteční souřadnice postavy
        self.player.center_x = CHARACTER_START_POSITION_X
        self.player.center_y = CHARACTER_START_POSITION_Y

        self.player_list.append(self.player)

        self.load_level(self.level)
        
    
    def load_level(self, level):
        #nastavení barev pozadí pro jednotlivé levely
        if self.level == 1: 
            arcade.set_background_color(arcade.csscolor.POWDER_BLUE)
        elif self.level == 2:
            arcade.set_background_color((0, 65, 106))
        elif self.level == 3:
            arcade.set_background_color((27, 27, 27))

        #přidání mapy .tmx
        my_map = arcade.read_tiled_map("levels\\level_" + str(level) + ".tmx", 1)

        self.ground_list = arcade.generate_sprites(my_map, "ground", 1)
        
        #nastavení gravitace a bariér na přidanou mapu
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.ground_list, gravity_constant=GRAVITATION)

        #přidání odměn
        self.coin = arcade.generate_sprites(my_map, "coins", 1)

        #přidání domu
        self.house = arcade.generate_sprites(my_map, "house", 1)

        #přidání vody
        self.water = arcade.generate_sprites(my_map, "water", 1)

        #přidání soupeřů
        self.rival = arcade.generate_sprites(my_map, "rival", 1)

        #přidání dalších prvků
        self.stars = arcade.generate_sprites(my_map, "other", 1)

        self.view_bottom = 0
        self.view_left = 0


    def on_draw(self):
        arcade.start_render()
        self.stars.draw()
        self.ground_list.draw()
        self.player_list.draw()
        self.coin.draw()
        self.house.draw()
        self.water.draw()
        self.rival.draw()
        
        #vypisuje skore
        arcade.draw_text(f"Score: {self.count_score}", arcade.get_viewport()[0], arcade.get_viewport()[2] + 5, arcade.color.WHITE, font_size=25)

        #vypisuje zbývající čas
        seconds = int(self.time) % 60
        arcade.draw_text(f"Time: {seconds:02d}", arcade.get_viewport()[0], arcade.get_viewport()[2] + 60, arcade.color.WHITE, font_size=25)

        #vypisuje informaci o levelu
        arcade.draw_text(f"Level: {self.level}", arcade.get_viewport()[0] + 800, arcade.get_viewport()[2] + 550, arcade.color.WHITE, font_size=30)
        

    #ovládání hry
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player.change_y = JUMP
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0


    def on_update(self, delta_time):
        self.player_list.update_animation()
        self.player_list.update()
        self.physics_engine.update()
        self.time -= delta_time

        #zabraňuje padání mimo mapu
        if self.player.right < 100 or self.player.right > 15000:
            self.player.change_x = 0
        elif self.player.top > 600:
            self.player.change_y = -1

        #pohyb protivníka
        for one_rival in self.rival:
            if int(self.time) % 2 == 0:
                one_rival.right += 2
            else:
                one_rival.right -= 2

        #pohyb coin
        for one_coin in self.coin:
            if int(self.time) % 2 == 0:
                one_coin.angle += 0.5
            else:
                one_coin.angle -= 0.5

        scroll_map = False

        #nastavení posunu mapy - pravá
        right_boundary = self.view_left + WIDTH - RIGHT_SCROLL
        if self.player.right > right_boundary:
            if self.player.right < 6900:
                self.view_left += self.player.right - right_boundary
                scroll_map = True

        #nastavení posunu mapy - levá
        left_boundary = self.view_left + 20
        if self.player.left < left_boundary:
            if self.player.right < 6900:
                self.view_left -= left_boundary - self.player.left
                scroll_map = True

        #nastavení posunu mapy - nahoru
        top_boundary = self.view_bottom + HEIGHT - 40
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            scroll_map = True

        #nastavení posunu mapy - dolů
        bottom_boundary = self.view_bottom + 150

        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom

            #aby se neposouvala mapa pod vodu
            if self.view_bottom < 0:
                self.view_bottom = 0
            scroll_map = True
        
        if scroll_map == True:
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left, WIDTH + self.view_left, self.view_bottom, HEIGHT + self.view_bottom)
        

        #pokud spadne postava do vody
        water_hit = arcade.check_for_collision_with_list(self.player, self.water)
        if water_hit:
            time.sleep(0.3)
            view = End_lose()
            self.window.show_view(view)
            

        #pokud narazí do tanku
        rival_hit = arcade.check_for_collision_with_list(self.player, self.rival)
        if rival_hit:
            time.sleep(0.3)
            view = End_lose()
            self.window.show_view(view)
            
        
        #sbírání peněz
        coin_hit = arcade.check_for_collision_with_list(self.player, self.coin)
        for coin in coin_hit:
            self.count_score += 1
            coin.kill()


        #pokud dojde do domečku
        house_end = arcade.check_for_collision_with_list(self.player, self.house)
        for house in house_end:
            if self.level < 3:
                
                self.level += 1
                self.load_level(self.level)
                self.player.center_x = 200
                self.player.center_y = 200
                self.player.change_x = 0
                self.player.change_y = 0
                arcade.set_viewport(0, WIDTH, 0, HEIGHT)
                self.time = 50
            else:
                time.sleep(0.9)
                view = End_win()
                self.window.show_view(view)


        #pokud vyprší čas
        if int(self.time) % 60 == 0:
            time.sleep(0.3)
            view = End_lose()
            self.window.show_view(view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    start_view = Start_view()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()


