
from skills.base_skill import BaeSkill

class ChooseShanDian(BaeSkill):
    name = "闪电技能"

    def __init__(self, images_path: str = 'assets/shan_dian/'):
        super().__init__(images_path)

    def choose_skill(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point =  self.auto_gui.match_image(skill_image)
            if point:
                return point
        return None