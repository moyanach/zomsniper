from skills.base_skill import BaeSkill

class ChooseZidan(BaeSkill):
    name = "基础子弹"

    def __init__(self, images_path: str = 'assets/zi_dan/'):
        super().__init__(images_path)

    def choose_skill(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = self.auto_gui.match_image(skill_image)
            if point:
                return point
        return None