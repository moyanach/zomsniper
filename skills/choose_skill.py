
import time
import random

import pyautogui

from common.find_image import match_image
from skills.choose_wenydadan import ChooseWenYuDadan
from skills.choose_zidan import ChooseZidan
from skills.choose_shandian import ChooseShanDian
from skills.choose_zhuangjiache import ChooseZhuangJiaChe

zi_dan = ChooseZidan()
wen_ya_dan = ChooseWenYuDadan()
shan_dian = ChooseShanDian()
zhuang_jia_che = ChooseZhuangJiaChe()   


class ChooseSkills:
    def __init__(self, skills: list = [zi_dan, wen_ya_dan, shan_dian, zhuang_jia_che]):
        self.skills = skills


    def skil_click(self, pos, description=""):
        """安全点击：带随机偏移和分步操作（技能点击位置下移 100 像素）"""
        if pos is None:
            print(f"❌ 未找到 {description} 位置，跳过点击")
            return False
        
        screen_w, screen_h = pyautogui.size()
        
        # 加上模拟器窗口偏移 + 技能按钮下移
        x = int(pos.x) * 0.5 
        y = int(pos.y) * 0.5 
        
        # 验证坐标是否在屏幕范围内
        if x < 0 or x >= screen_w or y < 0 or y >= screen_h:
            print(f"❌ 坐标 ({x}, {y}) 超出屏幕范围 ({screen_w}x{screen_h})，跳过点击")
            return False
        
        # 添加微小随机偏移（模拟人类操作，避免被检测）
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)
        target_x, target_y = x + offset_x, y + offset_y
        
        # 确保偏移后仍在屏幕内
        target_x = max(0, min(screen_w - 1, target_x))
        target_y = max(0, min(screen_h - 1, target_y))
        
        print(f"🖱️ 点击 {description}: ({target_x}, {target_y})")
        
        # 分两步：先移动再点击，带 duration 让移动更自然
        pyautogui.moveTo(target_x, target_y , duration=0.2)
        time.sleep(0.1)  # 短暂停顿
        pyautogui.click()
        return True

    def choose_skill_by_default(self):
        #  2. 战斗中：自动选择技能（假设技能图标出现时点击）
        skill_pos = match_image("assets/choose_skill.png")
        if skill_pos:
            if self.skil_click(skill_pos, "选择中间技能"):
                time.sleep(1)

    def final_choose_skill(self):
        has_choose_skill = False
        for skill in self.skills:
            point = skill.choose_skill()
            if point:
                if self.skil_click(point, f"{skill.name}技能"):
                    time.sleep(1)
                    has_choose_skill = True
                    break
        if not has_choose_skill:
            self.choose_skill_by_default()
        # continue