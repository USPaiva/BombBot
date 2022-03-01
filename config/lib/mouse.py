import time
import pyautogui
from random import *
import config.lib.imagens as im

def randomize(loc: float, width: float, safe_factor=0):
    """randomize a number between loc and width with a safe distance (safe_factor*width).

    Returns
    -------
    float
        random float
    """
    if safe_factor > 0.5:
        raise ValueError("safe_factor must be between 0 and 0.5")

    safe_dist = width * safe_factor
    min_value = loc + safe_dist
    max_value = loc + width - safe_dist
    
    return uniform(min_value, max_value)

def randomize_int(loc: float, width: float, safe_factor=0):
    """randomize a number between loc and width with a safe distance (safe_factor*width).

    Returns
    -------
    int
        random integer
    """
    return round(randomize(loc, width, safe_factor))
    
def randomize_values(x, w, y, h):
    x_rand = randomize_int(x, w, 0.20)
    y_rand = randomize_int(y, h, 0.20)
    move_duration = randomize(0.1, 0.5)
    click_duration = randomize(0.05, 0.2)
    time_between = randomize(0.05, 0.3)

    return x_rand, y_rand, move_duration, click_duration, time_between


def click_randomly_in_position(x, y, w, h):
    x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
    pyautogui.moveTo(x, y)
    time.sleep(1)
    pyautogui.click()


def scroll_and_click_on_targets(safe_scroll_target: str, repeat: int, distance:float, duration: float, wait:float, function_between, execute_before=True):
    res = []
    if execute_before:
        res.append(function_between())

    for i in range(repeat):
        move_to(safe_scroll_target)
        pyautogui.mouseDown(duration=0.1)
        pyautogui.moveRel(0, distance, duration)
        #time.sleep(0.3)
        pyautogui.mouseUp(duration=0.1)
        #time.sleep()
        click_when_target_appears(safe_scroll_target)
        res.append(function_between())    
    
    return res

def click_when_target_appears(target: str, time_beteween: float = 0.5, timeout: float = 10):
    """ Click in a target when it appears.
        It will check for target every `time_beteween` seconds.
        After timeout seconds it will return 0 if no target was found.
        Returns 1 if target was found.
    """
    
    return do_with_timeout(click_one_target, args = [target])

def click_one_target(target: str):
    """click in a target. Returns number of clicks"""
    result = None
    try:
        x_left, y_top, w, h = im.get_one_target_position(target)
        x, y, move_duration, click_duration, time_between  = randomize_values(x_left, w, y_top, h)
        pyautogui.moveTo(x, y)
        time.sleep()
        pyautogui.click()
        result = True
    except Exception as e:
        return None
        # logger(f"Error: {e}")
    
    return result

def move_to(target:str):
    def move_to_logical():
        try:
            x, y, w, h = im.get_one_target_position(target)
            x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
            pyautogui.moveTo(x, y)
            return True
        except Exception as e:
            return None

    return do_with_timeout(move_to_logical)


def do_with_timeout(function, args = [], kwargs = {}, time_beteween: float = 0.5, timeout: float = 20):
    start_time = time.time()
    while True:
        if time.time() - start_time > timeout:
            return None
        
        result = function(*args, **kwargs)

        if result is not None:
            return result
        
        time.sleep(time_beteween)