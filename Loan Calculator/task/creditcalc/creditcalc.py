import math
import argparse


class Loan:
    principal = 0
    payment = 0
    periods = 0
    interest = 0.0
    
    def __init__(self, operation, princ, pay, per, inter):
        self.interest = inter / 12 / 100
        if operation == 'n':  # number of payments
            self.principal = princ
            self.payment = pay
            self.periods = math.log(self.payment / (self.payment - self.interest * self.principal), 1 + self.interest)
            self.periods = math.ceil(self.periods)
    
        if operation == 'a':  # payment
            self.principal = princ
            self.periods = per
            numer = self.interest * math.pow(1 + self.interest, self.periods)
            denom = math.pow((1 + self.interest), self.periods) - 1
            self.payment = math.ceil(self.principal * (numer/denom))
            
        if operation == 'p':  # principal
            self.payment = pay
            self.periods = per
            numer = self.interest * math.pow(1 + self.interest, periods)
            denom = math.pow(1 + self.interest, self.periods) - 1
            self.principal = math.ceil(self.payment / (numer / denom))

        if operation == 'd':  # differentiated payment
            self.principal = princ
            self.periods = per

    def differentiated_payment(self, payment_number):
        numer = self.principal * (payment_number - 1)
        part_1 = numer / self.periods
        part_2 = self.principal - part_1
        part_3 = self.interest * part_2
        dm = self.principal / self.periods + part_3
        return math.ceil(dm)
    
    def print_principal(self):
        print(f"Your loan principal = {self.principal}!")
        
    def print_payment(self):
        print(f"Your monthly payment = {self.payment}!")
        
    def print_periods(self):
        return self.convert_months()
        
    def convert_months(self):
        years = int(self.periods / 12)
        months = self.periods % 12
        if years == 0:
            val = f"It will take {months} months to repay this loan!"
        elif months == 0:
            val = f"It will take {years} years to repay this loan!"
        else:
            val = f"It will take {years} years and {months} months to repay this loan!"
        return val


principal = 0.0
payment = 0.0
periods = 0
interest = 0.0

parser = argparse.ArgumentParser()
# --type --payment --principal --periods --interest
parser.add_argument("--type", action='store', choices=['diff', 'annuity'])
parser.add_argument("--payment", action='store', default=0)
parser.add_argument("--principal", action='store', default=0)
parser.add_argument("--periods", action='store', default=0)
parser.add_argument("--interest", action='store', default=0)

args = parser.parse_args()

if len(vars(args)) < 5:
    print('Incorrect parameters')
    exit(0)
if args.type != 'diff' and args.type != 'annuity':
    print('Incorrect parameters')
    exit(0)

payment = int(args.payment)
principal = int(args.principal)
periods = int(args.periods)
interest = float(args.interest)

if payment < 0 or principal < 0 or periods < 0 or interest <= 0:
    print('Incorrect parameters')
    exit(0)
if args.type == 'diff' and principal == 0:
    print('Incorrect parameters')
    exit(0)

# Determine what to calculate
selection = ''
if periods == 0:
    selection = 'n'
if principal == 0:
    selection = 'p'
if payment == 0:
    if args.type == 'annuity':
        selection = 'a'
    else:
        selection = 'd'

my_loan = Loan(selection, principal, payment, periods, interest)
total_paid = 0
if selection == 'n':
    print(my_loan.convert_months())
    total_paid = my_loan.payment * my_loan.periods
if selection == 'a':
    my_loan.print_payment()
    total_paid = my_loan.payment * my_loan.periods
if selection == 'p':
    my_loan.print_principal()
    total_paid = my_loan.payment * my_loan.periods
if selection == 'd':
    for counter in range(1, periods):
        print(f"Month {counter}: payment is {my_loan.differentiated_payment(counter)}")
        total_paid += my_loan.differentiated_payment(counter)
print('')
print(f'Overpayment = {total_paid - my_loan.principal}')
