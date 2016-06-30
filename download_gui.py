import tkMessageBox
from Tkinter import *

class DownloadGui(Toplevel):

    def __init__(self, parent, controller, folders_dictionary):
        Toplevel.__init__(self, parent)
        self.controller = controller
        self.transient(parent)
        self.parent = parent
        body = Frame(self)
        self.create_window()
        self.galleries_dictionary = folders_dictionary
        self.galleries_list = folders_dictionary.keys()
        self.create_body(body, self.galleries_list)
        body.pack()
        self.wait_window(self)

    def create_window(self):
        self.grab_set()
        self.title("Download Gallery")
        self.geometry("340x190")
        self.resizable(width=False, height=False)
        self.iconbitmap('images/icon.ico')
        self.protocol('WM_DELETE_WINDOW', lambda: self.exit_action())

    def create_body(self, body, folders_list):
        frame = LabelFrame(body, text="Download Gallery:")
        frame.pack(side=TOP, fill=BOTH, pady=5, padx=5)
        frame_buttons = Frame(frame)

        label_info = Label(frame, justify=LEFT, wraplength=320,
                           text="From here you can download content of your SecureCloud galery to your computer.")
        label_gallery = Label(frame, text="Choose Gallery:")

        gallery_chosen = StringVar(frame)
        gallery_chosen.set(folders_list[0])
        cloud_value = apply(OptionMenu, (frame, gallery_chosen) + tuple(folders_list))

        button_ok = Button(frame_buttons, text="Download", width=17, height=1 ,command=lambda: self.prepare_download(gallery_chosen))
        button_cancel = Button(frame_buttons, text="Cancel", width=12, height=1 ,command=lambda: self.exit_action())

        cloud_value.configure(width=28)
        cloud_value.configure(justify=LEFT)
        cloud_value.configure(anchor=W)

        label_info.grid(row=0, column=0, padx=5, columnspan=2)
        label_gallery.grid(row=1, column=0, padx=1, pady=(25,5))
        cloud_value.grid(row=1, column=1, pady=(25,5))

        frame_buttons.grid(row=2, column=0, sticky=E, columnspan=2, pady=(25,15))
        button_ok.pack(side=RIGHT, anchor=E, padx=8)
        button_cancel.pack(side=RIGHT, anchor=E, padx=8)

    def exit_action(self):
        self.destroy()

    def prepare_download(self, gallery_chosen):
        key = gallery_chosen.get()
        value = self.galleries_dictionary[key]
        self.destroy()
        self.controller.download_action(value)
