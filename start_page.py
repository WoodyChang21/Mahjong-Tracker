from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, Clock, StringProperty, ObjectProperty
from kivy.animation import Animation
from kivymd.uix.button import MDRectangleFlatButton

class Start_page(RelativeLayout):

    def __init__(self,**kwargs):
        super(RelativeLayout, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)