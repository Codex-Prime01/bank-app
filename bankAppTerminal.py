import random
import json

class Account:

    def __init__(self, accountNumber, accountHolderName, balance):
        self.accountNumber =  accountNumber
        self. accountHolderName = accountHolderName
        self.balance = balance


    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f'\n{self.accountHolderName},you have successfully deposited ₦{amount:2f} \n to your account {self.accountNumber}')
            print(f'Your total balance is ₦{self.balance}')
            return True
        else:
            print('\nYour amount must be positive')
            return False

    def withdraw(self, amount):
        if amount > self.balance:
            print("InSufficient Funds")
            return False
        if amount <= 0 :
            print('The amount must be positive')
            return False
        self.balance -= amount
        print(f'Withdrew ₦{amount:.2f} from your account \n Your balance is now ₦{self.balance}')
        return True

    def getBalance(self):
        return self.balance

    def getAccountNumber(self):
        return self.accountNumber


    def __str__(self):
        return (f'Account Number: {self.accountNumber}\n'
                f'Account Name: {self.accountHolderName}\n'
                f'Balance:  ₦{self.balance:2f}')

class SavingsAccount(Account):
    def __init__(self, accountNumber, accountHolderName, balance, interestRate):
        super().__init__(accountNumber,accountHolderName , balance)
        self.interestRate = interestRate

    def addInterest(self):
        interest = self.balance * self.interestRate
        self.balance += interest
        print(f"Interest of ₦{interest:.2f}added to {self.accountHolderName}'s account ")

    def __str__(self):
        return (super().__str__() +
                f"\nAccount Type: Savings\n"
                f"Interest Rate: {self.interestRate * 100:.2f}%")


class CheckingAccount(Account):
    def __init__(self,accountNumber ,accountHolderName, balance, overdraftLimit):
        super().__init__(accountNumber,accountHolderName, balance)
        self.overdraftLimit = overdraftLimit

        #polymorphism is  the act of overriding a method from another base
    def withdraw(self, amount):
        if amount <= 0:
            print('Withdrawal amount must be positive')
            return False
        if amount > (self.balance + self.overdraftLimit):
            print('Withdrawal exceeds overdraft limit.')
            return False
        self.balance -= amount
        print(f"{self.accountHolderName}, you withdrew, ₦{amount:.2f} successfully ")
        return True


    def __str__(self):
        return (super().__str__() +
                f"\n Account Type: Checking \n"
                f"Overdraft Limit: ₦{self.overdraftLimit:.2f}\n")


class Bank:
    def __init__(self):
        self.accounts = {}
        self.logged_in_account = None  # store the current logged-in account number

    def createAccount(self, accountType, accountHolderName, balance, **kwargs):
        accountNumber = ''.join(str(random.randint(0, 9)) for _ in range(11))
        accountNumber = f"{''.join(accountHolderName.upper()[0:3])}-{''.join(accountNumber[0:4])}-{''.join(accountNumber[4:7])}-{''.join(accountNumber[7:11])}"
        print(f"This is your account number: {accountNumber}")

        if accountType == "savings":
            account = SavingsAccount(accountNumber, accountHolderName, balance, kwargs.get("interestRate", 0.01))

        elif accountType == "checking":
            overdraftLimit = kwargs.get("overdraftLimit", 500.0)
            account = CheckingAccount(accountNumber,accountHolderName, balance, overdraftLimit)

        else:
            raise ValueError('Invalid account  type')

        self.accounts[accountNumber] = account
        print(f"Account created successfully. Account Number: {accountNumber}")
        return accountNumber

    def deposit(self, accountNumber, amount):
        account = self.accounts.get(accountNumber)
        if account:
            account.deposit(amount)

        else:
            print('Account not found')


    def withdraw(self, accountNumber, amount):
        account = self.accounts.get(accountNumber)

        if account:
            account.withdraw(amount)
        else:
            print('Account  not found')



    def transfer(self, fromAccountNo, toAccountNo,amount):
        if fromAccountNo not in  self.accounts:
            print(f"{fromAccountNo} not found")
            return False

        elif toAccountNo not in self.accounts:
            print(f"{toAccountNo} not found")
            return False

        elif fromAccountNo not in self.accounts or toAccountNo not in self.accounts:
            print(f"Both accounts are not found")
            return False

        if self.accounts[fromAccountNo].withdraw(amount):
            self.accounts[toAccountNo].deposit(amount)

            print(f"Successfully transferred ₦{amount:.2f} from {fromAccountNo} to {toAccountNo}.")
            return True


    def getAccountBalance(self, accountNumber):
        account = self.accounts.get(accountNumber)
        if account:
            print(f"Balance: ₦{account.getBalance():.2f}")

        else:
            print('Account not found')


    def listAllAccounts(self):
        for acc in self.accounts.values():
            print(f'\n{"-" * 30}')
            print(acc)
        else:
            print("There are no accounts yet")

    def deleteAccount(self,accountNumber):
        if not self.accounts:
            print("There is no account to delete")
        try:
            for acc in self.accounts.values():
                no = acc.getAccountNumber()
                name = acc.accountHolderName
            if accountNumber == no:
                question = input(f"\nAre you sure you want to delete {name}'s account (Y/N): ").lower()
                if question == "y":
                    del self.accounts[no]
                    print(f"You have deleted {name}'s account")
                else:
                    print("Thanks for staying with us")

            else:
                print("It is incorrect")

        except ValueError:
            print("Please enter a valid account number")

    def login(self):
        self.loadData()
        acc_num = input("Account Number: ")
        for acc in self.accounts.values():
            no = acc.getAccountNumber()
            name = acc.accountHolderName
        if  acc_num == no:  
            confirm = input(f"Is This your account name '{name}' (Y/N): ").lower()
            if confirm == "y":
                self.logged_in_account = acc_num
                print(f"\n {name}, Welcome to Codex Bank!\n")
                print("\n--- Codex Bank --- \n"
                      "1. Deposit \n"
                      "2. Withdraw\n"
                      "3. Transfer\n"
                      "4. Check Balance\n"
                      "5. Delete Accoount\n"
                      "6. Exit\n")
                self.choice()
            elif confirm == "n":
                print("Input your account number again")
                self.login()
            else:
                print("Invalid Input")
                self.login()
        else:
            print("Account not found")

    def saveData(self, filename="bankData.json"):
        data = []
        for acc in self.accounts.values():
            accType = "savings" if isinstance(acc, SavingsAccount) else "checking"
            accData = {
                "type" : accType,
                "accountNumber": acc.getAccountNumber(),
                "name": acc.accountHolderName,
                "balance" : acc.getBalance(),
                "interestRate" : getattr(acc, "interestRate", None),
                "overdraftLimit" : getattr(acc, "overdraftLimit", None)
            }

            data.append(accData)
        with open(filename, "w") as f:
            json.dump(data, f,indent=4)

    def loadData(self, filename = "bankData.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            for accData in data:
                if accData["type"] == "savings":
                    acc = SavingsAccount(
                        accData["accountNumber"],
                        accData["name"],
                        accData["balance"],
                        accData["interestRate"]
                    )

                elif accData["type"] == "checking":
                    acc = CheckingAccount(
                        accData["accountNumber"],
                        accData["name"],
                        accData["balance"],
                        accData["overdraftLimit"]
                    )
                self.accounts[accData["accountNumber"]] = acc

        except FileNotFoundError:
            print("No saved  data found")

    def menu(self):
        question = input("\n\tDo you wish to continue to main menu (or to exit) (y) or (n) ").lower()
        if question != "y":
            return None
        else:
            self.choice()


    def choice(self):
        self.loadData()
        #bank.login(getattr("acc-Num"))

        choice = input("\n\nChoose an  option: ")

        try:
            if choice == "1":
                if not self.logged_in_account:
                    print("You mus be logged in first.")
                    return

                amount = float(input("Amount to deposit: "))
                confirm = input(f"Are you sure you want to deposit ₦{amount} (Y/N): ").lower()
                if confirm == "y":
                    self.deposit(self.logged_in_account, amount)
                    self.saveData()
                    self.menu()
                else:
                    self.choice()


            elif choice == "2":
                if  not self.logged_in_account:
                    print("You must be logged in first")
                    return

                amount = float(input("Amount to withdraw: "))
                confirm = input(f"Are you sure you want to withdraw ₦{amount} (Y/N): ").lower()
                if confirm == "y":
                    self.withdraw(self.logged_in_account, amount)
                    self.saveData()
                    self.menu()
                else:
                    self.choice()

            elif choice == "3":
                if not self.logged_in_account:
                    print("You  must be logged in first")
                    return

                to_acc = input("To Account Number: ")
                amount = float(input("Amount to transfer: "))
                confirm = input(f"Are you sure you want to transfer ₦{amount} (Y/N): ").lower()
                if confirm == "y":
                    self.transfer(self.logged_in_account, to_acc, amount)
                    self.saveData()
                    self.menu()
                else:
                    self.choice()


            elif choice == "4":
                if not self.logged_in_account:
                    print("You  must be logged in first")
                    return

                self.getAccountBalance(self.logged_in_account)
                self.saveData()
                self.menu()

            elif choice == "5":
                if not self.logged_in_account:
                    print("You  must be  logged in firsy")
                    return

                self.deleteAccount(self.logged_in_account)
                self.saveData()
                self.menu()


            elif choice == "6":
                self.saveData()
                confirm = input(f"Are you sure you want to exit (Y/N): ").lower()
                if confirm == "y":
                    print("Goodbye 🖐👌.")
                    self.saveData()
                    self.menu()
                else:
                    self.choice()

            else:
                print("Invalid option.")
                self.choice()

        except ValueError:
            print("Invalid input. Please enter correct values.")
            self.choice()


def runBankApp():
    bank = Bank()
    bank.loadData()

    while True:
        print("\n--- Codex Bank --- \n"
              "1. Create Account \n"
              "2. Login\n"
              "3. List All Accounts\n"
              "4. Exit\n"
              "(Choose from 1 - 4)")

        choice = input("\n\nChoose an option: ")
        try:
            if choice == "1":
                accType = input("Account Type "
                                "\n    For savings account  (s) "
                                "\n    For current account  (c): ").lower()
                name = input("Account Holder Name: ").capitalize()
                balance = float(input("Initial Balance: "))

                if accType == "s":
                    accType = "savings"
                    rate = float(input("Interest Rate (e.g. 0.01 for 1%): "))
                    if rate == " ":
                        interestRate = rate
                    bank.createAccount(accType, name, balance, interestRate=rate)


                elif accType == "c":
                    accType = "checking"
                    limit = float(input("Overdraft Limit: "))
                    bank.createAccount(accType, name, balance, overdraftLimit=limit)

                else:
                    print("Invalid account type.")
                bank.saveData()

            elif choice == "2":
                bank.login()


            elif choice == "3":
                bank.listAllAccounts()

            elif choice == "4":
                bank.saveData()
                confirm = input(f"Are you sure you want to exit (Y/N): ").lower()
                if confirm == "y":
                    print("Goodbye 🖐👌.")
                    break
                    bank.saveData()

                else:
                    runBankApp()
            else:
                print("It is invalid")




        except ValueError:
            print("Invalid input. Please enter correct values.")
            bank.choice()




if __name__ == "__main__":
    runBankApp()




