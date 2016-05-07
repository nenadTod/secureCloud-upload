from Tkinter import *
from PIL import Image, ImageTk

class Gui:

    def __init__(self, root):
        self.create_window(root)
        self.create_status_bar(root)
        self.create_menu_bar(root)
        self.create_panels(root)

    def create_window(self, root):
        root.title("Secure Clouding - Upload pictures")
        root.geometry("420x400")
        root.minsize(width=420, height=380)
        root.iconbitmap('images/icon.ico')

    def create_status_bar(self, root):
        status_bar = Frame(root, height=25)
        status_bar.pack(side=BOTTOM, fill=BOTH)

        print_status = StringVar()
        print_files = StringVar()
        print_connection = StringVar()
        base_status = "Status: "
        base_files = "Files: "
        base_connection = "Connection: "

        label_status = Label(status_bar, width=15, textvariable=print_status, relief=RIDGE)#SUNKEN
        label_files = Label(status_bar, width=15, textvariable=print_files, relief=RIDGE)
        label_users = Label(status_bar, width=15, textvariable=print_connection, relief=RIDGE)
        label_status.pack(side=LEFT, fill=X, expand=1)
        label_files.pack(side=LEFT, fill=X, expand=1)
        label_users.pack(side=LEFT, fill=X, expand=1)

        value_status = base_status + "Ready"
        value_files = base_files + "(no files imported)"
        value_connection = base_connection + "Alive"
        print_status.set(value_status)
        print_files.set(value_files)
        print_connection.set(value_connection)

    def create_menu_bar(self, root):
        menu_bar = Menu(root)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Add Folder")
        file_menu.add_command(label="Add File")
        file_menu.add_separator()
        file_menu.add_command(label="Remove Selected File")
        file_menu.add_command(label="Clear Files List")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")
        menu_bar.add_cascade(label="File", menu=file_menu)

        action_menu = Menu(menu_bar, tearoff=0)
        action_menu.add_command(label="Encrypt And Upload")
        action_menu.add_command(label="Cancel All")
        menu_bar.add_cascade(label="Action", menu=action_menu)

        account_menu = Menu(menu_bar, tearoff=0)
        account_menu.add_command(label="Configure Cloud")
        account_menu.add_command(label="Change Account")
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

        label_cloud = Label(frame_cloud_data, anchor=W, text="Cloud name: ")
        label_user = Label(frame_cloud_data, anchor=W, text="User name: ")
        label_location = Label(frame_cloud_data, anchor=W, text="Upload location: ")
        # label_process = Label(frame_cloud_data, width=15, textvariable=print_connection, relief=RIDGE)
        label_cloud_value = Label(frame_cloud_data, anchor=W, text="DropBox")
        label_user_value = Label(frame_cloud_data, anchor=W, text="Pera9987")
        label_location_value = Label(frame_cloud_data, anchor=W, text="/NewFolder (1)/Slike sa mora 2015/NewFolderNewFolderNewFolder")

        button_switch = Button(frame_cloud_buttons, text="Switch Account", width=12, height=1)
        button_location = Button(frame_cloud_buttons, text="Set Location", width=12, height=1)

        label_cloud.grid(row=0, column=0, pady=(3,3), padx=5, sticky=W)
        label_user.grid(row=1, column=0, pady=3, padx=5, sticky=W)
        label_location.grid(row=2, column=0, pady=(3,10), padx=5, sticky=W)
        label_cloud_value.grid(row=0, column=1, pady=3, padx=0, sticky=W)
        label_user_value.grid(row=1, column=1, pady=3, padx=0, sticky=W)
        label_location_value.grid(row=2, column=1, pady=(3,10), padx=0, sticky=W)

        button_switch.pack(side=TOP, pady=(26,1), padx=10)
        button_location.pack(side=TOP, pady=(1,10), padx=10)

        return frame_cloud

    def create_files_panel(self, frame):
        frame_files = LabelFrame(frame, text="Affected files:")
        frame_files_panel = Frame(frame_files)
        frame_files_buttons = Frame(frame_files)
        frame_files_panel.pack(side=LEFT, fill=BOTH, pady=(5,10), expand=1)
        frame_files_buttons.pack(side=RIGHT, fill=BOTH, pady=5)

        files_list_scroll = Scrollbar(frame_files_panel)
        files_list_scroll.pack(side=RIGHT, fill=BOTH)
        files_files_list = Listbox(frame_files_panel, height=1500, yscrollcommand=files_list_scroll.set)
        files_files_list.pack(side=LEFT, fill=BOTH, padx=(10,0), expand=1)
        files_list_scroll.config(command=files_files_list.yview)

        button_add_folder = Button(frame_files_buttons, text="Add Folder", width=3, height=1)
        button_add_file = Button(frame_files_buttons, text="Add File", width=3, height=1)
        button_remove_file = Button(frame_files_buttons, text="Remove Selected", width=3, height=1)
        button_clear_all = Button(frame_files_buttons, text="Clear All", width=3, height=1)
        button_add_folder.pack(side=TOP, pady=(0,5), padx=(15,10))
        button_add_file.pack(side=TOP, pady=5, padx=(15,10))
        button_remove_file.pack(side=TOP, pady=5, padx=(15,10))
        button_clear_all.pack(side=TOP, pady=5, padx=(15,10))

        img1 = ImageTk.PhotoImage(Image.open("images/filenew.png"))
        button_add_folder.config(image=img1)

        for line in range(50):
            files_files_list.insert(END, "This is line number " + str(line))

        return frame_files

    def create_action_panel(self, frame):
        frame_action = LabelFrame(frame, text="Actions:")

        #label_process = Label(frame_action, width=15, textvariable=print_connection, relief=RIDGE)
        label_process = Label(frame_action, anchor=W, text="Encrypting and uploading.....uploadinguploadinguploadinguploadinguploading")

        button_cancel = Button(frame_action, text="Cancel", width=6, height=1)
        button_start = Button(frame_action, text="Encrypt and Upload", width=18, height=1)

        button_start.pack(side=RIGHT, fill=BOTH, pady=(5, 10), padx=(10, 10))
        button_cancel.pack(side=RIGHT, fill=BOTH, pady=(5, 10), padx=5)
        label_process.pack(side=LEFT, fill=BOTH, pady=(5,10), padx=5)
        return frame_action