import random
from enum import Enum

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 900
MAX_PLAYER_COUNT = 120

PLATFORM_HEIGHT = 40
PLAYER_COL_WIDTH = 12
PLAYER_COL_HEIGHT = 33

READY_TIME = 4
WATCH_TIME = 4

other_player_move_range = 10
REMAIN_TIME = 80
PLAYER_SPEED = 3

ROAD_POS_X = 18


class Scene(Enum):
    menu = 0
    play = 1
    result = 2


class RenderLayer(Enum):
    none = 0
    back = 1
    middle = 2
    front_1 = 3
    front_2 = 4
    ui_back = 5
    ui_middle = 6
    ui_front = 7
    max_length = 8


class CollideLayer(Enum):
    none = 0
    group_a = 1
    group_b = 2
    max_length = 3


class OnKeyDown(Enum):
    space = 0
    left = 1
    right = 2
    up = 3
    down = 4
    enter = 5
    max_length = 6


class EnemyState(Enum):
    ready = 0
    watch = 1


class PlayerState(Enum):
    idle = 0
    move = 1
    dead = 2
    success = 3
    max_length = 4


class GameObject:
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        self.image_list = image_list
        self.rect = self.image_list[1].get_rect()
        self.width = self.rect.size[0]
        self.height = self.rect.size[1]
        self.col_width = self.width
        self.col_height = self.height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.render_time = 0
        update_object_list.append(self)
        render_list[render_layer].append(self)
        collision_list[collide_layer].append(self)

    def initialize(self):
        pass

    def update(self):
        pass

    def render(self, index=1):
        if index > 0:
            screen.blit(self.image_list[index], (self.pos_x, self.pos_y))


class Enemy(GameObject):
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        super().__init__(image_list, render_layer, collide_layer, pos_x, pos_y)
        self.state = EnemyState.ready.value
        self.state_time = 0
        self.is_voice_ready = True
        self.beat_rate = 0

    def initialize(self):
        self.state = EnemyState.ready.value
        self.state_time = 0
        self.is_voice_ready = True
        self.beat_rate = 0

    def update(self):
        self.state_time += clock.get_time() / 1000

        if self.state == EnemyState.ready.value:
            if self.is_voice_ready is True:
                self.is_voice_ready = False
                heartbeat_sound_slow.stop()
                heartbeat_sound_fast.stop()
                voice_sound.play()

            if self.state_time >= READY_TIME:
                self.state_time = 0
                self.state = EnemyState.watch.value
                self.beat_rate = random.randint(5, 12)

                if self.beat_rate <= 8:
                    heartbeat_sound_slow.play()
                else:
                    heartbeat_sound_fast.play()

        elif self.state == EnemyState.watch.value:
            if self.state_time >= WATCH_TIME:
                self.state_time = 0
                self.state = EnemyState.ready.value
                self.is_voice_ready = True

    def render(self, index=1):
        render_index = index

        if self.state == EnemyState.ready.value:
            render_index = 1
        elif self.state == EnemyState.watch.value:
            render_index = 2

        super().render(render_index)


class Player(GameObject):
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        super().__init__(image_list, render_layer, collide_layer, pos_x, pos_y)
        self.state = PlayerState.idle.value
        self.speed = PLAYER_SPEED
        self.key_down_list = []
        self.col_width = PLAYER_COL_WIDTH
        self.col_height = PLAYER_COL_HEIGHT
        for i in range(OnKeyDown.max_length.value):
            self.key_down_list.append(False)

    def initialize(self):
        self.state = PlayerState.idle.value
        self.speed = PLAYER_SPEED
        self.col_width = PLAYER_COL_WIDTH
        self.col_height = PLAYER_COL_HEIGHT
        self.pos_x = SCREEN_WIDTH / 2 - player.width / 2
        self.pos_y = SCREEN_HEIGHT - PLATFORM_HEIGHT - player.height

    def restore_speed(self):
        self.speed = PLAYER_SPEED

    def update(self):
        if self.state == PlayerState.success.value or self.state == PlayerState.dead.value:
            if self.state == PlayerState.dead.value:
                play_gunshot_sound()

            global scene_index
            scene_index = Scene.result.value
            return

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] == 1 and self.key_down_list[OnKeyDown.left.value] is False:
            self.key_down_list[OnKeyDown.left.value] = True
            self.pos_x -= self.speed
            self.state = PlayerState.move.value
        elif key[pygame.K_LEFT] == 0 and self.key_down_list[OnKeyDown.left.value] is True:
            self.key_down_list[OnKeyDown.left.value] = False
            self.state = PlayerState.idle.value

        if key[pygame.K_RIGHT] == 1 and self.key_down_list[OnKeyDown.right.value] is False:
            self.key_down_list[OnKeyDown.right.value] = True
            self.pos_x += self.speed
            self.state = PlayerState.move.value
        elif key[pygame.K_RIGHT] == 0 and self.key_down_list[OnKeyDown.right.value] is True:
            self.key_down_list[OnKeyDown.right.value] = False
            self.state = PlayerState.idle.value

        if key[pygame.K_UP] == 1 and self.key_down_list[OnKeyDown.up.value] is False:
            self.key_down_list[OnKeyDown.up.value] = True
            self.pos_y -= self.speed
            self.state = PlayerState.move.value
        elif key[pygame.K_UP] == 0 and self.key_down_list[OnKeyDown.up.value] is True:
            self.key_down_list[OnKeyDown.up.value] = False
            self.state = PlayerState.idle.value

        if key[pygame.K_DOWN] == 1 and self.key_down_list[OnKeyDown.down.value] is False:
            self.key_down_list[OnKeyDown.down.value] = True
            self.pos_y += self.speed
            self.state = PlayerState.move.value
        elif key[pygame.K_DOWN] == 0 and self.key_down_list[OnKeyDown.down.value] is True:
            self.key_down_list[OnKeyDown.down.value] = False
            self.state = PlayerState.idle.value

        if enemy.state == EnemyState.watch.value and self.state == PlayerState.move.value:
            self.state = PlayerState.dead.value

        if self.pos_x < 0:
            self.pos_x = 0

        if self.pos_x > SCREEN_WIDTH - self.width:
            self.pos_x = SCREEN_WIDTH - self.width

        if self.pos_y >= SCREEN_HEIGHT - PLATFORM_HEIGHT - player.height:
            self.pos_y = self.pos_y = SCREEN_HEIGHT - PLATFORM_HEIGHT - player.height

        if self.pos_y <= 28:
            self.state = PlayerState.success.value

    def render(self, index=1):
        render_index = index

        if self.state == PlayerState.idle.value:
            render_index = 1
        elif self.state == PlayerState.move.value:
            render_index = 2
        elif self.state == PlayerState.dead.value:
            render_index = 3

        super().render(render_index)


class OtherPlayer(GameObject):
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        super().__init__(image_list, render_layer, collide_layer, pos_x, pos_y)
        self.state = PlayerState.idle.value
        self.speed = 4.5
        self.move_time = 0
        self.col_width = PLAYER_COL_WIDTH
        self.col_height = PLAYER_COL_HEIGHT
        self.move_index = 0
        self.wait_time = 0
        self.after_wait_time = 0
        self.check_move = False

    def initialize(self):
        self.state = PlayerState.idle.value
        self.speed = 4.5
        self.move_time = 0
        self.col_width = PLAYER_COL_WIDTH
        self.col_height = PLAYER_COL_HEIGHT
        self.move_index = 0
        self.wait_time = 0
        self.after_wait_time = 0
        self.check_move = False
        self.pos_x = random.randint(0, SCREEN_WIDTH - self.width)
        self.pos_y = SCREEN_HEIGHT - PLATFORM_HEIGHT - self.height

    def restore_speed(self):
        self.speed = 4.5

    def move(self):
        self.move_time += clock.get_time() / 1000
        if self.move_time >= 0.1:
            self.move_time = 0
            self.state = PlayerState.move.value
            index = random.randint(1, 20)
            if index <= 15:
                self.pos_y -= self.speed
            elif index <= 17:
                self.pos_x -= self.speed
            elif index <= 19:
                self.pos_x += self.speed
            else:
                self.pos_y += self.speed
        else:
            self.state = PlayerState.idle.value

    def update(self):
        if self.pos_y <= 28 or self.state == PlayerState.dead.value:
            return

        if enemy.state == EnemyState.ready.value:
            self.check_move = False
            self.move()
        elif enemy.state == EnemyState.watch.value:
            if self.check_move is False:
                self.move_index = random.randint(1, other_player_move_range)
                self.check_move = True
            if self.move_index == 1:
                if self.wait_time == 0:
                    self.after_wait_time = random.random() * (WATCH_TIME - 2)

                self.wait_time += clock.get_time() / 1000

                if self.wait_time >= self.after_wait_time:
                    self.move()

                if self.wait_time >= self.after_wait_time + 1:
                    play_gunshot_sound()
                    self.state = PlayerState.dead.value

        if self.pos_x < 0:
            self.pos_x = 0

        if self.pos_x > SCREEN_WIDTH - self.width:
            self.pos_x = SCREEN_WIDTH - self.width

        if self.pos_y >= SCREEN_HEIGHT - PLATFORM_HEIGHT - player.height:
            self.pos_y = self.pos_y = SCREEN_HEIGHT - PLATFORM_HEIGHT - player.height

    def render(self, index=1):
        render_index = index

        if self.state == PlayerState.idle.value:
            render_index = 1
        elif self.state == PlayerState.move.value:
            render_index = 2
        elif self.state == PlayerState.dead.value:
            render_index = 3

        super().render(render_index)


class Heart(GameObject):
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        super().__init__(image_list, render_layer, collide_layer, pos_x, pos_y)
        self.is_bigger = False
        self.beat_interval = 0.5

    def initialize(self):
        self.is_bigger = False
        self.beat_interval = 0.5

    def render(self, index=1):
        self.render_time += clock.get_time() / 1000
        render_index = 1

        if enemy.state == EnemyState.watch.value:
            if enemy.beat_rate <= 8:
                if self.render_time < 0.53:
                    render_index = 2
                elif self.render_time < 1.06:
                    render_index = 1
                else:
                    self.render_time = 0
            else:
                if self.render_time < 0.265:
                    render_index = 2
                elif self.render_time < 0.53:
                    render_index = 1
                else:
                    self.render_time = 0
        else:
            render_index = 1

        super().render(render_index)


class Rod(GameObject):
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        super().__init__(image_list, render_layer, collide_layer, pos_x, pos_y)
        self.is_left = True
        self.speed = 50
        self.key_down = False
        self.save = False

    def initialize(self):
        self.is_left = True
        self.speed = 50
        self.pos_x = ROAD_POS_X
        self.key_down = False
        self.save = False

    def update(self):
        if enemy.state == EnemyState.watch.value:
            key = pygame.key.get_pressed()

            if enemy.state == EnemyState.watch.value:
                if key[pygame.K_SPACE] == 1 and self.key_down is False:
                    self.key_down = True
                elif key[pygame.K_SPACE] == 0 and self.key_down is True:
                    self.key_down = False

            if self.is_left is True:
                self.pos_x += enemy.beat_rate * self.speed * clock.get_time() / 1000

                if self.pos_x < 300:
                    if self.key_down is True:
                        if check_collide_rect(self, line_safe_zone):
                            if self.save is False:
                                effect.effect_on(self.pos_x - 6, self.pos_y - 6)
                                self.save = True
                        elif self.save is False:
                            effect.effect_on(self.pos_x - 6, self.pos_y - 6)
                            player.state = PlayerState.dead.value
                else:
                    self.pos_x = 300
                    self.is_left = False

                    if self.save is False:
                        player.state = PlayerState.dead.value

                    self.save = False

            elif self.is_left is False:
                self.pos_x -= enemy.beat_rate * self.speed * clock.get_time() / 1000

                if self.pos_x > ROAD_POS_X:
                    if self.key_down is True:
                        if check_collide_rect(self, line_safe_zone):
                            if self.save is False:
                                effect.effect_on(self.pos_x - 6, self.pos_y - 6)
                                self.save = True
                        elif self.save is False:
                            effect.effect_on(self.pos_x - 6, self.pos_y - 6)
                            player.state = PlayerState.dead.value
                else:
                    self.pos_x = ROAD_POS_X
                    self.is_left = True

                    if self.save is False:
                        player.state = PlayerState.dead.value

                    self.save = False
        else:
            self.initialize()


class Effect(GameObject):
    def __init__(self, image_list, render_layer, collide_layer, pos_x=0, pos_y=0):
        super().__init__(image_list, render_layer, collide_layer, pos_x, pos_y)
        self.render_time = 0
        self.render_state = False


    def initialize(self):
        self.render_time = 0
        self.render_state = False
        self.pos_x = 0
        self.pos_y = 0

    def effect_on(self, pos_x, pos_y):
        self.initialize()
        self.render_state = True
        self.pos_x = pos_x
        self.pos_y = pos_y

    def render(self, index=1):
        render_index = 0

        if self.render_state is True:
            self.render_time += clock.get_time() / 1000

            if self.render_time < 0.05:
                render_index = 1
            elif self.render_time < 0.1:
                render_index = 2
            elif self.render_time < 0.15:
                render_index = 3
            elif self.render_time < 0.2:
                render_index = 4
            elif self.render_time < 0.25:
                render_index = 5
            else:
                render_index = 0

        super().render(render_index)


# 충돌 계산을 위해 렉트 객체를 만들어주는 함수
def calc_rect_collider(game_object):
    # 렉트 객체 초기화
    rect = pygame.Rect(0, 0, 0, 0)

    # 오브젝트가 플레이어라면 충돌 렉트 사이즈에 맞게 재조정
    if isinstance(game_object, Player) or isinstance(game_object, OtherPlayer):
        rect.left = game_object.pos_x + game_object.width / 2 - game_object.col_width / 2
        rect.top = game_object.pos_y + game_object.height - game_object.col_height
        rect.width = game_object.col_width
        rect.height = game_object.col_height
    # 나머지 경우에는 이미지 크기와 위치를 그대로 적용
    else:
        rect.left = game_object.pos_x
        rect.top = game_object.pos_y
        rect.width = game_object.col_width
        rect.height = game_object.col_height

    return rect  # 렉트 객체를 반환


# 두 객체가 렉트 충돌을 하는지 판별하는 함수
def check_collide_rect(a, b):
    # calc_rect_collider함수로 렉트 객체를 생성한 뒤 비교
    a.rect = calc_rect_collider(a)
    b.rect = calc_rect_collider(b)

    # 충돌 결과를 리턴
    return a.rect.colliderect(b.rect)


def play_gunshot_sound():
    index = random.randint(0, 5)
    gunshot_sound_list[index].play()

# 스크린 정의
pygame.init()
pygame.display.set_caption('Squid Game - Mugungwha')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

icon_image = pygame.image.load('resources/images/icon.png')
pygame.display.set_icon(icon_image)

# 사운드 로드
voice_sound = pygame.mixer.Sound('resources/sounds/voice.wav')
voice_length = voice_sound.get_length()

heartbeat_sound_slow = pygame.mixer.Sound('resources/sounds/heart_beat_slow.wav')
heartbeat_sound_fast = pygame.mixer.Sound('resources/sounds/heart_beat_fast.wav')

gunshot_sound_list = []
for i in range(1, 7):
    gunshot_sound_list.append(pygame.mixer.Sound('resources/sounds/bang' + str(i) + '.ogg'))

clear_sound = pygame.mixer.Sound('resources/sounds/clear.wav')

# 이미지 로드
background_image_list = [None, pygame.image.load('resources/images/background.png')]

heart_image_list = [None]
for i in range(1, 3):
    heart_image_list.append(pygame.image.load('resources/images/heart' + str(i) + '.png'))

line_image_list = [None, pygame.image.load('resources/images/line.png')]

line_safe_zone_image_list = [None, pygame.image.load('resources/images/line_safe_zone.png')]

rod_image_list = [None, pygame.image.load('resources/images/rod.png')]

effect_image_list = [None]
for i in range(1, 6):
    effect_image_list.append(pygame.image.load('resources/images/effect' + str(i) + '.png'))

enemy_image_list = [None]
for i in range(1, 3):
    enemy_image_list.append(pygame.image.load('resources/images/enemy' + str(i) + '.png'))

player_image_list = [None]
for i in range(1, 4):
    player_image_list.append(pygame.image.load('resources/images/player' + str(i) + '.png'))

other_player_man_list = [None]
for i in range(1, 4):
    other_player_man_list.append(pygame.image.load('resources/images/man' + str(i) + '.png'))

other_player_woman_list = [None]
for i in range(1, 4):
    other_player_woman_list.append(pygame.image.load('resources/images/woman' + str(i) + '.png'))

# 폰트 로드
timer_font = pygame.font.Font('resources/fonts/LAB디지털.ttf', 40)
small_font = pygame.font.Font('resources/fonts/DungGeunMo.ttf', 30)
default_font = pygame.font.Font('resources/fonts/DungGeunMo.ttf', 40)
large_font = pygame.font.Font('resources/fonts/DungGeunMo.ttf', 60)

# 오브젝트 관리 리스트 생성
update_object_list = []

render_list = []
for i in range(RenderLayer.max_length.value):
    render_list.append([])

collision_list = []
for i in range(CollideLayer.max_length.value):
    collision_list.append([])

# 오브젝트 초기화
background = GameObject(background_image_list, RenderLayer.back.value, CollideLayer.none.value)

heart = Heart(heart_image_list, RenderLayer.ui_front.value, CollideLayer.none.value)
heart.pos_x = 0
heart.pos_y = SCREEN_HEIGHT - 45

line = GameObject(line_image_list, RenderLayer.ui_back.value, CollideLayer.none.value)
line.pos_x = 10
line.pos_y = SCREEN_HEIGHT - 28

line_safe_zone = GameObject(line_safe_zone_image_list, RenderLayer.ui_back.value, CollideLayer.none.value)
line_safe_zone.pos_x = 140
line_safe_zone.pos_y = SCREEN_HEIGHT - 28

rod = Rod(rod_image_list, RenderLayer.ui_middle.value, CollideLayer.none.value)
rod.pos_x = ROAD_POS_X
rod.pos_y = SCREEN_HEIGHT - rod.height - 3

effect = Effect(effect_image_list, RenderLayer.ui_middle.value, CollideLayer.none.value)

enemy = Enemy(enemy_image_list, RenderLayer.middle.value, CollideLayer.none.value)
enemy.pos_x = SCREEN_WIDTH / 2 - enemy.width / 2
enemy.pos_y = 18

player = Player(player_image_list, RenderLayer.front_2.value, CollideLayer.group_a.value)
player.initialize()

man_count = random.randint(int((MAX_PLAYER_COUNT + 1) / 3 * 1), int((MAX_PLAYER_COUNT + 1) / 3 * 2))
woman_count = MAX_PLAYER_COUNT - man_count

for i in range(man_count):
    other_player = OtherPlayer(other_player_man_list, RenderLayer.front_1.value, CollideLayer.group_b.value)
    other_player.initialize()

for i in range(woman_count):
    other_player = OtherPlayer(other_player_woman_list, RenderLayer.front_1.value, CollideLayer.group_b.value)
    other_player.initialize()

# 기타 변수 초기화
clock = pygame.time.Clock()
is_running = True
scene_index = Scene.menu.value
game_timer = 0
is_game_success = False

while is_running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
            if scene_index == Scene.menu.value:
                if event.key == pygame.K_SPACE:
                    scene_index = Scene.play.value
            if scene_index == Scene.play.value:
                if event.key == pygame.K_d:
                    if enemy.state == EnemyState.ready.value:
                        enemy.state = EnemyState.watch.value
                    elif enemy.state == EnemyState.watch.value:
                        enemy.state = EnemyState.ready.value
            if scene_index == Scene.result.value:
                if event.key == pygame.K_SPACE:
                    scene_index = Scene.menu.value

    if scene_index == Scene.menu.value:
        game_timer = 0
        is_game_success = False
        other_player_move_range = 10

        for game_object in update_object_list:
            game_object.initialize()

        screen.blit(background_image_list[1], (0, 0))
        screen.blit(enemy_image_list[2], (enemy.pos_x, enemy.pos_y))

        # 타이틀
        result_text = large_font.render('오징어 게임', True, (203, 36, 89))
        text_rect = result_text.get_rect()
        text_rect.centerx = round(SCREEN_WIDTH / 2)
        text_rect.y = 200
        screen.blit(result_text, text_rect)

        # 정보 텍스트
        replay_text = default_font.render('시작, 심장박동: SPACE 키', True, (0, 0, 0))
        text_rect = replay_text.get_rect()
        text_rect.centerx = round(SCREEN_WIDTH / 2)
        text_rect.y = 400
        screen.blit(replay_text, text_rect)

        # 정보 텍스트
        replay_text = default_font.render('이동: 방향키', True, (0, 0, 0))
        text_rect = replay_text.get_rect()
        text_rect.centerx = round(SCREEN_WIDTH / 2)
        text_rect.y = 500
        screen.blit(replay_text, text_rect)

    if scene_index == Scene.play.value:
        game_timer += clock.get_time() / 1000

        if game_timer > 35:
            other_player_move_range = 4

        if game_timer > 44:
            other_player_move_range = 2

        if game_timer >= REMAIN_TIME:
            game_timer = REMAIN_TIME
            player.state = PlayerState.dead.value

        for game_object in update_object_list:
            game_object.update()

        player.restore_speed()

        for game_object in collision_list[CollideLayer.group_b.value]:
            if check_collide_rect(player, game_object):
                if game_object.state == PlayerState.dead.value:
                    player.speed = 1

        for layer in render_list:
            for game_object in layer:
                game_object.render()
                # pygame.draw.rect(screen, (0, 255, 0), calc_rect_collider(game_object), 1)

        timer_text = timer_font.render('TIME : ' + str(round(REMAIN_TIME - game_timer, 2)), True, (203, 36, 89))
        screen.blit(timer_text, (SCREEN_WIDTH - 220, 15))

    if scene_index == Scene.result.value:
        voice_sound.stop()
        heartbeat_sound_slow.stop()
        heartbeat_sound_fast.stop()

        # 게임 결과 텍스트 표시
        if player.state == PlayerState.success.value:
            result_string = '성   공'
            if is_game_success is False:
                clear_sound.play()
                is_game_success = True
        else:
            result_string = '실   패'

        # 게임 결과 텍스트
        result_text = large_font.render(result_string, True, (203, 36, 89))
        text_rect = result_text.get_rect()
        text_rect.centerx = round(SCREEN_WIDTH / 2)
        text_rect.y = 200
        screen.blit(result_text, text_rect)

        # 남은 시간 텍스트
        if player.state == PlayerState.success.value:
            score_text = default_font.render('남은 시간: ' + str(round(REMAIN_TIME - game_timer, 3)), True, (0, 0, 0))
            text_rect = score_text.get_rect()
            text_rect.centerx = round(SCREEN_WIDTH / 2)
            text_rect.y = 400
            screen.blit(score_text, text_rect)

        # 재시작 정보 텍스트
        replay_text = default_font.render('재시작: SPACE 키', True, (0, 0, 0))
        text_rect = replay_text.get_rect()
        text_rect.centerx = round(SCREEN_WIDTH / 2)
        text_rect.y = 500
        screen.blit(replay_text, text_rect)

    pygame.display.update()

pygame.quit()