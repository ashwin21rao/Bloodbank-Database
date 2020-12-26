import subprocess as sp
import pymysql
import pymysql.cursors
from getpass import getpass
import config as cfg
import insertions
import updates
import deletions
import selections


def connectToDatabase():
    sp.call('clear', shell=True)

    try:
        username = input("Username: ")
        password = getpass("Password: ")
        cfg.db = pymysql.connect(host='localhost',
                             user=username,
                             password=password,
                             db='bloodbank')
        sp.call('clear', shell=True)
        if cfg.db.open:
            print("Connected")
        else:
            print("Failed to connect")
    except Exception:
        sp.call('clear', shell=True)
        print(cfg.RED,
              "Connection Refused: Either username or password is incorrect or user doesn't have access to database",
              cfg.RESET, sep="")
        tmp = input("Enter Q to quit, any other key to continue>")
        if tmp == 'Q':
            return
        connectToDatabase()


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
            "Place an Order",
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
            if i+1 in [8, 22, 27, 28]:
                print("---------------------------------------------------")
        try:
            choice = int(input("Enter choice> "))
        except ValueError:
            sp.call('clear', shell=True)
            print(cfg.RED, "Error: Invalid Choice", cfg.RESET, sep="")
            input("Press Enter to CONTINUE> ")
            continue

        sp.call('clear', shell=True)

        if choice == 28:
            break
        else:
            if choice == 1:
                insertions.addDonor()
            elif choice == 2:
                insertions.addReceptionist()
            elif choice == 3:
                insertions.addBloodDonationCenter()
            elif choice == 4:
                insertions.addDonation()
            elif choice == 5:
                insertions.addTestResult()
            elif choice == 6:
                insertions.addToInventory()
            elif choice == 7:
                insertions.addHospital()
            elif choice == 8:
                insertions.placeOrder()
            elif choice == 9:
                selections.getDonorDetails()
            elif choice == 10:
                selections.generateBloodSampleList()
            elif choice == 11:
                selections.generateBloodInventoryReport()
            elif choice == 12:
                selections.getDailyOrders()
            elif choice == 13:
                selections.findCommonlyOrderedBloodTypes()
            elif choice == 14:
                selections.findTotalStock()
            elif choice == 15:
                selections.findExpiredBlood()
            elif choice == 16:
                selections.getDonorsByAge()
            elif choice == 17:
                selections.getDonorsFromArea()
            elif choice == 18:
                selections.getDonorsFromBloodType()
            elif choice == 19:
                selections.getDonationsFromTestResults()
            elif choice == 20:
                selections.getDonorsFromEmployee()
            elif choice == 21:
                selections.getDonorsRegisteredAtCenter()
            elif choice == 22:
                selections.getDonorsDonatedAtCenter()
            elif choice == 23:
                updates.updateDonorDetails()
            elif choice == 24:
                deletions.removeDonor()
            elif choice == 25:
                deletions.removeOrderedSamplesFromInventory()
            elif choice == 26:
                deletions.removeExpiredSamplesFromInventory()
            elif choice == 27:
                deletions.removeDiseasedBlood()
            else:
                print(cfg.RED, "Error: Invalid Choice", cfg.RESET, sep="")
            input("Press Enter to CONTINUE> ")


connectToDatabase()
if cfg.db is None:
    exit(1)
else:
    cfg.cursor = cfg.db.cursor()
    cfg.dict_cursor = cfg.db.cursor(pymysql.cursors.DictCursor)
    loop()
