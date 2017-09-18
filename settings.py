class Setting():
    """  存储设置的类  """

    def __init__(self):
        """ 初始化游戏设置 """

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 20

        self.bullet_speed = 100
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 10

