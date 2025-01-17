class User:
    def __init__(self, username, role="user"):
        self.username = username
        self.role = role

    def display_info(self):
        print(f"Имя:{self.username},Роль:{self.role}")

    def read_data(self):
        if self.has_permission("read"):
            print("Чтение данных из базы...")
        else:
            print("Недостаточно прав для чтения данных.")

    def write_data(self):
        if self.has_permission("write"):
            print("Запись данных в базу...")
        else:
            print("Недостаточно прав для записи данных.")

    def has_permission(self, action):
        return action == "read"


class Manager(User):
    def __init__(self, username):
        super().__init__(username, role="manager")

    def write_data(self):
        if self.has_permission("write"):
            print("Запись данных в базу...")
        else:
            print("Недостаточно прав для записи данных.")

    def has_permission(self, action):

        return action in ["read", "write"]


class Admin(Manager):
    def __init__(self, username):
        super().__init__(username)

    def delete_data(self):
        if self.has_permission("delete"):
            print("Удаление данных из базы...")
        else:
            print("Недостаточно прав для удаления данных.")

    def has_permission(self, action):
        # Admin имеет права на все действия
        return True


user1 = User("Alis", "admin")
user1.display_info()
user1.read_data()
user1.write_data()
user1.write_data()

manager1 = Manager("Bob")
manager1.display_info()
manager1.read_data()
manager1.write_data()

admin1 = Admin("Charlie")
admin1.display_info()
admin1.read_data()
admin1.write_data()
admin1.delete_data()
