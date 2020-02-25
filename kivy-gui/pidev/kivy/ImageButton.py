from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import os.path

dpea_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "DPEALogoTransparent.png")


class ImageButton(ButtonBehavior, Image):
    """
    Defines an image with button capabilities
    """

    def __init__(self, **kwargs):
        """
        Constructor for the image button
        When using specify : id, source, size, position, on_press, on_release
        :param kwargs: Arguments supplied to super
        """
        super(ImageButton, self).__init__(**kwargs)
        self.size_hint = None, None
        self.keep_ratio = False
        self.allow_stretch = True
        self.size = 150, 150
        self.background_color = 0, 0, 0, 0
        self.background_normal = ''
        self.source = dpea_logo_path
