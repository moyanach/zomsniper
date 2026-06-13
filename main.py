import pyautogui
import cv2
import numpy as np
import time
import random

from skills.choose_skill import ChooseSkills



# 设置 PyAutoGUI 的安全选项
pyautogui.FAILSAFE = True  # 鼠标移到左上角可紧急停止
pyautogui.PAUSE = 0.15     # 每次操作后的微小延迟

# 模拟器窗口偏移量（需要根据实际情况调整）
# 如果游戏运行在模拟器中，需要加上模拟器窗口相对于屏幕左上角的偏移
EMULATOR_OFFSET_X = 0  # 模拟器窗口 X 偏移
EMULATOR_OFFSET_Y = 0  # 模拟器窗口 Y 偏移

def find_image(template_path, confidence=0.75):
    """在当前屏幕中寻找目标图片，返回中心坐标"""
    try:
        import os
        # 检查文件是否存在
        if not os.path.exists(template_path):
            print(f"❌ 文件不存在 [{template_path}]")
            return None
        
        # 打印图片尺寸用于调试
        from PIL import Image
        img = Image.open(template_path)
        print(f"   📷 模板图片 [{template_path}]: {img.size}")
        
        location = pyautogui.locateOnScreen(template_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            print(f"   ✅ 匹配成功 -> ({int(center.x)}, {int(center.y)})")
            return center
        else:
            print(f"   ❌ 未匹配到模板 [{template_path}]（置信度阈值: {confidence}）")
    except Exception as e:
        print(f"⚠️ 图片识别异常 [{template_path}]: {e}")
    return None

def safe_click(pos, description=""):
    """安全点击：带随机偏移和分步操作"""
    if pos is None:
        return False
    
    screen_w, screen_h = pyautogui.size()
    
    # 加上模拟器窗口偏移（如果游戏在模拟器中运行）
    x = int(pos.x) * 0.5 + EMULATOR_OFFSET_X
    y = int(pos.y) * 0.5 + EMULATOR_OFFSET_Y
    
    # 验证坐标是否在屏幕范围内
    if x < 0 or x >= screen_w or y < 0 or y >= screen_h:
        print(f"❌ 坐标 ({x}, {y}) 超出屏幕范围 ({screen_w}x{screen_h})，跳过点击")
        print(f"   提示：如果游戏在模拟器中运行，请设置 EMULATOR_OFFSET_X/Y")
        return False
    
    # 添加微小随机偏移（模拟人类操作，避免被检测）
    offset_x = random.randint(-3, 3)
    offset_y = random.randint(-3, 3)
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

# def skil_click(pos, description=""):
#     """安全点击：带随机偏移和分步操作（技能点击位置下移 100 像素）"""
#     if pos is None:
#         return False
    
#     screen_w, screen_h = pyautogui.size()
    
#     # 加上模拟器窗口偏移 + 技能按钮下移
#     x = int(pos.x) * 0.5 + EMULATOR_OFFSET_X
#     y = int(pos.y) * 0.5  + EMULATOR_OFFSET_Y + 100
    
#     # 验证坐标是否在屏幕范围内
#     if x < 0 or x >= screen_w or y < 0 or y >= screen_h:
#         print(f"❌ 坐标 ({x}, {y}) 超出屏幕范围 ({screen_w}x{screen_h})，跳过点击")
#         return False
    
#     # 添加微小随机偏移（模拟人类操作，避免被检测）
#     offset_x = random.randint(-3, 3)
#     offset_y = random.randint(-3, 3)
#     target_x, target_y = x + offset_x, y + offset_y
    
#     # 确保偏移后仍在屏幕内
#     target_x = max(0, min(screen_w - 1, target_x))
#     target_y = max(0, min(screen_h - 1, target_y))
    
#     print(f"🖱️ 点击 {description}: ({target_x}, {target_y})")
    
#     # 分两步：先移动再点击，带 duration 让移动更自然
#     pyautogui.moveTo(target_x, target_y , duration=0.2)
#     time.sleep(0.1)  # 短暂停顿
#     pyautogui.click()
    
#     return True


# def choose_skill(skills: list = [zi_dan, wen_ya_dan]):
#     for skill in skills:
#         point = skill.choose_skill()
#         print(f"skill: {skill.name}")
#         if point:
#             print("🛡️ 检测到技能选择，自动点击")
#             if skil_click(point, "技能"):
#                 time.sleep(1)
#             continue
        

def auto_battle_loop():
    print("🚀 辅助工具已启动，请将游戏窗口置于前台...")
    print("⚠️  提示：确保游戏窗口有 macOS 辅助功能权限")
    print("   系统设置 → 隐私与安全性 → 辅助功能 → 添加终端/iTerm/IDE\n")
    
    while True:
        # 1. 寻找并点击"开始战斗"按钮
        start_pos = find_image("assets/start_game2.png")
        if start_pos:
            print(f"✅ 检测到开始按钮，点击进入关卡")
            if safe_click(start_pos, "开始战斗"):
                time.sleep(2)
            # continue

        # 1. 寻找并点击"前往"按钮
        next_map_pos = find_image("assets/next_map.png")
        if next_map_pos:
            print(f"✅ 检测到前往按钮，点击进入下一关关卡")
            if safe_click(next_map_pos, "前往"):
                time.sleep(2)
            continue

        ChooseSkills().final_choose_skill()
        
            
        # 3. 结算界面：点击"继续"或"返回"
        back_pos = find_image("assets/back.png")
        if back_pos:
            print("🎉 关卡结束，准备下一局")
            if safe_click(back_pos, "返回"):
                time.sleep(2)
            continue

        # 未匹配到任何状态，短暂休眠避免 CPU 占用过高
        time.sleep(2)

if __name__ == "__main__":
    auto_battle_loop()

    # choose_skill()
    # ChooseSkills().final_choose_skill()