# --------------------------------------------------

"""Creation and management of the database that contains all the measurements made by the sensors"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import sqlite3

# --------------------------------------------------

# Database class definition
class Database_Sensor:
    """Database related functions"""

# --------------------------------------------------

    def create_table(self):
        """Function that creates the table where the sensor data is stored"""
        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE data_ultrasonic (sensor integer, distance integer)""")

# --------------------------------------------------

    def create_row(self, sensor, distance):
        """Function that creates rows inside the table"""

        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        c.execute("INSERT INTO data_ultrasonic VALUES (:sensor, :distance)", {'sensor': sensor, 'distance': distance})
        conn.commit()

# --------------------------------------------------

    def delete_row(self, sensor):
        """Function that deletes rows inside the table"""

        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        c.execute("DELETE * FROM data_ultrasonic WHERE sensor = :sensor", {'sensor': sensor})
        conn.commit()

# --------------------------------------------------

    def update_value(self, sensor, distance):
        """Function that modifies values inside the table"""

        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE data_ultrasonic SET distance = :distance WHERE sensor = :sensor""", {'sensor': sensor, 'distance': distance})
            conn.commit()

# --------------------------------------------------

    def update_all(self, sensors, distances):
        """Function that modifies values inside the table"""

        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        with conn:
            for sensor, distance in zip(sensors, distances):
                c.execute("""UPDATE data_ultrasonic SET distance = :distance WHERE sensor = :sensor""", {'sensor': sensor, 'distance': distance})
            conn.commit()

# --------------------------------------------------
    def select_value(self, sensor):
        """Function that selects values inside the table"""

        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT distance FROM data_ultrasonic WHERE sensor = :sensor", {'sensor': sensor})
            conn.commit()
            return c.fetchone()[0]

# --------------------------------------------------

    def select_all(self):
        """Function that selects all values inside the table"""

        conn = sqlite3.connect('/home/pi/data_ultrasonic.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT * FROM data_ultrasonic")
            conn.commit()
            rows = c.fetchall()
            return [(row[0], row[1]) for row in rows]

# --------------------------------------------------

# if __name__ == "__main__":
    # db = Database()

    # db.create_table()
    # for counter in range(19):
    #     db.create_row(counter, -1)

    # data = db.select_value(0)
    # print(data[0])

# --------------------------------------------------
