from Tkinter import *

class DownloadGui:

    def __init__(self, folders_list):
        self.root=Tk()
        self.create_window()
        self.create_body(folders_list)
        self.gallery_chosen=""

    def create_window(self):
        self.root.grab_set_global()
        self.root.title("Download Gallery")
        self.root.geometry("340x190")
        self.root.resizable(width=False, height=False)
        self.root.iconbitmap('images/icon.ico')

    def create_body(self, folders_list):
        frame = LabelFrame(self.root, text="Download Gallery:")
        frame.pack(side=TOP, fill=BOTH, pady=5, padx=5)
        frame_buttons = Frame(frame)

        label_info = Label(frame, justify=LEFT, wraplength=320,
                           text="From here you can download content of your SecureCloud galery to your computer.")
        label_gallery = Label(frame, text="Choose Gallery:")
        button_ok = Button(frame_buttons, text="Download", width=17, height=1 ,command=lambda: self.download_action())
        button_cancel = Button(frame_buttons, text="Cancel", width=12, height=1 ,command=lambda: self.exit_action())

        self.gallery_chosen = StringVar(frame)
        self.gallery_chosen.set(folders_list[0])
        cloud_value = apply(OptionMenu, (frame, self.gallery_chosen) + tuple(folders_list))
        cloud_value.configure(width=28)
        cloud_value.configure(justify=LEFT)
        cloud_value.configure(anchor=W)

        label_info.grid(row=0, column=0, padx=5, columnspan=2)
        label_gallery.grid(row=1, column=0, padx=1, pady=(25,5))
        cloud_value.grid(row=1, column=1, pady=(25,5))

        frame_buttons.grid(row=2, column=0, sticky=E, columnspan=2, pady=(25,15))
        button_ok.pack(side=RIGHT,anchor=E, padx=8)
        button_cancel.pack(side=RIGHT,anchor=E, padx=8)


    def exit_action(self):
        self.root.destroy()

    def download_action(self):
        print "tu je"