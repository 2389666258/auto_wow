from time import sleep
import easyocr
from PIL import ImageGrab, ImageOps, Image
import numpy as np
import os
from datetime import datetime
import pyautogui
from pynput.mouse import Listener
import threading

import cv2

""" 图形UI缩放调整为109% 以下所有定位与1.*版本不一致！(1.*版本为115%) """

''' 坐标位置 '''
# 分解 的坐标位置
resolve_position = (200, 300)

''' 操作间隔 '''
interval = 1.05

class MouseController:
    def __init__(self):
        self.mouse_moving = False
        self.start_mouse_listener()

    def perform_mouse_click(self, position):
        """ 在指定位置执行鼠标点击 """
        if not self.mouse_moving:
            pyautogui.click(position)
            print(f"鼠标点击操作完成，点击位置：{position}")
        else:
            print("鼠标正在移动，禁止点击操作")
            # 休息 5s 倒计时cccdc
            for i in range(5, 0, -1):
                print(f"检测到鼠标移动，{i} 秒后重试")
                sleep(1)

    def on_move(self, x, y):
        self.mouse_moving = True
        if hasattr(self, 'mouse_timer'):
            self.mouse_timer.cancel()
        self.mouse_timer = threading.Timer(0.5, self.reset_mouse_movement)
        self.mouse_timer.start()

    def reset_mouse_movement(self):
        self.mouse_moving = False

    def start_mouse_listener(self):
        self.listener = Listener(on_move=self.on_move)
        self.listener.start()


class ScreenCaptureOCR:
    def __init__(self):

        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def press_resolve(self, region=None):
        while True:
            # 点击分解按钮
            self.mouse_controller.perform_mouse_click(resolve_position)
            sleep(interval)


if __name__ == "__main__":

    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR()

    # 指定截取的屏幕区域
    ocr_processor.press_resolve()
