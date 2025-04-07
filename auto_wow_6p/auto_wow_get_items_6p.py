from time import sleep
import pyautogui
from pynput.mouse import Listener
import threading
import random  # 导入随机模块

""" 图形UI缩放调整为109% 以下所有定位与1.*版本不一致！(1.*版本为115%) """

''' 坐标位置 '''
positions = {
    1: {'focus': (420, 120)},
    2: {'focus': (1280, 120)},
    3: {'focus': (2140, 120)},
    4: {'focus': (420, 580)},
    5: {'focus': (1280, 580)},
    6: {'focus': (2140, 580)},
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
            # 在指定位置上添加随机偏移
            x_offset = random.randint(-50, 50)  # 随机生成偏移
            y_offset = random.randint(-50, 50)  # 随机生成偏移
            random_position = (position[0] + x_offset, position[1] + y_offset)

            pyautogui.moveTo(random_position)
            pyautogui.click()
            print(f"鼠标点击操作完成，点击位置：{random_position}")
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


class Application:
    def __init__(self, save_directory='pic', languages=None):
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def produce_and_Disenchant(self):

        sleep(1)

        while True:
            # 交易操作循环
            for i in range(2, len(positions) + 1):
                self.mouse_controller.perform_mouse_click(positions[i]['focus'])
                pyautogui.press('9')
                sleep(interval)

                pyautogui.press('9')
                sleep(interval)

                pyautogui.press('0')
                sleep(interval)

                self.mouse_controller.perform_mouse_click(positions[1]['focus'])
                pyautogui.press('0')
                sleep(interval)




if __name__ == "__main__":
    # 实例化 Application 类
    application = Application()
    # 开始制造和分解操作
    application.produce_and_Disenchant()
