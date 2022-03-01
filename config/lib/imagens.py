from dataclasses import replace
from os import listdir
from turtle import width
import mss
import numpy as np
from cv2 import cv2
import pyautogui
import config.lib.contas as us
from random import *
from config.lib.utils import *

go_work_img = cv2.imread('./images/targets/go-work.png')
home_img = cv2.imread('./images/targets/home.png')
arrow_img = cv2.imread('./images/targets/go-back-arrow.png')
full_screen_img = cv2.imread('./images/targets/full_screen.png')
hero_img = cv2.imread('./images/targets/hero-icon.png')
x_button_img = cv2.imread('./images/targets/x.png')
teasureHunt_icon_img = cv2.imread('./images/targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('./images/targets/ok.png')
connect_wallet_btn_img = cv2.imread('./images/targets/connect-wallet.png')
sign_btn_img = cv2.imread('./images/targets/metamask_sign.png')
new_map_btn_img = cv2.imread('./images/targets/new-map.png')
green_bar = cv2.imread('./images/targets/green-bar.png')
full_stamina = cv2.imread('./images/targets/full-stamina.png')
character_indicator = cv2.imread('./images/targets/character_indicator.png')
error_img = cv2.imread('./images/targets/error.png')
metamask_unlock_img = cv2.imread('./images/targets/unlock_metamask.png')
metamask_cancel_button = cv2.imread('./images/targets/metamask_cancel_button.png')
puzzle_img = cv2.imread('./images/targets/puzzle.png')
piece = cv2.imread('./images/targets/piece.png')
robot = cv2.imread('./images/targets/robot.png')
slider = cv2.imread('./images/targets/slider.png')
chest_button = cv2.imread('./images/targets/treasure_chest.png')
coin_icon = cv2.imread('./images/targets/coin.png')
maintenance_popup = cv2.imread('./images/targets/maintenance.png')
chest1 = cv2.imread('./images/targets/chest1.png')
chest2 = cv2.imread('./images/targets/chest2.png')
chest3 = cv2.imread('./images/targets/chest3.png')
chest4 = cv2.imread('./images/targets/chest4.png')
####################################################################
allwork = cv2.imread('./images/targets/all_work.png')
allrest = cv2.imread('./images/targets/all_rest.png')
common = cv2.imread('./images/targets/common.png')
rest = cv2.imread('./images/targets/go-rest.png')
#########################################################
server_manu = cv2.imread('./images/targets/server_online.png')
bomb_guia = cv2.imread('./images/targets/bomb_guia.png')
select_guia = cv2.imread('./images/targets/select_guia.png')
menu_de_guias = cv2.imread('./images/targets/menu_de_guias.png')
new_win = cv2.imread('./images/targets/new_win.png')
#################################################################
new_connect = cv2.imread('./images/targets/new_connect.png')
user = cv2.imread('./images/targets/user.png')
pswd = cv2.imread('./images/targets/pass.png')
login = cv2.imread('./images/targets/login.png')
#################################################################
guia = cv2.imread('./images/targets/perfil_1_guia.png')
#################################################################
hero_search_area = cv2.imread('./images/targets/hero_search_area.png')

class img:           
    TARGETS = []
    MONITOR_LEFT = None
    MONITOR_TOP = None

    @staticmethod
    def load_targets():
        path = "images/targets/"
        file_names = listdir(path)
        targets = {}
        for file in file_names:
            targets[replace(file, ".png")] = cv2.imread(path + file)
        img.TARGETS = targets

    def screen():
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = np.array(sct.grab(monitor))
            img.MONITOR_LEFT = monitor["left"]
            img.MONITOR_TOP = monitor["top"]
            return sct_img[:, :, :3]
    
def get_monitor_with_target(target):
        position_bomb = get_one_target_position(target, 0)
        with mss.mss() as sct:
            monitors = sct.monitors
        
        for monitor in monitors:
            if len(monitors) == 1:
                return monitor.values()
            if position_inside_position(position_bomb, monitor.values()):
                return monitor.values()

        return monitors[0]
    
def get_compare_result(img1, img2):
        return cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    
def position_inside_position(position_in, position_out):
        x_in,y_in,w_in,h_in = position_in
        x_out,y_out,w_out,h_out = position_out

        start_inside_x = x_out <= x_in <= (x_out+w_out)
        finish_inside_x = x_out <= x_in + w_in <= (x_out + w_out)
        start_inside_y = y_out <= y_in <= (y_out+h_out)
        finish_inside_y = y_out <= y_in + h_in <= (y_out + h_out)
        
        return start_inside_x and finish_inside_x and start_inside_y and finish_inside_y


def print_full_screen(image_name: str, target):
        image_name = f'{image_name}.png'
        monitor_screen = get_monitor_with_target(target)
        image = pyautogui.screenshot(region=(monitor_screen))
        image.save(image_name)
        return image_name
        
def print_partial_screen(image_name: str, target: str):
        image_name = f'{image_name}.png'
        x,y,w,h = get_one_target_position(target, 0)
        image = pyautogui.screenshot(region=(x,y,w,h))
        image.save(image_name)
        return image_name

def get_target_positions(target:str, screen_image = None, threshold:float=0.8, not_target:str=None):
        threshold_config = us.configThreshold["go_to_work_btn"]
        if(threshold_config):
            threshold = threshold_config    
        target_img = img.TARGETS[target]
        #print(target_img)
        
        screen_img = img.screen() if screen_image is None else screen_image
        result = cv2.matchTemplate(screen_img, target_img, cv2.TM_CCOEFF_NORMED)

        if not_target is not None:
            not_target_img = img.TARGETS[not_target]
            not_target_result = cv2.matchTemplate(screen_img, not_target_img, cv2.TM_CCOEFF_NORMED)
            result[result < not_target_result] = 0

        y_result, x_result = np.where( result >= threshold)
        
        
        height, width = target_img.shape[:2]
        targets_positions = []
        for (x,y) in zip(x_result, y_result):
            x += img.MONITOR_LEFT
            y += img.MONITOR_TOP
            targets_positions.append([x,y,width,height])
            
        return targets_positions

#get_target_positions("button_work_unchecked", not_target="button_work_checked", screen_image=screen())
def get_one_target_position(target:str, threshold:float=0.8):
        threshold_config = us.configThreshold['default']
        if(threshold_config):
            threshold = threshold_config
            
        target_img = img.TARGETS[target]
        screen_img = img.screen()
        result = cv2.matchTemplate(screen_img, target_img, cv2.TM_CCOEFF_NORMED)

        if result.max() < threshold:
            raise Exception(f"{target} not found")
            
        yloc, xloc = np.where(result == result.max())
        xloc += img.MONITOR_LEFT
        yloc += img.MONITOR_TOP
        height, width = target_img.shape[:2]
        
        return xloc[0], yloc[0], width, height

def get_max_result_between(TARGETS:list, y_limits=None, x_limits=None, threshold:float=0):
        index = 0
        max_result = 0
        for i, target in enumerate(img.targets):
            sscreen = img.screen()
            if y_limits is not None:
                sscreen= sscreen[y_limits[0]:y_limits[1], :]
            if x_limits is not None:
                x,w = x_limits
                sscreen= sscreen[:, x:x+w]
            result = cv2.matchTemplate(sscreen, img.TARGETS[target], cv2.TM_CCOEFF_NORMED)
            if result.max() > max_result:
                max_result = result.max()
                index = i
        
        return index


def filter_by_green_bar(item):
        x,y,w,h = item
        y_increment = round(h*0.1)
        screen_img = img.screen()[y:y+h+y_increment,:]
        result = get_target_positions("hero_bar_green", screen_image=screen_img)
        return len(result) > 0

def get_one_target_position(target:str, threshold:float=0.8):
        threshold_config = us.configThreshold['default']['default']
        if(threshold_config):
            threshold = threshold_config
            
        target_img = img.TARGETS[target]
        screen_img = img.screen()
        result = cv2.matchTemplate(screen_img, target_img, cv2.TM_CCOEFF_NORMED)

        if result.max() < threshold:
            raise Exception(f"{target} not found")
            
        yloc, xloc = np.where(result == result.max())
        xloc += img.MONITOR_LEFT
        yloc += img.MONITOR_TOP
        height, width = target_img.shape[:2]
        
        return xloc[0], yloc[0], width, height