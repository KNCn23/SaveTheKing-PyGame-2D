import pygame
import math
import random
from config import SCREEN_WIDTH

KING_COLOR = (220, 180, 50)
KING_OUTLINE = (255, 230, 100)
FOLLOW_DIST = 80
KING_SPEED = 2.5

class King:
    def __init__(self, x, y):
        self.max_vitality = 80
        self.vitality = 80
        self.is_alive = True

        self.image_rect = pygame.Rect(x, y, 28, 44)
        self.hitbox = pygame.Rect(x, y + 26, 28, 18)

        self.is_hit = False
        self.hit_timer = 0
        self.hit_cooldown = 800

        self._label_font = pygame.font.SysFont("arial", 13, bold=True)
        self._bar_font = pygame.font.SysFont("arial", 13)
        self._label_surf = self._label_font.render("KING", True, (255, 255, 255))

    def update(self, player_hitbox, walls):
        dx = player_hitbox.centerx - self.hitbox.centerx
        dy = player_hitbox.centery - self.hitbox.centery
        dist = math.sqrt(dx**2 + dy**2)

        if dist > FOLLOW_DIST:
            move_x = (dx / dist) * KING_SPEED
            move_y = (dy / dist) * KING_SPEED

            self.hitbox.x += move_x
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    if move_x > 0: self.hitbox.right = wall.left
                    if move_x < 0: self.hitbox.left = wall.right

            self.hitbox.y += move_y
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    if move_y > 0: self.hitbox.bottom = wall.top
                    if move_y < 0: self.hitbox.top = wall.bottom

        self.image_rect.midbottom = self.hitbox.midbottom

    def take_damage(self, amount):
        if self.is_hit:
            return
        self.vitality -= amount
        self.is_hit = True
        self.hit_timer = pygame.time.get_ticks()
        if self.vitality <= 0:
            self.vitality = 0
            self.is_alive = False

    def on_room_change(self, player_hitbox):
        self.hitbox.centerx = player_hitbox.centerx - 50
        self.hitbox.centery = player_hitbox.centery
        self.image_rect.midbottom = self.hitbox.midbottom

    def draw(self, surface):
        if self.is_hit:
            elapsed = pygame.time.get_ticks() - self.hit_timer
            color = (220, 60, 60) if elapsed < 400 else KING_COLOR
            if elapsed >= 400:
                self.is_hit = False
        else:
            color = KING_COLOR

        pygame.draw.rect(surface, color, self.image_rect)
        pygame.draw.rect(surface, KING_OUTLINE, self.image_rect, 2)

        surface.blit(self._label_surf, (self.image_rect.centerx - self._label_surf.get_width() // 2, self.image_rect.top - 18))

    def draw_hp_bar(self, surface):
        bar_x, bar_y = surface.get_width() - 220, 50
        bar_w, bar_h = 200, 16
        ratio = max(0, self.vitality / self.max_vitality)

        pygame.draw.rect(surface, (120, 80, 0), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, (220, 180, 50), (bar_x, bar_y, int(bar_w * ratio), bar_h))
        pygame.draw.rect(surface, (255, 230, 100), (bar_x, bar_y, bar_w, bar_h), 2)

        txt = self._bar_font.render(f"King Vitality  {self.vitality}/{self.max_vitality}", True, (255, 240, 180))
        surface.blit(txt, txt.get_rect(center=(bar_x + bar_w // 2, bar_y + bar_h // 2)))


RIDDLE_POOL = [
    {"q": "If you speak my name, you break me. What am I?",
     "a": ["silence"]},
    {"q": "I have cities but no houses, mountains but no trees, water but no fish. What am I?",
     "a": ["map"]},
    {"q": "The more you take, the more you leave behind. What are they?",
     "a": ["footsteps", "steps"]},
    {"q": "The maker doesn't want it; the buyer doesn't use it; the user doesn't see it. What is it?",
     "a": ["coffin"]},
    {"q": "If you have me, you want to share me. If you share me, you haven't got me. What am I?",
     "a": ["secret"]},
]

class Guard:
    GATE_LOCK_Y = 30

    def __init__(self, x, y):
        self.image_rect = pygame.Rect(x, y, 32, 48)
        self.hitbox = pygame.Rect(x, y + 28, 32, 20)

        self.riddle = random.choice(RIDDLE_POOL)
        self.mistakes = 0
        self.is_hostile = False
        self.gate_open = False
        self.asked_already = False

        self.attack_power = 20
        self.speed = 2
        self.start_x = x
        self.hp = 120
        self.last_attack_time = 0
        self.attack_cooldown = 800

        self._font = pygame.font.SysFont("arial", 13, bold=True)
        self._label_surf = self._font.render("GUARD", True, (255, 255, 255))
        self._color = (100, 120, 200)

    def check_approach(self, player_hitbox):
        if self.gate_open or self.asked_already or self.is_hostile:
            return False
        dist_x = abs(player_hitbox.centerx - self.hitbox.centerx)
        dist_y = abs(player_hitbox.centery - self.hitbox.centery)
        return dist_x < 80 and dist_y < 80

    def answer(self, text):
        if text.strip().lower() in self.riddle["a"]:
            self.gate_open = True
            self.asked_already = True
            return "correct"

        self.mistakes += 1
        if self.mistakes >= 3:
            self.is_hostile = True
            self.asked_already = True
            return "failed"
        return "wrong"

    def update(self, player_hitbox, walls):
        if not self.is_hostile:
            return

        dx = player_hitbox.centerx - self.hitbox.centerx
        dy = player_hitbox.centery - self.hitbox.centery
        dist = math.sqrt(dx**2 + dy**2)

        if dist > 0:
            move_x = (dx / dist) * self.speed
            move_y = (dy / dist) * self.speed

            self.hitbox.x += move_x
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    if move_x > 0: self.hitbox.right = wall.left
                    else: self.hitbox.left = wall.right

            self.hitbox.y += move_y
            for wall in walls:
                if self.hitbox.colliderect(wall):
                    if move_y > 0: self.hitbox.bottom = wall.top
                    else: self.hitbox.top = wall.bottom

        self.image_rect.midbottom = self.hitbox.midbottom

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0

    def draw(self, surface):
        color = (180, 50, 50) if self.is_hostile else self._color
        pygame.draw.rect(surface, color, self.image_rect)
        pygame.draw.rect(surface, (255, 255, 255), self.image_rect, 2)

        surface.blit(self._label_surf, (self.image_rect.centerx - self._label_surf.get_width() // 2, self.image_rect.top - 18))


NPC_COLORS = {
    "merchant": (200, 160, 50),
    "knight": (100, 120, 200),
    "villager": (160, 120, 80),
}
NPC_LABELS = {
    "merchant": "Merchant",
    "knight": "Knight",
    "villager": "Villager",
}

VILLAGER_DIALOGUES = {
    "hero": [
        "You killed the Bandit Leader! You are our hero!",
        "We are finally free! Please, take whatever you need.",
        "I knew you were a savior the moment I saw you!",
        "The King will surely reward you for this!",
    ],
    "suspicious": [
        "Get out! You look just like those bandits!",
        "Did you kill the knights? Stay away from my family!",
        "I don't trust you. You have blood on your hands.",
        "Don't hurt me! Take what you want and leave!",
    ],
    "info": [
        "I saw smoke rising from the deep forest. The bandit camp must be there.",
        "The Mayor hid something in the archives before he fled. But it's locked.",
        "Be careful on the cliffs. The ground is unstable.",
        "I heard the merchant in the town square likes gold coins.",
        "Those bandits... they have heavy armor. You'll need a strong weapon.",
    ],
    "friendly": [
        "Please help us... We have no food left.",
        "May the gods protect you, traveler.",
        "It's dangerous to go alone. Watch your back.",
        "If you see the King, tell him we are still loyal.",
    ],
    "attack": "I won't let you hurt anyone else! DIE TRAITOR!",
}

class NPC:
    def __init__(self, x, y, npc_type):
        self.npc_type = npc_type
        self.color = NPC_COLORS.get(npc_type, (180, 180, 180))
        self.label = NPC_LABELS.get(npc_type, npc_type.capitalize())
        self.image_rect = pygame.Rect(x, y, 32, 48)
        self.hitbox = pygame.Rect(x, y + 28, 32, 20)
        self._font = pygame.font.SysFont("arial", 14, bold=True)
        self._label_surf = self._font.render(self.label, True, (255, 255, 255))

        self.dialogue = ""
        self.is_hostile = False
        self.attack_power = 5
        self.hp = 30
        self.is_hit = False
        self.hit_timer = 0
        self.last_attack_time = 0
        self.attack_cooldown = 800
        self._talked = False

    def trigger_villager(self, bandit_camp_cleared):
        if self.npc_type != "villager" or self._talked:
            return "", False

        self._talked = True

        if bandit_camp_cleared:
            self.dialogue = random.choice(VILLAGER_DIALOGUES["hero"])
            return self.dialogue, False

        roll = random.randint(1, 100)

        if roll <= 10:
            self.dialogue = VILLAGER_DIALOGUES["attack"]
            self.is_hostile = True
            return self.dialogue, True
        elif roll <= 40:
            self.dialogue = random.choice(VILLAGER_DIALOGUES["suspicious"])
        elif roll <= 70:
            self.dialogue = random.choice(VILLAGER_DIALOGUES["info"])
        else:
            self.dialogue = random.choice(VILLAGER_DIALOGUES["friendly"])

        return self.dialogue, False

    def take_damage(self, amount):
        self.hp -= amount
        self.is_hit = True
        self.hit_timer = pygame.time.get_ticks()
        return self.hp <= 0

    def update(self, player_hitbox):
        if not self.is_hostile:
            return
        dx = player_hitbox.centerx - self.hitbox.centerx
        dy = player_hitbox.centery - self.hitbox.centery
        dist = math.sqrt(dx**2 + dy**2) or 1
        self.hitbox.x += (dx / dist) * 1.5
        self.hitbox.y += (dy / dist) * 1.5
        self.image_rect.midbottom = self.hitbox.midbottom

    def draw(self, surface):
        now = pygame.time.get_ticks()
        if self.is_hit and now - self.hit_timer < 150:
            color = (255, 255, 255)
        elif self.is_hostile:
            color = (180, 50, 50)
        else:
            color = self.color

        if self.is_hit and now - self.hit_timer >= 150:
            self.is_hit = False

        pygame.draw.rect(surface, color, self.image_rect)
        pygame.draw.rect(surface, (255, 255, 255), self.image_rect, 2)

        surface.blit(self._label_surf, (self.image_rect.centerx - self._label_surf.get_width() // 2, self.image_rect.top - 18))
