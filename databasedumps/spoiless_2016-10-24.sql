# ************************************************************
# Sequel Pro SQL dump
# Version 4135
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.42)
# Database: spoiless
# Generation Time: 2016-10-24 16:37:28 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table actors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `actors`;

CREATE TABLE `actors` (
  `actor_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` int(11) DEFAULT NULL,
  PRIMARY KEY (`actor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table appearence
# ------------------------------------------------------------

DROP TABLE IF EXISTS `appearence`;

CREATE TABLE `appearence` (
  `actor_id` int(11) unsigned NOT NULL,
  `character_id` int(11) unsigned NOT NULL,
  `show_id` int(11) unsigned NOT NULL,
  PRIMARY KEY (`actor_id`,`character_id`,`show_id`),
  KEY `character` (`character_id`),
  KEY `show` (`show_id`),
  CONSTRAINT `actor` FOREIGN KEY (`actor_id`) REFERENCES `actors` (`actor_id`),
  CONSTRAINT `character` FOREIGN KEY (`character_id`) REFERENCES `characters` (`character_id`),
  CONSTRAINT `show` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table characters
# ------------------------------------------------------------

DROP TABLE IF EXISTS `characters`;

CREATE TABLE `characters` (
  `character_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` int(11) DEFAULT NULL,
  PRIMARY KEY (`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table shows
# ------------------------------------------------------------

DROP TABLE IF EXISTS `shows`;

CREATE TABLE `shows` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `tvdbid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `shows` WRITE;
/*!40000 ALTER TABLE `shows` DISABLE KEYS */;

INSERT INTO `shows` (`id`, `name`, `year`, `tvdbid`)
VALUES
	(1,'Game of Thrones',2011,NULL),
	(2,'Silicon Valley',2014,NULL),
	(3,'Making a Mu',2015,NULL),
	(4,'Vikings',2013,NULL);

/*!40000 ALTER TABLE `shows` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table spoiler-example
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spoiler-example`;

CREATE TABLE `spoiler-example` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `show_id` int(11) unsigned NOT NULL,
  `training_file` int(11) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`id`,`show_id`),
  KEY `show_id` (`show_id`),
  CONSTRAINT `show_id` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table spoiler-of
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spoiler-of`;

CREATE TABLE `spoiler-of` (
  `user_id` int(11) unsigned NOT NULL,
  `show_id` int(11) unsigned NOT NULL,
  `current` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`user_id`,`show_id`),
  KEY `show` (`show_id`),
  CONSTRAINT `show2` FOREIGN KEY (`show_id`) REFERENCES `shows` (`id`),
  CONSTRAINT `user2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`)
VALUES
	(1);

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
