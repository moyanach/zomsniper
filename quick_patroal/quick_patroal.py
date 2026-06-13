
import time

from skills.base_skill import BaeSkill

class QuickPatroal(BaeSkill):
    name = "快速巡逻"

    def __init__(self, images_path: str = 'assets/quick_xunluo/'):
        super().__init__(images_path)

    def click_xunluoche(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = self.auto_gui.match_image(skill_image)
            if point:
                self.auto_gui.skil_click(point)
                self.auto_gui.skil_click(point)
                time.sleep(3)

                return point
        return None

    def click_qucik_xunluo(self):
        skill_images = self.find_images()
        for skill_image in skill_images:
            point = self.auto_gui.match_image(skill_image)
            if point:
                self.auto_gui.skil_click(point)
                self.auto_gui.safe_scroll(100, point, "开始滚动广告")
                return point
        return None

    def choose_run(self):
        s = 300
        while s:
            point = self.click_xunluoche()
            time.sleep(3)
            self.click_qucik_xunluo()
            time.sleep(1)
            s -= 1
        

