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

''' 截图区域 '''
# 价格列表区域
# price_list_region = (500, 245, 584, 700)
# price_list_region = (500, 245, 582, 455)
# price_list_region = (500, 245, 582, 290)

# 金
price_list_region = (530, 250, 582, 290)
# 金 & 银
# price_list_region = (530, 250, 665, 290)

# 价格确认区域
# price_confirm_region = (1220, 285, 1305, 610)
# price_confirm_region = (1220, 285, 1305, 490)

# 金
# price_confirm_region = (1220, 285, 1305, 325)
# 金 & 银
price_confirm_region = (1220, 285, 1420, 325)

''' 坐标位置 '''
# 选择商品 的坐标位置
choose_position = (500, 275)

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

# 退出拍卖行 的坐标位置
exit_position = (1700, 70)
# 进入拍卖行 的坐标位置 (屏幕中心)
screen_width, screen_height = pyautogui.size()
enter_position = (screen_width // 2, screen_height // 2)


''' 操作间隔 '''
click_interval = 0.15
interval = 0.1

''' 预设值 '''
# 定义预设值
preset_value = 35

''' 开关 '''
# 截图保存开关
save_screenshot_switch = True

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
    def __init__(self, save_directory='pic', languages=None, preset_value=None):
        # 初始化 OCR 读者
        self.reader = easyocr.Reader(languages if languages else ['ch_sim', 'en'])
        # 设置保存截图的目录
        self.save_directory = save_directory
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        # 设置预设值
        self.preset_value = preset_value
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def capture_screen(self, region=None):
        """ 截取屏幕区域并返回图像 """
        if region:
            screenshot = ImageGrab.grab(bbox=region)
        else:
            screenshot = ImageGrab.grab()

        # 对截图进行二值化处理
        binary_image = self.preprocess_image(screenshot)
        return binary_image

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

    def process_price_list_region(self, region=None):
        # 错误次数
        error_count = 0
        while True:
            # 点击 偏好
            self.mouse_controller.perform_mouse_click(preference_position)
            # sleep(click_interval)
            # sleep(click_interval)
            # sleep(click_interval)
            sleep(interval)
            sleep(interval)
            sleep(interval)

            # self.mouse_controller.perform_mouse_click(preference_position)
            # sleep(click_interval)

            """ 处理图像，执行 OCR 直到读出数字"""
            image_price_list = self.capture_screen(region)
            text_result_price_list = self.read_text_from_image(image_price_list)

            # 过滤出结果中的数字
            numbers = [int(item[1]) for item in text_result_price_list if item[1].isdigit()]

            print("完整识别结果：", text_result_price_list)
            print("识别到的数字：", numbers)

            if save_screenshot_switch:
                file_path = self.save_screenshot(image_price_list)
                print("截图保存路径：", file_path)
            """ 处理完毕 """

            # 如果没有识别到数字 错误次数 +1
            if not numbers:
                error_count += 1
                print(f"未识别到数字，错误次数：{error_count}")
                if error_count >= 10:
                    print("连续错误达到10次，重启拍卖行")
                    # 点击 退出拍卖行
                    self.mouse_controller.perform_mouse_click(exit_position)
                    sleep(interval * 100)

                    # 点击 进入拍卖行
                    self.mouse_controller.perform_mouse_click(enter_position)
                    sleep(interval * 100)

                    # 重置错误次数
                    error_count = 0

                    continue

            while numbers:
                # 正确识别 错误次数清零
                error_count = 0
                # number = 第一个数字
                number = numbers[0]
                if number < self.preset_value:
                    print(f"数字 {number} 小于预设值 {self.preset_value}，执行点击操作")
                    # 点击 选择商品
                    self.mouse_controller.perform_mouse_click(choose_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(choose_position)
                    # sleep(click_interval)
                    self.mouse_controller.perform_mouse_click(choose_position)
                    # sleep(click_interval)

                    # sleep(click_interval)
                    # sleep(click_interval)
                    # sleep(click_interval)
                    # sleep(click_interval)
                    # sleep(click_interval)
                    sleep(interval)
                    sleep(interval)
                    sleep(interval)
                    sleep(interval)
                    sleep(interval)
                    sleep(interval)
                    sleep(interval)

                    # 点击 确认(该商品不存在)
                    self.mouse_controller.perform_mouse_click(confirm_position)

                    """ 进行价格确认 """
                    if self.process_price_confirm_region(price_confirm_region) is not True:
                        break

                    ''' 为了能点击 购买 按钮 '''
                    # 点击 确认(该商品不存在)
                    self.mouse_controller.perform_mouse_click(confirm_position)

                    # 点击 选择所有 (可选 慎重选择)
                    self.mouse_controller.perform_mouse_click(select_all_position)
                    # sleep(click_interval)
                    # self.mouse_controller.perform_mouse_click(select_all_position)
                    # # sleep(click_interval)

                    # 点击 购买
                    self.mouse_controller.perform_mouse_click(buy_position)
                    # sleep(click_interval)
                    # self.mouse_controller.perform_mouse_click(buy_position)
                    # # sleep(click_interval)

                    # 点击 立即购买
                    self.mouse_controller.perform_mouse_click(confirm_buy_position)
                    # sleep(click_interval)
                    # self.mouse_controller.perform_mouse_click(confirm_buy_position)
                    # # sleep(click_interval)

                    # 点击 确认(该商品不存在)
                    self.mouse_controller.perform_mouse_click(confirm_position)
                    sleep(interval)
                    self.mouse_controller.perform_mouse_click(confirm_position)
                    sleep(click_interval)

                    sleep(interval)
                    sleep(interval)
                    # 点击 偏好
                    self.mouse_controller.perform_mouse_click(preference_position)
                    sleep(click_interval)

                    print("购买已执行完成")

                break


    def process_price_confirm_region(self, region=None):
        """ 处理图像，执行 OCR """
        image_price_confirm = self.capture_screen(region)
        text_result_price_confirm = self.read_text_from_image(image_price_confirm)

        # 过滤出结果中的数字
        numbers = [int(item[1]) for item in text_result_price_confirm if item[1].isdigit()]

        print("完整识别结果：", text_result_price_confirm)
        print("识别到的数字：", numbers)

        if save_screenshot_switch:
            file_path = self.save_screenshot(image_price_confirm)
            print("截图保存路径：", file_path)

        # if preset_value == 62 and len(numbers) == 4:
        #     print(f"应该是识别不了9，买吧")
        #     return True

        for number in numbers:
            if number < preset_value:
                print(f"数字 {number} 小于预设值 {preset_value}，通过价格确认")
                return True
            else:
                print(f"数字 {number} 大于等于预设值 {preset_value}，未通过价格确认，取消购买")
                break

        print("未识别到数字")
        return False


if __name__ == "__main__":

    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR(preset_value=preset_value)

    # 指定截取的屏幕区域
    ocr_processor.process_price_list_region(price_list_region)
