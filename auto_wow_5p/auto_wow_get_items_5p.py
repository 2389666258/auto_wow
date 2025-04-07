from time import sleep
import pyautogui
from pynput.mouse import Listener
import threading


""" 图形UI缩放调整为109% 以下所有定位与1.*版本不一致！(1.*版本为115%) """


''' 坐标位置 '''
positions = {
    1: {'tailor': (250, 125), 'produce': (265, 342), 'focus': (400, 340)},
    2: {'tailor': (1100, 125), 'produce': (1115, 342), 'focus': (1250, 340)},
    3: {'tailor': (1955, 125), 'produce': (1970, 342), 'focus': (2105, 340)},
    4: {'tailor': (250, 590), 'produce': (265, 807), 'focus': (400, 805)},
    5: {'tailor': (1100, 590), 'produce': (1115, 807), 'focus': (1250, 805)},
}

''' 操作间隔 '''
# 普通间隔
interval = 0.5
# 等待时间
wait_time = 1


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
    def __init__(self, save_directory='pic', languages=None):
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def perform_actions(self, position_key, key_to_press):
        """ 辅助函数，执行点击并按下指定的键 """
        self.mouse_controller.perform_mouse_click(positions[position_key]['focus'])
        sleep(interval)
        pyautogui.press(key_to_press)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(positions[position_key]['tailor'])
        sleep(interval)

    def press_product_and_focus(self):
        sleep(1)

        # 分解和裁缝操作循环
        # for i in range(1, len(positions) + 1):
        #     self.perform_actions(i, 'k')

        while True:
            # 收成品材料循环
            for i in range(2, len(positions) + 1):
                self.mouse_controller.perform_mouse_click(positions[i]['focus'])
                sleep(interval)
                sleep(interval)

                # 模拟键盘按下 8



                pyautogui.press('8')
                sleep(interval)

                pyautogui.press('8')
                sleep(interval)

                pyautogui.press('9')
                sleep(interval)

                self.mouse_controller.perform_mouse_click(positions[1]['focus'])

                pyautogui.press('9')
                sleep(interval)

            sleep(0.2)


if __name__ == "__main__":
    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR()
    # 开始制造和分解操作
    ocr_processor.press_product_and_focus()
