from time import sleep
import easyocr
from PIL import ImageGrab
import numpy as np
import os
from datetime import datetime
import pyautogui
from pynput.mouse import Listener
import threading

''' 截图区域 '''
# 价格列表区域
price_list_region = (500, 245, 584, 700)
# 价格确认区域
price_confirm_region = (1220, 290, 1320, 490)

''' 坐标位置 '''
# 购买 的坐标位置
buy_position = (900, 805)
# 选择所有 的坐标位置
select_all_position = (1250, 310)
# 立即购买(确认购买) 的坐标位置
confirm_buy_position = (770, 540)
# 偏好 的坐标位置
preference_position = (460, 150)

# 后退 的坐标位置
back_position = (560, 230)
# 确认(该商品不存在) 的坐标位置
confirm_position = (800, 533)

''' 操作间隔 '''
click_interval = 0.01
interval = 0.1

''' 预设值 '''
# 定义预设值
preset_values = [500, 500, 100, 50, 100, 60, 400, 1000]

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
            # 休息 5s 倒计时
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
    def __init__(self, save_directory='pic', languages=None, preset_values=None):
        # 初始化 OCR 读者
        self.reader = easyocr.Reader(languages if languages else ['ch_sim', 'en'])
        # 设置保存截图的目录
        self.save_directory = save_directory
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        # 设置预设值
        self.preset_values = preset_values if preset_values else []
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def capture_screen(self, region=None):
        """ 截取屏幕区域并返回图像 """
        if region:
            screenshot = ImageGrab.grab(bbox=region)
        else:
            screenshot = ImageGrab.grab()
        return screenshot

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

    def process_price_list_region(self, region=None):
        while True:
            # 点击 偏好
            self.mouse_controller.perform_mouse_click(preference_position)
            # sleep(click_interval)
            self.mouse_controller.perform_mouse_click(preference_position)
            sleep(interval)
            # self.mouse_controller.perform_mouse_click(preference_position)
            # sleep(click_interval)

            """ 处理图像，执行 OCR 直到读出数字"""
            t = 0
            while True:
                image_price_list = self.capture_screen(region)
                text_result_price_list = self.read_text_from_image(image_price_list)

                # 过滤出结果中的数字
                numbers = [int(item[1]) for item in text_result_price_list if item[1].isdigit()]

                print("完整识别结果：", text_result_price_list)
                print("识别到的数字：", numbers)

                file_path = self.save_screenshot(image_price_list)
                print("截图保存路径：", file_path)
                if numbers or t > 3:
                    break
                else:
                    t = t + 1
            """ 处理完毕 """

            # 选择商品 的坐标位置
            x = 500
            y = 275
            offset = 40
            choose_positions = [(x, y + offset * i) for i in range(len(self.preset_values))]

            i = 0
            for number in numbers:
                if number < self.preset_values[i]:
                    print(f"数字 {number} 小于预设值 {self.preset_values[i]}，执行点击操作")
                    # 点击 选择商品
                    self.mouse_controller.perform_mouse_click(choose_positions[i])
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(choose_positions[i])
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(choose_positions[i])
                    # sleep(click_interval)

                    sleep(click_interval)
                    sleep(click_interval)
                    sleep(click_interval)
                    sleep(interval)

                    """ 进行价格确认 """
                    if self.process_price_confirm_region(price_confirm_region, self.preset_values[i]) is not True:
                        break

                    # 点击 选择所有 (可选 慎重选择)
                    self.mouse_controller.perform_mouse_click(select_all_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(select_all_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(select_all_position)
                    # sleep(click_interval)

                    # 点击 购买
                    self.mouse_controller.perform_mouse_click(buy_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(buy_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(buy_position)
                    # sleep(click_interval)

                    # 点击 立即购买
                    self.mouse_controller.perform_mouse_click(confirm_buy_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(confirm_buy_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(confirm_buy_position)
                    # sleep(click_interval)

                    # 点击 确认(该商品不存在)
                    self.mouse_controller.perform_mouse_click(confirm_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(confirm_position)
                    sleep(click_interval)

                    # 点击 偏好
                    self.mouse_controller.perform_mouse_click(preference_position)
                    # sleep(click_interval)
                    sleep(click_interval)
                    break  # 根据需求决定是否继续检查其他数字和预设值
                i = i + 1

            print("处理完成!!!!!!!!!!!!!!!!!!!!")

    def process_price_confirm_region(self, region=None, preset_value=None):
        """ 处理图像，执行 OCR """
        t = 0
        while True:
            image_price_confirm = self.capture_screen(region)
            text_result_price_confirm = self.read_text_from_image(image_price_confirm)

            # 过滤出结果中的数字
            numbers = [int(item[1]) for item in text_result_price_confirm if item[1].isdigit()]

            print("完整识别结果：", text_result_price_confirm)
            print("识别到的数字：", numbers)

            file_path = self.save_screenshot(image_price_confirm)
            print("截图保存路径：", file_path)

            if numbers or t > 3:
                break

            t = t + 1
        # if not numbers:
        #     print("未识别到数字，直接买了")
        #     return True

        for number in numbers:
            if number < preset_value:
                print(f"数字 {number} 小于预设值 {preset_value}，通过价格确认")
                return True
            else:
                print(f"数字 {number} 大于等于预设值 {preset_value}，未通过价格确认，取消购买")
                break

        return False


if __name__ == "__main__":

    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR(preset_values=preset_values)

    # 指定截取的屏幕区域
    ocr_processor.process_price_list_region(price_list_region)
