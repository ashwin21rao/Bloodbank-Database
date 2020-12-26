-- IF DATABASE WITH SAME NAME ALREADY EXISTS, DELETE IT

DROP DATABASE IF EXISTS bloodbank;
CREATE DATABASE bloodbank;
USE bloodbank;


-- CREATE TABLES OF DATABASE

CREATE TABLE `blood_donation_center` (
  `center_id` INT AUTO_INCREMENT,
  `phone_number` VARCHAR(15) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`center_id`)
);

CREATE TABLE `receptionist` (
  `employee_id` INT AUTO_INCREMENT,
  `center_id` INT NOT NULL,
  `first_name` VARCHAR(30) NOT NULL,
  `middle_name` VARCHAR(30),
  `last_name` VARCHAR(30) NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`employee_id`),
  FOREIGN KEY (`center_id`) REFERENCES `blood_donation_center` (`center_id`) ON DELETE CASCADE
);

CREATE TABLE `donor` (
  `donor_id` INT AUTO_INCREMENT,
  `employee_id` INT NOT NULL,
  `first_name` VARCHAR(30) NOT NULL,
  `middle_name` VARCHAR(30),
  `last_name` VARCHAR(30) NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  `email_id` VARCHAR(50) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `gender` VARCHAR(10) NOT NULL,
  `date_of_registration` DATE NOT NULL,
  PRIMARY KEY (`donor_id`),
  FOREIGN KEY (`employee_id`) REFERENCES `receptionist` (`employee_id`) ON DELETE CASCADE
);

CREATE TABLE `donor_address` (
  `donor_id` INT,
  `address` VARCHAR(100),
  PRIMARY KEY (`donor_id`, `address`),
  FOREIGN KEY (`donor_id`) REFERENCES `donor` (`donor_id`) ON DELETE CASCADE
);

CREATE TABLE `donation` (
  `donation_id` INT AUTO_INCREMENT,
  `blood_pressure` VARCHAR(10) NOT NULL,
  `haemoglobin_level` DECIMAL(4, 2) NOT NULL,
  `date_of_donation` DATE NOT NULL,
  `weight` DECIMAL(5, 2) NOT NULL,
  `travel_history` VARCHAR(255),
  PRIMARY KEY (`donation_id`)
);

CREATE TABLE `blood_cost` (
  `blood_type` VARCHAR(20),
  `blood_type_cost` DECIMAL(5, 2) NOT NULL,
  PRIMARY KEY (`blood_type`)
);

CREATE TABLE `blood` (
  `blood_barcode` INT AUTO_INCREMENT,
  `description` VARCHAR(255),
  `test_result` VARCHAR(255),
  PRIMARY KEY (`blood_barcode`)
);

CREATE TABLE `donor_participation` (
  `blood_barcode` INT,
  `donor_id` INT NOT NULL,
  `center_id` INT NOT NULL,
  `donation_id` INT NOT NULL,
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`) ON DELETE CASCADE,
  FOREIGN KEY (`donor_id`) REFERENCES `donor` (`donor_id`) ON DELETE CASCADE,
  FOREIGN KEY (`center_id`) REFERENCES `blood_donation_center` (`center_id`) ON DELETE CASCADE,
  FOREIGN KEY (`donation_id`) REFERENCES `donation` (`donation_id`) ON DELETE CASCADE
);

CREATE TABLE `test_result` (
  `blood_barcode` INT,
  `blood_type` VARCHAR(20) NOT NULL,
  `hiv1` bool NOT NULL,
  `hiv2` bool NOT NULL,
  `hepatitis_b` bool NOT NULL,
  `hepatitis_c` bool NOT NULL,
  `htlv1` bool NOT NULL,
  `htlv2` bool NOT NULL,
  `syphilis` bool NOT NULL,
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`) ON DELETE CASCADE,
  FOREIGN KEY (`blood_type`) REFERENCES `blood_cost` (`blood_type`) ON DELETE CASCADE
);

CREATE TABLE `component` (
  `component_id` INT AUTO_INCREMENT,
  `component_type` VARCHAR(20) NOT NULL,
  `standard_quantity` INT NOT NULL,
  `storage_temperature` DECIMAL(5, 2) NOT NULL,
  `max_storage_duration` INT NOT NULL,
  PRIMARY KEY (`component_id`)
);

CREATE TABLE `hospital` (
  `hospital_id` INT AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `email_id` VARCHAR(50) NOT NULL,
  `phone_number` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`hospital_id`)
);

CREATE TABLE `orders` (
  `order_id` INT AUTO_INCREMENT,
  `hospital_id` INT NOT NULL,
  `date_of_order` DATE NOT NULL,
  `total_cost` DECIMAL(10, 2) NOT NULL,
  PRIMARY KEY (`order_id`),
  FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`hospital_id`) ON DELETE CASCADE
);

CREATE TABLE `order_components` (
  `order_id` INT,
  `blood_type` VARCHAR(20),
  `component_type` VARCHAR(20),
  `quantity` INT NOT NULL,
  PRIMARY KEY (`order_id`, `blood_type`, `component_type`),
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE
);

CREATE TABLE `blood_inventory` (
  `blood_barcode` INT,
  `component_id` INT,
  `order_id` INT,
  `date_of_storage` DATE NOT NULL,
  `date_of_expiry` DATE,
  PRIMARY KEY (`blood_barcode`, `component_id`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`) ON DELETE CASCADE,
  FOREIGN KEY (`component_id`) REFERENCES `component` (`component_id`) ON DELETE CASCADE,
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE
);


-- INSERT SAMPLE DATA INTO TABLES

INSERT INTO blood_donation_center (phone_number, address) VALUES("6024049178", "Level 0 44 Trisha Roadside Vincentberg, SA 0234");
INSERT INTO blood_donation_center (phone_number, address) VALUES("1265418099", "0 Grady Crossway Cloydview, NT 0939");
INSERT INTO blood_donation_center (phone_number, address) VALUES("1265218099", "Level 0 424 Nellie Line Greggville, ACT 2920");

INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number) VALUES (1, "Dario", "Borer", "Boris", "720801445");
INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number) VALUES (2, "Frida", "Borer", "Jast", "611711549");
INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number) VALUES (3, "Tabitha", NULL, "Paucek", "0714239233");
INSERT INTO receptionist (center_id, first_name, middle_name, last_name, phone_number) VALUES (1, "Nicklaus", "Lynch", "V", "0720801445");
  
INSERT INTO donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) VALUES (2, "Adeline", NULL, "Donnelly", "48518244", "tristian69@hotmail.com.au", "1974-06-27", "F", "2010-05-17");
INSERT INTO donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) VALUES (1, "Malinda", "II", "Klein", "97615138", "vkuphal@brekke.com.au", "1982-06-27", "F", "2005-05-17");
INSERT INTO donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) VALUES (4, "Alfredo", "Morar", "PhD", "40534793", "ahyatt@hotmail.com.au", "1996-06-20", "M", "2017-07-30");
INSERT INTO donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) VALUES (3, "Harvey", NULL, "Specter", "53400892", "specter@hotmail.com.au", "2000-09-24", "M", "2019-05-13");
INSERT INTO donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) VALUES (3, "Eloy", NULL, "Zboncak", "866545325", "emilio06@gmail.com.au", "1971-09-30", "F", "2020-07-17");

INSERT INTO donor_address (donor_id, address) VALUES (1, "Apt. 782 125 Barney Stairs Port Sonny, TAS 2920");
INSERT INTO donor_address (donor_id, address) VALUES (1, "408B Angeline Stairs Mantetown, VIC 7626");
INSERT INTO donor_address (donor_id, address) VALUES (2, "710 Orion Walk Hagenesfurt, SA 7443");
INSERT INTO donor_address (donor_id, address) VALUES (3, "Apt. 662 23 Kertzmann Sound Lucieland, NT 2920");
INSERT INTO donor_address (donor_id, address) VALUES (4, "8C Amani Crossway New Nicola, NT 2920");
INSERT INTO donor_address (donor_id, address) VALUES (5, "385A Annabel Basin West Marlin, NT 2680");

INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) VALUES ("120/80", "14", "2020-09-15", "44", "travel to the great nation of America (lol)");
INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) VALUES ("120/78", "14.5", "2020-09-14", "45", "travel to bangladesh");
INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) VALUES ("111/80", "14.55", "2020-08-31", "44", "travel to nowhere");
INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) VALUES ("110/67", "14.12", "2020-08-30", "46", "travel to antarctica");
INSERT INTO donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) VALUES ("119/77", "13.92", "2020-09-20", "20", "travel to white house");

INSERT INTO blood (test_result) VALUES ("Negative");
INSERT INTO blood (test_result) VALUES ("Negative");
INSERT INTO blood (test_result) VALUES ("Negative");
INSERT INTO blood (test_result) VALUES ("Negative");
INSERT INTO blood (test_result) VALUES ("Negative");

INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("A+", 220);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("B+", 210);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("O+", 200);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("A-", 220);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("B-", 210);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("O-", 200);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("AB+", 250);
INSERT INTO blood_cost (blood_type, blood_type_cost) VALUES ("AB-", 250);

INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) VALUES (1, 1, 2, 1);
INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) VALUES (2, 2, 1, 2);
INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) VALUES (3, 3, 1, 3);
INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) VALUES (4, 4, 3, 4);
INSERT INTO donor_participation (blood_barcode, donor_id, center_id, donation_id) VALUES (5, 3, 1, 5);

INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) VALUES (1, "B+", false, false, false, false, false, false, false);
INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) VALUES (2, "A+", false, false, false, false, false, false, false);
INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) VALUES (3, "A-", false, false, false, false, false, false, false);
INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) VALUES (4, "O+", false, false, false, false, false, false, false);
INSERT INTO test_result (blood_barcode, blood_type, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) VALUES (5, "A-", false, false, false, false, false, false, false);

INSERT INTO component (component_type, standard_quantity, storage_temperature, max_storage_duration) VALUES ("RBC", 10, 6, 42);
INSERT INTO component (component_type, standard_quantity, storage_temperature, max_storage_duration) VALUES ("Platelets", 20, 25, 5);
INSERT INTO component (component_type, standard_quantity, storage_temperature, max_storage_duration) VALUES ("Plasma", 20, 0, 365);

INSERT INTO hospital (name, address, email_id, phone_number) VALUES ("Synergy", "Rest Port Florida, NT 2092", "pweimann@gmail.com.au", "27585300");
INSERT INTO hospital (name, address, email_id, phone_number) VALUES ("Melb Hospital", "0B Reggie Colonnade New Rettastad, SA 3439", "walter.jamar@dickens.edu", "19554195");
INSERT INTO hospital (name, address, email_id, phone_number) VALUES ("Sydney Hospital", "87 Brady Towers St. Isidrochester, NSW 0976", "evangeline94@hotmail.com", "29431063");
INSERT INTO hospital (name, address, email_id, phone_number) VALUES ("Adlaide Hospital", "056 Palma Estate New Jovan, VIC 2516", "luettgen.marge@reilly.org", "3383717");

INSERT INTO orders (hospital_id, date_of_order, total_cost) VALUES (1, "2020-09-25", 440);
INSERT INTO orders (hospital_id, date_of_order, total_cost) VALUES (2, "2020-09-27", 200);
INSERT INTO orders (hospital_id, date_of_order, total_cost) VALUES (3, "2020-09-28", 650);
INSERT INTO orders (hospital_id, date_of_order, total_cost) VALUES (4, "2020-09-29", 430);

INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (1, "A+", "RBC", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (1, "A-", "RBC", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (2, "O+", "Plasma", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (3, "B+", "RBC", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (3, "A+", "Platelets", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (3, "A-", "Plasma", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (4, "B+", "Plasma", 1);
INSERT INTO order_components (order_id, blood_type, component_type, quantity) VALUES (4, "A-", "RBC", 1);

INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (1, 1, 3, "2020-09-22");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (1, 2, NULL, "2020-09-22");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (1, 3, 4, "2020-09-22");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (2, 1, 1, "2020-08-24");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (2, 2, 3, "2020-08-24");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (2, 3, NULL, "2020-08-24");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (3, 1, 1, "2020-09-02");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (3, 2, NULL, "2020-09-02");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (3, 3, 3, "2020-09-02");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (4, 1, NULL, "2020-09-05");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (4, 2, NULL, "2020-09-05");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (4, 3, 2, "2020-09-05");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (5, 1, 4, "2020-09-26");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (5, 2, NULL, "2020-09-26");
INSERT INTO blood_inventory (blood_barcode, component_id, order_id, date_of_storage) VALUES (5, 3, NULL, "2020-09-26");

UPDATE blood_inventory
    JOIN component ON blood_inventory.component_id = component.component_id
SET date_of_expiry = date_of_storage + INTERVAL max_storage_duration DAY;
