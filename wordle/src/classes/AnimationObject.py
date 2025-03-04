from enum import Enum
from constants import DEFAULT_FRAMERATE



# enum to hold the direction of animation
class Direction(Enum):
    up = "up"
    down = "down"


# Class to extend classes into animation objects
class AnimationObject:
    def __init__(self):
        self.active = False
        self.lower_bound = 0
        self.upper_bound = 0
        self.direction: Direction | None = None
        self.step_size: float = 0
        self.current_offset: float = 0
        self.current_stage = 0
        self.total_stages = 0
        self.end_at_origin = False

    def start_jump_animation(self, height: int, duration: int):
        self.active = True
        self.step_size = height * 2 / (DEFAULT_FRAMERATE / 1000 * duration)
        self.direction = Direction.up
        self.lower_bound = 0
        self.upper_bound = -height
        self.current_offset = 0
        self.current_stage = 1
        self.total_stages = 2
        self.end_at_origin = False

    def start_shaking_animation(self, height: int, duration: int, num_shakes: int):
        self.active = True
        self.step_size = height * (num_shakes * 4) / \
            (DEFAULT_FRAMERATE / 1000 * duration)
        self.direction = Direction.up
        self.lower_bound = height
        self.upper_bound = -height
        self.current_offset = 0
        self.current_stage = 1
        self.total_stages = num_shakes * 2 + 1
        self.end_at_origin = True

    def update_animation_frame(self):
        if not self.active or not self.direction:
            return 0

        # check which direction of movement
        match self.direction:
            case Direction.up:
                y = self.current_offset - self.step_size
                if y >= self.upper_bound:  # keep moving in same direction
                    self.current_offset = y
                else:  # breakpoint -> finish or change directions
                    if self.current_stage == self.total_stages:
                        self.active = False
                    elif self.end_at_origin and self.current_stage == self.total_stages - 1:
                        self.lower_bound = 0

                    self.direction = Direction.down
                    self.current_stage += 1

            case Direction.down:
                y = self.current_offset + self.step_size
                if y <= self.lower_bound:  # keep moving in same direction
                    self.current_offset = y
                else:  # breakpoint -> finish or change directions
                    if self.current_stage == self.total_stages:
                        self.active = False
                    elif self.end_at_origin and self.current_stage == self.total_stages - 1:
                        self.upper_bound = 0

                    self.direction = Direction.up
                    self.current_stage += 1

        return self.current_offset
