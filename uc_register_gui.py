from Tkinter import *
import tkMessageBox

###     UPUTSTVO
#
# POZIVAS SA: uc_register = UCRegister(self.view.root, self)
# self.view.root je referenca na parenta - glavni gui, a
# self je referenca na glavni kontroler u aplikaciji
# kadje sve kako treba poziva metodu register_user() iz kontrolera,
# prosledi joj potrebne parametre i iskljuci se


class UCRegister(Toplevel):

    def __init__(self, parent, controller):
        Toplevel.__init__(self, parent)
        self.controller = controller
        self.email_value = None
        self.transient(parent)
        self.parent = parent
        body = Frame(self)
        self.create_window()
        self.create_body(body)
        body.pack()
        self.wait_window(self)

    def create_window(self):
        self.grab_set()
        self.title("Register User-Cloud")
        self.geometry("320x227")
        self.resizable(width=False, height=False)
        self.iconbitmap('images/icon.ico')

    def create_body(self, body):
        frame = LabelFrame(body, text="Register User-Cloud:")
        frame.pack(side=TOP, fill=BOTH, pady=5, padx=5)
        frame_buttons = Frame(frame)

        label_info = Label(frame, justify=LEFT, wraplength=300,
                           text="Please emter your e-mail address and password, so we can bring it back to you when needed.")
        label_email = Label(frame, text="Enter e-mail:")
        label_password1 = Label(frame, text="Enter password:")
        label_password2 = Label(frame, text="Repeat password:")

        email_value = Entry(frame, width=30)
        pass1_value = Entry(frame, width=30)
        pass2_value = Entry(frame, width=30)
        pass1_value.config(show=u"\u25CF")
        pass2_value.config(show=u"\u25CF")

        button_ok = Button(frame_buttons, text="Register", width=17, height=1,command=lambda: self.prepare_register(email_value.get(), pass1_value.get(), pass2_value.get()))
        button_cancel = Button(frame_buttons, text="Cancel", width=12, height=1, command=lambda: self.exit_action())

        label_info.grid(row=0, column=0, padx=5, columnspan=2)
        label_email.grid(row=1, column=0, sticky=W, padx=(5,0), pady=(15, 5))
        label_password1.grid(row=2, column=0, sticky=W, padx=(5,0), pady=5)
        label_password2.grid(row=3, column=0, sticky=W, padx=(5,0), pady=5)

        email_value.grid(row=1, column=1, sticky=W, pady=(15, 5))
        pass1_value.grid(row=2, column=1, sticky=W, pady=5)
        pass2_value.grid(row=3, column=1, sticky=W, pady=5)

        frame_buttons.grid(row=4, column=0, sticky=E, columnspan=2, pady=(20, 15))
        button_ok.pack(side=RIGHT, anchor=E, padx=8)
        button_cancel.pack(side=RIGHT, anchor=E, padx=8)


    def exit_action(self):
        self.destroy()

    def prepare_register(self, email, pass1, pass2):
        if email == "" or pass1 == "" or pass2 == "":
            tkMessageBox.showerror("Empty Fields",  "You have left some of the fields empty!\nPlease fill them.")
            return
        if pass1 != pass2:
            tkMessageBox.showerror("Passwords Mismatching", "Entered passwords are not equal!\nPlease enter same values.")
            return
        self.destroy()
        self.controller.register_user(email, pass1)
