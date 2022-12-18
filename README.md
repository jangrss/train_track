# train_track <br />
Main respository for the mobile application "TrainTrack" <br />

Setup:
Programming Language: Python 3.7.5
Development Environment: PyCharm Community Edition 2019.2.3
GUI-library: kivy 1.11.1
Database: PostgreSQL by ElephantSQL (https://www.elephantsql.com/) configured in queries.py
Datacenter: Google Compute Engine europe-west2 (London)
PostgreSQL interface: pg8000

Structure:
/main.py - main application
/main.kv - Kv-file to load Kv-code into main application
/kv (folder) - folder containing Kv-files with kivy language to create widget trees in declarative way (screens of app)
/graphics (folder) - folder containing graphics in png-format used in Kv-files (background, buttons, logo, navigation)
/queries.py - queries to PostgreSQL database