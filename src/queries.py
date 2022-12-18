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

# *********************************************************Notes********************************************************
# In case of a Database Error only queries that are called by submit-, delete- or login-buttons return -1. Other
# queries exit application in case of an Error to prevent data corruption and consistency issues. Database Error is
# printed in console.
# Apart from Database Errors also the return of 'None' values will be caught.
# **********************************************************************************************************************

# library imports
import pg8000
import sys
import logging
import re


# all required queries for trainer and athlete
class Database:
    def __init__(self):
        self.conn = None

    
    # connection to database (call at the beginning of the following functions)
    def connection(self):
        try:
            self.conn = pg8000.connect(
                # parameters according to used database
                database=None,
                user=None,
                password=None,
                host=None,
                port=None) #anonymized
        # if error occurs, stop connection establishment
        except pg8000.core.InterfaceError as e:
            print(e)
            logging.error(e)
            sys.exit()
        finally:
            logging.info('Connection with PostgreSQL established.')  # output in console

# ==================================================queries for trainer=================================================

    
    # adding a new athlete into the application by creating a new data row in the database
    def add_athlete_trainer(self, id_athlete, id_trainer, athlete_first_name, athlete_last_name, athlete_password,
                            athlete_gender, athlete_email, athlete_height, athlete_weight):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # add a new row in the table "athlete" with given values for the parameters
                cur.execute('''INSERT INTO athlete (id_athlete, id_trainer, first_name, last_name, password, 
                            gender, mail, height, weight) VALUES (%s, %s, %s, %s, %s, 
                            %s, %s, %s, %s) RETURNING first_name, last_name, password, gender, mail, height, weight''',
                            (id_athlete, id_trainer, athlete_first_name, athlete_last_name, athlete_password,
                             athlete_gender, athlete_email, athlete_height, athlete_weight))

                # take this row of the query, save it into the database and return the result
                add_athlete = cur.fetchone()
                self.conn.commit()
                return add_athlete
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # adding a new exercise into the application by creating a new data row in the database
    def add_exercise_trainer(self, training_name, id_trainer, exercise_name, exercise_description, sets, reps,
                             weight,
                             distance):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # add a new row in the table "exercise" with given values for the parameters
                cur.execute(
                    '''INSERT INTO exercise (id_training, id_trainer, name, description, sets, reps, weight, distance)
                    VALUES ((SELECT id_training FROM training WHERE name = %s AND id_trainer = %s), %s, %s, %s, %s, 
                    %s, %s, %s) RETURNING name, description''',
                    (training_name, id_trainer, id_trainer, exercise_name, exercise_description, sets, reps,
                     weight, distance))

                # take this row of the query, save it into the database and return the result
                add_exercise = cur.fetchone()
                self.conn.commit()
                return add_exercise
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # adding a new training into the application by creating a new data row in the database
    def add_training_trainer(self, training_name, id_trainer, training_description):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # add a new row in the table "training" with given values for the parameters
                cur.execute('''INSERT INTO training (name, id_trainer, description) VALUES (%s, %s, %s) 
                            RETURNING name, description''', (training_name, id_trainer, training_description))

                # take this row of the query, save it into the database and return the result
                add_exercise = cur.fetchone()
                self.conn.commit()
                return add_exercise
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # check if the given email of a trainer exists in the database
    def check_email_trainer(self, trainer_email):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the email address of the table "trainer" where the value in the column "mail" matches with
                # a given input
                cur.execute('''SELECT mail FROM trainer WHERE mail = '%s' ''' % trainer_email)

                # take the first result and return it
                trainer_check_email = cur.fetchone()
                return trainer_check_email
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # match the given input of an ID and email with the database to check if the trainer exists
    def check_email_id_trainer(self, id_trainer, trainer_email):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all the rows from the table "mail" which values in the columns "id_trainer" and "mail"
                # matches with the given input
                cur.execute('''SELECT id_trainer, mail FROM trainer WHERE id_trainer = %s AND mail = %s''',
                            (id_trainer, trainer_email))

                # take the first result of the query and return it
                trainer_check_email = cur.fetchone()
                return trainer_check_email
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # delete an athlete on the "Edit Athlete" screen
    def edit_athlete_delete_trainer(self, id_athlete):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # delete a row of the table "athlete" where a given input matches the value of the column "id_athlete"
                cur.execute('''DELETE FROM athlete WHERE id_athlete = '%s' ''' % id_athlete)

                # count all rows that were deleted by the query, save the changes and return
                # the quantity of deleted rows (used to determine if a row was affected by the DELETE query)
                deletes_workout = cur.rowcount
                self.conn.commit()
                # prevents Database Error if ID of athlete not available
                return deletes_workout
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # update an athlete on the "Edit Athlete" screen
    def edit_athlete_update_trainer(self, id_athlete, athlete_first_name, athlete_last_name,
                                    athlete_gender, athlete_email, athlete_height, athlete_weight):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # update the values of the columns "first_name", "last_name", "gender", "mail", "height" and "weight
                # from the table "athlete" where a given input matches the value of the column "id_athlete"
                cur.execute(('''UPDATE athlete SET first_name = %s, last_name = %s, gender = %s, mail = %s, 
                height = %s, weight = %s WHERE id_athlete = %s '''),
                            (athlete_first_name, athlete_last_name, athlete_gender, athlete_email, athlete_height,
                             athlete_weight, id_athlete))

                # count all rows that were changed by the query, save the changes and return
                # the quantity of changed rows (used to determine if a row was affected by the UPDATE query)
                updates_athlete = cur.rowcount
                self.conn.commit()
                return updates_athlete
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # delete an exercise on the "Edit Workout" screen
    def edit_exercise_delete_trainer(self, id_workout):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # delete a row of the table "exercise" where a given input matches the value of the column "id_exercise"
                cur.execute('''DELETE FROM exercise WHERE id_exercise = '%s' ''' % id_workout)

                # count all rows that were deleted by the query, save the changes and return
                # the quantity of deleted rows (used to determine if a row was affected by the DELETE query)
                deletes_exercise = cur.rowcount
                self.conn.commit()
                return deletes_exercise
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # update an exercise on the "Edit Workout" screen
    def edit_exercise_update_trainer(self, name_of_workout, description_workout, id_workout):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # update the values of the columns "name" and "description" from the table "exercise" where a given
                # input matches the value of the column "id_exercise"
                cur.execute('''UPDATE exercise SET name = %s, description = %s WHERE id_exercise = %s''',
                            (name_of_workout, description_workout, id_workout))

                # count all rows that were changed by the query, save the changes and return
                # the quantity of changed rows (used to determine if a row was affected by the UPDATE query)
                updates_workout = cur.rowcount
                self.conn.commit()
                return updates_workout
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # delete a training on the "Edit Workout" screen
    def edit_training_delete_trainer(self, id_workout):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # delete a row of the table "training" where a given input matches the value of the column "id_training"
                cur.execute('''DELETE FROM training WHERE id_training = '%s' ''' % id_workout)

                # count all rows that were deleted by the query, save the changes and return
                # the quantity of deleted rows (used to determine if a row was affected by the DELETE query)
                deletes_workout = cur.rowcount
                self.conn.commit()
                return deletes_workout
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # update a training on the "Edit Workout" screen
    def edit_training_update_trainer(self, name_of_workout, description_workout, id_workout):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # update the values of the columns "name" and "description" from the table "training" where a given
                # input matches the value of the column "id_training"
                cur.execute('''UPDATE training SET name = %s, description = %s WHERE id_training = %s''',
                            (name_of_workout, description_workout, id_workout))

                # count all rows that were changed by the query, save the changes and return
                # the quantity of changed rows (used to determine if a row was affected by the UPDATE query)
                updates_training = cur.rowcount
                self.conn.commit()
                return updates_training
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch a specific exercise by matching a given input of an ID for the trainer and exercise
    def fetch_exercise_trainer(self, id_trainer, id_exercise):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all exercise names and descriptions from the table "exercise" which values in the columns
                # "id_trainer" and "id_exercise" match with a given input
                cur.execute('''SELECT name, description FROM exercise WHERE id_trainer = %s AND id_exercise = %s''',
                            (id_trainer, id_exercise))

                # take the first result of the query and return it
                fetching_exercise_description = cur.fetchone()
                if fetching_exercise_description is not None:
                    return fetching_exercise_description
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the id of a specific athlete
    def fetch_id_athlete_trainer(self, athlete_first_name, athlete_last_name):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the ID of an athlete from the table "athlete" where the value in the columns "first_name"
                # and "last_name" match a given input
                cur.execute('''SELECT id_athlete FROM athlete WHERE first_name = %s AND last_name = %s''',
                            (athlete_first_name, athlete_last_name))

                # take the first result (ID of athlete) of the query,
                # turn it into a string to display it in the application, remove special characters from the result
                # so that only the number remains and if the whole result is not none then return it
                fetching_athlete_id = cur.fetchone()
                fetching_athlete_id = str(fetching_athlete_id)
                match = re.findall("[0-9]+", fetching_athlete_id)[0]
                fetching_athlete_id = match
                if fetching_athlete_id is not None:
                    return fetching_athlete_id
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the id of a specific exercise
    def fetch_id_exercise_trainer(self, workout_name):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the ID of an exercise from the table "exercise" where the value in the column "name" matches
                # a given input
                cur.execute('''SELECT id_exercise FROM exercise WHERE name = '%s' ''' % workout_name)

                # take the first result (ID of exercise) of the query,
                # turn it into a string to display it in the application, remove special characters from the result
                # so that only the number remains and if the whole result is not none then return it
                fetching_id = cur.fetchone()
                fetching_id = str(fetching_id)
                match = re.findall("[0-9]+", fetching_id)[0]
                fetching_id = match
                if fetching_id is not None:
                    return fetching_id
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the id of a specific workout
    def fetch_id_workout_trainer(self, workout_name):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the ID of a training from the table "training" where the value in the column "name" matches
                # a given input
                cur.execute('''SELECT id_training FROM training WHERE name = '%s' ''' % workout_name)

                # take the first result (ID of training) of the query,
                # turn it into a string to display it in the application, remove special characters from the result
                # so that only the number remains and if the whole result is not none then return it
                fetching_id = cur.fetchone()
                fetching_id = str(fetching_id)
                match = re.findall("[0-9]+", fetching_id)[0]
                fetching_id = match
                if fetching_id is not None:
                    return fetching_id
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the team of a particular trainer
    def fetch_team_trainer(self, trainer_mail):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the team name from the table "trainer" where the value in the column "mail"
                # matches with a given input
                cur.execute('''SELECT team FROM trainer WHERE mail = '%s' ''' % trainer_mail)

                # take the first result (Team name), turn the first element into a string
                # and if the result is not none return it
                fetching_team = cur.fetchone()
                fetching_team = fetching_team[0]
                fetching_team = str(fetching_team)
                if fetching_team is not None:
                    return fetching_team
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch a specific training by matching a given input of an ID for the trainer and training
    def fetch_training_trainer(self, id_trainer, id_training):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all training names and descriptions from the table "training" which values in the columns
                # "id_trainer" and "id_trainer" match with a given input
                cur.execute('''SELECT name, description FROM training WHERE id_trainer = %s AND id_training = %s''',
                            (id_trainer, id_training))

                # take the first result of the query and return it
                fetching_training = cur.fetchone()
                if fetching_training is not None:
                    return fetching_training
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # determine the lowest, next available ID for an athlete
    def find_free_id_add_athlete_trainer(self):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all IDs of athlete from the table "athlete"
                cur.execute('''SELECT id_athlete FROM athlete''')

                # take all results of the query and save the first element (ID of athlete) of each result in a list
                assigned_id = cur.fetchall()
                list_used_ids = []
                for row in assigned_id:
                    list_used_ids.append(int(row[0]))
                list_used_ids = list(list_used_ids)

                # create a second list with a range of numbers between the lowest and highest value in the list prior
                ints_list = [1] + list(range(min(list_used_ids), max(list_used_ids) + 2))

                # compare both lists with each other and save only those ID numbers
                # that are not present in the first list in a third list
                missing_list = [x for x in ints_list if x not in list_used_ids]

                # take the lowest number of the third list, turn it into a string to display it in the application
                # and return it
                first_missing = min(missing_list)
                first_missing = str(first_missing)
                if first_missing is not None:
                    return first_missing
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # determine the lowest, next available ID for an exercise
    def find_free_id_exercise_trainer(self):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all IDs of exercises from the table "exercise"
                cur.execute('''SELECT id_exercise FROM exercise''')

                # take all results of the query and save the first element (ID of exercise) of each result in a list
                assigned_id = cur.fetchall()
                list_used_ids = []
                for row in assigned_id:
                    list_used_ids.append(int(row[0]))
                list_used_ids = list(list_used_ids)

                # create a second list with a range of numbers between the lowest and highest value in the list prior
                ints_list = [1] + list(range(min(list_used_ids), max(list_used_ids) + 2))

                # compare both lists with each other and save only those ID numbers
                # that are not present in the first list in a third list
                missing_list = [x for x in ints_list if x not in list_used_ids]

                # take the lowest number of the third list, turn it into a string to display it in the application
                # and return it
                first_missing = min(missing_list)
                first_missing = str(first_missing)
                if first_missing is not None:
                    return first_missing
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # determine the lowest, next available ID for a training
    def find_free_id_training_trainer(self):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all IDs of trainings from the table "training"
                cur.execute('''SELECT id_training FROM training''')

                # take all results of the query and save the first element (ID of training) of each result in a list
                assigned_id = cur.fetchall()
                list_used_ids = []
                for row in assigned_id:
                    list_used_ids.append(int(row[0]))
                list_used_ids = list(list_used_ids)

                # create a second list with a range of numbers between the lowest and highest value in the list prior
                ints_list = [1] + list(range(min(list_used_ids), max(list_used_ids) + 2))

                # compare both lists with each other and save only those ID numbers
                # that are not present in the first list in a third list
                missing_list = [x for x in ints_list if x not in list_used_ids]

                # take the lowest number of the third list, turn it into a string to display it in the application
                # and return it
                first_missing = min(missing_list)
                first_missing = str(first_missing)
                if first_missing is not None:
                    return first_missing
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # update the database when a trainer request a new password on the "Forget Password" screen
    def forgot_password_trainer(self, password, id_trainer, trainer_email):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # update the value in the column "password" where the given input matches the values in the columns
                # "id_athlete" and "mail"
                cur.execute('''UPDATE trainer SET password = %s WHERE id_trainer = %s AND mail = %s''',
                            (password, id_trainer, trainer_email))

                # count the updated rows, save the change in the database and return the count number
                change_password = cur.rowcount
                self.conn.commit()
                return change_password
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # ID of athlete at login for the global variable "id_athlete"
    def get_id_trainer(self, trainer_mail):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the ID of the trainer where the value in the column "mail" matches with a given input
                cur.execute('''SELECT id_trainer FROM trainer WHERE mail = '%s' ''' % trainer_mail)

                # take the first result of the query and return it
                trainer_id = cur.fetchone()
                return trainer_id[0]
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the information of a trainer for sending a new password
    def get_trainer(self, id_trainer):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all the rows form the table "trainer" which values in the column "id_trainer" matches with
                # the given input
                cur.execute('''SELECT * from trainer WHERE id_trainer = '%s''' % id_trainer)

                # take the first result of the query and return it
                athlete_db = cur.fetchone()
                return athlete_db
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the IDs of exercises from a particular trainer
    def id_exercises_trainer(self, id_trainer):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the IDs of exercise from the table "training" where the value in the column "id_trainer"
                # matches a given input
                cur.execute('''SELECT id_exercise from exercise WHERE id_trainer = '%s' ''' % id_trainer)

                # take all results of the query, save the first element (ID of exercise) of each result in a list
                # and return it
                training_db = cur.fetchall()
                name_possible_exercises_trainer = []
                for row in training_db:
                    name_possible_exercises_trainer.append(row[0])
                return name_possible_exercises_trainer
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # fetch the IDs of trainings from a particular trainer
    def id_trainings_trainer(self, id_trainer):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the IDs of trainings from the table "training" where the value in the column "id_trainer"
                # matches a given input
                cur.execute('''SELECT id_training from training WHERE id_trainer = %s ''' % id_trainer)

                # take all results of the query, save the first element (ID of training) of each result in a list
                # and return it
                training_db = cur.fetchall()
                name_possible_trainings_trainer = []
                for row in training_db:
                    name_possible_trainings_trainer.append(row[0])
                return name_possible_trainings_trainer
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # reveal all possible athletes to edit by trainer
    def possible_athletes_trainer(self, id_trainer):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get all values in every column of the table "athlete"
                cur.execute('''SELECT first_name, last_name from athlete WHERE id_trainer = %s 
                ORDER BY id_athlete DESC''' % id_trainer)

                # take all results of the query, save the second (first name) and third element (last name)
                # of each result in a list and return
                athlete_db = cur.fetchall()
                name_possible_athletes = []
                for row in athlete_db:
                    name_possible_athletes.append(row[0] + " " + row[1])
                return name_possible_athletes
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # reveal all exercises that a particular trainer can choose from
    def possible_exercises_trainer(self, id_trainer):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the exercise names from the table "exercise" where the value in the column "id_trainer" matches
                # with a given input
                cur.execute(
                    '''SELECT name from exercise WHERE id_trainer = '%s' ORDER BY id_exercise DESC''' % id_trainer)

                # take all results of the query, save the first element (name of exercise)
                # of each result in a list and return it
                training_db = cur.fetchall()
                possible_exercises_trainer = []
                for row in training_db:
                    possible_exercises_trainer.append(row[0])
                return possible_exercises_trainer
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # reveal all trainings that a particular trainer can choose from
    def possible_trainings_trainer(self, id_trainer):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the training names from the table "training" where the value in the column "id_trainer" matches
                # with a given input
                cur.execute('''SELECT name from training WHERE id_trainer = '%s' ORDER BY id_training DESC'''
                            % id_trainer)

                # take all results of the query, save the first element (name of training)
                # of each result in a list and return it
                training_db = cur.fetchall()
                possible_trainings_trainer = []
                for row in training_db:
                    possible_trainings_trainer.append(row[0])
                return possible_trainings_trainer
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # register a new trainer into the application by creating a new data row in the database
    def register_trainer(self, trainer_first_name, trainer_last_name, trainer_mail, password, team_name):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # add a new row in the table "trainer" with given values for the parameters
                cur.execute('''INSERT INTO trainer (first_name, last_name, mail, password, team) VALUES
                            (%s, %s, %s, %s, %s) RETURNING first_name, last_name, mail, password, team''',
                            (trainer_first_name, trainer_last_name, trainer_mail, password, team_name))

                # take this row of the query, save it into the database and return the result
                registry_trainer = cur.fetchone()
                self.conn.commit()
                return registry_trainer
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # validate trainer during the login process
    def validate_trainer(self, trainer_mail, trainer_password):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the mail and password of the trainer where the values in the columns "mail" and "password"
                # matches with a given input
                cur.execute('''SELECT mail, password FROM trainer WHERE mail = %s AND password = %s''',
                            (trainer_mail, trainer_password))

                # take the first result of the query and return it
                trainer_login = cur.fetchone()
                return trainer_login
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')


# =================================================queries for athlete==================================================
    
    # check if email already exists in database
    def check_email_athlete(self, athlete_email):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT mail FROM athlete WHERE mail = '%s' ''' % athlete_email)
                athlete_check_email = cur.fetchone()
                if athlete_check_email is not None:
                    return athlete_check_email  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            self.conn.close()  # close connection to database
            logging.info('Database connection closed.')

    
    # check if ID and email match in the database
    def check_email_id_athlete(self, id_athlete, email_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT id_athlete, mail FROM athlete WHERE id_athlete = %s AND mail = %s''',
                            (id_athlete, email_athlete))  # select data from database
                check_email_athlete = cur.fetchone()
                if check_email_athlete is not None:
                    return check_email_athlete  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # check if current password of athlete is correct
    def check_password_athlete(self, id_athlete, athlete_password):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT password FROM athlete WHERE id_athlete = %s AND password = %s''',
                            (id_athlete, athlete_password))  # select data from database
                athlete_check_password = cur.fetchone()
                if athlete_check_password is not None:
                    return athlete_check_password
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # delete workout, using id_workout
    def delete_workout_athlete(self, id_workout, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''DELETE FROM performs WHERE id_workout = %s AND id_athlete = %s''',
                            (id_workout, id_athlete))  # delete data from database
                check_delete_workout_athlete = cur.rowcount
                self.conn.commit()
                return check_delete_workout_athlete
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # select data of athlete
    def fetch_athlete(self, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT * from athlete WHERE id_athlete = '%s' ''' % id_athlete)
                athlete_db = cur.fetchone()
                return athlete_db  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # get ID of athlete at login
    def fetch_id_athlete(self, athlete_mail):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT id_athlete FROM athlete WHERE mail = '%s' ''' % athlete_mail)
                athlete_id = cur.fetchone()
                return athlete_id[0]  # return first element from selected data
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch description of exercise
    def fetch_exercise_description_athlete(self, name_of_exercise):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT description FROM exercise WHERE name = '%s' ''' % name_of_exercise)
                fetching_exercise_description = cur.fetchone()
                if fetching_exercise_description is not None:
                    return fetching_exercise_description
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch ID of exercise
    def fetch_id_exercise_athlete(self, name_exercise):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT id_exercise from exercise WHERE name = '%s' ''' % name_exercise)
                id_exercise = cur.fetchone()
                return id_exercise[0]
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch ID of training, using name of training
    def fetch_id_training_athlete(self, name_training):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT id_training from training WHERE name = '%s' ''' % name_training)
                id_training = cur.fetchone()
                return id_training[0]
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch previous workouts of athlete
    def fetch_workout_athlete(self, id_workout, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT * FROM performs WHERE id_workout = %s AND id_athlete = %s''',
                            (id_workout, id_athlete))  # select data from database
                workout = cur.fetchone()
                return workout
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch name of training, using ID of training
    def fetch_name_training_athlete(self, id_training):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute("SELECT name FROM training WHERE id_training = %s" % id_training)
                name_training = cur.fetchone()  # select data from database
                return name_training
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch name of exercise, using ID of exercise
    def fetch_name_exercise_athlete(self, id_exercise):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT name FROM exercise WHERE id_exercise = %s''' % id_exercise)
                name_exercise = cur.fetchone()  # select data from database
                return name_exercise
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch parameters of training (sets, reps, weight, distance)
    def fetch_parameters_exercise_athlete(self, id_exercise):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT sets, reps, weight, distance FROM exercise WHERE id_exercise = %s'''
                            % id_exercise)
                parameters = cur.fetchone()
                return parameters
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # fetch description of training
    def fetch_training_description_athlete(self, name_of_training):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # select data from database
                cur.execute('''SELECT description FROM training WHERE name = '%s' ''' % name_of_training)
                fetching_training_description = cur.fetchone()
                if fetching_training_description is not None:
                    return fetching_training_description
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # possible exercises for spinner
    def possible_exercises_athlete(self, id_training, id_athlete):
        try:
            self.connection()
            with self.conn.cursor() as cur:

                # get the exercise names from the table "exercise" where the value in the column "id_trainer"
                # and where the column "id_athlete" from the table "athlete" match with a given input
                cur.execute(
                    '''SELECT * from exercise WHERE id_training = %s AND
                    id_trainer = (SELECT id_trainer FROM athlete WHERE id_athlete = %s)''', (id_training, id_athlete))

                # take all results of the query, save the first element of each result in a list and return it
                training_db = cur.fetchall()
                name_possible_exercises = []
                for row in training_db:
                    name_possible_exercises.append(row[3])
                return name_possible_exercises
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()
                logging.info('Database connection closed.')

    
    # select possible IDs for workouts of athlete
    def possible_id_workouts_athlete(self, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT id_workout FROM performs WHERE id_athlete = %s ORDER BY id_workout ASC'''
                            % id_athlete)  # select data from database
                workout_db = cur.fetchall()
                id_possible_workouts = []
                for row in workout_db:
                    id_possible_workouts.append(str(row[0]))
                return id_possible_workouts  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # select trainings, which are possible for athlete
    def possible_trainings_athlete(self, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT name from training WHERE id_trainer = (SELECT id_trainer FROM athlete WHERE
                            id_athlete = %s)''' % id_athlete)  # select data from database
                training_db = cur.fetchall()
                name_possible_trainings = []
                for row in training_db:
                    name_possible_trainings.append(row[0])
                return name_possible_trainings  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # submit update of athlete
    def submit_edit_athlete(self, first_name, last_name, gender, mail, height, weight, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # update data in database
                cur.execute(
                    '''UPDATE athlete SET first_name = %s, last_name = %s, gender = %s, mail = %s, height = %s,
                    weight = %s WHERE id_athlete = %s''',
                    (first_name, last_name, gender, mail, height, weight, id_athlete))
                check_submit_edit_athlete = cur.rowcount
                self.conn.commit()
                return check_submit_edit_athlete
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # submit update of athlete including password
    def submit_edit_athlete_password(self, first_name, last_name, password, gender, mail, height, weight, id_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                # update data in database
                cur.execute(
                    '''UPDATE athlete SET first_name = %s, last_name = %s, password = %s, gender = %s, mail = %s,
                    height = %s, weight = %s WHERE id_athlete = %s''',
                    (first_name, last_name, password, gender, mail, height, weight, id_athlete))
                check_submit_edit_athlete = cur.rowcount
                self.conn.commit()
                return check_submit_edit_athlete
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # submit workout of athlete
    def submit_track_workout_athlete(self, id_workout, id_athlete, id_training, id_exercise, start_date, start_time,
                                     end_date, end_time, sets, reps, weight, distance):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                if sets == '':
                    sets = None
                if reps == '':
                    reps = None
                if weight == '':
                    weight = None
                if distance == '':
                    distance = None
                # insert data into database
                cur.execute(
                    '''INSERT INTO public.performs (id_workout, id_athlete, id_training, id_exercise, start_date,
                    start_time, end_date, end_time, sets, reps, weight, distance) VALUES (%s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s)''',
                    (id_workout, id_athlete, id_training, id_exercise, start_date, start_time, end_date, end_time, sets,
                     reps, weight, distance))
                check_track_workout = cur.fetchone
                self.conn.commit()
                return check_track_workout
        except pg8000.Error as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # update password after athlete requested new password
    def update_password_athlete(self, password, id_athlete, email_athlete):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''UPDATE athlete SET password = %s WHERE id_athlete = %s AND mail = %s''',
                            (password, id_athlete, email_athlete))  # update data in database
                change_password = cur.rowcount
                self.conn.commit()  # commit update
                if change_password is not None:
                    return change_password  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            sys.exit()
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')

    
    # check if email and password exist in database (login of athlete)
    def validate_athlete(self, athlete_mail, athlete_password):
        try:
            self.connection()  # connect to database
            with self.conn.cursor() as cur:
                cur.execute('''SELECT mail, password FROM athlete WHERE mail = %s AND password = %s''',
                            (athlete_mail, athlete_password))  # select data from database
                athlete_login = cur.fetchone()
                return athlete_login  # return selected data
        except pg8000.DatabaseError as e:
            print(e)
            return -1
        finally:
            if self.conn:
                self.conn.close()  # close connection to database
                logging.info('Database connection closed.')
