import subprocess as sp
import pymysql
import pymysql.cursors
from prettytable import from_db_cursor
from getpass import getpass
from datetime import date
import re

RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[m"


# ------------------------ REGEX VALIDATION ------------------------
def validateInput(inp_str, inp_type, opt=False):
    validator = None
    if inp_type == "Name":
        validator = lambda name: re.match("^[A-Za-z]+$", name)
    elif inp_type == "Integer":
        validator = lambda num: num.isdigit()
    elif inp_type == "Float":
        validator = lambda num: num.replace(".", "", 1).isdigit()
    elif inp_type == "Bool":
        validator = lambda bool: bool == "true" or bool == "false"
    elif inp_type == "Email":
        validator = lambda email: re.match("^[A-Za-z][.\w]+@[A-Za-z]+\.[.A-Za-z]+$", email)
    elif inp_type == "Date":
        validator = lambda date: re.match("^\d{4}/\d{2}/\d{2}$", date)
    elif inp_type == "Sex":
        validator = lambda sex: sex == "M" or sex == "F" or sex == "Other"
    elif inp_type == "Address":
        validator = lambda address: re.match("^[ \w]+$", address)
    elif inp_type == "Blood":
        validator = lambda b_type: b_type in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    elif inp_type == "BP":
        validator = lambda bp: re.match("^\d{2,3}/\d{2,3}$", bp)
    elif inp_type == "Result":
        validator = lambda res: res == "Positive" or res == "Negative" or res == "Pending"

    inp = input(inp_str + ": ")
    while not validator(inp):
        if (opt and not inp):
            return inp
        print(RED, "Invalid input", RESET, sep="")
        inp = input(inp_str + ": ")
    return inp


# ------------------------ CONNECT TO DATABASE ------------------------
def connectToDatabase():
    global db, cursor
    sp.call('clear', shell=True)

    try:
        username = input("Username: ")
        password = getpass("Password: ")
        db = pymysql.connect(host='localhost',
                             user=username,
                             password=password,
                             db='bloodbank')
        sp.call('clear', shell=True)
        if db.open:
            print("Connected")
        else:
            print("Failed to connect")
    except Exception:
        sp.call('clear', shell=True)
        print(RED,
              "Connection Refused: Either username or password is incorrect or user doesn't have access to database",
              RESET, sep="")
        tmp = input("Enter Q to quit, any other key to continue>")
        if tmp == 'Q':
            return
        connectToDatabase()


# ------------------------ INSERTION QUERIES ------------------------
def addDonor():
    try:
        donor = {}
        donor["fname"] = validateInput("First Name", "Name")
        donor["mname"] = validateInput("Middle Name*", "Name", opt=True)
        donor["lname"] = validateInput("Last Name", "Name")

        donor["dob"] = validateInput("Date of Birth (YYYY/MM/DD)", "Date")
        year, month, day = map(int, donor["dob"].split("/"))
        if ((date.today() - date(year, month, day)).days // 365) < 18:
            print("Donor must be 18 years or above to donate!")
            return

        donor["eid"] = int(validateInput("Employee ID of Receptionist", "Integer"))
        donor["phoneno"] = validateInput("Phone Number", "Integer")
        donor["email"] = validateInput("Email ID", "Email")
        donor["sex"] = validateInput("Sex (M/F/Other)", "Sex")

        SQL_query = "INSERT INTO donor (employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) " \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"

        cursor.execute(SQL_query, (donor["eid"], donor["fname"], donor["mname"] if donor["mname"] != "" else None, donor["lname"],
                                   donor["phoneno"], donor["email"], donor["dob"], donor["sex"]))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def addReceptionist():
    try:
        receptionist = {}
        receptionist["fname"] = validateInput("First Name", "Name")
        receptionist["mname"] = validateInput("Middle Name*", "Name", opt=True)
        receptionist["lname"] = validateInput("Last Name", "Name")
        receptionist["cid"] = int(validateInput("Center ID", "Integer"))
        receptionist["phoneno"] = validateInput("Phone Number", "Integer")

        SQL_query = "INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number) " \
                    "VALUES(%s, %s, %s, %s, %s)"

        cursor.execute(SQL_query, (receptionist["cid"], receptionist["fname"], receptionist["mname"] if receptionist["mname"] != "" else None,
                                   receptionist["lname"], receptionist["phoneno"]))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def addBloodDonationCenter():
    try:
        center = {}
        center["address"] = validateInput("Address", "Address")
        center["phoneno"] = validateInput("Phone Number", "Integer")

        SQL_query = "INSERT INTO blood_donation_center (phone_number, address) VALUES(%s, %s)"

        cursor.execute(SQL_query, (center["phoneno"], center["address"]))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def addDonation():
    try:
        donor_id = int(validateInput("Donor ID", "Integer"))
        center_id = int(validateInput("Center ID", "Integer"))

        SQL_query = "SELECT gender FROM donor WHERE donor_id = %s"
        dict_cursor.execute(SQL_query, (donor_id))
        sex = dict_cursor.fetchone()["gender"]

        donation = {}
        donation["bp"] = validateInput("Blood Pressure (systolic/diastolic)", "BP")
        sys, dia = map(int, donation["bp"].split("/"))
        if sys > 180 or dia > 100:
            print("Blood pressure must be below 180 (systolic) and 100 (diastolic) to donate")
            return

        donation["haem"] = float(validateInput("Haemoglobin Level (g/dl)", "Float"))
        if donation["haem"] > 20:
            print("Haemoglobin level must be below 20 g/dl to donate")
            return
        if sex == 'M' and donation["haem"] < 13:
            print("Haemoglobin level must be above 13 g/dl to donate")
            return
        if sex == 'F' and donation["haem"] < 12.5:
            print("Haemoglobin level must be above 12.5 g/dl to donate")
            return

        donation["weight"] = float(validateInput("Weight (kg)", "Float"))
        if(donation["weight"] < 50):
            print("Weight must be greater than 50kg to donate")
            return

        donation["travel"] = input("Travel History*: ")

        SQL_query = "INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) " \
                    "VALUES (%s, %s, CURDATE(), %s, %s)"

        cursor.execute(SQL_query, (donation["bp"], donation["haem"], donation["weight"], donation["travel"] if donation["travel"] != "" else None))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

        # Insert into blood
        blood = {}
        blood["description"] = input("Blood Description*: ")
        SQL_query = "INSERT INTO blood (description, test_result) VALUES (%s, %s)"
        cursor.execute(SQL_query, (blood["description"] if blood["description"] != "" else None, "Pending"))
        db.commit()

        # Insert into donor participation
        donor_participation = {}
        donor_participation["donor_id"] = donor_id
        donor_participation["center_id"] = center_id

        SQL_query = "SELECT MAX(donation_id) AS 'max' FROM donation"
        dict_cursor.execute(SQL_query)
        donor_participation["donation_id"] = dict_cursor.fetchone()["max"]

        SQL_query = "SELECT MAX(blood_barcode) AS 'max' FROM blood"
        dict_cursor.execute(SQL_query)
        donor_participation["barcode"] = dict_cursor.fetchone()["max"]

        SQL_query = "INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) " \
                    "VALUES (%s, %s, %s, %s)"
        cursor.execute(SQL_query, (donor_participation["barcode"], donor_participation["donor_id"],
                                   donor_participation["center_id"], donor_participation["donation_id"]))
        db.commit()

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def addTestResult():
    try:
        blood_barcode = int(validateInput("Blood Barcode", "Integer"))

        result = {}
        result["blood_type"] = validateInput("Blood Type", "Blood")
        result["hiv1"] = validateInput("HIV 1 (true/false)", "Bool") == "true"
        result["hiv2"] = validateInput("HIV 2 (true/false)", "Bool") == "true"
        result["hepatitis_b"] = validateInput("Hepatitis B (true/false)", "Bool") == "true"
        result["hepatitis_c"] = validateInput("Hepatitis C (true/false)", "Bool") == "true"
        result["htlv1"] = validateInput("HTLV 1 (true/false)", "Bool") == "true"
        result["htlv2"] = validateInput("HTLV 2 (true/false)", "Bool") == "true"
        result["syphilis"] = validateInput("Syphilis (true/false)", "Bool") == "true"

        SQL_query = "INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv1, htlv2, syphilis) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(SQL_query, (blood_barcode, result["blood_type"], result["hiv1"], result["hiv2"], result["hepatitis_b"],
                                   result["hepatitis_c"], result["htlv1"], result["htlv2"], result["syphilis"]))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

        # Update blood table
        SQL_query = "UPDATE blood SET test_result = %s WHERE blood.blood_barcode = %s"
        cursor.execute(SQL_query, ("Positive" if True in result.values() else "Negative", blood_barcode))
        db.commit()

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def addToInventory():
    try:
        inventory = {}
        inventory["barcode"] = int(validateInput("Blood Barcode", "Integer"))

        # Check if tests are negative
        SQL_query = "SELECT test_result FROM blood WHERE blood.blood_barcode = %s"
        dict_cursor.execute(SQL_query, (inventory["barcode"]))
        result = dict_cursor.fetchone()["test_result"]
        if result == "Positive":
            print("Blood is unhealthy, cannot store in inventory")
            return
        elif result == "Pending":
            print("Blood can be stored only after test results are released")
            return

        inventory["comp_id"] = int(validateInput("Component ID", "Integer"))
        inventory["storage_date"] = validateInput("Date of Storage (YYYY/MM/DD)", "Date")

        SQL_query = "INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage)" \
                    "VALUES (%s, %s, %s, %s)"

        cursor.execute(SQL_query, (inventory["barcode"], inventory["comp_id"], None, inventory["storage_date"]))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

        # update blood inventory
        SQL_query = "UPDATE blood_inventory " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "SET date_of_expiry = date_of_storage + INTERVAL max_storage_duration DAY " \
                    "WHERE blood_inventory.blood_barcode = %s AND blood_inventory.component_id = %s"

        cursor.execute(SQL_query, (inventory["barcode"], inventory["comp_id"]))
        db.commit()

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def addHospital():
    try:
        hospital = {}
        hospital["name"] = validateInput("Hospital Name", "Name")
        hospital["phoneno"] = validateInput("Phone Number", "Integer")
        hospital["email"] = validateInput("Email ID", "Email")
        hospital["address"] = validateInput("Address", "Address")

        SQL_query = "INSERT INTO hospital (name, address, email_id, phone_number)" \
                    "VALUES(%s, %s, %s, %s)"

        cursor.execute(SQL_query, (hospital["name"], hospital["address"], hospital["email"], hospital["phoneno"]))
        db.commit()
        print(GREEN, "Insert successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to insert into database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


# def placeOrder():
#     pass


# ------------------------ UPDATE QUERIES ------------------------
def updateDonorDetails():
    try:
        donor_id = int(validateInput("Donor ID", "Integer"))
        options = [
            "Update Phone Number",
            "Update Email ID",
            "Add New Address",
            "Remove Address"
        ]
        for i in range(0, len(options)):
            print(f'{i + 1}. {options[i]}')
        try:
            choice = int(input("Enter choice> "))
        except ValueError:
            print(RED, "Invalid Choice", RESET, sep="")
            return

        if choice == 1:
            phone_number = validateInput("New Phone Number", "Integer")
            SQL_query = "UPDATE donor SET phone_number = %s WHERE donor_id = %s"
            cursor.execute(SQL_query, (phone_number, donor_id))
        elif choice == 2:
            email_id = validateInput("New Email ID", "Email")
            SQL_query = "UPDATE donor SET email_id = %s WHERE donor_id = %s"
            cursor.execute(SQL_query, (email_id, donor_id))
        elif choice == 3:
            address = validateInput("New Address", "Address")
            SQL_query = "INSERT INTO donor_address (donor_id, address) VALUES (%s, %s)"
            cursor.execute(SQL_query, (donor_id, address))
        elif choice == 4:
            address = validateInput("Address", "Address")
            SQL_query = "DELETE FROM donor_address WHERE donor_id = %s AND address = %s"
            cursor.execute(SQL_query, (donor_id, address))
        else:
            return

        db.commit()
        print(GREEN, "Update successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to update database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


# ------------------------ DELETION QUERIES ------------------------
def removeDonor():
    try:
        donor_id = int(validateInput("Donor ID", "Integer"))
        SQL_query = "DELETE FROM donor WHERE donor_id = %s"

        cursor.execute(SQL_query, (donor_id))
        db.commit()
        print(GREEN, "Delete successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to delete from database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def removeOrderedSamplesFromInventory():
    try:
        SQL_query = "DELETE FROM blood_inventory WHERE order_id IS NOT NULL"

        cursor.execute(SQL_query)
        db.commit()
        print(GREEN, "Delete successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to delete from database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def removeExpiredSamplesFromInventory():
    try:
        SQL_query = "DELETE FROM blood_inventory WHERE order_id IS NULL AND date_of_expiry < CURDATE()"

        cursor.execute(SQL_query)
        db.commit()
        print(GREEN, "Delete successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to delete from database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def removeDiseasedBlood():
    try:
        SQL_query = "DELETE FROM blood WHERE test_result = 'Positive'"

        cursor.execute(SQL_query)
        db.commit()
        print(GREEN, "Delete successful", RESET, sep="")

    except Exception as e:
        db.rollback()
        print(RED, "Failed to delete from database", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


# ------------------------ SELECTION QUERIES ------------------------
def getDonorDetails():
    try:
        SQL_query = "SELECT DISTINCT donor.donor_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, blood_type FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def generateBloodSampleList():
    try:
        SQL_query = "SELECT * FROM blood"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def generateBloodInventoryReport():
    try:
        SQL_query = "SELECT * FROM blood_inventory ORDER BY date_of_storage"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDailyOrders():
    try:
        date = validateInput("Date (YYYY/MM/DD)", "Date")
        SQL_query = "SELECT * FROM orders WHERE date_of_order = %s"

        cursor.execute(SQL_query, (date))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonorsByAge():
    try:
        lower_age = int(validateInput("Lower Age", "Integer"))
        upper_age = int(validateInput("Upper Age", "Integer"))
        SQL_query = "SELECT * FROM donor WHERE TIMESTAMPDIFF(year, date_of_birth, CURDATE()) BETWEEN %s AND %s"

        cursor.execute(SQL_query, (lower_age, upper_age))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def findCommonlyOrderedBloodTypes():
    try:
        SQL_query = "SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory " \
                    "JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE order_id IS NOT NULL " \
                    "GROUP BY blood_type, component_type " \
                    "ORDER BY total_orders DESC"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def findTotalStock():
    try:
        SQL_query = "SELECT blood_type, component_type, COUNT(*) AS total_stock FROM blood_inventory " \
                    "JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE order_id IS NULL " \
                    "GROUP BY blood_type, component_type " \
                    "ORDER BY total_stock DESC"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonorsFromArea():
    try:
        search_string = input("Search String: ")
        SQL_query = "SELECT donor.*, donor_address.address FROM donor " \
                    "JOIN donor_address ON donor.donor_id = donor_address.donor_id " \
                    "WHERE donor_address.address LIKE CONCAT(%s, %s, %s)"

        cursor.execute(SQL_query, ("%", search_string, "%"))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonorsFromBloodType():
    try:
        blood_type = validateInput("Blood Type ([ABO][+-])", "Blood")
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE blood_type = %s"

        cursor.execute(SQL_query, (blood_type))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonationsFromTestResults():
    try:
        test_result = validateInput("Test Result (Negative/Positive/Pending)", "Result")
        SQL_query = "SELECT donor_participation.*, blood.test_result FROM donor_participation " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "WHERE blood.test_result = %s"

        cursor.execute(SQL_query, (test_result))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonorsFromEmployee():
    try:
        employee_id = int(validateInput("Employee ID", "Integer"))
        SQL_query = "SELECT * FROM donor WHERE employee_id = %s"

        cursor.execute(SQL_query, (employee_id))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonorsRegisteredAtCenter():
    try:
        center_id = int(validateInput("Center ID", "Integer"))
        SQL_query = "SELECT donor.* FROM donor " \
                    "JOIN receptionist ON donor.employee_id = receptionist.employee_id " \
                    "JOIN blood_donation_center ON receptionist.center_id = blood_donation_center.center_id " \
                    "WHERE blood_donation_center.center_id = %s"

        cursor.execute(SQL_query, (center_id))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def getDonorsDonatedAtCenter():
    try:
        center_id = int(validateInput("Center ID", "Integer"))
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood_donation_center ON donor_participation.center_id = blood_donation_center.center_id " \
                    "WHERE blood_donation_center.center_id = %s"

        cursor.execute(SQL_query, (center_id))
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


def findExpiredBlood():
    try:
        SQL_query = "SELECT blood_barcode, component_id, date_of_storage, date_of_expiry FROM blood_inventory " \
                    "WHERE order_id IS NULL AND date_of_expiry < CURDATE()"

        cursor.execute(SQL_query)
        table = from_db_cursor(cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(RED, "Query failed", RESET, sep="")
        print(RED, "ERROR>>>>>>>>>>>>> ", e, RESET, sep="")


# ------------------------ COMMAND LINE INTERFACE ------------------------
def loop():
    while True:
        sp.call('clear', shell=True)
        options = [
            "Add a Donor",
            "Add a Receptionist",
            "Add a Blood Donation Center",
            "Add a Donation",
            "Add a Blood Test Result",
            "Add a Sample to Blood Inventory",
            "Add a Hospital",
            "Get Details of all Donors who have Donated",
            "Generate List of all Donated Blood Samples",
            "Generate Blood Inventory Report",
            "Get Orders on a Particular Date",
            "Find Most Commonly Ordered Blood Type and Component Type",
            "Find Total Stock of Each Blood Type and Component Type",
            "Find Samples in Blood Inventory which have Expired",
            "Get Donors in a Specific Age Group",
            "Get Donors living in a Particular Area",
            "Get Donors with a Specific Blood Type",
            "Get Blood Donations with a Specific Test Result",
            "Get Donors Registered by a Particular Employee",
            "Get Donors Registered at a Particular Center",
            "Get Donors who have Donated at a Particular Center",
            "Update Details of a Donor",
            "Remove a Donor",
            "Delete Ordered Samples from Inventory",
            "Delete Expired Samples from Inventory",
            "Delete Blood Samples With Test Result Positive",
            "Quit"
        ]

        for i in range(0, len(options)):
            print(f'{i + 1}. {options[i]}')
        try:
            choice = int(input("Enter choice> "))
        except ValueError:
            sp.call('clear', shell=True)
            print(RED, "Error: Invalid Choice", RESET, sep="")
            input("Press Enter to CONTINUE> ")
            continue

        sp.call('clear', shell=True)

        if choice == 27:
            break
        else:
            if choice == 1:
                addDonor()
            elif choice == 2:
                addReceptionist()
            elif choice == 3:
                addBloodDonationCenter()
            elif choice == 4:
                addDonation()
            elif choice == 5:
                addTestResult()
            elif choice == 6:
                addToInventory()
            elif choice == 7:
                addHospital()
            elif choice == 8:
                getDonorDetails()
            elif choice == 9:
                generateBloodSampleList()
            elif choice == 10:
                generateBloodInventoryReport()
            elif choice == 11:
                getDailyOrders()
            elif choice == 12:
                findCommonlyOrderedBloodTypes()
            elif choice == 13:
                findTotalStock()
            elif choice == 14:
                findExpiredBlood()
            elif choice == 15:
                getDonorsByAge()
            elif choice == 16:
                getDonorsFromArea()
            elif choice == 17:
                getDonorsFromBloodType()
            elif choice == 18:
                getDonationsFromTestResults()
            elif choice == 19:
                getDonorsFromEmployee()
            elif choice == 20:
                getDonorsRegisteredAtCenter()
            elif choice == 21:
                getDonorsDonatedAtCenter()
            elif choice == 22:
                updateDonorDetails()
            elif choice == 23:
                removeDonor()
            elif choice == 24:
                removeOrderedSamplesFromInventory()
            elif choice == 25:
                removeExpiredSamplesFromInventory()
            elif choice == 26:
                removeDiseasedBlood()
            else:
                print(RED, "Error: Invalid Choice", RESET, sep="")
            input("Press Enter to CONTINUE> ")


db = None
cursor = None
dict_cursor = None
connectToDatabase()
if db is None:
    exit(1)
else:
    cursor = db.cursor()
    dict_cursor = db.cursor(pymysql.cursors.DictCursor)
    loop()
