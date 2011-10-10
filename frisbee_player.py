from pygame import sprite, Rect, Surface
PLAYER_WIDTH = 1

class Frisbee_Player(sprite.Sprite):
    def __init__(self, initial_position, color, field_scalar=1.0):
        sprite.Sprite.__init__(self)
        self.radius = int(PLAYER_WIDTH * field_scalar)
        self.image = Surface([field_scalar, field_scalar])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position 

    def update(self):
        self.rect.move_ip(10, 10)
