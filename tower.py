import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        x1, y1 = enemy.get_pos()  # 取得 enemy 座標
        x2, y2 = self.center  # 取得 tower 的中心座標
        if math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= self.radius:  # 在攻擊範圍內
            return True
        else:  # 不在攻擊範圍內
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """

        # create semi-transparent surface
        transparent_surface = pygame.Surface((1024, 680), pygame.SRCALPHA)
        transparency = 120  # define transparency: 0~255, 0 is fully transparent
        # draw the rectangle on the transparent surface
        pygame.draw.circle(transparent_surface, (128, 128, 128, transparency),  # 繪製灰色圓圈，顯示攻擊範圍
                           (self.center[0] - self.radius, self.center[1] - self.radius), self.radius)
        # draw three towers on the window
        win.blit(transparent_surface, (150, 150))   # 顯示三個灰色圓圈


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 0.5   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """

        if self.cd_count < self.cd_max_count:  # 冷卻的幀數每 60 幀歸零一次，if 條件為 tower 尚未冷卻完畢
            self.cd_count += 1
            return False
        else:  # tower 冷卻完畢
            self.cd_count = 0  # 幀數歸零
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """

        for i in range(len(enemy_group.get())):  # len(enemy_group.get())：計算有幾隻 enemy
            if self.is_cool_down() and self.range_circle.collide(enemy_group.get()[i]):
                # self.is_cool_down()：判斷 tower 是否冷卻完畢
                # (enemy_group.get()[i])：從 enemy_group 的 list 中，抓出第 i 隻 enemy
                # self.range_circle.collide(enemy_group.get()[i])：判斷第 i 隻 enemy 有無在灰色圈圈內
                enemy_group.get()[i].get_hurt(self.damage)
                # 攻擊符合上述攻擊條件的第 i 隻 enemy

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        return self.rect.collidepoint(x, y)  # 判斷 (x,y) 有無 (Bool) 在 rect 裡面 (return Bool)

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected  # 改變灰色圈圈有無 (Bool) 顯示之狀態

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

