
ALTER TABLE `raw_shots`
	ROW_FORMAT=DEFAULT,
	AUTO_INCREMENT=0,
	ADD COLUMN `shot_id` INT(11) NOT NULL FIRST;
	
ALTER TABLE `raw_shots`
	ADD INDEX `Index 1` (`shot_id`);
	
	
	
