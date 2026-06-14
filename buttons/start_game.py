from common.base_skill import BaeSkill


class StartGameBtn(BaeSkill):
    name = "选择开始游戏按钮"

    def __init__(self, images_path: str = "assets/btns/startgame/"):
        super().__init__(images_path)

    def choose_btn(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = self.auto_gui.match_image(skill_image)
            if point:
                return point
        return None
