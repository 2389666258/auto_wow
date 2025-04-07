from time import sleep
import pyautogui
from pynput.mouse import Listener
import threading


""" 图形UI缩放调整为109% 以下所有定位与1.*版本不一致！(1.*版本为115%) """


''' 坐标位置 '''
# 裁缝1 的坐标位置
tailor_position_1 = (395, 180)
# 制造1 的坐标位置
produce_position_1 = (900, 648)
# 分解1 的坐标位置
resolve_position_1 = (900, 450)

# 裁缝2 的坐标位置
tailor_position_2 = (1675, 180)
# 制造2 的坐标位置
produce_position_2 = (2180, 648)
# 分解2 的坐标位置
resolve_position_2 = (2180, 450)

# 裁缝3 的坐标位置
tailor_position_3 = (395, 875)
# 制造3 的坐标位置
produce_position_3 = (900, 1348)
# 分解3 的坐标位置
resolve_position_3 = (900, 1150)

# 裁缝4 的坐标位置
tailor_position_4 = (1675, 875)
# 制造4 的坐标位置
produce_position_4 = (2180, 1348)
# 分解4 的坐标位置
resolve_position_4 = (2180, 1150)


''' 操作间隔 '''
# 普通间隔
interval = 0.1
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
        # 初始化鼠标控制器
        self.mouse_controller = MouseController()

    def press_product_and_resolve(self):

        sleep(1)

        # 点击 分解1
        pyautogui.moveTo(resolve_position_1)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(resolve_position_1)
        sleep(interval)
        # 按下 k 键
        pyautogui.press('k')
        sleep(interval)
        # 点击 裁缝1
        pyautogui.moveTo(tailor_position_1)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(tailor_position_1)
        sleep(interval)

        # 点击 分解2
        pyautogui.moveTo(resolve_position_2)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(resolve_position_2)
        sleep(interval)
        # 按下 k 键
        pyautogui.press('k')
        sleep(interval)
        # 点击 裁缝2
        pyautogui.moveTo(tailor_position_2)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(tailor_position_2)
        sleep(interval)

        # 点击 分解3
        pyautogui.moveTo(resolve_position_3)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(resolve_position_3)
        sleep(interval)
        # 按下 k 键
        pyautogui.press('k')
        sleep(interval)
        # 点击 裁缝3
        pyautogui.moveTo(tailor_position_3)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(tailor_position_3)
        sleep(interval)

        # 点击 分解4
        pyautogui.moveTo(resolve_position_4)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(resolve_position_4)
        sleep(interval)
        # 按下 k 键
        pyautogui.press('k')
        sleep(interval)
        # 点击 裁缝4
        pyautogui.moveTo(tailor_position_4)
        sleep(interval)
        self.mouse_controller.perform_mouse_click(tailor_position_4)
        sleep(interval)


        while True:
            # 点击 制造1
            pyautogui.moveTo(produce_position_1)
            self.mouse_controller.perform_mouse_click(produce_position_1)
            pyautogui.click()
            # 按下 = 键
            # pyautogui.press('=')
            # pyautogui.press('=')

            # 点击 制造2
            pyautogui.moveTo(produce_position_2)
            self.mouse_controller.perform_mouse_click(produce_position_2)
            pyautogui.click()
            # 按下 = 键
            # pyautogui.press('=')
            # pyautogui.press('=')

            # 点击 制造3
            pyautogui.moveTo(produce_position_3)
            self.mouse_controller.perform_mouse_click(produce_position_3)
            pyautogui.click()
            # 按下 = 键
            # pyautogui.press('=')
            # pyautogui.press('=')

            # 点击 制造4
            pyautogui.moveTo(produce_position_4)
            self.mouse_controller.perform_mouse_click(produce_position_4)
            pyautogui.click()
            # 按下 = 键
            # pyautogui.press('=')
            # pyautogui.press('=')

            # 等待制造时间0
            # sleep(0.9) # 稳妥
            # sleep(0.3)
            # sleep(0.1)



            # 点击 分解1
            self.mouse_controller.perform_mouse_click(resolve_position_1)
            pyautogui.click()
            # 按下 数字7 键
            pyautogui.press('7')
            pyautogui.press('7')

            # 点击 分解2
            self.mouse_controller.perform_mouse_click(resolve_position_2)
            pyautogui.click()
            # 按下 数字7 键
            pyautogui.press('7')
            pyautogui.press('7')

            # 点击 分解3
            self.mouse_controller.perform_mouse_click(resolve_position_3)
            pyautogui.click()
            # 按下 数字7 键
            pyautogui.press('7')
            pyautogui.press('7')

            # 点击 分解4
            self.mouse_controller.perform_mouse_click(resolve_position_4)
            pyautogui.click()
            # 按下 数字7 键
            pyautogui.press('7')
            pyautogui.press('7')

            # 等待分解时间
            # sleep(0.9) # 稳妥
            # sleep(0.4)
            # sleep(0.2)



if __name__ == "__main__":
    # 实例化 ScreenCaptureOCR 类
    ocr_processor = ScreenCaptureOCR()
    # 指定截取的屏幕区域
    ocr_processor.press_product_and_resolve()
