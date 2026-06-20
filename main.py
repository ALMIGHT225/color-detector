import cv2
import numpy as np
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window

def get_color_name(b, g, r):
    # Conversion en hexadécimal
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return f"RGB({r},{g},{b}) - {hex_color}"

class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.img = Image()
        self.label = Label(text="Clique sur l’écran pour identifier une couleur",
                           size_hint=(1, 0.2))
        self.layout.add_widget(self.img)
        self.layout.add_widget(self.label)

        # Capture caméra
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/30.0)

        # Gestion du clic
        Window.bind(on_touch_down=self.on_touch)

        return self.layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Conversion pour affichage Kivy
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture
            self.frame = frame

    def on_touch(self, window, touch):
        if hasattr(self, 'frame'):
            # Conversion coordonnées écran → image
            x = int(touch.x)
            y = int(Window.height - touch.y)  # inversion verticale
            if 0 <= x < self.frame.shape[1] and 0 <= y < self.frame.shape[0]:
                b, g, r = self.frame[y, x]
                color_name = get_color_name(b, g, r)
                self.label.text = f"Couleur détectée : {color_name}"

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    CameraApp().run()
