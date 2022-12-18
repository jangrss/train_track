# **********************************************************************************************************************
# Name of Application: TrainTrack
# Version: 1.0
# Date created: 2020/01/28
# Developer: Johannes Breitenbach 79493 (JB), Jan Gross 61318 (JG), Filmon Mesgun 79513 (FM)
# (Code sections of each developer are marked by initials)
#
# Setup:
# Programming Language: Python 3.7.5
# Development Environment: PyCharm Community Edition 2019.2.3
# GUI-library: kivy 1.11.1
# Database: PostgreSQL by ElephantSQL (https://www.elephantsql.com/) configured in queries.py
# Datacenter: Google Compute Engine europe-west2 (London)
# PostgreSQL interface: pg8000
# **********************************************************************************************************************

# **********************************************************************************************************************
# insert lines for insert statements exceed the margin of 120 (acc. PEP 8) to achieve sufficient formatting in database
# references used for training and exercise description are mentioned before each statement
# **********************************************************************************************************************


# import pure-python interface to the PostgreSQL database engine
import pg8000

'''===============================================Database Connection================================================'''
connection = pg8000.connect(
    database=None,
    user=None,
    password=None,
    host=None,
    port=None
) #anonymized
print('connected to postgreSQL')

cur = connection.cursor()

'''======================================SQL Queries for TrainTrack SCA Example======================================'''
queries = (
    # table for trainer
    '''CREATE TABLE trainer
    (id_trainer SERIAL,
     first_Name VARCHAR(255) NOT NULL,
     last_Name VARCHAR(255) NOT NULL,
     mail VARCHAR(255) NOT NULL UNIQUE,
     password TEXT NOT NULL,
     team TEXT NOT NULL,
     PRIMARY KEY (id_trainer)
    );''',

    # table for athlete
    '''CREATE TABLE athlete
    (id_athlete SERIAL,
     id_trainer INT NOT NULL, 
     first_name VARCHAR(255) NOT NULL,
     last_name VARCHAR(255) NOT NULL, 
     password TEXT NOT NULL,
     gender VARCHAR(10) NOT NULL,
     mail VARCHAR(255) NOT NULL UNIQUE,
     height DECIMAL NOT NULL,
     weight DECIMAL NOT NULL,
     PRIMARY KEY (id_athlete),
     FOREIGN KEY (id_trainer) REFERENCES trainer (id_trainer) ON UPDATE CASCADE ON DELETE CASCADE
    );''',

    # table for training
    '''CREATE TABLE training
    (id_training SERIAL,
     id_trainer INT NOT NULL,
     name VARCHAR(255) NOT NULL UNIQUE,
     description TEXT,
     PRIMARY KEY (id_training),
     FOREIGN KEY (id_trainer) REFERENCES trainer (id_trainer) ON UPDATE CASCADE ON DELETE CASCADE
    );''',

    # table for exercise
    '''CREATE TABLE exercise
    (id_exercise SERIAL,
     id_training INT NOT NULL,
     id_trainer INT NOT NULL,
     name VARCHAR(255) NOT NULL UNIQUE,
     description TEXT,
     sets BOOLEAN NOT NULL,
     reps BOOLEAN NOT NULL,
     weight BOOLEAN NOT NULL,
     distance BOOLEAN NOT NULL,
     PRIMARY KEY (id_exercise),
     FOREIGN KEY (id_trainer) REFERENCES trainer (id_trainer) ON UPDATE CASCADE ON DELETE CASCADE,
     FOREIGN KEY (id_training) REFERENCES training (id_training) ON UPDATE CASCADE ON DELETE CASCADE
    );''',

    # table performs including performed workouts
    '''CREATE TABLE performs
    (id_workout INT,
     id_athlete INT,
     id_training INT,
     id_exercise INT,
     start_date DATE not NULL,
     start_time TIME NOT NULL,
     end_date DATE NOT NULL,
     end_time TIME NOT NULL,
     Sets INT,
     Reps INT,
     Weight DECIMAL,
     Distance DECIMAL,
     PRIMARY KEY (id_athlete,id_workout),
     FOREIGN KEY (id_athlete) REFERENCES athlete (id_athlete) ON UPDATE CASCADE ON DELETE CASCADE,
     FOREIGN KEY (id_training) REFERENCES training (id_training) ON UPDATE CASCADE ON DELETE CASCADE,
     FOREIGN KEY (id_exercise) REFERENCES exercise (id_exercise) ON UPDATE CASCADE ON DELETE CASCADE
    );''',

    # deletes all records in the existing tables and resets the serial keys (IDs)
    '''TRUNCATE TABLE trainer RESTART IDENTITY CASCADE;''',
    '''TRUNCATE TABLE athlete RESTART IDENTITY CASCADE;''',
    '''TRUNCATE TABLE training RESTART IDENTITY CASCADE;''',
    '''TRUNCATE TABLE exercise RESTART IDENTITY CASCADE;''',
    '''TRUNCATE TABLE performs RESTART IDENTITY CASCADE;''',

    # insert the example data set into the existing tables

    # insert trainer "Marc Fernandes"
    '''INSERT INTO trainer(first_name, last_name, mail, password, team) 
    VALUES ('Marc', 'Fernandes', 'm.fernandes@sca.de', 'analytics20', 'SC Analytics');''',

    # insert athletes "Johannes Breitenbach" and "Filmon Mesgun"
    '''INSERT INTO athlete(id_trainer, first_name, last_name, password, gender, mail, height, weight)
    VALUES (1, 'Johannes', 'Breitenbach', 'perform19', 'male', 'j.breitenbach@sca.de', '1.88', '88');''',
    '''INSERT INTO athlete(id_trainer, first_name, last_name, password, gender, mail, height, weight)
    VALUES (1, 'Filmon', 'Mesgun', 'perform19', 'male', 'f.mesgun@sca.de', '1.77', '77');''',
    '''INSERT INTO athlete(id_trainer, first_name, last_name, password, gender, mail, height, weight)
    VALUES (1, 'Jan', 'Gross', 'perform19', 'male', 'j.gross@sca.de', '1.88', '88');''',

    # insert training "Coordination
    '''INSERT INTO training(name, id_trainer, description)
    VALUES ('Coordination', 1, 'Coordination is the ability to execute smooth, accurate, and controlled motor responses. It is the process that results in activation of motor units of multiple muscles with simultaneous inhibition of all other muscles.');''',

    # insert exercise "Side Plank Raises" (reference: https://completenutrition.com/blogs/news/exercises-to-improve-coordination)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (1, 1, 'Side Plank Raises', 'A basic isometric side plank, in which you hold the pose for 30 to 60 seconds. On an exhale, lift your left leg up as high as you can, keeping it straight. Inhale and slowly lower the leg. Perform 4 sets: 15 reps on each side.', TRUE, TRUE, FALSE, FALSE);''',

    # insert exercise "Weighted Balancing" (reference: https://completenutrition.com/blogs/news/exercises-to-improve-coordination)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (1, 1, 'Weighted Balancing', 'Hold a dumbbell in one hand and raise the foot on the same side off the ground. Perform 3 sets: 12 curls, keeping the leg raised the entire time.', TRUE, TRUE, TRUE, FALSE);''',

    # insert exercise "Jumping Rope" (reference: https://www.sportsrec.com/498619-examples-coordination-exercises.html)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (1, 1, 'Jumping Rope', 'Run in place while spinning the rope, hop on one foot, alternate kicking one foot out and cross the rope in front of you. Perform 4 sets: 60s each.', TRUE, FALSE, FALSE, FALSE);''',

    # insert exercise "Racquet Ball" (reference: https://www.sportsrec.com/498619-examples-coordination-exercises.html)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (1, 1, 'Racquet Ball', 'Drop-and-Hit: Stand at the receiving line, approximately two and a half steps from the sidewall. Perform 5 sets: 20 drop-and-hit each with the forehand and your backhand.', TRUE, TRUE, FALSE, FALSE);''',

    # insert training "Endurance"
    '''INSERT INTO training(name, id_trainer, description)
    VALUES ('Endurance', 1, 'Cardiovascular fitness is the ability of the heart and lungs to supply oxygen-rich blood to the working muscle tissues, and the ability of the muscles to use oxygen to produce energy for movement.');''',

    # insert exercise "Tabata Jump Squats" (reference: http://www.exercisemenu.com/squat-jump-4-minute-workout/)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (2, 1, 'Tabata Jump Squats', 'The tabata format requires you to exercise at 100% effort for 20 seconds, followed by 10 seconds of rest, which does build one set. For the 20 seconds of activity, perform regular jump-squats with a high frequency. Perform 10 sets.', TRUE, FALSE, FALSE, FALSE);''',

    # insert exercise "Kettlebell Swings" (reference: https://www.t-nation.com/training/kettlebell-swings-youre-doing-them-wrong)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (2, 1, 'Kettlebell Swings', 'Kettlebell swing is a basic ballistic exercise used to train the posterior chain in a manner similar to broad jumping. It involves moving the bell in a pendulum motion. Perform 5 sets: 20 reps each with maximum weight.', TRUE, TRUE, TRUE, FALSE);''',

    # insert exercise "Indoor Rowing" (reference: https://www.mensjournal.com/health-fitness/5-rowing-workouts-get-you-ripped/)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (2, 1, 'Indoor Rowing', 'A great non-weight-bearing exercise machine. A rowing machine uses both your upper- and lower-body muscles to increase cardiovascular conditioning. Perform 5 sets: 500m each with maximum weight.', TRUE, FALSE, TRUE, TRUE);''',

    # insert exercise "Interval Running" (reference: https://www.roadrunnersports.com/blog/interval-training/)
    '''INSERT INTO exercise(id_training, id_trainer, name, description, sets, reps, weight, distance)
    VALUES (2, 1, 'Interval Running', 'Interval running alternates between periods of intense, fast paces followed by less intense recovery periods. Perform a total distance of 3km: Sprint for 200m and slow down to a jog for 400m.', FALSE, FALSE, FALSE, TRUE);'''
    )

'''===========================================End the Database Transaction==========================================='''
# make changes available by ending the transaction
try:
    for query in queries:
        cur.execute(query)
    cur.close()
    connection.commit()

# display database errors appearing during the transaction
except (Exception, pg8000.DatabaseError) as error:
    print(error)
