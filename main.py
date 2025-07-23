# Licensed under NC-PE - For personal and educational use only.
# Copyright © 2025 Martin Mosqueira. All rights reserved.

import dearpygui.dearpygui as dpg
from HandTracker import HandTracker
from ResourcePaths import resource_path
from controller.AdaptiveCursor import AdaptiveCursor

config = {
    "play_sound": True,
    "show_camera": True,
    "camera": "0",  # 0: extern camera, 1: intern camera
    "smoothness": 3.0,
    "amplification": 1.5
}
start_requested = False


def toggle_sound(sender):
    config["play_sound"] = dpg.get_value(sender)


def toggle_camera(sender):
    config["show_camera"] = dpg.get_value(sender)


def combo_camera(sender):
    config["camera"] = dpg.get_value(sender)


def slider_sensibility(sender):
    value = dpg.get_value(sender)
    config["smoothness"] = value
    dpg.set_value("smoothness_value", f"{value:.1f}")


def slider_amplification(sender):
    value = dpg.get_value(sender)
    config["amplification"] = value
    dpg.set_value("amplification_value", f"{value:.1f}")


def on_start(sender, app_data):
    global start_requested
    start_requested = True
    dpg.stop_dearpygui()


def start_tracker():
    cursor = AdaptiveCursor(
        alpha_min=0.2,
        alpha_max=0.9,
        speed_sens=config["smoothness"],
        amplification=config["amplification"]
    )

    tracker = HandTracker(
        model_hand=resource_path("model/hand/hand_landmarker.task"),
        cursor_controller=cursor
    )
    tracker.enable_sound = config["play_sound"]
    tracker.show_camera = config["show_camera"]
    tracker.camera = config["camera"]
    tracker.run()


if __name__ == "__main__":
    dpg.create_context()

    dpg.set_global_font_scale(0.8)
    with dpg.font_registry():
        title_font = dpg.add_font(resource_path("assets/fonts/Inter-Medium.otf"), 30, tag="title_font")
        text_font = dpg.add_font(resource_path("assets/fonts/Inter-Medium.otf"), 25, tag="text_font")

    with dpg.texture_registry(show=False):
        width, height, channels, data = dpg.load_image(resource_path("assets/icons/logo.png"))
        dpg.add_static_texture(width, height, data, tag="imagen_logo")

    with dpg.theme(tag="start_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (56, 171, 74), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="exit_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (219, 61, 61), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5, category=dpg.mvThemeCat_Core)

    with dpg.theme(tag="slider_theme"):
        with dpg.theme_component(dpg.mvSliderFloat):
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (65, 150, 245), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (85, 180, 255), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (20, 20, 30), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 10, category=dpg.mvThemeCat_Core)

    with dpg.window(label="Configuration", tag="main_window"):
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=75)
            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_image("imagen_logo", width=250, height=90)
                dpg.add_spacer(height=20)
                dpg.add_text("CONFIGURACIÓN", tag="title_config")
                dpg.bind_item_font("title_config", "title_font")
                dpg.add_spacer(height=7)
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(default_value=True, callback=toggle_sound)
                    dpg.add_text(
                        "Activar sonido",
                        tag="sound",
                    )
                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(default_value=True, callback=toggle_sound)
                    dpg.add_text(
                        "Mostrar captura",
                        tag="caption"
                    )
                dpg.add_spacer(height=5)
                dpg.add_text("Cámara")
                dpg.add_combo(["0", "1"], width=120, default_value="0", callback=combo_camera)
                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    dpg.add_text("Suavidad", tag="smoothness")
                    dpg.add_spacer(width=75)
                    dpg.add_text("3.0", tag="smoothness_value")
                dpg.add_slider_float(
                    width=200,
                    default_value=3.0,
                    min_value=0.1, max_value=5,
                    format="",
                    callback=slider_sensibility,
                    tag="slider_sensibility"
                )
                dpg.bind_item_theme("slider_sensibility", "slider_theme")
                dpg.add_spacer(height=5)
                with dpg.group(horizontal=True):
                    dpg.add_text("Amplificar", tag="amplification")
                    dpg.add_spacer(width=75)
                    dpg.add_text("1.5", tag="amplification_value")
                dpg.add_slider_float(
                    width=200,
                    default_value=1.5,
                    min_value=0.5, max_value=4.0,
                    format="",
                    callback=slider_amplification,
                    tag="slider_amplification"
                )
                dpg.bind_item_theme("slider_amplification", "slider_theme")
                with dpg.tooltip("amplification"):
                    dpg.add_text("Amplitud de alcance del cursor")
                with dpg.tooltip("smoothness"):
                    dpg.add_text("Bajo: Cursor muy suave\nAlto: Cursor más reactivo")
                with dpg.tooltip("sound"):
                    dpg.add_text("Sonido cuando el gesto es detectado")
                with dpg.tooltip("caption"):
                    dpg.add_text("Ventana de captura de la mano")
                dpg.add_spacer(height=20)
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Iniciar", width=120, height=45, callback=on_start, tag="start_button")
                    dpg.bind_item_theme("start_button", "start_button_theme")
                    dpg.bind_item_font("start_button", "title_font")
                    dpg.add_spacer(width=5)
                    dpg.add_button(label="Salir", width=120, height=45, callback=lambda s, a: dpg.stop_dearpygui(),
                                   tag="exit_button")
                    dpg.bind_item_theme("exit_button", "exit_button_theme")
                    dpg.bind_item_font("exit_button", "title_font")
            dpg.add_spacer(width=50)

    with dpg.theme() as global_theme:

        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (29, 35, 51), category=dpg.mvThemeCat_Core)

    dpg.create_viewport(title="Visionic", width=400, height=550, resizable=False, vsync=True)
    dpg.bind_theme(global_theme)
    dpg.bind_font("text_font")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)

    dpg.start_dearpygui()
    dpg.destroy_context()

    if start_requested:
        start_tracker()
