
from common.find_image import match_image
from skills.base_skill import BaeSkill

class ChooseWenYuDadan(BaeSkill):
    name = "温压弹"

    def __init__(self, images_path: str = 'assets/wen_ya_dan/'):
        super().__init__(images_path)

    def choose_skill(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = match_image(skill_image)
            if point:
                return point
        return None