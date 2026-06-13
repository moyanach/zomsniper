import os

class BaeSkill:
    def __init__(self, images_path: str = 'assets/zi_dan/'):
        self.images_path = images_path
        self.image_extensions = {'.png', '.jpg', '.jpeg'}

    def find_images(self):
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
        image_list = []
        if os.path.exists(self.images_path ):
            for filename in os.listdir(self.images_path ):
                if os.path.splitext(filename)[1].lower() in self.image_extensions:
                    image_list.append(os.path.join(self.images_path, filename))
        return image_list


