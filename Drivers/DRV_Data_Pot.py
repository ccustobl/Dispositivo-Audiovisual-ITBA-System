# --------------------------------------------------

"""Creation and management of the database that contains all the measurements made by the potentiometers"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import sqlite3

# --------------------------------------------------

# Database class definition
class Database_Pot:
    """Database related functions"""

# --------------------------------------------------

    def create_table(self):
        """Function that creates the table where the potentiometer data is stored"""
        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE data_pot (potentiometer integer, meassurement integer, meassurement_old integer)""")

# --------------------------------------------------

    def create_row(self, potentiometer, meassurement, meassurement_old):
        """Function that creates rows inside the table"""

        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        c.execute("INSERT INTO data_pot VALUES (:potentiometer, :meassurement, :meassurement_old)", {'potentiometer': potentiometer, 'meassurement': meassurement, 'meassurement_old': meassurement_old})
        conn.commit()

# --------------------------------------------------

    def delete_row(self, potentiometer):
        """Function that deletes rows inside the table"""

        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        c.execute("DELETE * FROM data_pot WHERE potentiometer = :potentiometer", {'potentiometer': potentiometer})
        conn.commit()

# --------------------------------------------------

    def update_value_col1(self, potentiometer, meassurement):
        """Function that modifies values inside the table"""

        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE data_pot SET meassurement = :meassurement WHERE potentiometer = :potentiometer""", {'potentiometer': potentiometer, 'meassurement': meassurement})
            conn.commit()

# --------------------------------------------------

    def update_value_col2(self, potentiometer, meassurement_old):
        """Function that modifies values inside the table"""

        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE data_pot SET meassurement_old = :meassurement_old WHERE potentiometer = :potentiometer""", {'potentiometer': potentiometer, 'meassurement_old': meassurement_old})
            conn.commit()

# --------------------------------------------------

    def select_value_col1(self, potentiometer):
        """Function that selects values inside the table"""

        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT meassurement FROM data_pot WHERE potentiometer = :potentiometer", {'potentiometer': potentiometer})
            conn.commit()
            return c.fetchone()[0]

# --------------------------------------------------

    def select_value_col2(self, potentiometer):
        """Function that selects values inside the table"""

        conn = sqlite3.connect('/home/pi/data_pot.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT meassurement_old FROM data_pot WHERE potentiometer = :potentiometer", {'potentiometer': potentiometer})
            conn.commit()
            return c.fetchone()[0]

# --------------------------------------------------

if __name__ == "__main__":
    db = Database_Pot()

    db.create_table()
    for counter in range(4):
       db.create_row(counter, 0, 0)

#    data = db.select_value(2)[0]
#    print(data)

#    print(os.getcwd())

# --------------------------------------------------
