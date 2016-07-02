
class Msg:

###########################################
###                 GUI                 ###

    naming_folder_error_title = "Wrong Folder Name"
    naming_folder_error_message = "Folder name can contain only:\nLetters, Numbers, Underscores and/or Dashes!\nPlease retype folder name!"

    naming_folder_missing_title = "Missing Folder Name"
    naming_folder_missing_message = "Please confirm upload folder\nand then try again!"

    quit_application_title = "Quit?"
    quit_application_message = "Are you sure you want to quit?"

###########################################
###              CONTROLLER             ###

    galleries_no_available_title = "No Available Galleries"
    galleries_no_available_message = "You have no galleries that could be downloaded!\nPlease try with another account, or create gallery within this."

    connection_rejected_title = "Rejection"
    connection_rejected_message = "Authorization rejected by user."

    download_success_title = "Download success"
    download_success_message = "Files downloaded successfully."

    upload_success_title = "Upload success"
    upload_success_message = "Files uploaded successfully."


###########################################
###               DOWNLOAD              ###

    dialog_download_explanation = "From here you can download content of your SecureCloud galery to your computer."

    location_missing_title = "Location Not Set"
    location_missing_message = "You haven't set download location!\nPlease choose it."

###########################################
###        REGISTER USER - CLOUD        ###

    dialog_uc_register_explanation = "Please enter your e-mail address and password, so we can bring it back to you when needed."

    fields_empty_title = "Empty Fields"
    fields_empty_message = "You have left some of the fields empty!\nPlease fill them."

    password_mismatch_title = "Passwords Mismatching"
    password_wrong_title = "Wrong Password Value"
    password_not_equal = "Entered passwords are not equal!\nPlease enter same values."
    password_description = "Password should contain from 6 to 32 characters\nAt least one of the characters has to be:\n" \
                           "- Capital letter\n- Small letter\n- Number\n" \
                           "- Special character: ! # $ % & ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ { | } ~\n"
    password_lowcase = "Please enter small letters."
    password_bigcase = "Please enter some capital letters."
    password_digit = "Please enter some digits."
    password_character = "Please enter some special character."

    email_wrong_title = "Wrong E-mail Value"
    email_pattern = "Wrong e-mail address format!\nE-mail should look like:\n(something)@(something).(something)\n" \
                    "something - can contain only letters, numbers, ' . ', ' - ', ' _ ', ' + '"
