import os
import tkinter as tk

from hope2 import launcher


from tkinter import ttk
from framework import tk_utils as tku
from framework import utils

from app.my import img
from app.my import Color
from app.my import String
from app.my import Font


# from scipy.misc import imsave

import time

workspace_dir = "images"
result_prefix = 'style_transfer_'

iterations = 1

# style_weight = 1.
# content_weight = 0.025

class GUI(tku.WinBase):

    target_file_name = ""
    # style_file_name = ""

    def __init__(self):
        tku.WinBase.__init__(self)

        self.title = String.r_app_title
        self.set_size(1024, 768)
        self.set_icon(img("Money.ico"))
        self.selected = False
        self.lay_body()

    def lay_body(self):
        self.lay_title(self.win).pack(fill=tk.X)

        self.lay_main(self.win).pack(expand=tk.YES, fill=tk.BOTH)

        self.lay_bottom(self.win).pack(fill=tk.X)

        self.txtIterations.insert('end', iterations)
        return self.win

    def lay_title(self, parent):
        """ 标题栏 """
        frame = tk.Frame(parent, bg="black")

        def _label(_frame, text, size=12, bold=False):
            return tku.label(_frame, text, size=size, bold=bold, bg="black", fg="white")

        def _button(_frame, text, size=12, bold=False, width=12, command=None):   # bg = DarkSlateGray
            return tk.Button(_frame, text=text, bg="black", fg="white",
                             width=width, height=2, font=tku.font(size=size, bold=bold),
                             relief=tk.FLAT, command=command)

        _label(frame, String.r_app_title, 16, True).pack(side=tk.LEFT, padx=10)
        _label(frame, "").pack(side=tk.LEFT, padx=50)  # 用于布局的空字符串
        _label(frame, "").pack(side=tk.RIGHT, padx=5)
        _button(frame, "退出", width=8, command=self.do_close).pack(side=tk.RIGHT, padx=15)
        tku.image_label(frame, img("user.png"), 40, 40, False).pack(side=tk.RIGHT)

        return frame

    def lay_bottom(self, parent):
        """ 窗体最下面留空白 """
        frame = tk.Frame(parent, height=10, bg="whitesmoke")
        frame.propagate(True)
        return frame

    def lay_main(self, parent):
        frame = tk.Frame(parent, bg=Color.r_background)

        self.lay_org_image(frame).pack(side=tk.LEFT, fill=tk.Y)
        self.lay_result_image(frame).pack(expand=tk.YES, fill=tk.BOTH, padx=5, pady=5)

        return frame

    def lay_org_image(self, parent):
        frame = tk.Frame(parent, bg=Color.r_whitesmoke, width=450)

        self.org_img = tku.ImageLabel(frame, width=300, height=300)
        self.org_img.pack(side=tk.TOP, fill=tk.Y, padx=10, pady=5)
        self.org_img.set_image(img("flower.jpg"))
        self.org_img.bind('<Button-1>', self.do_choice_image)
        self.target_file_name = img("flower.jpg")

        # self.style_img = tku.ImageLabel(frame, width=300, height=300)
        # self.style_img.pack(side=tk.TOP, padx=10, pady=5)
        # self.style_img.set_image(img("style.jpg"))
        # # self.style_img.bind('<Button-1>', self.do_choice_style_image)
        # self.style_file_name = img("style.jpg")  # 设置缺省风格格式文件


        tk.Button(frame, text=" 选择图片 ", bg="LightBlue", font=Font.r_normal, command=self.do_choice_image)\
            .pack(side=tk.LEFT, fill=tk.X, padx=10)
        # tk.Button(frame, text=" 风格图片 ", bg="LightYellow", font=Font.r_normal)\
        #     .pack(side=tk.LEFT, fill=tk.X)
        tk.Button(frame, text=" 生成目录 ", bg="LightYellow", font=Font.r_normal, command=self.do_browser_workspace) \
            .pack(side=tk.LEFT, fill=tk.X,padx=10)
        tk.Button(frame, text="开始转换", bg="LightGreen", font=Font.r_medium_title, command=self.do_transfer) \
            .pack(side=tk.LEFT, fill=tk.X, padx=10)
        tk.Button(frame, text=" 专家模式 ", bg="LightGreen", font=Font.r_medium_title, command=self.do_HC_transfer) \
            .pack(side=tk.LEFT, fill=tk.X,padx=10)
        # tk.Button(frame, text=" 图片生成目录 ", bg="LightBlue", font=Font.r_small_content,
        #           command=self.do_browser_workspace) \
        #     .pack(side=tk.RIGHT, anchor='se', padx=20,fill=tk.X)

        frame.propagate(True)
        frame.pack_propagate(0)
        return frame

    def lay_result_image(self, parent):

        frame = tk.Frame(parent, bg=Color.r_white)

        fra_result = tk.Frame(frame, bg=Color.r_white)
        fra_result.pack(expand=tk.YES, fill=tk.BOTH, pady=5)
        fra_result.pack_propagate(0)

        self.final_img = tku.ImageLabel(fra_result, width=460, height=460)
        self.final_img.pack(side='top', padx=10, pady=10)
        self.final_img.set_image(img("style_flower.png"))
        self.final_img.bind('<Button-1>', self.do_browser_workspace)



        # --------------------------------------------------------------
        self.fra_output = tk.Frame(frame, height=200, bg=Color.r_whitesmoke)
        self.fra_output.pack(side=tk.BOTTOM, fill=tk.X)
        self.fra_output.pack_propagate(0)

        # fra_output-tabControl
        self.tabControl = ttk.Notebook(self.fra_output)  # Create Tab Control
        self.tabControl.pack(side=tk.TOP, fill=tk.X, anchor=tk.NW)

        # fra_output - tabControl - tabParameters
        tabParameters = ttk.Frame(self.tabControl)

        #
        # f3 = tk.Frame(tabParameters)
        # f3.pack(side='top', fill='x', pady=10)
        # tk.Label(f3, text="风格权重", font=Font.r_small_title).pack(side='left', anchor='w', pady=3, padx=10)
        # txtStyle = tk.Entry(f3, width=40, font=Font.r_normal)
        # txtStyle.pack(side='left', anchor='n', padx=30, pady=3)
        # self.txtStyle = txtStyle

        # fra_output - tabControl - tabOutput
        self.tabOutput = ttk.Frame(self.tabControl)  # Create a tab
        self.tabControl.add(self.tabOutput, text='处理信息')

        txtOutput = tk.Text(self.tabOutput, font=Font.r_small_content)
        ysb = ttk.Scrollbar(self.tabOutput, orient="vertical", command=txtOutput.yview)  # y滚动条
        ysb.pack(side='right', fill='y')

        txtOutput.configure(yscrollcommand=ysb.set)
        txtOutput.pack(expand='yes', fill='both')
        self.txtOutput = txtOutput

        self.tabControl.add(tabParameters, text='系统评价')

        f1 = tk.Frame(tabParameters)
        f1.pack(side='top', fill='x', pady=10)
        tk.Label(f1, text="您的姓名", font=Font.r_small_title).pack(side='left', anchor='w', pady=3, padx=10)
        txtIterations = tk.Entry(f1, width=40, font=Font.r_normal)
        txtIterations.pack(side='left', anchor='n', padx=30, pady=3)
        self.txtIterations = txtIterations

        f2 = tk.Frame(tabParameters)
        f2.pack(side='top', fill='x')
        tk.Label(f2, text="您的评价", font=Font.r_small_title).pack(side='left', anchor='w', pady=3, padx=10)
        txtContent = tk.Entry(f2, width=40, font=Font.r_normal)
        txtContent.pack(side='left', anchor='n', padx=30, pady=3)

        print("laysuccessful")
        self.log_message("GUI完成加载，欢迎使用")
        return frame

    # -------------------------------------------------------------------------
    def do_close(self):
        """ 关闭应用程序 """
        msg = String.r_exit_system
        if tku.show_confirm(msg):
            self.close()

    def do_choice_image(self, *args):
        """ 选择目标图片 """
        img_path = tku.ask_for_filename()
        if img_path is not None and img_path != "":
            self.target_file_name = img_path
            self.org_img.set_image(img_path)
            self.selected = True
            self.log_message("选择图片成功")
        # self.refresh()

    def do_browser_workspace(self, *args):
        """ 浏览新生成的图片 """
        self.log_message("打开生成图片目录")
        if os.path.exists(workspace_dir):
            os.startfile(workspace_dir)
    def log_message(self, *messages):
        """ 记录处理过程的日志信息 """
        info = utils.strftime(True) + " : "
        for message in messages:
            info += str(message) + "  "
        info += "\n"
        self.txtOutput.insert('end', info)
        self.refresh()  # 这句话很重要
        self.txtOutput.see('end')
    def do_transfer(self):
        print("ok")
        target_image_path = self.target_file_name

        if not os.path.exists(target_image_path) and self.selected:
            tku.show_message("请先选择目标图片文件！")
            return
        if self.selected:
            self.log_message("读取图片成功")
        # utils.create_folder(workspace_dir)
            launcher.run.upscale(target_image_path)
            image = "./images/fsrcnnOutput.png"
            self.log_message("开始处理")
            self.refresh()
        
            self.log_message('获得图片信息.')
            temp_filename = image
            self.final_img.set_image(temp_filename)
            # self.log_message("ssim:",ssim)
            self.log_message('处理完成')
    def do_HC_transfer(self):
        print("ok")
        target_image_path = self.target_file_name

        if not os.path.exists(target_image_path) and self.selected:
            tku.show_message("请先选择目标图片文件！")
            return
        if self.selected:
            self.log_message("读取图片成功")
            # utils.create_folder(workspace_dir)
            ori_psnr,bicuic_psnr = launcher.run.testFromPb(target_image_path)
            image = "./images/fsrcnnOutput.png"
            self.log_message("开始处理")
            self.refresh()

            self.log_message('获得图片信息.')
            temp_filename = image
            self.final_img.set_image(temp_filename)
            # self.log_message("ssim:",ssim)
            self.log_message("PSNR of FSRCNN  upscaled image:",ori_psnr)
            self.log_message("PSNR of bicuic upscaled image",bicuic_psnr)
            self.log_message('处理完成')
