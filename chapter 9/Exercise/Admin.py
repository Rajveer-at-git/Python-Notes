class User:
    def __init__(self, first_name, last_name, age, premium_user):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.premium_user = premium_user
        self.login_attempts = 0

    def describe_user(self):
        print(f"Name: {self.first_name} {self.last_name}\nAge: {self.age}")
        if self.premium_user == False:
            print("Free tier")
        else:
            print("Premium User") 

    def greet_user(self):
        print(f"Hey {self.first_name}, welcome to our website.\n")

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0

class Privileges():
    def __init__(self):
        self.privileges = ["can add post", "can delete post", "can ban user", "can change the security"]
    
    def show_privileges(self):
        for privilege in self.privileges:
            print(privilege)

class Admin(User):
    def __init__(self,first_name, last_name, age, premium_user):
        super().__init__(first_name, last_name, age, premium_user) # no self here
        self.privilege = Privileges()
        