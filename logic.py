from PyQt6.QtWidgets import *
from gui import *


class Logic(QMainWindow, Ui_FinalProject):
    def __init__(self, balance = 0):
        super().__init__()
        self.setupUi(self)



        self.__account_balance = balance

        self.input_pin.setEchoMode(QLineEdit.EchoMode.Password)

        self.hide_main_ui()

        self.hide_ui()

        self.radioButton_withdraw.setChecked(True)
        self.pushButton_submit.clicked.connect(lambda: self.submit_button())
        self.pushButton_enter.clicked.connect(lambda: self.enter_button())
        self.pushButton_log_out.clicked.connect(lambda: self.log_out())

        self.radioButton_deposit.toggled.connect(self.update_enter_button)
        self.radioButton_withdraw.toggled.connect(self.update_enter_button)
        self.update_enter_button()

        self.radioButton_sign_in.toggled.connect(self.update_submit_button)
        self.radioButton_create_account.toggled.connect(self.update_submit_button)
        self.update_submit_button()

    def submit_button(self):
        if self.radioButton_sign_in.isChecked():
            self.sign_in()
        elif self.radioButton_create_account.isChecked():
            self.create_account()

    def sign_in(self):
        account_num = self.input_account_num.text().strip()
        pin = self.input_pin.text().strip()


        try:
            with open('user_info.txt', 'r') as user_info:
                for line in user_info:
                    saved_account_num, saved_first_name, saved_last_name, saved_pin, saved_balance = line.strip().split(',')
                    if saved_account_num == account_num and saved_pin == pin:
                        self.__account_balance = float(saved_balance)
                        self.Label_welcome.show()
                        self.Label_welcome.setText(
                            f'Welcome {saved_first_name} {saved_last_name}!')
                        self.show_ui()
                        return
                self.Label_welcome.setText(
                    'We could not find your account. select on create account above to make an account.')
        except ValueError:
            self.Label_welcome.setText(
                f'We could not find your account. select on create account above to make an account.')

    def account_num(self):
        account_number = 1
        try:
            with open('user_info.txt', 'r') as user_info:
                lines = user_info.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if last_line:
                        last_account_num = int(last_line.split(',')[0])
                        account_number = last_account_num + 1
        except IOError:
            pass
        return account_number
    def create_account(self):
        first_name = self.input_first_name.text().strip()
        last_name = self.input_last_name.text().strip()
        pin = self.input_pin.text().strip()

        self.Label_welcome.show()
        self.label_account_num_2.show()


        account_number = self.account_num()
        initial_balance = 0
        user_information = f'{account_number},{first_name},{last_name},{pin},{initial_balance}'

        if self.input_first_name.text() == '' or self.input_last_name.text() == '' or self.input_pin.text() == '':
            self.Label_welcome.setText('Required information not filled, please fill in boxes')
        else:
            with open('user_info.txt', 'a+') as user_info:
                user_info.seek(0, 2)
                pos = user_info.tell()
                if pos > 0:
                    user_info.write("\n")
                user_info.write(user_information)
            self.Label_welcome.setText('Your account was created succesfully!')
            self.label_account_num_2.setText(f'You have been assigned account number {account_number}. Use it to log in.')

    def enter_button(self):
        if self.radioButton_deposit.isChecked():
            self.deposit()
        elif self.radioButton_withdraw.isChecked():
            self.withdraw()

    def withdraw(self):
        try:
            amount = float(self.input_amount_text.text())
        except ValueError:
            self.Label_account_balance.setText('Please enter numeric value')
            return

        if amount <= 0:
            self.Label_account_balance.setText('You currently have $0 or less in your account')
        elif amount > self.__account_balance:
            self.Label_account_balance.setText('You cannot withdraw more than your current account balance')
        else:
            total = self.__account_balance - amount
            self.set_balance(total)
            self.Label_account_balance.setText(f'You successfully withdrew ${amount:.2f} Your account balance is now ${total:.2f}')
            self.update_balance()




    def deposit(self):
        try:
            amount = float(self.input_amount_text.text())
        except ValueError:
            self.Label_account_balance.setText('Please enter numeric value')
            return

        if amount <= 0:
            self.Label_account_balance.setText('You need to deposit more than $0')
        else:
            total = self.__account_balance + amount
            self.set_balance(total)
            self.Label_account_balance.setText(f'You successfully deposited ${amount:.2f} Your account balance is now ${total:.2f}')
            self.update_balance()

    def set_balance(self, value):
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def update_balance(self):
        account_num = self.input_account_num.text().strip()
        pin = self.input_pin.text().strip()

        lines = []
        try:
            with open('user_info.txt', 'r') as user_info:
                lines = user_info.readlines()

            with open('user_info.txt', 'w') as user_info:
                for line in lines:
                    saved_account_num, saved_first_name, saved_last_name, saved_pin, saved_balance = line.strip().split(',')
                    if saved_account_num == account_num and saved_pin == pin:
                        updated_line = f'{saved_account_num}, {saved_first_name},{saved_last_name},{saved_pin},{self.__account_balance:.2f}\n'
                        user_info.write(updated_line)
                    else:
                        user_info.write(line)
        except IOError:
            pass
    def update_enter_button(self):
        if self.radioButton_deposit.isChecked():
            self.input_amount_text.clear()
            self.Label_account_balance.clear()
            self.pushButton_enter.setText('Deposit')
        elif self.radioButton_withdraw.isChecked():
            self.Label_account_balance.clear()
            self.input_amount_text.clear()
            self.pushButton_enter.setText('Withdraw')
        else:
            self.pushButton_enter.setText('Enter')
    def update_submit_button(self):
        if self.radioButton_sign_in.isChecked():
            self.input_account_num.show()
            self.label_account_num.show()
            self.input_pin.show()
            self.label_pin.show()
            self.pushButton_submit.show()



            self.input_first_name.hide()
            self.input_last_name.hide()
            self.label_first_name.hide()
            self.label_last_name.hide()
            self.label_account_num_2.hide()
            self.Label_welcome.hide()

            self.input_first_name.clear()
            self.input_last_name.clear()
            self.input_pin.clear()
            self.pushButton_submit.setText('Log In')
        elif self.radioButton_create_account.isChecked():
            self.input_first_name.show()
            self.input_last_name.show()
            self.label_first_name.show()
            self.label_last_name.show()
            self.input_pin.show()
            self.label_pin.show()
            self.pushButton_submit.show()

            self.input_account_num.hide()
            self.label_account_num.hide()

            self.input_first_name.clear()
            self.input_last_name.clear()
            self.input_pin.clear()
            self.Label_welcome.clear()
            self.pushButton_submit.setText('Create Account')

    def log_out(self):
        self.clear_text()
        self.hide_ui()
        self.radioButton_sign_in.setChecked(True)

    def hide_main_ui(self):
        self.input_first_name.hide()
        self.input_last_name.hide()
        self.label_first_name.hide()
        self.label_last_name.hide()
        self.input_account_num.hide()
        self.label_account_num.hide()
        self.label_pin.hide()
        self.input_pin.hide()
        self.pushButton_submit.hide()
    def hide_ui(self):
        self.radioButton_deposit.hide()
        self.radioButton_withdraw.hide()
        self.label_amount.hide()
        self.input_amount_text.hide()
        self.pushButton_enter.hide()
        self.pushButton_log_out.hide()
    def show_ui(self):
        self.radioButton_deposit.show()
        self.radioButton_withdraw.show()
        self.label_amount.show()
        self.input_amount_text.show()
        self.pushButton_enter.show()
        self.pushButton_log_out.show()
    def clear_text(self):
        self.input_first_name.clear()
        self.input_last_name.clear()
        self.input_pin.clear()
        self.Label_welcome.clear()
        self.Label_account_balance.clear()
        self.input_amount_text.clear()
        self.input_account_num.clear()
