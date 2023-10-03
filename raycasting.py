'''
hàm này dùng thuật toán ray casting để thiết lập góc nhìn của người chơi trong game
'''
import pygame as pg
import math
from settings import *

class RayCasting:
    
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures =  self.game.object_renderer.wall_textures
        
    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            #chính sửa hiệu suất hình ảnh khi đi xa và đi gần
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))
    
    def ray_cast(self):
        self.ray_casting_result = []
        #toa do ng choi
        ox, oy = self.game.player.pos
        #tru sai so 0,0001 giua hai goc
        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        
        #toa do vat the 
        x_map, y_map = self.game.player.map_pos
        
        texture_vert, texture_hor = 1, 1
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            
            #xử lý va chạm ngang
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            #do xau tiep cho truyen thang
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor),int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
        
            #toa do tia va cham cheo 
            #cai nay thi ve ra so do rieng
            
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            
            #khoang cach tu player to vật cản
            depth_vert = (x_vert - ox) / cos_a
            #tinh y vert dựa vào hàm lượng giác
            y_vert = oy + depth_vert * sin_a
            
            #khoảng cách từ đó đến giao điểm tiếp theo của tia
            delta_depth = dx / cos_a
            #khoảng cách trục y từ điểm đầu đến giao điểm sau
            dy = delta_depth * sin_a
            
            #check truyền tia và va chạm
            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                #check tầm nhìn va chạm với tường
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                
                #tiếp tục truyền tia
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
                
            #duyệt tia va chạm
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor
            
            #drawline for debug
            #pg.draw.line(self.game.screen ,'yellow',(100 * ox, 100 * oy),
            #            (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)    
            #ray_angle += DELTA_ANGLE
            
            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)
            
            proj_height = SCREEN_DIST / (depth + 0.0001)
            
            #vẽ tường
            
            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()