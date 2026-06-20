[app]

# (str) Titre de votre application
title = DetecteurCouleur

# (str) Nom du package
package.name = colorapp

# (str) Domaine du package (org.test)
package.domain = org.monapp

# (str) Code source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (str) Version de l'application
version = 0.1

# (list) Exigences de l'application
# CRUCIAL : Ne retirez pas ces modules !
requirements = python3, kivy, android, pyjnius

# (str) Orientations supportées
orientation = portrait

# (list) Permissions requises (CRUCIAL pour la caméra)
android.permissions = CAMERA

# (int) API Android cible (33 est le standard actuel pour le Play Store)
android.api = 33

# (int) API Android minimum
android.minapi = 21

# (str) Architecture cible
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
