from db.db_connect import db_connect
from models.user import User
import argparse
import cmd_example

DB_NAME = "workshop"


def view_users_list(cursor):
    print("Listing users:")
    print('\n')
    users_list = User.load_users(cursor)
    for user in users_list:
        print(f" {user.id}. {user.username} {user.email}")


def add_new_user(cursor, email, password):
    if input(f'User {email} was not found in database.\nPress Y to add new user\n').upper() == 'Y':
        username = input('\nPlease provide new user name:  ')
        u = User()
        u.username = username
        u.email = email.lower()
        u.set_password(password)
        u.save_to_db(cursor)
        print(f'User [{username}] successfully added')


def edit_user(cursor, user, new_pass, new_name, new_email):
    print(new_name)
    print(new_email)
    print(new_pass)
    if new_name is None and new_pass is None and new_email is None:
        print(f'Arguments -pass, -name, -email are required')
    if new_pass is not None:
        if len(new_pass) < 8:
            print('Password has to be minimum 8 characters long')
        else:
            user.set_password(new_pass)
            user.save_to_db(cursor)
            print('Password changed')
    if new_name is not None:
        if len(new_name) < 2:
            print('Name has to be minimum 2 characters long')
        else:
            user.username = new_name
            user.save_to_db(cursor)
            print('User name changed')
    if new_email is not None:
        if User.check_email(new_email):
            user.email = new_email
            user.save_to_db(cursor)
            print('User email change')
        else:
            print('Provided email is not valid email address')


def delete_user(cursor, user):
    if input(f'Type Y to confirm you want to delete account for user [{user.email}]').upper() == 'Y':
        user.delete(cursor)
        print("User's account deleted")


def do_stuff(cursor):
    u1 = User.load_user_by_id(cursor, 1)
    print(u1.id, u1.username)
    u1.username = "test123"
    u1.save_to_db(cursor)


def main(args):
    connection = db_connect(DB_NAME)
    cursor = connection.cursor()
    email = args.email.lower() if args.email is not None else None
    password = args.password if args.password is not None else None
    new_pass = args.newpass if args.newpass is not None else None
    new_name = args.newname if args.newname is not None else None
    new_email = args.newemail if args.newemail is not None else None
    edit = args.edit
    delete = args.delete

    if args.list:
        view_users_list(cursor)
    # parameters -m -p only (add new user case)
    elif None not in (email, password):
        if not edit and not delete:
            # print(f'mail: {args.email}, pass: {args.password}')
            # print('New user case')
            user = User.load_user_by_mail(cursor, email)
            if user is None:
                if len(password) < 8:
                    print('Password has to be minimum 8 characters long')
                elif User.check_email(email) is None:
                    print(f'Provided email [{email}] is not valid email address. Please try again.')
                else:
                    add_new_user(cursor, email, password)
            else:
                print(f'User {email} already exists.')
        # parameters -u -p -e [-pass and/or -name and/or -email] (edit user)
        elif edit or delete:
            # load user by email
            user = User.load_user_by_mail(cursor, email)
            if user is None:
                print('Such user does not exist')
            elif not user.check_password(password):
                print(f'Wrong password')
            elif edit:
                edit_user(cursor, user, new_pass, new_name, new_email)
            elif delete:
                delete_user(cursor, user)
    else:
        print('Nothing to do')

    cursor.close()
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage users and messages.')
    parser.add_argument("-l", "--list", help="list users", action="store_true")
    parser.add_argument("-u", "--email", help="User email")
    parser.add_argument("-p", "--password", help="User password")
    parser.add_argument("-pass", "--newpass", help="New user password")
    parser.add_argument("-name", "--newname", help="New user name")
    parser.add_argument("-email", "--newemail", help="New user email")
    parser.add_argument("-e", "--edit", help="Edit user", action="store_true")
    parser.add_argument("-d", "--delete", help="Delete user", action="store_true")
    parser.add_argument("-q", "--quit", help="Quit program", action="store_true")
    args = parser.parse_args()

    # print(args)
    main(args)
