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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('recruiter','intern') NOT NULL,
  `organization_name` varchar(255) DEFAULT NULL,
  `contact_details` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `website_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'B Chaitanya Reddy','bchai@gmail.com','pbkdf2:sha256:1000000$IwoXxqdu1zYIIf4P$70064a2ae7d2103e54d2957aa2d0899d547854e2e6313e5c3b648f52d83435ba','recruiter',NULL,NULL,NULL,NULL),(6,'abc','abc@gmail.com','pbkdf2:sha256:1000000$5spHg9C2M6oBOLJ2$05bb400421a6b5688a9281addbcef96479a8ca79bb20ca849de1b472a616bfab','recruiter',NULL,NULL,NULL,NULL),(10,'abc','def@gmail.com','pbkdf2:sha256:1000000$eMbeIagjigPKOqAC$b6cbc477d0069b53a09a893c498d5be05e50a18351dd319ebd9f40c55e7ff4f6','intern',NULL,NULL,NULL,NULL),(11,'John Doe','john.doe@email.com','pbkdf2:sha256:1000000$sh6a4Yxb4DDUQ9MO$10755d88a3a30ef0d77dcdb53997a73b863c8f76f2133f6a32a359e1ae23457f','intern',NULL,NULL,NULL,NULL),(12,'John Doe','john.doe@company.com','pbkdf2:sha256:1000000$uBZdoWuUL8eAnEDr$961b25cf97f37bcd33224a75fd53e3773970ba649e671c22ad1fef2a6e16832f','recruiter','TechCorp','+1-800-555-1234','San Francisco, CA','https://www.techcorp.com'),(13,'Jane Smith','jane.smith@gmail.com','pbkdf2:sha256:1000000$17VAt8BB2IpEntKf$37fd999fdf86dc8d002725aaed06cead50046f7667cf4d84cee78dbfa7a361d9','intern','','','',''),(14,'B Chaitanya Reddy','bchaitanyareddy902@gmail.com','pbkdf2:sha256:1000000$qHYm9jyDvaqpc5d6$d40a49464a6366af81b8792c95b01e84fb5b6e5c3579ab2d1c4d068e4148f915','intern','','','','');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 23:26:10
