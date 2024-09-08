import json

class ATM:
    """
    Creates an object that represents an ATM machine with various account information
    """
    
    def __init__(self, bank_info_file_path: str):
        """
        Initialize an instace of ATM class with a .json file containing bank account information

        Args:
            bank_info_json: file path of a .json file that contains information of registered accounts
        """
        self.bank_account_info = json.load(open(bank_info_file_path))
    
    def validate_account_info(self, card_name: str, pin: str, account_type: str) -> bool:
        """
        checks the existence of an account corresponding to the given card's name, pin number, and account type

        Args:
            card_name (str): card name
            pin (int): the card's PIN number
            account_Type (str): type of account being accessed

        Returns:
            bool: whether an account corresponding to the given card's name, pin number, and account type exists
        """
        try:
            # check the existence of card's name and PIN number
            if card_name not in self.bank_account_info or pin != self.bank_account_info[card_name]["PIN"]:
                raise ValueError("There is an incorrect card name or PIN.")

            # check the existence of the specified account type
            if account_type not in self.bank_account_info[card_name]["accounts_to_balance"]:
                raise ValueError("There is an incorrect account type specified.")

        except ValueError as e:
            print(f"Error: {e}")
            return False
        
        return True

    def deposit(self, card_name: str, pin: str, account_type: str, amount: int) -> bool:
        """
        deposits a specified amount of money to an account corresponding to the given card's name, pin number, and account type

        Args:
            card_name (str): card name
            pin (int): the card's PIN number
            account_Type (str): type of account being accessed
            amount (int): amount of money to deposit

        Returns:
            bool: whether the spcified amount of money was deposited successfully
        """
        account_info_validation_result = self.validate_account_info(card_name, pin, account_type)

        if(account_info_validation_result):
            self.bank_account_info[card_name]["accounts_to_balance"][account_type] += amount

        return account_info_validation_result

    def withdraw(self, card_name: str, pin: str, account_type: str, amount: int) -> bool:
        """
        withdraws a specified amount of money to an account corresponding to the given card's name, pin number, and account type

        Args:
            card_name (str): card name
            pin (int): the card's PIN number
            account_Type (str): type of account being accessed
            amount (int): amount of money to deposit

        Returns:
            bool: whether the spcified amount of money was withdrawn successfully
        """

        account_info_validation_result = self.validate_account_info(card_name, pin, account_type)
        withdraw_result = False

        # withdrawing cannot happen if the specified amount is bigger than the existing balance
        if(account_info_validation_result):
            if(self.bank_account_info[card_name]["accounts_to_balance"][account_type] >= amount):
                self.bank_account_info[card_name]["accounts_to_balance"][account_type] -= amount
                withdraw_result = True
            else: 
                print("The amount being withdrawn is bigger than the existing balance.")

        return withdraw_result

    def get_balance(self, card_name: str, pin: str, account_type: str) -> None | int:
        """
        obtains how much balance is left within an account

        Args:
            card_name (str): card name
            pin (int): the card's PIN number
            account_Type (str): type of account being accessed

        Returns:
            int | None: existing balance within the account corresponding to the given card's name, pin number, and account type, or 
                        None if there is no account corresponding to the given card's name, pin number, and account type
        """
        account_info_validation_result = self.validate_account_info(card_name, pin, account_type)

        if(account_info_validation_result):
            return self.bank_account_info[card_name]["accounts_to_balance"][account_type]

        return None

    def user_interaction_flow(self):
        """
        implements the ATM workflow that involves an interaction with a user
        """
        exited = False

        while(not exited):
            user_action_decided = False
            user_action = None

            # check what the user will do
            while(not user_action_decided):
                user_action = input("What would you like to do? [see balance, deposit, or withdraw]")
                if(user_action == "see balance" or user_action == "deposit" or user_action == "withdraw"):
                    user_action_decided = True
                else:
                    print("Please provide your option as see balance, deposit, or withdraw.")

            # ask the user for information needed
            card_name = input("Please provide your card name: ")
            pin = input("Please provide your pin number: ")
            account_type = input("Please provide the type of the account you are using: ")
            amount = 0

            # ask for amount if the user wants to withdraw or deposit
            if(user_action != "see balance"):
                amount = int(input("Please provide the amount: "))

            # execute the user action and print out the result 
            if(user_action == "deposit"):
                deposit_result = self.deposit(card_name, pin, account_type, amount)
                if(deposit_result):
                    print(f"Successfully deposited ${amount:.2f} into the {account_type} account.")
            
            elif(user_action == "withdraw"):
                deposit_result = self.withdraw(card_name, pin, account_type, amount)
                if(deposit_result):
                    print(f"Successfully withdrew ${amount:.2f} from the {account_type} account.")

            elif(user_action == "see balance"):
                balance = self.get_balance(card_name, pin, account_type)
                if(balance != None):
                    print(f"Your {account_type} account has the balance of ${balance:.2f}.")

            # ask the user whether to continue using the ATM or not
            user_decided_to_continue_or_not = False
            while(not user_decided_to_continue_or_not):
                exit_or_continue = input("Would you like to continue using the ATM? [y or n]: ")

                if(exit_or_continue == "y"):
                    user_decided_to_continue_or_not = True
                elif(exit_or_continue == "n"):
                    exited = True
                    user_decided_to_continue_or_not = True
                else:
                    print("Please provide your option as y or n")
