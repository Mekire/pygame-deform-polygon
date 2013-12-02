import os
import sys
import math
import pygame as pg


CAPTION = "Deform"
SCREEN_SIZE = (500,500)
POINT_SIZE = (10,10)
RADIUS = 100


class Point(pg.sprite.Sprite):
    def __init__(self,point):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(POINT_SIZE).convert()
        self.image.fill(pg.Color("green"))
        self.rect = self.image.get_rect(center=point)
        self.clicked = False

    def update(self,surface_rect):
        if self.clicked:
            self.rect.move_ip(pg.mouse.get_rel())
            self.rect.clamp_ip(surface_rect)


class Control(object):
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.done = False
        self.keys = pg.key.get_pressed()
        self.points = self.make_points(self.screen_rect.center,RADIUS)
        self.draw_points = [point.rect.center for point in self.points]

    def make_points(self,offset,scale):
        x,y = offset
        angle_72 = math.radians(72)
        angle_36 = math.radians(36)
        points = []
        points.append((x+scale, y))
        points.append((x+scale*math.cos(angle_72), y-scale*math.sin(angle_72)))
        points.append((x-scale*math.cos(angle_36), y-scale*math.sin(angle_36)))
        points.append((x-scale*math.cos(angle_36), y+scale*math.sin(angle_36)))
        points.append((x+scale*math.cos(angle_72), y+scale*math.sin(angle_72)))
        control_points = [Point(pair) for pair in points]
        return pg.sprite.OrderedUpdates(*control_points)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for point in self.points:
                    if point.rect.collidepoint(event.pos):
                        pg.mouse.get_rel()
                        point.clicked = True
                        break
            elif event.type == pg.MOUSEBUTTONUP:
                for point in self.points:
                    point.clicked = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    center = self.screen_rect.center
                    self.points = self.make_points(center,RADIUS)

    def update(self):
        self.points.update(self.screen_rect)
        self.draw_points = [point.rect.center for point in self.points]

    def draw(self,surface):
        surface.fill(pg.Color("black"))
        pg.draw.polygon(surface,pg.Color("red"),self.draw_points)
        self.points.draw(surface)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.draw(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)
            caption = "{} - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
            pg.display.set_caption(caption)


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()