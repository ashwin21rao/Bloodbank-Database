import pymysql.cursors
import config as cfg
from regexp import validateInput


def removeDonor():
    try:
        donor_id = int(validateInput("Donor ID", "Integer"))
        SQL_query = "DELETE FROM donor WHERE donor_id = %s"

        cfg.cursor.execute(SQL_query, (donor_id))
        cfg.db.commit()
        print(cfg.GREEN, "Delete successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to delete from database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def removeOrderedSamplesFromInventory():
    try:
        SQL_query = "DELETE FROM blood_inventory WHERE order_id IS NOT NULL"

        cfg.cursor.execute(SQL_query)
        cfg.db.commit()
        print(cfg.GREEN, "Delete successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to delete from database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")


def removeExpiredSamplesFromInventory():
    try:
        SQL_query = "DELETE FROM blood_inventory WHERE order_id IS NULL AND date_of_expiry < CURDATE()"

        cfg.cursor.execute(SQL_query)
        cfg.db.commit()
        print(cfg.GREEN, "Delete successful", cfg.RESET, sep="")

    except Exception as e:
        cfg.db.rollback()
        print(cfg.RED, "Failed to delete from database", cfg.RESET, sep="")
        print(cfg.RED, "ERROR>>>>>>>>>>>>> ", e, cfg.RESET, sep="")
