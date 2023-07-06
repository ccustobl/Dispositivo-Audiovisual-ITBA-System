# --------------------------------------------------

"""Creation and management of the database that contains all the measurements made by the mics"""
# Author: Custo Blanch, Christian
# Project: Overhead Projector Phase 2
# ITBA

# --------------------------------------------------

# Imports
import sqlite3

# --------------------------------------------------

# Database class definition
class Database_Mic:
    """Database related functions"""

# --------------------------------------------------

    def create_table(self):
        """Function that creates the table where the mic data is stored"""
        conn = sqlite3.connect('data_mic.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE data_mic (mic integer, meassurement integer)""")

# --------------------------------------------------

    def create_row(self, mic, meassurement):
        """Function that creates rows inside the table"""

        conn = sqlite3.connect('data_mic.db')
        c = conn.cursor()
        c.execute("INSERT INTO data_mic VALUES (:mic, :meassurement)", {'mic': mic, 'meassurement': meassurement})
        conn.commit()

# --------------------------------------------------

    def delete_row(self, mic):
        """Function that deletes rows inside the table"""

        conn = sqlite3.connect('/home/pi/data_mic.db')
        c = conn.cursor()
        c.execute("DELETE * FROM data_mic WHERE mic = :mic", {'mic': mic})
        conn.commit()

# --------------------------------------------------

    def update_value(self, mic, meassurement):
        """Function that modifies values inside the table"""

        conn = sqlite3.connect('/home/pi/data_mic.db')
        c = conn.cursor()
        with conn:
            c.execute("""UPDATE data_mic SET meassurement = :meassurement WHERE mic = :mic""", {'mic': mic, 'meassurement': meassurement})
            conn.commit()

# --------------------------------------------------

    def select_value(self, mic):
        """Function that selects values inside the table"""

        conn = sqlite3.connect('/home/pi/data_mic.db')
        c = conn.cursor()
        with conn:
            c.execute("SELECT meassurement FROM data_mic WHERE mic = :mic", {'mic': mic})
            conn.commit()
            return c.fetchone()[0]

# --------------------------------------------------

if __name__ == "__main__":
    db = Database_Mic()

    db.create_table()
    for counter in range(2):
        db.create_row(counter, 0)

#    data = db.select_value(2)[0]
#    print(data)

#    print(os.getcwd())

# --------------------------------------------------
