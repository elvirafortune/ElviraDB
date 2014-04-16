SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema ElviraApiDb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `ElviraApiDb` ;
CREATE SCHEMA IF NOT EXISTS `ElviraApiDb` DEFAULT CHARACTER SET utf8 ;
USE `ElviraApiDb` ;

-- -----------------------------------------------------
-- Table `ElviraApiDb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ElviraApiDb`.`user` ;

CREATE TABLE IF NOT EXISTS `ElviraApiDb`.`user` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(200) NOT NULL,
  `name` VARCHAR(100) NULL DEFAULT NULL,
  `about` VARCHAR(100) NULL DEFAULT NULL,
  `username` VARCHAR(50) NULL DEFAULT NULL,
  `isAnonymous` TINYINT(1) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 143
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `ElviraApiDb`.`followers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ElviraApiDb`.`followers` ;

CREATE TABLE IF NOT EXISTS `ElviraApiDb`.`followers` (
  `follower` VARCHAR(200) NOT NULL,
  `followee` VARCHAR(200) NOT NULL,
  `isFollowing` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`follower`, `followee`),
  INDEX `fk_followers_user2_idx` (`followee` ASC),
  CONSTRAINT `fk_followers_user1`
    FOREIGN KEY (`follower`)
    REFERENCES `ElviraApiDb`.`user` (`email`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_followers_user2`
    FOREIGN KEY (`followee`)
    REFERENCES `ElviraApiDb`.`user` (`email`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `ElviraApiDb`.`forum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ElviraApiDb`.`forum` ;

CREATE TABLE IF NOT EXISTS `ElviraApiDb`.`forum` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  `short_name` VARCHAR(100) NOT NULL,
  `user` VARCHAR(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`user`, `short_name`),
  UNIQUE INDEX `short_name_UNIQUE` (`short_name` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_forum_user1_idx` (`user` ASC),
  CONSTRAINT `fk_forum_user1`
    FOREIGN KEY (`user`)
    REFERENCES `ElviraApiDb`.`user` (`email`)
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 105
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `ElviraApiDb`.`thread`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ElviraApiDb`.`thread` ;

CREATE TABLE IF NOT EXISTS `ElviraApiDb`.`thread` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `message` TEXT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `slug` VARCHAR(200) NOT NULL,
  `isClosed` TINYINT(1) NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL,
  `date` DATETIME NOT NULL,
  `likes` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  `dislikes` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  `points` INT(11) NOT NULL DEFAULT '0',
  `user` VARCHAR(200) NOT NULL DEFAULT '',
  `forum` VARCHAR(100) NOT NULL DEFAULT '',
  `posts` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`, `slug`, `user`, `forum`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_thread_user1_idx` (`user` ASC),
  INDEX `fk_thread_forum1_idx` (`forum` ASC),
  CONSTRAINT `fk_thread_forum1`
    FOREIGN KEY (`forum`)
    REFERENCES `ElviraApiDb`.`forum` (`short_name`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_thread_user1`
    FOREIGN KEY (`user`)
    REFERENCES `ElviraApiDb`.`user` (`email`)
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 88
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `ElviraApiDb`.`post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ElviraApiDb`.`post` ;

CREATE TABLE IF NOT EXISTS `ElviraApiDb`.`post` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `isApproved` TINYINT(1) NOT NULL,
  `isDeleted` TINYINT(1) NOT NULL,
  `isHighlighted` TINYINT(1) NOT NULL,
  `isEdited` TINYINT(1) NOT NULL,
  `isSpam` TINYINT(1) NOT NULL,
  `message` TEXT NOT NULL,
  `points` INT(11) NOT NULL DEFAULT '0',
  `likes` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  `dislikes` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  `parent` BIGINT(20) UNSIGNED NULL DEFAULT NULL,
  `user` VARCHAR(200) NOT NULL,
  `thread` BIGINT(20) UNSIGNED NOT NULL,
  `forum` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`, `user`, `thread`, `forum`),
  INDEX `fk_post_user1_idx` (`user` ASC),
  INDEX `fk_post_thread1_idx` (`thread` ASC),
  INDEX `fk_post_post1_idx` (`parent` ASC),
  INDEX `fk_post_forum1_idx` (`forum` ASC),
  CONSTRAINT `fk_post_thread1`
    FOREIGN KEY (`thread`)
    REFERENCES `ElviraApiDb`.`thread` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_forum1`
    FOREIGN KEY (`forum`)
    REFERENCES `ElviraApiDb`.`forum` (`short_name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_post1`
    FOREIGN KEY (`parent`)
    REFERENCES `ElviraApiDb`.`post` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_user1`
    FOREIGN KEY (`user`)
    REFERENCES `ElviraApiDb`.`user` (`email`)
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 73
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `ElviraApiDb`.`subscription`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ElviraApiDb`.`subscription` ;

CREATE TABLE IF NOT EXISTS `ElviraApiDb`.`subscription` (
  `user` VARCHAR(200) NOT NULL DEFAULT '',
  `thread` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0',
  `isSubscribed` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user`, `thread`),
  INDEX `fk_subscription_thread1_idx` (`thread` ASC),
  INDEX `fk_subscription_user1_idx` (`user` ASC),
  CONSTRAINT `fk_subscription_thread1`
    FOREIGN KEY (`thread`)
    REFERENCES `ElviraApiDb`.`thread` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_subscription_user1`
    FOREIGN KEY (`user`)
    REFERENCES `ElviraApiDb`.`user` (`email`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
