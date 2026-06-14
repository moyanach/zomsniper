import os

from common.base_autogui import BaseAutoGui


class BaeSkill:
    def __init__(self, images_path: str = "assets/zi_dan/"):
        self.images_path = images_path
        self.image_extensions = {".png", ".jpg", ".jpeg"}
        self.auto_gui = BaseAutoGui()
        self.iamges_list = None

    def find_images(self):
        # 加一层读取图片缓存，如果缓存存在，则直接返回缓存，否则读取图片，并缓存
        if self.iamges_list:
            return self.iamges_list
        image_list = []
        if os.path.exists(self.images_path):
            for filename in os.listdir(self.images_path):
                if os.path.splitext(filename)[1].lower() in self.image_extensions:
                    image_list.append(os.path.join(self.images_path, filename))
        self.iamges_list = image_list
        return image_list
