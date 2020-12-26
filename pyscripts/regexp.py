import re
import config as cfg


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
    elif inp_type == "Component":
        validator = lambda c_type: c_type in ["RBC", "Plasma", "Platelets"]
    elif inp_type == "BP":
        validator = lambda bp: re.match("^\d{2,3}/\d{2,3}$", bp)
    elif inp_type == "Result":
        validator = lambda res: res == "Positive" or res == "Negative" or res == "Pending"

    inp = input(inp_str + ": ")
    while not validator(inp):
        if (opt and not inp):
            return inp
        print(cfg.RED, "Invalid input", cfg.RESET, sep="")
        inp = input(inp_str + ": ")
    return inp
