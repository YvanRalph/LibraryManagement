import sqlite3
from datetime import datetime, date

connection = sqlite3.connect('library.db')
cursor = connection.cursor()

booktable = "CREATE TABLE IF NOT EXISTS book(bookid INTEGER PRIMARY KEY, bookname TEXT NOT NULL, author TEXT NOT NULL, copies INTEGER);"
cursor.execute(booktable)

usertable = "CREATE TABLE IF NOT EXISTS user(userid INTEGER PRIMARY KEY, username TEXT NOT NULL, phonenumber TEXT NOT NULL, useraddress TEXT NOT NULL);"
cursor.execute(usertable)

renttable = "CREATE TABLE IF NOT EXISTS rent(rentid INTEGER PRIMARY KEY, bookid INTEGER, userid INTEGER,rentdate DATE DEFAULT (DATE('now')), FOREIGN KEY(bookid) REFERENCES book(bookid),FOREIGN KEY(userid)REFERENCES user(userid));"
cursor.execute(renttable)

returntable = "CREATE TABLE IF NOT EXISTS return(returnid INTEGER PRIMARY KEY, rentid INTEGER, returndate DATE DEFAULT (DATE('now')), fine_RWF INTEGER, FOREIGN KEY(rentid) REFERENCES rent(rentid));"
cursor.execute(returntable)

#Dispaly Menu function
def show_menu():
    print("")
    print("")
    print("****** Welcome To Libary System ********")
    print("")
    print("1. Create account for new Customer")
    print("2. Register new book in the Inventory")
    print("3. Record book to be rented")
    print("4. Record book being returned")
    print("5. Search Book in the Inventory")
    print("6. View Books in Stock")
    print("7. Exit the system")

# Function to get validate username input
def getvalid_username():
    while True:
            username = input("Enter your new Username: ").strip().lower()
            if username == "":
                print("Input cannot be empty. Try again.")
                continue
                    
            cursor.execute("SELECT COUNT(*) FROM user WHERE LOWER(username) = ?;", (username,))
            count = cursor.fetchone()[0]
                    
            if count > 0:
                print("Username already in use. Try a different one.")
                continue
                    
            break
                
    return username

#function to get validated phonenumber input
def getvalid_phonenbr():
    while True:
        phone_num = input("Enter your PhoneNumber: ")
        if phone_num == "":
            print("Input cannot be empty. Try again.")
            continue
                    
        if not phone_num.isdigit():
            print("Phone number must contain only digits. Try again.")
            continue
        phonenumber = int(phone_num)

        cursor.execute("SELECT COUNT(*) FROM user WHERE phonenumber = ?;", (phonenumber,))
        count = cursor.fetchone()[0]
                    
        if count > 0:
            print("Phonenumber already in use. Try a different one.")
            continue
                    
        break
                
    return phonenumber

#function to get validated address input
def getvalid_address():
    while True:
        useraddress = input("Enter your Address: ").strip().lower()
        if useraddress == "":
            print("Input cannot be empty. Try again.")
            continue
        else:
            break
                
    return useraddress



def createnewcustomer():
    print("")
    print("*** All Users ***")
    cursor.execute("SELECT * FROM user;")
    results = cursor.fetchall()
    for user in results:
        print(f"ID: {user[0]}, Name: {user[1]}, Phone: {user[2]}")
    print("")
    print("** Add New User **")

    #calling getvalidusername function
    username = getvalid_username()

    #calling getvalidphonenumber fucntion
    phonenumber = getvalid_phonenbr()

    #calling getvalidaddress function
    useraddress = getvalid_address()

    #Error Handling And new customer Insertion in database
    try:
        cursor.execute("INSERT INTO user(username,phonenumber,useraddress) VALUES(?,?,?)",(username, phonenumber, useraddress,))
        connection.commit()
        print("")
        print("User has been created successfully")
    except sqlite3.Error as e:
        print(f"Database error: {e}")


#Function to valid number of copies to add 0-100 and Update Book Already Exists user would like to update nbr copies
def update_copies_bookexists(bookname):
    while True:
        numcopies = input("Enter number of copies to add [0 - 100]: ")
        if numcopies == "":
            print("Input cannot be empty. Try again.")
            continue
        if not numcopies.isdigit():
            print("Number of Copies must contain only digits. Try again.")
            continue
        copies = int(numcopies)
        if copies > 0 and copies < 101:
            cursor.execute("SELECT copies FROM book WHERE LOWER(bookname) = ?;",(bookname,))
            oldcopies = cursor.fetchone()
            newcopynbr = oldcopies[0] + copies
                                                
            #Error Handling and Updating copies in book table database 
            try:                
                cursor.execute("UPDATE book SET copies = ? WHERE LOWER(bookname) = ?;", (newcopynbr,bookname,))
                connection.commit()
                print("")
                print("Number of Copies has been Updated Successfully.")
                break
            except sqlite3.Error as e:
                print(f"Database error: {e}")


        else:
            print("Try Again, Copies must be less than 100 and over 0")
            continue


#function to get if user would like to update copies or not Book Already Exists
def updatecopies(bookname):                            
    while True:
        newcopies = input("Book Already Exists, Update number of copies [ y/n ]: ").strip().lower()
        if newcopies == "":
            print("Input cannot be empty. Try again.")
            continue
        elif newcopies == "y" or newcopies == "yes":
            #Calling update copies bookexists function to update because user would like to update
            update_copies_bookexists(bookname)
        elif newcopies == "n" or newcopies == "no":
            print("Book Already Exists, Try Again Later")
            break
        else:
            print("Invalid input, Please try Again")
            continue
        break

#function to get valid author input form user
def getvalid_author():
    while True:
        author = input("Enter Author name: ").strip().lower()
        if author == "":
            print("Input cannot be empty. Try again.")
            continue
        else:
            break
    return author


# function to get valid input for copy number for New Book                   
def getvalid_copy_newbook():
    while True:
        copiesnumber = input("Enter How Many Copies [0-100]: ")
        if copiesnumber == "":
            print("Input cannot be empty. Try again")
            continue
        
        if not copiesnumber.isdigit():
            print("Number of Copies must contain only digits. Try again")
            continue
        
        copy = int(copiesnumber)
        if copy > 0 and copy < 101:
                break
        
        else:
            print("Try Again, Copies must be less than 100 and over 0")
    return copy


#Function to Insert new Book in the Book inventory
def create_newbook():
    while True:
        bookname = input("Enter book name: ").strip().lower()
        if bookname == "":
            print("Input cannot be empty. Try again.")
            continue
                    
        cursor.execute("SELECT COUNT(*) FROM book WHERE LOWER(bookname) = ?;", (bookname,))
        count = cursor.fetchone()[0]
        if count > 0:

            #calling updatecopies function, book Already exists                        
            updatecopies(bookname)
        
        else:
            newbookname = bookname

            #calling getvalid_author to get validated author input
            author = getvalid_author()

            #calling getvalid_copy_newbook to get validated copy input for new book
            copy = getvalid_copy_newbook()
                        

            #Error Handling and Inserting new book in the database
            try:
                cursor.execute("INSERT INTO book(bookname,author,copies) VALUES(?,?,?);",(newbookname,author,copy))
                connection.commit()
                print("")
                print("Book has been added in the Inventory")
                break
            except sqlite3.Error as e:
                print(f"Database error: {e}")

                        
        break


#Function to register New book 
def register_newbook():
    print("")
    print("*** All Books ***")
    cursor.execute("SELECT * FROM book;")
    results1 = cursor.fetchall()
    for user in results1:
        print(f"ID: {user[0]}, BookName: {user[1]}, Author: {user[2]}, Copies: {user[3]}")
    print("")
    print("** Register new book **")
    create_newbook()


#Function to get validated input of bookname for book about to be rented
def getvalid_bookname_rent():
    while True:
        booknamez = input("Enter bookname: ").strip().lower()
        if booknamez == "":
            print("Input cannot be empty. Try again.")
            continue
                    
        cursor.execute("SELECT COUNT(*) FROM book WHERE LOWER(bookname) = ?;", (booknamez,))
        count = cursor.fetchone()[0]
                    
        if count > 0:
            break
        
        else:
            print("Book doesn't Exist, Choose Another Book")
            continue                  
                    
                
    return booknamez


#Function to get valid username for book to be rented
def getvalid_usernamez():
    while True:
            usernamez = input("Enter your new Username: ").strip().lower()
            if usernamez == "":
                print("Input cannot be empty. Try again.")
                continue
                    
            cursor.execute("SELECT COUNT(*) FROM user WHERE LOWER(username) = ?;", (usernamez,))
            count = cursor.fetchone()[0]
                    
            if count > 0:
                break

            else:
                print("User not found, Try Again")
                continue
                
    return usernamez



#Function to Record a new book rent
def record_bookrent():
    print("")
    print("*** All Rents ***")
    cursor.execute("SELECT * FROM rent;")
    results2 = cursor.fetchall()
    for user in results2:
        print(f"ID: {user[0]}, BookId: {user[1]}, UserId: {user[2]}, Rentdate: {user[3]}")
    print("")
    print("** Record book rent **")
    cursor.execute("SELECT bookname FROM book;")
    nameofbook = cursor.fetchall()
    print(f'All Books in Inventory:')
    for userd in nameofbook:
        print(f"Book: {userd[0]}")
    print("")

    #Calling getvalid_bookname_rent to get validated bookname
    booknamez = getvalid_bookname_rent()

    cursor.execute("SELECT copies from book where LOWER(bookname) = ?", (booknamez,))
    nbrcopies = cursor.fetchone()
    nbrcopies = nbrcopies[0]
    if nbrcopies > 0:
        cursor.execute("SELECT bookid from book where LOWER(bookname) = ?", (booknamez,))
        idbook = cursor.fetchone()
        nbrcopies -= 1
        
    else:
        print("")
        print(f"Book {booknamez} Rented Out, Pick New one")        
                
                

    print("")
    print("*** All Users ***")
    cursor.execute("SELECT * FROM user;")
    results = cursor.fetchall()
    for user in results:
        print(f"Name: {user[1]}")
    print("")

    usernamez = getvalid_usernamez()
      
    cursor.execute("SELECT userid from user where LOWER(username) = ?", (usernamez,))
    iduser = cursor.fetchone()
    
    print("")

    #Error Handling and Recording the New Rent into database
    try:
        cursor.execute("INSERT INTO rent(bookid,userid) VALUES(?,?);",(idbook[0],iduser[0],))
        connection.commit()
        cursor.execute("UPDATE book SET copies = ? WHERE LOWER(bookname) = ?", (nbrcopies,booknamez,))
        connection.commit()
        print("")
        print("Book Rent has been Recorded")
    except sqlite3.Error as e:
        print(f"Database error: {e}")



#Function to get validated RentID
def getvalid_rentid():
    while True:
        rent_id = input("Enter RentID: ")
        if rent_id == "":
            print("Input cannot be empty. Try again.")
            continue
                    
        if not rent_id.isdigit():
            print("RentID must contain only digits. Try again.")
            continue
        
        rentid = int(rent_id)

        cursor.execute("SELECT COUNT(*) FROM rent WHERE rentid = ?;", (rentid,))
        count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM return WHERE rentid = ?;", (rentid,))
        countz = cursor.fetchone()[0]
                    
        if count > 0 and countz < 1:
            break
        
        else:
            print("Rent ID Entered Doesn't Exist or Already Returned || TRY AGAIN")
            continue                   
                    
                
    return rentid


def record_bookreturn():
    while True:
        print("")
        print("*** All Returns ***")
        cursor.execute("SELECT * FROM return;")
        results3 = cursor.fetchall()
        for user in results3:
            print(f"ID: {user[0]}, RentId: {user[1]}, ReturnDate: {user[2]}, Fine[RWF]: {user[3]}")
        print("")
        print("** Record book return **")
        cursor.execute(""" SELECT rent.rentid, user.username, book.bookname,
        rent.rentdate FROM rent JOIN user ON rent.userid = user.userid
        JOIN book ON rent.bookid = book.bookid; """)
        nameofbook = cursor.fetchall()
        print("All Books Rented:")
        for use in nameofbook:
            print(f"RentID: {use[0]}, Username: {use[1]}, Bookname: {use[2]}, Rentdate: {use[3]}")
            

        #Calling getvalid_rentid To get Validated rentID  
        rentid = getvalid_rentid()

        print("")
        returndate = date.today()
        cursor.execute("SELECT rentdate FROM rent WHERE rentid = ?;", (rentid,))
        rentdate = cursor.fetchone()
        rentdate = datetime.strptime(rentdate[0], '%Y-%m-%d').date()
        days_used = (returndate - rentdate).days
        fine = 0
        if days_used > 30 and days_used <= 31:
            fine = 1000
        elif days_used > 31 and days_used <= 35:
            fine = 5000
        elif days_used > 35:
            fine = 20000
        else:
            fine = 0
            
        #Adding the returned book back in the Inventory by Incrementing
        cursor.execute("SELECT bookid FROM rent WHERE rentid = ?;", (rentid,))
        bookid = cursor.fetchone()
        cursor.execute("SELECT copies FROM book WHERE bookid = ?;", (bookid[0],))
        copynum = cursor.fetchone()
        newcopynbr = copynum[0] + 1

        #Error Handling : Updating new number of copies after return and Inserting a record of the return in the database
        try:
            cursor.execute("UPDATE book SET copies = ? WHERE bookid = ?;", (newcopynbr,bookid[0],))
            connection.commit()

            cursor.execute("DELETE FROM rent WHERE rentid = ?;", (rentid,))
            connection.commit()            

            cursor.execute("INSERT INTO return(rentid,fine_RWF) VALUES(?,?);",(rentid,fine,))
            connection.commit()
            print("")
            print("Book Return has been Recorded")
            break
        except sqlite3.Error as e:
            print(f"Database error: {e}")


#Function for searching books by name or author inside the book Inventory
def searchbook():
    while True:
        search = input("Enter Bookname or Author: ").strip().lower()
        if search == "":
            print("Input cannot be empty. Try again.")
            continue
                    
        cursor.execute("SELECT * FROM book WHERE LOWER(bookname) LIKE ? OR LOWER(author) LIKE ?;",(f'%{search}%', f'%{search}%'))
        result = cursor.fetchall()

        if result == []:
            print("")
            print("Book Not in Stock")
            break
                    
        else:
            print("")
            print("Book In Stock:")
            for user in result:
                print(f"ID: {user[0]}, BookName: {user[1]}, Author: {user[2]}, Copies: {user[3]}")
        break


#Function to get all Books in Stock
def booksinstock():
    cursor.execute("SELECT * FROM book WHERE copies > 0")
    view = cursor.fetchall()
    print("")
    print("All Books In Stock:")
    for book in view:
        print(f"ID: {book[0]}, BookName: {book[1]}, Author: {book[2]}, Copies: {book[3]}")




    
# Main function controls the whole Program
def startup():
    while True:
        #calling menu Function
        show_menu()

        choice = input("Enter your choice [1-7]: ")
        if choice == "1":
            createnewcustomer()
        elif choice == "2":
            register_newbook()
        elif choice == "3":
            record_bookrent()
        elif choice == "4":
            record_bookreturn()
        elif choice == "5":
            searchbook()
        elif choice == "6":
            booksinstock()
        elif choice == "7":
            print("Bye!!!!!")
            break
        elif choice == "":
            print("")
            print("Input can't be Empty,  < TRY AGAIN >")
        else:
            print("")
            print("Invalid choice,  < TRY AGAIN >")


startup()