import os
import json
import datetime
import argparse

def read_json():
    
    # Check if json file exists 
    if setup_file():
        with open('expanses.json', 'r') as file:
            return json.load(file)

def write_json(values):
    with open('expanses.json', 'w') as file:
        return json.dump(values, file, indent=4, separators=(',', ': '))
    
def create_card():
    print("You haven't added your card yet. Please add it, so that you could use this expanse tracker.")
    name = input('What is the name of your card: ')
    deposit = input('How much do you want to deposit to your card: ')
    
    with open('expanses.json', 'r') as file:
        expanses = json.load(file)


    card = {
        'name': name,
        'id': 0,
        'balance': deposit,
        'time': datetime.datetime.now().strftime("%Y-%m-%d")
    }

    expanses.append(card)
    write_json(expanses)

    print(f'Successfully created your new card, with name: {name}')



def setup_file():

    if os.path.isfile('expanses.json'):
        with open('expanses.json', 'r') as file:

            # Reads json file, without empty spaces        
            data = ''.join(file.read().split())

            # If json file only has [] or is empty, create user card then returns True, otherwise just returns True
            if data == '' or data == '[]':
                with open('expanses.json', 'w') as file:
                    json.dump([], file)
                    # create_card()
                    print("Expanse Json File exists, but is empty and doesn't have a card")
        
                create_card()
                return True
        
            else:
                return True
    
    # Creates json file, if it doesn't exist, then creates a card, and return True
    else:
        with open('expanses.json', 'w') as file:
            json.dump([], file)

            print("Expanse Json file doesn't exist, just created one.")
        create_card()
        return True

def add_expanse(desc, amount):

    expanses = read_json()

    # Gets the highest id+1, (returns 0 if there are no ids(id: 0, is for the card))
    new_exp_id = max([exp.get('id', 0) for exp in expanses] or [0]) + 1

    
    balance = expanses[0]['balance']
    expanses[0]['balance'] = int(balance) - int(amount)

    new_expanse = {
        'id': new_exp_id,
        'description': desc,
        'amount': f"${amount}",
        'date': datetime.datetime.now().strftime("%Y-%m-%d")
    }

    expanses.append(new_expanse)

    write_json(expanses) 

    print(f'Successfully added a new expense, with id: {new_exp_id}')


def delete_expanse(id):

    expanses = read_json()
    c = 0
    for exp in expanses:
        if exp['id'] == id and exp['id'] != 0:
            c += 1
            expanses[0]['balance'] += int(exp['amount'][1:])
            expanses.remove(exp)
            print(f'Successfully removed expanse with ID: {exp['id']}')
    if c < 1:
        print(f"Couldn't find any expanses with ID: {id}")

    write_json(expanses)


# Turns months input into 2 digits, e.g Dec --> 12, december --> 12, 2 --> 02
def turn_month_to_int(month):

    if len(month) <= 3 and month.isalpha() and month.lower() != 'may':
        month = datetime.datetime.strptime(month, '%b').month

        return month
    
    elif month.isalpha() == False:
        if len(month) == 1:
            month = '0' + month
            return month
        return month
    
    month = datetime.datetime.strptime(month, '%B').month
    return month


def list_expanse(month=None):

    expanses = read_json()

    # If you are seeing this, please fix the indentation
    print(f"# ID \tDate \t\tDescription\t\t\tAmount")
    if month:
        month_int = turn_month_to_int(month)

        c = 0
        for month_num in expanses[1:]:

            # Check if user month exists in the json file.
            exp = month_num['date'][5:7]
            if int(exp) == int(month_int):
                c += 1
                print(f'# {month_num['id']}\t{month_num['date']}\t{month_num['description']}\t\t\t{month_num['amount']}')

        if c < 1:
            print(f"No expanse was done in: {month}")

    else:
        for i in range(1, len(expanses)):
            print(f'# {expanses[i]['id']}\t{expanses[i]['date']}\t{expanses[i]['description']}\t\t\t{expanses[i]['amount']}')
            

def update_expanse(id, desc=None, amount=None):
    
    expanses = read_json()


    for exp in expanses[1:]:
        if exp['id'] == id:
            if desc:
                exp['description'] = desc
                print(f'Successfully updated description of expanse {exp}')

            if amount:
                print(expanses[0]['balance'], type(expanses[0]['balance']), exp['amount'], type(exp['amount']))
                expanses[0]['balance'] = expanses[0]['balance'] + int(exp['amount'][1:]) - amount
                exp['amount'] = f"${amount}"
                print(f'Successfully updated amount of expanse {exp}')
        
            if not desc and not amount:
                print("New description/amount wasn't passed")
            break

    write_json(expanses)
        

def summary(month=None):
    
    expanses = read_json()

    total = 0
    if month:
        month_int = turn_month_to_int(month)

        for month_num in expanses[1:]:
            exp = month_num['date'][5:7]
            month_amount = int(month_num['amount'][1:])
            if int(exp) == int(month_int):
                total += month_amount
        print(f'Total money spent in {month} month: ${total}\nAmount left on the card: ${expanses[0]['balance']}')
        if expanses[0]['balance'] < 0:
            print(f"WARNING! your credit balance is negative. You will be charged with interest, unless you pay off your card.")
        return

    total = 0
    for i in range(1, len(expanses)):
        total += int(expanses[i]['amount'][1:])
    
    print(f'Total spent: ${total}\nAmount left on the card: ${expanses[0]['balance']}')


def main():
    parser = argparse.ArgumentParser('Expanse Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_expanse_parser = subparsers.add_parser('add', help='Add a new expanse')
    add_expanse_parser.add_argument('--desc', required=True, nargs='+', type=str, help='Description of the expanse')
    add_expanse_parser.add_argument('--amount', required=True, type=int, help='Amount of the new expanse')

    delete_expanse_parser = subparsers.add_parser('delete', help='Delete an expanse')
    delete_expanse_parser.add_argument('--id', required=True, type=int, help='ID of the expanse')

    list_expanse_parser = subparsers.add_parser('list', help='List expanses')
    list_expanse_parser.add_argument('--month', type=str, help='Date of the expanses')

    summary_parser = subparsers.add_parser('summary', help='Summary of the expanses')
    summary_parser.add_argument('--month', type=str, help='Month of the expanses')

    update_expanse_parser = subparsers.add_parser('update', help='Update expanse')
    update_expanse_parser.add_argument('--id', required=True, type=int, help='ID of the expanse')
    update_expanse_parser.add_argument('--new_desc', nargs='+', type=str, help='Description of the expanse')
    update_expanse_parser.add_argument('--new_amount', type=int, help='Amount of the new expanse')

    args = parser.parse_args()

    if args.command == 'add':
        add_expanse(' '.join(args.desc), args.amount)
    elif args.command == 'delete':
        delete_expanse(args.id)
    elif args.command == 'list':
        list_expanse(args.month)
    elif args.command == 'summary':
        summary(args.month)
    elif args.command == 'update':
        desc = ' '.join(args.new_desc) if args.new_desc else None
        update_expanse(args.id, desc, args.new_amount)

if __name__ == '__main__':
    main()