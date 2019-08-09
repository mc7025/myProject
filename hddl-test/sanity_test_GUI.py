#!/usr/bin/env python3
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASE_HDDLR = os.path.join(BASE, "hddl_r_sw_validation")
BASE_HDDLS = os.path.join(BASE, "hddl_s_sw_validation")
BASE_HDDLL = os.path.join(BASE, "hddl_l_sw_validation")
BASE_IOP = os.path.join(BASE, "IOP")


class AppUi(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("HDDL Sanity Test")
        # if os.name == "posix":
        #     self.__center(680, 720)
        # else:
        #     self.__center(620, 790)
        self.master.resizable(width=0, height=0)
        self.create_widgets()

    def __center(self, width, height):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        ww = width
        wh = height
        x = int((sw - ww) / 2)
        y = int((sh - wh) / 2)
        self.master.geometry("{}x{}+{}+{}".format(ww, wh, x, y))

    @staticmethod
    def __create_tab(control, text, state="normal"):
        tab = ttk.Frame(control)
        control.add(tab, text=text, state=state)
        return tab

    @staticmethod
    def __mod_space(f, padx=0, pady=0, ipadx=0, ipady=0):
        for child in f.winfo_children():
            child.grid_configure(padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

    def create_widgets(self):
        top = self.winfo_toplevel()

        # 创建分页frame
        frame_top = ttk.Frame(top)
        frame_top.grid(column=0, row=0)

        # 创建分页
        self.tab_control = ttk.Notebook(frame_top)

        tab1 = self.__create_tab(self.tab_control, "HDDL-R")
        tab2 = self.__create_tab(self.tab_control, "HDDL-S")
        tab3 = self.__create_tab(self.tab_control, "HDDL-L")
        tab4 = self.__create_tab(self.tab_control, "IOP")

        self.tab_control.grid(column=0, row=0)

        # ========================tab1分页的frame==========================
        hddl_r = ttk.Frame(tab1)
        hddl_r.grid(column=0, row=0, pady=10)

        # tab1下的Configuration
        cfg = ttk.Labelframe(hddl_r, text="Configuration")
        cfg.grid(column=0, row=0, sticky=tk.W)

        # Configuration中所有控件
        user_label = ttk.Label(cfg, text="User Name : ")
        user_label.grid(column=0, row=0, sticky=tk.W)

        self.user_entry = ttk.Entry(cfg, width=23)
        self.user_entry.grid(column=1, row=0)

        pw_label = ttk.Label(cfg, text="Password : ")
        pw_label.grid(column=2, row=0, sticky=tk.W)

        self.pw_entry = ttk.Entry(cfg, width=24)
        self.pw_entry.grid(column=3, row=0)

        # 调整Configuration中各个控件距离
        self.__mod_space(cfg, padx=5, pady=5)

        # tab1下的Component
        com = ttk.Labelframe(hddl_r, text='Components')
        com.grid(column=0, row=2)

        # Component中所有控件名称
        values = ["ALL", "OS&&Driver", "System Control", "Do Inference from HAL", "Do Inference from IE"]

        self.rad_list = []

        for col in range(5):
            cur_rad = ttk.Radiobutton(com, text=values[col], value=col)
            cur_rad.grid(row=0, column=col, sticky=tk.W)
            self.rad_list.append(cur_rad)

        # Custom component
        cus_rad = ttk.Radiobutton(com, text="Custom Component", value=5)
        cus_rad.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.rad_list.append(cus_rad)

        cus_label = ttk.Label(com, text="PATH : ")
        cus_label.grid(row=2, column=0, sticky=tk.W)

        self.cus_entry = ttk.Entry(com, width=47)
        self.cus_entry.grid(row=2, column=1, columnspan=3, sticky=tk.W)

        self.cus_btn = ttk.Button(com, text="Select")
        self.cus_btn.grid(row=2, column=4, sticky=tk.W)

        cus_pat_label = ttk.Label(com, text="Pattern : ")
        cus_pat_label.grid(row=3, column=0, sticky=tk.W)

        self.cus_pat_entry = ttk.Entry(com, width=47)
        self.cus_pat_entry.grid(row=3, column=1, columnspan=3, sticky=tk.W)

        if os.name == "nt":
            self.cus_entry.config(width=58)
            self.cus_pat_entry.config(width=58)

        self.cus_entry.config(state="disabled")
        self.cus_pat_entry.config(state="disabled")
        self.cus_btn.config(state="disabled")

        # 调整Component中各控件距离
        self.__mod_space(com, padx=5, pady=5)

        # 调整tab1分页中各控件距离
        self.__mod_space(hddl_r, padx=10, pady=10)
        # ========================tab1分页的frame==========================

        # ========================tab2分页的frame==========================
        hddl_s = ttk.Frame(tab2)
        hddl_s.grid(column=0, row=0, pady=10)

        # tab2下的component
        com2 = ttk.Labelframe(hddl_s, text="Components")
        com2.grid(column=0, row=0)

        # Component中所有控件名称
        values2 = ["ALL", "Linux OS", "GStreamer And Plugin", "Remote Controller", "Custom Component"]

        self.rad_list2 = []

        for col in range(5):
            cur_rad2 = ttk.Radiobutton(com2, text=values2[col], value=col)
            cur_rad2.grid(row=0, column=col, sticky=tk.W)
            self.rad_list2.append(cur_rad2)

        cus_label2 = ttk.Label(com2, text="PATH : ")
        cus_label2.grid(row=1, column=0, sticky=tk.W)

        self.cus_entry2 = ttk.Entry(com2, width=47)
        self.cus_entry2.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        self.cus_btn2 = ttk.Button(com2, text="Select")
        self.cus_btn2.grid(row=1, column=4, sticky=tk.W)

        cus_pat_label2 = ttk.Label(com2, text="Pattern : ")
        cus_pat_label2.grid(row=2, column=0, sticky=tk.W)

        self.cus_pat_entry2 = ttk.Entry(com2, width=47)
        self.cus_pat_entry2.grid(row=2, column=1, columnspan=3, sticky=tk.W)

        if os.name == "nt":
            self.cus_entry2.config(width=58)
            self.cus_pat_entry2.config(width=58)

        self.cus_entry2.config(state="disabled")
        self.cus_pat_entry2.config(state="disabled")
        self.cus_btn2.config(state="disabled")

        # 调整Component中各控件距离
        self.__mod_space(com2, padx=5, pady=20)

        # 调整tab2分页中各控件距离
        self.__mod_space(hddl_s, padx=20, pady=10)
        # ========================tab2分页的frame==========================

        # ========================tab3分页的frame==========================
        hddl_l = ttk.Frame(tab3)
        hddl_l.grid(column=0, row=0, pady=10)

        # tab3下的Configuration
        cfg3 = ttk.Labelframe(hddl_l, text="Configuration")
        cfg3.grid(column=0, row=0, sticky=tk.W)

        # Configuration中所有控件
        user_label3 = ttk.Label(cfg3, text="User Name : ")
        user_label3.grid(column=0, row=0)

        self.user_entry3 = ttk.Entry(cfg3, width=23)
        self.user_entry3.grid(column=1, row=0)

        pw_label3 = ttk.Label(cfg3, text="Password : ")
        pw_label3.grid(column=2, row=0)

        self.pw_entry3 = ttk.Entry(cfg3, width=24)
        self.pw_entry3.grid(column=3, row=0)

        # 调整Configuration中各个控件距离
        self.__mod_space(cfg3, padx=5, pady=5)

        # tab3下的Component
        com3 = ttk.Labelframe(hddl_l, text='Components')
        com3.grid(column=0, row=1)

        # Component中所有控件名称
        values = ["ALL", "OS&&Driver", "System Control", "Do Inference from HAL", "Do Inference from IE"]

        self.rad_list3 = []

        for col in range(5):
            cur_rad3 = ttk.Radiobutton(com3, text=values[col], value=col)
            cur_rad3.grid(row=0, column=col, sticky=tk.W)
            self.rad_list3.append(cur_rad3)

        # Custom component
        cus_rad3 = ttk.Radiobutton(com3, text="Custom Component", value=5)
        cus_rad3.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.rad_list3.append(cus_rad3)

        cus_label3 = ttk.Label(com3, text="PATH : ")
        cus_label3.grid(row=2, column=0, sticky=tk.W)

        self.cus_entry3 = ttk.Entry(com3, width=47)
        self.cus_entry3.grid(row=2, column=1, columnspan=3, sticky=tk.W)

        self.cus_btn3 = ttk.Button(com3, text="Select")
        self.cus_btn3.grid(row=2, column=4, sticky=tk.W)

        cus_pat_label3 = ttk.Label(com3, text="Pattern : ")
        cus_pat_label3.grid(row=3, column=0, sticky=tk.W)

        self.cus_pat_entry3 = ttk.Entry(com3, width=47)
        self.cus_pat_entry3.grid(row=3, column=1, columnspan=3, sticky=tk.W)

        if os.name == "nt":
            self.cus_entry3.config(width=58)
            self.cus_pat_entry3.config(width=58)

        self.cus_entry3.config(state="disabled")
        self.cus_pat_entry3.config(state="disabled")
        self.cus_btn3.config(state="disabled")

        # 调整Component中各控件距离
        self.__mod_space(com3, padx=5, pady=5)

        # 调整tab3分页中各控件距离
        self.__mod_space(hddl_l, padx=10, pady=10)
        # ========================tab3分页的frame==========================

        # ========================tab4分页的frame==========================
        iop = ttk.Frame(tab4)
        iop.grid(column=0, row=0, pady=10)

        # tab4下的Configuration
        cfg4 = ttk.Labelframe(iop, text="Configuration")
        cfg4.grid(column=0, row=0, sticky=tk.W)

        # Configuration中所有控件
        user_label4 = ttk.Label(cfg4, text="User Name : ")
        user_label4.grid(column=0, row=0, stick=tk.W)

        self.user_entry4 = ttk.Entry(cfg4, width=23)
        self.user_entry4.grid(column=1, row=0)

        pw_label4 = ttk.Label(cfg4, text="Password : ")
        pw_label4.grid(column=2, row=0, sticky=tk.W)

        self.pw_entry4 = ttk.Entry(cfg4, width=24)
        self.pw_entry4.grid(column=3, row=0)

        card_type4 = ttk.Label(cfg4, text="Card Type : ")
        card_type4.grid(column=0, row=1, sticky=tk.W)

        card_type_values = ["RVP", "UZEL", "IEI"]

        self.card_combobox4 = ttk.Combobox(cfg4, value=card_type_values)
        self.card_combobox4.grid(column=1, row=1)

        device_num4 = ttk.Label(cfg4, text="Device Number : ")
        device_num4.grid(column=2, row=1, sticky=tk.W)

        self.card_entry4 = ttk.Entry(cfg4, width=24)
        self.card_entry4.grid(column=3, row=1)

        # 调整Configuration中各个控件距离
        self.__mod_space(cfg4, padx=5, pady=5)

        # tab4下的Component
        com4 = ttk.Labelframe(iop, text='Components')
        com4.grid(column=0, row=1)

        # Component中所有控件名称
        values = ["ALL", "OS&&Driver", "System Control", "Do Inference from IE", "Test all of POR's Open CNN"]

        self.rad_list4 = []

        for col in range(5):
            cur_rad4 = ttk.Radiobutton(com4, text=values[col], value=col)
            cur_rad4.grid(row=0, column=col, sticky=tk.W)
            self.rad_list4.append(cur_rad4)

        # Custom component
        cus_rad4 = ttk.Radiobutton(com4, text="Custom Component", value=5)
        cus_rad4.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.rad_list4.append(cus_rad4)

        cus_label4 = ttk.Label(com4, text="PATH : ")
        cus_label4.grid(row=2, column=0, sticky=tk.W)

        self.cus_entry4 = ttk.Entry(com4, width=47)
        self.cus_entry4.grid(row=2, column=1, columnspan=3, sticky=tk.W)

        self.cus_btn4 = ttk.Button(com4, text="Select")
        self.cus_btn4.grid(row=2, column=4, sticky=tk.W)

        cus_pat_label4 = ttk.Label(com4, text="Pattern : ")
        cus_pat_label4.grid(row=3, column=0, sticky=tk.W)

        self.cus_pat_entry4 = ttk.Entry(com4, width=47)
        self.cus_pat_entry4.grid(row=3, column=1, columnspan=3, sticky=tk.W)

        if os.name == "nt":
            self.cus_entry4.config(width=58)
            self.cus_pat_entry4.config(width=58)

        self.cus_entry4.config(state="disabled")
        self.cus_pat_entry4.config(state="disabled")
        self.cus_btn4.config(state="disabled")

        # 调整Component中各控件距离
        self.__mod_space(com4, padx=5, pady=5)

        # 调整tab4分页中各控件距离
        self.__mod_space(iop, padx=10, pady=10)
        # ========================tab4分页的frame==========================

        # ========================按钮frame==========================
        frame_min = ttk.Frame(top)
        frame_min.grid(column=0, row=1)

        # start按钮
        self.sta_btn = ttk.Button(frame_min, text='Start')
        self.sta_btn.grid(column=0, row=1)

        # report按钮
        self.re_btn = ttk.Button(frame_min, text='Open Report')
        self.re_btn.grid(column=1, row=1)

        # exit按钮
        self.exit_btn = ttk.Button(frame_min, text='Exit')
        self.exit_btn.grid(column=2, row=1)

        # 调整按钮frame中控件距离
        self.__mod_space(frame_min, padx=65, pady=15)
        # ========================按钮frame==========================

        # ========================log frame==========================
        frame_bottom = ttk.Labelframe(top, text="Log Printer")
        frame_bottom.grid(column=0, row=2)

        # scrolledtext滚动文本框控件
        if os.name == 'posix':
            self.log_scr = scrolledtext.ScrolledText(frame_bottom, width=85, height=20, wrap=tk.WORD)
        else:
            self.log_scr = scrolledtext.ScrolledText(frame_bottom, width=77, height=20, wrap=tk.WORD)
        self.log_scr.pack()
        self.log_scr.config(state='disabled')

        # 调整log frame中控件距离
        self.__mod_space(frame_bottom, padx=10, pady=10, ipady=10, ipadx=10)
        # ========================log frame==========================

        # 调整整体frame中各控件距离
        if os.name == 'posix':
            self.__mod_space(top, pady=15, padx=12)
        else:
            self.__mod_space(top, pady=5, padx=10)


class App(AppUi):

    def __init__(self, master=None):
        AppUi.__init__(self, master)

        self.ret = None

        self.user_info_file1 = os.path.join(BASE_HDDLR, "user_info")
        self.user_info_file3 = os.path.join(BASE_HDDLL, "user_info")
        self.user_info_file4 = os.path.join(BASE_IOP, "info")

        # tab1 username输入框
        self.username = tk.StringVar()
        self.user_entry['textvariable'] = self.username

        # tab1 password输入框
        self.password = tk.StringVar()
        self.pw_entry['textvariable'] = self.password

        # tab1 component值
        # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from HAL", 4:"Do Inference from IE", 5: "Custom"
        self.component_value = tk.IntVar()
        self.component_value.set(0)
        for item in self.rad_list:
            item['variable'] = self.component_value
            item['command'] = lambda: self.__set_state(self.component_value.get(), self.cus_entry, self.cus_btn,
                                                       self.cus_pat_entry)

        # tab1 path值
        self.path = tk.StringVar()
        self.cus_entry["textvariable"] = self.path

        # tab1 select 按钮
        self.cus_btn['command'] = lambda: self.__select_dir(self.path)

        # tab1 pattern值
        self.pattern = tk.StringVar()
        self.cus_pat_entry['textvariable'] = self.pattern

        # tab2 component值
        # 0:"ALL",  1:"Linux OS",   2:"GStreamer And Plugin",   3:"Remote Controller",  4:"Custom Component"
        self.com2_value = tk.IntVar()
        self.com2_value.set(0)
        for item in self.rad_list2:
            item['variable'] = self.com2_value
            item['command'] = lambda: self.__set_state(self.com2_value.get(), self.cus_entry2, self.cus_btn2,
                                                       self.cus_pat_entry2)

        # tab2 path
        self.path2 = tk.StringVar()
        self.cus_entry2['textvariable'] = self.path2

        # tab2 select button
        self.cus_btn2['command'] = lambda: self.__select_dir(self.path2)

        # tab2 pattern
        self.pattern2 = tk.StringVar()
        self.cus_pat_entry2['textvariable'] = self.pattern2

        # tab3 username输入框
        self.username3 = tk.StringVar()
        self.user_entry3['textvariable'] = self.username3

        # tab3 password输入框
        self.password3 = tk.StringVar()
        self.pw_entry3['textvariable'] = self.password3

        # tab3 component值
        # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from HAL", 4:"Do Inference from IE", 5: "Custom"
        self.component_value3 = tk.IntVar()
        self.component_value3.set(0)
        for item in self.rad_list3:
            item['variable'] = self.component_value3
            item['command'] = lambda: self.__set_state(self.component_value3.get(), self.cus_entry3, self.cus_btn3,
                                                       self.cus_pat_entry3)

        # tab3 path值
        self.path3 = tk.StringVar()
        self.cus_entry3["textvariable"] = self.path3

        # tab3 select 按钮
        self.cus_btn3['command'] = lambda: self.__select_dir(self.path3)

        # tab3 pattern值
        self.pattern3 = tk.StringVar()
        self.cus_pat_entry3['textvariable'] = self.pattern3

        # tab4 username输入框
        self.username4 = tk.StringVar()
        self.user_entry4['textvariable'] = self.username4

        # tab4 password输入框
        self.password4 = tk.StringVar()
        self.pw_entry4['textvariable'] = self.password4

        # tab4 card type
        self.type_value4 = tk.StringVar()
        self.card_combobox4['textvariable'] = self.type_value4
        self.card_combobox4.current(0)
        self.card_combobox4.bind("<<ComboboxSelected>>", self.fun)
        self.card_t = None

        # tab4 device num
        self.d_num = tk.StringVar()
        self.card_entry4['textvariable'] = self.d_num

        # tab4 component值
        # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from IE", 4:"Test all of POR's Open CNN", 5: "Custom"
        self.component_value4 = tk.IntVar()
        self.component_value4.set(0)
        for item in self.rad_list4:
            item['variable'] = self.component_value4
            item['command'] = lambda: self.__set_state(self.component_value4.get(), self.cus_entry4, self.cus_btn4,
                                                       self.cus_pat_entry4)

        # tab4 path值
        self.path4 = tk.StringVar()
        self.cus_entry4["textvariable"] = self.path4

        # tab4 select 按钮
        self.cus_btn4['command'] = lambda: self.__select_dir(self.path4)

        # tab4 pattern值
        self.pattern4 = tk.StringVar()
        self.cus_pat_entry4['textvariable'] = self.pattern4

        # start按钮
        self.sta_btn['command'] = self.start

        # Open Report按钮
        self.re_btn['command'] = self.report

        # Exit按钮
        self.exit_btn['command'] = self.exit

        if os.name == "nt":
            self.user_entry.config(state="disabled")
            self.pw_entry.config(state="disabled")
            self.user_entry3.config(state="disabled")
            self.pw_entry3.config(state="disabled")
            self.user_entry4.config(state="disabled")
            self.pw_entry4.config(state="disabled")

        self.__read_u_p(self.user_info_file1, self.username, self.password)
        self.__read_u_p(self.user_info_file3, self.username3, self.password3)
        self.__read_u_p(self.user_info_file4, self.username4, self.password4, self.d_num)

    def fun(self, *args):
        self.card_t = self.type_value4.get()

    def start(self):
        if self.ret:
            messagebox.showwarning(title="Warnning", message="Is running...")
        else:
            cmd = []
            self.__clear_log()
            # 0:"HDDL-R"    1:"HDDL-S"  2:"HDDL-L"      3: "IOP"
            self.current_tab = self.tab_control.index("current")
            if self.current_tab == 0:
                un = self.username.get()
                pw = self.password.get()
                # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from HAL", 4:"Do Inference from IE",
                #  5:"custom"
                component_index = str(self.component_value.get())
                main_file = os.path.join(BASE_HDDLR, "main.py")
                path_value = self.cus_entry.get()
                pat_value = self.cus_pat_entry.get()
                cmd = self.__get_cmd(un, pw, component_index, main_file, path_value, pat_value)
            elif self.current_tab == 1:
                # 0:"ALL",  1:"Linux OS",   2:"GStreamer And Plugin",   3:"Remote Controller",  4:"Custom Component"
                com2_index = str(self.com2_value.get())
                main_file = os.path.join(BASE_HDDLS, "main.py")
                cmd = [main_file, com2_index]
                if com2_index == "4":
                    path_value = self.cus_entry2.get()
                    pat_value = self.cus_pat_entry2.get()
                    if path_value and pat_value:
                        cmd = cmd + [path_value, pat_value]
                    else:
                        messagebox.showerror(title="Error", message="Please input the Path and Pattern for your case!")
                        return 0
            elif self.current_tab == 2:
                un = self.username3.get()
                pw = self.password3.get()
                # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from HAL", 4:"Do Inference from IE",
                #  5:"custom"
                component_index = str(self.component_value3.get())
                main_file = os.path.join(BASE_HDDLL, "main.py")
                path_value = self.cus_entry3.get()
                pat_value = self.cus_pat_entry3.get()
                cmd = self.__get_cmd(un, pw, component_index, main_file, path_value, pat_value)
            elif self.current_tab == 3:
                if not self.card_t:
                    self.card_t = "RVP"
                d_num = self.card_entry4.get()
                if not d_num:
                    d_num = "8"
                un = self.username4.get()
                pw = self.password4.get()
                # 0:"ALL", 1:"OS&&Driver", 2:"System Control", 3:"Do Inference from IE", 4:"Test all of POR's Open CNN"
                #  5:"custom"
                component_index = str(self.component_value4.get())
                main_file = os.path.join(BASE_IOP, "main.py")
                path_value = self.cus_entry4.get()
                pat_value = self.cus_pat_entry4.get()
                cmd = self.__get_cmd(un, pw, component_index, main_file, path_value, pat_value, self.card_t, d_num)
            self.__run(cmd)

    def report(self):

        try:
            report_file = "output{}report.html".format(os.sep)
            if not self.ret:
                if os.path.exists(report_file):
                    if os.name == "posix":
                        os.popen("firefox {}".format(report_file))
                    else:
                        os.popen("start {}".format(report_file))
                else:
                    messagebox.showwarning(title="Warnning", message="Not found the test report...")
            else:
                messagebox.showwarning(title="Warnning", message="Test not completed...")
        except AttributeError:
            messagebox.showwarning(title="Warnning", message="Please test first...")

    def exit(self):
        res = messagebox.askokcancel("Info", "Are you sure to exit?")
        # exit
        if res:
            # save the username and password
            with open(self.user_info_file1, 'w') as f:
                content = self.username.get() + "\t" + self.password.get()
                f.write(content)
            with open(self.user_info_file3, 'w') as f:
                content = self.username3.get() + "\t" + self.password3.get()
                f.write(content)
            with open(self.user_info_file4, 'w') as f:
                content = self.username4.get() + "\t" + self.password4.get() + "\t" + self.card_entry4.get()
                f.write(content)
            if self.ret:
                self.ret.kill()
            self.master.destroy()
            sys.exit(0)

    @staticmethod
    def __select_dir(obj):
        _path = filedialog.askdirectory()
        obj.set(_path)

    @staticmethod
    def __set_state(com_value, entry, btn, pat_entry):
        value = com_value
        if value == 5:
            entry.config(state="readonly")
            btn.config(state="normal")
            pat_entry.config(state="normal")
        else:
            entry.config(state="disabled")
            btn.config(state="disabled")
            pat_entry.config(state="disabled")

    @staticmethod
    def __read_u_p(file, user_entry, pw_entry, card_entry=None):
        """
        read the username and password
        :return:
        """
        if os.path.exists(file):
            with open(file) as f:
                content = f.read()
            if content:
                username = content.split("\t")[0]
                password = content.split("\t")[1]
                try:
                    card_type = content.split("\t")[2]
                except IndexError as e:
                    pass
                else:
                    if card_entry:
                        card_entry.set(card_type)
                user_entry.set(username)
                pw_entry.set(password)

    def __run(self, cmd):
        self.__printer("{} : Start...\n\n".format(time.strftime("%H:%M:%S")))
        cmd = [sys.executable] + cmd
        self.ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
        t = threading.Thread(target=self.__process_stdout, args=(self.ret,), daemon=True)
        t.start()

    def __process_stdout(self, ret):
        while ret.poll() is None:
            log = ret.stdout.readline().decode("utf-8")
            self.__printer(log=log)
            time.sleep(0.5)
        else:
            self.__printer("\n{} : End...\n\n".format(time.strftime("%H:%M:%S")))
            self.ret = None

    @staticmethod
    def __get_cmd(user_object, pw_object, com_index, main_file, path_value, pat_value, c_type=None, d_num=None):
        un = user_object
        pw = pw_object
        component_index = str(com_index)
        main_file = main_file
        cmd = [main_file, component_index, un, pw]
        if c_type and d_num:
            cmd += [c_type, d_num]
        if component_index == "5":
            path_value = path_value
            pat_value = pat_value
            if path_value and pat_value:
                cmd = cmd + [path_value, pat_value]
            else:
                messagebox.showerror(title="Error", message="Please input the Path and Pattern for your case!")
                return 0
        return cmd

    def __printer(self, log):
        self.log_scr.config(state='normal')
        self.log_scr.insert(tk.END, log)
        self.log_scr.see(tk.END)
        self.log_scr.update()
        self.log_scr.config(state='disabled')

    def __clear_log(self):
        self.log_scr.config(state='normal')
        self.log_scr.delete(1.0, tk.END)
        self.log_scr.see(tk.END)
        self.log_scr.update()
        self.log_scr.config(state='disabled')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
