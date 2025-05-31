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
-- Table structure for table `resume_info`
--

DROP TABLE IF EXISTS `resume_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resume_info` (
  `name_of_applicant` varchar(50) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `linkedin_account` varchar(300) DEFAULT NULL,
  `skills` text NOT NULL,
  `education` text NOT NULL,
  `experience` text,
  `projects` text,
  `achievements` text,
  `hobbies` text,
  `resume_file` longblob,
  `user_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resume_info`
--

LOCK TABLES `resume_info` WRITE;
/*!40000 ALTER TABLE `resume_info` DISABLE KEYS */;
INSERT INTO `resume_info` VALUES ('John Doe','1234567890','john.doe@email.com','https://linkedin.com/in/johndoe','Python, Machine Learning, Data Science','B.Sc in Computer Science','2 years at XYZ Corp','AI Chatbot, Web Scraper','Best AI Project Award','Reading, Chess',_binary 'john_doe_resume.pdf',0),('Alice Smith','9876543210','alice.smith@email.com','https://linkedin.com/in/alicesmith','Java, Spring Boot, SQL','M.Sc in Software Engineering','3 years at ABC Tech','E-commerce Website, Chatbot','Top Developer Award','Painting, Hiking',_binary 'alice_smith_resume.pdf',0),('Michael Johnson','1122334455','michael.johnson@email.com','https://linkedin.com/in/michaeljohnson','JavaScript, React, Node.js','B.Tech in IT','1.5 years at Web Solutions','Portfolio Website, API Development','Employee of the Month','Gaming, Coding',_binary 'michael_johnson_resume.pdf',0),('Emily Davis','2233445566','emily.davis@email.com','https://linkedin.com/in/emilydavis','C++, Embedded Systems, Robotics','B.E in Electronics','2.5 years at IoT Innovations','Smart Home Automation, AI-driven Drone','Best Robotics Paper','Robotics, Traveling',_binary 'emily_davis_resume.pdf',0),('Robert Brown','3344556677','robert.brown@email.com','https://linkedin.com/in/robertbrown','Cybersecurity, Ethical Hacking, Python','M.Sc in Cybersecurity','4 years at SecureNet','Network Security Tool, Ethical Hacking Guide','Certified Ethical Hacker','Security Research, Blogging',_binary 'robert_brown_resume.pdf',0);
/*!40000 ALTER TABLE `resume_info` ENABLE KEYS */;
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
