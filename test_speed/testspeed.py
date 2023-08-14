import autopy
import time
import webbrowser
import os
import keyboard


def find_btn(btn):
    btn = autopy.bitmap.Bitmap.open(btn)
    background = autopy.bitmap.capture_screen()

    pos = background.find_bitmap(btn)
    return pos



if __name__ == "__main__":

    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url='file://' + os.path.realpath('speedtest.html'),  new=1)
    keyboard.send('F11')
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.get('file://' + os.path.realpath('speedtest.html'))
    # driver.maximize_window()


    time.sleep(5)
    pos_btn = find_btn('btn.png')
    if pos_btn is not None:
        autopy.mouse.move(pos_btn[0] + 20, pos_btn[1] + 20)
        autopy.mouse.click()
        while True:
            time.sleep(10)
            pos_confirm = find_btn('btn_confirm.png')
            if pos_confirm is None:              
                pos_restart = find_btn('btn_restart.png')
                if pos_restart is None:
                    time.sleep(5)
                else: 
                    autopy.mouse.move(pos_btn[0] + 20, pos_btn[1] + 20)           
                    autopy.mouse.click()
                    # time.sleep(3)
            else:
                autopy.mouse.move(pos_confirm[0] + 20, pos_confirm[1] + 20)
                autopy.mouse.click()
    else:
        print("Please restart the Program!")