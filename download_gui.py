import tkMessageBox
from Tkinter import *

class DownloadGui:

    def __init__(self, controller, folders_dictionary):
        self.root=Tk()
        self.controller=controller
        self.galleries_dictionary=folders_dictionary
        self.galleries_list = folders_dictionary.keys()
        self.create_window()
        if self.check_folders(folders_dictionary):
            self.exit_action()
        self.create_body(self.galleries_list)

    def create_window(self):
        self.root.grab_set_global()
        self.root.title("Download Gallery")
        self.root.geometry("340x190")
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap('images/icon.ico')
        self.root.protocol('WM_DELETE_WINDOW', lambda: self.exit_action())

    def create_body(self, folders_list):
        frame = LabelFrame(self.root, text="Download Gallery:")
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
        self.root.destroy()

    def prepare_download(self, gallery_chosen):
        key = gallery_chosen.get()
        value = self.galleries_dictionary[key]
        self.root.destroy()
        self.controller.download_action(value)

    def check_folders(self, folders_dictionary):
        if len(folders_dictionary) == 0:
            tkMessageBox.showinfo("No Available Galleries","You have no galleries that could be downloaded!\n"
                                "Please try with another account, or create gallery with this.")
            return True
        else:
            return False
