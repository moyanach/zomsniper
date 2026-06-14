from buttons.start_game import StartGameBtn
from buttons.back_index import BackIndexBtn
from buttons.next_map import NextMapBtn
from buttons.stay_index import StayIndexBtn

start_game_btn = StartGameBtn()
back_index_btn = BackIndexBtn()
next_map_btn = NextMapBtn()
stay_index_btn = StayIndexBtn()

btn_maps = {
    "start_game": start_game_btn,
    "back_index": back_index_btn,
    "next_map": next_map_btn,
    "stay_index": stay_index_btn,
}


class ClickFuncButton:
    def __init__(self, btns: list[str]):
        self.btns = btns

    def final_choose_btn_point(self):
        for btn in self.btns:
            btn_obj = btn_maps.get(btn)
            if not btn_obj:
                continue
            point = btn_obj.choose_btn()
            if point:
                return btn_obj, point
        return None, None

    def click_btn(self, y_offset: int):
        btn_obj, point = self.final_choose_btn_point()
        if not btn_obj or not point:
            return False
        btn_obj.auto_gui.btn_click(point, btn_obj.name, y_offset)
        return True
