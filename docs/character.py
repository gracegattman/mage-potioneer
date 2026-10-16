import pygame  # Import the pygame library to use its functionalities for 2D graphics and sound.
from progress import power_ups

class Character(pygame.sprite.Sprite):  # Define a class `Character` that inherits from pygame's `Sprite` class.
    def __init__(self, position):  # Initialize the character object with a starting position.
    
        super().__init__()
        # Load the image file (spritesheet) into the `sheet` attribute.
        self.idle_sheet = pygame.image.load('assets/spritesheet/main_char_idle.png')
        self.run_sheet = pygame.image.load('assets/spritesheet/main_char_run.png')
        
        # Set up animation loops for character        
        self.anim = self.load_anim()

        # Get default state for load in
        self.direction = "down"
        self.state = "idle"
        self.frame = 0
        self.frame_delay = 75
        self.last_update = pygame.time.get_ticks()  # Track the last time the frame was updated
        
        # Set the top-left position of the sprite on the screen using the position parameter.
        self.image = self.anim[self.state][self.direction][self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        
        # Define the coordinates of each animation frame in the spritesheet for different directions.
        #self.left_states = {0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76)}
        #self.right_states = {0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76)}
        #self.up_states = {0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76)}
        #self.down_states = {0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76)}

    def load_anim(self):  # Get the next frame in the given frame set (animation loop).
        anims = {"idle": {}, "run": {}}
        sheets = {"idle": self.idle_sheet, "run": self.run_sheet}

        for state, sheet in sheets.items():
            for index, dir in enumerate(["up", "down", "left", "right"]):
                row_frames = []
                sheet_w, sheet_h = sheet.get_size()
                frames_per_row = sheet_w // 40

                for frame in range(frames_per_row):
                    if state == "idle":
                        x = frame * 40
                        y = index * 40
                        frame_rect_surface = sheet.subsurface(pygame.Rect(x,y,40,40))
                    else:
                        x = frame * 40
                        y = index * 42
                        frame_rect_surface = sheet.subsurface(pygame.Rect(x,y,40,42))
                    row_frames.append(frame_rect_surface)
                anims[state][dir] = row_frames
        return anims


    def update(self, state, direction, dont_walk=None):  # Update the character's position and animation based on the direction.
        speed = 3
        if power_ups["speed_boost"]:
            speed = 6
        move = state == "run"

        old_x, old_y = self.rect.x, self.rect.y
        
        if move:
            self.state = "run"

            if direction == 'left':  # Move left and play left walking animation.
                self.rect.x -= speed  # Move the sprite left by [speed] pixels.
            if direction == 'right':  # Move right and play right walking animation.
                self.rect.x += speed
            if direction == 'up':  # Move up and play up walking animation.
                self.rect.y -= speed
            if direction == 'down':  # Move down and play down walking animation.
                self.rect.y += speed
        
        else:
            self.state = "idle"

        # sub-collision handling (for props, etc)
        if dont_walk:
            for i in dont_walk:
                if self.rect.colliderect(i):
                    self.rect.x, self.rect.y = old_x, old_y
                    break

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1600:
            self.rect.right = 1600
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 1600:
            self.rect.bottom = 1600

        # animation handling
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.frame = (self.frame + 1) % len(self.anim[self.state][self.direction])
            self.image = self.anim[self.state][self.direction][self.frame]


    def handle_event(self, event):  # Handle keyboard events to move the character or stop movement.
        if event.type == pygame.KEYDOWN:  # If a key is pressed down:
            if event.key == pygame.K_LEFT:  # Move left if the left arrow is pressed.
                self.direction = 'left'
                self.update('run', 'left')
            if event.key == pygame.K_RIGHT:  # Move right if the right arrow is pressed.
                self.direction = 'right'
                self.update('run', 'right')
            if event.key == pygame.K_UP:  # Move up if the up arrow is pressed.
                self.direction = 'up'
                self.update('run', 'up')
            if event.key == pygame.K_DOWN:  # Move down if the down arrow is pressed.
                self.direction = 'down'
                self.update('run', 'down')

        if event.type == pygame.KEYUP:  # If a key is released (stop movement):
            if event.key == pygame.K_LEFT:  # Stop and stand facing left.
                self.direction = 'left'
                self.update('idle', 'left')
            if event.key == pygame.K_RIGHT:  # Stop and stand facing right.
                self.direction = 'right'
                self.update('idle', 'right')
            if event.key == pygame.K_UP:  # Stop and stand facing up.
                self.direction = 'up'
                self.update('idle', 'up')
            if event.key == pygame.K_DOWN:  # Stop and stand facing down.
                self.direction = 'down'
                self.update('idle', 'down')
