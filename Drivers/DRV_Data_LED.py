# --------------------------------------------------

"""Creation and management of the database that contains all the measurements made by the leds"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import sqlite3

# --------------------------------------------------

# Database class definition
class Database_LED:
    """Database related functions"""

# --------------------------------------------------

    def create_table(self):
        """Function that creates the table where the led data is stored"""
        conn = sqlite3.connect('data_led.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE data_led (led integer, duty_cycle integer)""")

# --------------------------------------------------

    def create_row(self, led, duty_cycle):
        """Function that creates rows inside the table"""

        conn = sqlite3.connect('data_led.db')
        c = conn.cursor()
        c.execute("INSERT INTO data_led VALUES (:led, :duty_cycle)", {'led': led, 'duty_cycle': duty_cycle})
        conn.commit()

# --------------------------------------------------

    def delete_row(self, led):
        """Function that deletes rows inside the table"""

        conn = sqlite3.connect('/home/pi/data_led.db')
        c = conn.cursor()
        c.execute("DELETE * FROM data_led WHERE led = :led", {'led': led})
        conn.commit()

# --------------------------------------------------

    def update_value(self, led, duty_cycle):
        """Function that modifies values inside the table"""

        conn = sqlite3.connect('/home/pi/data_led.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE data_led SET duty_cycle = :duty_cycle WHERE led = :led""", {'led': led, 'duty_cycle': duty_cycle})
            conn.commit()

# --------------------------------------------------

    def select_value(self, led):
        """Function that selects values inside the table"""

        conn = sqlite3.connect('/home/pi/data_led.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT duty_cycle FROM data_led WHERE led = :led", {'led': led})
            conn.commit()
            return c.fetchone()[0]

# --------------------------------------------------

if __name__ == "__main__":
    db = Database_LED()

    db.create_table()
    for counter in range(4):
       db.create_row(counter, 0)

#    data = db.select_value(2)[0]
#    print(data)

#    print(os.getcwd())

# --------------------------------------------------
