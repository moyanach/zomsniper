import random
import time

import pyautogui

# 设置 PyAutoGUI 的安全选项
pyautogui.FAILSAFE = True  # 鼠标移到左上角可紧急停止
pyautogui.PAUSE = 0.15  # 每次操作后的微小延迟


class BaseAutoGui(object):
    def __init__(self):
        pass

    def match_image(self, template_path, confidence=0.85):
        """在当前屏幕中寻找目标图片，返回中心坐标"""
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                print(f"✅ 匹配成功 -> ({int(center.x)}, {int(center.y)})")
                return center
            else:
                print(f" ❌ 未匹配到模板 [{template_path}]")
        except Exception as e:
            print(f"⚠️ 图片识别异常 [{template_path}]: {e}")
        return None

    def skil_click(self, pos, description="", y_offset=0):
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
        offset_y = random.randint(-1, 1) + y_offset
        target_x, target_y = x + offset_x, y + offset_y

        # 确保偏移后仍在屏幕内
        target_x = max(0, min(screen_w - 1, target_x))
        target_y = max(0, min(screen_h - 1, target_y))

        print(f"🖱️ 点击 {description}: ({target_x}, {target_y})")

        # 分两步：先移动再点击，带 duration 让移动更自然
        pyautogui.moveTo(target_x, target_y, duration=0.2)
        time.sleep(1)  # 短暂停顿
        pyautogui.doubleClick()
        print("技能选择完成，休眠 6 秒，等待下一次选择")
        time.sleep(6)  # 短暂停顿

        return True

    def btn_click(self, pos, description="", y_offset=0):
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
        offset_y = random.randint(-1, 1) + y_offset
        target_x, target_y = x + offset_x, y + offset_y

        # 确保偏移后仍在屏幕内
        target_x = max(0, min(screen_w - 1, target_x))
        target_y = max(0, min(screen_h - 1, target_y))

        print(f"🖱️ 点击 {description}: ({target_x}, {target_y})")

        # 分两步：先移动再点击，带 duration 让移动更自然
        pyautogui.moveTo(target_x, target_y, duration=0.2)
        time.sleep(1)  # 短暂停顿
        pyautogui.doubleClick()
        print("技能选择完成，休眠 2 秒，等待下一次选择")
        time.sleep(2)  # 短暂停顿
        return True

    def safe_scroll(self, clicks, pos, description=""):
        """安全滚动：带坐标校验和人类模拟停顿

        Args:
            clicks (int): 滚动的格数，正数向上滚动，负数向下滚动
            x (int, optional): 滚动发生的x坐标，默认为当前鼠标位置
            y (int, optional): 滚动发生的y坐标，默认为当前鼠标位置
            description (str, optional): 操作描述，用于日志打印
        """

        # 加上模拟器窗口偏移 + 技能按钮下移
        # x = int(pos.x) * 0.5
        # y = int(pos.y) * 0.5
        x = y = None

        screen_w, screen_h = pyautogui.size()
        # 如果未指定坐标，获取当前鼠标位置
        if x is None or y is None:
            current_x, current_y = pyautogui.position()
            x = x if x is not None else current_x
            y = y if y is not None else current_y

        # 验证坐标是否在屏幕范围内
        if x < 0 or x >= screen_w or y < 0 or y >= screen_h:
            print(
                f"❌ 滚动坐标 ({x}, {y}) 超出屏幕范围 ({screen_w}x{screen_h})，跳过滚动"
            )
            return False

        direction = "⬆️ 向上" if clicks > 0 else "⬇️ 向下"
        print(f"📜 {direction}滚动 {description}: 位置({x}, {y}), 格数({clicks})")

        # 先移动到指定位置，模拟人类操作
        pyautogui.moveTo(x, y, duration=0.2)
        time.sleep(0.1)

        # 执行滚动
        s = 40
        while s > 0:
            pyautogui.scroll(clicks, x=x, y=y)
            time.sleep(0.2)  # 滚动后短暂停顿，等待界面响应
            s -= 1
            print(f"滚动中 {s}")

        return True
