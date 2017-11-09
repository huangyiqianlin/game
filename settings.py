class Setting:
    """  存储设置的类  """

    def __init__(self):
        """ 初始化游戏设置 """

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        # 背景色
        self.bg_color = (230, 230, 230)

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 允许在屏幕上同时出现的子弹数量
        self.bullet_allowed = 10

        self.fleet_drop_speed = 10

        self.ship_limit = 3

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 2

        # 外星人点数的提高速度
        self.score_scale = 1.5

        # 飞船移动速度
        self.ship_speed = 5
        self.bullet_speed = 10

        # 外星人设置
        self.alien_speed = 10

        # fleet_direction = 1表示向右移动 -1 表示向左
        self.fleet_direction = 1

        # 记分
        self.alien_point = 50

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ 初始化随着游戏进行而变化的设置 """

        # 飞船移动速度
        self.ship_speed = 5
        self.bullet_speed = 10

        # 外星人设置
        self.alien_speed = 10

        # 记分,一个外星人值50分
        self.alien_point = 50

    def increase_speed(self):
        """ 提高速度设置和外星人点数 """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.score_scale)
