import pygetwindow as gw

def show_window_buttons(process_name):
    windows = gw.getWindowsWithTitle(process_name)
    if len(windows) > 0:
        window = windows[0]
        window.activate()  # Kích hoạt cửa sổ
        window.maximize()  # Phóng to cửa sổ

if __name__ == '__main__':
    process_name = 'notepad.exe'  # Thay đổi thành tên tiến trình mong muốn
    show_window_buttons(process_name)