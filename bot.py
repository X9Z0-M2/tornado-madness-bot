import threading
import pyautogui
import keyboard
from PIL import Image
from ultralytics import YOLO
from ultralytics.utils.files import increment_path
from screeninfo import get_monitors
from pathlib import Path

import time

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

def get_screen_size():
    monitors = get_monitors()
    screen_width = monitors[0].width
    screen_height = monitors[0].height
    return screen_width, screen_height

def get_screen_center():
    screen_width, screen_height = get_screen_size()
    return screen_width / 2, screen_height / 2

def get_screen_distance(x, y):
    return abs((x - screenx_center) ** 2 - (y - screeny_center) ** 2) **.5

def analyze_screen(stop_event, model, start_botaction, stop_botaction):
    pyautogui.FAILSAFE = False
    region = ( screenx_left, screeny_top, screenx_size, screeny_size )
    decision = {
        "play_count": 0,
    }
    # try:
    #     rmdir(Path("runs/detect/predict"))
    # except FileNotFoundError:
    #     pass
    # except PermissionError:
    #     pass

    while not stop_event.is_set():
        decision = {
            "loading": False,
            "close_ad": False,
            "buy": False,
            "play": False,
            "play_count": decision["play_count"],
            "next": False,
            "continue": False,
            "berserk": False,
            "refuel": False,
            "gas": False,
            "tornado": False,
            "shrub": False,
            "tree": False,
            "tall_tree": False,
            "build": False,
            "house": False,
            "donut_shop": False,
        }

        screenshot = pyautogui.screenshot(region=region)
        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())

        
        predicts_dir = 'runs\\bot\\predict'
        VAL_DIR = increment_path(predicts_dir, exist_ok=True)
        #results = model([screenshot], conf=0.35, line_width=1, save=True, save_dir=VAL_DIR) # iterate over a low confidence score so classes with lower detection can be checked
        results = model([screenshot], conf=0.50) # iterate over a low confidence score so classes with lower detection can be checked
        #results = model([screenshot], conf=0.50, show=True) # iterate over a low confidence score so classes with lower detection can be checked
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        for bb, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = bb
            center_x = (x1 + x2) / 2 + screenx_left
            center_y = (y1 + y2) / 2 + screeny_top

            name = names[int(cls)]

            if name == "loading" and conf > 0.7:
                decision["loading"] = True
                decision["loading_loc"] = (center_x, center_y)
            elif name == "close_ad" and conf > 0.7:
                decision["close_ad"] = True
                decision["close_ad_loc"] = (center_x, center_y)
            elif name == "buy" and conf > 0.50:
                decision["buy"] = True
                decision["buy_loc"] = (center_x, center_y)
            elif name == "play" and conf > 0.7:
                decision["play"] = True
                decision["play_count"] = decision["play_count"] + 1
                decision["play_loc"] = (center_x, center_y)
            elif name == "next" and conf > 0.7:
                decision["next"] = True
                decision["next_loc"] = (center_x, center_y)
            elif name == "continue" and conf > 0.7:
                decision["continue"] = True
                decision["continue_loc"] = (center_x, center_y)
            elif name == "berserk" and conf > 0.7:
                decision["berserk"] = True
                decision["berserk_loc"] = (center_x, center_y)
            elif name == "gas" and conf > 0.7:
                decision["gas"] = True
                distance = get_screen_distance(center_x, center_y)
                if "gas_loc" in decision:
                    if distance < decision["gas_dist"]:
                        decision["gas_loc"] = (center_x, center_y)
                        decision["gas_dist"] = distance
                else:
                    decision["gas_loc"] = (center_x, center_y)
                    decision["gas_dist"] = distance
            elif name == "refuel" and conf > 0.7:
                decision["refuel"] = True
                decision["refuel_loc"] = (center_x, center_y)
            elif name == "tornado" and conf > 0.7:
                decision["tornado"] = True
                decision["tornado_loc"] = (center_x, center_y)
            elif name == "shrub" and conf > 0.7:
                decision["shrub"] = True
                distance = get_screen_distance(center_x, center_y)
                if "shrub_loc" in decision:
                    if distance < decision["shrub_dist"]:
                        decision["shrub_loc"] = (center_x, center_y)
                        decision["shrub_dist"] = distance
                else:
                    decision["shrub_loc"] = (center_x, center_y)
                    decision["shrub_dist"] = distance
            elif name == "tree" and conf > 0.83:
                decision["shrub"] = True
                distance = get_screen_distance(center_x, center_y)
                if "shrub_loc" in decision:
                    if distance < decision["shrub_dist"]:
                        decision["shrub_loc"] = (center_x, center_y)
                        decision["shrub_dist"] = distance
                else:
                    decision["shrub_loc"] = (center_x, center_y)
                    decision["shrub_dist"] = distance
                # decision["tree"] = True
                # distance = get_screen_distance(center_x, center_y)
                # if "tree_loc" in decision:
                #     if distance < decision["tree_dist"]:
                #         decision["tree_loc"] = (center_x, center_y)
                #         decision["tree_dist"] = distance
                # else:
                #     decision["tree_loc"] = (center_x, center_y)
                #     decision["tree_dist"] = distance
            elif name == "tall_tree" and conf > 0.92:
                decision["shrub"] = True
                distance = get_screen_distance(center_x, center_y)
                if "shrub_loc" in decision:
                    if distance < decision["shrub_dist"]:
                        decision["shrub_loc"] = (center_x, center_y)
                        decision["shrub_dist"] = distance
                else:
                    decision["shrub_loc"] = (center_x, center_y)
                    decision["shrub_dist"] = distance
                # decision["tall_tree"] = True
                # distance = get_screen_distance(center_x, center_y)
                # if "tall_tree_loc" in decision:
                #     if distance < decision["tall_tree_dist"]:
                #         decision["tall_tree_loc"] = (center_x, center_y)
                #         decision["tall_tree_dist"] = distance
                # else:
                #     decision["tall_tree_loc"] = (center_x, center_y)
                #     decision["tall_tree_dist"] = distance
            elif name == "build" and conf > 0.7:
                decision["build"] = True
                distance = get_screen_distance(center_x, center_y)
                if "build_loc" in decision:
                    if distance < decision["build_dist"]:
                        decision["build_loc"] = (center_x, center_y)
                        decision["build_dist"] = distance
                else:
                    decision["build_loc"] = (center_x, center_y)
                    decision["build_dist"] = distance
            elif name == "house" and conf > 0.83:
                decision["build"] = True
                distance = get_screen_distance(center_x, center_y)
                if "build_loc" in decision:
                    if distance < decision["build_dist"]:
                        decision["build_loc"] = (center_x, center_y)
                        decision["build_dist"] = distance
                else:
                    decision["build_loc"] = (center_x, center_y)
                    decision["build_dist"] = distance
                # decision["house"] = True
                # distance = get_screen_distance(center_x, center_y)
                # if "house_loc" in decision:
                #     if distance < decision["house_dist"]:
                #         decision["house_loc"] = (center_x, center_y)
                #         decision["house_dist"] = distance
                # else:
                #     decision["house_loc"] = (center_x, center_y)
                #     decision["house_dist"] = distance
            elif name == "donut_shop" and conf > 0.92:
                decision["build"] = True
                distance = get_screen_distance(center_x, center_y)
                if "build_loc" in decision:
                    if distance < decision["build_dist"]:
                        decision["build_loc"] = (center_x, center_y)
                        decision["build_dist"] = distance
                else:
                    decision["build_loc"] = (center_x, center_y)
                    decision["build_dist"] = distance
                # decision["donut_shop"] = True
                # distance = get_screen_distance(center_x, center_y)
                # if "donut_shop_loc" in decision:
                #     if distance < decision["donut_shop_dist"]:
                #         decision["donut_shop_loc"] = (center_x, center_y)
                #         decision["donut_shop_dist"] = distance
                # else:
                #     decision["donut_shop_loc"] = (center_x, center_y)
                #     decision["donut_shop_dist"] = distance

                if not decision["play"]:
                    decision["play_count"] = 0
                else:
                    decision["play_count"] = decision["play_count"] + 1

        #print(decision)
        if start_botaction.is_set():
            run_bot(decision)
        # time.sleep(0.3)

def run_bot(decision):
    distance_target = 9999999

    if "buy_loc" in decision:
        pyautogui.click(decision["buy_loc"])
    elif "play_loc" in decision and decision["play_count"] > 7:
        pyautogui.click(decision["play_loc"])
    elif "continue_loc" in decision:
        pyautogui.click(decision["continue_loc"])
    elif "next_loc" in decision:
        pyautogui.click(decision["next_loc"])
    elif "loading_loc" in decision:
        return
    elif "close_ad_loc" in decision:
        pyautogui.click(decision["close_ad_loc"])
    elif "refuel_loc" in decision:
        return
    elif "gas_loc" in decision and decision["gas_dist"] < 700:
        pyautogui.moveTo(decision["gas_loc"])
    else:
        if decision["shrub"] and decision["build"]:
            if decision["shrub_dist"] + 170 < decision["build_dist"]:
                pyautogui.moveTo(decision["shrub_loc"])
                distance_target = decision["shrub_dist"]
            else:
                pyautogui.moveTo(decision["build_loc"])
                distance_target = decision["build_dist"]
        elif decision["shrub"]:
            pyautogui.moveTo(decision["shrub_loc"])
            distance_target = decision["shrub_dist"]
        elif decision["build"]:
            pyautogui.moveTo(decision["build_loc"])
            distance_target = decision["build_dist"]

    if distance_target < 10:
        pyautogui.press('1')
        pyautogui.press('2')


        

# use these centers if analyzing the entire screen
# screenx_center, screeny_center = get_screen_center()

# manually defined region on screen
screenx_left = 415    # left to right, 0 being furthest left 
screeny_top = 276    # top to bottom, 0 being highest
screenx_right = 1520   # bottom right's
screeny_bottom = 854    # right bottom's
screenx_center = (screenx_left + screenx_right) / 2
screeny_center = (screeny_top + screeny_bottom) / 2
screenx_size = abs(screenx_left - screenx_right)
screeny_size = abs(screeny_top - screeny_bottom)


def main():
    model = YOLO('./weights/best-yolov8-mAP-92.7 copy.pt')
    stop_event = threading.Event()
    stop_botaction = threading.Event()
    start_botaction = threading.Event()

    screenshot_thread = threading.Thread(target=analyze_screen, args=(stop_event, model, start_botaction, stop_botaction))
    screenshot_thread.start()

    # print(KeyboardEvent.name, KeyboardEvent.scan_code, KeyboardEvent.time)
    def keyboard_quit_cb(KeyboardEvent):
        nonlocal stop_event
        nonlocal quit
        quit = True
        stop_event.set()
    def keyboard_startbotaction_cb(KeyboardEvent):
        nonlocal stop_botaction
        nonlocal start_botaction
        stop_botaction.clear()
        start_botaction.set()
    def keyboard_stopbotaction_cb(KeyboardEvent):
        nonlocal stop_botaction
        nonlocal start_botaction
        stop_botaction.set()
        start_botaction.clear()

    quit = False
    keyboard.on_press_key("q",keyboard_quit_cb )
    keyboard.on_press_key("s",keyboard_startbotaction_cb )
    keyboard.on_press_key("w",keyboard_stopbotaction_cb )
    while not quit:
        # Wait for the next event.
        event = keyboard.read_event()

    screenshot_thread.join()

    print("Ended.")


if __name__ == "__main__":
    main()

