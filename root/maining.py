from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

import pygame


pygame.init()

WIDTH, HEIGHT = 1280, 720
PLAY_HEIGHT = 630
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEAD SIGNAL")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 20)
SMALL = pygame.font.SysFont("consolas", 15)
BIG = pygame.font.SysFont("consolas", 52, bold=True)

Vec = pygame.Vector2
Color = tuple[int, int, int]

WHITE: Color = (230, 240, 245)
RED: Color = (255, 85, 95)
GREEN: Color = (105, 240, 145)
BLUE: Color = (90, 185, 255)
GOLD: Color = (255, 205, 100)

CHAPTERS = [
    ("THE HOTEL", "Reach the blue safe-room door."),
    ("THE STREETS", "Cross the streets. Stay together."),
    ("THE HOSPITAL", "Defeat the Tank, then reach evacuation."),
]

# Health, speed, damage, radius, color.
ENEMY_STATS: dict[str, tuple[int, float, int, int, Color]] = {
    "common": (3, 83.0, 7, 12, GREEN),
    "hunter": (5, 145.0, 10, 12, (185, 115, 255)),
    "boomer": (7, 65.0, 8, 18, (180, 220, 70)),
    "tank": (65, 58.0, 20, 29, RED),
}


@dataclass
class Actor:
    pos: pygame.Vector2
    name: str
    hp: int = 100
    radius: int = 12
    cooldown: float = 0.0
    hurt_timer: float = 0.0


@dataclass
class Player(Actor):
    magazine: int = 30
    reserve: int = 150
    reload_timer: float = 0.0
    stamina: float = 100.0
    aim: pygame.Vector2 = field(default_factory=lambda: Vec(1, 0))


@dataclass
class Enemy:
    pos: pygame.Vector2
    kind: str = "common"
    hp: int = field(init=False)
    speed: float = field(init=False)
    damage: int = field(init=False)
    radius: int = field(init=False)
    color: Color = field(init=False)
    cooldown: float = 0.0
    hurt_timer: float = 0.0

    def __post_init__(self) -> None:
        stats = ENEMY_STATS[self.kind]
        self.hp, self.speed, self.damage, self.radius, self.color = stats


@dataclass
class Bullet:
    pos: pygame.Vector2
    velocity: pygame.Vector2
    life: float = 1.1


@dataclass
class Particle:
    pos: pygame.Vector2
    velocity: pygame.Vector2
    color: Color
    life: float
    size: int


@dataclass
class Pickup:
    pos: pygame.Vector2
    kind: str


def point(pos: pygame.Vector2) -> tuple[int, int]:
    return round(pos.x), round(pos.y)


def text(
    message: str,
    x: int,
    y: int,
    color: Color = WHITE,
    font: pygame.font.Font = FONT,
) -> None:
    screen.blit(font.render(message, True, color), (x, y))


def center_text(
    message: str,
    y: int,
    color: Color = WHITE,
    font: pygame.font.Font = FONT,
) -> None:
    image = font.render(message, True, color)
    screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))


def blocked(
    pos: pygame.Vector2,
    radius: int,
    walls: list[pygame.Rect],
) -> bool:
    if not (
        radius <= pos.x <= WIDTH - radius
        and radius <= pos.y <= PLAY_HEIGHT - radius
    ):
        return True

    box = pygame.Rect(
        round(pos.x - radius),
        round(pos.y - radius),
        radius * 2,
        radius * 2,
    )
    return any(box.colliderect(wall) for wall in walls)


def move_actor(
    pos: pygame.Vector2,
    delta: pygame.Vector2,
    radius: int,
    walls: list[pygame.Rect],
) -> None:
    candidate = pos + Vec(delta.x, 0)
    if not blocked(candidate, radius, walls):
        pos.x = candidate.x

    candidate = pos + Vec(0, delta.y)
    if not blocked(candidate, radius, walls):
        pos.y = candidate.y


def clear_line(
    start: pygame.Vector2,
    end: pygame.Vector2,
    walls: list[pygame.Rect],
) -> bool:
    return not any(
        wall.clipline(point(start), point(end))
        for wall in walls
    )


def draw_bar(
    x: int,
    y: int,
    width: int,
    fraction: float,
    color: Color,
) -> None:
    pygame.draw.rect(
        screen, (30, 40, 50), (x, y, width, 6), border_radius=3
    )
    fill = round(width * max(0.0, min(1.0, fraction)))
    if fill:
        pygame.draw.rect(
            screen, color, (x, y, fill, 6), border_radius=3
        )


# Reusable glow images avoid recreating them every frame.
GLOW_CACHE: dict[tuple[Color, int], pygame.Surface] = {}


def glow(pos: pygame.Vector2, color: Color, radius: int) -> None:
    key = (color, radius)
    if key not in GLOW_CACHE:
        image = pygame.Surface(
            (radius * 2, radius * 2), pygame.SRCALPHA
        )
        for layer in range(10, 0, -1):
            pygame.draw.circle(
                image,
                (*color, 7 + (10 - layer) * 2),
                (radius, radius),
                max(1, radius * layer // 10),
            )
        GLOW_CACHE[key] = image

    screen.blit(
        GLOW_CACHE[key],
        (round(pos.x) - radius, round(pos.y) - radius),
    )


def draw_character(
    pos: pygame.Vector2,
    facing: pygame.Vector2,
    color: Color,
    radius: int,
    hurt: bool = False,
    armed: bool = True,
) -> None:
    direction = (
        facing.normalize()
        if facing.length_squared() > 0
        else Vec(1, 0)
    )
    side = Vec(-direction.y, direction.x)
    x, y = point(pos)

    pygame.draw.ellipse(
        screen,
        (4, 7, 11),
        (x - radius - 3, y + 4, radius * 2 + 6, radius + 6),
    )

    for sign in (-1, 1):
        boot = pos - direction * 7 + side * sign * 6
        pygame.draw.circle(screen, (10, 15, 22), point(boot), 5)

    body_color = WHITE if hurt else color
    pygame.draw.line(
        screen,
        body_color,
        point(pos - side * radius * 0.65),
        point(pos + side * radius * 0.65),
        max(6, radius),
    )
    pygame.draw.circle(screen, (25, 35, 45), (x, y), radius - 3)
    pygame.draw.circle(screen, body_color, (x, y), radius, 2)

    head = pos + direction * 5
    pygame.draw.circle(
        screen,
        (175, 157, 132) if armed else (135, 155, 122),
        point(head),
        max(4, radius // 3),
    )

    if armed:
        start = pos + side * 5
        end = start + direction * (radius + 17)
        pygame.draw.line(screen, (5, 9, 13), point(start), point(end), 7)
        pygame.draw.line(
            screen, (135, 150, 165), point(start), point(end), 3
        )
    else:
        for sign in (-1, 1):
            eye = head + direction * 3 + side * sign * 3
            pygame.draw.circle(screen, RED, point(eye), 2)


class Game:
    def __init__(self) -> None:
        self.chapter = 0
        self.kills = 0
        self.state = "title"
        self.elapsed = 0.0
        self.shake = 0.0
        self.banner_timer = 0.0
        self.horde_timer = 12.0
        self.start_delay = 0.0

        self.walls: list[pygame.Rect] = []
        self.enemies: list[Enemy] = []
        self.bullets: list[Bullet] = []
        self.particles: list[Particle] = []
        self.pickups: list[Pickup] = []
        self.allies: list[Actor] = []

        self.player = Player(Vec(80, 315), "YOU")
        self.exit_zone = pygame.Rect(WIDTH - 85, 260, 65, 110)

        self.load_level()

    def load_level(self) -> None:
        # A clear central road connects the spawn to the exit.
        self.walls = [
            pygame.Rect(230, 90, 180, 95),
            pygame.Rect(500, 65, 95, 155),
            pygame.Rect(760, 85, 200, 80),
            pygame.Rect(290, 435, 180, 105),
            pygame.Rect(610, 410, 100, 160),
            pygame.Rect(900, 450, 160, 90),
        ]

        self.player = Player(Vec(80, 315), "YOU")
        self.allies = [
            Actor(Vec(65, 260), "MAYA", hp=75),
            Actor(Vec(65, 370), "COLE", hp=75),
            Actor(Vec(120, 315), "JUNE", hp=75),
        ]

        self.enemies.clear()
        self.bullets.clear()
        self.particles.clear()

        self.pickups = [
            Pickup(Vec(180, 315), "ammo"),
            Pickup(Vec(460, 285), "medkit"),
            Pickup(Vec(735, 345), "bomb"),
            Pickup(Vec(1030, 280), "ammo"),
        ]

        self.horde_timer = 12.0
        self.banner_timer = 3.0
        self.shake = 0.0
        self.start_delay = 0.2

        for _ in range(9 + self.chapter * 4):
            self.spawn_enemy(initial=True)

        if self.chapter >= 1:
            self.spawn_enemy("hunter", initial=True)
            self.spawn_enemy("boomer", initial=True)

        if self.chapter == 2:
            self.enemies.append(Enemy(Vec(1100, 315), "tank"))

    def restart(self) -> None:
        self.chapter = 0
        self.kills = 0
        self.load_level()
        self.state = "play"

    def spawn_enemy(
        self,
        kind: str = "common",
        initial: bool = False,
    ) -> None:
        for _ in range(100):
            if initial:
                pos = Vec(
                    random.randint(750, WIDTH - 45),
                    random.randint(35, PLAY_HEIGHT - 35),
                )
            else:
                edge = random.randrange(4)
                if edge == 0:
                    pos = Vec(35, random.randint(35, PLAY_HEIGHT - 35))
                elif edge == 1:
                    pos = Vec(
                        WIDTH - 35,
                        random.randint(35, PLAY_HEIGHT - 35),
                    )
                elif edge == 2:
                    pos = Vec(random.randint(35, WIDTH - 35), 35)
                else:
                    pos = Vec(
                        random.randint(35, WIDTH - 35),
                        PLAY_HEIGHT - 35,
                    )

            if (
                not blocked(pos, ENEMY_STATS[kind][3], self.walls)
                and pos.distance_to(self.player.pos) > 220
            ):
                self.enemies.append(Enemy(pos, kind))
                return

    def burst(
        self,
        pos: pygame.Vector2,
        color: Color,
        count: int = 12,
    ) -> None:
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(35, 190)
            velocity = Vec(math.cos(angle), math.sin(angle)) * speed
            self.particles.append(
                Particle(
                    pos.copy(),
                    velocity,
                    color,
                    random.uniform(0.15, 0.45),
                    random.randint(2, 4),
                )
            )

    def fire(
        self,
        pos: pygame.Vector2,
        direction: pygame.Vector2,
    ) -> None:
        if direction.length_squared() == 0:
            return

        direction = direction.normalize()
        self.bullets.append(
            Bullet(pos + direction * 19, direction * 800)
        )
        self.burst(pos + direction * 22, GOLD, 3)

    def reload(self) -> None:
        p = self.player
        if p.reload_timer <= 0 and p.magazine < 30 and p.reserve > 0:
            p.reload_timer = 1.2

    def collect(self) -> None:
        for item in self.pickups[:]:
            if item.pos.distance_to(self.player.pos) > 48:
                continue

            if item.kind == "medkit":
                if self.player.hp >= 100:
                    continue
                self.player.hp = min(100, self.player.hp + 45)

            elif item.kind == "ammo":
                self.player.reserve += 90

            elif item.kind == "bomb":
                self.burst(item.pos, GOLD, 65)
                self.shake = 0.35
                for enemy in self.enemies:
                    if enemy.pos.distance_to(item.pos) < 280:
                        enemy.hp -= 18

            self.pickups.remove(item)

    def update(self, dt: float) -> None:
        self.shake = max(0.0, self.shake - dt)
        self.banner_timer = max(0.0, self.banner_timer - dt)
        self.start_delay = max(0.0, self.start_delay - dt)

        p = self.player
        keys = pygame.key.get_pressed()

        movement = Vec(
            int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
            int(keys[pygame.K_s]) - int(keys[pygame.K_w]),
        )
        aiming = Vec(
            int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]),
            int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]),
        )

        if aiming.length_squared() > 0:
            p.aim = aiming.normalize()
        elif movement.length_squared() > 0:
            p.aim = movement.normalize()

        sprinting = (
            bool(keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
            and p.stamina > 1
            and movement.length_squared() > 0
        )
        speed = 260.0 if sprinting else 180.0

        if sprinting:
            p.stamina = max(0.0, p.stamina - 30 * dt)
        else:
            p.stamina = min(100.0, p.stamina + 20 * dt)

        if movement.length_squared() > 0:
            move_actor(
                p.pos,
                movement.normalize() * speed * dt,
                p.radius,
                self.walls,
            )

        p.cooldown = max(0.0, p.cooldown - dt)
        p.hurt_timer = max(0.0, p.hurt_timer - dt)

        if p.reload_timer > 0:
            p.reload_timer = max(0.0, p.reload_timer - dt)
            if p.reload_timer == 0:
                amount = min(30 - p.magazine, p.reserve)
                p.magazine += amount
                p.reserve -= amount

        if (
            keys[pygame.K_SPACE]
            and p.cooldown <= 0
            and p.reload_timer <= 0
            and p.magazine > 0
            and self.start_delay <= 0
        ):
            self.fire(p.pos, p.aim)
            p.magazine -= 1
            p.cooldown = 0.12

        # Teammates follow and shoot visible infected.
        for index, ally in enumerate(self.allies):
            if ally.hp <= 0:
                continue

            ally.cooldown = max(0.0, ally.cooldown - dt)
            ally.hurt_timer = max(0.0, ally.hurt_timer - dt)

            follow = p.pos + Vec(-45, (index - 1) * 45)
            direction = follow - ally.pos

            if direction.length() > 45:
                move_actor(
                    ally.pos,
                    direction.normalize() * 170 * dt,
                    ally.radius,
                    self.walls,
                )

            targets = [
                enemy
                for enemy in self.enemies
                if enemy.hp > 0
                and ally.pos.distance_to(enemy.pos) < 360
                and clear_line(ally.pos, enemy.pos, self.walls)
            ]

            if targets and ally.cooldown <= 0:
                target = min(
                    targets,
                    key=lambda enemy: ally.pos.distance_squared_to(
                        enemy.pos
                    ),
                )
                self.fire(ally.pos, target.pos - ally.pos)
                ally.cooldown = 0.45

        # Small projectile steps reduce missed collisions.
        for bullet in self.bullets[:]:
            bullet.life -= dt
            remove = bullet.life <= 0

            for _ in range(4):
                if remove:
                    break

                bullet.pos += bullet.velocity * (dt / 4)

                if blocked(bullet.pos, 2, self.walls):
                    remove = True
                    break

                for enemy in self.enemies:
                    if enemy.hp <= 0:
                        continue

                    if bullet.pos.distance_to(enemy.pos) < enemy.radius + 3:
                        enemy.hp -= 1
                        enemy.hurt_timer = 0.08
                        self.burst(bullet.pos, enemy.color, 5)
                        remove = True
                        break

            if remove:
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            if enemy.hp <= 0:
                self.kills += 1
                self.burst(enemy.pos, enemy.color, 18)
                self.enemies.remove(enemy)
                continue

            enemy.cooldown = max(0.0, enemy.cooldown - dt)
            enemy.hurt_timer = max(0.0, enemy.hurt_timer - dt)

            living: list[Actor] = [p]
            living.extend(ally for ally in self.allies if ally.hp > 0)

            target = min(
                living,
                key=lambda actor: actor.pos.distance_squared_to(
                    enemy.pos
                ),
            )

            direction = target.pos - enemy.pos
            distance = direction.length()

            if distance > 1:
                move_actor(
                    enemy.pos,
                    direction.normalize() * enemy.speed * dt,
                    enemy.radius,
                    self.walls,
                )

            if distance < enemy.radius + target.radius + 5:
                if enemy.cooldown <= 0:
                    target.hp = max(0, target.hp - enemy.damage)
                    target.hurt_timer = 0.18
                    enemy.cooldown = 0.75
                    self.burst(target.pos, RED, 10)

                    if target is p:
                        self.shake = 0.18

                    if enemy.kind == "boomer":
                        self.burst(enemy.pos, GREEN, 45)
                        for actor in living:
                            if actor.pos.distance_to(enemy.pos) < 130:
                                actor.hp = max(0, actor.hp - 8)
                        enemy.hp = 0

        for particle in self.particles[:]:
            particle.pos += particle.velocity * dt
            particle.velocity *= max(0.0, 1.0 - 5.0 * dt)
            particle.life -= dt
            if particle.life <= 0:
                self.particles.remove(particle)

        self.horde_timer -= dt
        if self.horde_timer <= 0:
            self.horde_timer = random.uniform(12, 17)
            for _ in range(6 + self.chapter * 2):
                self.spawn_enemy()

        if p.hp <= 0:
            self.state = "dead"
            return

        tank_alive = any(
            enemy.kind == "tank" and enemy.hp > 0
            for enemy in self.enemies
        )

        if self.exit_zone.collidepoint(point(p.pos)) and not tank_alive:
            if self.chapter == len(CHAPTERS) - 1:
                self.state = "win"
            else:
                self.chapter += 1
                self.load_level()

    def draw(self) -> None:
        screen.fill((9, 13, 20))

        offset = Vec()
        if self.shake > 0 and self.state == "play":
            offset = Vec(
                random.randint(-4, 4),
                random.randint(-4, 4),
            )

        # Road and sidewalks.
        pygame.draw.rect(
            screen, (25, 32, 42), (0, 0, WIDTH, PLAY_HEIGHT)
        )

        for x in range(0, WIDTH, 80):
            pygame.draw.line(
                screen, (34, 43, 53), (x, 0), (x, PLAY_HEIGHT)
            )
        for y in range(0, PLAY_HEIGHT, 80):
            pygame.draw.line(
                screen, (34, 43, 53), (0, y), (WIDTH, y)
            )

        pygame.draw.rect(
            screen, (13, 20, 28), (0, 235, WIDTH, 160)
        )
        for y in (233, 397):
            pygame.draw.line(
                screen, (73, 85, 91), (0, y), (WIDTH, y), 4
            )
        for x in range(0, WIDTH, 100):
            pygame.draw.rect(
                screen,
                (134, 122, 69),
                (x, 312, 48, 4),
                border_radius=2,
            )

        # Puddles.
        for index in range(19):
            x = (index * 173 + 35) % WIDTH
            y = (index * 97 + 53) % PLAY_HEIGHT
            pygame.draw.ellipse(
                screen,
                (25, 43, 55),
                (x, y, 58 + index % 4 * 17, 10),
            )
            pygame.draw.line(
                screen,
                (42, 67, 80),
                (x + 12, y + 4),
                (x + 43, y + 4),
            )

        # Grates.
        for x, y in ((170, 217), (700, 403), (1100, 217)):
            pygame.draw.rect(
                screen, (8, 13, 18), (x, y, 52, 12)
            )
            for slot in range(7):
                pygame.draw.line(
                    screen,
                    (64, 77, 85),
                    (x + 5 + slot * 6, y + 2),
                    (x + 5 + slot * 6, y + 9),
                )

        # Buildings and neon.
        for index, wall in enumerate(self.walls):
            rect = wall.move(round(offset.x), round(offset.y))
            accent = BLUE if index % 2 == 0 else (237, 80, 145)

            pygame.draw.rect(
                screen,
                (3, 7, 12),
                rect.move(10, 14),
                border_radius=7,
            )
            pygame.draw.rect(
                screen, (42, 53, 67), rect, border_radius=5
            )
            pygame.draw.rect(
                screen, (83, 101, 117), rect, 2, border_radius=5
            )

            inner = rect.inflate(-14, -14)
            pygame.draw.rect(
                screen, (28, 38, 50), inner, border_radius=3
            )

            for y in range(inner.top + 10, inner.bottom, 15):
                pygame.draw.line(
                    screen,
                    (38, 49, 62),
                    (inner.left + 4, y),
                    (inner.right - 4, y),
                )

            pygame.draw.line(
                screen,
                accent,
                (rect.left + 8, rect.bottom - 4),
                (rect.right - 8, rect.bottom - 4),
                3,
            )
            glow(Vec(rect.centerx, rect.bottom), accent, 58)

            vent = pygame.Rect(
                rect.centerx - 14, rect.centery - 12, 28, 24
            )
            pygame.draw.rect(
                screen, (65, 77, 88), vent, border_radius=3
            )
            pygame.draw.circle(
                screen, (22, 29, 37), vent.center, 8, 2
            )

        # Exit.
        exit_rect = self.exit_zone.move(
            round(offset.x), round(offset.y)
        )
        tank_alive = any(
            enemy.kind == "tank" and enemy.hp > 0
            for enemy in self.enemies
        )
        exit_color = RED if tank_alive else BLUE

        glow(Vec(exit_rect.center), exit_color, 90)
        pygame.draw.rect(
            screen, (15, 35, 47), exit_rect, border_radius=5
        )
        pygame.draw.rect(
            screen, exit_color, exit_rect, 3, border_radius=5
        )
        text(
            "LOCK" if tank_alive else "EXIT",
            exit_rect.x + 10,
            exit_rect.y + 43,
            exit_color,
            SMALL,
        )

        # Items.
        for item in self.pickups:
            pos = item.pos + offset
            x, y = point(pos)
            color = {
                "medkit": RED,
                "ammo": GOLD,
                "bomb": BLUE,
            }[item.kind]

            glow(pos, color, 34)
            pygame.draw.rect(
                screen,
                (13, 21, 29),
                (x - 13, y - 11, 26, 22),
                border_radius=4,
            )
            pygame.draw.rect(
                screen,
                color,
                (x - 13, y - 11, 26, 22),
                2,
                border_radius=4,
            )

            if item.kind == "medkit":
                pygame.draw.line(
                    screen, WHITE, (x - 6, y), (x + 6, y), 3
                )
                pygame.draw.line(
                    screen, WHITE, (x, y - 6), (x, y + 6), 3
                )
            elif item.kind == "ammo":
                for shift in (-6, 0, 6):
                    pygame.draw.line(
                        screen,
                        GOLD,
                        (x + shift, y - 5),
                        (x + shift, y + 5),
                        3,
                    )
            else:
                pygame.draw.circle(screen, BLUE, (x, y), 6)

            if item.pos.distance_to(self.player.pos) < 48:
                text(
                    f"[E] {item.kind.upper()}",
                    x - 45, y - 37, WHITE, SMALL,
                )

        # Survivors.
        for ally in self.allies:
            if ally.hp <= 0:
                continue

            facing = self.player.aim
            targets = [
                enemy
                for enemy in self.enemies
                if enemy.hp > 0
                and ally.pos.distance_to(enemy.pos) < 360
            ]
            if targets:
                target = min(
                    targets,
                    key=lambda enemy: ally.pos.distance_squared_to(
                        enemy.pos
                    ),
                )
                facing = target.pos - ally.pos

            pos = ally.pos + offset
            draw_character(
                pos, facing, GOLD, ally.radius, ally.hurt_timer > 0
            )
            text(
                ally.name,
                round(pos.x - 20),
                round(pos.y - 34),
                GOLD,
                SMALL,
            )
            draw_bar(
                round(pos.x - 20),
                round(pos.y - 16),
                40,
                ally.hp / 75,
                GOLD,
            )

        # Infected.
        for enemy in self.enemies:
            pos = enemy.pos + offset
            draw_character(
                pos,
                self.player.pos - enemy.pos,
                enemy.color,
                enemy.radius,
                enemy.hurt_timer > 0,
                armed=False,
            )

            if enemy.kind != "common":
                text(
                    enemy.kind.upper(),
                    round(pos.x - 28),
                    round(pos.y - enemy.radius - 29),
                    enemy.color,
                    SMALL,
                )
                draw_bar(
                    round(pos.x - 25),
                    round(pos.y - enemy.radius - 9),
                    50,
                    enemy.hp / ENEMY_STATS[enemy.kind][0],
                    enemy.color,
                )

        # Flashlight: decorative, without wall-shadow calculations.
        origin = self.player.pos + offset
        direction = self.player.aim
        side = Vec(-direction.y, direction.x)
        light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for length, spread, alpha in ((255, 100, 12), (160, 43, 16)):
            tip = origin + direction * length
            pygame.draw.polygon(
                light,
                (180, 210, 235, alpha),
                [
                    point(origin),
                    point(tip + side * spread),
                    point(tip - side * spread),
                ],
            )
        screen.blit(light, (0, 0))

        glow(origin, BLUE, 42)
        draw_character(
            origin,
            direction,
            BLUE,
            self.player.radius,
            self.player.hurt_timer > 0,
        )

        # Tracers and particles.
        for bullet in self.bullets:
            end = bullet.pos + offset
            tail = end - bullet.velocity.normalize() * 22
            pygame.draw.line(screen, (135, 93, 38), tail, end, 6)
            pygame.draw.line(screen, (255, 239, 183), tail, end, 2)

        for particle in self.particles:
            pygame.draw.circle(
                screen,
                particle.color,
                point(particle.pos + offset),
                particle.size,
            )

        if self.player.cooldown > 0.085 and self.state == "play":
            muzzle = origin + direction * 31
            glow(muzzle, GOLD, 38)
            pygame.draw.polygon(
                screen,
                (255, 245, 200),
                [
                    point(muzzle - direction * 5),
                    point(muzzle + side * 6),
                    point(muzzle + direction * 18),
                    point(muzzle - side * 6),
                ],
            )

        # Aim marker.
        rx, ry = point(origin + direction * 90)
        for sign in (-1, 1):
            pygame.draw.line(
                screen, BLUE,
                (rx + sign * 5, ry),
                (rx + sign * 10, ry), 2,
            )
            pygame.draw.line(
                screen, BLUE,
                (rx, ry + sign * 5),
                (rx, ry + sign * 10), 2,
            )

        # Rain.
        rain = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for index in range(100):
            x = (index * 131 - self.elapsed * 105) % WIDTH
            y = (index * 79 + self.elapsed * 480) % PLAY_HEIGHT
            pygame.draw.line(
                rain,
                (140, 180, 205, 55),
                (round(x), round(y)),
                (round(x - 4), round(y + 13)),
            )
        screen.blit(rain, (0, 0))

        if self.player.hurt_timer > 0:
            damage = pygame.Surface(
                (WIDTH, PLAY_HEIGHT), pygame.SRCALPHA
            )
            damage.fill((185, 20, 35, 30))
            screen.blit(damage, (0, 0))

        # HUD.
        pygame.draw.rect(
            screen, (5, 9, 15), (0, PLAY_HEIGHT, WIDTH, 90)
        )
        pygame.draw.line(
            screen, (55, 88, 110),
            (0, PLAY_HEIGHT), (WIDTH, PLAY_HEIGHT), 2,
        )

        title, objective = CHAPTERS[self.chapter]
        text(f"0{self.chapter + 1} / {title}", 20, 642)
        text(objective, 20, 675, (145, 167, 185), SMALL)

        text(f"HEALTH {self.player.hp:03d}", 440, 642, RED)
        draw_bar(440, 681, 155, self.player.hp / 100, RED)

        text(
            f"AMMO {self.player.magazine:02d}/{self.player.reserve:03d}",
            635, 642, GOLD,
        )
        text(
            "RELOADING..."
            if self.player.reload_timer > 0
            else "SPACE fire | R reload",
            635, 676, WHITE, SMALL,
        )

        text(f"KILLS {self.kills:03d}", 930, 642, GREEN)
        text("STAMINA", 1090, 642, BLUE)
        draw_bar(
            1090, 681, 160, self.player.stamina / 100, BLUE
        )

        if self.banner_timer > 0 and self.state == "play":
            center_text(title, 32, BLUE)
            center_text(
                "KEEP MOVING. STAY TOGETHER.",
                58, WHITE, SMALL,
            )

        if self.state != "play":
            overlay = pygame.Surface(
                (WIDTH, HEIGHT), pygame.SRCALPHA
            )
            overlay.fill((3, 6, 14, 215))
            screen.blit(overlay, (0, 0))

            if self.state == "title":
                center_text("DEAD SIGNAL", 240, RED, BIG)
                center_text(
                    "THE CITY IS LOST. YOU ARE NOT.",
                    305,
                    (170, 190, 205),
                )
                center_text(
                    "WASD move / ARROWS aim / Hold SPACE to fire",
                    370, WHITE, SMALL,
                )
                center_text(
                    "R reload / E collect / SHIFT sprint",
                    403, WHITE, SMALL,
                )
                center_text("[ ENTER TO DEPLOY ]", 475, BLUE)

            elif self.state == "dead":
                center_text("SIGNAL LOST", 265, RED, BIG)
                center_text(
                    f"{self.kills} INFECTED ELIMINATED", 345
                )
                center_text("[ R TO RETRY ]", 425, BLUE)

            elif self.state == "win":
                center_text("EXTRACTION COMPLETE", 265, GREEN, BIG)
                center_text(
                    f"{self.kills} INFECTED ELIMINATED", 345
                )
                center_text("[ R TO PLAY AGAIN ]", 425, BLUE)


def main() -> None:
    game = Game()
    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        game.elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif game.state == "title":
                    if event.key == pygame.K_RETURN:
                        game.state = "play"

                elif game.state in ("dead", "win"):
                    if event.key == pygame.K_r:
                        game.restart()

                elif game.state == "play":
                    if event.key == pygame.K_r:
                        game.reload()
                    elif event.key == pygame.K_e:
                        game.collect()

        if not running:
            break

        if game.state == "play":
            game.update(dt)

        game.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()