from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import os
import re

from django.core.serializers.xml_serializer import EntitiesForbidden

from messages import Msg


class Gui:

    def __init__(self, root, controller, model):
        self.controller=controller
        self.model=model
        self.root = root
        self.files_list = lambda: None
        self.files_selected_list = lambda: None
        self.print_status = lambda: None
        self.print_files = lambda: None
        self.print_selected = lambda: None
        self.path_type = 0
        self.files_selected_list = []
        self.encoding_value = 0
        self.drive_value = 0
        self.location_enabled = False
        self.location_value = 0
        self.button_location = 0

        self.create_window(root)
        self.create_status_bar(root)
        self.create_menu_bar(root)
        self.create_panels(root)

    def create_window(self, root):
        root.title("Secure Cloud - Secure uploader")
        root.geometry("400x440")
        root.minsize(width=400, height=440)
        root.iconbitmap('images/icon.ico')
        root.protocol('WM_DELETE_WINDOW', lambda:self.exit_action())

    def create_status_bar(self, root):
        status_bar = Frame(root, height=25)
        status_bar.pack(side=BOTTOM, fill=BOTH)

        self.print_status = StringVar()
        self.print_files = StringVar()
        self.print_selected = StringVar()

        label_status = Label(status_bar, width=15, textvariable=self.print_status, relief=RIDGE)#SUNKEN
        label_files = Label(status_bar, width=15, textvariable=self.print_files, relief=RIDGE)
        label_users = Label(status_bar, width=15, textvariable=self.print_selected, relief=RIDGE)
        label_status.pack(side=LEFT, fill=X, expand=1)
        label_files.pack(side=LEFT, fill=X, expand=1)
        label_users.pack(side=LEFT, fill=X, expand=1)

        value_status = "Status: Ready"
        value_files = "Added Files: (no files)"
        value_selected = "Selected files: (no files)"
        self.print_status.set(value_status)
        self.print_files.set(value_files)
        self.print_selected.set(value_selected)

    def create_menu_bar(self, root):
        menu_bar = Menu(root)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Add Folder", command=lambda:self.controller.add_folder_action())
        file_menu.add_command(label="Add File", command=lambda:self.controller.add_file_action())
        file_menu.add_separator()
        file_menu.add_command(label="Remove Selected File/Files", command=lambda:self.controller.remove_file_action(self.files_selected_list))
        file_menu.add_command(label="Clear Files List", command=lambda:self.controller.clear_all_action())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda:self.exit_action())
        menu_bar.add_cascade(label="File", menu=file_menu)

        value_var = IntVar()
        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_radiobutton(label="Show Full Path", var=value_var, value=1, command=lambda: self.set_path_type(0))
        view_menu.add_radiobutton(label="Show Folder And File Name", var=value_var, value=2, command=lambda: self.set_path_type(1))
        view_menu.add_radiobutton(label="Show File Name", var=value_var, value=3, command=lambda: self.set_path_type(2))
        value_var.set(1)
        menu_bar.add_cascade(label="View", menu=view_menu)

        account_menu = Menu(menu_bar, tearoff=0)
        account_menu.add_command(label="Change/Set Location", command=lambda: self.update_location())
        menu_bar.add_cascade(label="Account", menu=account_menu)

        action_menu = Menu(menu_bar, tearoff=0)
        action_menu.add_command(label="Encrypt and Upload", command=lambda: self.check_start_action())
        action_menu.add_command(label="Download and Decrypt", command=lambda: self.controller.open_download(self.drive_value.get()))
        menu_bar.add_cascade(label="Action", menu=action_menu)

        root.config(menu=menu_bar)

    def create_panels(self, root):
        frame = Frame(root, height=100)
        frame.pack(side=TOP, fill=BOTH, padx=5, pady=5)

        frame_cloud = self.create_cloud_panel(frame)
        frame_files = self.create_files_panel(frame)
        frame_action = self.create_action_panel(frame)

        frame_action.pack(side=BOTTOM, fill=BOTH, pady=2)
        frame_cloud.pack(side=TOP, fill=BOTH, pady=(0,2))
        frame_files.pack(side=TOP, fill=BOTH, pady=2)

    def create_cloud_panel(self, frame):
        frame_cloud = LabelFrame(frame, text="Cloud account:")
        frame_cloud_button = Frame(frame_cloud)
        frame_cloud_data = Frame(frame_cloud)
        frame_cloud_button.pack(side=RIGHT, fill=BOTH, pady=0)
        frame_cloud_data.pack(side=LEFT, fill=BOTH, expand=1)

        label_cloud = Label(frame_cloud_data, anchor=W, text="Cloud name: ")
        label_location = Label(frame_cloud_data, anchor=W, text="Upload folder: ")

        self.drive_value = StringVar(frame_cloud_data)
        self.drive_value.set("Google Drive")
        cloud_value = OptionMenu(frame_cloud_data, self.drive_value, "Google Drive", "Dropbox", "One Drive")
        self.location_value = Entry(frame_cloud_data, text="Secure-Folder", width=50)
        self.location_value.insert(10,"Secure-Folder")
        self.location_value.configure(state='readonly')

        label_cloud.grid(row=0, column=0, pady=5, padx=5, sticky=W)
        cloud_value.grid(row=0, column=1, pady=5, padx=0, sticky=W)
        label_location.grid(row=1, column=0, pady=(5,15), padx=5, sticky=W)
        self.location_value.grid(row=1, column=1, pady=(5,10), padx=2, sticky=W)

        self.button_location = Button(frame_cloud_button, text="Change folder", width=12, height=1, command=lambda: self.update_location())
        self.button_location.pack(side=BOTTOM, pady=10, padx=10)

        return frame_cloud

    def create_files_panel(self, frame):
        frame_files = LabelFrame(frame, text="Affected files:")
        frame_files_panel = Frame(frame_files)
        frame_files_buttons = Frame(frame_files)
        frame_files_panel.pack(side=LEFT, fill=BOTH, pady=(5,10), expand=1)
        frame_files_buttons.pack(side=RIGHT, fill=BOTH, pady=5)

        files_list_scroll = Scrollbar(frame_files_panel)
        files_list_scroll.pack(side=RIGHT, fill=BOTH)
        self.files_list = Listbox(frame_files_panel,height=1500, yscrollcommand=files_list_scroll.set, selectmode=EXTENDED)
        self.files_list.pack(side=LEFT, fill=BOTH, padx=(10,0), expand=1)
        self.files_list.bind("<<ListboxSelect>>",self.selection_list)
        self.files_list.insert(END, "(No files chosen)")
        files_list_scroll.config(command=self.files_list.yview)

        addfile = ImageTk.PhotoImage(file="images/addfile.png")
        addfold = ImageTk.PhotoImage(file="images/addfolder.png")
        remov = ImageTk.PhotoImage(file="images/remove.png")
        clear = ImageTk.PhotoImage(file="images/clear.png")
        button_add_folder = Button(frame_files_buttons, width=25, height=25, image=addfold, command=lambda:self.controller.add_folder_action())
        button_add_file = Button(frame_files_buttons, width=25, height=25, image=addfile, command=lambda:self.controller.add_file_action())
        button_remove_file = Button(frame_files_buttons, width=25, height=25, image=remov, command=lambda:self.controller.remove_file_action(self.files_selected_list))
        button_clear_all = Button(frame_files_buttons, width=25, height=25, image=clear, command=lambda:self.controller.clear_all_action())
        button_add_folder.image = addfold
        button_add_file.image = addfile
        button_remove_file.image = remov
        button_clear_all.image = clear

        button_add_file.pack(side=TOP, pady=(0,5), padx=(15,10))
        button_add_folder.pack(side=TOP, pady=5, padx=(15,10))
        button_clear_all.pack(side=BOTTOM, pady=5, padx=(15,10))
        button_remove_file.pack(side=BOTTOM, pady=5, padx=(15,10))
        return frame_files

    def create_action_panel(self, frame):
        frame_action = LabelFrame(frame, text="Actions:")
        frame_action_up = Frame(frame_action)
        frame_action_up.pack(anchor=W)
        frame_action_down = Frame(frame_action)
        frame_action_down.pack(anchor=E)

        label_crypto = Label(frame_action_up, anchor=W, text="Encryption type: ")

        self.encoding_value = IntVar()
        radiobutton1 = Radiobutton(frame_action_up, text="For storing", variable=self.encoding_value, value=1)
        radiobutton2 = Radiobutton(frame_action_up, text="For preview", variable=self.encoding_value, value=2)
        self.encoding_value.set(1)

        button_download = Button(frame_action_down, text="Download and Decrypt", width=18, height=1, command=lambda: self.controller.open_download(self.drive_value.get()))
        button_start = Button(frame_action_down, text="Encrypt and Upload", width=18, height=1, command=lambda: self.check_start_action())

        label_crypto.pack(side=LEFT, pady=(5,10), padx=5)
        radiobutton1.pack(side=LEFT)
        radiobutton2.pack(side=LEFT)

        button_start.pack(side=RIGHT, pady=(5, 10), padx=(10, 10))
        button_download.pack(side=LEFT, pady=(5, 10), padx=5)
        return frame_action

############################## FUNKCIJE ##############################

    def update_list(self):
        self.files_list.delete(0, END)
        self.selection_list(Event())

        if len(self.model.opened_files) == 0:
            value_files = "Added Files: (no files)"
            self.files_list.insert(END, "(no files choosen)")
        else:
            value_files = "Added Files: "+str(len(self.model.opened_files))
            for file in self.model.opened_files:
                ### prikazivanje velicine fajla
                file_size_kb = os.path.getsize(file)/1024.0
                if file_size_kb > 1024.0:
                    file_size=file_size_kb/1024.0
                    file_size_string = " ("+str("%.2f" % file_size)+" MB)"
                else:
                    file_size_string = " ("+str("%.2f" % file_size_kb)+" KB)"
                ### nacin prikazivanja putanje
                if self.path_type == 0:
                    write_file=file
                elif self.path_type == 1:
                    write_file = os.path.join(os.path.split(os.path.split(file)[0])[1],os.path.basename(file))
                else:
                    write_file=os.path.basename(file)
                ### konacan prikaz podataka o fajlu
                self.files_list.insert(END, write_file+file_size_string)
        self.print_files.set(value_files)

    def selection_list(self, event):
        if len(self.model.opened_files) == 0:
            self.files_selected_list = []
            self.print_selected.set("Selected files: (no files)")
        else:
            self.files_selected_list = self.files_list.curselection()
            self.print_selected.set("Selected files: "+str(len(self.files_selected_list)))

    def set_path_type(self, type):
        self.path_type=type
        self.update_list()

    def create_start_action(self):
        self.controller.start_action(self.drive_value.get(), self.encoding_value.get(), self.location_value.get())

    def update_location(self):
        if self.location_enabled:
            location = self.location_value.get()
            pattern = re.compile("^([A-Za-z0-9\-\_])+$")
            if pattern.match(location):
                self.location_value.configure(state='readonly')
                self.location_enabled = False
                self.button_location.configure(text="Change Folder")
            else:
                tkMessageBox.showerror(Msg.naming_folder_error_title, Msg.naming_folder_error_message)
        else:
            self.location_value.configure(state='normal')
            self.location_enabled = True
            self.button_location.configure(text="Set folder")

    def check_start_action(self):
        if self.location_enabled:
            tkMessageBox.showerror(Msg.naming_folder_missing_title, Msg.naming_folder_missing_message)
        else:
            self.create_start_action()

    def exit_action(self):
        if tkMessageBox.askokcancel(Msg.quit_application_title, Msg.quit_application_message):
            self.root.destroy()
