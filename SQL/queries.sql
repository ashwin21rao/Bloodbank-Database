-- SELECTION QUERIES

-- get details of all donors who have donated
SELECT DISTINCT donor.donor_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, blood_type FROM donor 
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
    JOIN test_result ON blood.blood_barcode = test_result.blood_barcode;

-- generate blood inventory report
SELECT * FROM blood_inventory ORDER BY date_of_storage;

-- get orders on a particular date
SELECT * FROM orders WHERE date_of_order = "2020/12/1";

-- find most commonly ordered blood type and component type
SELECT blood_type, component_type, COUNT(*) AS total_orders FROM blood_inventory
    JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode
    JOIN component ON blood_inventory.component_id = component.component_id
    JOIN test_result ON blood.blood_barcode = test_result.blood_barcode
WHERE order_id IS NOT NULL
GROUP BY blood_type, component_type
ORDER BY total_orders DESC;

-- find total stock of each blood type and component type
SELECT blood_type, component_type, COUNT(*) AS total_stock FROM blood_inventory
    JOIN blood ON blood_inventory.blood_barcode = blood.blood_barcode
    JOIN component ON blood_inventory.component_id = component.component_id
    JOIN test_result ON blood.blood_barcode = test_result.blood_barcode
WHERE order_id IS NULL
GROUP BY blood_type, component_type
ORDER BY total_stock DESC;

-- find samples in blood inventory which have expired
SELECT blood_inventory.blood_barcode, blood_inventory.component_id, blood_inventory.date_of_storage, component.max_storage_duration FROM blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE();

-- get donors in a specific age group
SELECT * FROM donor WHERE TIMESTAMPDIFF(year, date_of_birth, CURDATE()) BETWEEN 20 AND 30;

-- get donors living in a particular area
SELECT donor.*, donor_address.address FROM donor
    JOIN donor_address ON donor.donor_id = donor_address.donor_id
WHERE donor_address.address LIKE CONCAT('%', 'bangalore', '%');

-- get donors with a specific blood type
SELECT DISTINCT donor.* FROM donor
    JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
    JOIN test_result ON blood.blood_barcode = test_result.blood_barcode
WHERE blood_type = 'B+';

-- get blood donations with a specific test result
SELECT donor_participation.*, blood.test_result FROM donor_participation
    JOIN blood ON donor_participation.blood_barcode = blood.blood_barcode
WHERE blood.test_result = "Negative"

-- get donors registered by a particular employee
SELECT * FROM donor WHERE employee_id = 12;

-- get donors registered at a particular center
SELECT donor.* FROM donor
    JOIN receptionist ON donor.employee_id = receptionist.employee_id
    JOIN blood_donation_center ON receptionist.center_id = blood_donation_center.center_id
WHERE blood_donation_center.center_id = 12;

-- get donors who have donated at a particular center
SELECT DISTINCT donor.* FROM donor
    LEFT JOIN donor_participation ON donor.donor_id = donor_participation.donor_id
    LEFT JOIN blood_donation_center ON donor_participation.center_id = blood_donation_center.center_id
WHERE blood_donation_center.center_id = 12;


-- INSERTION QUERIES

-- add a donor
INSERT INTO donor (employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) 
VALUES (1, "John", NULL, "Doe", "9980221156", "johndoe@yoyo.com", "1995/06/12", "M", CURDATE());

-- add a receptionist
INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number)
VALUES(1, "Jane", NULL, "Doe", "9882736152")

-- add a blood donation center
INSERT INTO blood_donation_center (phone_number, address)
VALUES("7162830483", "Bangalore, India")

-- add a donation
INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history)
VALUES ("160/90", 15, CURDATE(), 75.5, NULL)

-- add a blood test result
INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis)
VALUES (1, "B+", false, false, false, false, false, false, false);

-- add a sample to blood inventory
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage)
VALUES (2, 2, NULL, "2020-12-12");


-- UPDATE QUERIES

-- update phone number of a donor
UPDATE donor SET phone_number = "8890096331" WHERE donor_id = 1;

-- update email address of a donor
UPDATE donor SET email_id = "johndoe&gmail.com" WHERE donor_id = 1;

-- add another address for specified donor
INSERT INTO donor_address (donor_id, address) VALUES (1, "South India");

-- delete specified address of a donor
DELETE FROM donor_address WHERE donor_id = 1 AND address = "North India";


-- DELETE QUERIES

-- remove a donor
DELETE FROM donor WHERE donor_id = 1;

-- delete ordered samples from inventory
DELETE FROM blood_inventory WHERE order_id IS NOT NULL;

-- delete expired samples from inventory
DELETE blood_inventory FROM blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
WHERE order_id IS NULL AND date_of_storage + INTERVAL max_storage_duration DAY < CURDATE();
