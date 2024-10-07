import sqlite3
from random import randint

card_table = "CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER);"
insert_card = "INSERT INTO card (id, number, pin, balance) VALUES (?, ?, ?, ?);"
card_number_pin = "SELECT number, pin FROM card;"
card_number = "SELECT number FROM card;"
all_table = 'SELECT * FROM card'
card_balance = "SELECT balance FROM card;"
find_balance = "SELECT balance FROM card WHERE number = ?;"
user_delete = "DELETE FROM card WHERE number = ?;"
resever_check = 'SELECT count(*) FROM card WHERE number = ?;'


def connect():
    return sqlite3.connect('card.s3db')


def create_table(connection):
    with connection:
        connection.execute(card_table)


def add_card(cur, id, number, pin, balance):
    cur.execute(insert_card, (id, number, pin, balance))


def all_numbers_pins(cur):
    return cur.execute(card_number_pin).fetchall()


def all_numbers(cur):
    return cur.execute(card_number).fetchall()


def all_balacnce(cur):
    return cur.execute(card_balance).fetchall()


class CreateAccount:
    def __init__(self):
        self.card_number = 0
        self.intn = 0
        self.password = 0
        self.numbers = []
        self.check = 0
        self.last = 0
        self.last_dig = 0
        self.usern = []
        self.balance = 0
        self.for_time = 0
        self.conn = connect()
        self.cur = self.conn.cursor()
        self.number_check = False
        self.pin_check = False
        self.both = False
        self.balance_cal = 0
        self.in_table = True

    def RandomCard(self):
        self.numbers = []
        self.usern = []
        self.check = 0
        odd = True
        a = randint(0000000000, 9999999999)
        self.card_number = (4000000000000000 + a)
        for w in str(self.card_number):
            self.numbers.append(w)
        for y in self.numbers:
            if odd:
                self.check = int(y) * 2
                if self.check > 9:
                    self.check -= 9
                self.usern.append(int(self.check))
            else:
                self.usern.append(int(y))
            if odd:
                odd = False
            else:
                odd = True
            self.check = 0
        odd = True
        self.numbers = []
        self.check = 0
        for z in range(15):
            self.check += self.usern.pop(0)
        if self.check % 10 != 0:
            self.last = round(self.check / 10) * 10
            if self.last > self.check:
                self.card_number = ((int(self.card_number / 10)) * 10) + self.last - self.check
            else:
                self.last += 10
                self.card_number = ((int(self.card_number / 10)) * 10) + self.last - self.check
        else:
            self.card_number = ((int(self.card_number / 10)) * 10) + self.last - self.check
        self.password = ''.join([str(randint(0, 9)) for x in range(4)])
        print(f'''
Your card has been created
Your card number:
{self.card_number}
Your card PIN:
{self.password}''')
        self.user = self.card_number
        self.pin = self.password
        add_card(self.cur, 1, self.card_number, self.password, self.balance)
        self.conn.commit()

    def card_Luhn(self, card):
        self.numbers = []
        self.usern = []
        self.check = 0
        odd = True
        for s in str(card):
            self.numbers.append(s)
        self.last_dig = int(self.numbers.pop())
        self.numbers = []
        for w in str(int(card / 10)):
            self.numbers.append(w)
        for y in self.numbers:
            if odd:
                self.check = int(y) * 2
                if self.check > 9:
                    self.check -= 9
                self.usern.append(int(self.check))
            else:
                self.usern.append(int(y))
            if odd:
                odd = False
            else:
                odd = True
            self.check = 0
        odd = True
        self.numbers = []
        self.check = 0
        for z in range(15):
            self.check += self.usern.pop(0)
        if (self.check + self.last_dig) % 10 == 0:
            return True
        else:
            return False

    def find_card_balance(self, cur, usercard):
        for q in cur.execute(find_balance, [usercard]).fetchall():
            for w in q:
                return w
        self.conn.commit()

    def check_card_number(self, number, pin):
        self.number_check = False
        self.pin_check = False
        for x in self.cur.execute(card_number_pin).fetchall():
            for y in x:
                if self.for_time == 0:
                    if number == y:
                        print(y)
                        self.number_check = True
                        self.for_time = 1
                        self.both = True
                else:
                    if pin == y and self.both:
                        print(y)
                        self.pin_check = True
                        self.for_time = 0
                        break
            self.for_time = 0
            self.both = False

    def user_delete_card(self, user):
        self.cur.execute(user_delete, [user])
        card.conn.commit()

    def resever_card_check(self, number):
        self.in_table = True
        print(all_numbers(self.cur))
        for x in all_numbers(self.cur):
            for y in x:
                if y == str(number):
                    self.in_table = False
        card.conn.commit()
        return self.in_table



def add_income(income1, user1):
    card.cur.execute('UPDATE card SET balance = ? WHERE number = ?;', (income1 + int(card.find_card_balance(card.cur, user1)), user1))
    card.conn.commit()


def tran_income(income, resever, deliver):
    card.cur.execute('''UPDATE card SET balance = ? WHERE number = ?;''', (int(card.find_card_balance(card.cur, user)) - income, deliver))
    card.cur.execute('''UPDATE card SET balance = ? WHERE number = ?;''', (int(card.find_card_balance(card.cur, resever)) + int(income), resever))
    print('Success!')
    card.conn.commit()


card = CreateAccount()
create_table(card.conn)
infoin = ''
while True:
    print('''
1. Create an account
2. Log into account
0. Exit''')
    infoin = input('>')
    if infoin == '1':
        card.RandomCard()
    if infoin == '2':
        print('''
Enter your card number:''')
        user = str(input(">"))
        print('Enter your PIN:')
        pin = str(input(">"))
        card.check_card_number(user, pin)
        if card.number_check and card.pin_check:
            print('''
You have successfully logged in!''')
            #print(card.cur.execute('SELECT * FROM card').fetchall())
            # print(user)
            while True:
                print('''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
                # print(user)
                infoin = input('>')
                if infoin == '1':
                    print(f'''
Balance: {card.find_card_balance(card.cur, user)}''')
                elif infoin == '2':
                    print('''
Enter income:''')
                    income = int(input('>'))
                    add_income(income, user)
                elif infoin == '3':
                    print('''
transfer 
enter card number:''')
                    resever = int(input('>'))
                    if user == resever:
                        print("You can't transfer money to the same account!")
                    elif not card.card_Luhn(resever):
                        print('Probably you made a mistake in the card number. Please try again!')
                    elif card.resever_card_check(resever):
                        print("Such a card does not exist.")
                    else:
                        print('Enter how much money you want to transfer:')
                        money = int(input('>'))
                        if card.find_card_balance(card.cur, user) >= money:
                            tran_income(money, resever, user)
                        else:
                            print("Not enough money!")
                elif infoin == '4':
                    card.user_delete_card(user)
                    print('''
The account has been closed''')
                    break
                elif infoin == '5':
                    print('''
You have successfully logged out!''')
                    break
                elif infoin == '0':
                    exit()
        else:
            print('''
Wrong card number or PIN!''')
    elif infoin == '0':
        print('''

Bye!''')
        break