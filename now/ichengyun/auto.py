import io
import time
import pandas
import traceback
import win32gui, win32api, win32con
from PIL import ImageGrab
from sqlalchemy import create_engine
from types import MethodType, FunctionType

from utils.baidu_ocr import BaiduOCR
from config import DATABASES, logger, DEBUG


class WinOperate(object):
    def __init__(self):
        self.handle = win32gui.FindWindow(None, "CS")
        self.get_windows()

    def get_windows(self):
        self.left, self.top, right, bottom = win32gui.GetWindowRect(
            self.handle)

    def mouse_move(self, offset_x, offset_y, click=True):
        win32gui.SetForegroundWindow(self.handle)

        win32api.SetCursorPos([self.left + offset_x, self.top + offset_y])

        if click:
            self.mouse_left_click()

    def mouse_left_click(self):
        win32api.mouse_event(
            win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0,
            0, 0)

    def screenshot(self):
        return ImageGrab.grab((self.left + 570, self.top + 125,
                               self.left + 875, self.top + 430))


class Ichengyun(object):
    def __init__(self):
        self.win = WinOperate()
        self.info = pandas.DataFrame(columns=["姓名", "注册号", "证书", "电话"])
        # df.drop(df.index,inplace=True)

        self.run_func(self.init_sql)

    def init_sql(self):
        self.engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset={charset}"
            .format(**DATABASES))

    def get_word(self):
        pic = self.win.screenshot()
        byte_io = io.BytesIO()
        pic.save(byte_io, 'png')
        byte_io.seek(0)

        words = BaiduOCR().pic2word(byte_io.read())["words_result"]
        # words = FaceOcr().pic2word(byte_io.read())["result"]
        # print(words)
        # print("OCR Now")

        if words:
            # print("OCR OK")
            self.run_func(self.data_clean, words)
        else:
            print("OCR ERROR")
            print(words)
            print(set(list(pic.getdata())))

    def data_clean(self, words):
        info = {}
        register_list = []
        for item in words:
            word = item["words"]

            if ":" in word:
                temp = word.split(":")
                if "姓名" in temp[0]:
                    if "(" in temp[1]:
                        info["姓名"] = temp[1].split("(")[0]
                    elif "（" in temp[1]:
                        info["姓名"] = temp[1].split("（")[0]
                    elif "O" in temp[1]:
                        info["姓名"] = temp[1].split("O")[0]
                    elif "o" in temp[1]:
                        info["姓名"] = temp[1].split("o")[0]
                    elif "0" in temp[1]:
                        info["姓名"] = temp[1].split("0")[0]
                    elif "男)" in temp[1]:
                        info["姓名"] = temp[1].split("男)")[0]
                    elif "侽男)" in temp[1]:
                        info["姓名"] = temp[1].split("侽男)")[0]
                    else:
                        info["姓名"] = temp[1]
                elif "注册" in temp[0]:
                    info["注册号"] = temp[1]
            elif "~" in word:
                if "主册" in word:
                    word = word.replace("主册", "注册")
                register_list.append(word)

            elif len(word) == 11:
                info["电话"] = word

        level_list = []
        for index, item in enumerate(register_list):
            if "级" in item:
                level_temp = item.split("级")

                if len(level_temp) == 2:
                    if len(level_temp[0]) == 0:
                        level_list.append(True)
                    elif len(level_temp[0]) == 1:
                        level_list.append(level_temp[0])
                    else:
                        level_list.append(False)
                else:
                    level_list.append(False)
            else:
                level_list.append(False)

        if True in level_list:
            for item in level_list:
                if isinstance(item, str):
                    level_temp = item

            for index, item in enumerate(level_list):
                if item is True:
                    register_list[index] = "{}{}".format(
                        level_temp, register_list[index])

        info["证书"] = "\n".join(register_list)
        # print("ADD NOW")
        self.info = self.info.append(info, ignore_index=True)
        # print(len(self.info), "\n")

    def next_page(self):
        self.run_func(self.win.mouse_move, 335, 565)
        hold_on(8)
        self.run_func(self.win.mouse_move, 600, 375)

    def save_info(self):
        if len(self.info) >= 180:
            self.info.to_excel(
                "./{}.xlsx".format(int(time.time() * 1000)), index=False)
            self.info.to_sql(
                "ichengyun", self.engine, if_exists="append", index=False)
            del self.info
            self.info = pandas.DataFrame(columns=["姓名", "注册号", "证书", "电话"])

            logger.info("--->Info: save info")

            return False
        else:
            logger.info("--->Info: No.{} is down".format(len(self.info)))
            return True

    def loading_status(self):
        hold_on(1.5)
        start_time = time.time()
        while True:
            if time.time() - start_time >= 30:
                break

            pic = self.win.screenshot()

            if self.run_func(judge_pixel, pic) == "colorful":
                hold_on(1)
                self.run_func(self.win.mouse_move, 600, 345)
                hold_on(0.5)
                break
            else:
                hold_on(1)
                continue

    def auto_click(self):
        starttime = time.time()

        for _ in range(84):
            self.run_func(self.win.mouse_move, 230, 160)
            pic = self.run_func(self.win.screenshot)

            self.run_func(self.loading_status)

            self.run_func(self.win.mouse_move, 555, 540)
            hold_on(1)

            self.run_func(self.get_word)

            if self.run_func(self.save_info) is False:
                logger.info("--->Info: sleep 24 hours now")
                hold_on(86400)

        for index in range(16):
            offset = 24 * index
            self.run_func(self.win.mouse_move, 230, 160 + offset)

            self.run_func(self.loading_status)

            self.run_func(self.get_word)

            if self.run_func(self.save_info) is False:
                logger.info("--->Info: sleep 24 hours now")
                hold_on(86400)

        self.run_func(self.next_page)
        self.run_func(self.save_info)
        logger.info("--->Info: next page")
        hold_on(5)

    def main(self):
        while True:
            self.run_func(self.auto_click)

    def run_func(self, func, *args, **kwargs):
        if isinstance(func, (MethodType, FunctionType)):
            if DEBUG:
                return func(*args, **kwargs)
            else:
                try:
                    return func(*args, **kwargs)
                except:
                    logger.error(
                        "--->Error: The function {} is wrong, the error is {}".
                        format(func.__name__, traceback.format_exc()))

        else:
            logger.error(
                "--->Error: The type {} is wrong, the func is {}".format(
                    type(func), func))


def hold_on(second):
    time.sleep(second)


def judge_pixel(img):
    pixels = list(img.getdata())

    if (113, 166, 255) in pixels:
        return "blue"
    else:
        single = set(pixels)
        if len(single) > 1:
            return "colorful"
        elif (255, 255, 255) in single:
            return "white"


if __name__ == "__main__":
    Ichengyun().main()
