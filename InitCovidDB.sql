DROP DATABASE IF EXISTS coviddb;
CREATE DATABASE IF NOT EXISTS coviddb;
DROP USER IF EXISTS 'djangouser'@'%';
FLUSH PRIVILEGES;
CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'admin';
GRANT ALL ON coviddb.* TO 'djangouser'@'%';
FLUSH PRIVILEGEs;

USE coviddb;
/* -------------- */

/* CREATE regions */
CREATE TABLE regions
(
	regionID INT(1) CHECK (regionID IN (1,2,3,4)),
	regionName CHAR(8) CHECK (regionName IN ('Flanders','Wallonia','Brussels',NULL)),
	
	primary key(regionID)
);

INSERT INTO regions(regionID,regionName) VALUES 
	(1,NULL),
	(2,'Flanders'),
	(3,'Wallonia'),
	(4,'Brussels');
/* ---------------- */

/* CREATE provinces */
CREATE TABLE provinces
(
	provinceID INT(2) UNIQUE AUTO_INCREMENT,
	regionID INT(1) CHECK (regionID IN (1,2,3,4)),
	provinceName VARCHAR(14) CHECK (provinceName IN ('Antwerpen','WestVlaanderen','OostVlaanderen','Limburg','VlaamsBrabant','Brussels','Hainaut','Luxembourg','Liège','BrabantWallon','Namur',NULL)),
	
	primary key(provinceID),
	foreign key(regionID) references regions(regionID)
);

INSERT INTO provinces(regionID, provinceName) VALUES
	(1,NULL),
	(2,'Antwerpen'),
	(2,'WestVlaanderen'),
	(2,'OostVlaanderen'),
	(2,'Limburg'),
	(2,'VlaamsBrabant'),
	(3,'Hainaut'),
	(3,'Luxembourg'),
	(3,'Liège'),
	(3,'BrabantWallon'),
	(3,'Namur'),
	(4,'Brussels');
/* ------------------ */

/* CREATE cases table */
CREATE TABLE cases
(
	caseID INT NOT NULL UNIQUE AUTO_INCREMENT,
	caseDate DATE,
	caseProvinceID INT(2) DEFAULT 1,
	caseRegionID INT(1) DEFAULT 1,
	caseAgeGroup VARCHAR(5) CHECK (caseAgeGroup IN ('0-9','10-19','20-29','30-39','40-49','50-59','60-69','70-79','80-89','90+')),
	caseSex CHAR(1) CHECK (caseSex IN ('M','F')),
	cases INT,
	
	primary key(caseID),
	foreign key(caseProvinceID) references provinces(provinceID),
	foreign key(caseRegionID) references regions(regionID)
);
/* ----------------------------- */

/* CREATE hospitalisations table */
CREATE TABLE hosps
(
	hospID INT NOT NULL UNIQUE AUTO_INCREMENT,
	hospDate DATE NOT NULL,
	hospProvinceID INT(2) DEFAULT 1,
	hospRegionID INT(1) DEFAULT 1,
	totalInHosp INT,
	totalInICU INT,
	totalInResp INT,
	newInHosp INT,
	newOutHosp INT,
	
	primary key(hospID),
	foreign key(hospProvinceID) references provinces(provinceID),
	foreign key(hospRegionID) references regions(regionID)
);
/* ------------------- */

/* CREATE deaths table */
CREATE TABLE deaths
(
	deathID INT NOT NULL UNIQUE AUTO_INCREMENT,
	deathDate DATE NOT NULL,
	deathRegionID INT(1) DEFAULT 1,
	deathAgeGroup VARCHAR(5) CHECK (deathAgeGroup in ('0-24','25-44','45-64','65-74','75-84','85+')),
	deathSex CHAR(1) CHECK (deathSex IN ('M','F')),
	deaths INT,
	
	primary key(deathID),
	foreign key(deathRegionID) references regions(regionID)
);
/* ------------------ */

/* CREATE tests table */
CREATE TABLE tests
(
	testID INT NOT NULL UNIQUE AUTO_INCREMENT,
	testDate DATE DEFAULT NULL,
	testProvinceID INT(2) DEFAULT 1,
	testRegionID INT(1) DEFAULT 1,
	testAll INT,
	testPos INT,
	
	primary key(testID),
	foreign key(testProvinceID) references provinces(provinceID),
	foreign key(testRegionID) references regions(regionID)
);

