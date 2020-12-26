import pymysql.cursors
from prettytable import from_db_cursor
import config as cfg
from regexp import validateInput


def getDonorDetails():
    try:
        SQL_query = "SELECT DISTINCT donor.donor_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, blood_type FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode"

        cfg.cursor.execute(SQL_query)
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def generateBloodInventoryReport():
    try:
        SQL_query = "SELECT * FROM blood_inventory ORDER BY date_of_storage"

        cfg.cursor.execute(SQL_query)
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDailyOrders():
    try:
        date = validateInput("Date (YYYY/MM/DD)", "Date")
        SQL_query = "SELECT * FROM orders WHERE date_of_order = %s"

        cfg.cursor.execute(SQL_query, (date))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonorsByAge():
    try:
        lower_age = int(validateInput("Lower Age", "Integer"))
        upper_age = int(validateInput("Upper Age", "Integer"))
        SQL_query = "SELECT * FROM donor WHERE TIMESTAMPDIFF(year, date_of_birth, CURDATE()) BETWEEN %s AND %s"

        cfg.cursor.execute(SQL_query, (lower_age, upper_age))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def findCommonlyOrderedBloodTypes():
    try:
        SQL_query = "SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory " \
                    "JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE order_id IS NOT NULL " \
                    "GROUP BY blood_type, component_type " \
                    "ORDER BY total_orders DESC"

        cfg.cursor.execute(SQL_query)
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def findTotalStock():
    try:
        SQL_query = "SELECT blood_type, component_type, COUNT(*) AS total_stock FROM blood_inventory " \
                    "JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode " \
                    "JOIN component ON blood_inventory.component_id = component.component_id " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE order_id IS NULL " \
                    "GROUP BY blood_type, component_type " \
                    "ORDER BY total_stock DESC"

        cfg.cursor.execute(SQL_query)
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonorsFromArea():
    try:
        search_string = input("Search String: ")
        SQL_query = "SELECT donor.*, donor_address.address FROM donor " \
                    "JOIN donor_address ON donor.donor_id = donor_address.donor_id " \
                    "WHERE donor_address.address LIKE CONCAT(%s, %s, %s)"

        cfg.cursor.execute(SQL_query, ("%", search_string, "%"))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonorsFromBloodType():
    try:
        blood_type = validateInput("Blood Type ([ABO][+-])", "Blood")
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "JOIN test_result ON blood.blood_barcode = test_result.blood_barcode " \
                    "WHERE blood_type = %s"

        cfg.cursor.execute(SQL_query, (blood_type))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonationsFromTestResults():
    try:
        test_result = validateInput("Test Result (Negative/Positive/Pending)", "Result")
        SQL_query = "SELECT donor_participation.*, blood.test_result FROM donor_participation " \
                    "JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode " \
                    "WHERE blood.test_result = %s"

        cfg.cursor.execute(SQL_query, (test_result))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonorsFromEmployee():
    try:
        employee_id = int(validateInput("Employee ID", "Integer"))
        SQL_query = "SELECT * FROM donor WHERE employee_id = %s"

        cfg.cursor.execute(SQL_query, (employee_id))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonorsRegisteredAtCenter():
    try:
        center_id = int(validateInput("Center ID", "Integer"))
        SQL_query = "SELECT donor.* FROM donor " \
                    "JOIN receptionist ON donor.employee_id = receptionist.employee_id " \
                    "JOIN blood_donation_center ON receptionist.center_id = blood_donation_center.center_id " \
                    "WHERE blood_donation_center.center_id = %s"

        cfg.cursor.execute(SQL_query, (center_id))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def getDonorsDonatedAtCenter():
    try:
        center_id = int(validateInput("Center ID", "Integer"))
        SQL_query = "SELECT DISTINCT donor.* FROM donor " \
                    "JOIN donor_participation ON donor.donor_id = donor_participation.donor_id " \
                    "JOIN blood_donation_center ON donor_participation.center_id = blood_donation_center.center_id " \
                    "WHERE blood_donation_center.center_id = %s"

        cfg.cursor.execute(SQL_query, (center_id))
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def findExpiredBlood():
    try:
        SQL_query = "SELECT blood_barcode, component_id, date_of_storage, date_of_expiry FROM blood_inventory " \
                    "WHERE order_id IS NULL AND date_of_expiry < CURDATE()"

        cfg.cursor.execute(SQL_query)
        table = from_db_cursor(cfg.cursor)
        table.align = "r"
        print(table)

    except Exception as e:
        print(cfg.RED, "Query failed", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")
