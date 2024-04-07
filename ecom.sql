-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: ecom
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `s_no` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`s_no`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  KEY `product_name` (`product_name`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `cart_ibfk_3` FOREIGN KEY (`product_name`) REFERENCES `products` (`pName`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,4,1,'iPhone 12 Pro',1),(2,5,3,'Sony PlayStation 5',1),(3,5,5,'DJI Mavic Air 2',1),(4,6,2,'Samsung Galaxy S21 Ultra',1),(5,6,4,'Apple MacBook Pro 13\"',1);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `quantity` int NOT NULL,
  `price` int NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expected_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  KEY `product_name` (`product_name`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`product_name`) REFERENCES `products` (`pName`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,4,1,'iPhone 12 Pro',2,999,'2024-04-05 09:46:24','2024-04-10'),(2,4,3,'Sony PlayStation 5',1,499,'2024-04-05 09:46:24','2024-04-12'),(3,5,2,'Samsung Galaxy S21 Ultra',1,1199,'2024-04-05 09:46:24','2024-04-15'),(4,6,4,'Apple MacBook Pro 13\"',1,1299,'2024-04-05 09:46:24','2024-04-20'),(5,6,5,'DJI Mavic Air 2',1,799,'2024-04-05 09:46:24','2024-04-25');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pName` varchar(100) NOT NULL,
  `price` int NOT NULL,
  `description` text NOT NULL,
  `quantity` int NOT NULL,
  `category` varchar(100) NOT NULL,
  `picture_url` varchar(255) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `pName` (`pName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'iPhone 12 Pro',109900,'The latest iPhone with 5G technology and A14 Bionic chip.',28,'Smartphones','https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/refurb-iphone-12-pro-graphite-2020?wid=1144&hei=1144&fmt=jpeg&qlt=90&.v=1635202842000','2024-04-05 09:46:12'),(2,'Samsung Galaxy S21 Ultra',72999,'Samsung Galaxy S21 Ultra with a powerful camera and dynamic AMOLED display.',40,'Smartphones','https://images.samsung.com/is/image/samsung/p6pim/levant/galaxy-s21/gallery/levant-galaxy-s21-ultra-5g-g988-371058-sm-g998bztgmea-368334338?$684_547_JPG$','2024-04-05 09:46:12'),(3,'Sony PlayStation 5',54999,'Next-gen gaming console with stunning graphics and lightning-fast SSD.',30,'Gaming Consoles','https://m.media-amazon.com/images/I/41BR-uI9jkL._SX300_SY300_QL70_FMwebp_.jpg','2024-04-05 09:46:12'),(4,'Apple MacBook Pro 13\"',102999,'High-performance laptop with M1 chip and Retina display.',20,'Laptops','https://www.macworld.com/wp-content/uploads/2023/12/space-black-macbook-pro-back-angle.jpg?resize=1536%2C1023&quality=50&strip=all','2024-04-05 09:46:12'),(5,'DJI Mavic Air 2',96999,'Foldable drone with 4K camera and intelligent shooting modes.',15,'Drones','https://5.imimg.com/data5/SELLER/Default/2020/9/YW/OB/QY/48277058/dji-mavic-air-2-pro-drone-camera.png','2024-04-05 09:46:12');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `user_type` enum('Admin','Cust') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (4,'test','123','saik@gmail.com','Cust'),(5,'Adolf Witler','war','HailGermany@1939.com','Cust'),(6,'Admin1','RamRam','RamisGod@earth.com','Admin'),(7,'Chitra','cool','chitteshkumar13@gmail.com','Cust');
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

-- Dump completed on 2024-04-07 19:27:33
