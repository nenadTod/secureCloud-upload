from Tkinter import *
import tkMessageBox
from messages import Msg

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
        self.pass1_value = None
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

        label_info = Label(frame, justify=LEFT, wraplength=300, text=Msg.dialog_uc_register_explanation)
        label_email = Label(frame, text="Enter e-mail:")
        label_password1 = Label(frame, text="Enter password:")
        label_password2 = Label(frame, text="Repeat password:")

        self.email_value = Entry(frame, width=30)
        self.pass1_value = Entry(frame, width=30)
        self.pass2_value = Entry(frame, width=30)
        self.pass1_value.config(show=u"\u25CF")
        self.pass2_value.config(show=u"\u25CF")

        button_ok = Button(frame_buttons, text="Register", width=17, height=1,command=lambda: self.prepare_register(self.email_value.get(), self.pass1_value.get(), self.pass2_value.get()))
        button_cancel = Button(frame_buttons, text="Cancel", width=12, height=1, command=lambda: self.exit_action())

        label_info.grid(row=0, column=0, padx=5, columnspan=2)
        label_email.grid(row=1, column=0, sticky=W, padx=(5,0), pady=(15, 5))
        label_password1.grid(row=2, column=0, sticky=W, padx=(5,0), pady=5)
        label_password2.grid(row=3, column=0, sticky=W, padx=(5,0), pady=5)

        self.email_value.grid(row=1, column=1, sticky=W, pady=(15, 5))
        self.pass1_value.grid(row=2, column=1, sticky=W, pady=5)
        self.pass2_value.grid(row=3, column=1, sticky=W, pady=5)

        frame_buttons.grid(row=4, column=0, sticky=E, columnspan=2, pady=(20, 15))
        button_ok.pack(side=RIGHT, anchor=E, padx=8)
        button_cancel.pack(side=RIGHT, anchor=E, padx=8)


    def exit_action(self):
        self.destroy()

    def prepare_register(self, email, pass1, pass2):
        if email == "" or pass1 == "" or pass2 == "":
            tkMessageBox.showerror(Msg.fields_empty_title, Msg.fields_empty_message)
            return
        if self.check_email_values(email) and self.check_password_values(pass1):
            if pass1 != pass2:
                tkMessageBox.showerror(Msg.password_mismatch_title, Msg.password_not_equal)
                return
            else:
                self.destroy()
                self.controller.register_user(email, pass1)

    def check_email_values(self, event):
        email = self.email_value.get()
        pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9_.+-]+")
        if not pattern.match(email):
            tkMessageBox.showerror(Msg.email_wrong_title, Msg.email_pattern)
            return False
        return True

    def check_password_values(self, event):
        password = self.pass1_value.get()

        pattern = re.compile(r"[a-zA-Z0-9!#$%&()*+,\-.\/:;<=>?@[\\\]\^\_\{\|\}\~]{6,32}")
        pattern_low_case = re.compile(r"[a-z]+")
        pattern_big_case = re.compile(r"[A-Z]+")
        pattern_digit = re.compile(r"[0-9]+")
        pattern_special = re.compile(r"[!#$%&()*+,\-.\/:;<=>?@[\\\]\^\_\{\|\}\~]+")

        if not pattern.match(password):
            tkMessageBox.showerror(Msg.password_wrong_title,  Msg.password_description)
            return False
        elif not pattern_low_case.search(password):
            tkMessageBox.showerror(Msg.password_wrong_title, Msg.password_description + "\n" + Msg.password_lowcase)
            return False
        elif not pattern_big_case.search(password):
            tkMessageBox.showerror(Msg.password_wrong_title, Msg.password_description + "\n" + Msg.password_bigcase)
            return False
        elif not pattern_digit.search(password):
            tkMessageBox.showerror(Msg.password_wrong_title, Msg.password_description + "\n" + Msg.password_digit)
            return False
        elif not pattern_special.search(password):
            tkMessageBox.showerror(Msg.password_wrong_title, Msg.password_description + "\n" + Msg.password_character)
            return False
        return True


