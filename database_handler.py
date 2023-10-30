import sqlite3
from typing import Union


class DatabaseHandler :
    filename = "user_data.db"
    table = "user_table"
    cols = (
        "id", "user_id", "total_cards", "type_ss", "type_splus", "type_s", "type_aplus", "type_a", "type_bplus",
        "type_b",
        "type_c")
    type_cols = (
        "INTEGER PRIMARY KEY", "TEXT", "INTEGER", "INTEGER", "INTEGER", "INTEGER", "INTEGER", "INTEGER", "INTEGER",
        "INTEGER", "INTEGER")
    card_types = ("ss", "s+", "s", "a+", "a", "b+", "b", "c")

    connection: sqlite3.connect = None
    cursor: sqlite3.Cursor = None

    def __init__(self, filename=None, table=None) :
        if filename :
            self.filename = filename
        if table :
            self.table = table

    # Writing Data
    def addNewUser(self, name: str) -> str :
        if name in self.getListOfUser() :
            return f"[!] Already Exist User Id : {name}"

        command = f"INSERT INTO {self.table} ({', '.join([col for col in self.cols if col != self.cols[0]])}) VALUES ({', '.join(['?' for _ in range(len(self.cols) - 1)])})"
        self.cursor.execute(command, (name, *[0 for _ in range(len(self.cols) - 2)]))
        # self.connection.commit()

        return "[/] Successfully Created"

    def updateUserData(self, user_id: str, card_type: str, added_by=1) -> str :
        if user_id not in self.getListOfUser() :
            return f"[!] Does not Exist User Id : {user_id}"

        if card_type.lower() not in self.card_types :
            return f"[!] Does not Exist Card Type : {card_type}"

        card_type = self.cols[self.card_types.index(card_type.lower()) + 3]
        command = f"UPDATE {self.table} SET {card_type} = {card_type} + ?, {self.cols[2]} = {self.cols[2]} + ?  WHERE {self.cols[1]} = ?"
        self.cursor.execute(command, (added_by, added_by, user_id))
        # self.connection.commit()
        return "[/] Successfully Updated Data"

    # Reading Data
    def getListOfUser(self) -> tuple :
        self.cursor.execute(f"SELECT {self.cols[1]} FROM {self.table}")
        return tuple(user[0] for user in self.cursor.fetchall())

    def getUserInfo(self, user_id: str) -> Union[str, tuple] :
        if user_id not in self.getListOfUser() :
            return f"[!] Does Not Exist User Id : {user_id}"
        command = f"SELECT * FROM {self.table} WHERE {self.cols[1]} = ?"
        self.cursor.execute(command, (user_id,))
        return self.cursor.fetchone()

    def readAll(self) -> list :
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()

    # Other Functions
    def connectToDatabase(self) :
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        command = f'CREATE TABLE IF NOT EXISTS {self.table} ( '
        for i in range(len(self.cols)) :
            command += f"{self.cols[i]} {self.type_cols[i]}"
            if i != len(self.cols) - 1 :
                command += ", "
        command += ")"

        self.cursor.execute(command)
        self.connection.commit()

    def close(self) :
        self.connection.close()


def consoleWindow(filename=None, table=None) :
    controller = DatabaseHandler(filename, table)
    controller.connectToDatabase()
    print(f"[/] Successfully Open Database : {controller.filename}")

    # Events
    cols = ("ID", "User", "Total", "SS", "S+", "S ", "A+", "A ", "B+", "B ", "C ")
    activities = ("add", "update", "check", "users" ,"close")
    while True :
        print("=" * 40)
        print("List of Activities : ")
        for i, activity in enumerate(activities) :
            print(f"   {i + 1} : {activity}")
        activity = input("Activity : ")

        # Checking Activity
        if not activity.isdigit() :
            print(f"[!] The Activity not in the list : {activity} ")
            continue

        activity = int(activity)
        if activity < 1 or activity > 5 :
            print(f"[!] The Activity is not in the list : {activity}")
            continue

        if activity == 1 :
            print(" Add Username ".center(40, '-'))
            username = input("Username : ")
            verification = input(f"Username \'{username}\' is correct (y/n) : ").lower()
            if verification == 'y' :
                print(controller.addNewUser(username))
            else :
                print(f"[!] Unsuccessful adding new user ")
            print(f"[?] Closing Activity ...")
        elif activity == 2 :
            print(" Update User Card ".center(40, '-'))
            username = input("Username : ")
            card_type = input("Card Type : ").lower()
            verification = input("Proceed Updating (y/n) : ").lower()
            if verification == 'y' :
                print(controller.updateUserData(user_id=username, card_type=card_type))
            print(f"[?] Closing Activity ...")
        elif activity == 3 :
            print(" Check User Info ".center(40, '-'))
            username = input("Username : ")
            information = controller.getUserInfo(user_id=username)
            if isinstance(information, str) :
                print(information)
            else :
                print("Information : ")
                for i, info in enumerate(information) :
                    print(f"    {cols[i]} : {info}")
        elif activity == 4:
            print(" Check Users ".center(40, '-'))
            users = sorted(controller.getListOfUser())
            start = ""
            for user in users :
                if start != user[0] :
                    start = user[0]
                    print(f"{start.upper()} :")
                print(f"   - {user}")
            print(f"\nTotal Users : {len(users)}")
        else :
            controller.close()
            print(f"[?] The Program is closed !!! ")
            break

        input()
        print("\n")


if __name__ == "__main__" :
    consoleWindow()


