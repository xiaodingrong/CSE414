from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None

import re
def check_password_strength(password):
    """
    Check if the password meets the strong password criteria and return specific errors.
    """
    errors = []

    # Check if the password is at least 8 characters
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    # Check for a mixture of uppercase and lowercase letters
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")

    # Check for a mixture of letters and numbers
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number.")

    # Check for at least one special character
    if not re.search(r'[!@#?]', password):
        errors.append("Password must contain at least one special character (!, @, #, ?).")

    return errors


def create_patient(tokens):
    # create_patient <username> <password>
    if len(tokens) != 3:
        print("Create patient failed")
        return

    username = tokens[1]
    password = tokens[2]

    # Check if the password is strong
    errors = check_password_strength(password)
    if errors:
        print("Password is not strong enough. Ensure it meets the following criteria:")
        for error in errors:
            print(f"- {error}")
        return

    if username_exists_patient(username):
        print("Username taken, try again")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    patient = Patient(username, salt=salt, hash=hash)

    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Create patient failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Create patient failed")
        print("Error:", e)
        return

    print("Created user", username)


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]

    # Check if the password is strong
    errors = check_password_strength(password)
    if errors:
        print("Password is not strong enough. Ensure it meets the following criteria:")
        for error in errors:
            print(f"- {error}")
        return

    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def create_patient(tokens):

    # TODO: Part 1
        # create_patient <username> <password>
    if len(tokens) != 3:
        print("Create patient failed")
        return

    username = tokens[1]
    password = tokens[2]


    if username_exists_patient(username):
        print("Username taken, try again")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    patient = Patient(username, salt=salt, hash=hash)

    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Create patient failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Create patient failed")
        print("Error:", e)
        return

    print("Created user", username)

    #pass


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):

    #TODO: Part 1
    global current_patient

    if current_patient is not None or current_caregiver is not None:
        print("User already logged in, try again")
        return

    if len(tokens) != 3:
        print("Login patient failed")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login patient failed")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login patient failed")
        print("Error:", e)
        return

    if patient is None:
        print("Login patient failed")
    else:
        print("Logged in as ", username)
        current_patient = patient

   # pass

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False

def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    global current_patient, current_caregiver

    # Check if the user is logged in
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return

    # Extract the date from the tokens
    if len(tokens) < 2:
        print("Please try again")
        return

    date = tokens[1]

    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        # Query caregivers available on the date
        query_caregivers = """
            SELECT Username FROM Caregivers 
            WHERE Username NOT IN (
                SELECT CaregiverUsername FROM Reservations WHERE Date = %s
            )
            ORDER BY Username;
        """
        cursor.execute(query_caregivers, (date,))
        caregivers = cursor.fetchall()

        # If no caregivers are available
        if not caregivers:
            print("Please try again")
            return

        # Output available caregivers
        for caregiver in caregivers:
            print(caregiver['Username'])

        # Query vaccines and available doses
        query_vaccines = """
            SELECT Name, Doses FROM Vaccines;
        """
        cursor.execute(query_vaccines)
        vaccines = cursor.fetchall()

        # Output available vaccines and doses
        for vaccine in vaccines:
            print(f"{vaccine['Name']} {vaccine['Doses']}")

    except Exception as e:
        print("Please try again")
        print("Error:", e)
    pass


def reserve(tokens):
    """
    TODO: Part 2
    """
    global current_patient, current_caregiver

    if current_patient is None:
        print("Please login first")
        return

    if current_caregiver is not None:
        print("Please login as a patient")
        return

    # Extract the date and vaccine name from the tokens
    if len(tokens) < 3:
        print("Please try again")
        return

    date = tokens[1]
    vaccine_name = tokens[2]

    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        # Check if enough vaccine doses are available
        query = """
            SELECT Doses FROM Vaccines WHERE Name = %s;
        """
        cursor.execute(query, (vaccine_name,))
        vaccine = cursor.fetchone()

        if not vaccine or vaccine["Doses"] <= 0:
            print("Not enough available doses")
            return

        # Find a caregiver who is available on the selected date (alphabetically sorted)
        query_caregivers = """
            SELECT Username FROM Caregivers 
            WHERE Username NOT IN (
                SELECT CaregiverUsername FROM Reservations WHERE Date = %s
            )
            ORDER BY Username
        """
        cursor.execute(query_caregivers, (date,))
        caregiver = cursor.fetchone()

        if not caregiver:
            print("No caregiver is available")
            return

        # Reserve the appointment: reduce vaccine doses and add reservation record
        cursor.execute("""
            UPDATE Vaccines SET Doses = Doses - 1 WHERE Name = %s;
        """, (vaccine_name,))

        query_reservation = """
            INSERT INTO Reservations (Date, VaccineName, PatientUsername, CaregiverUsername)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query_reservation, (date, vaccine_name, current_patient.username, caregiver["Username"]))

        # Commit the transaction
        conn.commit()

        # Get the appointment ID
        cursor.execute("""
            SELECT AppointmentID FROM Reservations WHERE Date = %s AND VaccineName = %s 
            AND PatientUsername = %s AND CaregiverUsername = %s;
        """, (date, vaccine_name, current_patient.username, caregiver["Username"]))
        appointment = cursor.fetchone()

        # Output the appointment details
        print(f"Appointment ID {appointment['AppointmentID']}, Caregiver username {caregiver['Username']}")

    except Exception as e:
        print("Please try again")
        print("Error:", e)

    #pass


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra credits
    """

    global current_patient, current_caregiver

    # Ensure the user is logged in
    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return

    # Validate the command syntax
    if len(tokens) != 2:
        print("Please try again")
        return

    appointment_id = tokens[1]

    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        # Check if the appointment exists and is associated with the logged-in user
        if current_patient:
            query = """
                 SELECT * FROM Reservations 
                 WHERE AppointmentID = %s AND PatientUsername = %s;
             """
            cursor.execute(query, (appointment_id, current_patient.username))
        elif current_caregiver:
            query = """
                 SELECT * FROM Reservations 
                 WHERE AppointmentID = %s AND CaregiverUsername = %s;
             """
            cursor.execute(query, (appointment_id, current_caregiver.username))

        appointment = cursor.fetchone()

        # If the appointment doesn't exist or doesn't belong to the user, return an error
        if not appointment:
            print("Appointment not found or access denied")
            return

        # Retrieve appointment details
        vaccine_name = appointment["VaccineName"]

        # Delete the appointment from the reservations table
        delete_query = """
             DELETE FROM Reservations WHERE AppointmentID = %s;
         """
        cursor.execute(delete_query, (appointment_id,))

        # Update vaccine doses by increasing the count
        update_vaccine_query = """
             UPDATE Vaccines SET Doses = Doses + 1 WHERE Name = %s;
         """
        cursor.execute(update_vaccine_query, (vaccine_name,))

        # Commit all changes
        conn.commit()

        print(f"Appointment {appointment_id} canceled successfully")

    except pymssql.Error as e:
        print("Error occurred when canceling the appointment")
        print("Db-Error:", e)
    except Exception as e:
        print("Error occurred when canceling the appointment")
        print("Error:", e)
    finally:
        cm.close_connection()
    #pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    """
    TODO: Part 2
    """
    global current_patient, current_caregiver

    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return

    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)

        if current_patient is not None:
            # Fetch appointments for the current patient
            query = """
                 SELECT AppointmentID, Date, VaccineName, CaregiverUsername
                 FROM Reservations
                 WHERE PatientUsername = %s
                 ORDER BY Date;
             """
            cursor.execute(query, (current_patient.username,))  # Use correct attribute name
            appointments = cursor.fetchall()

            if not appointments:
                print("No appointments found")
                return

            print("Appointments for patient:")
            for appointment in appointments:
                print(
                    f"Appointment ID: {appointment['AppointmentID']}, Date: {appointment['Date']}, "
                    f"Vaccine: {appointment['VaccineName']}, Caregiver: {appointment['CaregiverUsername']}"
                )

        elif current_caregiver is not None:
            # Fetch appointments for the current caregiver
            query = """
                 SELECT AppointmentID, Date, VaccineName, PatientUsername
                 FROM Reservations
                 WHERE CaregiverUsername = %s
                 ORDER BY Date;
             """
            cursor.execute(query, (current_caregiver.username,))  # Use correct attribute name
            appointments = cursor.fetchall()

            if not appointments:
                print("No appointments found")
                return

            print("Appointments for caregiver:")
            for appointment in appointments:
                print(
                    f"Appointment ID: {appointment['AppointmentID']}, Date: {appointment['Date']}, "
                    f"Vaccine: {appointment['VaccineName']}, Patient: {appointment['PatientUsername']}"
                )

    except Exception as e:
        print("Please try again")
        print("Error:", e)
    #pass


def logout(tokens):
    """
    TODO: Part 2
    """
    global current_patient, current_caregiver

    if current_patient is None and current_caregiver is None:
        print("Please login first")
        return

    try:
        # If a patient is logged in
        if current_patient:
            print("Successfully logged out")
            current_patient = None

        # If a caregiver is logged in
        elif current_caregiver:
            print("Successfully logged out")
            current_caregiver = None

    except Exception as e:
        print("Please try again")
        print("Error:", e)
    pass


def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
