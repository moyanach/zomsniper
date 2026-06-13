import random
import time

from common.base_autogui import BaseAutoGui
from skills.choose_wenydadan import ChooseWenYuDadan
from skills.choose_zidan import ChooseZidan
from skills.choose_shandian import ChooseShanDian
from skills.choose_zhuangjiache import ChooseZhuangJiaChe
from skills.choose_random import ChooseRandom

zi_dan = ChooseZidan()
wen_ya_dan = ChooseWenYuDadan()
shan_dian = ChooseShanDian()
zhuang_jia_che = ChooseZhuangJiaChe()  
random_skill = ChooseRandom()


class ChooseSkills:
    def __init__(self, skills: list = [zi_dan, wen_ya_dan, shan_dian, zhuang_jia_che, random_skill]):
        self.skills = skills
        self.key_skill = [zi_dan, wen_ya_dan]
        self.key_skill_names = [zi_dan.name]
        self.has_chosen_skill = False  # 记录是否匹配到技能

    def choose_skill_by_default(self):
        #  2. 战斗中：自动选择技能（假设技能图标出现时点击）
        auto_gui = BaseAutoGui()
        skill_pos = auto_gui.match_image("assets/choose_skill.png")
        if skill_pos:
            if auto_gui.skil_click(skill_pos, "选择默认中间技能"):
                time.sleep(1)

    def final_choose_skill(self):
        self.has_chosen_skill = False  # 重置状态
        for skill in self.skills:
            point = skill.choose_skill()
            if point:
                # 如果匹配到技能，则判断是否是关键技能，如果不是，尝试补偿一次
                if skill.name not in self.key_skill_names:
                    for k_skill in self.key_skill:
                        k_point = k_skill.choose_skill()
                        if k_point:
                            skill.auto_gui.skil_click(k_point, f"{k_skill.name}技能")
                            self.has_chosen_skill = True
                            break
                    continue
                else:
                    skill.auto_gui.skil_click(point, f"{skill.name}技能")
                    self.has_chosen_skill = True
                    break
        if not self.has_chosen_skill:
            self.choose_skill_by_default()
        # continue