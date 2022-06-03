# on this page we have two functions that will be used on the server side page

# in a case of a new sign up this function receives the user name and password
# from the client and saves it and returns the user name
# the user names and passwords are stored with a number from the user_number file
# and then at the authentication it checks if the numbers much
def new_user(name, password):
# here we open all the necessary files
    user_names = open("?\\?\\?\\user_names.txt", 'a')
    user_password = open("?\\?\\?\\user_password.txt", 'a')
# note that you need to open the user_number file and write there 0 before running the program
    user_number = open("?\\?\\?\\user_number.txt", 'r')

# here we take the user number and one to it so the next user as the next number
    num = int(user_number.read())
    user_number.close()
    user_number = open("?\\?\\?\\user_number.txt", 'w')
    num_count = num + 1
    user_number.write(f"{num_count}")
    user_number.close()

# here we wright the user name and password
    user_names.write(name+" = "+f"{num}"+"\n")
    user_names.close()

    user_password.write(password+" = "+f"{num}"+"\n")
    user_password.close()
    return name


# in case of a sign in this function receives the credentials
# and checks for authentication if the credentials are right
# it returns the user name and if there wrong it returns not a user

def login(name, password):
# first off we open the necessary files
    user_names = open("?\\?\\?\\user_names.txt", 'r')
    user_password = open("?\\?\\?\\user_password.txt", 'r')
    name_list = user_names.read()
    password_list = user_password.read()

# where we check if the user_name number and password number much
# if we get an error when looking for them that means they don't
# exist so we return not user
    try:
        user_check = name_list.split(name + " = ")
        user_check1 = user_check[1].split("\n")
    except IndexError:
        return "not user"
    try:
        password_check = password_list.split(password + " = ")
        password_check1 = password_check[1].split("\n")
    except IndexError:
        return "not user"

# if the numbers much we return the user name else we return not user
    if user_check1[0] == password_check1[0]:
        return name
    else:
        return "not user"
