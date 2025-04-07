from time import sleep
import pyautogui
from pynput.mouse import Listener
import threading

""" 图形UI缩放调整为109% 以下所有定位与1.*版本不一致！(1.*版本为115%) """


''' 坐标位置 '''
# 人物图标 的坐标位置
character_position = (650, 915)
# 离开副本 的坐标位置
quit_position = (750, 1362)
# 确认离开副本 的坐标位置
confirm_quit_position = (1150, 370)
# 选择副本 的坐标位置
select_instance_position = (170, 920)
# 寻找队伍 的坐标位置
search_team_position = (660, 877)
# 进入副本 的坐标位置
join_instance_position = (1140, 545)


''' 操作间隔 '''
# 普通间隔
interval = 0.2
# 等待时间
wait_time = 7


class MouseController:
    def __init__(self):
        self.mouse_moving = False

    def perform_mouse_click(self, position, right_click=False):
        """ 在指定位置执行鼠标点击 """
        pyautogui.moveTo(position)
        if right_click:
            pyautogui.rightClick()
            print(f"鼠标右击操作完成，点击位置：{position}")
        else:
            pyautogui.click()
            print(f"鼠标点击操作完成，点击位置：{position}")


class ScreenCaptureOCR:
    def __init__(self):
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def press_product_and_resolve(self):
        # 点击 人物图标
        self.mouse_controller.perform_mouse_click(character_position)
        sleep(interval)
        # 右击 人物图标
        self.mouse_controller.perform_mouse_click(character_position, right_click=True)
        sleep(interval)
        # 点击 离开副本
        self.mouse_controller.perform_mouse_click(quit_position)
        sleep(interval)
        # 点击 确认离开副本h
        self.mouse_controller.perform_mouse_click(confirm_quit_position)
        sleep(interval)

        sleep(wait_time)

        # 按下 H 键
        pyautogui.press('h')
        sleep(interval)
        # 点击 选择副本
        self.mouse_controller.perform_mouse_click(select_instance_position)
        sleep(interval)
        # 点击 寻找队伍
        self.mouse_controller.perform_mouse_click(search_team_position)
        sleep(interval)

        sleep(5)

        # 点击 进入副本
        self.mouse_controller.perform_mouse_click(join_instance_position)
        sleep(interval)


if __name__ == "__main__":
    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR()
    # 指定截取的屏幕区域
    ocr_processor.press_product_and_resolve()
