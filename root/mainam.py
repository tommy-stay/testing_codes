from ursina import *
from ursina.shaders import lit_with_shadows_shader
from dataclasses import dataclass
import math
import random


app = Ursina()
window.title = "DEAD SIGNAL | Eight Chapter Campaign"
window.borderless = False
window.fullscreen = False
window.color = color.rgb(.025, .035, .055)
window.fps_counter.enabled = False
window.exit_button.visible = False

camera.orthographic = True
camera.fov = 39
camera.position = (0, 38, -29)
camera.look_at(Vec3(0, 0, 0))

mouse.visible = True

# All colors use normalized 0–1 values.
WHITE = color.rgb(.86, .93, 1)
CYAN = color.rgb(.18, .78, 1)
RED = color.rgb(1, .23, .32)
GOLD = color.rgb(1, .72, .27)
GREEN = color.rgb(.31, .94, .54)
PURPLE = color.rgb(.69, .40, 1)
DARK = color.rgb(.045, .065, .09)

sun = DirectionalLight(shadow_map_resolution=(2048, 2048))
sun.look_at(Vec3(1, -2, -1))
sun.color = color.rgb(.88, .94, 1)

CHAPTERS = [
    ("THE HOTEL", "Escape the hotel block."),
    ("DEAD STREETS", "Cross the shopping district."),
    ("THE WAREHOUSE", "Move through the loading yard."),
    ("QUARANTINE", "Break through the checkpoint."),
    ("THE HOSPITAL", "Defeat the Tank. Reach safety."),
    ("RAIL YARD", "Cross the maintenance tracks."),
    ("THE DOCKS", "Reach the waterfront route."),
    ("LAST SIGNAL", "Defeat both Tanks. Reach extraction."),
]

ACCENTS = [
    CYAN, color.rgb(.95, .30, .57), GOLD,
    GREEN, color.rgb(.30, .85, .90),
    color.rgb(.90, .49, .25),
    color.rgb(.38, .49, 1), RED,
]

# Original Pygame map coordinates.
LAYOUTS = [
    [(220,65,190,130), (500,70,100,145),
     (760,80,190,100), (270,435,190,115),
     (610,420,110,145), (900,445,170,100)],

    [(180,75,120,120), (360,100,120,100),
     (560,60,140,135), (790,90,150,110),
     (1020,70,100,135), (200,435,130,120),
     (410,455,140,90), (650,420,120,140),
     (860,450,130,105), (1060,430,100,120)],

    [(190,75,330,125), (660,70,350,125),
     (220,430,310,120), (700,430,320,120)],

    [(200,95,80,110), (390,150,150,45),
     (630,65,85,145), (840,145,180,50),
     (1070,90,75,115), (210,425,80,125),
     (400,435,160,45), (660,420,80,145),
     (850,435,180,50), (1090,425,70,120)],

    [(170,65,190,145), (445,70,150,130),
     (700,65,130,145), (930,80,190,120),
     (190,425,170,145), (460,435,160,125),
     (720,420,130,145), (950,440,170,110)],

    [(160,90,280,65), (520,90,270,65),
     (870,90,250,65), (250,440,280,65),
     (610,440,270,65), (960,440,200,65),
     (450,180,100,35), (810,545,140,35)],

    [(190,75,180,65), (190,155,180,55),
     (470,90,190,80), (760,80,90,130),
     (950,90,180,100), (210,430,180,65),
     (210,515,180,55), (490,445,190,95),
     (780,420,90,145), (970,445,170,100)],

    [(200,90,100,100), (420,110,100,80),
     (660,80,110,120), (930,95,130,100),
     (220,440,110,100), (450,450,100,100),
     (700,425,110,130), (990,450,110,100)],
]

STATS = {
    "common": (3, 3.3, 7, .46, GREEN),
    "hunter": (5, 5.8, 10, .46, PURPLE),
    "boomer": (7, 2.6, 8, .66, color.rgb(.65, .82, .20)),
    "tank": (65, 2.3, 20, 1.10, RED),
}

SPECIALS = [
    (), ("hunter",), ("boomer",),
    ("hunter", "boomer"), ("hunter", "hunter"),
    ("hunter", "boomer"),
    ("hunter", "boomer", "boomer"),
    ("hunter", "boomer"),
]

OPENING_COUNTS = [9, 12, 14, 15, 16, 17, 18, 14]
HORDE_INTERVALS = [16, 15, 14, 14, 13, 13, 12, 12]


def map_position(x, y):
    return Vec2((x - 640) / 25, (315 - y) / 25)


def world_position(p, height=0):
    return Vec3(p.x, height, p.y)


def box(parent, position, scale, tint, lit=True):
    return Entity(
        parent=parent,
        model="cube",
        position=position,
        scale=scale,
        color=tint,
        shader=lit_with_shadows_shader if lit else None,
        unlit=not lit,
    )


def segment_box(a, b, rect, padding=0):
    """Return first segment intersection, or None."""
    xmin, xmax, zmin, zmax = rect
    low, high = 0.0, 1.0

    for start, delta, lower, upper in (
        (a.x, b.x-a.x, xmin-padding, xmax+padding),
        (a.y, b.y-a.y, zmin-padding, zmax+padding),
    ):
        if abs(delta) < .000001:
            if start < lower or start > upper:
                return None
        else:
            t1 = (lower-start) / delta
            t2 = (upper-start) / delta
            low = max(low, min(t1, t2))
            high = min(high, max(t1, t2))
            if low > high:
                return None

    return low


def segment_circle(a, b, center, radius):
    delta = b-a
    length_squared = delta.dot(delta)

    if length_squared < .000001:
        return 0 if (a-center).length() <= radius else None

    offset = a-center
    c = offset.dot(offset)-radius*radius
    if c <= 0:
        return 0

    q = offset.dot(delta)
    discriminant = q*q-length_squared*c
    if discriminant < 0:
        return None

    t = (-q-math.sqrt(discriminant))/length_squared
    return t if 0 <= t <= 1 else None


class Survivor:
    def __init__(self, game, p, name, tint, kind=None):
        self.p = Vec2(p)
        self.name = name
        self.kind = kind
        self.hp = STATS[kind][0] if kind else (
            100 if name == "YOU" else 75
        )
        self.max_hp = self.hp
        self.radius = STATS[kind][3] if kind else .46
        self.speed = STATS[kind][1] if kind else 6.8
        self.damage = STATS[kind][2] if kind else 0
        self.aim = Vec2(1, 0)
        self.cooldown = 0
        self.hurt = 0
        self.phase = random.uniform(0, math.tau)

        self.root = Entity(parent=game.room)
        size = self.radius/.46
        self.visual = Entity(parent=self.root, scale=size)

        # Flat stylized contact shadow.
        Entity(
            parent=self.root, model="sphere",
            position=(0, .025, 0),
            scale=(self.radius*2.5, .035, self.radius*1.8),
            color=color.rgba(0, 0, 0, .38), unlit=True
        )

        self.body = box(
            self.visual, (0, .65, 0),
            (.65, .75, .42), tint
        )
        box(self.visual, (0, .72, -.23),
            (.47, .46, .16), DARK)

        box(
            self.visual, (0, 1.17, 0),
            (.39, .38, .38),
            color.rgb(.52, .64, .49)
            if kind else color.rgb(.72, .59, .46)
        )
        box(self.visual, (0, 1.39, 0),
            (.44, .12, .44), DARK)

        self.legs = [
            box(self.visual, (x, .22, 0),
                (.21, .45, .24), DARK)
            for x in (-.19, .19)
        ]

        if kind:
            for x in (-.11, .11):
                box(self.visual, (x, 1.21, .20),
                    (.07, .055, .025), RED, False)
        else:
            box(self.visual, (.34, .72, .43),
                (.15, .17, .86), DARK)
            box(self.visual, (.34, .74, .88),
                (.10, .10, .11), tint, False)

        self.flash = box(
            self.visual, (.34, .75, 1),
            (.24, .24, .40), GOLD, False
        )
        self.flash.enabled = False

    def sync(self, dt, moving):
        self.root.position = world_position(self.p)
        self.visual.rotation_y = math.degrees(
            math.atan2(self.aim.x, self.aim.y)
        )
        self.phase += dt*12
        self.visual.y = abs(math.sin(self.phase))*.035 if moving else 0

        for i, leg in enumerate(self.legs):
            leg.rotation_x = (
                math.sin(self.phase+i*math.pi)*28
                if moving else 0
            )

        self.hurt = max(0, self.hurt-dt)
        self.body.color = WHITE if self.hurt > 0 else (
            STATS[self.kind][4] if self.kind
            else CYAN if self.name == "YOU" else GOLD
        )
        self.flash.enabled = (
            not self.kind and self.cooldown > (
                .08 if self.name == "YOU" else .40
            )
        )


@dataclass
class Shot:
    p: Vec2
    direction: Vec2
    entity: Entity
    life: float = 1.1


class Campaign:
    def __init__(self):
        self.chapter = 0
        self.kills = 0
        self.state = "title"
        self.elapsed = 0
        self.room = None
        self.effects = []
        self.rain = []

        self.make_ui()
        self.load_level()
        self.show_menu("title")

    def make_ui(self):
        self.ui = Entity(parent=camera.ui)

        Entity(
            parent=self.ui, model="quad",
            position=(0, -.405), scale=(2, .19),
            color=color.rgb(.025, .035, .055)
        )
        Entity(
            parent=self.ui, model="quad",
            position=(0, .435), scale=(2, .13),
            color=color.rgba(.015, .025, .04, .92)
        )

        self.title = Text(
            parent=self.ui, position=(-.85, .47),
            scale=1.05, color=CYAN
        )
        self.objective = Text(
            parent=self.ui, position=(-.85, .425),
            scale=.75, color=WHITE
        )
        self.stats = Text(
            parent=self.ui, position=(-.85, -.34),
            scale=.9, color=WHITE
        )
        self.squad = Text(
            parent=self.ui, position=(-.85, -.395),
            scale=.75, color=GOLD
        )
        self.controls = Text(
            parent=self.ui,
            text="WASD move   ARROWS aim   SPACE fire   R reload"
                 "   E collect / exit   SHIFT sprint   ESC pause",
            position=(-.85, -.465),
            scale=.65, color=color.rgb(.47, .60, .72)
        )
        self.prompt = Text(
            parent=self.ui, origin=(0, 0),
            position=(0, -.27), scale=.95, color=GOLD
        )

        self.health_bar = Entity(
            parent=self.ui, model="quad",
            origin=(-.5, 0), position=(.38, -.37),
            scale=(.43, .012), color=RED
        )
        self.stamina_bar = Entity(
            parent=self.ui, model="quad",
            origin=(-.5, 0), position=(.38, -.405),
            scale=(.43, .008), color=CYAN
        )

        self.damage_overlay = Entity(
            parent=camera.ui, model="quad",
            scale=(2, 1), color=color.clear
        )

        self.menu = Entity(parent=camera.ui)
        Entity(
            parent=self.menu, model="quad",
            scale=(2, 1.1),
            color=color.rgba(.015, .025, .045, .94)
        )
        Entity(
            parent=self.menu, model="quad",
            position=(0, .24), scale=(.58, .008),
            color=RED
        )
        self.menu_title = Text(
            parent=self.menu, origin=(0, 0),
            position=(0, .12), scale=2.7, color=RED
        )
        self.menu_body = Text(
            parent=self.menu, origin=(0, 0),
            position=(0, -.06), scale=.95, color=WHITE
        )
        self.menu_hint = Text(
            parent=self.menu, origin=(0, 0),
            position=(0, -.25), scale=1.05, color=CYAN
        )

    def show_menu(self, state):
        self.state = state
        self.menu.enabled = state != "play"

        messages = {
            "title": (
                "DEAD SIGNAL",
                "EIGHT CHAPTERS. ONE WAY OUT.\n\n"
                "Keep moving. Stay together. Reach extraction.",
                "ENTER TO DEPLOY"
            ),
            "paused": (
                "SIGNAL HELD",
                "Campaign paused.",
                "ESC TO RESUME"
            ),
            "dead": (
                "SIGNAL LOST",
                f"Chapter {self.chapter+1} / 8\n\n"
                f"{self.kills} infected eliminated",
                "R TO RESTART CAMPAIGN"
            ),
            "win": (
                "EXTRACTION",
                f"All eight chapters completed.\n\n"
                f"{self.kills} infected eliminated",
                "R TO PLAY AGAIN"
            ),
        }

        if state in messages:
            title, body, hint = messages[state]
            self.menu_title.text = title
            self.menu_body.text = body
            self.menu_hint.text = hint
            self.menu_title.color = GREEN if state == "win" else RED

    def blocked(self, p, radius):
        if abs(p.x) > 25.6-radius or abs(p.y) > 12.6-radius:
            return True

        return any(
            xmin-radius < p.x < xmax+radius
            and zmin-radius < p.y < zmax+radius
            for xmin, xmax, zmin, zmax in self.walls
        )

    def move(self, actor, delta):
        old = Vec2(actor.p)
        candidate = actor.p+Vec2(delta.x, 0)
        if not self.blocked(candidate, actor.radius):
            actor.p.x = candidate.x

        candidate = actor.p+Vec2(0, delta.y)
        if not self.blocked(candidate, actor.radius):
            actor.p.y = candidate.y

        return (actor.p-old).length() > .0001

    def clear_line(self, a, b):
        return not any(
            segment_box(a, b, wall) is not None
            for wall in self.walls
        )

    def load_level(self):
        if self.room is not None:
            destroy(self.room)

        self.room = Entity()
        self.walls = []
        self.enemies = []
        self.shots = []
        self.pickups = []
        self.effects = []
        self.rain = []

        self.ammo = 30
        self.reserve = 180
        self.reload_timer = 0
        self.stamina = 100
        self.horde_timer = HORDE_INTERVALS[self.chapter]
        self.start_delay = .4
        accent = ACCENTS[self.chapter]

        self.title.text = (
            f"DEAD SIGNAL   /   {self.chapter+1:02d}"
            f"   {CHAPTERS[self.chapter][0]}"
        )
        self.title.color = accent
        self.objective.text = CHAPTERS[self.chapter][1]

        box(self.room, (0, -.25, 0),
            (51.2, .5, 25.2), color.rgb(.12, .16, .20))

        box(self.room, (0, .012, 0),
            (51, .02, 6.4), color.rgb(.045, .065, .085))

        for z in (-3.3, 3.3):
            box(self.room, (0, .04, z),
                (51, .035, .10), color.rgb(.35, .42, .46))

        for x in range(-24, 25, 4):
            box(self.room, (x, .04, 0),
                (1.7, .025, .10),
                color.rgb(.48, .41, .19), False)

        # Deterministic room dressing.
        rng = random.Random(300+self.chapter)

        for _ in range(28):
            Entity(
                parent=self.room, model="sphere",
                position=(rng.uniform(-25, 25), .035,
                          rng.uniform(-12, 12)),
                scale=(rng.uniform(.8, 2.2), .015,
                       rng.uniform(.25, .7)),
                color=color.rgb(.10, .22, .28),
                unlit=True
            )

        for index, (x, y, width, height) in enumerate(
            LAYOUTS[self.chapter]
        ):
            p = map_position(x+width/2, y+height/2)
            w, d = width/25, height/25
            h = rng.uniform(1.6, 2.6)

            self.walls.append((
                p.x-w/2, p.x+w/2, p.y-d/2, p.y+d/2
            ))

            box(self.room, (p.x, h/2, p.y),
                (w, h, d), color.rgb(.19, .24, .29))
            box(self.room, (p.x, h+.06, p.y),
                (w+.10, .12, d+.10), color.rgb(.29, .35, .40))
            box(self.room, (p.x, .45, p.y-d/2-.025),
                (max(.2, w-.3), .07, .04), accent, False)

            # Glowing panels/windows on the front face.
            count = max(1, int(w/1.3))
            for j in range(count):
                wx = p.x-w/2+(j+.5)*w/count
                box(self.room, (wx, h*.65, p.y-d/2-.035),
                    (.55, .35, .035), accent, False)

            # Roof vents / container ribs.
            if self.chapter in (2, 6):
                for offset in range(max(1, int(w))):
                    rx = p.x-w/2+.35+offset
                    box(self.room, (rx, h+.15, p.y),
                        (.055, .13, d*.88),
                        color.rgb(.35, .40, .43))
            else:
                box(self.room, (p.x, h+.22, p.y),
                    (.75, .3, .65), DARK)

        # Boundary curb: decorative, collision handled numerically.
        for z in (-12.6, 12.6):
            box(self.room, (0, .15, z),
                (51.5, .3, .18), DARK)

        if self.chapter == 5:
            for z in (-1.8, -1.2, 1.2, 1.8):
                box(self.room, (0, .06, z),
                    (51, .06, .08), color.rgb(.44, .51, .55))
            for x in range(-25, 26):
                for z in (-1.5, 1.5):
                    box(self.room, (x, .035, z),
                        (.18, .04, 1.2), color.rgb(.25, .19, .14))

        if self.chapter == 6:
            box(self.room, (0, .06, -11.7),
                (51, .07, 1.4), color.rgb(.035, .23, .35), False)
            for x in range(-24, 25, 3):
                box(self.room, (x, .11, -11.7),
                    (1.1, .02, .025), CYAN, False)

        self.exit_p = map_position(1225, 315)
        self.exit_tile = box(
            self.room, world_position(self.exit_p, .07),
            (2.4, .10, 4.4), CYAN, False
        )
        for z in (-2.2, 2.2):
            box(self.room,
                (self.exit_p.x, 1.3, z),
                (.16, 2.6, .16), CYAN, False)

        self.player = Survivor(
            self, map_position(80, 315), "YOU", CYAN
        )
        self.allies = [
            Survivor(self, map_position(x, y), name, GOLD)
            for x, y, name in [
                (65, 260, "MAYA"),
                (65, 370, "COLE"),
                (120, 315, "JUNE"),
            ]
        ]

        for x, y, kind in [
            (180,280,"ammo"), (390,350,"medkit"),
            (610,280,"ammo"), (760,350,"bomb"),
            (990,280,"medkit"), (1100,350,"ammo"),
        ]:
            p = map_position(x, y)
            tint = {"ammo": GOLD, "medkit": RED, "bomb": CYAN}[kind]
            root = Entity(parent=self.room)
            box(root, (0, .3, 0), (.8, .5, .65), DARK)
            box(root, (0, .58, 0), (.62, .06, .48), tint, False)

            if kind == "medkit":
                box(root, (0, .63, 0), (.40, .025, .10), WHITE, False)
                box(root, (0, .64, 0), (.10, .025, .40), WHITE, False)

            root.position = world_position(p)
            self.pickups.append((p, kind, root))

        for _ in range(OPENING_COUNTS[self.chapter]):
            self.spawn(initial=True)

        for kind in SPECIALS[self.chapter]:
            self.spawn(kind, initial=True)

        if self.chapter == 4:
            self.add_enemy(map_position(1080, 315), "tank")
        elif self.chapter == 7:
            self.add_enemy(map_position(1010, 275), "tank")
            self.add_enemy(map_position(1120, 355), "tank")

        for _ in range(70):
            drop = box(
                self.room,
                (rng.uniform(-26, 26), rng.uniform(1, 13),
                 rng.uniform(-13, 13)),
                (.018, .55, .018),
                color.rgba(.40, .66, .85, .38), False
            )
            self.rain.append(drop)

        sun.update_bounds(self.room)
        self.update_hud()

    def add_enemy(self, p, kind):
        enemy = Survivor(self, p, kind.upper(), STATS[kind][4], kind)
        self.enemies.append(enemy)

    def spawn(self, kind="common", initial=False):
        for _ in range(100):
            if initial:
                p = map_position(
                    random.uniform(750, 1230),
                    random.uniform(40, 590)
                )
            else:
                p = Vec2(random.uniform(-24, 24),
                         random.uniform(-11, 11))
                if random.random() < .5:
                    p.x = random.choice((-24, 24))
                else:
                    p.y = random.choice((-11, 11))

            if (
                not self.blocked(p, STATS[kind][3])
                and (p-self.player.p).length() > 8.8
            ):
                self.add_enemy(p, kind)
                return

    def burst(self, p, tint, count=8):
        # Cap decorative particles to prevent runaway effects.
        for _ in range(min(count, max(0, 180-len(self.effects)))):
            e = box(
                self.room, world_position(p, .7),
                (.09, .09, .09), tint, False
            )
            velocity = Vec3(
                random.uniform(-4, 4),
                random.uniform(1, 5),
                random.uniform(-4, 4)
            )
            self.effects.append([e, velocity, random.uniform(.15, .4)])

    def fire(self, actor):
        direction = actor.aim.normalized()
        p = actor.p+direction*.75
        e = box(
            self.room, world_position(p, .75),
            (.055, .055, .8), GOLD, False
        )
        e.rotation_y = math.degrees(
            math.atan2(direction.x, direction.y)
        )
        self.shots.append(Shot(p, direction, e))

    def reload(self):
        if self.reload_timer <= 0 and self.ammo < 30 and self.reserve:
            self.reload_timer = 1.2

    def collect(self):
        for item in self.pickups[:]:
            p, kind, root = item
            if (p-self.player.p).length() > 1.92:
                continue

            if kind == "medkit":
                if self.player.hp >= 100:
                    continue
                self.player.hp = min(100, self.player.hp+45)
            elif kind == "ammo":
                self.reserve += 90
            else:
                self.burst(p, GOLD, 45)
                for enemy in self.enemies:
                    if (enemy.p-p).length() < 11.2:
                        enemy.hp -= 18

            self.pickups.remove(item)
            destroy(root)

    def interact(self):
        self.collect()
        tank_alive = any(
            e.kind == "tank" and e.hp > 0 for e in self.enemies
        )
        if (self.player.p-self.exit_p).length() < 2.4 and not tank_alive:
            if self.chapter == 7:
                self.show_menu("win")
            else:
                self.chapter += 1
                self.load_level()

    def restart(self):
        self.chapter = 0
        self.kills = 0
        self.load_level()
        self.show_menu("play")

    def update_hud(self):
        p = self.player
        ammo = "RELOADING" if self.reload_timer > 0 else (
            f"{self.ammo:02d} / {self.reserve:03d}"
        )
        self.stats.text = (
            f"HEALTH {p.hp:03d}       AMMO {ammo}"
            f"       KILLS {self.kills:03d}"
        )
        self.squad.text = "   ".join(
            f"{a.name}: {a.hp if a.hp > 0 else 'LOST'}"
            for a in self.allies
        )
        self.health_bar.scale_x = .43*max(0, p.hp)/100
        self.stamina_bar.scale_x = .43*self.stamina/100
        self.damage_overlay.color = color.rgba(
            .8, .025, .05, .16 if p.hurt > 0 else 0
        )

        tanks = [
            e for e in self.enemies
            if e.kind == "tank" and e.hp > 0
        ]
        self.exit_tile.color = RED if tanks else CYAN

        self.prompt.text = ""
        if tanks:
            self.prompt.text = "TANK SIGNAL  /  " + "   ".join(
                f"{e.hp}/{e.max_hp}" for e in tanks
            )

        for pos, kind, root in self.pickups:
            if (pos-p.p).length() < 1.92:
                self.prompt.text = f"[ E ] COLLECT {kind.upper()}"
                break

        if (p.p-self.exit_p).length() < 2.8:
            self.prompt.text = (
                "EXIT LOCKED — ELIMINATE THE TANKS"
                if tanks else "[ E ] ENTER NEXT ROOM"
                if self.chapter < 7 else "[ E ] EXTRACT"
            )

    def tick(self, dt):
        if self.state != "play":
            return

        self.elapsed += dt
        self.start_delay = max(0, self.start_delay-dt)
        p = self.player

        movement = Vec2(
            held_keys["d"]-held_keys["a"],
            held_keys["w"]-held_keys["s"]
        )
        aiming = Vec2(
            held_keys["right arrow"]-held_keys["left arrow"],
            held_keys["up arrow"]-held_keys["down arrow"]
        )

        if aiming.length() > 0:
            p.aim = aiming.normalized()
        elif movement.length() > 0:
            p.aim = movement.normalized()

        sprint = (
            held_keys["shift"] and self.stamina > 1
            and movement.length() > 0
        )
        self.stamina = max(
            0, min(100, self.stamina+(-30 if sprint else 20)*dt)
        )

        moving = False
        if movement.length() > 0:
            moving = self.move(
                p, movement.normalized()*(10.4 if sprint else 7.2)*dt
            )

        p.cooldown = max(0, p.cooldown-dt)

        if self.reload_timer > 0:
            self.reload_timer = max(0, self.reload_timer-dt)
            if self.reload_timer == 0:
                amount = min(30-self.ammo, self.reserve)
                self.ammo += amount
                self.reserve -= amount

        if (
            held_keys["space"] and p.cooldown <= 0
            and self.reload_timer <= 0 and self.ammo > 0
            and self.start_delay <= 0
        ):
            self.fire(p)
            self.ammo -= 1
            p.cooldown = .12

        p.sync(dt, moving)

        for index, ally in enumerate(self.allies):
            if ally.hp <= 0:
                ally.root.enabled = False
                continue

            ally.cooldown = max(0, ally.cooldown-dt)
            follow = p.p+Vec2(-1.8, (index-1)*1.8)
            delta = follow-ally.p
            moved = False

            if delta.length() > 1.8:
                moved = self.move(ally, delta.normalized()*6.8*dt)

            targets = [
                e for e in self.enemies
                if e.hp > 0 and (e.p-ally.p).length() < 14.4
                and self.clear_line(ally.p, e.p)
            ]

            if targets:
                target = min(
                    targets, key=lambda e: (e.p-ally.p).length()
                )
                ally.aim = (target.p-ally.p).normalized()
                if ally.cooldown <= 0:
                    self.fire(ally)
                    ally.cooldown = .45
            else:
                ally.aim = Vec2(p.aim)

            ally.sync(dt, moved)

        # Swept collision: bullets cannot jump through walls/enemies.
        for shot in self.shots[:]:
            start = Vec2(shot.p)
            end = start+shot.direction*32*dt
            shot.life -= dt
            first_t = 2
            target = None

            for wall in self.walls:
                t = segment_box(start, end, wall)
                if t is not None and t < first_t:
                    first_t, target = t, None

            for enemy in self.enemies:
                if enemy.hp <= 0:
                    continue
                t = segment_circle(
                    start, end, enemy.p, enemy.radius+.12
                )
                if t is not None and t < first_t:
                    first_t, target = t, enemy

            hit = first_t <= 1
            shot.p = start+(end-start)*first_t if hit else end

            if target is not None:
                target.hp -= 1
                target.hurt = .08
                self.burst(shot.p, STATS[target.kind][4], 4)

            if hit or shot.life <= 0 or abs(shot.p.x) > 27 or abs(shot.p.y) > 14:
                destroy(shot.entity)
                self.shots.remove(shot)
            else:
                shot.entity.position = world_position(shot.p, .75)

        for enemy in self.enemies[:]:
            if enemy.hp <= 0:
                self.kills += 1
                self.burst(enemy.p, STATS[enemy.kind][4], 14)
                destroy(enemy.root)
                self.enemies.remove(enemy)
                continue

            enemy.cooldown = max(0, enemy.cooldown-dt)
            living = [p]+[a for a in self.allies if a.hp > 0]
            target = min(
                living, key=lambda a: (a.p-enemy.p).length()
            )
            delta = target.p-enemy.p
            distance = delta.length()
            moved = False

            if distance > .01:
                enemy.aim = delta.normalized()
                moved = self.move(
                    enemy, enemy.aim*enemy.speed*dt
                )

            if (
                distance < enemy.radius+target.radius+.2
                and enemy.cooldown <= 0
                and self.clear_line(enemy.p, target.p)
            ):
                target.hp = max(0, target.hp-enemy.damage)
                target.hurt = .18
                enemy.cooldown = .75
                self.burst(target.p, RED, 7)

                if enemy.kind == "boomer":
                    self.burst(enemy.p, GREEN, 30)
                    for actor in living:
                        if (actor.p-enemy.p).length() < 5.2:
                            actor.hp = max(0, actor.hp-8)
                            actor.hurt = .18
                    enemy.hp = 0

            enemy.sync(dt, moved)

        for effect in self.effects[:]:
            entity, velocity, life = effect
            entity.position += velocity*dt
            velocity.y -= 12*dt
            effect[2] -= dt

            if effect[2] <= 0:
                destroy(entity)
                self.effects.remove(effect)

        for drop in self.rain:
            drop.y -= 17*dt
            drop.x -= 3*dt
            if drop.y < .2:
                drop.y = random.uniform(9, 14)
                drop.x = random.uniform(-26, 26)

        for pos, kind, root in self.pickups:
            root.y = .08+math.sin(self.elapsed*3+pos.x)*.08

        self.horde_timer -= dt
        if self.horde_timer <= 0:
            self.horde_timer = HORDE_INTERVALS[self.chapter]+random.uniform(0, 4)
            limit = 32+self.chapter*2

            for _ in range(min(5+self.chapter, max(0, limit-len(self.enemies)))):
                self.spawn()

            if self.chapter >= 2 and len(self.enemies) < limit:
                if random.random() < .45:
                    self.spawn(random.choice(("hunter", "boomer")))

        self.update_hud()
        if p.hp <= 0:
            self.show_menu("dead")


game = Campaign()


def update():
    game.tick(min(time.dt, .05))


def input(key):
    if key == "escape":
        if game.state == "play":
            game.show_menu("paused")
        elif game.state == "paused":
            game.show_menu("play")
        else:
            application.quit()
        return

    if game.state == "title":
        if key == "enter":
            game.show_menu("play")
        return

    if game.state in ("dead", "win"):
        if key == "r":
            game.restart()
        return

    if game.state != "play":
        return

    if key == "r":
        game.reload()
    elif key == "e":
        game.interact()


app.run()