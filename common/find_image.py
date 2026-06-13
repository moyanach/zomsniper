import pyautogui

def match_image(template_path, confidence=0.85):
    """在当前屏幕中寻找目标图片，返回中心坐标"""
    try:
        location = pyautogui.locateOnScreen(template_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            print(f"   ✅ 匹配成功 -> ({int(center.x)}, {int(center.y)})")
            return center
        else:
            print(f" ❌ 未匹配到模板 [{template_path}]（置信度阈值: {confidence}）")
    except Exception as e:
        print(f"⚠️ 图片识别异常 [{template_path}]: {e}")
    return None