drop database if exists bmicalc;
create database if not exists bmicalc;
use bmicalc;

create table if not exists patient (
pid int(10) unsigned NOT NULL AUTO_INCREMENT primary key,
name varchar(50),
age tinyint(3),
phone bigint(10),
gender varchar(20),
bmi decimal(10,2),
date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


DELIMITER $$
drop trigger if exists t1 $$
create trigger t1 before insert on patient for each row
begin
	if length(new.name) < 2 or new.name is null then
		signal SQLSTATE '23456' set message_text="Invalid Name. Enter a valid name with alteast 2 charecters";
	end if;
	if new.age < 1 then 
		signal SQLSTATE '12345' set message_text="Age canot be negative! Neither can it be 0! Nor can it be more than 120 ";
	end if;
	if new.age > 120 then 
		signal SQLSTATE '12345' set message_text="Age canot be negative! Neither can it be 0! Nor can it be more than 120 ";
	end if;
	if length(new.phone) != 10 or new.phone is null then
		signal SQLSTATE '23456' set message_text="invalid Phone number";
	end if;



end $$

DELIMITER ;

DELIMITER $$

drop procedure if exists p1 $$
Create PROCEDURE p1(IN name varchar(50),IN age tinyint(3), IN phone bigint(10), IN gender varchar(20), IN bmi decimal(10,2))
BEGIN
insert into patient (name, age, phone, gender, bmi) values (name, age, phone, gender, bmi);
END $$

DELIMITER ;

DELIMITER $$

drop procedure if exists p2 $$
Create PROCEDURE p2(out c INT )
BEGIN
select count(*) into c from patient;

select @c;
END $$

DELIMITER ;

DELIMITER $$
drop procedure if exists p3 $$
create PROCEDURE p3()
BEGIN
SET @TS = DATE_FORMAT(NOW(),'_%d_%m_%Y_%H_%i_%s');

SET @FOLDER = "G:\\";
SET @PREFIX = "Patient_Data";
SET @EXT    = '.csv';

SET @CMD = CONCAT("(select 'pid','name','age','phone','gender','bmi','date') union SELECT * FROM patient INTO OUTFILE '",@FOLDER,@PREFIX,@TS,@EXT,
				   "' FIELDS ENCLOSED BY '\"' TERMINATED BY ',' ESCAPED BY '\"'",
				   "  LINES TERMINATED BY '\r\n';");

PREPARE statement FROM @CMD;

EXECUTE statement;
END $$
DELIMITER ;