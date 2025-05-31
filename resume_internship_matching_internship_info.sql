-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: resume_internship_matching
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `internship_info`
--

DROP TABLE IF EXISTS `internship_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internship_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(50) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `company_mail` varchar(100) NOT NULL,
  `type_of_internship` varchar(300) NOT NULL,
  `skills_required` text NOT NULL,
  `location` varchar(200) DEFAULT NULL,
  `years_of_experience` float DEFAULT NULL,
  `description_of_internship` text NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `duration` varchar(50) DEFAULT NULL,
  `expected_salary` varchar(50) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `posted_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `internship_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internship_info`
--

LOCK TABLES `internship_info` WRITE;
/*!40000 ALTER TABLE `internship_info` DISABLE KEYS */;
INSERT INTO `internship_info` VALUES (1,'Data Science Intern','Tech Innovations','hr@techinnovations.com','Remote','Python, Machine Learning, Data Science','New York, USA',1,'Work on AI models and data analytics projects.','5551234567','6','45000 USD','2025-06-01','2025-12-01','2025-03-13 18:30:00',1),(2,'Software Engineer Intern','Web Solutions','careers@websolutions.com','Onsite','Java, Spring Boot, SQL','San Francisco, USA',2,'Develop scalable backend services and REST APIs.','5559876543','3','50000 USD','2025-07-01','2025-10-01','2025-03-13 18:30:00',1),(3,'Frontend Developer Intern','Creative Web','jobs@creativeweb.com','Hybrid','JavaScript, React, Node.js','London, UK',1,'Build dynamic UI components for web applications.','5552233445','4','40000 GBP','2025-06-15','2025-10-15','2025-03-13 18:30:00',1),(4,'Cybersecurity Intern','SecureNet','security@securenet.com','Remote','Cybersecurity, Ethical Hacking, Python','Berlin, Germany',2,'Conduct security audits and penetration testing.','5553344556','5','42000 EUR','2025-05-10','2025-10-10','2025-03-13 18:30:00',6),(5,'Robotics Intern','IoT Innovations','iot@iotinnovations.com','Onsite','C++, Embedded Systems, Robotics','Tokyo, Japan',1,'Develop embedded AI for IoT devices.','5554455667','6','48000 JPY','2025-04-20','2025-10-20','2025-03-13 18:30:00',6),(6,'Software Developer Intern','TechCorp','hr@techcorp.com','Full-Time','Python, Django, SQL','Remote',1,'Develop and maintain web applications.','1234567890','6 months','5000 USD','2025-06-01','2025-12-01','2025-05-01 05:50:51',6),(7,'Software Developer Intern','TechCorp','john.doe@company.com','Full-Time','Python, Django, REST APIs','Remote',0,'Work on backend development using Python and Django.','+1-800-555-5678','3',NULL,'2025-06-01','2025-08-31','2025-05-01 10:43:02',12),(8,'Frontend Developer Intern','TechCorp','john.doe@company.com','Part-Time','HTML, CSS, JavaScript, React','Remote',0,'Build responsive web applications using React.','+1-800-555-5678','6',NULL,'2025-07-01','2025-12-31','2025-05-01 10:44:58',12);
/*!40000 ALTER TABLE `internship_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 23:26:09
