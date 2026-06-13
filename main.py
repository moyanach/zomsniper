import pyautogui
import cv2
import numpy as np
import time

from common.base_autogui import BaseAutoGui
from skills.choose_skill import ChooseSkills
from quick_patroal.quick_patroal import QuickPatroal


def auto_battle_loop():
    """
    主循环：根据当前界面状态自动执行操作
    
    状态机：
    - IDLE: 未进入打怪界面，检测开始战斗、前往、等级提升、见面礼、任务礼
    - BATTLE: 已进入打怪界面，检测技能选择和返回按钮
    - FULL_SCAN: 连续多轮未识别到按钮，全量检测所有按钮
    """
    print("🚀 辅助工具已启动，请将游戏窗口置于前台...")
    print("⚠️  提示：确保游戏窗口有 macOS 辅助功能权限")
    print("   系统设置 → 隐私与安全性 → 辅助功能 → 添加终端/iTerm/IDE\n")
    
    auto_gui = BaseAutoGui()
    battle_mode = False  # 战斗模式标志：False=主界面, True=战斗中
    no_match_count = 0   # 连续未匹配次数
    max_no_match = 3     # 连续未匹配阈值，达到后触发全量检测
    
    while True:
        if not battle_mode:
            # ========== 主界面状态：检测开始战斗、前往、奖励按钮 ==========
            battle_mode, no_match_count = _idle_mode(auto_gui, no_match_count, max_no_match)
        else:
            # ========== 战斗模式：检测技能选择、返回按钮 ==========
            battle_mode, no_match_count = _battle_mode(auto_gui, no_match_count, max_no_match)


def _idle_mode(auto_gui, no_match_count, max_no_match):
    """
    主界面状态：检测非战斗相关的按钮
    
    Args:
        auto_gui: BaseAutoGui 实例
        no_match_count: 连续未匹配次数
        max_no_match: 触发全量检测的最大未匹配次数
        
    Returns:
        tuple: (是否进入战斗模式, 更新后的未匹配次数)
    """
    matched = False
    
    # 1. 开始战斗按钮
    start_pos = auto_gui.match_image("assets/start_game_zfb.png")
    if start_pos:
        print(f"✅ [主界面] 检测到开始按钮，点击进入关卡")
        auto_gui.skil_click(start_pos, "开始战斗")
        time.sleep(2)
        matched = True
        return True, 0  # 进入战斗模式，重置计数
    
    # 2. 前往下一关按钮
    next_map_pos = auto_gui.match_image("assets/next_map_zfb.png")
    if next_map_pos:
        print(f"✅ [主界面] 检测到前往按钮，点击进入下一关")
        auto_gui.skil_click(next_map_pos, "前往")
        time.sleep(2)
        matched = True
        return True, 0  # 进入战斗模式，重置计数
    
    # 3. 等级提升按钮
    level_up_pos = auto_gui.match_image("assets/level_up.png")
    if level_up_pos:
        print(f"🎉 [主界面] 检测到等级提升按钮")
        auto_gui.skil_click(level_up_pos, "等级提升", -100)
        time.sleep(1)
        matched = True
    
    # 4. 见面礼按钮
    face_gift_pos = auto_gui.match_image("assets/face_gift.png")
    if face_gift_pos:
        print(f"🎁 [主界面] 检测到见面礼按钮")
        auto_gui.skil_click(face_gift_pos, "见面礼", -500)
        time.sleep(1)
        matched = True
    
    # 5. 任务礼按钮
    task_gift_pos = auto_gui.match_image("assets/task_gift.png")
    if task_gift_pos:
        print(f"📋 [主界面] 检测到任务礼按钮")
        auto_gui.skil_click(task_gift_pos, "任务礼", -200)
        time.sleep(1)
        matched = True
    
    # 未匹配到任何按钮
    if not matched:
        no_match_count += 1
        print(f"⚠️ [主界面] 未检测到任何按钮 (连续 {no_match_count}/{max_no_match} 轮)")
        
        # 达到阈值，触发全量检测
        if no_match_count >= max_no_match:
            print(f"🔄 [全量检测] 连续 {max_no_match} 轮未识别到按钮，开始全量检测所有按钮...")
            _full_scan_mode(auto_gui)
            no_match_count = 0  # 重置计数
    else:
        no_match_count = 0  # 匹配成功，重置计数
    
    # 短暂休眠
    time.sleep(1)
    return False, no_match_count


def _battle_mode(auto_gui, no_match_count, max_no_match):
    """
    战斗模式：检测技能选择和返回按钮
    
    Args:
        auto_gui: BaseAutoGui 实例
        no_match_count: 连续未匹配次数
        max_no_match: 触发全量检测的最大未匹配次数
        
    Returns:
        tuple: (是否保持战斗模式, 更新后的未匹配次数)
    """
    matched = False
    
    # 1. 自动选择技能（检测是否真的匹配到技能）
    choose_skills = ChooseSkills()
    choose_skills.final_choose_skill()  # 执行技能选择
    has_chosen_skill = choose_skills.has_chosen_skill  # 检查是否匹配到技能
    
    if has_chosen_skill:
        matched = True
        print(f"✅ [战斗中] 已选择技能")
    # else:
    #     # 未匹配到技能，尝试默认选择
    #     choose_skills.choose_skill_by_default()
    #     print(f"⚠️ [战斗中] 未匹配到技能，尝试默认选择")
    
    # 2. 返回按钮（关卡结束）
    back_pos = auto_gui.match_image("assets/back_zfb.png")
    if back_pos:
        print(f"🎉 [战斗结束] 检测到返回按钮，准备下一局")
        auto_gui.skil_click(back_pos, "返回")
        time.sleep(2)
        return False, 0  # 返回主界面状态，重置计数
    
    # 3. 连续未匹配检测
    if not matched:
        no_match_count += 1
        print(f"⚠️ [战斗中] 未匹配到技能 (连续 {no_match_count}/{max_no_match} 轮)")
        
        # 达到阈值，触发全量检测
        if no_match_count >= max_no_match:
            print(f"🔄 [全量检测] 连续 {max_no_match} 轮未识别到技能，开始全量检测...")
            _full_scan_mode(auto_gui)
            no_match_count = 0  # 重置计数
    else:
        no_match_count = 0  # 匹配成功，重置计数
    
    # 战斗中，保持战斗模式
    time.sleep(0.5)  # 短暂休眠，避免 CPU 占用过高
    return True, no_match_count


def _full_scan_mode(auto_gui):
    """
    全量检测模式：同时检测所有可能的按钮
    
    用于连续多轮未识别到按钮时的兜底检测
    """
    print(f"🔍 [全量检测] 开始扫描所有可能的按钮...")
    
    # 主界面按钮
    buttons_idle = [
        ("assets/start_game_zfb.png", "开始战斗", 0),
        ("assets/next_map.png", "前往", 0),
        ("assets/level_up.png", "等级提升", -100),
        ("assets/face_gift.png", "见面礼", -500),
        ("assets/task_gift.png", "任务礼", -200),
    ]
    
    # 战斗界面按钮
    buttons_battle = [
        ("assets/back_zfb.png", "返回", 0),
    ]
    
    # 先检测主界面按钮
    for img_path, desc, y_offset in buttons_idle:
        pos = auto_gui.match_image(img_path)
        if pos:
            print(f"✅ [全量检测] 匹配到主界面按钮: {desc}")
            auto_gui.skil_click(pos, desc, y_offset)
            time.sleep(1)
            return  # 匹配到一个就返回
    
    # 再检测战斗界面按钮
    for img_path, desc, y_offset in buttons_battle:
        pos = auto_gui.match_image(img_path)
        if pos:
            print(f"✅ [全量检测] 匹配到战斗按钮: {desc}")
            auto_gui.skil_click(pos, desc, y_offset)
            time.sleep(1)
            return  # 匹配到一个就返回
    
    print(f"⚠️ [全量检测] 未匹配到任何按钮，请检查游戏界面")

if __name__ == "__main__":
    auto_battle_loop()
    # QuickPatroal().choose_run()

    # choose_skill()
    # ChooseSkills().final_choose_skill()