-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema FinalProject
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema FinalProject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `FinalProject` DEFAULT CHARACTER SET latin1 ;
USE `FinalProject` ;

-- -----------------------------------------------------
-- Table `FinalProject`.`Seller`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Seller` (
  `seller_id` INT(4) NOT NULL DEFAULT '0',
  `phone_num` VARCHAR(12) NULL DEFAULT NULL,
  `email` VARCHAR(70) NULL DEFAULT NULL,
  `seller_fname` VARCHAR(30) NULL DEFAULT NULL,
  `seller_lname` VARCHAR(30) NULL DEFAULT NULL,
  PRIMARY KEY (`seller_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`Home`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Home` (
  `hid` INT(5) NOT NULL,
  `address` VARCHAR(40) NOT NULL,
  `home_type` VARCHAR(40) NOT NULL,
  `acres` INT(3) NOT NULL,
  `construct_date` VARCHAR(10) NOT NULL,
  `cost` DOUBLE(8,2) NULL DEFAULT NULL,
  `seller` INT(4) NULL DEFAULT NULL,
  PRIMARY KEY (`hid`),
  UNIQUE INDEX `hid` (`hid` ASC),
  INDEX `seller` (`seller` ASC),
  CONSTRAINT `Home_ibfk_1`
    FOREIGN KEY (`seller`)
    REFERENCES `FinalProject`.`Seller` (`seller_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NOT NULL,
  `email` VARCHAR(120) NULL DEFAULT NULL,
  `password_hash` VARCHAR(128) NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `username`),
  UNIQUE INDEX `id` (`id` ASC),
  UNIQUE INDEX `username` (`username` ASC),
  INDEX `ix_user_email` (`email` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 43
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`Bookmarks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Bookmarks` (
  `bookmark_id` INT(6) NOT NULL DEFAULT '0',
  `home` INT(5) NULL DEFAULT NULL,
  `user` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`bookmark_id`),
  INDEX `home` (`home` ASC),
  INDEX `user` (`user` ASC),
  CONSTRAINT `Bookmarks_ibfk_1`
    FOREIGN KEY (`home`)
    REFERENCES `FinalProject`.`Home` (`hid`),
  CONSTRAINT `Bookmarks_ibfk_2`
    FOREIGN KEY (`user`)
    REFERENCES `FinalProject`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`Features`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Features` (
  `entryid` INT(3) NOT NULL,
  `house` INT(5) NOT NULL,
  `feature_type` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`entryid`),
  UNIQUE INDEX `entryid` (`entryid` ASC),
  INDEX `house` (`house` ASC),
  CONSTRAINT `Features_ibfk_1`
    FOREIGN KEY (`house`)
    REFERENCES `FinalProject`.`Home` (`hid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`Room`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Room` (
  `house` INT(5) NOT NULL,
  `room_type` VARCHAR(15) NOT NULL,
  `amount` INT(2) NULL DEFAULT NULL,
  `entryid` INT(2) NOT NULL,
  PRIMARY KEY (`entryid`),
  INDEX `house` (`house` ASC),
  CONSTRAINT `Room_ibfk_1`
    FOREIGN KEY (`house`)
    REFERENCES `FinalProject`.`Home` (`hid`),
  CONSTRAINT `Room_ibfk_2`
    FOREIGN KEY (`house`)
    REFERENCES `FinalProject`.`Home` (`hid`),
  CONSTRAINT `Room_ibfk_3`
    FOREIGN KEY (`house`)
    REFERENCES `FinalProject`.`Home` (`hid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`Utilities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Utilities` (
  `entryid` INT(5) NOT NULL,
  `house` INT(5) NOT NULL,
  `util_type` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`entryid`),
  UNIQUE INDEX `entryid` (`entryid` ASC),
  INDEX `house` (`house` ASC),
  CONSTRAINT `Utilities_ibfk_1`
    FOREIGN KEY (`house`)
    REFERENCES `FinalProject`.`Home` (`hid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `FinalProject`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`users` (
  `idusers` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email_address` VARCHAR(45) NOT NULL,
  `phone_number` INT(12) NOT NULL,
  PRIMARY KEY (`idusers`),
  UNIQUE INDEX `idusers_UNIQUE` (`idusers` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_address_UNIQUE` (`email_address` ASC),
  UNIQUE INDEX `phone_number_UNIQUE` (`phone_number` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
