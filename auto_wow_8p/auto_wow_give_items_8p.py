import ctypes
from time import sleep
from pynput.keyboard import Listener as KeyboardListener, KeyCode
import random
import sys

# 导入 Windows API 用于点击模拟（仅在 Windows 环境有效）
user32 = ctypes.windll.user32

# 定义输入结构
class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("mi", ctypes.c_void_p)]

# 定义模拟键盘按下和释放的函数
def press_key(key):
    # 模拟按下
    user32.keybd_event(key, 0, 0, 0)
    sleep(0.1)
    # 模拟释放
    user32.keybd_event(key, 0, 2, 0)

# 坐标位置
positions = {
    1: {'focus': (420, 120)},
    2: {'focus': (1280, 120)},
    3: {'focus': (2140, 120)},
    4: {'focus': (420, 580)},
    5: {'focus': (1280, 580)},
    6: {'focus': (2140, 580)},
    7: {'focus': (420, 1040)},
    8: {'focus': (1280, 1040)},
    # 9: {'focus': (2140, 1040)},
}

# 操作间隔
interval = 0.5

# 模拟鼠标左键点击
def mouse_click(x, y):
    # 设置鼠标坐标到指定位置
    ctypes.windll.user32.SetCursorPos(x, y)
    # 模拟鼠标左键按下和释放
    # user32.mouse_event(2, 0, 0, 0, 0)  # 鼠标左键按下
    # user32.mouse_event(4, 0, 0, 0, 0)  # 鼠标左键释放

    # 模拟鼠标右键按下和释放
    user32.mouse_event(8, 0, 0, 0, 0)  # 鼠标右键按下
    user32.mouse_event(16, 0, 0, 0, 0)  # 鼠标右键释放

class MouseController:
    def __init__(self):
        self.mouse_moving = False

    def perform_mouse_click(self, position):
        # 在指定位置上添加随机偏移
        x_offset = random.randint(-10, 10)
        y_offset = random.randint(-10, 10)
        random_position = (position[0] + x_offset, position[1] + y_offset)

        # 直接点击，不移动鼠标
        mouse_click(random_position[0], random_position[1])
        print(f"鼠标点击操作完成，点击位置：{random_position}")

class Application:
    def __init__(self):
        self.mouse_controller = MouseController()
        self.last_minute_checked = None  # 用于避免重复吃药
        self.running = True  # 控制程序运行状态

    def produce_and_disenchant(self):
        sleep(1)
        # give items
        for i in range(2, len(positions) + 1):
            if not self.running:  # 检查是否仍在运行
                return
            self.mouse_controller.perform_mouse_click(positions[i]['focus'])
            sleep(interval)

            # 按下 '9' 键 (0x39是键码)
            press_key(0x39)
            sleep(interval)

            press_key(0x39)
            sleep(interval)

            if not self.running:  # 检查是否仍在运行
                return
            self.mouse_controller.perform_mouse_click(positions[1]['focus'])
            sleep(interval)

            # 按下 '-' 键 (0xBD是键码)
            press_key(0xBD)
            sleep(interval)

            press_key(0xBD)
            sleep(interval)

            if not self.running:  # 检查是否仍在运行
                return
            self.mouse_controller.perform_mouse_click(positions[1]['focus'])
            sleep(interval)

            # 按下 '0' 键 (0x30是键码)
            press_key(0x30)
            sleep(interval)

            if not self.running:  # 检查是否仍在运行
                return
            self.mouse_controller.perform_mouse_click(positions[i]['focus'])
            # 按下 '0' 键 (0x30是键码)
            press_key(0x30)
            sleep(interval)

        sys.exit() # 退出程序

    def stop(self):
        """ 停止程序运行 """
        self.running = False
        print("程序已停止")
        sys.exit()  # 退出程序

def on_press(key):
    """ 监听键盘按键 """
    if key == KeyCode(char='q'):  # 按下 'q' 键时停止程序
        application.stop()

if __name__ == "__main__":
    # 实例化 Application 类
    application = Application()

    # 启动键盘监听
    keyboard_listener = KeyboardListener(on_press=on_press)
    keyboard_listener.start()

    # 开始制造和分解操作
    application.produce_and_disenchant()

    # 等待键盘监听结束
    keyboard_listener.join()
