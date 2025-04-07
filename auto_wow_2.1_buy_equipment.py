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

''' --- 多屏幕偏移量 --- '''
# 坐标偏移量
x_offset = 0

''' --- 截图区域 --- '''
# 价格列表区域
# 金
# price_list_region = (500, 272, 548, 305)
# 金 (两位数)
# price_list_region = (515, 272, 548, 305)
# 金 & 银
# price_list_region = (530, 250, 665, 290)
# 金 & 金
# price_list_region = (530, 250, 582, 330)
# 金 & 金 & 金
price_list_region = (490 + x_offset, 280, 544 + x_offset, 391)
# 金 & 金 & 金 & 金
# price_list_region = (500, 272, 548, 425)

# 价格确认区域
# 金
price_confirm_region = (635 + x_offset, 540, 764 + x_offset, 576)
# 金 （小）
# price_confirm_region = (635, 540, 755, 576)
# 金 （小小）
# price_confirm_region = (635, 540, 735, 576)
# 金 （小小小）
# price_confirm_region = (635, 540, 708, 576)
# 金 & 金 & 金
# price_confirm_region = (560, 540, 708, 649)


''' --- 坐标位置 --- '''

# 选择商品 的坐标位置 （第一个）
choose_position = (1200 + x_offset, 300)
# 选择商品 的坐标位置 （第二个）
# choose_position = (1200, 335)
# 第二次 选择商品 的坐标位置
choose_position_2nd = (650 + x_offset, 555)


# 一口价 的坐标位置
buy_position = (1460 + x_offset, 1090)

# 一口价购买确认 的坐标位置（接受）
buy_confirm_position = (1060 + x_offset, 420)

# 搜索 的坐标位置
search_position = (1420 + x_offset, 180)

# 鼠标休息区域
mouse_rest_position = (700 + x_offset, 1100)

# 退出拍卖行 的坐标位置
exit_position = (1610 + x_offset, 100)
# 进入拍卖行 的坐标位置 (屏幕中心)
screen_width, screen_height = pyautogui.size()
enter_position = (screen_width // 2, screen_height // 2)


# '武器' 的坐标位置
weapon_position = (230 + x_offset, 255)
# '护甲' 的坐标位置 (已经选中'武器'时的坐标位置)
armor_position = (230 + x_offset, 460)
# '专业装备' 的坐标位置 (已经选中'护甲'时的坐标位置)
professional_equipment_position = (230 + x_offset, 865)
# '武器' '护甲' '专业装备' 的坐标位置的集合
equipment_positions = [weapon_position, armor_position, professional_equipment_position]

# 已经选中 '专业装备' 时 '专业装备' 的坐标位置
professional_equipment_cancel_position = (230 + x_offset, 355)

''' --- 操作间隔 --- '''
# 普通间隔
interval = 0.2
# 卡顿添加间隔
add_interval = 0.1

''' --- 预设值 --- '''
# 价值预设值 (小于该值时执行购买操作)
preset_value = 191
# 选择第几个商品 （0是第一个）
preset_item_number = 0
# 选择 '武器' '护甲' '专业装备' 的坐标位置的集合 的索引 （0是武器 1是护甲 2是专业装备）
preset_equipment_number = 0

''' --- 开关 --- '''
# 截图保存开关
save_screenshot_switch = True

''' --- 阈值 --- '''
# 识别错误阈值
error_threshold = 5
# 价格大于预设值阈值
price_greater_than_preset_value_threshold = 3


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
        self.preset_item_number = preset_item_number
        self.preset_equipment_number = preset_equipment_number
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

    def process_price_list_region(self):
        """ 处理价格列表区域 """
        # 价格连续大于预设值的次数
        price_greater_than_preset_value_count = 0
        while True:
            # 点击 搜索
            sleep(add_interval)
            sleep(add_interval)

            pyautogui.moveTo(search_position)
            self.mouse_controller.perform_mouse_click(search_position)

            # 扫描价格列表区域的次数
            price_list_region_scan_count = 0
            while True:
                print("正在检测价格列表区域...")
                image_price = self.capture_screen(price_list_region)
                text_result_price_confirm = self.read_text_from_image(image_price)

                # 过滤出结果中的数字
                prices = [int(item[1]) for item in text_result_price_confirm if item[1].isdigit()]

                print("完整识别结果：", text_result_price_confirm)
                print("识别到的数字：", prices)

                if save_screenshot_switch:
                    file_path = self.save_screenshot(image_price)
                    print("截图保存路径：", file_path)

                if prices and len(prices) == 3:
                    price = prices[self.preset_item_number]
                    if price < self.preset_value:
                        print(f"价格区域识别到数字 {price} 小于预设值 {self.preset_value}，执行购买操作，进入价格确认区域")
                        # 点击 选择商品
                        pyautogui.moveTo(choose_position)
                        self.mouse_controller.perform_mouse_click(choose_position)

                        # 鼠标移动到休息区域
                        pyautogui.moveTo(mouse_rest_position)

                        # 处理价格确认区域
                        self.process_price_confirm_region(price_confirm_region, price)
                        price_greater_than_preset_value_count = 0

                        # 点击 搜索
                        pyautogui.moveTo(search_position)
                        self.mouse_controller.perform_mouse_click(search_position)
                        sleep(interval)
                        break
                    else:
                        print(f"确认价格区域识别到数字 {price} 大于等于预设值 {self.preset_value}，取消购买！")
                        price_greater_than_preset_value_count = price_greater_than_preset_value_count + 1
                        if price_greater_than_preset_value_count >= price_greater_than_preset_value_threshold:
                            print(f"连续 {price_greater_than_preset_value_threshold} 次价格大于等于预设值 {self.preset_value}，更换购买商品类目！")
                            # 选择 '武器' '护甲' '专业装备' 的坐标位置的集合 中的下一个
                            self.preset_equipment_number = (self.preset_equipment_number + 1) % len(equipment_positions)

                            # 如果需要选择 '武器' 则先取消 '专业装备'
                            if self.preset_equipment_number == 0:
                                # 点击 取消 '专业装备'
                                pyautogui.moveTo(professional_equipment_cancel_position)
                                sleep(interval)
                                sleep(interval)
                                sleep(interval)
                                self.mouse_controller.perform_mouse_click(professional_equipment_cancel_position)
                                sleep(interval)
                                sleep(interval)
                                sleep(interval)

                            # 点击 下一个商品类目
                            pyautogui.moveTo(equipment_positions[self.preset_equipment_number])
                            sleep(interval)
                            sleep(interval)
                            sleep(interval)
                            self.mouse_controller.perform_mouse_click(equipment_positions[self.preset_equipment_number])

                            price_greater_than_preset_value_count = 0
                        break
                else:
                    print("确认价格区域未识别到数字，继续检测...")
                    price_list_region_scan_count = price_list_region_scan_count + 1
                    if price_list_region_scan_count >= error_threshold:
                        print(f"扫描次数达到阈值 {error_threshold}，重新扫描价格列表区域！")
                        break



    def process_price_confirm_region(self, region=None, price_before_confirmation=None):
        """ 处理价格确认区域 """
        error_count = 0
        while True:
            image_price_confirm = self.capture_screen(region)
            text_result_price_confirm = self.read_text_from_image(image_price_confirm)

            # 过滤出结果中的数字
            prices = [int(item[1]) for item in text_result_price_confirm if item[1].isdigit()]

            print("完整识别结果：", text_result_price_confirm)
            print("识别到的数字：", prices)

            if save_screenshot_switch:
                file_path = self.save_screenshot(image_price_confirm)
                print("截图保存路径：", file_path)

            # 金 & 金 & 金

            # if numbers and len(numbers) == 3:
            #     number = numbers[0]
            #     if number < self.preset_value:
            #         print(f"确认价格确认区域识别到数字 {number} 依然小于预设值 {self.preset_value}，执行购买操作")
            #         self.execute_purchase()
            #         return 1
            #     else:
            #         print(f"确认价格确认区域识别到数字 {number} 大于等于预设值 {self.preset_value}，取消购买！")
            #         return 0
            # else:
            #     error_count = error_count + 1
            #     print(f"确认价格区域未识别到数字，错误次数：{error_count}")
            #     if error_count >= error_threshold:
            #         print(f"错误次数达到阈值 {error_threshold}")
            #
            #         # 重启拍卖行
            #         self.restart_auction_house()
            #
            #         return 2

            # 金
            if prices:
                price = prices[0]
                if price < self.preset_value and price_before_confirmation == price:
                    print(f"确认价格确认区域识别到数字 {price} 依然小于预设值 {self.preset_value}，执行购买操作")
                    self.execute_purchase()
                    return 1
                else:
                    print(f"确认价格确认区域识别到数字 {price} 大于等于预设值 {self.preset_value}，取消购买！")
                    return 0
            else:
                error_count = error_count + 1
                print(f"确认价格区域未识别到数字，错误次数：{error_count}")
                if error_count >= error_threshold:
                    print(f"错误次数达到阈值 {error_threshold}")

                    # 重启拍卖行
                    # self.restart_auction_house()

                    return 2

    # 执行购买操作
    def execute_purchase(self):
        # 点击 第二次 选择商品
        pyautogui.moveTo(choose_position_2nd)
        self.mouse_controller.perform_mouse_click(choose_position_2nd)
        # sleep(interval)

        # 点击 一口价
        pyautogui.moveTo(buy_position)
        self.mouse_controller.perform_mouse_click(buy_position)
        # sleep(interval)

        # 点击 一口价购买确认（接受）
        pyautogui.moveTo(buy_confirm_position)
        self.mouse_controller.perform_mouse_click(buy_confirm_position)
        # sleep(interval)

        print("购买已执行完成")

        sleep(add_interval)
        sleep(add_interval)

    # 重启拍卖行
    def restart_auction_house(self):
        print("正在重启拍卖行...")
        sleep(5)
        # 点击 退出拍卖行
        self.mouse_controller.perform_mouse_click(exit_position)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(exit_position)
        sleep(10)

        # 点击 进入拍卖行
        self.mouse_controller.perform_mouse_click(enter_position)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(enter_position)
        sleep(interval)

        print("拍卖行重启完成，重新进入拍卖行")

        print("先退出程序")
        exit(0)

if __name__ == "__main__":

    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR(preset_value=preset_value)

    # 指定截取的屏幕区域
    ocr_processor.process_price_list_region()
