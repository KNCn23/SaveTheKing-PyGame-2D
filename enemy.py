import pygame
import math

class Enemy:
    def __init__(self, x, y, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_vitality = hp
        self.attack_power = attack_power

        self.image_rect = pygame.Rect(x, y, 32, 48)
        self.hitbox = pygame.Rect(x, y + 28, 32, 20)

        self.speed = 2
        self.detection_range = 260
        self.start_x = x
        self.patrol_range = 100
        self.direction = 1

        # ranged enemies keep their distance and attack from afar
        self.is_ranged = "archer" in name.lower()
        self.attack_range = 175 if self.is_ranged else 42

        self.is_hit = False
        self.hit_timer = 0
        self.last_attack_time = 0
        self.attack_cooldown = 800

    def update(self, player_hitbox, walls):
        dx = player_hitbox.centerx - self.hitbox.centerx
        dy = player_hitbox.centery - self.hitbox.centery
        dist = math.sqrt(dx**2 + dy**2)

        if dist < self.detection_range:
            # only close in if we're outside attack range
            if dist > self.attack_range and dist != 0:
                self.speed = 3
                move_x = (dx / dist) * self.speed
                move_y = (dy / dist) * self.speed
                self.hitbox.x += move_x
                if self.hitbox.colliderect(player_hitbox):
                    self.hitbox.x -= move_x
                self.hitbox.y += move_y
                if self.hitbox.colliderect(player_hitbox):
                    self.hitbox.y -= move_y
        else:
            self.speed = 2
            self.hitbox.x += self.speed * self.direction
            if abs(self.hitbox.x - self.start_x) > self.patrol_range:
                self.direction *= -1

        self.image_rect.midbottom = self.hitbox.midbottom

    def take_damage(self, amount):
        self.hp -= amount
        self.is_hit = True
        self.hit_timer = pygame.time.get_ticks()
        return self.hp <= 0

    def draw(self, surface):
        now = pygame.time.get_ticks()
        if self.is_hit and now - self.hit_timer < 150:
            color = (255, 255, 255)
        elif self.is_ranged:
            color = (180, 80, 200)
        else:
            color = (200, 50, 50)

        if self.is_hit and now - self.hit_timer >= 150:
            self.is_hit = False

        pygame.draw.rect(surface, color, self.image_rect)

        bar_w = self.image_rect.width
        bar_h = 5
        bar_x = self.image_rect.left
        bar_y = self.image_rect.bottom + 3
        ratio = max(0, self.hp / self.max_vitality)

        pygame.draw.rect(surface, (120, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (220, 50, 50), (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1)
