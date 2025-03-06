CREATE TABLE geocoded_aqi_dataset (
	`CITY` VARCHAR(42) NOT NULL, 
	`CBSA` VARCHAR(46) NOT NULL, 
	`Percent_Unhealthy_Days` DECIMAL(38, 17) NOT NULL, 
	`Latitude` DECIMAL(38, 15), 
	`Longitude` DECIMAL(38, 14)
);
