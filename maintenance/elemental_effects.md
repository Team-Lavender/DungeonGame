
## Elemental Effects
`elemental_effects.py` contains classes for elemental effects in the game, such as acid pools and explosions. this allows for easy creation of hazardous surfaces and the like in the game. these effects are added when their constructor is called and removed from the game when their time limit expires. this allows for flexible usage such as in throwables and projectile on hit effects.
### Adding new elements
To create a new elemental effect a new elemental class must be created with its own render method and method to be called when it activates. this method should be called when the effect is instantiated in its init function and the effect added to the games list of elemental effects in the game. The render method provides the functionality to remove the effect after its animation plays out.
 ```python
class Explosion:
    def __init__(self, game, damage, size, pos_x, pos_y):
        self.game = game
        self.damage = damage
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprite = config.get_magic_sprite("explosion")["idle"]
        # height is size times 2 times a cell width
        self.height = self.size * 16 * 2
        self.width = self.height * 114 / 64 # aspect ratio of explosion
        self.frame = 0
        self.update_frame = 0
        self.rendering = True
        self.explosion()
        self.game.elemental_surfaces.append(self)

    def explosion(self):
        for actor in self.game.curr_actors:
            if isinstance(actor, Entity):
                if abs(actor.pos_x - self.pos_x) <= self.width / 2 and abs(
                        actor.pos_y - self.pos_y) <= self.height / 2:
                    actor.take_damage(self.damage)
        audio.explosion()

    def render(self):

        frames = self.sprite
        anim_length = len(frames)

        # render animation if it exists
        if frames is not None:
            curr_frame = frames[self.frame]
            curr_height = curr_frame.get_height()
            curr_frame = pygame.transform.scale(curr_frame, (round(curr_frame.get_width() * self.height / curr_height), round(self.height)))
            frame_rect = curr_frame.get_rect()
            frame_rect.center = (self.pos_x, self.pos_y)
            self.game.display.blit(curr_frame, frame_rect)

        if self.update_frame == 0:
            self.frame = (self.frame + 1) % anim_length
        if self.frame == anim_length - 1:
            self.game.elemental_surfaces.remove(self)
```


