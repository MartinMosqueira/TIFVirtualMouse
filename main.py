# Licensed under NC-PE - For personal and educational use only.
# Copyright © 2025 Martin Mosqueira. All rights reserved.

import dearpygui.dearpygui as dpg
from HandTracker import HandTracker
from ResourcePaths import resource_path

config = {
    "play_sound": True,
    "show_camera": True,
    "camera": "0",  # 0: extern camera, 1: intern camera
    "smoothness": 3.0
}
start_requested = False

def toggle_sound(sender):
    config["play_sound"] = dpg.get_value(sender)

def toggle_camera(sender):
    config["show_camera"] = dpg.get_value(sender)

def combo_camera(sender):
    config["camera"] = dpg.get_value(sender)

def slider_sensibility(sender):
    config["smoothness"] = dpg.get_value(sender)

def on_start(sender, app_data):
    global start_requested
    start_requested = True
    dpg.stop_dearpygui()

def start_tracker():
    tracker = HandTracker(resource_path("model/hand/hand_landmarker.task"), config["smoothness"])
    tracker.enable_sound = config["play_sound"]
    tracker.show_camera = config["show_camera"]
    tracker.camera = config["camera"]
    tracker.run()

if __name__ == "__main__":
    dpg.create_context()

    dpg.set_global_font_scale(0.8)
    with dpg.font_registry():
        my_font = dpg.add_font(resource_path("assets/fonts/MotivaSansBold.woff.ttf"), 22, tag="custom_font")

    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image(resource_path("assets/icons/logo.png"))
        dpg.add_static_texture(width, height, data, tag="imagen_logo")


    with dpg.window(label="Configuration", tag="main_window"):
        with dpg.group(horizontal=True):
            dpg.add_image("imagen_logo", width=80, height=70)
        dpg.add_text("CONFIGURACIÓN")
        dpg.add_spacer(height=7)
        with dpg.group(horizontal=True):
            dpg.add_text(
                "Activar sonido",
                tag="slider_sound",
            )
            dpg.add_checkbox(default_value=True, callback=toggle_sound)
        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_text(
                "Mostrar captura",
                tag="slider_caption"
            )
            dpg.add_checkbox(default_value=True, callback=toggle_camera)
        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_text("Camara")
            dpg.add_combo(["0", "1"] , width=120, default_value = "0", callback=combo_camera)
        dpg.add_spacer(height=5)
        with dpg.group(horizontal=True):
            dpg.add_text(
                "Suavidad",
                tag="slider_smoothness",
            )
            dpg.add_slider_float(
                default_value=3.0,
                min_value=0.1, max_value=5,
                format="%.1f",
                callback=slider_sensibility
            )
        with dpg.tooltip("slider_smoothness"):
            dpg.add_text("Bajo: Cursor muy suave\nAlto: Cursor más reactivo")
        with dpg.tooltip("slider_sound"):
            dpg.add_text("Sonido cuando el gesto es detectado")
        with dpg.tooltip("slider_caption"):
            dpg.add_text("Ventana de captura de la mano")
        dpg.add_spacer(height=60)
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=100)
            dpg.add_button(label="Iniciar", width=100, callback=on_start)
            dpg.add_spacer(width=20)
            dpg.add_button(label="Salir",  width=100, callback=lambda s,a: dpg.stop_dearpygui())
            dpg.add_spacer(width=100)

    with dpg.theme() as global_theme:

        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (23, 29, 36), category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (159, 239, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (34, 50, 45), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5, category=dpg.mvThemeCat_Core)


    dpg.create_viewport(title="Visionic", width=500, height=360, resizable=False, vsync=True)
    dpg.bind_theme(global_theme)
    dpg.bind_font("custom_font")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)

    dpg.start_dearpygui()
    dpg.destroy_context()

    if start_requested:
        start_tracker()
