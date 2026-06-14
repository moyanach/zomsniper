from common.base_skill import BaeSkill


class ChooseShenXian(BaeSkill):
    name = "射线技能"

    def __init__(self, images_path: str = "assets/skills/e_shen_xian/"):
        super().__init__(images_path)

    def choose_skill(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = self.auto_gui.match_image(skill_image)
            if point:
                return point
        return None
