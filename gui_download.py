import tkFileDialog
import tkMessageBox
from Tkinter import *

from messages import Msg


class DownloadGui(Toplevel):

    def __init__(self, parent, controller, folders_dictionary):
        Toplevel.__init__(self, parent)
        self.controller = controller
        self.download_path=""
        self.location_value = ""
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
        self.geometry("340x212")
        self.resizable(width=False, height=False)
        self.iconbitmap('images/icon.ico')
        self.protocol('WM_DELETE_WINDOW', lambda: self.exit_action())

    def create_body(self, body, folders_list):
        frame = LabelFrame(body, text="Download Gallery:")
        frame.pack(side=TOP, fill=BOTH, pady=5, padx=5)
        frame_buttons = Frame(frame)
        frame_gallery = Frame(frame)
        frame_location = Frame(frame)

        label_info = Label(frame, justify=LEFT, wraplength=320, text=Msg.dialog_download_explanation)
        label_gallery = Label(frame_gallery, text="Choose gallery:")
        label_location = Label(frame_location, text="Download loc:")

        gallery_chosen = StringVar(frame)
        gallery_chosen.set(folders_list[0])
        cloud_value = apply(OptionMenu, (frame_gallery, gallery_chosen) + tuple(folders_list))
        self.location_value = Entry(frame_location, width=30)

        button_ok = Button(frame_buttons, text="Download", width=17, height=1 ,command=lambda: self.prepare_download(gallery_chosen))
        button_cancel = Button(frame_buttons, text="Cancel", width=12, height=1 ,command=lambda: self.exit_action())
        button_location = Button(frame_location, text="...", width=2, height=1, command=lambda: self.choose_location())

        cloud_value.configure(width=30)
        cloud_value.configure(justify=LEFT)
        cloud_value.configure(anchor=W)

        label_info.grid(row=0, column=0, padx=5, columnspan=2)

        frame_gallery.grid(row=1, column=0, sticky=W, columnspan=2, pady=(15, 5))
        label_gallery.pack(side=LEFT, anchor=W, padx=4)
        cloud_value.pack(side=LEFT, anchor=W)

        frame_location.grid(row=2, column=0, sticky=W, columnspan=2, pady=10)
        label_location.pack(side=LEFT, anchor=W, padx=5)
        self.location_value.pack(side=LEFT, anchor=W, padx=5)
        button_location.pack(side=LEFT, anchor=W, padx=8)

        frame_buttons.grid(row=3, column=0, sticky=E, columnspan=2, pady=(10,15))
        button_ok.pack(side=RIGHT, anchor=E, padx=8)
        button_cancel.pack(side=RIGHT, anchor=E, padx=8)

    def choose_location(self):
        options = {}
        self.download_path = tkFileDialog.askdirectory(**options)
        self.location_value.insert(10,self.download_path)

    def exit_action(self):
        self.destroy()

    def prepare_download(self, gallery_chosen):
        if self.download_path == "":
            tkMessageBox.showerror(Msg.location_missing_title, Msg.location_missing_message)
            return
        key = gallery_chosen.get()
        value = self.galleries_dictionary[key]
        self.destroy()
        self.controller.download_action(value, self.download_path)
