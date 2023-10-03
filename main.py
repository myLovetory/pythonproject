import pygame as pg 
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import  *
from weapon import *
from sound import *

class Game:
    
    #tao man hinh va gan fps
    def __init__(self):
        pg.init()
        #check mouse và cho mouse vô hình
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        
        #delta time for frame
        self.delta_time = 1
        self.new_game()
       
    #phuong thuc new game  
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self) 
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        #self.static_sprite = SpriteObject(self)
        #self.animated_sprite = AnimatedSprite(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        
    #update de cap nhat 
    def update(self):
        self.player.update()
        self.raycasting.update()
        #self.static_sprite.update()
        #self.animated_sprite.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        

    #ve man den moi khi refrese 1 frame
    def draw(self):
        #self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        #self.map.draw()
        #self.player.draw()
        
    #ham check cac event
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            #check fire event
            self.player.single_fire_event(event)
    
    #while loop 
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
if __name__ == '__main__':
    game = Game()
    game.run()