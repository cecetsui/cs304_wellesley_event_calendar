-- MySQL dump 10.13  Distrib 5.5.50, for Linux (x86_64)
--
-- Host: localhost    Database: eventscal_db
-- ------------------------------------------------------
-- Server version	5.5.50-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `spam` varchar(100) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `event_date` date NOT NULL,
  `time_start` time NOT NULL,
  `time_end` time DEFAULT NULL,
  `description` varchar(500) NOT NULL,
  `location` varchar(25) NOT NULL,
  `event_type` enum('Lecture','Meeting','Performance','Rehearsal','Workshop','Conference','Exhibit','Film Showing','Panel','Party','Recital','Seminar','Reception','Community Service','Discussion','Other') DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (2,'http://www.test.com','Jam On It','2016-11-30','19:00:00','22:00:00','Hop Hop Dance Show!','Jewettt','Performance'),(5,'','Fireside Chat','2016-12-02','13:00:00','14:00:00','Come have a fireside chat with us!','Lulu Anderson Forum','Panel'),(13,'','Rock Climbing','2016-12-02','17:00:00','00:00:00','Come climb, no experience needed!','KSC Rock Climbing walls','Other'),(15,'','WHACK Spring 2017','2017-02-13','09:00:00','00:00:00','Wellesley\'s Spring 2017 Hackathon!','Tishman Commons','Conference'),(16,'','conflict','2017-02-13','09:09:00','00:00:00','a conflict','Tishman Commons','Lecture'),(17,'','Owl walk','2016-12-02','21:00:00','23:00:00','walk to find owls','lake waban','Other'),(18,'','Independent Org Training','2016-12-07','19:00:00','20:00:00','Learn more about the resources independent orgs (formerly known as unconstituted orgs) have on campus!','Lulu 415','Workshop'),(19,'','Cocoa & Cookies Study Break','2016-12-14','15:00:00','16:00:00','Come hang out with Cabinet as we decorate cookies and enjoy some warm hot chocolate!','Lake House Living Room','Other'),(20,'','Inter-Fellowship Prayer Meeting','2016-12-08','07:30:00','08:30:00','	Inter-Fellowship Prayer Meeting','Houghton Chapel','Meeting'),(21,'','Phi Sigma Lecture','2016-12-08','18:30:00','19:30:00','Professor Irene Mata from the WGST department will be discussing the importance of Chicanx art, and its relation to Chicanx political movements. ','Pendleton East 225A Knapp','Lecture'),(22,'','Holiday Card Sale','2016-12-09','13:30:00','22:00:00','Art Club Fundraiser','4th floor vendor area','Other'),(23,'','Senate Party','2016-12-09','18:00:00','21:00:00','College Government would like to host a Senate Movie Night for the end of the Semester to celebrate the work of Senators. We will watch a movie and enjoy light snacks. ','Freeman Residence Hall TV','Party'),(24,'','CSA Chinese Table','2016-12-05','12:30:00','13:30:00','CSA Chinese Table - practice Chinese!','Severance TV Room','Other'),(25,'','Congressmen Seth Moulton and Joe Kennedy','2016-12-05','13:00:00','15:00:00','Post election reflection','Tower Court West Residenc','Lecture'),(26,'','Bushra Rehman Poetry','2016-12-05','15:00:00','17:00:00','	Bushra Rehman Poetry Event and Workshop','Wang Campus Center Cow Ch','Workshop'),(27,'','CGPC Town Hall','2016-12-05','19:30:00','21:00:00','CGPC Town Hall','Wang Campus Center Tishma','Conference'),(29,'','KSA Korean Table Lunch','2016-12-06','12:30:00','13:30:00','Speak in Korean!','Severance TV Room','Meeting'),(30,'','Culture + Mental Health Open Mic','2016-12-06','19:00:00','20:30:00','An open mic','Wang Campus Center Anders','Lecture');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `head_contacts`
--

DROP TABLE IF EXISTS `head_contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `head_contacts` (
  `bnumber` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(25) NOT NULL,
  `contact_type` enum('Student','Staff') DEFAULT NULL,
  PRIMARY KEY (`bnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `head_contacts`
--

LOCK TABLES `head_contacts` WRITE;
/*!40000 ALTER TABLE `head_contacts` DISABLE KEYS */;
INSERT INTO `head_contacts` VALUES ('2B23498','Casey Melton','casey.melton@wellesley.ed','Student'),('B10038474','Kelly Kung','kelly.kung@wellesley.edu','Student'),('B123123123','scott','scott.anderson@wellesley.','Student'),('B129837878','Rachel Seo','rachel.seo@wellesley.edu','Student'),('B20000000','Brian Tjaden','btjaden@wellesley.edu','Staff'),('B201658','Anna Page','apage@wellesley.edu','Student'),('B2039573','Hannah Oettgen','hoettge@wellesley.edu','Student'),('B20711395','Grace Hu','ghu@wellesley.edu','Student'),('B20775266','Cece Tsui','cgvp@wellesley.edu','Student'),('B20928374','Helena Yan','hyan@wellesley.edu','Student'),('B209341','Jamie','jyang6@wellesley.edu','Student'),('B230947485','Karina Lin','klin3@wellesley.edu','Student'),('B23299484','Yue Qiu','yue.qiu@wellesley.edu','Student'),('B2384729','Agnes Reiger','Agnes.reigner@wellesley.e','Student'),('B239845783','Nynika Jhaveri','njhaveri@wellesley.edu','Student'),('B29384793','Rafa Tasneem','rafa.tasneem@wellesley.ed','Student'),('B2982738','Lauren Mostrom','lmostrom@wellesley.edu','Student'),('B2983477','Ivana Castro','ivana.castro@wellesley.ed','Student'),('B3925847','Tiffany Ang','tang@wellesley.edu','Student'),('er','me','fake','Staff');
/*!40000 ALTER TABLE `head_contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orgs`
--

DROP TABLE IF EXISTS `orgs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orgs` (
  `org_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `email` varchar(25) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  `org_type` enum('Academic','Career','CGHP Affiliates','Cultural','Media & Publication','Performance & Arts','Political','Religious','Social Justice & Awareness','Societies','Sports & Teams','Volunteer') DEFAULT NULL,
  PRIMARY KEY (`org_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orgs`
--

LOCK TABLES `orgs` WRITE;
/*!40000 ALTER TABLE `orgs` DISABLE KEYS */;
INSERT INTO `orgs` VALUES (3,'FreeStyle','Hip Hop Dance Crew','freestyle@wellesley.edu','freestyle.com','Performance & Arts'),(5,'Agora Society','Our mission is to promote an intelligent interest in political questions of the day by translating thoughts into meaningful action, and providing platforms for political advocacy. In executing this mission, the sisters of Agora uphold the pillars of Sisterhood, Citizenship, Politics, and Service.','agora@wellesley.edu','theagorasociety.com','Societies'),(10,'(BC)^2','Biochemistry and Biology Club is a science organization on campus that aims to promote community between students in science classes, regardless of their major, and their fellow classmates and professors. Additionally, we host events each semester that help students navigate their college life (eg. course registration, finding research opportunities etc.) and raise awareness of how science can remain relevant after Wellesley.','','','Academic'),(14,'A.S.T.R.O. Club','Feeling real excited about Mars + stars, but have no one to talk to about it?? Join A.S.T.R.O. to watch exciting space movies, kick lip-sync butt, and go dark-sky camping!','','','Academic'),(15,'Classics Club','','','','Academic'),(16,'Club Rocks','Club Rocks is an organization for students within the Geosciences Department to make friends, share the geosciences with the wider community, and stay involved in the department. Join us!','','','Academic'),(17,'Computer Science Club','','cs-club-eboard@wellesley.','https://www.facebook.com/Wellesley-CS-Club-856871510992038/','Academic'),(18,'birding club','we watch birds','birders@wellesley.edu','','Societies'),(20,'SOAC','We oversee (1) the constituted organizations on campus, (2) the constitution process, and (3) student appointments onto faculty or administrative boards.','cgvp@wellesley.edu','sites.google.com/a/wellesley.edu/soac','CGHP Affiliates'),(21,'College Government','','cgpresident@wellesley.edu','http://wellesleycg.com','CGHP Affiliates'),(22,'Wellesley Intervarsity Christian Fellowship','Wellesley Intervarsity seeks to create a space for Christians (and non-Christians!) on campus to talk about, learn about, and worship Christ.','','','Religious'),(23,'Alpha Phi Sigma Society','Alpha Phi Sigma is the oldest society at Wellesley College. Made up of a diverse group of young women, Phi Sigma boasts members from college government, varsity athletics, Slater International, and various on and off campus organizations. Our members abide by the four pillars of the society: Lecture, Social, Sisterhood, and Passion.','','','Academic'),(24,'Art Club','Art Club is an group of students interested in any facet of the visual arts. Art Club strives to bring opportunities to create and experience art to the Wellesley student community, to provide a space for students to learn more about art and to explore their personal growth as creative individuals. Art Club organizes such events as figure drawings sessions, art-related and crafts-related workshops, trips to local art museums, to help students develop their artistic skills in a stress-free enviro','','','Performance & Arts'),(25,'Chinese Students\' Association','Wellesley Chinese Students\' Association (CSA) is a cultural group on campus which hosts many events throughout the school year to celebrate the Chinese Culture. Some of these events include the Mid-Autumn Festival, Lunar New Year Festival, and the annual CSA Culture Show. We also host social events such as a dance and our Casino night. Although our group focuses on celebrating Chinese traditions, we welcome members of all backgrounds!','','','Cultural'),(26,'Wellesley College Democrats','The Wellesley College Democrats are a political organization on campus, and a chapter of the College Democrats of Massachusetts. Our mission is to increase progressive dialogue and action at Wellesley through informational lectures, workshops, panels, and discussions, as well as through community service opportunities and direct political engagement via phone-banking, canvassing, and volunteering. The WC Dems strive to provide a safe, inclusive space where everyone can feel welcome to voice thei','','','Political'),(27,'Wellesley Association of South Asian Cultures','The purpose of WASAC is to represent and serve the interests of the South Asian and South Asian American community on campus and to promote awareness of the culture and history of South Asia. WASAC is a cultural, political, and social organization that also aims to provide a support system for students of South Asian descent.','','','Cultural'),(28,'Korean Students Association','Wellesley Korean Students Association (KSA) is an organization that seeks to cultivate and promote the culture, history and other areas of the Korean/Korean-American experience. The mission of KSA is to enrich the lives of all people, not just those of Korean descent, but for all those who are interested in Korean culture in the Wellesley College community and the greater Boston area. KSAâ€™s goal is to encourage the community to be more active by providing them with a political voice and repres','','','Cultural'),(29,'Active Minds','Active Minds works to reduce mental health stigma and raise campus awareness about mental health.','','','Social Justice & Awareness');
/*!40000 ALTER TABLE `orgs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orgs_contacts`
--

DROP TABLE IF EXISTS `orgs_contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orgs_contacts` (
  `org_id` int(11) NOT NULL,
  `bnumber` varchar(10) NOT NULL,
  `date_added` date NOT NULL,
  PRIMARY KEY (`org_id`,`bnumber`,`date_added`),
  KEY `bnumber` (`bnumber`),
  CONSTRAINT `orgs_contacts_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `orgs` (`org_id`) ON UPDATE CASCADE,
  CONSTRAINT `orgs_contacts_ibfk_2` FOREIGN KEY (`bnumber`) REFERENCES `head_contacts` (`bnumber`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orgs_contacts`
--

LOCK TABLES `orgs_contacts` WRITE;
/*!40000 ALTER TABLE `orgs_contacts` DISABLE KEYS */;
INSERT INTO `orgs_contacts` VALUES (14,'2B23498','2016-11-22'),(25,'B10038474','2016-12-08'),(18,'B123123123','2016-11-28'),(28,'B129837878','2016-12-08'),(5,'B201658','2016-11-22'),(16,'B2039573','2016-11-22'),(20,'B20775266','2016-12-08'),(21,'B20775266','2016-12-08'),(10,'B20928374','2016-11-22'),(3,'B209341','2016-11-22'),(22,'B230947485','2016-12-08'),(24,'B23299484','2016-12-08'),(29,'B2384729','2016-12-08'),(23,'B239845783','2016-12-08'),(27,'B29384793','2016-12-08'),(15,'B2982738','2016-11-22'),(26,'B2983477','2016-12-08'),(17,'B3925847','2016-11-22');
/*!40000 ALTER TABLE `orgs_contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orgs_events`
--

DROP TABLE IF EXISTS `orgs_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orgs_events` (
  `org_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`org_id`,`event_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `orgs_events_ibfk_1` FOREIGN KEY (`org_id`) REFERENCES `orgs` (`org_id`) ON UPDATE CASCADE,
  CONSTRAINT `orgs_events_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orgs_events`
--

LOCK TABLES `orgs_events` WRITE;
/*!40000 ALTER TABLE `orgs_events` DISABLE KEYS */;
INSERT INTO `orgs_events` VALUES (3,2),(5,5),(16,13),(17,15),(16,16),(18,17),(20,18),(21,19),(22,20),(23,21),(24,22),(21,23),(25,24),(26,25),(27,26),(21,27),(28,29),(29,30);
/*!40000 ALTER TABLE `orgs_events` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-08 23:55:57
