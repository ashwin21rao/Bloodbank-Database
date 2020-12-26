import pymysql.cursors
from datetime import date
import config as cfg
from regexp import validateInput


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

        cfg.cursor.execute(SQL_query, (donor["eid"], donor["fname"], donor["mname"] if donor["mname"] != "" else None, donor["lname"],
                                   donor["phoneno"], donor["email"], donor["dob"], donor["sex"]))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


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

        cfg.cursor.execute(SQL_query, (receptionist["cid"], receptionist["fname"], receptionist["mname"] if receptionist["mname"] != "" else None,
                                   receptionist["lname"], receptionist["phoneno"]))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def addBloodDonationCenter():
    try:
        center = {}
        center["address"] = validateInput("Address", "Address")
        center["phoneno"] = validateInput("Phone Number", "Integer")

        SQL_query = "INSERT INTO blood_donation_center (phone_number, address) VALUES(%s, %s)"

        cfg.cursor.execute(SQL_query, (center["phoneno"], center["address"]))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def addDonation():
    try:
        donor_id = int(validateInput("Donor ID", "Integer"))
        center_id = int(validateInput("Center ID", "Integer"))

        SQL_query = "SELECT gender FROM donor WHERE donor_id = %s"
        cfg.dict_cursor.execute(SQL_query, (donor_id))
        sex = cfg.dict_cursor.fetchone()["gender"]

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

        cfg.cursor.execute(SQL_query, (donation["bp"], donation["haem"], donation["weight"], donation["travel"] if donation["travel"] != "" else None))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

        # Insert into blood
        blood = {}
        blood["description"] = input("Blood Description*: ")
        SQL_query = "INSERT INTO blood (description, test_result) VALUES (%s, %s)"
        cfg.cursor.execute(SQL_query, (blood["description"] if blood["description"] != "" else None, "Pending"))
        cfg.db.commit()

        # Insert into donor participation
        donor_participation = {}
        donor_participation["donor_id"] = donor_id
        donor_participation["center_id"] = center_id

        SQL_query = "SELECT MAX(donation_id) AS 'max' FROM donation"
        cfg.dict_cursor.execute(SQL_query)
        donor_participation["donation_id"] = cfg.dict_cursor.fetchone()["max"]

        SQL_query = "SELECT MAX(blood_barcode) AS 'max' FROM blood"
        cfg.dict_cursor.execute(SQL_query)
        donor_participation["barcode"] = cfg.dict_cursor.fetchone()["max"]

        SQL_query = "INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) " \
                    "VALUES (%s, %s, %s, %s)"
        cfg.cursor.execute(SQL_query, (donor_participation["barcode"], donor_participation["donor_id"],
                                   donor_participation["center_id"], donor_participation["donation_id"]))
        cfg.db.commit()

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


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

        cfg.cursor.execute(SQL_query, (blood_barcode, result["blood_type"], result["hiv1"], result["hiv2"], result["hepatitis_b"],
                                   result["hepatitis_c"], result["htlv1"], result["htlv2"], result["syphilis"]))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

        # Update blood table
        SQL_query = "UPDATE blood SET test_result = %s WHERE blood.blood_barcode = %s"
        cfg.cursor.execute(SQL_query, ("Positive" if True in result.values() else "Negative", blood_barcode))
        cfg.db.commit()

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def addToInventory():
    try:
        inventory = {}
        inventory["barcode"] = int(validateInput("Blood Barcode", "Integer"))

        # Check if tests are negative
        SQL_query = "SELECT test_result FROM blood WHERE blood.blood_barcode = %s"
        cfg.dict_cursor.execute(SQL_query, (inventory["barcode"]))
        result = cfg.dict_cursor.fetchone()["test_result"]
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

        cfg.cursor.execute(SQL_query, (inventory["barcode"], inventory["comp_id"], None, inventory["storage_date"]))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

        # update blood inventory
        SQL_query = "UPDATE blood_inventory " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "SET date_of_expiry = date_of_storage + INTERVAL max_storage_duration DAY " \
                    "WHERE blood_inventory.blood_barcode = %s AND blood_inventory.component_id = %s"

        cfg.cursor.execute(SQL_query, (inventory["barcode"], inventory["comp_id"]))
        cfg.db.commit()

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def addHospital():
    try:
        hospital = {}
        hospital["name"] = validateInput("Hospital Name", "Name")
        hospital["phoneno"] = validateInput("Phone Number", "Integer")
        hospital["email"] = validateInput("Email ID", "Email")
        hospital["address"] = validateInput("Address", "Address")

        SQL_query = "INSERT INTO hospital (name, address, email_id, phone_number)" \
                    "VALUES(%s, %s, %s, %s)"

        cfg.cursor.execute(SQL_query, (hospital["name"], hospital["address"], hospital["email"], hospital["phoneno"]))
        cfg.db.commit()
        print(cfg.GREEN, "Insert successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to insert into database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


# def placeOrder():
#     pass
