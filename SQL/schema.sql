# IF DATABASE WITH SAME NAME EXISTS ALREADY DELETE IT
DROP DATABASE IF EXISTS bloodbank;
CREATE DATABASE bloodbank;
USE bloodbank;


CREATE TABLE `blood_donation_center` (
  `center_id` int AUTO_INCREMENT,
  `phone_number` varchar(15) NOT NULL,
  `address` varchar(100) NOT NULL,
  PRIMARY KEY (`center_id`)
);

CREATE TABLE `receptionist` (
  `employee_id` int AUTO_INCREMENT,
  `center_id` int NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30),
  `last_name` varchar(30) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  PRIMARY KEY (`employee_id`),
  FOREIGN KEY (`center_id`) REFERENCES `blood_donation_center` (`center_id`) ON DELETE CASCADE
);

CREATE TABLE `donor` (
  `donor_id` int AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `middle_name` varchar(30),
  `last_name` varchar(30) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(10) NOT NULL,
  `date_of_registration` date NOT NULL,
  PRIMARY KEY (`donor_id`),
  FOREIGN KEY (`employee_id`) REFERENCES `receptionist` (`employee_id`) ON DELETE CASCADE
);

CREATE TABLE `donor_address` (
  `donor_id` int,
  `address` varchar(100),
  PRIMARY KEY (`donor_id`, `address`),
  FOREIGN KEY (`donor_id`) REFERENCES `donor` (`donor_id`) ON DELETE CASCADE
);

CREATE TABLE `donation` (
  `donation_id` int AUTO_INCREMENT,
  `blood_pressure` varchar(10) NOT NULL,
  `haemoglobin_level` varchar(10) NOT NULL,
  `date_of_donation` date NOT NULL,
  `weight` decimal NOT NULL,
  `travel_history` varchar(255) NOT NULL,
  PRIMARY KEY (`donation_id`)
);

CREATE TABLE `blood_cost` (
  `blood_type` varchar(20),
  `blood_type_cost` decimal NOT NULL,
  PRIMARY KEY (`blood_type`)
);

CREATE TABLE `blood` (
  `blood_barcode` int AUTO_INCREMENT,
  `blood_type` varchar(20) NOT NULL,
  `description` varchar(255),
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_type`) REFERENCES `blood_cost` (`blood_type`) ON DELETE CASCADE
);

CREATE TABLE `donor_participation` (
  `blood_barcode` int,
  `donor_id` int NOT NULL,
  `center_id` int NOT NULL,
  `donation_id` int NOT NULL,
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`) ON DELETE CASCADE,
  FOREIGN KEY (`donor_id`) REFERENCES `donor` (`donor_id`) ON DELETE CASCADE,
  FOREIGN KEY (`center_id`) REFERENCES `blood_donation_center` (`center_id`) ON DELETE CASCADE,
  FOREIGN KEY (`donation_id`) REFERENCES `donation` (`donation_id`) ON DELETE CASCADE
);

CREATE TABLE `test_result` (
  `blood_barcode` int,
  `hiv1` bool NOT NULL,
  `hiv2` bool NOT NULL,
  `hepatitis_b` bool NOT NULL,
  `hepatitis_c` bool NOT NULL,
  `htlv1` bool NOT NULL,
  `htlv2` bool NOT NULL,
  `syphilis` bool NOT NULL,
  PRIMARY KEY (`blood_barcode`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`) ON DELETE CASCADE
);

CREATE TABLE `component` (
  `component_id` int AUTO_INCREMENT,
  `component_type` varchar(20) NOT NULL,
  `standard_quantity` decimal NOT NULL,
  `storage_temperature` decimal NOT NULL,
  `max_storage_duration` int NOT NULL,
  PRIMARY KEY (`component_id`)
);

CREATE TABLE `hospital` (
  `hospital_id` int AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `address` varchar(100) NOT NULL,
  `email_id` varchar(50) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  PRIMARY KEY (`hospital_id`)
);

CREATE TABLE `orders` (
  `order_id` int AUTO_INCREMENT,
  `hospital_id` int NOT NULL,
  `date_of_order` date NOT NULL,
  `total_cost` decimal NOT NULL,
  PRIMARY KEY (`order_id`),
  FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`hospital_id`) ON DELETE CASCADE
);

CREATE TABLE `order_components` (
  `order_id` int,
  `blood_type` varchar(20),
  `component_type` varchar(20),
  `quantity` int NOT NULL,
  PRIMARY KEY (`order_id`, `blood_type`, `component_type`),
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE
);

CREATE TABLE `blood_inventory` (
  `blood_barcode` int,
  `component_id` int,
  `order_id` int,
  `date_of_storage` date NOT NULL,
  PRIMARY KEY (`blood_barcode`, `component_id`),
  FOREIGN KEY (`blood_barcode`) REFERENCES `blood` (`blood_barcode`) ON DELETE CASCADE,
  FOREIGN KEY (`component_id`) REFERENCES `component` (`component_id`) ON DELETE CASCADE,
  FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE
);


INSERT into blood_donation_center (phone_number, address) values("6024049178", "Level 0 44 Trisha Roadside Vincentberg, SA 0234");
INSERT into blood_donation_center (phone_number, address) values("1265418099", "0 Grady Crossway Cloydview, NT 0939");
INSERT into blood_donation_center (phone_number, address) values("1265218099", "Level 0 424 Nellie Line Greggville, ACT 2920");

INSERT into receptionist (center_id, first_name, middle_name, last_name, phone_number) values (1, "Dario", "Borer", "Boris", "720801445");
INSERT into receptionist (center_id, first_name, middle_name, last_name, phone_number) values (2, "Frida", "Borer", "Jast", "611711549");
INSERT into receptionist (center_id, first_name, middle_name, last_name, phone_number) values (3, "Tabitha", "", "Paucek", "0714239233");
INSERT into receptionist (center_id, first_name, middle_name, last_name, phone_number) values (1, "Nicklaus", "Lynch", "V", "0720801445");
  
INSERT into donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) values (2, "Adeline", "", "Donnelly", "48518244", "tristian69@hotmail.com.au", "1974-06-27", "F", "2010-05-17");
INSERT into donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) values (1, "Malinda", "II", "Klein", "97615138", "vkuphal@brekke.com.au", "1982-06-27", "F", "2005-05-17");
INSERT into donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) values (4, "Alfredo", "Morar", "PhD", "40534793", "ahyatt@hotmail.com.au", "1996-06-20", "M", "2017-07-30");
INSERT into donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) values (3, "Harvey", "", "Specter", "53400892", "specter@hotmail.com.au", "2000-09-24", "M", "2019-05-13");
INSERT into donor(employee_id, first_name, middle_name, last_name, phone_number, email_id, date_of_birth, gender, date_of_registration) values (3, "Eloy", "", "Zboncak", "866545325", "emilio06@gmail.com.au", "1971-09-30", "F", "2020-07-17");

INSERT into donor_address (donor_id, address) values (1, "Apt. 782 125 Barney Stairs Port Sonny, TAS 2920");
INSERT into donor_address (donor_id, address) values (1, "408B Angeline Stairs Mantetown, VIC 7626");
INSERT into donor_address (donor_id, address) values (2, "710 Orion Walk Hagenesfurt, SA 7443");
INSERT into donor_address (donor_id, address) values (3, "Apt. 662 23 Kertzmann Sound Lucieland, NT 2920");
INSERT into donor_address (donor_id, address) values (4, "8C Amani Crossway New Nicola, NT 2920");
INSERT into donor_address (donor_id, address) values (5, "385A Annabel Basin West Marlin, NT 2680");

INSERT into donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) values ("120/80", "14", "2020-09-15", "44", "travel to the great nation of America (lol)");
INSERT into donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) values ("120/78", "14.5", "2020-09-14", "45", "travel to bangladesh");
INSERT into donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) values ("111/80", "14.55", "2020-08-31", "44", "travel to nowhere");
INSERT into donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) values ("110/67", "14.12", "2020-08-30", "46", "travel to antarctica");
INSERT into donation (blood_pressure, haemoglobin_level, date_of_donation, weight, travel_history) values ("119/77", "13.92", "2020-09-20", "20", "travel to white house");

INSERT into blood_cost (blood_type, blood_type_cost) values ("A+", 220);
INSERT into blood_cost (blood_type, blood_type_cost) values ("B+", 210);
INSERT into blood_cost (blood_type, blood_type_cost) values ("O+", 200);
INSERT into blood_cost (blood_type, blood_type_cost) values ("A-", 220);
INSERT into blood_cost (blood_type, blood_type_cost) values ("B-", 210);
INSERT into blood_cost (blood_type, blood_type_cost) values ("O-", 200);
INSERT into blood_cost (blood_type, blood_type_cost) values ("AB+", 250);
INSERT into blood_cost (blood_type, blood_type_cost) values ("AB-", 250);

INSERT into blood (blood_type) values ("B+");
INSERT into blood (blood_type) values ("A+");
INSERT into blood (blood_type) values ("A-");
INSERT into blood (blood_type) values ("O+");
INSERT into blood (blood_type) values ("A-");

INSERT into donor_participation (blood_barcode, donor_id, center_id, donation_id) values (1, 1, 2, 1);
INSERT into donor_participation (blood_barcode, donor_id, center_id, donation_id) values (2, 2, 1, 2);
INSERT into donor_participation (blood_barcode, donor_id, center_id, donation_id) values (3, 3, 1, 3);
INSERT into donor_participation (blood_barcode, donor_id, center_id, donation_id) values (4, 4, 3, 4);
INSERT into donor_participation (blood_barcode, donor_id, center_id, donation_id) values (5, 3, 1, 5);

INSERT into test_result (blood_barcode, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) values (1, false, false, false, false, false, false, false);
INSERT into test_result (blood_barcode, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) values (2, false, false, false, false, false, false, false);
INSERT into test_result (blood_barcode, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) values (3, false, false, false, false, false, false, false);
INSERT into test_result (blood_barcode, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) values (4, false, false, false, false, false, false, false);
INSERT into test_result (blood_barcode, hiv1, hiv2, hepatitis_b, hepatitis_c, htlv2, htlv1, syphilis) values (5, false, false, false, false, false, false, false);

INSERT into component (component_type, standard_quantity, storage_temperature, max_storage_duration) values ("RBC", 10, 6, 42);
INSERT into component (component_type, standard_quantity, storage_temperature, max_storage_duration) values ("Platelets", 20, 25, 5);
INSERT into component (component_type, standard_quantity, storage_temperature, max_storage_duration) values ("Plasma", 20, 0, 365);

INSERT into hospital (name, address, email_id, phone_number) values ("Synergy", "Rest Port Florida, NT 2092", "pweimann@gmail.com.au", "27585300");
INSERT into hospital (name, address, email_id, phone_number) values ("Melb Hospital", "0B Reggie Colonnade New Rettastad, SA 3439", "walter.jamar@dickens.edu", "19554195");
INSERT into hospital (name, address, email_id, phone_number) values ("Sydney Hospital", "87 Brady Towers St. Isidrochester, NSW 0976", "evangeline94@hotmail.com", " 29431063");
INSERT into hospital (name, address, email_id, phone_number) values ("Adlaide Hospital", "056 Palma Estate New Jovan, VIC 2516", "luettgen.marge@reilly.org", "3383717");

INSERT into orders (hospital_id, date_of_order, total_cost) values (1, "2020-09-25", 440);
INSERT into orders (hospital_id, date_of_order, total_cost) values (2, "2020-09-27", 200);
INSERT into orders (hospital_id, date_of_order, total_cost) values (3, "2020-09-28", 650);
INSERT into orders (hospital_id, date_of_order, total_cost) values (4, "2020-09-29", 430);

INSERT into order_components (order_id, blood_type, component_type, quantity) values (1, "A+", "RBC", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (1, "A-", "RBC", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (2, "O+", "Plasma", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (3, "B+", "RBC", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (3, "A+", "Platelets", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (3, "A-", "Plasma", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (4, "B+", "Plasma", 1);
INSERT into order_components (order_id, blood_type, component_type, quantity) values (4, "A-", "RBC", 1);

INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (1, 1, 3, "2020-09-22");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (1, 2, NULL, "2020-09-22");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (1, 3, 4, "2020-09-22");

INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (2, 1, 1, "2020-08-24");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (2, 2, 3, "2020-08-24");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (2, 3, NULL, "2020-08-24");

INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (3, 1, 1, "2020-09-02");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (3, 2, NULL, "2020-09-02");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (3, 3, 3, "2020-09-02");

INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (4, 1, NULL, "2020-09-05");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (4, 2, NULL, "2020-09-05");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (4, 3, 2, "2020-09-05");

INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (5, 1, 4, "2020-09-26");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (5, 2, NULL, "2020-09-26");
INSERT into blood_inventory (blood_barcode, component_id, order_id, date_of_storage) values (5, 3, NULL, "2020-09-26");

