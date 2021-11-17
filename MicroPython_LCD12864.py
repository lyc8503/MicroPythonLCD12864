"""
MicroPython LCD12864 取模工具
by lyc8503
"""
import tkinter as tk
from tkinter import messagebox, IntVar
import sys
import os
from tkinter.simpledialog import askstring, askinteger
from tkinter.filedialog import askopenfilename
from PIL import Image
from copy import deepcopy
import pygame
sys.setrecursionlimit(10**9)
fill_block = []
fill_loc1 = []


print("LCD12864 取模工具")
root = tk.Tk()


cv = tk.Canvas(root, width=640, height=320)


def refresh():
    print("GUI Refresh")
    cv.delete("all")
    cv.create_line(0, 0, 640, 0)
    cv.create_line(0, 0, 0, 320)
    cv.create_line(0, 320, 640, 320)
    cv.create_line(640, 0, 640, 320)
    for i in range(0, 640):
        if i % 5 == 0:
            cv.create_line(i, 0, i, 320)
    for i in range(0, 320):
        if i % 5 == 0:
            cv.create_line(0, i, 640, i)
    for block in fill_block:
        cv.create_rectangle(block[0] * 5, block[1] * 5, block[0] * 5 + 5, block[1] * 5 + 5, outline="black", fill="black")
    cv.place(x=0, y=0)
    cv.update()


def mouse_paint(event):
    loc = [int(event.x / 5), int(event.y / 5)]
    if loc[0] <= 127 and loc[1] <= 63 and loc[0] >= 0 and loc[1] >= 0:
        if loc not in fill_block:
            fill_block.append(loc)
    print(loc)
    root.title("MicroPython LCD12864 取模工具  鼠标位置:" + str(loc))
    refresh()


def mouse_clear(event):
    loc = [int(event.x / 5), int(event.y / 5)]
    if loc[0] <= 127 and loc[1] <= 63 and loc[0] >= 0 and loc[1] >= 0:
        if loc in fill_block:
            fill_block.remove(loc)
    root.title("MicroPython LCD12864 取模工具  鼠标位置:" + str(loc))
    print(loc)
    refresh()


def area_fill(event):
    global fill_loc1
    loc = [int(event.x / 5), int(event.y / 5)]
    if not (loc[0] <= 127 and loc[1] <= 64 and loc[0] >= 0 and loc[1] >= 0):
        return
    if fill_loc1 == []:
        fill_loc1 = loc
        messagebox.showinfo("提示", "填充开始点已经确定!")
        return
    for i in range(min(fill_loc1[0], loc[0]), max(fill_loc1[0], loc[0])):
        for i1 in range(min(fill_loc1[1], loc[1]), max(fill_loc1[1], loc[1])):
            if [i, i1] not in fill_block:
                fill_block.append([i, i1])
    print((min(fill_loc1[0], loc[0]), max(fill_loc1[0], loc[0])))
    print((min(fill_loc1[1], loc[1]), max(fill_loc1[1], loc[1])))
    fill_loc1 = []
    messagebox.showinfo("提示", "已经填充完成!")
    refresh()


cv.bind("<B1-Motion>", mouse_paint)
cv.bind("<Button-1>", mouse_paint)

cv.bind("<B3-Motion>", mouse_clear)
cv.bind("<Button-3>", mouse_clear)

cv.bind("<Button-2>", area_fill)


def clear():
    fill_block.clear()
    refresh()


def fill_all():
    fill_block.clear()
    for i in range(0, 128):
        for i1 in range(0, 64):
            fill_block.append([i, i1])
    refresh()


def reserve():
    for i in range(0, 128):
        for i1 in range(0, 64):
            if [i, i1] in fill_block:
                fill_block.remove([i, i1])
            else:
                fill_block.append([i, i1])
    refresh()


def get_temp_image(text, size):
    pygame.init()
    font = pygame.font.Font(os.path.join("font.ttc"), size)
    rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    pygame.image.save(rtext, "temp.jpg")


def insert_image(filename, trigger_value):
    im = Image.open(filename)
    gray = im.convert("L")
    startlocx = askinteger("插入位置", "请输入插入位置 X 坐标")
    startlocy = askinteger("插入位置", "请输入插入位置 Y 坐标")
    for dx in range(0, gray.size[0]):
        for dy in range(0, gray.size[1]):
            if not gray.getpixel((dx, dy)) > trigger_value:
                if [startlocx + dx, startlocy + dy] not in fill_block:
                    fill_block.append([startlocx + dx, startlocy + dy])
    refresh()
    try:
        os.remove("temp.jpg")
    except WindowsError:
        pass


def insert():
    messagebox.showinfo("提示", "请将你需要使用的字体改名为font.ttc并放在程序运行目录下\n若插入的文字包含中文,字体需要支持中文\n点击确认以继续")
    get_temp_image(askstring("输入文字", "请输入需要插入的文字"), askinteger("输入文字", "请输入字体大小"))
    insert_image("temp.jpg", 100)


def insert_img_get_info():
    loc = askopenfilename()
    trigger = askinteger("插入图像", "请输入在灰度值大于何值时,将该像素视为黑色块(例:100):")
    insert_image(loc, trigger)


refresh()

frame = tk.Frame(root, width=640, height=25)
clear = tk.Button(frame, width=10, text="清除", command=clear)
clear.place(x=0, y=0)
fill = tk.Button(frame, width=10, text="填充", command=fill_all)
fill.place(x=80, y=0)
reserve = tk.Button(frame, width=10, text="反转", command=reserve)
reserve.place(x=160, y=0)
help_ = tk.Button(frame, width=10, text="帮助", command=lambda: messagebox.showinfo("帮助信息", "感谢你使用LCD12864取模软件 by lyc8503,该软件为MicroPython设计\n鼠标左键或拖动填充像素\n鼠标右键或拖动擦除像素\n鼠标滚轮点击选取区域填充范围\n完成后可选择动画生成或普通生成"))
help_.place(x=400, y=0)
insert = tk.Button(frame, width=10, text="插入字符", command=insert)
insert.place(x=240, y=0)
insert_img = tk.Button(frame, width=10, text="插入图像", command=insert_img_get_info)
insert_img.place(x=320, y=0)


def create():
    print(fill_block)
    buffer_ = []
    for i in range(0, 1024):
        buffer_.append(0)
    for y_layer in range(0, 8):
        for x in range(0, 128):
            for y in range(0, 8):
                if [x, y + 8 * y_layer] in fill_block:
                    print([x, y + 8 * y_layer], end=" ")
                    buffer_[x + y_layer * 128] += 2 ** y
                    print("Add " + str(2 ** y) + " to " + str(x + y_layer * 128))
    print(buffer_)
    print(bytearray(buffer_))
    f = open(askstring("保存文件", "请输入保存文件名(无需后缀):") + ".py", "w")
    output = ""
    output += "def start(oled):\n"
    output += "    oled.buffer = %s\n" % str(bytearray(buffer_))
    output += "    oled.show()"
    f.write(output)
    f.close()
    messagebox.showinfo("提示", '成功保存!\n你可在你的代码中import <文件名>后输入"<文件名>.start(<此处传入OLED对象>)"即可显示图案')


def create_ani(mode, interval, times):
    global toplevel
    print(mode)
    print(interval)
    print(times)
    if interval is None or times is None or times < 0 or times > 128 or interval < 0:
        return
    toplevel.destroy()
    name = askstring("保存文件", "请输入保存文件名(无需后缀):")
    messagebox.showinfo("提示", '生成动画可能需要较长时间,期间程序可能会停止回应,请耐心等待\n点击确认以继续')
    if mode == 2:
        frames = []
        blocks_per_time = int(128 / times)
        for i in range(1, times):
            fill_block_bac = []
            for block in fill_block:
                block_bac = deepcopy(block)
                block_bac[0] -= (times - i) * blocks_per_time
                if block_bac[0] >= 0:
                    fill_block_bac.append(block_bac)
            frames.append(fill_block_bac)
        frames.append(deepcopy(fill_block))
        counter = 1
        for frame in frames:
            buffer_ = []
            for i in range(0, 1024):
                buffer_.append(0)
            for y_layer in range(0, 8):
                for x in range(0, 128):
                    for y in range(0, 8):
                        if [x, y + 8 * y_layer] in frame:
                            buffer_[x + y_layer * 128] += 2 ** y
            print(frame)
            f = open(name + "_frame" + str(counter) + ".py", "w")
            output = ""
            output += "def frame(oled):\n"
            output += "    oled.buffer = %s\n" % str(bytearray(buffer_))
            output += "    oled.show()"
            f.write(output)
            f.close()
            counter += 1
    if mode == 1:
        frames = []
        blocks_per_time = int(128 / times)
        for i in range(1, times):
            fill_block_bac = []
            for block in fill_block:
                block_bac = deepcopy(block)
                if block_bac[0] < i * blocks_per_time:
                    fill_block_bac.append(block_bac)
            frames.append(fill_block_bac)
        frames.append(deepcopy(fill_block))
        counter = 1
        for frame in frames:
            buffer_ = []
            for i in range(0, 1024):
                buffer_.append(0)
            for y_layer in range(0, 8):
                for x in range(0, 128):
                    for y in range(0, 8):
                        if [x, y + 8 * y_layer] in frame:
                            buffer_[x + y_layer * 128] += 2 ** y
            print(frame)
            f = open(name + "_frame" + str(counter) + ".py", "w")
            output = ""
            output += "def frame(oled):\n"
            output += "    oled.buffer = %s\n" % str(bytearray(buffer_))
            output += "    oled.show()"
            f.write(output)
            f.close()
            counter += 1
    f = open(name + ".py", "w")
    output_to_main = ""
    output_to_main += "import time\nimport gc\n"
    output_to_main += "\n\ndef start(oled):\n"
    for i in range(1, counter):
        output_to_main += ("    import " + name + "_frame" + str(i))
        output_to_main += ("\n    " + "time.sleep_ms(%s)\n" % str(interval))
        output_to_main += ("    " + name + "_frame" + str(i) + ".frame(oled)\n")
        output_to_main += ("    del " + name + "_frame" + str(i) + "\n")
        output_to_main += "    gc.collect()\n"
    f.write(output_to_main)
    f.close()
    messagebox.showinfo("提示", '成功保存!\n你可在你的代码中import <文件名>后输入"<文件名>.start(<此处传入OLED对象>)"即可显示图案')


def create_ani_info():
    global root
    global toplevel
    toplevel = tk.Toplevel(root)
    toplevel.title("生成动画")
    toplevel.geometry("248x175")
    toplevel.resizable(False, False)
    mode_label = tk.Label(toplevel, text="模式选择:")
    mode_label.place(x=0, y=0)
    v = IntVar()
    v.set(1)
    sneak_out = tk.Radiobutton(toplevel, text="淡出", variable=v, value=1)
    fly_in = tk.Radiobutton(toplevel, text="飞入", variable=v, value=2)
    sneak_out.place(x=0, y=20)
    fly_in.place(x=75, y=20)
    interval_label = tk.Label(toplevel, text="动画间隔(ms):", width=34)
    interval_label.place(x=0, y=50)
    interval = tk.Entry(toplevel, width=35)
    interval.place(x=0, y=70)
    times_label = tk.Label(toplevel, text="动画次数(最大128):", width=34)
    times_label.place(x=0, y=100)
    times = tk.Entry(toplevel, width=35)
    times.place(x=0, y=120)
    submit = tk.Button(toplevel, text="完成", command=lambda: create_ani(v.get(), int(interval.get()), int(times.get())), width=34)
    submit.place(x=0, y=150)


create = tk.Button(frame, width=10, text="生成代码", command=create)
create.place(x=480, y=0)
create_animation = tk.Button(frame, width=10, text="生成动画", command=create_ani_info)
create_animation.place(x=560, y=0)
frame.place(x=0, y=322)

root.title("MicroPython LCD12864 取模工具")
root.geometry("640x350")
root.resizable(False, False)
root.mainloop()
