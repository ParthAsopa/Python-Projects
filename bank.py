class Bank:
    def __init__(self, balance, name):
        self.balance = balance
        self.name = name

    def deposit(self, amt):
        self.balance += amt

    def withdraw(self, amt):
        self.balance -= amt

    def disp(self):
        print(f"Current ammount: {self.balance}")


if __name__ == "__main__":
    name = input("Enter name: ")
    amt = int(input("Enter initial balance: "))
    user = Bank(amt, name)
    user.disp()
    user.deposit(745)
    user.disp()
    user.withdraw(700)
    user.disp()
