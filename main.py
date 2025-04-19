from HandTracker import HandTracker

# ==== Ejecutar el tracker ====
if __name__ == '__main__':
    model_path = 'hand_landmarker.task'
    tracker = HandTracker(model_path)
    tracker.run()