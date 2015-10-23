
/* Entering session "Unnamed" */
SHOW CREATE TABLE `nbashots`.`raw_shots`;
SHOW CREATE DATABASE `nbashots`;
SHOW CREATE TABLE `nbashots`.`raw_shots`;
SHOW CREATE TABLE `nbashots`.`teams`;
ALTER TABLE `raw_shots`
	CHANGE COLUMN `Column 1` `Rk` INT(11) NULL DEFAULT NULL FIRST,
	ADD COLUMN `Date` DATE NULL DEFAULT NULL AFTER `Rk`,
	ADD COLUMN `Tm` TEXT(3) NULL DEFAULT NULL AFTER `Date`,
	ADD COLUMN `Opp` DATE NULL DEFAULT NULL AFTER `Tm`,
	ADD COLUMN `Column 5` DATE NULL DEFAULT NULL AFTER `Opp`,
	ADD COLUMN `Column 6` DATE NULL DEFAULT NULL AFTER `Column 5`,
	ADD COLUMN `Column 7` DATE NULL DEFAULT NULL AFTER `Column 6`,
	ADD COLUMN `Column 8` DATE NULL DEFAULT NULL AFTER `Column 7`,
	ADD COLUMN `Column 9` DATE NULL DEFAULT NULL AFTER `Column 8`;
SELECT `DEFAULT_COLLATION_NAME` FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME`='nbashots';
SHOW TABLE STATUS FROM `nbashots`;
SHOW FUNCTION STATUS WHERE `Db`='nbashots';
SHOW PROCEDURE STATUS WHERE `Db`='nbashots';
SHOW TRIGGERS FROM `nbashots`;
SELECT *, EVENT_SCHEMA AS `Db`, EVENT_NAME AS `Name` FROM information_schema.`EVENTS` WHERE `EVENT_SCHEMA`='nbashots';
SHOW CREATE TABLE `nbashots`.`raw_shots`;
/* Entering session "Unnamed" */
SHOW CREATE TABLE `nbashots`.`raw_shots`;
ALTER TABLE `raw_shots`
	CHANGE COLUMN `Column 8` `empty` DATE NULL DEFAULT NULL AFTER `Tm`,
	CHANGE COLUMN `Column 5` `Qtr` DATE NULL DEFAULT NULL AFTER `Opp`,
	CHANGE COLUMN `Column 6` `Time` TINYTEXT NULL DEFAULT NULL AFTER `Qtr`,
	CHANGE COLUMN `Column 7` `Score` TINYTEXT NULL DEFAULT NULL AFTER `Time`,
	CHANGE COLUMN `Column 9` `Description` TEXT NULL DEFAULT NULL AFTER `Score`,
	ADD COLUMN `Score_after` TEXT NULL DEFAULT NULL AFTER `Description`;
SELECT `DEFAULT_COLLATION_NAME` FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME`='nbashots';
SHOW TABLE STATUS FROM `nbashots`;
SHOW FUNCTION STATUS WHERE `Db`='nbashots';
SHOW PROCEDURE STATUS WHERE `Db`='nbashots';
SHOW TRIGGERS FROM `nbashots`;
SELECT *, EVENT_SCHEMA AS `Db`, EVENT_NAME AS `Name` FROM information_schema.`EVENTS` WHERE `EVENT_SCHEMA`='nbashots';
SHOW CREATE TABLE `nbashots`.`raw_shots`;
/* Entering session "Unnamed" */
SHOW CREATE TABLE `nbashots`.`raw_shots`;
SHOW CREATE TABLE `nbashots`.`teams`;
SHOW CREATE TABLE `nbashots`.`raw_shots`;
SHOW CREATE DATABASE `nbashots`;
SHOW CREATE TABLE `nbashots`.`raw_shots`;
LOAD DATA LOW_PRIORITY LOCAL INFILE 'C:\\Users\\marc\\Documents\\pynba-tfo\\data_in\\MIA_pbp_fga_x1.csv' REPLACE INTO TABLE `nbashots`.`raw_shots` FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (`Rk`, `Date`, `Tm`, `empty`, `Opp`, `Qtr`, `Time`, `Score`, `Description`, `Score_after`);
/* SQL Error (1265): Data truncated for column 'Rk' at row 1 */
SHOW CREATE DATABASE `nbashots`;
LOAD DATA LOW_PRIORITY LOCAL INFILE 'C:\\Users\\marc\\Documents\\pynba-tfo\\data_in\\MIA_pbp_fga_x1.csv' REPLACE INTO TABLE `nbashots`.`raw_shots` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (`Rk`, `Date`, `Tm`, `empty`, `Opp`, `Qtr`, `Time`, `Score`, `Description`, `Score_after`);
/* SQL Error (1292): Incorrect date value: '' for column 'empty' at row 1 */
ALTER TABLE `raw_shots`
	CHANGE COLUMN `Date` `Date` TINYTEXT NULL DEFAULT NULL AFTER `Rk`,
	CHANGE COLUMN `empty` `empty` TINYTEXT NULL DEFAULT NULL AFTER `Tm`,
	CHANGE COLUMN `Opp` `Opp` TINYTEXT NULL DEFAULT NULL AFTER `empty`,
	CHANGE COLUMN `Qtr` `Qtr` TINYTEXT NULL DEFAULT NULL AFTER `Opp`;
