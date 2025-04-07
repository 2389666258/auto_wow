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

''' --- 截图区域 --- '''
# 背包剩余值截图区域
bag_value_region = (2485, 1270, 2515, 1290)

''' 坐标位置 '''
# 分解 的坐标位置
resolve_position = (1840, 1195)
# 制造 的坐标位置
produce_position = (1860, 1295)
# 聊天栏 的坐标位置
chat_position = (124, 1340)
# 裁缝 的坐标位置
tailor_position = (795, 320)


''' 操作间隔 '''
# 普通间隔
interval = 0.04
# 等待时间
wait_time = 1

''' --- 预设值 --- '''
# 预设背包剩余值
preset_bag_value = 30

''' --- 开关 --- '''
# 截图保存开关
save_screenshot_switch = False


class MouseController:
    def __init__(self):
        self.mouse_moving = False
        self.start_mouse_listener()

    def perform_mouse_click(self, position):
        """ 在指定位置执行鼠标点击 """
        if not self.mouse_moving:
            pyautogui.moveTo(position)
            pyautogui.click()
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
    def __init__(self, save_directory='pic', languages=None):
        # 初始化 OCR 读者
        self.reader = easyocr.Reader(languages if languages else ['ch_sim', 'en'])
        # 设置保存截图的目录
        self.save_directory = save_directory
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        # 设置预设值
        self.preset_bag_value = preset_bag_value
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def capture_screen(self, region=None):
        """ 截取屏幕区域并返回图像 """
        if region:
            screenshot = ImageGrab.grab(bbox=region)
        else:
            screenshot = ImageGrab.grab()

        # 对截图进行二值化处理
        screenshot = self.preprocess_image(screenshot)

        return screenshot

    def preprocess_image(self, image):
        """ 对图像进行二值化处理 """
        # 将 PIL 图像转换为灰度图
        gray_image = ImageOps.grayscale(image)

        # 将灰度图转换为 NumPy 数组
        image_np = np.array(gray_image)

        # 应用 OpenCV 的 Otsu 二值化
        _, binary_np = cv2.threshold(image_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 将二值化的 NumPy 数组转换回 PIL 图像
        binary_image = Image.fromarray(binary_np)

        return binary_image

    def save_screenshot(self, image):
        """ 保存截图到指定路径并返回文件路径 """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.save_directory, f'screenshot_{timestamp}.png')
        image.save(file_path)
        return file_path

    def read_text_from_image(self, image):
        """ 读取图像中的文字 """
        # 将 PIL 图像对象转换为 NumPy 数组
        image_np = np.array(image)
        result = self.reader.readtext(image_np)
        return result

    def press_product_and_resolve(self):

        # self.refresh_and_reopen_produce_page()

        flag = True
        bag_value_same_value_count = 0
        bag_previous_value = 0

        while True:
            # 点击制造
            self.mouse_controller.perform_mouse_click(produce_position)
            pyautogui.click()

            # 等待制造时间
            # sleep(1.5) # 稳妥
            sleep(1.5)

            # # 点击分解
            # self.mouse_controller.perform_mouse_click(resolve_position)
            # pyautogui.click()

            pyautogui.moveTo(resolve_position)
            # 按下 数字7 键
            pyautogui.press('7')
            pyautogui.press('7')

            # 等待分解时间
            # sleep(1.4) # 稳妥777
            sleep(1.4)


    # 刷新页面并重新打开制造页面
    def refresh_and_reopen_produce_page(self):
        # 点击聊天栏
        pyautogui.moveTo(chat_position)
        sleep(wait_time)
        self.mouse_controller.perform_mouse_click(chat_position)
        sleep(wait_time)
        self.mouse_controller.perform_mouse_click(chat_position)

        # 输入 “/reload” 命令
        pyautogui.write("/reload")
        sleep(wait_time)

        # 按下 回车键
        pyautogui.press('enter')
        sleep(wait_time)
        pyautogui.press('enter')

        # 等待重启完成
        sleep(15)

        # 按下 k键 打开制造页面
        pyautogui.press('k')
        sleep(wait_time)

        # 点击 裁缝
        pyautogui.moveTo(tailor_position)
        sleep(wait_time)
        self.mouse_controller.perform_mouse_click(tailor_position)
        sleep(wait_time)
        self.mouse_controller.perform_mouse_click(tailor_position)
        sleep(wait_time)

    # 截图OCR识别
    def capture_screen_and_ocr(self, region):
        image = self.capture_screen(region)
        result_text = self.read_text_from_image(image)

        # 过滤出结果中的数字
        numbers = [int(item[1]) for item in result_text if item[1].isdigit()]

        print("完整识别结果：", result_text)
        print("识别到的数字：", numbers)

        if save_screenshot_switch:
            file_path = self.save_screenshot(image)
            print("截图保存路径：", file_path)

        return numbers


if __name__ == "__main__":
    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR()

    # 指定截取的屏幕区域
    ocr_processor.press_product_and_resolve()
