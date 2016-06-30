from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import os
import re

from django.core.serializers.xml_serializer import EntitiesForbidden


class Gui:

    @property
    def model(self):
        return self.__model

    @property
    def controller(self):
        return self.__controller

    @property
    def files_list(self):
        return self.__files_list

    @property
    def files_selected_list(self):
        return self.__files_selected_list

    @property
    def print_status(self):
        return self.__print_status

    @property
    def print_files(self):
        return self.__print_files

    @property
    def print_selected(self):
        return self.__print_selected

    @property
    def path_type(self):
        return self.__path_type

    encoding_value = 0
    drive_value = 0
    location_enabled = False
    label_location_value = 0
    button_location = 0

    _cloud_user_value="Pera9987"

    def __init__(self, root, controller, model):
        self.__controller=controller
        self.__model=model
        self.__path_type=0
        self.create_window(root)
        self.create_status_bar(root)
        self.create_menu_bar(root)
        self.create_panels(root)
        self.files_selected_list = []

    def create_window(self, root):
        root.title("Secure Clouding - Upload pictures")
        root.geometry("420x460")
        root.minsize(width=420, height=440)
        root.iconbitmap('images/icon.ico')
        root.protocol('WM_DELETE_WINDOW', lambda:self.controller.exit_action())

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
        file_menu.add_command(label="Exit", command=lambda:self.controller.exit_action())
        menu_bar.add_cascade(label="File", menu=file_menu)

        value_var = IntVar()
        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_radiobutton(label="Show Full Path", var=value_var, value=1, command=lambda: self.set_path_type(0))
        view_menu.add_radiobutton(label="Show Folder And File Name", var=value_var, value=2, command=lambda: self.set_path_type(1))
        view_menu.add_radiobutton(label="Show File Name", var=value_var, value=3, command=lambda: self.set_path_type(2))
        value_var.set(1)
        menu_bar.add_cascade(label="View", menu=view_menu)

        action_menu = Menu(menu_bar, tearoff=0)
        action_menu.add_command(label="Encrypt And Upload", command=lambda:self.check_start_action())
        action_menu.add_command(label="Cancel All", command=lambda:self.controller.cancel_all_action())
        menu_bar.add_cascade(label="Action", menu=action_menu)

        account_menu = Menu(menu_bar, tearoff=0)
        account_menu.add_command(label="Switch Cloud", command=lambda:self.controller.switch_account_action())
        account_menu.add_command(label="Change/Set Location", command=lambda: self.update_location())
        menu_bar.add_cascade(label="Account", menu=account_menu)

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
        frame_cloud_buttons = Frame(frame_cloud)
        frame_cloud_data = Frame(frame_cloud)
        frame_cloud_buttons.pack(side=RIGHT, fill=BOTH, pady=0)
        frame_cloud_data.pack(side=LEFT, fill=BOTH, expand=1)

        cloud_user = StringVar()
        cloud_location = StringVar()

        Gui.drive_value = StringVar(frame_cloud_data)
        Gui.drive_value.set("Google Drive")

        label_cloud = Label(frame_cloud_data, anchor=W, text="Cloud name: ")
        label_user = Label(frame_cloud_data, anchor=W, text="User name: ")
        label_location = Label(frame_cloud_data, anchor=W, text="Upload location: ")
        label_cloud_value = OptionMenu(frame_cloud_data, Gui.drive_value, "Google Drive", "Dropbox", "One Drive")
        label_user_value = Label(frame_cloud_data, anchor=W, textvariable=cloud_user)
        Gui.label_location_value = Entry(frame_cloud_data, text="secure-clouding", width=40)
        Gui.label_location_value.insert(10,"secure-clouding")
        Gui.label_location_value.configure(state='readonly')

        value_user = self._cloud_user_value
        cloud_user.set(value_user)

        button_switch = Button(frame_cloud_buttons, text="Switch Cloud", width=12, height=1)
        Gui.button_location = Button(frame_cloud_buttons, text="Change Location", width=12, height=1, command=lambda:self.update_location())

        label_cloud.grid(row=0, column=0, pady=(0,0), padx=5, sticky=W)
        label_user.grid(row=1, column=0, pady=3, padx=5, sticky=W)
        label_location.grid(row=2, column=0, pady=(6,10), padx=5, sticky=W)
        label_cloud_value.grid(row=0, column=1, pady=0, padx=0, sticky=W)
        label_user_value.grid(row=1, column=1, pady=3, padx=0, sticky=W)
        Gui.label_location_value.grid(row=2, column=1, pady=(6,10), padx=0, sticky=W)

        #button_switch.pack(side=BOTTOM, pady=(26,1), padx=10)
        #button_location.pack(side=BOTTOM, pady=(1,10), padx=10)
        Gui.button_location.pack(side=BOTTOM, pady=(30, 8), padx=10)

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
        frame_action_down = Frame(frame_action)

        label_crypto = Label(frame_action_up, anchor=W, text="Nacin kriptovanja: ")
        #label_process = Label(frame_action, width=15, textvariable=print_connection, relief=RIDGE)
        label_process = Label(frame_action_down, anchor=W, text="Encrypting and uploading.....uploadinguploadinguploadinguploadinguploading")

        Gui.encoding_value = IntVar()
        radiobutton1 = Radiobutton(frame_action_up, text="One", variable=Gui.encoding_value, value=1)
        radiobutton2 = Radiobutton(frame_action_up, text="Two", variable=Gui.encoding_value, value=2)
        Gui.encoding_value.set(1)

        button_cancel = Button(frame_action_down, text="Cancel", width=6, height=1, command=lambda:self.controller.cancel_all_action())
        button_start = Button(frame_action_down, text="Encrypt and Upload", width=18, height=1, command=lambda:self.check_start_action())

        frame_action_up.pack(anchor=W)
        frame_action_down.pack(anchor=E)
        label_crypto.pack(side=LEFT, pady=(5,10), padx=5)
        radiobutton1.pack(side=LEFT)
        radiobutton2.pack(side=LEFT)
        button_start.pack(side=RIGHT, pady=(5, 10), padx=(10, 10))
        button_cancel.pack(side=RIGHT, pady=(5, 10), padx=5)
        #label_process.pack(side=LEFT, expand=100, pady=(5,10), padx=5)
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
        self.controller.start_action(Gui.drive_value.get(), Gui.encoding_value.get(), Gui.label_location_value.get())

    def update_location(self):
        if (Gui.location_enabled):
            location = Gui.label_location_value.get()
            pattern = re.compile("^([A-Za-z0-9\-\_])+$")
            if pattern.match(location):
                Gui.label_location_value.configure(state='readonly')
                Gui.location_enabled = False
                Gui.button_location.configure(text="Change Location")
            else:
                tkMessageBox.showinfo("Wrong Location Name", "Location name can contain only:\n"
                                    "Letters, Numbers, Underscores and/or Dashes!\nPlease retype location!")
        else:
            Gui.label_location_value.configure(state='normal')
            Gui.location_enabled = True
            Gui.button_location.configure(text="Set Location")

    def check_start_action(self):
        if (Gui.location_enabled):
            tkMessageBox.showinfo("Missing Location Name","Please confirm upload location\nand then try again!")
        else:
            self.create_start_action()