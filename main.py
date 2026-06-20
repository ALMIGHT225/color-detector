import colorsys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.label import Label

class ColorDetector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # 1. Flux de la caméra en direct
        self.camera = Camera(play=True, resolution=(640, 480))
        self.add_widget(self.camera)

        # 2. Zone d'affichage textuelle des résultats
        self.result_label = Label(
            text="Pointez le centre de l'écran sur un objet\net touchez le bouton.", 
            size_hint_y=0.25, 
            font_size='18sp',
            halign='center',
            bold=True
        )
        self.add_widget(self.result_label)

        # 3. Bouton de déclenchement
        self.btn = Button(
            text="Identifier la couleur exacte", 
            size_hint_y=0.18,
            background_color=(0.1, 0.7, 0.4, 1),
            font_size='18sp',
            bold=True
        )
        self.btn.bind(on_press=self.get_color)
        self.add_widget(self.btn)

    def get_color(self, instance):
        texture = self.camera.texture
        if not texture:
            self.result_label.text = "[ Erreur : Caméra indisponible ]"
            return

        # Récupération de la matrice de pixels
        pixels = texture.pixels
        w, h = texture.size

        # Ciblage du pixel central exact (l'œil de la caméra)
        cx, cy = w // 2, h // 2
        bpp = 4 if texture.colorfmt == 'rgba' else 3
        index = (cy * w + cx) * bpp
        
        # Extraction des valeurs fondamentales (0 à 255)
        r = pixels[index]
        g = pixels[index+1]
        b = pixels[index+2]

        # Analyse universelle de la couleur
        color_description, hex_code = self.analyze_color_spectrum(r, g, b)
        
        # Mise à jour de l'affichage pour l'utilisateur
        self.result_label.text = (
            f"Nuance : {color_description}\n"
            f"Code Hex : {hex_code}\n"
            f"Composantes : R:{r} V:{g} B:{b}"
        )

    def analyze_color_spectrum(self, r, g, b):
        """
        Analyse mathématiquement n'importe quelle combinaison RGB 
        et retourne une description textuelle en français ainsi que le code HEX.
        """
        # Génération du code Hexadécimal standard
        hex_code = f"#{r:02X}{g:02X}{b:02X}"
        
        # Normalisation des valeurs pour l'espace HSL (0.0 à 1.0)
        r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
        h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
        
        # Conversion de la teinte en degrés (0 à 360°)
        hue_deg = h * 360

        # --- Étape 1 : Gestion des cas extrêmes (Noir, Blanc, Gris) ---
        if l < 0.10:
            return "Noir", hex_code
        if l > 0.92:
            return "Blanc", hex_code
        if s < 0.12:
            if l < 0.35: return "Gris foncé", hex_code
            if l > 0.65: return "Gris clair", hex_code
            return "Gris", hex_code

        # --- Étape 2 : Identification de la famille de couleur (Teinte) ---
        if hue_deg < 15 or hue_deg >= 345:
            base_name = "Rouge"
            if l > 0.65: base_name = "Rose"  # Un rouge très clair est un rose
        elif hue_deg < 45:
            if l < 0.35: base_name = "Marron" # Un orange foncé est un marron
            else: base_name = "Orange"
        elif hue_deg < 70:
            if l < 0.38: base_name = "Olive"
            else: base_name = "Jaune"
        elif hue_deg < 160:
            base_name = "Vert"
        elif hue_deg < 195:
            base_name = "Turquoise / Cyan"
        elif hue_deg < 255:
            base_name = "Bleu"
        elif hue_deg < 300:
            base_name = "Violet"
        else:
            base_name = "Magenta / Pourpre"

        # --- Étape 3 : Application des qualificatifs de précision ---
        modifier = ""
        
        # Précision sur la luminosité (si pas déjà intercepté par une catégorie dédiée)
        if l < 0.35 and base_name not in ["Marron", "Olive"]:
            modifier = " foncé"
        elif l > 0.68 and base_name not in ["Rose", "Jaune"]:
            modifier = " clair"
            
        # Précision sur l'intensité / pureté de la couleur
        if s < 0.35:
            modifier += " pastel" if l > 0.5 else " terne"
        elif s > 0.85:
            modifier += " vif"

        final_name = f"{base_name}{modifier}".strip()
        return final_name, hex_code

class ColorScannerApp(App):
    def build(self):
        # Demande dynamique de la permission de l'appareil photo sur Android
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])
        except ImportError:
            pass # Permet de tester le code sur un ordinateur sans planter
            
        return ColorDetector()

if __name__ == '__main__':
    ColorScannerApp().run()
