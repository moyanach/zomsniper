from common.base_skill import BaeSkill


class BackIndexBtn(BaeSkill):
    name = "选择返回主界面按钮"

    def __init__(self, images_path: str = "assets/btns/back/"):
        super().__init__(images_path)

    def choose_btn(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = self.auto_gui.match_image(skill_image)
            if point:
                return point
        return None
