import win32gui


# 枚举所有窗口句柄，并获取每个窗口的标题和类名
def enum_windows():
    hwnd_list = []

    # 回调函数：将每个窗口句柄和窗口标题添加到列表中
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):  # 仅显示可见窗口
            window_title = win32gui.GetWindowText(hwnd)  # 获取窗口标题
            class_name = win32gui.GetClassName(hwnd)  # 获取窗口类名
            hwnd_list.append((hwnd, window_title, class_name))

    win32gui.EnumWindows(callback, None)
    return hwnd_list


# 打印所有窗口的句柄、标题和类名
windows = enum_windows()
for hwnd, title, class_name in windows:
    print(f"句柄: {hwnd}, 标题: {title}, 类名: {class_name}")


# import ctypes
# from ctypes import wintypes
# import win32gui
# import win32con
#
# # 定义鼠标消息
# WM_LBUTTONDOWN = 0x0201
# WM_LBUTTONUP = 0x0202
#
# # 获取窗口句柄
# def get_window_handle(window_title):
#     hwnd = win32gui.FindWindow(None, window_title)
#     if hwnd == 0:
#         raise Exception(f"找不到窗口: {window_title}")
#     return hwnd
#
# # 发送鼠标点击事件到指定窗口和位置
# def click_in_window(hwnd, x, y):
#     lParam = (y << 16) | x  # 将 x, y 位置打包到lParam中
#     # 发送鼠标按下和松开的消息
#     ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 0, lParam)
#     ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, lParam)
#
# # 示例用法：获取名为 "Calculator" 的窗口句柄，在窗口内点击(100, 100)位置
# hwnd = get_window_handle("魔兽世界")  # 请将窗口名称换成你目标程序的窗口名称
# click_in_window(hwnd, 100, 100)


import ctypes
from ctypes import wintypes

# 定义鼠标事件消息
WM_LBUTTONDOWN = 0x0201  # 鼠标左键按下
WM_LBUTTONUP = 0x0202    # 鼠标左键抬起

# 将屏幕坐标转换为窗口内坐标
def screen_to_client(hwnd, x, y):
    point = wintypes.POINT(x, y)
    ctypes.windll.user32.ScreenToClient(hwnd, ctypes.byref(point))
    return point.x, point.y

# 发送鼠标点击事件到指定窗口和位置
def click_in_window(hwnd, x, y):
    # 将 x 和 y 坐标打包到 lParam 中（低16位是x，高16位是y）
    lParam = (y << 16) | x
    # 发送鼠标左键按下消息
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONDOWN, 0, lParam)
    # 发送鼠标左键抬起消息
    ctypes.windll.user32.SendMessageW(hwnd, WM_LBUTTONUP, 0, lParam)

# 示例用法：使用屏幕坐标点击窗口
hwnd = 1311310  # 替换为你已经获取的窗口句柄
screen_x, screen_y = 500, 500  # 屏幕上的位置
client_x, client_y = screen_to_client(hwnd, screen_x, screen_y)  # 转换为窗口内坐标
click_in_window(hwnd, client_x, client_y)  # 在窗口内点击
