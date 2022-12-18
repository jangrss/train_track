# **********************************************************************************************************************
# Name of Application: TrainTrack
# Version: 1.0
# Date created: 2020/01/28
#
# Setup:
# Programming Language: Python 3.7.5
# Development Environment: PyCharm Community Edition 2019.2.3
# GUI-library: kivy 1.11.1
# Database: PostgreSQL by ElephantSQL (https://www.elephantsql.com/) configured in queries.py
# Datacenter: Google Compute Engine europe-west2 (London)
# PostgreSQL interface: pg8000
#
# Structure:
# main.py - main application
# main.kv - Kv-file to load Kv-code into main application
# kv (folder) - folder containing Kv-files with kivy language to create widget trees in declarative way (screens of app)
# graphics (folder) - folder containing graphics in png-format used in Kv-files (background, buttons, logo, navigation)
# queries.py - queries to PostgreSQL database
# **********************************************************************************************************************
# -*- encoding: utf-8 -*-

# standard library imports
import re
import random
import string
import smtplib
from time import strftime, localtime
from datetime import datetime
from plyer import email

# GUI-library imports
import kivy

kivy.config.Config.set('graphics', 'resizable', False)  # needs to implemented right after "import kivy" (same scaling)
from kivy.uix.screenmanager import Screen, CardTransition
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import sp, dp

# local application import
from queries import Database

# create instance of class Database (py-file: queries.py)
queries = Database()

'''=================================================Global Variables================================================='''
id_athlete = 0
id_trainer = 0
'''===============================Base Values for Spinner widgets in different classes==============================='''
# defined once for multiple usage
values_gender = ['diverse', 'female', 'male']
values_height = []
for height_cm in range(100, 251, 1):  # list with height from 1 m to 2.5 m, step = 1
    height_m = "{:.2f}".format(height_cm / 100)
    values_height.append(height_m + ' ' + 'm')
values_weight = []
for weight_kg in range(40, 251, 1):  # list with weight from 40 kg to 250 kg, step = 1
    weight_kg = str(weight_kg)
    values_weight.append(weight_kg + ' ' + 'kg')
'''=================================================Basic Functions=================================================='''


# general function for pop-up with title, label, and close button
def pop_up(title, message):
    close_button = Button(text='Dismiss', size_hint_y=None, height=dp(value=50), color=[1, 1, 1, 1], background_normal='',
                          background_color=[47 / 255., 167 / 255., 212 / 255., 1.])  # button to close pop-up
    label = Label(text=message, color=[47 / 255., 167 / 255., 212 / 255., 1.],
                  valign='middle', halign='center', font_size=sp(14))  # label inside pop-up
    label.bind(size=lambda s, w: s.setter('text_size')(s, w))  # set label size according to text size

    content = BoxLayout(orientation='vertical')
    content.add_widget(label)
    content.add_widget(close_button)
    popup = Popup(title=title, title_align='center', title_size=sp(16),
                  title_color=[47 / 255., 167 / 255., 212 / 255., 1.], content=content, size_hint=(None, None),
                  size=(dp(value=250), dp(value=400)), background='graphics/background/background_popup.png',
                  separator_color=[47 / 255., 167 / 255., 212 / 255., 1.])  # entire pop-up
    close_button.bind(on_release=popup.dismiss)
    popup.open()


# generate a randomized password
def password_generator():
    characters = string.ascii_letters + string.punctuation + string.digits
    # choose randomly characters and append them to each other to create a string with a length between 5 and 8
    password = ''.join(random.choice(characters) for _ in range(random.randint(5, 8)))
    return password


# send a email to confirm the registration of a trainer
def confirmation_email_trainer(first_name_trainer, last_name_trainer, receiving_email, receiver_password):
    # assign login credentials for the TrainTrack email account
    password = None #anonymized
    sender_email = 'info.traintrack@gmail.com'
    subject = 'Welcome trainer to TrainTrack!'
    content = '''Hello %s %s!\n\nWe want to welcome you to our fitness application, TrainTrack! A trainer account was\
 created for you.\n\nYou can log in to your account with the following credentials:\n\nUsername (Your email address)\n
: %s\nPassword: %s\n\nFor security reasons, we would advise you to change your password immediately.\nEnjoy our\
 application, and if you have any questions or technical problems, do not hesitate to contact us!\n\nBest regards\n
Your TrainTrack support team''' % (first_name_trainer, last_name_trainer, receiving_email, receiver_password)

    try:
        server = smtplib.SMTP(host='smtp.gmail.com:587')
        # authenticate to the SMTP server
        server.ehlo()
        server.starttls()
        server.login(user=sender_email, password=password)
        message = 'Subject: {}\n\n{}'.format(subject, content)

        # send utf-8 encoded confirmation email to the trainer
        server.sendmail(from_addr=sender_email, to_addrs=receiving_email, msg=message.encode('utf8'))
        server.quit()
    except Exception as e:
        print(e)


# send a email to confirm the registration of an athlete
def confirmation_email_athlete(first_name_athlete, last_name_athlete, receiving_email, receiver_password):
    # assign login credentials for the TrainTrack email account
    password = None #anonymized
    sender_email = 'info.traintrack@gmail.com'
    subject = 'Welcome to TrainTrack!'
    content = '''Hello %s %s!\n\nWe want to welcome you to our fitness application, TrainTrack! An athlete account was\
 created for you.\n\nYou can log in to your account with the following credentials:\n\nUsername (Your email address)\n
: %s\nPassword: %s\n\nFor security reasons, we would advise you to change your password immediately.\nEnjoy our\
 application, and if you have any questions or technical problems, do not hesitate to contact us!\n\nBest regards\n
Your TrainTrack support team''' % (first_name_athlete, last_name_athlete, receiving_email, receiver_password)

    try:
        server = smtplib.SMTP(host=None)
        # authenticate to the SMTP server
        server.ehlo()
        server.starttls()
        server.login(user=sender_email, password=password)
        message = 'Subject: {}\n\n{}'.format(subject, content)

        # send encoded confirmation email to the trainer
        server.sendmail(from_addr=sender_email, to_addrs=receiving_email, msg=message.encode('utf8'))
        server.quit()
    except Exception as e:
        print(e)


# send a email when a user forgot the previous password
def new_password_email(first_name, last_name, receiving_email, receiver_password):
    # assign login credentials for the TrainTrack email account
    password = None #anonymized
    sender_email = 'info.traintrack@gmail.com'
    subject = 'Your new password'
    content = '''Hello %s %s!\n\nWe received a notification that you forgot your password. So we generated a new one\
 you.\n\nYou can log in to your account with the following credentials:\n\nNew Password: %s\n\nFor security reasons, we\
 would advise you to change your password immediately.\nEnjoy our application, and if you have any questions or\
 technical problems, do not hesitate to contact us!\n\nBest regards\nYour TrainTrack support team''' \
              % (first_name, last_name, receiver_password)

    try:
        server = smtplib.SMTP(host=None)
        # authenticate to the SMTP server
        server.ehlo()
        server.starttls()
        server.login(user=sender_email, password=password)
        message = 'Subject: {}\n\n{}'.format(subject, content)

        # send encoded confirmation email to the trainer
        server.sendmail(from_addr=sender_email, to_addrs=receiving_email, msg=message.encode('utf8'))
        server.quit()
    except Exception as e:
        print(e)


'''==================================================Custom Widgets=================================================='''


# image with behaviour of button
class ImageButton(ButtonBehavior, Image):
    pass


# label with behaviour of button
class LabelButton(ButtonBehavior, Label):
    pass


# drop-down option-fields for spinner
class SpinnerOptions(SpinnerOption):
    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = 'graphics/buttons/dropdownoption.png'
        self.background_down = 'graphics/buttons/dropdownoption_grau.png'
        self.height = dp(value=35)
        self.color = [47 / 255., 200 / 255., 212 / 255., 1.]


# Spinner widget that inherits mechanisms and triggered actions of Spinner and Spinner options
class SpinnerWidget(Spinner):
    def __init__(self, **kwargs):
        super(SpinnerWidget, self).__init__(**kwargs)
        self.option_cls = SpinnerOptions


'''*****************************************************SCREENS******************************************************'''
'''==================================================Basic Screens==================================================='''


# Screen shown when starting application (kv-file: home_screen.kv)
class HomeScreen(Screen):
    pass


# Screen to contact developers (kv-file: contact_screen.kv)
class ContactScreen(Screen):
    # sends email to developer "Jan"
    @staticmethod
    def mail_jan():
        recipient = None ##anonymized
        subject = 'TrainTrack: Your Request'
        text = 'Your Username/ Email (if available):\n\n[Your Request]'
        create_chooser = False
        email.send(recipient=recipient, subject=subject, text=text, create_chooser=create_chooser)


'''=================================================Trainer Screens=================================================='''


# Screen to register on the application as trainer (kv-file: registration_screen_trainer.kv)
class RegistrationScreenTrainer(Screen):

    def reset_data(self):

        self.ids.first_name_trainer.text = ''
        self.ids.last_name_trainer.text = ''
        self.ids.login_email.text = ''
        self.ids.team_name.text = ''

    def get_started(self):

        # compare characters of the inserted email address with alphanumeric and "@" characters and check if they match
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.login_email.text)

        # if the text fields are empty or the email address contains invalid characters, open a pop-up to inform
        if (self.ids.first_name_trainer.text == '') or (self.ids.last_name_trainer.text == '') or (match_mail is None) \
                or (self.ids.team_name.text == ''):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # if the inserted email address already exists in the database, open a pop-up to inform
        elif queries.check_email_trainer(trainer_email=self.ids.login_email.text) is not None:
            pop_up(title='Email address already in use', message='This email address is already in use.\nPlease '
                                                                 'choose another one.')

        # when the text fields are filled, the email address is valid and not already used, generate a password,
        # send a email, create a new entry in the database according to the user's inputs and
        # open a pop-up to confirm success
        else:
            password = password_generator()

            confirmation_email_trainer(first_name_trainer=self.ids.first_name_trainer.text,
                                       last_name_trainer=self.ids.last_name_trainer.text,
                                       receiving_email=self.ids.login_email.text,
                                       receiver_password=password)

            queries.register_trainer(trainer_first_name=self.ids.first_name_trainer.text,
                                     trainer_last_name=self.ids.last_name_trainer.text,
                                     trainer_mail=self.ids.login_email.text,
                                     password=password,
                                     team_name=self.ids.team_name.text)

            pop_up(title='New Trainer added: Registration complete', message='Your registration was successful! '
                                                                             '\nAn email with the password was sent to'
                                                                             ' the following email address: ' +
                                                                             self.ids.login_email.text)
            self.reset_data()
            MainApp().change_screen('login_screen_trainer', CardTransition(direction='up', duration=.3))


# Screen to request a new password, if trainer forgot the current password (kv-file: forgot_password_trainer.kv)
class ForgotPasswordTrainer(Screen):

    def reset_data(self):
        self.ids.id_trainer.text = ''
        self.ids.login_email.text = ''

    # if so, create a new password and send it via email to the user
    def get_started(self):

        # compare characters of the inserted email address with alphanumeric and "@" characters and check if they match
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.login_email.text)

        # if the text fields are empty or the email address contains invalid characters, open a pop-up to inform
        if (self.ids.id_trainer.text == '') or (self.ids.login_email.text == '') or (match_mail is None):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # if the inserted email does not exist in the database, open a pop-up to inform and stop the process
        elif queries.check_email_trainer(trainer_email=self.ids.login_email.text) is None:
            pop_up(title='Email address is not registered',
                   message='This email address is not registered on TrainTrack.'
                           '\nPlease choose another one or register.')

        # if the inserted email address and ID do not match, open a pop-up to inform and stop the process
        elif queries.check_email_id_trainer(id_trainer=self.ids.id_trainer.text,
                                            trainer_email=self.ids.login_email.text) == 0:
            pop_up(title='Forgot Password: Invalid Inputs', message='Invalid ID or email. Please check your inputs.')

        # when the text fields are filled and the email address and ID match, generate a new password and change it
        # send a email and open a pop-up to confirm the success
        else:

            password = self.password_generated()
            queries.forgot_password_trainer(password=password,
                                            id_trainer=self.ids.id_trainer.text,
                                            trainer_email=self.ids.login_email.text)

            first_name = queries.get_trainer(id_trainer=self.ids.id_trainer.text)[1]
            last_name = queries.get_trainer(id_trainer=self.ids.id_trainer.text)[2]

            new_password_email(first_name=first_name,
                               last_name=last_name,
                               receiving_email=self.ids.login_email.text,
                               receiver_password=password)
            pop_up(title='Forgot Password: New Password on your Way', message='Your Inputs matched!\nAn email with a '
                                                                              'newly generated Password was sent to the'
                                                                              ' following Email Address: ' +
                                                                              self.ids.login_mail.text)
            self.reset_data()
            MainApp().change_screen('login_screen_trainer', CardTransition(direction='up', duration=.3))


# Screen to log into the application with a trainer account (kv-file: login_screen_athlete.kv)
class LoginScreenTrainer(Screen):

    def reset_data(self):
        self.ids.login_email.text = ''
        self.ids.login_password.text = ''

    def get_started(self):

        # compare characters of the inserted email address with alphanumeric and "@" characters and check if they match
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.login_email.text)

        # if the text fields are empty or the email address contains invalid characters, open a pop-up to inform
        if (self.ids.login_email.text == '') or (self.ids.login_password.text == '') or (match_mail is None):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        elif (self.ids.login_email.text != '') and (self.ids.login_password.text != ''):

            # if the email address and password match,
            # load the necessary information about the trainer and enter "Main Screen"
            if queries.validate_trainer(trainer_mail=self.ids.login_email.text,
                                        trainer_password=self.ids.login_password.text) is not None:

                # access ID, email address and assigned team of particular trainer and save them in global variables
                # (for using them to limiting the trainers access to the own team)
                global id_trainer

                id_trainer = queries.get_id_trainer(trainer_mail=self.ids.login_email.text)
                team_trainer = queries.fetch_team_trainer(trainer_mail=self.ids.login_email.text)

                # load all base values, trainings, exercises and
                # the team for which the trainer is responsible and display the team
                GUI.ids.edit_workout_trainer.ids.select_training.values = \
                    queries.possible_trainings_trainer(id_trainer=id_trainer)
                GUI.ids.edit_workout_trainer.ids.select_exercise.values = \
                    queries.possible_exercises_trainer(id_trainer=id_trainer)
                GUI.ids.edit_athlete_trainer.ids.select_athlete.values = queries.possible_athletes_trainer(id_trainer)
                GUI.ids.main_screen_trainer.ids.team_label.text = '[b]' + 'Your Team: ' + team_trainer + '[/b]'
                GUI.ids.add_athlete_trainer.ids.gender_athlete.values = values_gender
                GUI.ids.add_athlete_trainer.ids.height_athlete.values = values_height
                GUI.ids.add_athlete_trainer.ids.weight_athlete.values = values_weight
                GUI.ids.edit_athlete_trainer.ids.gender_athlete.values = values_gender
                GUI.ids.edit_athlete_trainer.ids.height_athlete.values = values_height
                GUI.ids.edit_athlete_trainer.ids.weight_athlete.values = values_weight
                self.reset_data()
                MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))

            # if Database Error
            elif queries.validate_trainer(trainer_mail=self.ids.login_email.text,
                                          trainer_password=self.ids.login_password.text) == -1:
                pop_up(title='Database Error', message='Test of your Login Data was not possible.')

            # when there is no match between the email address and password, open a pop-up and inform the user
            else:
                pop_up(title='Invalid Login', message='Invalid Username or Password. Please check your Input.')


# Screen that gives access to the different functions of the application (kv-file: main_screen_trainer.kv)
class MainScreenTrainer(Screen):

    @staticmethod
    def logout_reset():
        global id_trainer
        id_trainer = None
        AddWorkoutTrainer().reset_data()
        EditWorkoutTrainer().reset_data()
        AddAthleteTrainer().reset_data()
        EditAthleteTrainer().reset_data()


# Screen that allows the trainer to add a new training or exercise
# for athletes of the own team (kv-file: add_workout_trainer.kv)
class AddWorkoutTrainer(Screen):

    @staticmethod
    def reset_data():
        GUI.ids.add_workout_trainer.ids.select_workout_add.text = 'Select Workout to add'
        GUI.ids.add_workout_trainer.ids.name_workout.hint_text = 'Name of Workout'
        GUI.ids.add_workout_trainer.ids.description_workout.hint_text = 'Description of Workout'
        GUI.ids.add_workout_trainer.ids.name_workout.text = ''
        GUI.ids.add_workout_trainer.ids.description_workout.text = ''
        GUI.ids.add_workout_trainer.ids.text_id_workout.text = 'ID of Workout:'
        GUI.ids.add_workout_trainer.ids.select_training_add.text = 'Select Training of Exercise'
        GUI.ids.add_workout_trainer.ids.check_sets.active = False
        GUI.ids.add_workout_trainer.ids.check_reps.active = False
        GUI.ids.add_workout_trainer.ids.check_weight.active = False
        GUI.ids.add_workout_trainer.ids.check_distance.active = False
        GUI.ids.add_workout_trainer.ids.check_sets.disabled = True
        GUI.ids.add_workout_trainer.ids.check_reps.disabled = True
        GUI.ids.add_workout_trainer.ids.check_weight.disabled = True
        GUI.ids.add_workout_trainer.ids.check_distance.disabled = True
        GUI.ids.add_workout_trainer.ids.select_training_add.disabled = True

    def update_workout(self):
        GUI.ids.edit_workout_trainer.ids.select_exercise.values = \
            queries.possible_exercises_trainer(id_trainer=id_trainer)
        GUI.ids.edit_workout_trainer.ids.select_training.values = \
            queries.possible_trainings_trainer(id_trainer=id_trainer)
        GUI.ids.track_workout_athlete.ids.name_training.values = \
            queries.possible_trainings_trainer(id_trainer=id_trainer)
        GUI.ids.track_workout_athlete.ids.name_exercise.values = \
            queries.possible_exercises_trainer(id_trainer=id_trainer)
        self.ids.select_training_add.values = \
            queries.possible_trainings_trainer(id_trainer=id_trainer)

    def reveal_spinner(self):

        # if the trainer decides to add a new training, the text fields for training will appear
        if self.ids.select_workout_add.text == 'Training':
            self.ids.text_id_workout.text = 'ID of Training:'
            self.ids.select_training_add.disabled = True

            # if the list of existing trainings is empty, set the displayed ID to "1" for the very first training
            if not queries.id_trainings_trainer(id_trainer):
                self.ids.id_workout.text = '1'

            # when the list of existing trainings is not empty, find the lowest, next available number for an ID
            else:
                self.ids.id_workout.text = queries.find_free_id_training_trainer()

            # disable all checkboxes and change the hidden text of text fields into the corresponding training ones
            self.ids.name_workout.hint_text = 'Name of Training'
            self.ids.description_workout.hint_text = 'Description of Training'
            self.ids.check_sets.active = False
            self.ids.check_reps.active = False
            self.ids.check_weight.active = False
            self.ids.check_distance.active = False
            self.ids.check_sets.disabled = True
            self.ids.check_reps.disabled = True
            self.ids.check_weight.disabled = True
            self.ids.check_distance.disabled = True

        # if the trainer decides to add a new exercise, a list with potential trainings will be available
        if self.ids.select_workout_add.text == 'Exercise':
            self.ids.text_id_workout.text = 'ID of Exercise'
            self.ids.select_training_add.values = queries.possible_trainings_trainer(id_trainer=id_trainer)
            self.ids.select_training_add.disabled = False

            # if the list of existing exercises is empty, set the displayed ID to "1" for the very first exercise
            if not queries.id_exercises_trainer(id_trainer):
                self.ids.id_workout.text = '1'
            else:
                if queries.find_free_id_exercise_trainer() is None:
                    self.ids.id_workout.text = '1'

                # when the list of existing exercises is not empty, find the lowest, next available number for an ID
                # and change hidden text of text fields into the corresponding ones of exercises
                else:
                    self.ids.id_workout.text = queries.find_free_id_exercise_trainer()
                self.ids.name_workout.hint_text = 'Name of Exercise'
                self.ids.description_workout.hint_text = 'Description of Exercise'

        # if an exercise and the associated training was selected, activate all checkboxes
        if (self.ids.select_workout_add.text == 'Exercise') and (
                self.ids.select_training_add.text != 'Select Training of Exercise'):
            self.ids.check_sets.disabled = False
            self.ids.check_reps.disabled = False
            self.ids.check_weight.disabled = False
            self.ids.check_distance.disabled = False
            self.ids.check_sets.active = False
            self.ids.check_reps.active = False
            self.ids.check_weight.active = False
            self.ids.check_distance.active = False

    def submit_workout(self):

        # if the text fields are empty, no training was selected or the trainer did not decide between a exercise
        # or training, open pop-up and inform trainer
        if (self.ids.name_workout.text == '') or (self.ids.description_workout.text == '') or (
                (self.ids.select_workout_add.text == 'Exercise') and (
                self.ids.select_training_add.text == 'Select Training of Exercise')) or (
                (self.ids.select_workout_add.text == 'Select Workout to add') and (
                self.ids.select_training_add.text == 'Select Training of Exercise')):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # when the trainer chose a training and filled in the text fields, create a new training in the database,
        # open a pop-up to inform about success and change to the main screen
        else:
            if self.ids.select_workout_add.text == 'Training':

                # if Database Error
                if queries.add_training_trainer(training_name=self.ids.name_workout.text,
                                                id_trainer=id_trainer,
                                                training_description=self.ids.description_workout.text) == -1:
                    pop_up(title='Database Error', message='Submitting your Workout was not possible.')

                else:

                    # when the trainer chose a training and filled in the text fields,
                    # create a new training in the database, open a pop-up to inform about success and
                    # change to the main screen
                    pop_up(title='Training: Confirmation', message='A new training has been added to the database!')
                    self.reset_data()
                    MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))
                    self.update_workout()

            # when the trainer chose a exercise, the corresponding training and filled in the text fields and checkboxes
            # create a new exercise in the database,
            # open a pop-up to inform about success and change to the main screen
            elif self.ids.select_workout_add.text == 'Exercise':
                # if Database Error
                if queries.add_exercise_trainer(training_name=self.ids.select_training_add.text,
                                                id_trainer=id_trainer,
                                                exercise_name=self.ids.name_workout.text,
                                                exercise_description=self.ids.description_workout.text,
                                                sets=self.ids.check_sets.active,
                                                reps=self.ids.check_reps.active,
                                                weight=self.ids.check_weight.active,
                                                distance=self.ids.check_distance.active) == -1:
                    pop_up(title='Database Error', message='Submitting your Workout was not possible.')

                else:

                    # when the trainer chose a exercise, the corresponding training and filled in the text fields and
                    # checkboxes create a new exercise in the database, open a pop-up to inform about success and
                    # change to the main screen
                    pop_up(title='Exercise: Confirmation', message='A new exercise has been added to the database.')
                    self.reset_data()
                    MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))
                    self.update_workout()


# Screen to edit a pre-existing training or exercise (kv-file: edit_workout_trainer.kv)
class EditWorkoutTrainer(Screen):

    @staticmethod
    def reset_data():
        GUI.ids.edit_workout_trainer.ids.select_training.text = 'Select Training'
        GUI.ids.edit_workout_trainer.ids.select_exercise.text = 'Select Exercise'
        GUI.ids.edit_workout_trainer.ids.text_id_workout.text = 'ID of Workout:'
        GUI.ids.edit_workout_trainer.ids.id_workout.text = ''
        GUI.ids.edit_workout_trainer.ids.name_workout.text = ''
        GUI.ids.edit_workout_trainer.ids.name_workout.hint_text = 'Name of Workout'
        GUI.ids.edit_workout_trainer.ids.description_workout.hint_text = 'Description of Workout'
        GUI.ids.edit_workout_trainer.ids.description_workout.text = ''
        GUI.ids.edit_workout_trainer.ids.select_training.disabled = False
        GUI.ids.edit_workout_trainer.ids.select_exercise.disabled = False

    def update_workout(self):
        self.ids.select_training.values = queries.possible_trainings_trainer(id_trainer=id_trainer)
        self.ids.select_exercise.values = queries.possible_exercises_trainer(id_trainer=id_trainer)

    def undo_selection(self):
        self.ids.select_training.disabled = False
        self.ids.select_exercise.disabled = False
        self.reset_data()

    def block_select_exercise(self):

        # if a specific training is selected, display its ID, reveal the hint text for trainings
        # and lock the exercise selection
        if self.ids.select_training.text != 'Select Training':
            id_training = queries.fetch_id_workout_trainer(workout_name=self.ids.select_training.text)
            self.ids.select_exercise.disabled = True
            self.ids.id_workout.text = 'ID of Training'
            self.ids.name_workout.hint_text = 'Name of Training'
            self.ids.description_workout.hint_text = 'Description of Training'

            # if the ID of a named training exists in the database, display its name and description
            if id_training is not None:
                self.ids.text_id_workout.text = "ID of Training"
                self.ids.id_workout.text = id_training
                self.ids.name_workout.text = \
                    queries.fetch_training_trainer(id_trainer=id_trainer, id_training=id_training)[0]
                self.ids.description_workout.text = \
                    queries.fetch_training_trainer(id_trainer=id_trainer, id_training=id_training)[1]

            # if the ID of a named training does not exist in the database, open pop-up and inform
            else:
                pop_up(title='Training: No existing training selected',
                       message='Your selected training does not exist. Please pick another one')

    def block_select_training(self):

        # if a specific exercise is selected, display its ID, reveal the hint text for exercises
        # and lock the training selection
        if self.ids.select_training.text != 'Select Exercise':
            id_exercise = queries.fetch_id_exercise_trainer(workout_name=self.ids.select_exercise.text)
            self.ids.select_training.disabled = True
            self.ids.id_workout.text = 'ID of Exercise'
            self.ids.name_workout.hint_text = 'Name of Exercise'
            self.ids.description_workout.hint_text = 'Description of Exercise'

            # if the ID of a named exercise exists in the database, display its name and description
            if id_exercise is not None:
                self.ids.text_id_workout.text = "ID of Exercise:"
                self.ids.id_workout.text = id_exercise
                self.ids.name_workout.text = queries.fetch_exercise_trainer(id_trainer=id_trainer,
                                                                            id_exercise=id_exercise)[0]
                self.ids.description_workout.text = \
                    queries.fetch_exercise_trainer(id_trainer=id_trainer, id_exercise=id_exercise)[1]

            # if the ID of a named exercise does not exist in the database, open pop-up and inform
            else:
                pop_up(title='Exercise: No existing exercise selected',
                       message='Your selected exercise does not exist. Please pick another one')

    # the "Update"-Button
    def check_data_update(self):

        # if the text fields are empty or the ID could not be displayed, open pop-up and inform
        if (self.ids.name_workout.text == '') or (self.ids.description_workout.text == '') or (
                self.ids.id_workout.text == 'ID of Workout'):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # when the training selection is disabled while the "Update" button was clicked, update a the exercise
        # open a pop-up to inform and change to main screen
        else:
            if self.ids.select_training.disabled is True:

                # if Database Error
                if queries.edit_exercise_update_trainer(name_of_workout=self.ids.name_workout.text,
                                                        description_workout=self.ids.description_workout.text,
                                                        id_workout=self.ids.id_workout.text) == -1:
                    pop_up(title='Database Error', message='Editing your Workout was not possible.')

                else:

                    # update the exercise, open a pop-up to inform and change to main screen
                    pop_up(title='Workout: Update complete', message='Workout was successfully updated.')
                    self.reset_data()
                    self.update_workout()
                    MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))

            # when the exercise selection is disabled while the "Update" button was clicked, update a the training
            # open a pop-up to inform and change to main screen
            if self.ids.select_exercise.disabled is True:

                # if Database Error
                if queries.edit_training_update_trainer(name_of_workout=self.ids.name_workout.text,
                                                        description_workout=self.ids.description_workout.text,
                                                        id_workout=self.ids.id_workout.text) == -1:
                    pop_up(title='Database Error', message='Editing your Workout was not possible.')

                else:

                    # update the training, open a pop-up to inform and change to main screen
                    pop_up(title='Workout: Update complete',
                           message='Workout was successfully updated.')
                    self.reset_data()
                    self.update_workout()
                    MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))

    # the "Update" button
    def check_data_delete(self):

        # if neither an exercise nor training was selected, display a pop-up and inform
        if self.ids.select_exercise.text == 'Select Exercise' and \
                self.ids.select_training.text == 'Select Training':
            pop_up(title='Workout: Delete not possible', message='Please choose a Workout to delete.')

        # if the ID could not be displayed, open pop-up and inform
        if self.ids.id_workout.text == 'ID of Workout':
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')
        else:

            # if the training selection is disabled and the selected exercise was already deleted,
            # open pop-up and inform
            if self.ids.select_training.disabled is True:

                # if Database Error
                if queries.edit_exercise_delete_trainer(id_workout=self.ids.id_workout.text) == -1:
                    pop_up(title='Database Error', message='Deleting your Workout was not possible.')

                else:

                    # when the training selection is disabled while the "Delete" button was clicked, delete the workout
                    # open a pop-up to inform and change to main screen
                    pop_up(title='Workout: Delete complete', message='Workout was successfully deleted.')
                    self.update_workout()
                    self.reset_data()
                    MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))

            # if the exercise selection is disabled and the selected training was already deleted,
            # open pop-up and inform
            if self.ids.select_exercise.disabled is True:

                # if Data Base error
                if queries.edit_training_delete_trainer(id_workout=self.ids.id_workout.text) == -1:
                    pop_up(title='Database Error', message='Deleting your Workout was not possible.')

                else:

                    # when the exercise selection is disabled while the "Delete" button was clicked, delete the workout
                    # open a pop-up to inform and change to main screen
                    pop_up(title='Workout: Delete complete', message='Workout was successfully deleted.')
                    self.reset_data()
                    self.update_workout()
                    MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))


# Screen to add a new athlete into the own team (kv-file: add_athlete_trainer.kv)
class AddAthleteTrainer(Screen):
    name_possible_athletes = queries.possible_athletes_trainer(id_trainer=id_trainer)

    @staticmethod
    def reset_data():
        GUI.ids.add_athlete_trainer.ids.id_athlete.text = ''
        GUI.ids.add_athlete_trainer.ids.gender_athlete.text = 'Select Gender of Athlete'
        GUI.ids.add_athlete_trainer.ids.first_name_athlete.text = ''
        GUI.ids.add_athlete_trainer.ids.last_name_athlete.text = ''
        GUI.ids.add_athlete_trainer.ids.email_athlete.text = ''
        GUI.ids.add_athlete_trainer.ids.height_athlete.text = 'Input Height of Athlete'
        GUI.ids.add_athlete_trainer.ids.weight_athlete.text = 'Input Weight of Athlete'
        GUI.ids.add_athlete_trainer.ids.bmi_athlete.text = 'Enter Height and Weight\nto calculate Body-Mass-Index'

    def get_free_id(self):

        # if there is no athlete in the database, display number "1" in the ID field
        if queries.find_free_id_add_athlete_trainer() is None:
            self.ids.id_athlete.text = '1'

        # if there are athletes in the database, display the next available ID
        else:
            self.ids.id_athlete.text = str(queries.find_free_id_add_athlete_trainer())

    @staticmethod
    def update_athlete():
        GUI.ids.edit_athlete_trainer.ids.select_athlete.values = queries.possible_athletes_trainer(id_trainer)

    def calculate_bmi(self):

        # if there is no information about the weight and the height of the Athlete, request a complete entry
        if ((self.ids.weight_athlete.text == 'Input Weight of Athlete') or
                (self.ids.height_athlete.text == 'Input Height of Athlete')):
            self.ids.bmi_athlete.text = 'Please complete your Entry!'

        # extract the number of the weight and height and calculate and display the rounded BMI
        else:
            weight = self.ids.weight_athlete.text.split(' ')[0]
            height = float(self.ids.height_athlete.text.split(' ')[0])
            bmi = round(int(weight) / ((float(height)) ** 2), 1)
            self.ids.bmi_athlete.text = 'BMI of the Athlete: ' + str(bmi)

    def check_data(self):
        # compare characters of the inserted email address with alphanumeric and "@" characters and check if they match
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.email_athlete.text)

        match_first_name = re.match(pattern=r'^[a-zA-Z]+(([\'-][a-zA-Z])?[a-zA-Z]*)*$',
                                    string=self.ids.first_name_athlete.text)
        match_last_name = re.match(pattern=r'^[a-zA-Z]+(([\'-][a-zA-Z])?[a-zA-Z]*)*$',
                                   string=self.ids.last_name_athlete.text)

        # if the text fields or button values are empty or the email address contains invalid characters,
        # open a pop-up to inform
        if match_mail is None or self.ids.gender_athlete.text == 'Select Gender of Athlete' or \
                self.ids.first_name_athlete.text == '' or self.ids.last_name_athlete.text == '' or \
                self.ids.height_athlete.text == 'Input Height of Athlete' or \
                self.ids.weight_athlete.text == 'Input Weight of Athlete':
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        elif match_first_name is None or match_last_name is None:
            pop_up(title='Invalid Name Input', message='Your Name Input did not match the predefined Structure.\n'
                                                       'Please ensure that your Input does not contain any spaces.')

        # check if the email address already exist in the database and if so, open pop-up and inform
        elif queries.check_email_athlete(athlete_email=self.ids.email_athlete.text) is not None:
            pop_up(title='Email already in use',
                   message='This email address is already in use.\nPlease choose another one.')

        # when all text fields and buttons are filled and the email address is valid, generate a password
        else:
            athlete_password = password_generator()

            # extract the number of the weight and height
            weight = int(self.ids.weight_athlete.text.split(' ')[0])
            height = float(self.ids.height_athlete.text.split(' ')[0])

            # if Database Error
            if queries.add_athlete_trainer(id_athlete=self.ids.id_athlete.text,
                                           id_trainer=id_trainer,
                                           athlete_first_name=self.ids.first_name_athlete.text,
                                           athlete_last_name=self.ids.last_name_athlete.text,
                                           athlete_password=athlete_password,
                                           athlete_gender=self.ids.gender_athlete.text,
                                           athlete_email=self.ids.email_athlete.text,
                                           athlete_height=height,
                                           athlete_weight=weight) == -1:

                pop_up(title='Database Error', message='Adding new Athlete was not possible.')

            else:

                # when creating a new athlete in the database was successful, send a email to the athlete,
                # open pop-up to inform and change to main screen
                confirmation_email_athlete(first_name_athlete=self.ids.first_name_athlete.text,
                                           last_name_athlete=self.ids.last_name_athlete.text,
                                           receiving_email=self.ids.email_athlete.text,
                                           receiver_password=athlete_password)

                pop_up(title='New Athlete added', message='A new athlete has been added to the application!'
                                                          '\nAn email with the password was sent to the following '
                                                          'email address: ' + self.ids.email_athlete.text)
                self.reset_data()
                self.update_athlete()
                MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))


# Screen to edit the information of a pre-existing athlete (kv-file: edit_athlete_trainer.kv)
class EditAthleteTrainer(Screen):
    name_possible_athletes = queries.possible_athletes_trainer(id_trainer=id_trainer)

    @staticmethod
    def reset_data():
        GUI.ids.edit_athlete_trainer.ids.id_athlete.text = ''
        GUI.ids.edit_athlete_trainer.ids.select_athlete.text = 'Select Athlete'
        GUI.ids.edit_athlete_trainer.ids.first_name_athlete.text = ''
        GUI.ids.edit_athlete_trainer.ids.last_name_athlete.text = ''
        GUI.ids.edit_athlete_trainer.ids.gender_athlete.text = 'Gender of selected Athlete'
        GUI.ids.edit_athlete_trainer.ids.email_athlete.text = ''
        GUI.ids.edit_athlete_trainer.ids.height_athlete.text = 'Input Height of Athlete'
        GUI.ids.edit_athlete_trainer.ids.weight_athlete.text = 'Input Weight of Athlete'
        GUI.ids.edit_athlete_trainer.ids.bmi_athlete.text = 'Enter Height and Weight\nto calculate Body-Mass-Index'

    def load(self):

        # save the displayed full name, split it into first and last name to find the ID of the athlete with
        # this specific combination
        s = self.ids.select_athlete.text
        athlete_first_name = s.split(' ')[0]
        athlete_last_name = s.split(' ')[1]
        id_athletes = queries.fetch_id_athlete_trainer(athlete_first_name=athlete_first_name,
                                                       athlete_last_name=athlete_last_name)

        # fill in all information of an athlete into the different text fields and buttons
        self.ids.id_athlete.text = str(id_athletes)
        self.ids.gender_athlete.text = queries.fetch_athlete(id_athlete=id_athletes)[5]
        self.ids.first_name_athlete.text = queries.fetch_athlete(id_athlete=id_athletes)[2]
        self.ids.last_name_athlete.text = queries.fetch_athlete(id_athlete=id_athletes)[3]
        self.ids.email_athlete.text = queries.fetch_athlete(id_athlete=id_athletes)[6]
        self.ids.height_athlete.text = str('{:.2f}'.format(queries.fetch_athlete(id_athlete=id_athletes)[7])) + ' m'
        self.ids.weight_athlete.text = str(queries.fetch_athlete(id_athlete=id_athletes)[8]) + ' kg'
        self.calculate_bmi()

    @staticmethod
    def update_athlete():
        GUI.ids.edit_athlete_trainer.ids.select_athlete.values = queries.possible_athletes_trainer(id_trainer)

    def get_id(self):

        # display the ID according to the athlete who is chose
        select_athlete = self.ids.select_athlete.text

        first_name = select_athlete.split(' ')[0]
        last_name = select_athlete.split(' ')[1]
        self.ids.id_athlete.text = queries.fetch_id_athlete_trainer(athlete_first_name=first_name,
                                                                    athlete_last_name=last_name)

    def calculate_bmi(self):

        # if there is no information about the weight and the height of the Athlete, request a complete entry
        if ((self.ids.weight_athlete.text == 'Input Weight of Athlete') or (
                self.ids.height_athlete.text == 'Input Height of Athlete')):
            self.ids.bmi_athlete.text = 'Please complete your Entry!'

        # extract the number of the weight and height and calculate and display the rounded BMI
        else:
            weight = self.ids.weight_athlete.text.split(' ')[0]
            height = self.ids.height_athlete.text.split(' ')[0]
            bmi = round(int(weight) / ((float(height)) ** 2), 1)
            self.ids.bmi_athlete.text = 'BMI of the Athlete: ' + str(bmi)

    def check_data_update(self):

        # compare characters of the inserted email address with alphanumeric and "@" characters and check if they match
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.email_athlete.text)

        match_first_name = re.match(pattern=r'^[a-zA-Z]+(([\'-][a-zA-Z])?[a-zA-Z]*)*$',
                                    string=self.ids.first_name_athlete.text)
        match_last_name = re.match(pattern=r'^[a-zA-Z]+(([\'-][a-zA-Z])?[a-zA-Z]*)*$',
                                   string=self.ids.last_name_athlete.text)

        if match_mail is None or self.ids.first_name_athlete.text == '' or self.ids.last_name_athlete == '' or \
                self.ids.gender_athlete.text == 'Select Gender of Athlete' or \
                self.ids.first_name_athlete.text == '' or self.ids.last_name_athlete.text == '' or \
                self.ids.height_athlete.text == 'Input Height of Athlete' or \
                self.ids.weight_athlete.text == 'Input Weight of Athlete' or \
                self.ids.select_athlete.text == 'Select Athlete':
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        elif match_first_name is None or match_last_name is None:
            pop_up(title='Invalid Name Input', message='Your Name Input did not match the predefined Structure.\n'
                                                       'Please ensure that your Input does not contain any spaces.')

        # when all text fields and buttons are filled with valid values, update the athlete row in the database,
        # open a pop-up to inform and change to main screen
        else:
            weight = int(self.ids.weight_athlete.text.split(' ')[0])
            height = float(self.ids.height_athlete.text.split(' ')[0])

            # if Database Error
            if queries.edit_athlete_update_trainer(id_athlete=self.ids.id_athlete.text,
                                                   athlete_first_name=self.ids.first_name_athlete.text,
                                                   athlete_last_name=self.ids.last_name_athlete.text,
                                                   athlete_gender=self.ids.gender_athlete.text,
                                                   athlete_email=self.ids.email_athlete.text,
                                                   athlete_height=height,
                                                   athlete_weight=weight) == -1:

                pop_up(title='Database Error', message='Updating Athlete was not possible.')

            else:

                # when all text fields and buttons are filled with valid values, update the athlete row in the database,
                # open a pop-up to inform and change to main screen
                self.reset_data()
                self.update_athlete()
                MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))
                pop_up(title='Athlete: Update complete', message='Athlete was successfully updated.')

    def check_data_delete(self):

        # if the ID of an athlete did not display in the screen, open a pop-up to inform
        if self.ids.id_athlete.text == '':
            pop_up(title='Information required',
                   message='Please fill in all the necessary Information to delete an Athlete.')
        else:

            # if Database Error
            if queries.edit_athlete_delete_trainer(id_athlete=self.ids.id_athlete.text) == -1:

                # if Database Error
                pop_up(title='Database Error',
                       message='Deleting Athlete was not possible.')

            else:

                # when the ID of an athlete match with the entry in the database, delete the athlete,
                # open a pop-up to inform and change to main screen
                pop_up(title='Athlete: Delete complete', message='Athlete was successfully deleted.')
                self.reset_data()
                self.update_athlete()
                MainApp().change_screen('main_screen_trainer', CardTransition(direction='up', duration=.3))


'''=================================================Athlete Screens=================================================='''


# Screen to request new password, if athlete forgot current password (kv-file: forgot_password_athlete.kv)
class ForgotPasswordAthlete(Screen):

    # reset of text in TextInput fields for ID of athlete and email after new password is generated end sent
    # (IDs in kv-file: id_athlete, login_email)
    def reset_data(self):
        self.ids.id_athlete.text = ''
        self.ids.login_email.text = ''

    # check ID and email of athlete, generate and send new password
    def get_started(self):
        # check if the form of the entered email is correct by using a Regular expression
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.login_email.text)
        # if no ID, no email or wrong form for email is entered
        if (self.ids.id_athlete.text == '') or (self.ids.login_email.text == '') or (match_mail is None):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')
        # if email has not been registered before
        elif queries.check_email_athlete(athlete_email=self.ids.login_email.text) is None:
            pop_up(title='Email address: Not registered', message='This email address is not registered on TrainTrack.'
                                                                  '\nPlease choose another one or register.')
        # if combination of entered ID and email does not exist in database
        elif queries.check_email_id_athlete(id_athlete=self.ids.id_athlete.text,
                                            email_athlete=self.ids.login_email.text) is None:
            pop_up(title='Forgot Password: Invalid Inputs', message='Invalid ID or email. Please check your inputs.')
        # continuation if inputs are correct
        else:
            password = password_generator()  # generate new password
            # add new password to database
            queries.update_password_athlete(password=password, id_athlete=self.ids.id_athlete.text,
                                            email_athlete=self.ids.login_email.text)
            athlete_data = queries.fetch_athlete(id_athlete=self.ids.id_athlete.text)
            first_name = athlete_data[2]
            last_name = athlete_data[3]
            # send email to athlete with new password and display of pop-up "forgot password confirmation"
            new_password_email(first_name=first_name, last_name=last_name, receiving_email=self.ids.login_email.text,
                               receiver_password=password)
            pop_up(title='Forgot password: New password on your way!', message='Your inputs matched!\nAn email with '
                                                                               'a newly generated password was sent to '
                                                                               'the following email address:\n%s'
                                                                               % self.ids.login_email.text)
            self.reset_data()
            # change to LoginScreenAthlete
            MainApp().change_screen(screen_name='login_screen_athlete',
                                    transition=CardTransition(direction='up', duration=.3))


# Screen for login of the athlete (kv-file: login_screen_athlete.kv)
class LoginScreenAthlete(Screen):

    # reset of text in TextInput fields for email and password
    def reset_data(self):
        self.ids.login_email.text = ''
        self.ids.login_password.text = ''

    # check email and password of athlete and login
    def get_started(self):
        # check if the form of the entered email is correct by using a Regular expression
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.login_email.text)

        # if no email, no password or wrong form for email is entered
        if (self.ids.login_email.text == '') or (self.ids.login_password.text == '') or (match_mail is None):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # if form of email and password are correct, continue method
        else:

            # check if email and password are correct
            if queries.validate_athlete(athlete_mail=self.ids.login_email.text,
                                        athlete_password=self.ids.login_password.text) is None:
                pop_up(title='Invalid Login', message='Invalid Username or Password. Please check your Input.')

            else:

                # if Database Error
                if queries.validate_athlete(athlete_mail=self.ids.login_email.text,
                                            athlete_password=self.ids.login_password.text) == -1:
                    pop_up(title='Database Error', message='Test of your Login Data was not possible.')

                # if login data correct
                else:
                    # setup for screen "TrackWorkoutAthlete" --> values are already available when the screen is opened
                    global id_athlete  # ID of the athlete as global variable (used in other methods for athlete)
                    id_athlete = queries.fetch_id_athlete(athlete_mail=self.ids.login_email.text)
                    GUI.ids.track_workout_athlete.ids.id_athlete.text = 'ID of Athlete: ' + str(id_athlete)
                    GUI.ids.track_workout_athlete.ids.name_training.values = queries.possible_trainings_athlete(
                        id_athlete=id_athlete)
                    GUI.ids.track_workout_athlete.ids.name_exercise.values = ['']

                    # setup for screen EditAthleteAthlete --> values are already available when the screen is opened
                    GUI.ids.edit_athlete_athlete.ids.id_athlete.text = 'ID of Athlete: ' + str(id_athlete)
                    GUI.ids.edit_athlete_athlete.ids.gender_athlete.values = values_gender
                    GUI.ids.edit_athlete_athlete.ids.height_athlete.values = values_height
                    GUI.ids.edit_athlete_athlete.ids.weight_athlete.values = values_weight

                    # reset data and change to MainScreenAthlete
                    self.reset_data()
                    MainApp().change_screen(screen_name='main_screen_athlete',
                                            transition=CardTransition(direction='up', duration=.3))


# Screen with all sub-screens for athlete, shown after successful login (kv-file: main_screen_athlete.kv)
class MainScreenAthlete(Screen):
    # reset of ID of athlete
    @staticmethod
    def logout_reset():
        global id_athlete
        id_athlete = 0


# Screen to track the workouts of the athlete (kv-file: track_workout_athlete.kv)
class TrackWorkoutAthlete(Screen):
    # fetch completed workouts of athlete
    def fetch_possible_workouts(self):
        # fetch IDs of workouts
        id_workouts_athlete = queries.possible_id_workouts_athlete(id_athlete=id_athlete)

        # if athlete has not completed any workouts before, no previous workouts to choose, only new one
        if len(id_workouts_athlete) == 0:
            self.ids.id_workout.text = '1 (new)'
            self.ids.id_workout.values = ['1 (new)']

        # if athlete has completed workouts before, fetch IDs of previous workouts and assign to objects of screen
        else:
            self.ids.id_workout.text = str(max([int(element) for element in id_workouts_athlete]) + 1) + ' (new)'
            self.ids.id_workout.values = id_workouts_athlete + [str(max([int(element) for element
                                                                         in id_workouts_athlete]) + 1) + ' (new)']

    # fetch all parameters of a workout and set status for objects of screen
    def fetch_workout(self):
        # if chosen workout is a new workout
        if self.ids.id_workout.text[-5:] == '(new)':
            # reset text in "TextInput" fields for all parameters
            self.ids.name_training.text = 'Name of Training'
            self.ids.id_training.text = ''
            self.ids.name_exercise.text = 'Name of Exercise'
            self.ids.id_exercise.text = ''
            self.ids.date_workout_start.text = ''
            self.ids.date_workout_end.text = ''
            self.ids.time_workout_start.text = ''
            self.ids.time_workout_end.text = ''
            self.ids.sets.text = ''
            self.ids.reps.text = ''
            self.ids.weight.text = ''
            self.ids.distance.text = ''

            # disable / enable objects of the screen to prevent incorrect entries
            self.ids.name_training.disabled = False
            self.ids.text_id_training.disabled = False
            self.ids.id_training.disabled = False
            self.ids.name_exercise.disabled = True
            self.ids.text_id_exercise.disabled = False
            self.ids.id_exercise.disabled = False
            self.ids.date_workout_start.disabled = True
            self.ids.date_workout_end.disabled = True
            self.ids.time_workout_start.disabled = True
            self.ids.time_workout_end.disabled = True
            self.ids.current_date_start.disabled = True
            self.ids.current_date_start.state = 'down'  # state for deactivated graphic (according to Kv-file)
            self.ids.current_date_end.disabled = True
            self.ids.current_date_end.state = 'down'  # state for deactivated graphic (according to Kv-file)
            self.ids.sets.disabled = True
            self.ids.reps.disabled = True
            self.ids.weight.disabled = True
            self.ids.distance.disabled = True
            self.ids.submit.disabled = True

        # if chosen workout is a previous workout
        else:
            # fetch complete data of workout
            data_workout = queries.fetch_workout_athlete(id_workout=self.ids.id_workout.text, id_athlete=id_athlete)
            # assign parameters of workout to objects of the screen
            self.ids.name_training.text = str(queries.fetch_name_training_athlete(id_training=data_workout[2])[0])
            self.ids.name_training.disabled = True
            self.ids.text_id_training.disabled = True
            self.ids.id_training.text = str(data_workout[2])  # ID of training
            self.ids.id_training.disabled = True
            self.ids.name_exercise.text = str(queries.fetch_name_exercise_athlete(id_exercise=data_workout[3])[0])
            self.ids.name_exercise.disabled = True
            self.ids.text_id_exercise.disabled = True
            self.ids.id_exercise.text = str(data_workout[3])  # ID of exercise
            self.ids.id_exercise.disabled = True
            self.ids.date_workout_start.text = str(data_workout[4])  # start date
            self.ids.date_workout_start.disabled = True
            self.ids.time_workout_start.text = str(data_workout[5])  # start time
            self.ids.time_workout_start.disabled = True
            self.ids.date_workout_end.text = str(data_workout[6])  # end date
            self.ids.date_workout_end.disabled = True
            self.ids.time_workout_end.text = str(data_workout[7])  # end time
            self.ids.time_workout_end.disabled = True
            self.ids.current_date_start.disabled = True
            self.ids.current_date_start.state = 'down'  # state for deactivated graphic (according to Kv-file)
            self.ids.current_date_end.disabled = True
            self.ids.current_date_end.state = 'down'  # state for deactivated graphic (according to Kv-file)
            self.ids.sets.text = 'Sets: ' + str(data_workout[8])  # number of sets
            self.ids.sets.disabled = True
            self.ids.reps.text = 'Reps: ' + str(data_workout[9])  # number of repetitions
            self.ids.reps.disabled = True
            self.ids.weight.disabled = True
            self.ids.distance.disabled = True
            self.ids.submit.disabled = True

            # if weight used for exercise is in database, assign value to corresponding object including unit
            if str(data_workout[10]) != 'None':
                self.ids.weight.text = 'Weight: ' + str(data_workout[10]) + " kg"
            # if weight used for exercise is not in database, assign value to corresponding object without unit
            else:
                self.ids.weight.text = 'Weight: ' + str(data_workout[10])

            # if unit for exercise is in database, assign value to corresponding object including unit
            if str(data_workout[11]) != "None":
                self.ids.distance.text = 'Distance: ' + str(data_workout[11]) + " km"
            # if unit for exercise is not in database, assign value to corresponding object without unit
            else:
                self.ids.distance.text = 'Distance: ' + str(data_workout[11])

    # fetch exercises included in the selected training
    def exercises_included(self):
        if self.ids.name_training.text == 'Name of Training':  # if no training has been selected, hint in spinner
            self.ids.name_exercise.values = ['please select training first']
        else:  # if training has been selected, fetch corresponding exercises
            self.ids.name_exercise.values = queries.possible_exercises_athlete(id_training=self.ids.id_training.text,
                                                                               id_athlete=id_athlete)

    # assign values for start of workout
    def start_time(self):
        self.ids.date_workout_start.text = strftime('%Y-%m-%d', localtime())  # start date
        self.ids.time_workout_start.text = strftime('%H:%M:%S', localtime())  # start time

    # assign values for end of workout
    def end_time(self):
        self.ids.date_workout_end.text = strftime('%Y-%m-%d', localtime())  # end date
        self.ids.time_workout_end.text = strftime('%H:%M:%S', localtime())  # end time

    # set the selected training, including ID of training
    def set_training(self):
        self.ids.id_athlete.text = 'ID of Athlete: ' + str(id_athlete)
        # ID of training according to name of Training
        self.ids.id_training.text = str(queries.fetch_id_training_athlete(
            name_training=self.ids.name_training.text))
        # disable / enable objects of the screen to prevent incorrect entries
        self.ids.name_training.disabled = False
        self.ids.text_id_training.disabled = False
        self.ids.id_training.disabled = False
        self.ids.name_exercise.text = 'Name of Exercise'
        self.ids.name_exercise.disabled = False
        self.ids.text_id_exercise.disabled = False
        self.ids.id_exercise.text = ''
        self.ids.id_exercise.disabled = False
        self.ids.date_workout_start.disabled = True
        self.ids.date_workout_end.disabled = True
        self.ids.time_workout_start.disabled = True
        self.ids.time_workout_end.disabled = True
        self.ids.current_date_start.disabled = True
        self.ids.current_date_start.state = 'down'  # state for deactivated graphic (according to Kv-file)
        self.ids.current_date_end.disabled = True
        self.ids.current_date_end.state = 'down'  # state for deactivated graphic (according to Kv-file)
        self.ids.sets.disabled = True
        self.ids.reps.disabled = True
        self.ids.weight.disabled = True
        self.ids.distance.disabled = True
        self.ids.submit.disabled = True

    # set the selected exercise, including ID of exercise
    def set_exercise(self):
        if self.ids.id_workout.text[-5:] == '(new)':  # if new workout is tracked
            self.ids.id_exercise.text = str(queries.fetch_id_exercise_athlete(
                name_exercise=self.ids.name_exercise.text))
            # enable other objects of screen
            self.ids.date_workout_start.disabled = False
            self.ids.date_workout_end.disabled = False
            self.ids.time_workout_start.disabled = False
            self.ids.time_workout_end.disabled = False
            self.ids.current_date_start.disabled = False
            self.ids.current_date_start.state = 'normal'  # state for activated graphic (according to Kv-file)
            self.ids.current_date_end.disabled = False
            self.ids.current_date_end.state = 'normal'  # state for activated graphic (according to Kv-file)
            self.ids.submit.disabled = False
            self.ids.sets.text = ''
            self.ids.sets.disabled = False
            self.ids.reps.text = ''
            self.ids.reps.disabled = False
            self.ids.weight.text = ''
            self.ids.weight.disabled = False
            self.ids.distance.text = ''
            self.ids.distance.disabled = False
        else:  # if previous workout is selected, pass
            pass

        # if selected exercise does not include certain parameters (sets, reps ...), deactivate corresponding objects
        parameters_exercise = queries.fetch_parameters_exercise_athlete(id_exercise=queries.fetch_id_exercise_athlete(
            name_exercise=self.ids.name_exercise.text))
        if parameters_exercise[0] is False:
            self.ids.sets.text = ''  # sets
            self.ids.sets.disabled = True
        if parameters_exercise[1] is False:
            self.ids.reps.text = ''  # reps
            self.ids.reps.disabled = True
        if parameters_exercise[2] is False:
            self.ids.weight.text = ''  # weight
            self.ids.weight.disabled = True
        if parameters_exercise[3] is False:
            self.ids.distance.text = ''  # distance
            self.ids.distance.disabled = True

    # display description of training
    def training_description(self):
        if self.ids.name_training.text == 'Name of Training':  # if no training selected, pop-up "no info selection"
            pop_up('Missing Selection', 'No Workout selected. Choose a Workout to show the Description.')
        else:  # if training selected, display pop-up "training description"
            pop_up(title=self.ids.name_training.text, message=queries.fetch_training_description_athlete(
                name_of_training=self.ids.name_training.text)[0])

    # display description of exercise
    def exercise_description(self):
        if self.ids.name_exercise.text == 'Name of Exercise':  # if no exercise selected, pop-up "no info selection"
            pop_up('Missing Selection', 'No Workout selected. Choose a Workout to show the Description.')

        else:  # if exercise selected, display pop-up "exercise description"
            pop_up(title=self.ids.name_exercise.text, message=queries.fetch_exercise_description_athlete(
                name_of_exercise=self.ids.name_exercise.text)[0])

    # delete selected workout
    def delete(self):
        if self.ids.id_workout.text[-5:] == '(new)':  # if selected workout is not created yet, no delete
            pop_up(title='Workout: Delete not possible',
                   message='Workout that has yet not been created can not be deleted.')

        # if previous workout selected
        else:

            # if Database Error
            if queries.delete_workout_athlete(id_workout=self.ids.id_workout.text, id_athlete=id_athlete) == -1:
                pop_up(title='Database error', message='Delete of your Workout was not possible.')

            # if delete successful
            else:
                pop_up(title='Workout: Delete complete', message='Workout was successfully deleted.')
                MainApp().change_screen(screen_name='main_screen_athlete',
                                        transition=CardTransition(direction='up', duration=.3))

    # check if data is correct and add to database
    def check_submit(self):
        # matches dates in yyyy-mm-dd format, separated by "-"
        match_start_date = re.match(pattern=r'^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$',
                                    string=self.ids.date_workout_start.text)
        match_end_date = re.match(pattern=r'^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$',
                                  string=self.ids.date_workout_end.text)
        # matches times in hh:mm: format, separated by ":"
        match_start_time = re.match(pattern=r'^((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$)',
                                    string=self.ids.time_workout_start.text)
        match_end_time = re.match(pattern=r'^^((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$)',
                                  string=self.ids.time_workout_end.text)
        match_sets = re.match(pattern=r'^[0-9]+$', string=self.ids.sets.text)  # one or more digits
        match_reps = re.match(pattern=r'^[0-9]+$', string=self.ids.reps.text)
        match_weight = re.match(pattern=r'^\d+(\.\d+)?$', string=self.ids.weight.text)  # one or more digits with dot
        match_distance = re.match(pattern=r'^\d+(\.\d+)?$', string=self.ids.distance.text)

        # if not all fields are filled out or have wrong format, pop-up "invalid form"
        if (match_start_date is None) or (match_end_date is None) or (match_start_time is None) or \
                (match_end_time is None) or (self.ids.name_training.text == 'Name of Training') or \
                (self.ids.name_exercise.text == 'Name of Exercise') or \
                (match_sets is None and self.ids.sets.disabled is False) or \
                (match_reps is None and self.ids.reps.disabled is False) or \
                (match_weight is None and self.ids.weight.disabled is False) or \
                (match_distance is None and self.ids.distance.disabled is False):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # if all fields filled out
        else:
            # split date and time into several elements
            split_date_start = self.ids.date_workout_start.text.split('-')
            split_time_start = self.ids.time_workout_start.text.split(':')
            split_date_end = self.ids.date_workout_end.text.split('-')
            split_time_end = self.ids.time_workout_end.text.split(':')

            # coerce elements of list to integer
            split_date_start = [int(element) for element in split_date_start]
            split_time_start = [int(element) for element in split_time_start]
            split_date_end = [int(element) for element in split_date_end]
            split_time_end = [int(element) for element in split_time_end]

            # validate date (only possible with try - except)
            try:
                datetime(year=split_date_start[0], month=split_date_start[1], day=split_date_start[2])
                datetime(year=split_date_end[0], month=split_date_end[1], day=split_date_end[2])
                correct_date = True
            except ValueError:
                correct_date = False

            if correct_date is False:
                pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

            else:
                # create date object from list
                start_time = datetime(year=split_date_start[0], month=split_date_start[1], day=split_date_start[2],
                                      hour=split_time_start[0], minute=split_time_start[1], second=split_time_start[2])
                end_time = datetime(year=split_date_end[0], month=split_date_end[1], day=split_date_end[2],
                                    hour=split_time_end[0], minute=split_time_end[1], second=split_time_end[2])

                # calculate time difference
                time_difference = end_time - start_time
                time_difference_seconds = time_difference.total_seconds()

            # if more than 24 hours time difference
                if time_difference_seconds >= 86400:
                    pop_up(title='Exceeded Workout Limit',
                           message='Your Workout exceeds a Duration of 24 Hours. '
                                   'If necessary, split your Workout into multiple sessions.')

            # if zero or negative time difference
                elif time_difference_seconds <= 0:
                    pop_up(title='Invalid Workout Time', message='Your Input results in a negative Time Difference. '
                                                                 'End Time has to be greater than Start Time.')

                # if all fields are filled out correct
                else:
                    # IDs previous workouts
                    id_workouts_athlete = queries.possible_id_workouts_athlete(id_athlete=id_athlete)

                    if not id_workouts_athlete:
                        id_workout = 1  # if no previous workouts ID = 1

                    # if previous workouts, max ID of athletes workout + 1
                    else:
                        id_workout = max([int(element) for element in id_workouts_athlete]) + 1

                    # add specified workout with all parameters to database
                    # if Database Error
                    if queries.submit_track_workout_athlete(id_workout=id_workout, id_athlete=id_athlete,
                                                            id_training=self.ids.id_training.text,
                                                            id_exercise=self.ids.id_exercise.text,
                                                            start_date=self.ids.date_workout_start.text,
                                                            start_time=self.ids.time_workout_start.text,
                                                            end_date=self.ids.date_workout_end.text,
                                                            end_time=self.ids.time_workout_end.text,
                                                            sets=self.ids.sets.text,
                                                            reps=self.ids.reps.text,
                                                            weight=self.ids.weight.text,
                                                            distance=self.ids.distance.text) == -1:
                        pop_up(title='Database Error', message='Tracking of your Workout was not possible.')

                    # if add successful
                    else:
                        pop_up(title='Workout: Tracking complete', message='Workout was successfully added.')
                        self.ids.name_exercise.disabled = True  # if opened next time, training has to be selected first
                        MainApp().change_screen(screen_name='main_screen_athlete',
                                                transition=CardTransition(direction='up', duration=.3))


# Screen to edit data of athlete (kv-file: edit_athlete_athlete.kv)
class EditAthleteAthlete(Screen):

    # load data of athlete, when screen is entered
    def load(self):
        data_athlete = queries.fetch_athlete(id_athlete=id_athlete)
        self.ids.gender_athlete.text = data_athlete[5]  # gender
        self.ids.first_name_athlete.text = data_athlete[2]  # first name
        self.ids.last_name_athlete.text = data_athlete[3]  # last name
        self.ids.email_athlete.text = data_athlete[6]  # email
        self.ids.password_athlete_new.text = ''
        self.ids.password_athlete_current.text = ''
        self.ids.height_athlete.text = str('{:.2f}'.format(data_athlete[7])) + ' m'  # height
        self.ids.weight_athlete.text = str(data_athlete[8]) + ' kg'  # weight
        self.calculate_bmi()

    # calculate Body Mass Index of athlete
    def calculate_bmi(self):
        # if entry is not complete, give hint to user
        if self.ids.weight_athlete.text == 'Input Weight of Athlete' or \
                self.ids.height_athlete.text == 'Input Height of Athlete':
            self.ids.bmi_athlete.text = 'Please complete your Entry!'
        # if entry complete
        else:
            weight = self.ids.weight_athlete.text.split(' ')[0]
            height = self.ids.height_athlete.text.split(' ')[0]
            bmi = round(int(weight) / ((float(height)) ** 2), 1)  # BMI = weight / height^2
            self.ids.bmi_athlete.text = 'BMI of the Athlete: ' + str(bmi)

    # check entered data and update database
    def check_data_update(self):
        # check if the form of the entered email and name is correct by using a Regular expression
        match_mail = re.match(pattern=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                              string=self.ids.email_athlete.text)
        match_first_name = re.match(pattern=r'^[a-zA-Z]+(([\'-][a-zA-Z])?[a-zA-Z])$',
                                    string=self.ids.first_name_athlete.text)
        match_last_name = re.match(pattern=r'^[a-zA-Z]+(([\'-][a-zA-Z])?[a-zA-Z])$',
                                   string=self.ids.last_name_athlete.text)

        # if one of the required fields is empty or email not correct, display pop-up "invalid form"
        if (self.ids.gender_athlete.text == 'Gender of selected Athlete') or \
                (self.ids.first_name_athlete.text == "") or (self.ids.last_name_athlete.text == "") or \
                (match_mail is None) or (self.ids.height_athlete.text == 'Height of selected Athlete') or \
                (self.ids.weight_athlete.text == 'Weight of selected Athlete'):
            pop_up(title='Invalid Input', message='Please fill in all Inputs with valid Information.')

        # if name is in wrong structure
        elif match_first_name is None or match_last_name is None:
            pop_up(title='Invalid Name Input', message='Your Name Input did not match the predefined Structure.\n'
                                                       'Please ensure that your Input does not contain any spaces.')

        # if all required fields are filled, exact classification of the required change
        else:

            # if new password is entered, check if current password is correct
            if self.ids.password_athlete_new.text != '' and queries.check_password_athlete(
                    id_athlete=id_athlete, athlete_password=self.ids.password_athlete_current.text) is not None:

                # update data and new password in database
                # if Database Error
                if queries.submit_edit_athlete_password(first_name=self.ids.first_name_athlete.text,
                                                        last_name=self.ids.last_name_athlete.text,
                                                        password=self.ids.password_athlete_new.text,
                                                        gender=self.ids.gender_athlete.text,
                                                        mail=self.ids.email_athlete.text,
                                                        height=float(self.ids.height_athlete.text.split(' ')[0]),
                                                        weight=int(self.ids.weight_athlete.text.split(' ')[0]),
                                                        id_athlete=id_athlete) == -1:
                    pop_up(title='Database Error', message='Update of your Data was not possible.')

                # if update successful
                else:
                    pop_up(title='Athlete: Update complete', message='Athlete was successfully updated.')
                    MainApp().change_screen(screen_name='main_screen_athlete',
                                            transition=CardTransition(direction='up', duration=.3))

            # if password is entered (mandatory to change password) for current password is not correct
            elif (self.ids.password_athlete_new.text != '' and
                  queries.check_password_athlete(id_athlete=id_athlete,
                                                 athlete_password=self.ids.password_athlete_current.text) is None) or \
                    (self.ids.password_athlete_current.text != '' and queries.check_password_athlete(
                        id_athlete=id_athlete, athlete_password=self.ids.password_athlete_current.text) is None):
                pop_up(title='Athlete: Invalid Password',
                       message='Your current Password did not match with your Input. Please try again.')

            # if change does not include change of password or no password is entered
            else:
                # update database with new data for athlete
                # if Database Error
                if queries.submit_edit_athlete(first_name=self.ids.first_name_athlete.text,
                                               last_name=self.ids.last_name_athlete.text,
                                               gender=self.ids.gender_athlete.text,
                                               mail=self.ids.email_athlete.text,
                                               height=float(self.ids.height_athlete.text.split(' ')[0]),
                                               weight=int(self.ids.weight_athlete.text.split(' ')[0]),
                                               id_athlete=id_athlete) == -1:
                    pop_up(title='Database Error', message='Update of your Data was not possible.')

                # if update successful
                else:
                    pop_up(title='Athlete: Update complete', message='Athlete was successfully updated.')
                    MainApp().change_screen(screen_name='main_screen_athlete',
                                            transition=CardTransition(direction='up', duration=.3))


'''**************************************************End of Screens**************************************************'''
'''=================================================Main Application================================================='''
# load Kv-code into main application
GUI = Builder.load_file(filename='main.kv')


# Main entry point into Kivy run loop
class MainApp(App):
    Window.size = (433, 770)  # proportional resolution iPhone

    def build(self):  # build-method to return widget trees constructed in Kv-files (GUI)
        return GUI

    @staticmethod
    def change_screen(screen_name, transition):  # enable changes between different screens
        screen_manager = GUI.ids['screen_manager']  # get screen manager from the Kv-file
        screen_manager.transition = transition  # type of transition if screen is changed
        screen_manager.current = screen_name  # currently displayed screen


if __name__ == '__main__':
    MainApp().run()
