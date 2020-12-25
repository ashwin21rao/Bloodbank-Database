import pymysql.cursors
import config as cfg
from regexp import validateInput


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
            print(cfg.RED, "Invalid Choice", cfg.RESET, sep="")
            return

        if choice == 1:
            phone_number = validateInput("New Phone Number", "Integer")
            SQL_query = "UPDATE donor SET phone_number = %s WHERE donor_id = %s"
            cfg.cursor.execute(SQL_query, (phone_number, donor_id))
        elif choice == 2:
            email_id = validateInput("New Email ID", "Email")
            SQL_query = "UPDATE donor SET email_id = %s WHERE donor_id = %s"
            cfg.cursor.execute(SQL_query, (email_id, donor_id))
        elif choice == 3:
            address = validateInput("New Address", "Address")
            SQL_query = "INSERT INTO donor_address (donor_id, address) VALUES (%s, %s)"
            cfg.cursor.execute(SQL_query, (donor_id, address))
        elif choice == 4:
            address = validateInput("Address", "Address")
            SQL_query = "DELETE FROM donor_address WHERE donor_id = %s AND address = %s"
            cfg.cursor.execute(SQL_query, (donor_id, address))
        else:
            return

        cfg.db.commit()
        print(cfg.GREEN, "Update successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to update database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")
