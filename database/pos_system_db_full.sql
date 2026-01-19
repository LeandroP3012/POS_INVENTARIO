CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `units`
--

DROP TABLE IF EXISTS `units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `units` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `symbol` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` enum('weight','length','volume','unit','other') COLLATE utf8mb4_unicode_ci DEFAULT 'unit',
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_symbol` (`symbol`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units`
--

LOCK TABLES `units` WRITE;
/*!40000 ALTER TABLE `units` DISABLE KEYS */;
INSERT INTO `units` VALUES (1,'Unidad','un','unit','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(2,'Kilogramo','kg','weight','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(3,'Gramo','g','weight','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(4,'Litro','L','volume','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(5,'Mililitro','ml','volume','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(6,'Metro','m','length','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(7,'Centímetro','cm','length','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(8,'Paquete','paq','unit','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(9,'Caja','cja','unit','active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(10,'Docena','doc','unit','active','2025-10-08 12:38:19','2025-10-08 12:38:19');
/*!40000 ALTER TABLE `units` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `parent_id` int DEFAULT NULL,
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_parent` (`parent_id`),
  CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'General','Categoría general para productos sin clasificación específica',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(2,'Electrónica','Productos electrónicos y tecnología',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(3,'Alimentos','Productos alimenticios y bebidas',NULL,'inactive','2025-10-08 12:38:19','2025-10-11 17:49:55'),(4,'Ropa','Ropa y accesorios',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(5,'Hogar','Artículos para el hogar',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(6,'Oficina','Artículos de oficina y papelería',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(7,'Salud','Productos de salud y cuidado personal',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(8,'Deportes','Artículos deportivos y fitness',NULL,'active','2025-10-08 12:38:19','2025-10-08 12:38:19'),(9,'Tecnologia','Para Pc',NULL,'active','2025-10-11 17:42:36','2025-10-11 17:42:36'),(10,'Comida','',NULL,'active','2025-10-12 01:03:11','2025-10-12 01:03:11');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `category_id` int NOT NULL,
  `unit_id` int NOT NULL DEFAULT '1',
  `barcode` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `cost` decimal(10,2) NOT NULL DEFAULT '0.00',
  `stock_quantity` decimal(10,2) NOT NULL DEFAULT '0.00',
  `min_stock` decimal(10,2) NOT NULL DEFAULT '0.00',
  `max_stock` decimal(10,2) NOT NULL DEFAULT '0.00',
  `tax_rate` decimal(5,2) NOT NULL DEFAULT '0.00',
  `image_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `created_by` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sku` (`sku`),
  KEY `idx_name` (`name`),
  KEY `idx_category` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_stock` (`stock_quantity`),
  KEY `idx_barcode` (`barcode`),
  KEY `unit_id` (`unit_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`unit_id`) REFERENCES `units` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'PROD-001','Laptop Dell Inspiron 15','Laptop Dell Inspiron 15 - Intel Core i5, 8GB RAM, 256GB SSD',2,1,NULL,799.99,650.00,1.00,2.00,20.00,16.00,NULL,'active',1,'2025-10-08 12:38:19','2025-10-26 02:40:19'),(2,'PROD-002','Mouse Inalámbrico Logitech','Mouse inalámbrico Logitech M185 - Sensor óptico, batería incluida',2,1,NULL,24.99,15.00,3.00,5.00,50.00,16.00,NULL,'active',1,'2025-10-08 12:38:19','2025-11-02 06:07:38'),(3,'PROD-000006','Cuaderno Universitario 100 hojas','Cuaderno universitario de 100 hojas, tapa dura',6,1,'7750000000069',0.00,0.00,0.00,0.00,0.00,0.00,NULL,'active',1,'2025-10-08 12:38:19','2025-11-01 04:43:27'),(4,'PROD-004','Agua Mineral 500ml','Agua mineral natural embotellada 500ml',3,5,NULL,0.75,0.40,177.00,50.00,500.00,0.00,NULL,'active',1,'2025-10-08 12:38:19','2025-11-02 22:01:10'),(5,'PROD-005','Teclado Mecánico RGB','Teclado mecánico retroiluminado RGB, switches azules',2,1,NULL,89.99,55.00,1.00,3.00,30.00,16.00,NULL,'active',1,'2025-10-08 12:38:19','2025-10-30 02:18:03'),(6,'PROD-000005','Guantes de Box','',8,1,'7750000000052',0.00,0.00,0.00,0.00,0.00,0.00,NULL,'active',1,'2025-10-11 23:47:44','2025-11-01 04:41:54'),(7,'PROD-000002','Trapeador','Se usa para secar',5,1,'7750000000021',15.00,5.00,1.00,5.00,10.00,0.00,NULL,'active',1,'2025-10-11 23:59:50','2025-10-21 06:09:02'),(8,'PROD-000003','Carro','',5,1,'7750000000038',1500.00,1000.00,1.00,0.00,0.00,0.00,NULL,'active',1,'2025-10-12 01:02:31','2025-11-01 02:44:27'),(9,'PROD-000004','Audifonos Redmi Negro','Audifonos con 500w de bateria',1,1,'7750000000045',0.00,0.00,0.00,0.00,0.00,18.00,NULL,'active',1,'2025-10-31 18:40:30','2025-11-01 03:08:01');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `document_type` enum('dni','ruc','passport','other') COLLATE utf8mb4_unicode_ci DEFAULT 'dni',
  `document_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'Perú',
  `tax_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'RUC para facturas',
  `customer_type` enum('retail','wholesale','corporate') COLLATE utf8mb4_unicode_ci DEFAULT 'retail',
  `credit_limit` decimal(10,2) DEFAULT '0.00',
  `status` enum('active','inactive') COLLATE utf8mb4_unicode_ci DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_document` (`document_number`),
  KEY `idx_status` (`status`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'GENERIC','Cliente Genérico','other','00000000',NULL,NULL,NULL,NULL,'Perú',NULL,'retail',0.00,'active','2025-10-18 19:38:46','2025-10-18 19:38:46',NULL);
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_person` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'Perú',
  `tax_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'RUC o documento tributario',
  `payment_terms` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Condiciones de pago',
  `credit_limit` decimal(12,2) DEFAULT '0.00',
  `active` tinyint(1) DEFAULT '1',
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_code` (`code`),
  KEY `idx_name` (`name`),
  KEY `idx_active` (`active`),
  KEY `idx_tax_id` (`tax_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `suppliers_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Proveedores';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'PROV001','Proveedor General','Contacto General','(01) 000-0000','contacto@proveedor.com',NULL,NULL,'Perú',NULL,NULL,0.00,1,NULL,'2025-09-29 05:42:46','2025-09-29 05:42:46',1);
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_type` enum('admin','supervisor','manager','employee','cashier','user') COLLATE utf8mb4_unicode_ci DEFAULT 'user',
  `role_id` int DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  `avatar_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `preferences` json DEFAULT NULL COMMENT 'Preferencias personales del usuario',
  `permissions` json DEFAULT NULL COMMENT 'Permisos específicos del usuario',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL,
  `failed_attempts` int DEFAULT '0',
  `locked_until` timestamp NULL DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci COMMENT 'Notas administrativas',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_username` (`username`),
  KEY `idx_email` (`email`),
  KEY `idx_user_type` (`user_type`),
  KEY `idx_active` (`active`),
  KEY `idx_last_login` (`last_login`),
  KEY `created_by` (`created_by`),
  KEY `idx_role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Usuarios del sistema';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','admin@sistema-pos.com','Administrador del Sistema',NULL,'admin',2,1,NULL,NULL,'{\"all_modules\": true, \"super_admin\": true}','2025-09-29 05:42:46','2025-11-02 22:00:33','2025-11-02 22:00:33',0,NULL,NULL,NULL),(2,'cajero1','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','cajero@sistema-pos.com','Cajero Principal',NULL,'cashier',5,1,NULL,NULL,'{\"ventas\": [\"ver\", \"crear\"], \"productos\": [\"ver\"]}','2025-09-29 05:42:46','2025-09-30 19:23:53','2025-09-29 22:28:31',0,NULL,NULL,NULL),(5,'test','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','postest@gmail.com','test020808','','cashier',5,1,'',NULL,NULL,'2025-10-01 02:50:16','2025-10-01 03:10:03','2025-10-01 03:10:03',0,NULL,NULL,NULL),(6,'lpando','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','lpando@lancaster.com.pe','lpando','','employee',6,1,'',NULL,NULL,'2025-10-04 06:13:02','2025-10-04 06:13:02',NULL,0,NULL,NULL,NULL),(7,'lpandov1','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','lpandov1@gmail.com','lpandov1','','employee',7,1,'',NULL,NULL,'2025-10-04 06:21:17','2025-10-04 06:22:37','2025-10-04 06:22:37',0,NULL,NULL,NULL),(8,'lpandov2','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','lpandov2@gmail.com','lpandov2','','user',8,1,'',NULL,NULL,'2025-10-04 06:34:05','2025-10-04 07:24:44','2025-10-04 07:24:44',0,NULL,NULL,NULL),(9,'testv2','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','testv2@lancaster.com.pe','testv2','','user',8,1,'',NULL,NULL,'2025-10-07 06:05:02','2025-10-07 06:05:15','2025-10-07 06:05:15',0,NULL,NULL,NULL),(10,'testv3','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','testv3@gmail.com','Es un test','','user',8,1,'',NULL,NULL,'2025-10-12 00:55:22','2025-10-29 21:25:10','2025-10-29 21:25:10',0,NULL,NULL,NULL),(11,'Davicito','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','sas@gmail.com','Divic','','user',10,1,'',NULL,NULL,'2025-10-19 21:16:42','2025-10-19 21:16:57','2025-10-19 21:16:57',0,NULL,NULL,NULL),(12,'testv4','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','testv4@gmail.com','testv4','','user',11,1,'',NULL,NULL,'2025-10-28 04:44:09','2025-11-02 04:16:26','2025-10-29 21:43:20',0,NULL,NULL,NULL),(13,'prueba_permisos','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','prueba@pos.com','Prueba Permisos',NULL,'employee',12,1,NULL,NULL,NULL,'2025-10-28 11:47:43','2025-10-28 11:48:37','2025-10-28 11:48:37',0,NULL,NULL,NULL),(14,'testv5','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','testv5@gmail.com','testv5','','user',12,1,'',NULL,NULL,'2025-10-29 21:40:34','2025-10-30 04:58:36','2025-10-30 04:58:36',0,NULL,NULL,NULL),(15,'testv6','15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225','testv6@gmail.com','testv6','','user',6,1,'',NULL,NULL,'2025-10-29 22:51:10','2025-11-02 06:14:31','2025-11-02 06:14:31',0,NULL,NULL,NULL),(16,'testv7','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','mathias123@gmail.com','Mathias Daniel','','user',6,1,'',NULL,NULL,'2025-10-31 17:36:10','2025-10-31 17:44:23','2025-10-31 17:40:47',0,NULL,NULL,NULL);
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

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `permissions` json DEFAULT NULL COMMENT 'Permisos del rol en formato JSON',
  `system_role` tinyint(1) DEFAULT '0' COMMENT 'Roles del sistema (protegidos)',
  `active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `idx_name` (`name`),
  KEY `idx_code` (`code`),
  KEY `idx_active` (`active`),
  KEY `idx_system_role` (`system_role`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `roles_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Roles del sistema con permisos personalizables';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Super Admin','super_admin','Acceso completo al sistema, puede gestionar todo','[\"*\"]',1,1,'2025-09-30 19:23:52','2025-09-30 19:23:52',NULL),(2,'Administrador','admin','Administrador del sistema con acceso a la mayoría de funciones','[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\", \"roles.view\", \"roles.create\", \"roles.edit\", \"roles.delete\", \"system.config\", \"system.backup\", \"system.reports\", \"inventory.view\", \"inventory.create\", \"inventory.edit\", \"inventory.delete\", \"inventory.reports\", \"inventory.export\", \"sales.view\", \"sales.create\", \"sales.edit\", \"sales.reports\", \"sales.export\", \"dashboard.view\", \"dashboard.stats\", \"reports.sales\", \"reports.inventory\", \"reports.users\"]',1,1,'2025-09-30 19:23:52','2025-10-28 11:40:56',NULL),(3,'Gerente','manager','Gerente de tienda con acceso a reportes y supervisión','[\"users.view\", \"inventory.view\", \"inventory.reports\", \"inventory.export\", \"sales.view\", \"sales.create\", \"sales.reports\", \"sales.export\", \"dashboard.view\", \"dashboard.stats\", \"reports.sales\", \"reports.inventory\"]',1,1,'2025-09-30 19:23:52','2025-10-28 11:40:56',NULL),(4,'Empleado','employee','Empleado con acceso básico para ventas','[\"sales.view\", \"sales.create\", \"inventory.view\", \"dashboard.view\"]',1,1,'2025-09-30 19:23:52','2025-10-28 11:40:56',NULL),(5,'Cajero','cashier','Cajero con acceso solo a ventas y caja','[\"sales.create\", \"sales.view_own\", \"cash.register\", \"dashboard.view\"]',1,1,'2025-09-30 19:23:52','2025-10-28 11:40:56',NULL),(6,'Test01','esuntest','EsunTest123','[\"reports.basic\", \"reports.full\"]',0,1,'2025-10-01 05:31:36','2025-11-02 06:13:40',NULL),(7,'ModoEsclavo','esunrolpersonalizado','EsUnRolPersonalizado','[\"inventory.edit\", \"inventory.delete\", \"inventory.stock\"]',0,1,'2025-10-04 06:20:15','2025-10-19 20:54:14',NULL),(8,'ModoEsclavoV1','modoesclavov1','ModoEsclavoV1','[\"users.view\", \"roles.view\", \"system.config\", \"dashboard.view\"]',0,1,'2025-10-04 06:33:21','2025-10-28 22:32:15',NULL),(9,'Test02','esuntest02','','[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"inventory.view\"]',0,1,'2025-10-12 00:56:32','2025-10-29 22:52:03',NULL),(10,'Davicito','123','123','[\"users.view\", \"roles.view\", \"dashboard.view\", \"inventory.view\", \"sales.view\", \"cash.register\", \"products.view\", \"customers.view\"]',0,1,'2025-10-19 21:15:13','2025-10-19 21:15:53',NULL),(11,'Test03','test03','','[\"users.view\", \"users.create\"]',0,1,'2025-10-28 04:42:51','2025-10-30 04:58:19',NULL),(12,'Gerente de Personal','gerente_personal','Rol de prueba para validar permisos - Puede ver y editar usuarios, cambiar estados','[\"roles.view\", \"inventory.view\"]',0,1,'2025-10-28 11:43:52','2025-10-31 05:34:29',NULL);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `inventory_movements`
--

DROP TABLE IF EXISTS `inventory_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_movements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `movement_type` enum('sale','purchase','adjustment','return','transfer') COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(10,2) NOT NULL COMMENT 'Positivo=entrada, Negativo=salida',
  `previous_stock` decimal(10,2) NOT NULL,
  `new_stock` decimal(10,2) NOT NULL,
  `reference_type` enum('sale','purchase','manual','other') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reference_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_product` (`product_id`),
  KEY `idx_type` (`movement_type`),
  KEY `idx_reference` (`reference_type`,`reference_id`),
  KEY `idx_date` (`created_at`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `inventory_movements_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `inventory_movements_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_movements`
--

LOCK TABLES `inventory_movements` WRITE;
/*!40000 ALTER TABLE `inventory_movements` DISABLE KEYS */;
INSERT INTO `inventory_movements` VALUES (1,4,'sale',-4.00,196.00,192.00,'sale',1,1,'Venta VTA-2025-00001','2025-10-21 04:36:09'),(2,3,'sale',-1.00,49.00,48.00,'sale',2,1,'Venta VTA-2025-00002','2025-10-21 05:02:57'),(3,1,'sale',-2.00,3.00,1.00,'sale',2,1,'Venta VTA-2025-00002','2025-10-21 05:02:57'),(4,7,'sale',-1.00,5.00,4.00,'sale',2,1,'Venta VTA-2025-00002','2025-10-21 05:02:57'),(5,2,'sale',-1.00,14.00,13.00,'sale',3,1,'Venta VTA-2025-00003','2025-10-21 05:47:36'),(6,7,'sale',-1.00,4.00,3.00,'sale',4,1,'Venta VTA-2025-00004','2025-10-21 05:56:41'),(7,7,'sale',-1.00,3.00,2.00,'sale',5,1,'Venta VTA-2025-00005','2025-10-21 05:56:54'),(8,2,'sale',-1.00,13.00,12.00,'sale',6,1,'Venta VTA-2025-00006','2025-10-21 06:02:14'),(9,2,'sale',-1.00,12.00,11.00,'sale',7,1,'Venta VTA-2025-00007','2025-10-21 06:03:52'),(10,7,'sale',-1.00,2.00,1.00,'sale',8,1,'Venta VTA-2025-00008','2025-10-21 06:04:13'),(11,7,'sale',-1.00,1.00,0.00,'sale',9,1,'Venta VTA-2025-00009','2025-10-21 06:09:02'),(12,3,'sale',-1.00,48.00,47.00,'sale',10,1,'Venta VTA-2025-00010','2025-10-21 06:11:50'),(13,3,'sale',-1.00,47.00,46.00,'sale',11,1,'Venta VTA-2025-00011','2025-10-21 06:12:32'),(14,2,'sale',-1.00,11.00,10.00,'sale',11,1,'Venta VTA-2025-00011','2025-10-21 06:12:32'),(15,6,'sale',-1.00,24.00,23.00,'sale',12,1,'Venta VTA-2025-00012','2025-10-25 22:43:53'),(16,2,'sale',-1.00,10.00,9.00,'sale',12,1,'Venta VTA-2025-00012','2025-10-25 22:43:53'),(17,3,'sale',-1.00,46.00,45.00,'sale',13,1,'Venta VTA-2025-00013','2025-10-26 00:05:50'),(18,8,'sale',-1.00,2.00,1.00,'sale',14,1,'Venta VTA-2025-00014','2025-10-26 01:50:44'),(19,8,'sale',-1.00,1.00,0.00,'sale',15,1,'Venta VTA-2025-00015','2025-10-26 02:03:50'),(20,8,'sale',-1.00,0.00,-1.00,'sale',16,1,'Venta VTA-2025-00016','2025-10-26 02:12:42'),(21,8,'sale',-1.00,-1.00,-2.00,'sale',17,1,'Venta VTA-2025-00017','2025-10-26 02:12:57'),(22,5,'sale',-1.00,7.00,6.00,'sale',18,1,'Venta VTA-2025-00018','2025-10-26 02:14:01'),(23,5,'sale',-1.00,6.00,5.00,'sale',19,1,'Venta VTA-2025-00019','2025-10-26 02:19:08'),(24,6,'sale',-1.00,23.00,22.00,'sale',20,1,'Venta VTA-2025-00020','2025-10-26 02:26:56'),(25,1,'sale',-1.00,2.00,1.00,'sale',21,1,'Venta VTA-2025-00021','2025-10-26 02:27:32'),(26,5,'sale',-1.00,5.00,4.00,'sale',22,1,'Venta VTA-2025-00022','2025-10-26 02:32:48'),(27,6,'sale',-1.00,22.00,21.00,'sale',23,1,'Venta VTA-2025-00023','2025-10-26 02:35:14'),(28,1,'sale',-1.00,1.00,0.00,'sale',24,1,'Venta VTA-2025-00024','2025-10-26 02:40:19'),(29,2,'sale',-2.00,8.00,6.00,'sale',25,1,'Venta VTA-2025-00025','2025-10-26 02:49:22'),(30,2,'sale',-1.00,7.00,6.00,'sale',26,1,'Venta VTA-2025-00026','2025-10-26 02:49:56'),(31,5,'sale',-1.00,4.00,3.00,'sale',27,1,'Venta VTA-2025-00027','2025-10-26 02:51:52'),(32,2,'sale',-1.00,6.00,5.00,'sale',28,1,'Venta VTA-2025-00028','2025-10-26 02:54:07'),(33,2,'sale',-1.00,5.00,4.00,'sale',29,1,'Venta VTA-2025-00029','2025-10-26 02:57:41'),(34,2,'sale',-1.00,4.00,3.00,'sale',30,1,'Venta VTA-2025-00030','2025-10-26 03:11:09'),(35,6,'sale',-1.00,21.00,20.00,'sale',31,1,'Venta VTA-2025-00031','2025-10-26 03:14:42'),(36,6,'sale',-1.00,20.00,19.00,'sale',32,1,'Venta VTA-2025-00032','2025-10-26 03:15:38'),(37,5,'sale',-1.00,3.00,2.00,'sale',33,1,'Venta VTA-2025-00033','2025-10-26 05:06:15'),(38,3,'sale',-1.00,45.00,44.00,'sale',34,1,'Venta VTA-2025-00034','2025-10-26 05:27:05'),(39,3,'sale',-12.00,33.00,21.00,'sale',36,1,'Venta VTA-2025-00035','2025-10-26 06:02:24'),(40,6,'sale',-2.00,18.00,16.00,'sale',37,1,'Venta VTA-2025-00036','2025-10-26 06:05:16'),(41,4,'sale',-5.00,191.00,186.00,'sale',38,1,'Venta VTA-2025-00037','2025-10-26 06:21:38'),(42,4,'sale',-1.00,190.00,189.00,'sale',39,1,'Venta VTA-2025-00038','2025-10-28 14:09:12'),(43,6,'sale',-1.00,17.00,16.00,'sale',39,1,'Venta VTA-2025-00038','2025-10-28 14:09:12'),(44,6,'sale',-1.00,16.00,15.00,'sale',40,1,'Venta VTA-2025-00039','2025-10-29 00:43:52'),(45,5,'sale',-1.00,2.00,1.00,'sale',40,1,'Venta VTA-2025-00039','2025-10-29 00:43:52'),(46,5,'sale',-1.00,1.00,0.00,'sale',41,1,'Venta VTA-2025-00040','2025-10-30 02:18:03'),(47,4,'sale',-4.00,186.00,182.00,'sale',42,1,'Venta VTA-2025-00041','2025-10-31 18:11:48'),(48,3,'sale',-2.00,31.00,29.00,'sale',43,1,'Venta VTA-2025-00042','2025-10-31 18:34:39'),(49,8,'sale',-1.00,3.00,2.00,'sale',44,1,'Venta VTA-2025-00043','2025-11-01 02:43:18'),(50,8,'sale',-1.00,2.00,1.00,'sale',45,1,'Venta VTA-2025-00044','2025-11-01 02:43:50'),(51,8,'sale',-1.00,1.00,0.00,'sale',46,1,'Venta VTA-2025-00045','2025-11-01 02:44:27'),(52,4,'sale',-5.00,181.00,176.00,'sale',47,1,'Venta VTA-2025-00046','2025-11-02 05:22:08'),(53,2,'sale',-1.00,3.00,2.00,'sale',48,1,'Venta VTA-2025-00047','2025-11-02 06:07:38'),(54,4,'sale',-1.00,180.00,179.00,'sale',49,1,'Venta VTA-2025-00048','2025-11-02 21:50:33'),(55,4,'sale',-1.00,179.00,178.00,'sale',50,1,'Venta VTA-2025-00049','2025-11-02 21:53:15'),(56,4,'sale',-1.00,178.00,177.00,'sale',51,1,'Venta VTA-2025-00050','2025-11-02 21:53:37'),(57,4,'sale',-1.00,177.00,176.00,'sale',52,1,'Venta VTA-2025-00051','2025-11-02 22:01:10');
/*!40000 ALTER TABLE `inventory_movements` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:05


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `product_movements`
--

DROP TABLE IF EXISTS `product_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_movements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `movement_type` enum('purchase','sale','adjustment','return','transfer') COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `previous_stock` decimal(10,2) NOT NULL,
  `new_stock` decimal(10,2) NOT NULL,
  `reference_id` int DEFAULT NULL COMMENT 'ID de referencia (venta, compra, etc)',
  `reference_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Tipo de referencia',
  `notes` text COLLATE utf8mb4_unicode_ci,
  `created_by` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_product` (`product_id`),
  KEY `idx_type` (`movement_type`),
  KEY `idx_date` (`created_at`),
  KEY `idx_reference` (`reference_type`,`reference_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `product_movements_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_movements_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_movements`
--

LOCK TABLES `product_movements` WRITE;
/*!40000 ALTER TABLE `product_movements` DISABLE KEYS */;
INSERT INTO `product_movements` VALUES (1,6,'purchase',15.00,10.00,25.00,NULL,NULL,'Entrada de stock: +15.0',1,'2025-10-12 00:36:26'),(2,7,'purchase',5.00,0.00,5.00,NULL,NULL,'Entrada de stock: +5.0',1,'2025-10-12 00:36:53'),(3,7,'purchase',1.00,5.00,6.00,NULL,NULL,'Entrada de stock: +1.0',1,'2025-10-12 00:37:02'),(4,8,'purchase',1.00,0.00,1.00,NULL,NULL,'Entrada de stock: +1.0',1,'2025-10-12 01:05:10'),(5,8,'purchase',5.00,1.00,6.00,NULL,NULL,'Entrada de stock: +5.0',1,'2025-10-12 01:05:25'),(6,8,'purchase',2.00,6.00,8.00,NULL,NULL,'Entrada de stock: +2.0',1,'2025-10-12 01:05:41'),(7,8,'purchase',2.00,8.00,10.00,NULL,NULL,'Entrada de stock: +2.0',1,'2025-10-18 17:29:22'),(8,8,'sale',-6.00,10.00,4.00,NULL,NULL,'Salida de stock: -6.0',1,'2025-10-18 17:33:45'),(9,8,'adjustment',1.00,4.00,5.00,NULL,NULL,'Ajuste manual: 4.0 → 5.0',1,'2025-10-18 17:34:03');
/*!40000 ALTER TABLE `product_movements` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sale_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'VTA-2025-00001',
  `user_id` int NOT NULL COMMENT 'Cajero',
  `customer_id` int DEFAULT NULL COMMENT 'Cliente (NULL = genérico)',
  `subtotal` decimal(10,2) NOT NULL,
  `tax_rate` decimal(5,2) DEFAULT '18.00',
  `tax_amount` decimal(10,2) NOT NULL,
  `discount_amount` decimal(10,2) DEFAULT '0.00',
  `total_amount` decimal(10,2) NOT NULL,
  `payment_method` enum('cash','card','transfer','multiple') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'cash',
  `paid_amount` decimal(10,2) NOT NULL,
  `change_amount` decimal(10,2) DEFAULT '0.00',
  `status` enum('completed','cancelled','pending','refunded') COLLATE utf8mb4_unicode_ci DEFAULT 'completed',
  `notes` text COLLATE utf8mb4_unicode_ci,
  `sale_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cancelled_at` timestamp NULL DEFAULT NULL,
  `cancelled_by` int DEFAULT NULL,
  `cancellation_reason` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sale_number` (`sale_number`),
  KEY `idx_sale_number` (`sale_number`),
  KEY `idx_sale_date` (`sale_date`),
  KEY `idx_user` (`user_id`),
  KEY `idx_customer` (`customer_id`),
  KEY `idx_status` (`status`),
  KEY `cancelled_by` (`cancelled_by`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL,
  CONSTRAINT `sales_ibfk_3` FOREIGN KEY (`cancelled_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,'VTA-2025-00001',1,1,3.00,18.00,0.54,0.00,3.54,'cash',20.00,16.46,'completed','','2025-10-21 04:36:09','2025-10-21 04:36:09','2025-10-21 04:36:09',NULL,NULL,NULL),(2,'VTA-2025-00002',1,1,1618.48,18.00,291.33,0.00,1909.81,'cash',1620.00,1.52,'completed','','2025-10-21 05:02:57','2025-10-21 05:02:57','2025-10-21 05:02:57',NULL,NULL,NULL),(3,'VTA-2025-00003',1,1,24.99,18.00,4.50,0.00,29.49,'cash',25.00,0.01,'completed','','2025-10-21 05:47:36','2025-10-21 05:47:36','2025-10-21 05:47:36',NULL,NULL,NULL),(4,'VTA-2025-00004',1,1,15.00,18.00,2.70,0.00,17.70,'cash',15.00,0.00,'completed','','2025-10-21 05:56:41','2025-10-21 05:56:41','2025-10-21 05:56:41',NULL,NULL,NULL),(5,'VTA-2025-00005',1,1,15.00,18.00,2.70,0.00,17.70,'cash',16.00,1.00,'completed','','2025-10-21 05:56:54','2025-10-21 05:56:54','2025-10-21 05:56:54',NULL,NULL,NULL),(6,'VTA-2025-00006',1,1,24.99,18.00,4.50,0.00,29.49,'cash',25.00,0.01,'completed','','2025-10-21 06:02:14','2025-10-21 06:02:14','2025-10-21 06:02:14',NULL,NULL,NULL),(7,'VTA-2025-00007',1,1,24.99,18.00,4.50,0.00,29.49,'cash',25.00,0.01,'completed','','2025-10-21 06:03:52','2025-10-21 06:03:52','2025-10-21 06:03:52',NULL,NULL,NULL),(8,'VTA-2025-00008',1,1,15.00,18.00,2.70,0.00,17.70,'cash',15.00,0.00,'completed','','2025-10-21 06:04:13','2025-10-21 06:04:13','2025-10-21 06:04:13',NULL,NULL,NULL),(9,'VTA-2025-00009',1,1,15.00,18.00,2.70,0.00,17.70,'cash',15.00,0.00,'completed','','2025-10-21 06:09:02','2025-10-21 06:09:02','2025-10-21 06:09:02',NULL,NULL,NULL),(10,'VTA-2025-00010',1,1,3.50,18.00,0.63,0.00,4.13,'cash',3.50,0.00,'completed','','2025-10-21 06:11:50','2025-10-21 06:11:50','2025-10-21 06:11:50',NULL,NULL,NULL),(11,'VTA-2025-00011',1,1,28.49,18.00,5.13,0.00,33.62,'cash',30.00,1.51,'completed','','2025-10-21 06:12:32','2025-10-21 06:12:32','2025-10-21 06:12:32',NULL,NULL,NULL),(12,'VTA-2025-00012',1,1,74.99,18.00,13.50,0.00,88.49,'cash',75.00,0.01,'completed','','2025-10-25 22:43:53','2025-10-25 22:43:53','2025-10-25 22:43:53',NULL,NULL,NULL),(13,'VTA-2025-00013',1,1,3.50,18.00,0.63,0.00,4.13,'cash',4.00,0.50,'completed','','2025-10-26 00:05:50','2025-10-26 00:05:50','2025-10-26 00:05:50',NULL,NULL,NULL),(14,'VTA-2025-00014',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1520.00,20.00,'completed','','2025-10-26 01:50:44','2025-10-26 01:50:44','2025-10-26 01:50:44',NULL,NULL,NULL),(15,'VTA-2025-00015',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1500.00,0.00,'completed','','2025-10-26 02:03:50','2025-10-26 02:03:50','2025-10-26 02:03:50',NULL,NULL,NULL),(16,'VTA-2025-00016',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1500.00,0.00,'completed','','2025-10-26 02:12:42','2025-10-26 02:12:42','2025-10-26 02:12:42',NULL,NULL,NULL),(17,'VTA-2025-00017',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1500.00,0.00,'completed','','2025-10-26 02:12:57','2025-10-26 02:12:57','2025-10-26 02:12:57',NULL,NULL,NULL),(18,'VTA-2025-00018',1,1,89.99,18.00,16.20,0.00,106.19,'cash',110.00,3.81,'completed','','2025-10-26 02:14:01','2025-10-26 02:14:01','2025-10-26 02:14:01',NULL,NULL,NULL),(19,'VTA-2025-00019',1,1,89.99,18.00,16.20,0.00,106.19,'cash',110.00,3.81,'completed','','2025-10-26 02:19:08','2025-10-26 02:19:08','2025-10-26 02:19:08',NULL,NULL,NULL),(20,'VTA-2025-00020',1,1,50.00,18.00,9.00,0.00,59.00,'cash',50.00,0.00,'completed','','2025-10-26 02:26:56','2025-10-26 02:26:56','2025-10-26 02:26:56',NULL,NULL,NULL),(21,'VTA-2025-00021',1,1,799.99,18.00,144.00,0.00,943.99,'cash',800.00,0.01,'completed','','2025-10-26 02:27:32','2025-10-26 02:27:32','2025-10-26 02:27:32',NULL,NULL,NULL),(22,'VTA-2025-00022',1,1,89.99,18.00,16.20,0.00,106.19,'cash',90.00,0.01,'completed','','2025-10-26 02:32:48','2025-10-26 02:32:48','2025-10-26 02:32:48',NULL,NULL,NULL),(23,'VTA-2025-00023',1,1,50.00,18.00,9.00,0.00,59.00,'cash',60.00,1.00,'completed','','2025-10-26 02:35:14','2025-10-26 02:35:14','2025-10-26 02:35:14',NULL,NULL,NULL),(24,'VTA-2025-00024',1,1,799.99,18.00,144.00,0.00,943.99,'cash',800.00,0.01,'completed','','2025-10-26 02:40:19','2025-10-26 02:40:19','2025-10-26 02:40:19',NULL,NULL,NULL),(25,'VTA-2025-00025',1,1,49.98,18.00,9.00,0.00,58.98,'cash',50.00,0.02,'completed','','2025-10-26 02:49:22','2025-10-26 02:49:22','2025-10-26 02:49:22',NULL,NULL,NULL),(26,'VTA-2025-00026',1,1,24.99,18.00,4.50,0.00,29.49,'cash',50.00,25.01,'completed','','2025-10-26 02:49:56','2025-10-26 02:49:56','2025-10-26 02:49:56',NULL,NULL,NULL),(27,'VTA-2025-00027',1,1,89.99,18.00,16.20,0.00,106.19,'cash',90.00,0.01,'completed','','2025-10-26 02:51:52','2025-10-26 02:51:52','2025-10-26 02:51:52',NULL,NULL,NULL),(28,'VTA-2025-00028',1,1,24.99,18.00,4.50,0.00,29.49,'cash',25.00,0.01,'completed','','2025-10-26 02:54:07','2025-10-26 02:54:07','2025-10-26 02:54:07',NULL,NULL,NULL),(29,'VTA-2025-00029',1,1,24.99,18.00,4.50,0.00,29.49,'cash',30.00,0.51,'completed','','2025-10-26 02:57:41','2025-10-26 02:57:41','2025-10-26 02:57:41',NULL,NULL,NULL),(30,'VTA-2025-00030',1,1,24.99,18.00,4.50,0.00,29.49,'cash',30.00,0.51,'completed','','2025-10-26 03:11:09','2025-10-26 03:11:09','2025-10-26 03:11:09',NULL,NULL,NULL),(31,'VTA-2025-00031',1,1,50.00,18.00,9.00,0.00,59.00,'cash',50.00,0.00,'completed','','2025-10-26 03:14:42','2025-10-26 03:14:42','2025-10-26 03:14:42',NULL,NULL,NULL),(32,'VTA-2025-00032',1,1,50.00,18.00,9.00,0.00,59.00,'cash',50.00,0.00,'completed','','2025-10-26 03:15:38','2025-10-26 03:15:38','2025-10-26 03:15:38',NULL,NULL,NULL),(33,'VTA-2025-00033',1,1,89.99,18.00,16.20,0.00,106.19,'cash',90.00,0.01,'completed','','2025-10-26 05:06:15','2025-10-26 05:06:15','2025-10-26 05:06:15',NULL,NULL,NULL),(34,'VTA-2025-00034',1,1,3.50,18.00,0.63,0.00,4.13,'cash',5.00,0.87,'completed','','2025-10-26 05:27:05','2025-10-26 05:27:05','2025-10-26 05:27:05',NULL,NULL,NULL),(36,'VTA-2025-00035',1,1,42.00,18.00,7.56,0.00,49.56,'cash',42.00,0.00,'completed','','2025-10-26 06:02:24','2025-10-26 06:02:24','2025-10-26 06:02:24',NULL,NULL,NULL),(37,'VTA-2025-00036',1,1,100.00,18.00,18.00,0.00,118.00,'cash',100.00,0.00,'completed','','2025-10-26 06:05:16','2025-10-26 06:05:16','2025-10-26 06:05:16',NULL,NULL,NULL),(38,'VTA-2025-00037',1,1,3.75,18.00,0.68,0.00,4.43,'cash',4.00,0.25,'completed','','2025-10-26 06:21:38','2025-10-26 06:21:38','2025-10-26 06:21:38',NULL,NULL,NULL),(39,'VTA-2025-00038',1,1,50.75,18.00,9.14,0.00,59.89,'cash',51.00,0.25,'completed','','2025-10-28 14:09:12','2025-10-28 14:09:12','2025-10-28 14:09:12',NULL,NULL,NULL),(40,'VTA-2025-00039',1,1,139.99,18.00,25.20,0.00,165.19,'cash',140.00,0.01,'completed','','2025-10-29 00:43:52','2025-10-29 00:43:52','2025-10-29 00:43:52',NULL,NULL,NULL),(41,'VTA-2025-00040',1,1,89.99,18.00,16.20,0.00,106.19,'cash',90.00,0.01,'completed','','2025-10-30 02:18:03','2025-10-30 02:18:03','2025-10-30 02:18:03',NULL,NULL,NULL),(42,'VTA-2025-00041',1,1,3.00,18.00,0.54,0.00,3.54,'cash',5.00,2.00,'completed','','2025-10-31 18:11:48','2025-10-31 18:11:48','2025-10-31 18:11:48',NULL,NULL,NULL),(43,'VTA-2025-00042',1,1,7.00,18.00,1.26,0.00,8.26,'cash',10.00,3.00,'completed','','2025-10-31 18:34:39','2025-10-31 18:34:39','2025-10-31 18:34:39',NULL,NULL,NULL),(44,'VTA-2025-00043',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1600.00,100.00,'completed','','2025-11-01 02:43:18','2025-11-01 02:43:18','2025-11-01 02:43:18',NULL,NULL,NULL),(45,'VTA-2025-00044',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1600.00,100.00,'completed','','2025-11-01 02:43:50','2025-11-01 02:43:50','2025-11-01 02:43:50',NULL,NULL,NULL),(46,'VTA-2025-00045',1,1,1500.00,18.00,270.00,0.00,1770.00,'cash',1800.00,30.00,'completed','','2025-11-01 02:44:27','2025-11-01 02:44:27','2025-11-01 02:44:27',NULL,NULL,NULL),(47,'VTA-2025-00046',1,1,3.75,18.00,0.68,0.00,4.43,'cash',4.00,0.25,'completed','','2025-11-02 05:22:08','2025-11-02 05:22:08','2025-11-02 05:22:08',NULL,NULL,NULL),(48,'VTA-2025-00047',1,1,24.99,18.00,4.50,0.00,29.49,'cash',25.00,0.01,'completed','','2025-11-02 06:07:38','2025-11-02 06:07:38','2025-11-02 06:07:38',NULL,NULL,NULL),(49,'VTA-2025-00048',1,1,0.75,18.00,0.14,0.00,0.89,'cash',1.00,0.25,'completed','','2025-11-02 21:50:33','2025-11-02 21:50:33','2025-11-02 21:50:33',NULL,NULL,NULL),(50,'VTA-2025-00049',1,1,0.75,18.00,0.14,0.00,0.89,'cash',1.00,0.25,'completed','','2025-11-02 21:53:15','2025-11-02 21:53:15','2025-11-02 21:53:15',NULL,NULL,NULL),(51,'VTA-2025-00050',1,1,0.75,18.00,0.14,0.00,0.89,'cash',1.00,0.25,'completed','','2025-11-02 21:53:37','2025-11-02 21:53:37','2025-11-02 21:53:37',NULL,NULL,NULL),(52,'VTA-2025-00051',1,1,0.75,18.00,0.14,0.00,0.89,'cash',1.00,0.25,'completed','','2025-11-02 22:01:10','2025-11-02 22:01:10','2025-11-02 22:01:10',NULL,NULL,NULL);
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `sale_items`
--

DROP TABLE IF EXISTS `sale_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sale_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_sku` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `discount_percent` decimal(5,2) DEFAULT '0.00',
  `discount_amount` decimal(10,2) DEFAULT '0.00',
  `subtotal` decimal(10,2) NOT NULL,
  `tax_rate` decimal(5,2) DEFAULT '18.00',
  `tax_amount` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_sale` (`sale_id`),
  KEY `idx_product` (`product_id`),
  CONSTRAINT `sale_items_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sale_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_items`
--

LOCK TABLES `sale_items` WRITE;
/*!40000 ALTER TABLE `sale_items` DISABLE KEYS */;
INSERT INTO `sale_items` VALUES (1,1,4,'PROD-004','Agua Mineral 500ml',4.00,0.75,0.00,0.00,3.00,18.00,0.54,3.54,'2025-10-21 04:36:09'),(2,2,3,'PROD-003','Cuaderno Universitario 100 hojas',1.00,3.50,0.00,0.00,3.50,18.00,0.63,4.13,'2025-10-21 05:02:57'),(3,2,1,'PROD-001','Laptop Dell Inspiron 15',2.00,799.99,0.00,0.00,1599.98,18.00,288.00,1887.98,'2025-10-21 05:02:57'),(4,2,7,'PROD-000002','Trapeador',1.00,15.00,0.00,0.00,15.00,18.00,2.70,17.70,'2025-10-21 05:02:57'),(5,3,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-21 05:47:36'),(6,4,7,'PROD-000002','Trapeador',1.00,15.00,0.00,0.00,15.00,18.00,2.70,17.70,'2025-10-21 05:56:41'),(7,5,7,'PROD-000002','Trapeador',1.00,15.00,0.00,0.00,15.00,18.00,2.70,17.70,'2025-10-21 05:56:54'),(8,6,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-21 06:02:14'),(9,7,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-21 06:03:52'),(10,8,7,'PROD-000002','Trapeador',1.00,15.00,0.00,0.00,15.00,18.00,2.70,17.70,'2025-10-21 06:04:13'),(11,9,7,'PROD-000002','Trapeador',1.00,15.00,0.00,0.00,15.00,18.00,2.70,17.70,'2025-10-21 06:09:02'),(12,10,3,'PROD-003','Cuaderno Universitario 100 hojas',1.00,3.50,0.00,0.00,3.50,18.00,0.63,4.13,'2025-10-21 06:11:50'),(13,11,3,'PROD-003','Cuaderno Universitario 100 hojas',1.00,3.50,0.00,0.00,3.50,18.00,0.63,4.13,'2025-10-21 06:12:32'),(14,11,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-21 06:12:32'),(15,12,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-25 22:43:53'),(16,12,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-25 22:43:53'),(17,13,3,'PROD-003','Cuaderno Universitario 100 hojas',1.00,3.50,0.00,0.00,3.50,18.00,0.63,4.13,'2025-10-26 00:05:50'),(18,14,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-10-26 01:50:44'),(19,15,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-10-26 02:03:50'),(20,16,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-10-26 02:12:42'),(21,17,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-10-26 02:12:57'),(22,18,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-26 02:14:01'),(23,19,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-26 02:19:08'),(24,20,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-26 02:26:56'),(25,21,1,'PROD-001','Laptop Dell Inspiron 15',1.00,799.99,0.00,0.00,799.99,18.00,144.00,943.99,'2025-10-26 02:27:32'),(26,22,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-26 02:32:48'),(27,23,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-26 02:35:14'),(28,24,1,'PROD-001','Laptop Dell Inspiron 15',1.00,799.99,0.00,0.00,799.99,18.00,144.00,943.99,'2025-10-26 02:40:19'),(29,25,2,'PROD-002','Mouse Inalámbrico Logitech',2.00,24.99,0.00,0.00,49.98,18.00,9.00,58.98,'2025-10-26 02:49:22'),(30,26,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-26 02:49:56'),(31,27,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-26 02:51:52'),(32,28,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-26 02:54:07'),(33,29,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-26 02:57:41'),(34,30,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-10-26 03:11:09'),(35,31,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-26 03:14:42'),(36,32,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-26 03:15:38'),(37,33,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-26 05:06:15'),(38,34,3,'PROD-003','Cuaderno Universitario 100 hojas',1.00,3.50,0.00,0.00,3.50,18.00,0.63,4.13,'2025-10-26 05:27:05'),(40,36,3,'PROD-003','Cuaderno Universitario 100 hojas',12.00,3.50,0.00,0.00,42.00,18.00,7.56,49.56,'2025-10-26 06:02:24'),(41,37,6,'PROD-000001','Guantes de Box',2.00,50.00,0.00,0.00,100.00,18.00,18.00,118.00,'2025-10-26 06:05:16'),(42,38,4,'PROD-004','Agua Mineral 500ml',5.00,0.75,0.00,0.00,3.75,18.00,0.68,4.43,'2025-10-26 06:21:38'),(43,39,4,'PROD-004','Agua Mineral 500ml',1.00,0.75,0.00,0.00,0.75,18.00,0.14,0.89,'2025-10-28 14:09:12'),(44,39,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-28 14:09:12'),(45,40,6,'PROD-000001','Guantes de Box',1.00,50.00,0.00,0.00,50.00,18.00,9.00,59.00,'2025-10-29 00:43:52'),(46,40,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-29 00:43:52'),(47,41,5,'PROD-005','Teclado Mecánico RGB',1.00,89.99,0.00,0.00,89.99,18.00,16.20,106.19,'2025-10-30 02:18:03'),(48,42,4,'PROD-004','Agua Mineral 500ml',4.00,0.75,0.00,0.00,3.00,18.00,0.54,3.54,'2025-10-31 18:11:48'),(49,43,3,'PROD-003','Cuaderno Universitario 100 hojas',2.00,3.50,0.00,0.00,7.00,18.00,1.26,8.26,'2025-10-31 18:34:39'),(50,44,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-11-01 02:43:18'),(51,45,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-11-01 02:43:50'),(52,46,8,'PROD-000003','Carro',1.00,1500.00,0.00,0.00,1500.00,18.00,270.00,1770.00,'2025-11-01 02:44:27'),(53,47,4,'PROD-004','Agua Mineral 500ml',5.00,0.75,0.00,0.00,3.75,18.00,0.68,4.43,'2025-11-02 05:22:08'),(54,48,2,'PROD-002','Mouse Inalámbrico Logitech',1.00,24.99,0.00,0.00,24.99,18.00,4.50,29.49,'2025-11-02 06:07:38'),(55,49,4,'PROD-004','Agua Mineral 500ml',1.00,0.75,0.00,0.00,0.75,18.00,0.14,0.89,'2025-11-02 21:50:33'),(56,50,4,'PROD-004','Agua Mineral 500ml',1.00,0.75,0.00,0.00,0.75,18.00,0.14,0.89,'2025-11-02 21:53:15'),(57,51,4,'PROD-004','Agua Mineral 500ml',1.00,0.75,0.00,0.00,0.75,18.00,0.14,0.89,'2025-11-02 21:53:37'),(58,52,4,'PROD-004','Agua Mineral 500ml',1.00,0.75,0.00,0.00,0.75,18.00,0.14,0.89,'2025-11-02 22:01:10');
/*!40000 ALTER TABLE `sale_items` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `sale_details`
--

DROP TABLE IF EXISTS `sale_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sale_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` decimal(10,3) NOT NULL,
  `unit_price` decimal(12,4) NOT NULL,
  `discount_rate` decimal(5,2) DEFAULT '0.00' COMMENT 'Descuento % sobre este item',
  `discount_amount` decimal(12,2) DEFAULT '0.00',
  `tax_rate` decimal(5,2) DEFAULT '18.00',
  `tax_amount` decimal(12,2) DEFAULT '0.00',
  `line_total` decimal(12,2) NOT NULL,
  `product_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Código del producto al momento de la venta',
  `product_name` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Nombre del producto al momento de la venta',
  `notes` text COLLATE utf8mb4_unicode_ci COMMENT 'Notas específicas de este item',
  PRIMARY KEY (`id`),
  KEY `idx_sale_id` (`sale_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_product_code` (`product_code`),
  CONSTRAINT `sale_details_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`id`) ON DELETE CASCADE,
  CONSTRAINT `sale_details_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Detalles de las ventas';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_details`
--

LOCK TABLES `sale_details` WRITE;
/*!40000 ALTER TABLE `sale_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `sale_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:05


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `sale_payments`
--

DROP TABLE IF EXISTS `sale_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sale_id` int NOT NULL,
  `payment_method` enum('cash','card','transfer','other') COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `card_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `card_last_digits` varchar(4) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `transaction_reference` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_sale` (`sale_id`),
  KEY `idx_method` (`payment_method`),
  CONSTRAINT `sale_payments_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_payments`
--

LOCK TABLES `sale_payments` WRITE;
/*!40000 ALTER TABLE `sale_payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `sale_payments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `stock_movements`
--

DROP TABLE IF EXISTS `stock_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_movements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `movement_type` enum('in','out','adjustment','transfer') COLLATE utf8mb4_unicode_ci NOT NULL,
  `movement_reason` enum('purchase','sale','return','loss','found','adjustment','transfer','initial') COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference_type` enum('sale','purchase','adjustment','transfer','manual') COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference_id` int DEFAULT NULL COMMENT 'ID del documento relacionado',
  `quantity` decimal(10,3) NOT NULL,
  `previous_stock` decimal(10,3) NOT NULL,
  `new_stock` decimal(10,3) NOT NULL,
  `unit_cost` decimal(12,4) DEFAULT '0.0000',
  `movement_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` int NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_movement_date` (`movement_date`),
  KEY `idx_movement_type` (`movement_type`),
  KEY `idx_reference` (`reference_type`,`reference_id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `stock_movements_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `stock_movements_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Movimientos de stock';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_movements`
--

LOCK TABLES `stock_movements` WRITE;
/*!40000 ALTER TABLE `stock_movements` DISABLE KEYS */;
INSERT INTO `stock_movements` VALUES (1,8,'in','purchase','manual',NULL,3.000,0.000,3.000,0.0000,'2025-10-25 22:43:00',1,'Entrada de stock: +3.0'),(2,8,'in','purchase','manual',NULL,3.000,0.000,3.000,0.0000,'2025-10-26 01:50:05',1,'Entrada de stock: +3.0'),(3,8,'in','purchase','manual',NULL,5.000,-1.000,4.000,0.0000,'2025-10-26 05:07:26',1,'Entrada de stock: +5.0'),(4,9,'in','purchase','manual',NULL,30.000,0.000,30.000,0.0000,'2025-10-31 18:40:49',1,'Entrada de stock: +30.0'),(5,9,'out','sale','manual',NULL,-2.000,30.000,28.000,0.0000,'2025-10-31 18:42:19',1,'Salida de stock: -2.0');
/*!40000 ALTER TABLE `stock_movements` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `activity_logs`
--

DROP TABLE IF EXISTS `activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `table_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `record_id` int DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `old_values` json DEFAULT NULL COMMENT 'Valores anteriores del registro',
  `new_values` json DEFAULT NULL COMMENT 'Valores nuevos del registro',
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` text COLLATE utf8mb4_unicode_ci,
  `session_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_action` (`action`),
  KEY `idx_table_name` (`table_name`),
  KEY `idx_record_id` (`record_id`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_session_id` (`session_id`),
  CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Logs de actividad del sistema';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_logs`
--

LOCK TABLES `activity_logs` WRITE;
/*!40000 ALTER TABLE `activity_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `activity_logs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:05


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `user_sessions`
--

DROP TABLE IF EXISTS `user_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `login_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `logout_time` timestamp NULL DEFAULT NULL,
  `login_method` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'manual',
  `logout_reason` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `permissions` json DEFAULT NULL,
  `expires_at` timestamp NOT NULL,
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_agent` text COLLATE utf8mb4_unicode_ci,
  `last_activity` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_username` (`username`),
  KEY `idx_is_active` (`is_active`),
  KEY `idx_expires_at` (`expires_at`),
  KEY `idx_login_time` (`login_time`),
  KEY `idx_last_activity` (`last_activity`),
  CONSTRAINT `user_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=412 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Sesiones de usuarios activas';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sessions`
--

LOCK TABLES `user_sessions` WRITE;
/*!40000 ALTER TABLE `user_sessions` DISABLE KEYS */;
INSERT INTO `user_sessions` VALUES (1,1,'admin','admin','2025-09-29 21:58:07','2025-09-29 21:59:06','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 05:58:07',NULL,NULL,'2025-09-29 21:59:05'),(2,1,'admin','admin','2025-09-29 22:06:03','2025-09-29 22:06:09','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 06:06:03',NULL,NULL,'2025-09-29 22:06:09'),(3,2,'cajero1','cashier','2025-09-29 22:06:11','2025-09-29 22:06:17','manual','manual',0,'{\"ventas\": [\"ver\", \"crear\"], \"productos\": [\"ver\"]}','2025-09-30 06:06:11',NULL,NULL,'2025-09-29 22:06:16'),(4,1,'admin','admin','2025-09-29 22:06:27','2025-09-29 22:06:32','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 06:06:27',NULL,NULL,'2025-09-29 22:06:31'),(5,2,'cajero1','cashier','2025-09-29 22:06:37','2025-09-29 22:06:45','manual','manual',0,'{\"ventas\": [\"ver\", \"crear\"], \"productos\": [\"ver\"]}','2025-09-30 06:06:37',NULL,NULL,'2025-09-29 22:06:45'),(6,1,'admin','admin','2025-09-29 22:13:13','2025-09-29 22:13:19','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 06:13:13',NULL,NULL,'2025-09-29 22:13:19'),(7,2,'cajero1','cashier','2025-09-29 22:28:31','2025-09-29 22:28:39','manual','manual',0,'{\"ventas\": [\"ver\", \"crear\"], \"productos\": [\"ver\"]}','2025-09-30 06:28:31',NULL,NULL,'2025-09-29 22:28:39'),(8,1,'admin','admin','2025-09-29 23:01:49','2025-09-29 23:01:57','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 07:01:49',NULL,NULL,'2025-09-29 23:01:57'),(9,1,'admin','admin','2025-09-29 23:43:52','2025-09-29 23:43:59','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 07:43:52',NULL,NULL,'2025-09-29 23:43:58'),(10,1,'admin','admin','2025-09-29 23:45:00','2025-09-29 23:45:05','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 07:45:00',NULL,NULL,'2025-09-29 23:45:04'),(11,1,'admin','admin','2025-09-29 23:45:15','2025-09-29 23:45:20','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 07:45:15',NULL,NULL,'2025-09-29 23:45:19'),(12,1,'admin','admin','2025-09-29 23:46:14','2025-09-29 23:51:07','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 07:46:14',NULL,NULL,'2025-09-29 23:51:06'),(13,1,'admin','admin','2025-09-30 01:25:09','2025-09-30 01:25:29','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 09:25:09',NULL,NULL,'2025-09-30 01:25:28'),(14,1,'admin','admin','2025-09-30 02:18:17','2025-09-30 02:44:37','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 10:18:17',NULL,NULL,'2025-09-30 02:44:37'),(15,1,'admin','admin','2025-09-30 02:49:39','2025-09-30 02:53:54','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 10:49:39',NULL,NULL,'2025-09-30 02:53:53'),(16,1,'admin','admin','2025-09-30 02:54:15','2025-09-30 02:56:56','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 10:54:15',NULL,NULL,'2025-09-30 02:56:55'),(17,1,'admin','admin','2025-09-30 03:03:12','2025-09-30 03:14:37','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-09-30 11:03:12',NULL,NULL,'2025-09-30 03:14:36'),(18,1,'admin','admin','2025-10-01 02:37:51','2025-10-01 02:49:28','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 10:37:51',NULL,NULL,'2025-10-01 02:49:28'),(19,1,'admin','admin','2025-10-01 02:49:42','2025-10-01 03:08:54','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 10:49:42',NULL,NULL,'2025-10-01 03:08:53'),(20,1,'admin','admin','2025-10-01 03:09:02','2025-10-01 03:09:34','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 11:09:02',NULL,NULL,'2025-10-01 03:09:33'),(21,1,'admin','admin','2025-10-01 03:09:48','2025-10-01 03:09:59','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 11:09:48',NULL,NULL,'2025-10-01 03:09:58'),(22,5,'test','cashier','2025-10-01 03:10:05','2025-10-01 03:10:45','manual','manual',0,'null','2025-10-01 11:10:05',NULL,NULL,'2025-10-01 03:10:44'),(23,1,'admin','admin','2025-10-01 04:58:09','2025-10-01 05:04:47','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 12:58:09',NULL,NULL,'2025-10-01 05:04:46'),(24,1,'admin','admin','2025-10-01 05:04:59','2025-10-01 05:09:36','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:04:59',NULL,NULL,'2025-10-01 05:09:36'),(25,1,'admin','admin','2025-10-01 05:09:46','2025-10-01 05:30:46','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:09:46',NULL,NULL,'2025-10-01 05:30:45'),(26,1,'admin','admin','2025-10-01 05:31:04','2025-10-01 05:35:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:31:04',NULL,NULL,'2025-10-01 05:35:08'),(27,1,'admin','admin','2025-10-01 05:38:09','2025-10-01 05:41:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:38:09',NULL,NULL,'2025-10-01 05:41:43'),(28,1,'admin','admin','2025-10-01 05:42:02','2025-10-01 05:44:31','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:42:02',NULL,NULL,'2025-10-01 05:44:30'),(29,1,'admin','admin','2025-10-01 05:44:58','2025-10-01 05:47:51','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:44:58',NULL,NULL,'2025-10-01 05:47:50'),(30,1,'admin','admin','2025-10-01 05:48:05','2025-10-01 05:49:11','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-01 13:48:05',NULL,NULL,'2025-10-01 05:49:10'),(31,1,'admin','admin','2025-10-03 11:28:28','2025-10-03 11:45:30','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-03 19:28:28',NULL,NULL,'2025-10-03 11:45:30'),(32,1,'admin','admin','2025-10-03 11:45:46','2025-10-03 12:00:10','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-03 19:45:46',NULL,NULL,'2025-10-03 12:00:10'),(33,1,'admin','admin','2025-10-03 12:00:31','2025-10-03 12:06:16','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-03 20:00:31',NULL,NULL,'2025-10-03 12:06:15'),(34,1,'admin','admin','2025-10-03 12:06:41','2025-10-03 12:23:46','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-03 20:06:41',NULL,NULL,'2025-10-03 12:23:45'),(35,1,'admin','admin','2025-10-04 05:54:41','2025-10-04 06:12:30','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 13:54:41',NULL,NULL,'2025-10-04 06:12:29'),(36,1,'admin','admin','2025-10-04 06:12:36','2025-10-04 06:18:54','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:12:36',NULL,NULL,'2025-10-04 06:18:53'),(37,1,'admin','admin','2025-10-04 06:19:15','2025-10-04 06:22:28','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:19:15',NULL,NULL,'2025-10-04 06:22:27'),(38,7,'lpandov1','employee','2025-10-04 06:22:39','2025-10-04 06:23:07','manual','manual',0,'null','2025-10-04 14:22:39',NULL,NULL,'2025-10-04 06:23:07'),(39,1,'admin','admin','2025-10-04 06:32:54','2025-10-04 06:34:15','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:32:54',NULL,NULL,'2025-10-04 06:34:15'),(40,8,'lpandov2','user','2025-10-04 06:34:25','2025-10-04 06:34:38','manual','manual',0,'null','2025-10-04 14:34:25',NULL,NULL,'2025-10-04 06:34:38'),(41,1,'admin','admin','2025-10-04 06:34:48','2025-10-04 06:36:50','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:34:48',NULL,NULL,'2025-10-04 06:36:49'),(42,8,'lpandov2','user','2025-10-04 06:37:05','2025-10-04 06:37:24','manual','manual',0,'null','2025-10-04 14:37:05',NULL,NULL,'2025-10-04 06:37:24'),(43,1,'admin','admin','2025-10-04 06:38:06','2025-10-04 06:40:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:38:06',NULL,NULL,'2025-10-04 06:40:43'),(44,1,'admin','admin','2025-10-04 06:42:33','2025-10-04 06:42:44','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:42:33',NULL,NULL,'2025-10-04 06:42:44'),(45,8,'lpandov2','user','2025-10-04 06:42:57','2025-10-04 06:46:02','manual','cleanup',0,'null','2025-10-04 14:42:57',NULL,NULL,'2025-10-04 06:46:01'),(46,1,'admin','admin','2025-10-04 06:51:51','2025-10-04 06:52:01','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 14:51:51',NULL,NULL,'2025-10-04 06:52:00'),(47,8,'lpandov2','user','2025-10-04 06:52:31','2025-10-04 06:52:49','manual','manual',0,'null','2025-10-04 14:52:31',NULL,NULL,'2025-10-04 06:52:49'),(48,8,'lpandov2','user','2025-10-04 07:00:35','2025-10-04 07:04:04','manual','cleanup',0,'null','2025-10-04 15:00:35',NULL,NULL,'2025-10-04 07:04:03'),(49,1,'admin','admin','2025-10-04 07:08:49','2025-10-04 07:09:28','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 15:08:49',NULL,NULL,'2025-10-04 07:09:28'),(50,8,'lpandov2','user','2025-10-04 07:09:36','2025-10-04 07:11:00','manual','cleanup',0,'null','2025-10-04 15:09:36',NULL,NULL,'2025-10-04 07:10:59'),(51,8,'lpandov2','user','2025-10-04 07:12:29','2025-10-04 07:13:50','manual','cleanup',0,'null','2025-10-04 15:12:29',NULL,NULL,'2025-10-04 07:13:50'),(52,8,'lpandov2','user','2025-10-04 07:16:05','2025-10-04 07:17:47','manual','cleanup',0,'null','2025-10-04 15:16:05',NULL,NULL,'2025-10-04 07:17:47'),(53,8,'lpandov2','user','2025-10-04 07:18:22','2025-10-04 07:18:56','manual','manual',0,'null','2025-10-04 15:18:22',NULL,NULL,'2025-10-04 07:18:55'),(54,8,'lpandov2','user','2025-10-04 07:22:29','2025-10-04 07:23:04','manual','manual',0,'null','2025-10-04 15:22:29',NULL,NULL,'2025-10-04 07:23:03'),(55,1,'admin','admin','2025-10-04 07:23:10','2025-10-04 07:24:35','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 15:23:10',NULL,NULL,'2025-10-04 07:24:34'),(56,8,'lpandov2','user','2025-10-04 07:24:46','2025-10-04 07:25:16','manual','manual',0,'null','2025-10-04 15:24:46',NULL,NULL,'2025-10-04 07:25:15'),(57,1,'admin','admin','2025-10-04 07:31:32','2025-10-04 07:36:39','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 15:31:32',NULL,NULL,'2025-10-04 07:36:38'),(58,1,'admin','admin','2025-10-04 07:45:17','2025-10-04 07:45:27','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 15:45:17',NULL,NULL,'2025-10-04 07:45:27'),(59,1,'admin','admin','2025-10-04 07:56:46','2025-10-04 08:01:52','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-04 15:56:46',NULL,NULL,'2025-10-04 08:01:51'),(60,1,'admin','admin','2025-10-06 05:59:54','2025-10-06 06:02:52','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-06 13:59:54',NULL,NULL,'2025-10-06 06:02:51'),(61,1,'admin','admin','2025-10-06 06:10:05','2025-10-06 06:17:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-06 14:10:05',NULL,NULL,'2025-10-06 06:17:35'),(62,1,'admin','admin','2025-10-06 06:17:42','2025-10-06 06:21:38','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-06 14:17:42',NULL,NULL,'2025-10-06 06:21:38'),(63,1,'admin','admin','2025-10-06 06:21:52','2025-10-06 06:24:02','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-06 14:21:52',NULL,NULL,'2025-10-06 06:24:02'),(64,1,'admin','admin','2025-10-06 06:24:17','2025-10-06 06:28:21','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-06 14:24:17',NULL,NULL,'2025-10-06 06:28:20'),(65,1,'admin','admin','2025-10-06 06:28:27','2025-10-06 06:28:36','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-06 14:28:27',NULL,NULL,'2025-10-06 06:28:36'),(66,1,'admin','admin','2025-10-07 05:07:59','2025-10-07 05:08:21','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:07:59',NULL,NULL,'2025-10-07 05:08:21'),(67,1,'admin','admin','2025-10-07 05:15:45','2025-10-07 05:17:30','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:15:45',NULL,NULL,'2025-10-07 05:17:29'),(68,1,'admin','admin','2025-10-07 05:17:39','2025-10-07 05:19:19','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:17:39',NULL,NULL,'2025-10-07 05:19:19'),(69,1,'admin','admin','2025-10-07 05:19:36','2025-10-07 05:22:30','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:19:36',NULL,NULL,'2025-10-07 05:22:30'),(70,1,'admin','admin','2025-10-07 05:22:53','2025-10-07 05:26:04','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:22:53',NULL,NULL,'2025-10-07 05:26:04'),(71,1,'admin','admin','2025-10-07 05:26:16','2025-10-07 05:31:00','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:26:16',NULL,NULL,'2025-10-07 05:30:59'),(72,1,'admin','admin','2025-10-07 05:31:09','2025-10-07 05:35:39','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:31:09',NULL,NULL,'2025-10-07 05:35:39'),(73,1,'admin','admin','2025-10-07 05:35:50','2025-10-07 05:36:20','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:35:50',NULL,NULL,'2025-10-07 05:36:20'),(74,1,'admin','admin','2025-10-07 05:37:47','2025-10-07 05:38:05','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:37:47',NULL,NULL,'2025-10-07 05:38:04'),(75,1,'admin','admin','2025-10-07 05:39:40','2025-10-07 05:41:49','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:39:40',NULL,NULL,'2025-10-07 05:41:49'),(76,1,'admin','admin','2025-10-07 05:42:00','2025-10-07 05:43:33','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:42:00',NULL,NULL,'2025-10-07 05:43:32'),(77,1,'admin','admin','2025-10-07 05:47:37','2025-10-07 05:48:23','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:47:37',NULL,NULL,'2025-10-07 05:48:23'),(78,1,'admin','admin','2025-10-07 05:50:47','2025-10-07 05:51:18','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:50:47',NULL,NULL,'2025-10-07 05:51:18'),(79,1,'admin','admin','2025-10-07 05:52:50','2025-10-07 05:53:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:52:50',NULL,NULL,'2025-10-07 05:53:15'),(80,1,'admin','admin','2025-10-07 05:54:15','2025-10-07 05:55:17','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:54:15',NULL,NULL,'2025-10-07 05:55:17'),(81,1,'admin','admin','2025-10-07 05:55:31','2025-10-07 05:57:16','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 13:55:31',NULL,NULL,'2025-10-07 05:57:15'),(82,1,'admin','admin','2025-10-07 06:03:07','2025-10-07 06:05:10','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-07 14:03:07',NULL,NULL,'2025-10-07 06:05:09'),(83,9,'testv2','user','2025-10-07 06:05:17','2025-10-07 06:06:33','manual','cleanup',0,'null','2025-10-07 14:05:17',NULL,NULL,'2025-10-07 06:06:32'),(84,1,'admin','admin','2025-10-08 11:41:23','2025-10-08 12:24:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-08 19:41:23',NULL,NULL,'2025-10-08 12:24:12'),(85,1,'admin','admin','2025-10-08 12:09:07','2025-10-08 12:14:37','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-08 20:09:07',NULL,NULL,'2025-10-08 12:14:36'),(86,1,'admin','admin','2025-10-08 12:14:48','2025-10-08 12:24:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-08 20:14:48',NULL,NULL,'2025-10-08 12:24:07'),(87,1,'admin','admin','2025-10-08 12:38:39','2025-10-08 12:39:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-08 20:38:39',NULL,NULL,'2025-10-08 12:39:58'),(88,1,'admin','admin','2025-10-10 05:38:38','2025-10-10 05:42:04','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-10 13:38:38',NULL,NULL,'2025-10-10 05:42:04'),(89,1,'admin','admin','2025-10-10 05:46:05','2025-10-10 06:08:02','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-10 13:46:05',NULL,NULL,'2025-10-10 06:08:02'),(90,1,'admin','admin','2025-10-10 06:10:55','2025-10-10 06:13:28','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-10 14:10:55',NULL,NULL,'2025-10-10 06:13:27'),(91,1,'admin','admin','2025-10-10 06:15:16','2025-10-10 06:16:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-10 14:15:16',NULL,NULL,'2025-10-10 06:16:58'),(92,1,'admin','admin','2025-10-11 17:16:00','2025-10-11 17:21:05','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 01:16:00',NULL,NULL,'2025-10-11 17:21:05'),(93,1,'admin','admin','2025-10-11 17:23:56','2025-10-11 17:29:07','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 01:23:56',NULL,NULL,'2025-10-11 17:29:07'),(94,1,'admin','admin','2025-10-11 17:29:30','2025-10-11 17:34:45','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 01:29:30',NULL,NULL,'2025-10-11 17:34:45'),(95,1,'admin','admin','2025-10-11 17:36:54','2025-10-11 17:40:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 01:36:54',NULL,NULL,'2025-10-11 17:40:07'),(96,1,'admin','admin','2025-10-11 17:40:21','2025-10-11 18:31:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 01:40:21',NULL,NULL,'2025-10-11 18:31:34'),(97,1,'admin','admin','2025-10-11 18:31:46','2025-10-11 18:33:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 02:31:46',NULL,NULL,'2025-10-11 18:33:23'),(98,1,'admin','admin','2025-10-11 21:52:02','2025-10-11 21:56:04','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 05:52:02',NULL,NULL,'2025-10-11 21:56:04'),(99,1,'admin','admin','2025-10-11 21:57:20','2025-10-11 22:00:25','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 05:57:20',NULL,NULL,'2025-10-11 22:00:24'),(100,1,'admin','admin','2025-10-11 22:00:38','2025-10-11 22:02:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:00:38',NULL,NULL,'2025-10-11 22:02:42'),(101,1,'admin','admin','2025-10-11 22:02:57','2025-10-11 22:03:53','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:02:57',NULL,NULL,'2025-10-11 22:03:52'),(102,1,'admin','admin','2025-10-11 22:04:57','2025-10-11 22:08:40','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:04:57',NULL,NULL,'2025-10-11 22:08:40'),(103,1,'admin','admin','2025-10-11 22:09:03','2025-10-11 22:11:04','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:09:03',NULL,NULL,'2025-10-11 22:11:04'),(104,1,'admin','admin','2025-10-11 22:11:12','2025-10-11 22:13:50','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:11:12',NULL,NULL,'2025-10-11 22:13:49'),(105,1,'admin','admin','2025-10-11 22:17:44','2025-10-11 22:19:25','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:17:44',NULL,NULL,'2025-10-11 22:19:24'),(106,1,'admin','admin','2025-10-11 22:30:07','2025-10-11 22:42:19','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:30:07',NULL,NULL,'2025-10-11 22:42:18'),(107,1,'admin','admin','2025-10-11 22:42:58','2025-10-11 22:47:41','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:42:58',NULL,NULL,'2025-10-11 22:47:40'),(108,1,'admin','admin','2025-10-11 22:51:04','2025-10-11 23:09:41','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 06:51:04',NULL,NULL,'2025-10-11 23:09:40'),(109,1,'admin','admin','2025-10-11 23:09:57','2025-10-11 23:16:51','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:09:57',NULL,NULL,'2025-10-11 23:16:51'),(110,1,'admin','admin','2025-10-11 23:17:04','2025-10-11 23:19:07','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:17:04',NULL,NULL,'2025-10-11 23:19:07'),(111,1,'admin','admin','2025-10-11 23:19:13','2025-10-11 23:24:19','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:19:13',NULL,NULL,'2025-10-11 23:24:18'),(112,1,'admin','admin','2025-10-11 23:24:33',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:24:33',NULL,NULL,'2025-10-11 23:24:33'),(113,1,'admin','admin','2025-10-11 23:27:51','2025-10-11 23:32:36','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:27:51',NULL,NULL,'2025-10-11 23:32:35'),(114,1,'admin','admin','2025-10-11 23:32:50','2025-10-11 23:42:41','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:32:50',NULL,NULL,'2025-10-11 23:42:41'),(115,1,'admin','admin','2025-10-11 23:44:12','2025-10-11 23:46:36','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:44:12',NULL,NULL,'2025-10-11 23:46:35'),(116,1,'admin','admin','2025-10-11 23:46:55','2025-10-11 23:58:03','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:46:55',NULL,NULL,'2025-10-11 23:58:03'),(117,1,'admin','admin','2025-10-11 23:58:17','2025-10-12 00:03:52','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 07:58:17',NULL,NULL,'2025-10-12 00:03:51'),(118,1,'admin','admin','2025-10-12 00:04:09','2025-10-12 00:06:04','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:04:09',NULL,NULL,'2025-10-12 00:06:04'),(119,1,'admin','admin','2025-10-12 00:06:13','2025-10-12 00:09:56','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:06:13',NULL,NULL,'2025-10-12 00:09:55'),(120,1,'admin','admin','2025-10-12 00:10:48','2025-10-12 00:15:09','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:10:48',NULL,NULL,'2025-10-12 00:15:08'),(121,1,'admin','admin','2025-10-12 00:15:23','2025-10-12 00:18:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:15:23',NULL,NULL,'2025-10-12 00:18:07'),(122,1,'admin','admin','2025-10-12 00:19:11','2025-10-12 00:21:30','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:19:11',NULL,NULL,'2025-10-12 00:21:30'),(123,1,'admin','admin','2025-10-12 00:25:14','2025-10-12 00:26:22','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:25:14',NULL,NULL,'2025-10-12 00:26:21'),(124,1,'admin','admin','2025-10-12 00:27:14','2025-10-12 00:32:00','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:27:14',NULL,NULL,'2025-10-12 00:31:59'),(125,1,'admin','admin','2025-10-12 00:32:13','2025-10-12 00:33:25','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:32:13',NULL,NULL,'2025-10-12 00:33:25'),(126,1,'admin','admin','2025-10-12 00:33:57','2025-10-12 00:34:31','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:33:57',NULL,NULL,'2025-10-12 00:34:31'),(127,1,'admin','admin','2025-10-12 00:35:58','2025-10-12 00:40:06','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:35:58',NULL,NULL,'2025-10-12 00:40:06'),(128,1,'admin','admin','2025-10-12 00:44:14','2025-10-12 00:44:54','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:44:14',NULL,NULL,'2025-10-12 00:44:54'),(129,1,'admin','admin','2025-10-12 00:47:59','2025-10-12 00:51:42','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:47:59',NULL,NULL,'2025-10-12 00:51:42'),(130,1,'admin','admin','2025-10-12 00:51:58','2025-10-12 00:52:27','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:51:58',NULL,NULL,'2025-10-12 00:52:27'),(131,1,'admin','admin','2025-10-12 00:52:50','2025-10-12 00:58:09','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:52:50',NULL,NULL,'2025-10-12 00:58:09'),(132,10,'testv3','user','2025-10-12 00:58:19','2025-10-12 00:59:08','manual','manual',0,'null','2025-10-12 08:58:19',NULL,NULL,'2025-10-12 00:59:08'),(133,1,'admin','admin','2025-10-12 00:59:18','2025-10-12 01:39:29','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-12 08:59:18',NULL,NULL,'2025-10-12 01:39:29'),(134,1,'admin','admin','2025-10-18 17:22:03','2025-10-18 17:32:31','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:22:03',NULL,NULL,'2025-10-18 17:32:30'),(135,1,'admin','admin','2025-10-18 17:28:42','2025-10-18 17:32:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:28:42',NULL,NULL,'2025-10-18 17:32:34'),(136,1,'admin','admin','2025-10-18 17:32:52','2025-10-18 17:38:09','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:32:52',NULL,NULL,'2025-10-18 17:38:09'),(137,1,'admin','admin','2025-10-18 17:38:26','2025-10-18 17:45:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:38:26',NULL,NULL,'2025-10-18 17:45:14'),(138,1,'admin','admin','2025-10-18 17:43:32','2025-10-18 17:45:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:43:32',NULL,NULL,'2025-10-18 17:45:23'),(139,1,'admin','admin','2025-10-18 17:45:35','2025-10-18 17:52:58','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:45:35',NULL,NULL,'2025-10-18 17:52:57'),(140,1,'admin','admin','2025-10-18 17:47:50','2025-10-18 17:50:10','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:47:50',NULL,NULL,'2025-10-18 17:50:09'),(141,1,'admin','admin','2025-10-18 17:50:19','2025-10-18 17:56:06','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:50:19',NULL,NULL,'2025-10-18 17:56:05'),(142,1,'admin','admin','2025-10-18 17:52:37','2025-10-18 17:56:40','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:52:37',NULL,NULL,'2025-10-18 17:56:39'),(143,1,'admin','admin','2025-10-18 17:56:12','2025-10-18 18:02:03','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 01:56:12',NULL,NULL,'2025-10-18 18:02:03'),(144,1,'admin','admin','2025-10-18 18:02:18','2025-10-18 18:21:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 02:02:18',NULL,NULL,'2025-10-18 18:21:42'),(145,1,'admin','admin','2025-10-18 18:13:56','2025-10-18 19:03:23','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 02:13:56',NULL,NULL,'2025-10-18 19:03:23'),(146,1,'admin','admin','2025-10-18 18:36:44','2025-10-18 19:03:20','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 02:36:44',NULL,NULL,'2025-10-18 19:03:20'),(147,1,'admin','admin','2025-10-18 19:03:36','2025-10-18 19:07:33','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 03:03:36',NULL,NULL,'2025-10-18 19:07:33'),(148,1,'admin','admin','2025-10-18 19:07:47','2025-10-18 19:10:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 03:07:47',NULL,NULL,'2025-10-18 19:10:08'),(149,1,'admin','admin','2025-10-18 19:10:27','2025-10-18 19:18:13','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 03:10:27',NULL,NULL,'2025-10-18 19:18:12'),(150,1,'admin','admin','2025-10-18 20:05:02','2025-10-18 20:11:46','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 04:05:02',NULL,NULL,'2025-10-18 20:11:46'),(151,1,'admin','admin','2025-10-18 20:11:59','2025-10-18 20:15:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 04:11:59',NULL,NULL,'2025-10-18 20:15:24'),(152,1,'admin','admin','2025-10-18 20:15:59','2025-10-18 20:20:21','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 04:15:59',NULL,NULL,'2025-10-18 20:20:21'),(153,1,'admin','admin','2025-10-18 20:25:53','2025-10-18 20:37:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 04:25:53',NULL,NULL,'2025-10-18 20:37:14'),(154,1,'admin','admin','2025-10-18 20:37:56','2025-10-18 20:38:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 04:37:56',NULL,NULL,'2025-10-18 20:38:23'),(155,1,'admin','admin','2025-10-18 20:41:01','2025-10-18 20:47:18','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 04:41:01',NULL,NULL,'2025-10-18 20:47:17'),(156,1,'admin','admin','2025-10-18 22:18:20','2025-10-18 22:30:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 06:18:20',NULL,NULL,'2025-10-18 22:30:43'),(157,1,'admin','admin','2025-10-18 22:30:58','2025-10-18 22:49:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 06:30:58',NULL,NULL,'2025-10-18 22:49:13'),(158,1,'admin','admin','2025-10-19 00:05:38','2025-10-19 00:08:52','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 08:05:38',NULL,NULL,'2025-10-19 00:08:51'),(159,1,'admin','admin','2025-10-19 00:11:04','2025-10-19 00:17:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 08:11:04',NULL,NULL,'2025-10-19 00:17:58'),(160,1,'admin','admin','2025-10-19 00:20:04','2025-10-19 00:57:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-19 08:20:04',NULL,NULL,'2025-10-19 00:57:44'),(161,1,'admin','admin','2025-10-19 20:51:41','2025-10-19 21:10:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-20 04:51:41',NULL,NULL,'2025-10-19 21:10:12'),(162,1,'admin','admin','2025-10-19 21:11:00','2025-10-19 21:16:50','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-20 05:11:00',NULL,NULL,'2025-10-19 21:16:50'),(163,11,'Davicito','user','2025-10-19 21:16:59','2025-10-19 21:18:29','manual','manual',0,'null','2025-10-20 05:16:59',NULL,NULL,'2025-10-19 21:18:29'),(164,1,'admin','admin','2025-10-19 21:18:37','2025-10-19 21:19:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-20 05:18:37',NULL,NULL,'2025-10-19 21:19:13'),(165,1,'admin','admin','2025-10-21 01:38:43','2025-10-21 01:53:31','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 09:38:43',NULL,NULL,'2025-10-21 01:53:30'),(166,1,'admin','admin','2025-10-21 01:53:44','2025-10-21 02:13:33','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 09:53:44',NULL,NULL,'2025-10-21 02:13:32'),(167,1,'admin','admin','2025-10-21 02:13:46','2025-10-21 02:21:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 10:13:46',NULL,NULL,'2025-10-21 02:21:34'),(168,1,'admin','admin','2025-10-21 02:24:33','2025-10-21 02:27:05','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 10:24:33',NULL,NULL,'2025-10-21 02:27:05'),(169,1,'admin','admin','2025-10-21 02:27:14','2025-10-21 02:29:30','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 10:27:14',NULL,NULL,'2025-10-21 02:29:29'),(170,1,'admin','admin','2025-10-21 02:29:38','2025-10-21 02:31:10','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 10:29:38',NULL,NULL,'2025-10-21 02:31:10'),(171,1,'admin','admin','2025-10-21 02:31:22','2025-10-21 04:35:12','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 10:31:22',NULL,NULL,'2025-10-21 04:35:12'),(172,1,'admin','admin','2025-10-21 04:35:32','2025-10-21 04:47:17','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 12:35:32',NULL,NULL,'2025-10-21 04:47:17'),(173,1,'admin','admin','2025-10-21 04:47:26','2025-10-21 05:01:49','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 12:47:26',NULL,NULL,'2025-10-21 05:01:48'),(174,1,'admin','admin','2025-10-21 05:02:04','2025-10-21 05:10:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:02:04',NULL,NULL,'2025-10-21 05:10:43'),(175,1,'admin','admin','2025-10-21 05:10:57','2025-10-21 05:18:06','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:10:57',NULL,NULL,'2025-10-21 05:18:06'),(176,1,'admin','admin','2025-10-21 05:18:14','2025-10-21 05:20:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:18:14',NULL,NULL,'2025-10-21 05:20:23'),(177,1,'admin','admin','2025-10-21 05:20:31','2025-10-21 05:24:12','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:20:31',NULL,NULL,'2025-10-21 05:24:11'),(178,1,'admin','admin','2025-10-21 05:24:21','2025-10-21 05:31:56','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:24:21',NULL,NULL,'2025-10-21 05:31:56'),(179,1,'admin','admin','2025-10-21 05:32:08','2025-10-21 05:35:54','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:32:08',NULL,NULL,'2025-10-21 05:35:54'),(180,1,'admin','admin','2025-10-21 05:40:10','2025-10-21 05:42:26','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:40:10',NULL,NULL,'2025-10-21 05:42:25'),(181,1,'admin','admin','2025-10-21 05:42:35','2025-10-21 05:46:47','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:42:35',NULL,NULL,'2025-10-21 05:46:46'),(182,1,'admin','admin','2025-10-21 05:46:57',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:46:57',NULL,NULL,'2025-10-21 05:46:56'),(183,1,'admin','admin','2025-10-21 05:55:37','2025-10-21 06:00:05','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 13:55:37',NULL,NULL,'2025-10-21 06:00:05'),(184,1,'admin','admin','2025-10-21 06:01:25','2025-10-21 06:03:29','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 14:01:25',NULL,NULL,'2025-10-21 06:03:28'),(185,1,'admin','admin','2025-10-21 06:03:39','2025-10-21 06:07:58','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 14:03:39',NULL,NULL,'2025-10-21 06:07:57'),(186,1,'admin','admin','2025-10-21 06:08:49','2025-10-21 06:11:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 14:08:49',NULL,NULL,'2025-10-21 06:11:14'),(187,1,'admin','admin','2025-10-21 06:11:25','2025-10-21 06:12:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-21 14:11:25',NULL,NULL,'2025-10-21 06:12:59'),(188,1,'admin','admin','2025-10-24 04:49:12','2025-10-24 04:51:03','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-24 12:49:12',NULL,NULL,'2025-10-24 04:51:03'),(189,1,'admin','admin','2025-10-24 11:49:50','2025-10-24 12:35:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-24 19:49:50',NULL,NULL,'2025-10-24 12:35:24'),(190,1,'admin','admin','2025-10-24 12:35:39','2025-10-24 12:37:01','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-24 20:35:39',NULL,NULL,'2025-10-24 12:37:01'),(191,1,'admin','admin','2025-10-25 16:14:59','2025-10-25 16:23:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 00:14:59',NULL,NULL,'2025-10-25 16:23:44'),(192,1,'admin','admin','2025-10-25 16:23:51','2025-10-25 18:08:39','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 00:23:51',NULL,NULL,'2025-10-25 18:08:39'),(193,1,'admin','admin','2025-10-25 18:27:46','2025-10-25 18:29:07','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 02:27:46',NULL,NULL,'2025-10-25 18:29:07'),(194,1,'admin','admin','2025-10-25 18:46:33','2025-10-25 19:07:03','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 02:46:33',NULL,NULL,'2025-10-25 19:07:02'),(195,1,'admin','admin','2025-10-25 19:07:10','2025-10-25 19:07:18','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 03:07:10',NULL,NULL,'2025-10-25 19:07:18'),(196,1,'admin','admin','2025-10-25 19:11:17',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 03:11:17',NULL,NULL,'2025-10-25 19:11:17'),(197,1,'admin','admin','2025-10-25 19:18:02','2025-10-25 20:09:14','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 03:18:02',NULL,NULL,'2025-10-25 20:09:14'),(198,1,'admin','admin','2025-10-25 20:10:55','2025-10-25 20:27:50','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 04:10:55',NULL,NULL,'2025-10-25 20:27:49'),(199,1,'admin','admin','2025-10-25 20:28:11','2025-10-25 20:32:46','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 04:28:11',NULL,NULL,'2025-10-25 20:32:45'),(200,1,'admin','admin','2025-10-25 20:32:51','2025-10-25 20:44:34','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 04:32:51',NULL,NULL,'2025-10-25 20:44:33'),(201,1,'admin','admin','2025-10-25 20:44:54','2025-10-25 20:46:48','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 04:44:54',NULL,NULL,'2025-10-25 20:46:48'),(202,1,'admin','admin','2025-10-25 20:48:25','2025-10-25 21:04:38','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 04:48:25',NULL,NULL,'2025-10-25 21:04:37'),(203,1,'admin','admin','2025-10-25 21:05:03','2025-10-25 21:06:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 05:05:03',NULL,NULL,'2025-10-25 21:06:08'),(204,1,'admin','admin','2025-10-25 21:08:17','2025-10-25 21:08:46','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 05:08:17',NULL,NULL,'2025-10-25 21:08:45'),(205,1,'admin','admin','2025-10-25 21:14:10','2025-10-25 21:18:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 05:14:10',NULL,NULL,'2025-10-25 21:18:59'),(206,1,'admin','admin','2025-10-25 21:19:13','2025-10-25 22:40:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 05:19:13',NULL,NULL,'2025-10-25 22:40:34'),(207,1,'admin','admin','2025-10-25 22:40:52','2025-10-25 23:58:11','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 06:40:52',NULL,NULL,'2025-10-25 23:58:11'),(208,1,'admin','admin','2025-10-25 23:58:33','2025-10-26 01:59:32','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 07:58:33',NULL,NULL,'2025-10-26 01:59:32'),(209,1,'admin','admin','2025-10-26 02:03:19','2025-10-26 02:11:46','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:03:19',NULL,NULL,'2025-10-26 02:11:46'),(210,1,'admin','admin','2025-10-26 02:11:55','2025-10-26 02:14:22','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:11:55',NULL,NULL,'2025-10-26 02:14:21'),(211,1,'admin','admin','2025-10-26 02:18:53','2025-10-26 02:22:51','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:18:53',NULL,NULL,'2025-10-26 02:22:51'),(212,1,'admin','admin','2025-10-26 02:26:43','2025-10-26 02:32:16','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:26:43',NULL,NULL,'2025-10-26 02:32:15'),(213,1,'admin','admin','2025-10-26 02:32:25','2025-10-26 02:34:20','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:32:25',NULL,NULL,'2025-10-26 02:34:19'),(214,1,'admin','admin','2025-10-26 02:34:33','2025-10-26 02:37:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:34:33',NULL,NULL,'2025-10-26 02:37:24'),(215,1,'admin','admin','2025-10-26 02:39:51','2025-10-26 02:48:55','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:39:51',NULL,NULL,'2025-10-26 02:48:55'),(216,1,'admin','admin','2025-10-26 02:49:04','2025-10-26 02:51:18','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:49:04',NULL,NULL,'2025-10-26 02:51:18'),(217,1,'admin','admin','2025-10-26 02:51:26',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:51:26',NULL,NULL,'2025-10-26 02:51:25'),(218,1,'admin','admin','2025-10-26 02:53:43',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:53:43',NULL,NULL,'2025-10-26 02:53:42'),(219,1,'admin','admin','2025-10-26 02:57:24','2025-10-26 02:58:10','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 10:57:24',NULL,NULL,'2025-10-26 02:58:09'),(220,1,'admin','admin','2025-10-26 03:10:37','2025-10-26 03:12:29','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 11:10:37',NULL,NULL,'2025-10-26 03:12:28'),(221,1,'admin','admin','2025-10-26 03:14:03','2025-10-26 04:36:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 11:14:03',NULL,NULL,'2025-10-26 04:36:08'),(222,1,'admin','admin','2025-10-26 05:05:55','2025-10-26 05:25:50','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:05:55',NULL,NULL,'2025-10-26 05:25:49'),(223,1,'admin','admin','2025-10-26 05:25:58','2025-10-26 05:27:33','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:25:58',NULL,NULL,'2025-10-26 05:27:33'),(224,1,'admin','admin','2025-10-26 05:34:21','2025-10-26 05:36:12','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:34:21',NULL,NULL,'2025-10-26 05:36:11'),(225,1,'admin','admin','2025-10-26 05:42:05','2025-10-26 05:44:38','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:42:05',NULL,NULL,'2025-10-26 05:44:38'),(226,1,'admin','admin','2025-10-26 05:44:47','2025-10-26 05:49:48','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:44:47',NULL,NULL,'2025-10-26 05:49:48'),(227,1,'admin','admin','2025-10-26 05:49:55','2025-10-26 05:53:31','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:49:55',NULL,NULL,'2025-10-26 05:53:30'),(228,1,'admin','admin','2025-10-26 05:53:39','2025-10-26 05:55:31','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:53:39',NULL,NULL,'2025-10-26 05:55:30'),(229,1,'admin','admin','2025-10-26 05:55:41','2025-10-26 05:59:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:55:41',NULL,NULL,'2025-10-26 05:59:44'),(230,1,'admin','admin','2025-10-26 05:59:59','2025-10-26 06:01:50','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 13:59:59',NULL,NULL,'2025-10-26 06:01:50'),(231,1,'admin','admin','2025-10-26 06:02:01','2025-10-26 06:04:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 14:02:01',NULL,NULL,'2025-10-26 06:04:43'),(232,1,'admin','admin','2025-10-26 06:04:49','2025-10-26 06:10:54','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 14:04:49',NULL,NULL,'2025-10-26 06:10:54'),(233,1,'admin','admin','2025-10-26 06:11:04','2025-10-26 06:14:22','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 14:11:04',NULL,NULL,'2025-10-26 06:14:21'),(234,1,'admin','admin','2025-10-26 06:14:36','2025-10-26 06:19:00','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 14:14:36',NULL,NULL,'2025-10-26 06:19:00'),(235,1,'admin','admin','2025-10-26 06:19:09','2025-10-26 06:20:25','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 14:19:09',NULL,NULL,'2025-10-26 06:20:24'),(236,1,'admin','admin','2025-10-26 06:20:32','2025-10-26 06:26:14','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-26 14:20:32',NULL,NULL,'2025-10-26 06:26:13'),(237,1,'admin','admin','2025-10-28 04:08:58','2025-10-28 11:32:50','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 12:08:58',NULL,NULL,'2025-10-28 11:32:49'),(238,1,'admin','admin','2025-10-28 04:22:30','2025-10-28 04:44:16','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 12:22:30',NULL,NULL,'2025-10-28 04:44:15'),(239,12,'testv4','user','2025-10-28 04:44:26','2025-10-28 04:47:09','manual','manual',0,'null','2025-10-28 12:44:26',NULL,NULL,'2025-10-28 04:47:08'),(240,1,'admin','admin','2025-10-28 04:50:46','2025-10-28 04:57:29','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 12:50:46',NULL,NULL,'2025-10-28 04:57:29'),(241,12,'testv4','user','2025-10-28 04:57:43','2025-10-28 04:58:00','manual','manual',0,'null','2025-10-28 12:57:43',NULL,NULL,'2025-10-28 04:57:59'),(242,1,'admin','admin','2025-10-28 04:58:10','2025-10-28 04:59:45','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 12:58:10',NULL,NULL,'2025-10-28 04:59:44'),(243,12,'testv4','user','2025-10-28 04:59:53','2025-10-28 05:01:16','manual','manual',0,'null','2025-10-28 12:59:53',NULL,NULL,'2025-10-28 05:01:16'),(244,1,'admin','admin','2025-10-28 05:01:30','2025-10-28 11:32:42','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 13:01:30',NULL,NULL,'2025-10-28 11:32:42'),(245,1,'admin','admin','2025-10-28 11:33:02','2025-10-28 11:35:20','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 19:33:02',NULL,NULL,'2025-10-28 11:35:19'),(246,12,'testv4','user','2025-10-28 11:35:40','2025-10-28 11:35:52','manual','cleanup',0,'null','2025-10-28 19:35:40',NULL,NULL,'2025-10-28 11:35:52'),(247,13,'prueba_permisos','employee','2025-10-28 11:48:39','2025-10-28 11:53:34','manual','cleanup',0,'null','2025-10-28 19:48:39',NULL,NULL,'2025-10-28 11:53:34'),(248,1,'admin','admin','2025-10-28 11:53:59','2025-10-28 12:03:00','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 19:53:59',NULL,NULL,'2025-10-28 12:03:00'),(249,1,'admin','admin','2025-10-28 12:21:27','2025-10-28 12:24:54','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 20:21:27',NULL,NULL,'2025-10-28 12:24:54'),(250,1,'admin','admin','2025-10-28 12:25:37',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 20:25:37',NULL,NULL,'2025-10-28 12:25:36'),(251,1,'admin','admin','2025-10-28 14:04:50','2025-10-28 15:26:49','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 22:04:50',NULL,NULL,'2025-10-28 15:26:48'),(252,1,'admin','admin','2025-10-28 15:26:59','2025-10-28 15:46:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 23:26:59',NULL,NULL,'2025-10-28 15:46:24'),(253,1,'admin','admin','2025-10-28 15:46:34','2025-10-28 16:15:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-28 23:46:34',NULL,NULL,'2025-10-28 16:15:24'),(254,1,'admin','admin','2025-10-28 16:15:48','2025-10-28 16:23:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 00:15:48',NULL,NULL,'2025-10-28 16:23:35'),(255,1,'admin','admin','2025-10-28 16:23:54','2025-10-28 16:27:38','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 00:23:54',NULL,NULL,'2025-10-28 16:27:37'),(256,1,'admin','admin','2025-10-28 16:34:18','2025-10-28 16:52:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 00:34:18',NULL,NULL,'2025-10-28 16:52:43'),(257,1,'admin','admin','2025-10-28 19:19:52','2025-10-28 19:23:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 03:19:52',NULL,NULL,'2025-10-28 19:23:44'),(258,1,'admin','admin','2025-10-28 19:23:53','2025-10-28 19:26:21','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 03:23:53',NULL,NULL,'2025-10-28 19:26:21'),(259,1,'admin','admin','2025-10-28 19:26:34','2025-10-28 19:28:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 03:26:34',NULL,NULL,'2025-10-28 19:28:23'),(260,1,'admin','admin','2025-10-28 22:10:45','2025-10-28 22:30:03','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:10:45',NULL,NULL,'2025-10-28 22:30:02'),(261,1,'admin','admin','2025-10-28 22:30:11','2025-10-28 22:38:58','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:30:11',NULL,NULL,'2025-10-28 22:38:57'),(262,1,'admin','admin','2025-10-28 22:39:38','2025-10-28 22:42:53','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:39:38',NULL,NULL,'2025-10-28 22:42:52'),(263,1,'admin','admin','2025-10-28 22:43:06','2025-10-28 22:48:17','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:43:06',NULL,NULL,'2025-10-28 22:48:16'),(264,1,'admin','admin','2025-10-28 22:48:26','2025-10-28 22:51:01','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:48:26',NULL,NULL,'2025-10-28 22:51:01'),(265,1,'admin','admin','2025-10-28 22:51:10',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:51:10',NULL,NULL,'2025-10-28 22:51:10'),(266,1,'admin','admin','2025-10-28 22:59:57','2025-10-28 23:01:21','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 06:59:57',NULL,NULL,'2025-10-28 23:01:21'),(267,12,'testv4','user','2025-10-28 23:01:33','2025-10-28 23:01:48','manual','manual',0,'null','2025-10-29 07:01:33',NULL,NULL,'2025-10-28 23:01:48'),(268,1,'admin','admin','2025-10-28 23:02:03','2025-10-28 23:03:39','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 07:02:03',NULL,NULL,'2025-10-28 23:03:38'),(269,1,'admin','admin','2025-10-28 23:05:03','2025-10-28 23:05:30','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 07:05:03',NULL,NULL,'2025-10-28 23:05:29'),(270,12,'testv4','user','2025-10-28 23:05:38','2025-10-28 23:05:50','manual','cleanup',0,'null','2025-10-29 07:05:38',NULL,NULL,'2025-10-28 23:05:49'),(271,1,'admin','admin','2025-10-29 00:42:46','2025-10-29 11:49:06','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 08:42:46',NULL,NULL,'2025-10-29 11:49:06'),(272,1,'admin','admin','2025-10-29 11:49:28','2025-10-29 11:50:31','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 19:49:28',NULL,NULL,'2025-10-29 11:50:30'),(273,12,'testv4','user','2025-10-29 11:50:43','2025-10-29 12:06:02','manual','cleanup',0,'null','2025-10-29 19:50:43',NULL,NULL,'2025-10-29 12:06:02'),(274,12,'testv4','user','2025-10-29 12:06:33','2025-10-29 12:07:25','manual','cleanup',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-29 20:06:33',NULL,NULL,'2025-10-29 12:07:24'),(275,12,'testv4','user','2025-10-29 15:06:47','2025-10-29 15:07:14','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-29 23:06:47',NULL,NULL,'2025-10-29 15:07:14'),(276,1,'admin','admin','2025-10-29 15:07:23','2025-10-29 15:13:52','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-29 23:07:23',NULL,NULL,'2025-10-29 15:13:51'),(277,1,'admin','admin','2025-10-29 17:46:09','2025-10-29 17:46:54','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 01:46:09',NULL,NULL,'2025-10-29 17:46:54'),(278,12,'testv4','user','2025-10-29 17:47:06','2025-10-29 17:54:28','manual','cleanup',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-30 01:47:06',NULL,NULL,'2025-10-29 17:54:28'),(279,12,'testv4','user','2025-10-29 17:54:56','2025-10-29 17:55:16','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-30 01:54:56',NULL,NULL,'2025-10-29 17:55:16'),(280,1,'admin','admin','2025-10-29 17:55:32','2025-10-29 17:57:06','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 01:55:32',NULL,NULL,'2025-10-29 17:57:05'),(281,12,'testv4','user','2025-10-29 17:57:14','2025-10-29 17:57:49','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-30 01:57:14',NULL,NULL,'2025-10-29 17:57:49'),(282,1,'admin','admin','2025-10-29 17:58:03','2025-10-29 17:58:37','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 01:58:03',NULL,NULL,'2025-10-29 17:58:36'),(283,12,'testv4','user','2025-10-29 17:58:58','2025-10-29 18:18:37','manual','cleanup',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-30 01:58:58',NULL,NULL,'2025-10-29 18:18:36'),(284,12,'testv4','user','2025-10-29 18:18:50','2025-10-29 18:19:55','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-30 02:18:50',NULL,NULL,'2025-10-29 18:19:54'),(285,1,'admin','admin','2025-10-29 18:20:04','2025-10-29 21:22:23','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 02:20:04',NULL,NULL,'2025-10-29 21:22:23'),(286,12,'testv4','user','2025-10-29 21:22:40','2025-10-29 21:22:56','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\"]','2025-10-30 05:22:40',NULL,NULL,'2025-10-29 21:22:56'),(287,1,'admin','admin','2025-10-29 21:23:52','2025-10-29 21:24:59','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 05:23:52',NULL,NULL,'2025-10-29 21:24:58'),(288,10,'testv3','user','2025-10-29 21:25:12','2025-10-29 21:25:40','manual','manual',0,'[\"users.view\", \"roles.view\", \"system.config\", \"dashboard.view\"]','2025-10-30 05:25:12',NULL,NULL,'2025-10-29 21:25:39'),(289,1,'admin','admin','2025-10-29 21:37:28','2025-10-29 21:37:35','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 05:37:28',NULL,NULL,'2025-10-29 21:37:34'),(290,12,'testv4','user','2025-10-29 21:39:06','2025-10-29 21:40:41','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\"]','2025-10-30 05:39:06',NULL,NULL,'2025-10-29 21:40:41'),(291,14,'testv5','user','2025-10-29 21:40:50','2025-10-29 21:41:14','manual','manual',0,'[\"dashboard.view\"]','2025-10-30 05:40:50',NULL,NULL,'2025-10-29 21:41:13'),(292,1,'admin','admin','2025-10-29 21:41:24','2025-10-29 21:41:45','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 05:41:24',NULL,NULL,'2025-10-29 21:41:45'),(293,14,'testv5','user','2025-10-29 21:41:53','2025-10-29 21:42:16','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\", \"users.deactivate\", \"users.export\", \"dashboard.view\"]','2025-10-30 05:41:53',NULL,NULL,'2025-10-29 21:42:15'),(294,1,'admin','admin','2025-10-29 21:42:30','2025-10-29 21:42:50','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 05:42:30',NULL,NULL,'2025-10-29 21:42:49'),(295,12,'testv4','user','2025-10-29 21:43:00','2025-10-29 21:43:12','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\"]','2025-10-30 05:43:00',NULL,NULL,'2025-10-29 21:43:12'),(296,12,'testv4','user','2025-10-29 21:43:22','2025-10-29 21:43:28','manual','cleanup',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\"]','2025-10-30 05:43:22',NULL,NULL,'2025-10-29 21:43:27'),(297,1,'admin','admin','2025-10-29 22:44:34','2025-10-29 22:45:00','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:44:34',NULL,NULL,'2025-10-29 22:45:00'),(298,14,'testv5','user','2025-10-29 22:45:09','2025-10-29 22:45:30','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\"]','2025-10-30 06:45:09',NULL,NULL,'2025-10-29 22:45:29'),(299,1,'admin','admin','2025-10-29 22:45:38','2025-10-29 22:46:17','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:45:38',NULL,NULL,'2025-10-29 22:46:16'),(300,1,'admin','admin','2025-10-29 22:46:31','2025-10-29 22:46:57','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:46:31',NULL,NULL,'2025-10-29 22:46:57'),(301,1,'admin','admin','2025-10-29 22:49:09','2025-10-29 22:50:14','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:49:09',NULL,NULL,'2025-10-29 22:50:13'),(302,1,'admin','admin','2025-10-29 22:50:29','2025-10-29 22:51:15','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:50:29',NULL,NULL,'2025-10-29 22:51:14'),(303,15,'testv6','user','2025-10-29 22:51:26','2025-10-29 22:51:38','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\"]','2025-10-30 06:51:26',NULL,NULL,'2025-10-29 22:51:38'),(304,1,'admin','admin','2025-10-29 22:51:45','2025-10-29 22:52:08','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:51:45',NULL,NULL,'2025-10-29 22:52:07'),(305,15,'testv6','user','2025-10-29 22:52:16','2025-10-29 22:52:28','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\"]','2025-10-30 06:52:16',NULL,NULL,'2025-10-29 22:52:28'),(306,15,'testv6','user','2025-10-29 22:53:54','2025-10-29 22:54:17','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\"]','2025-10-30 06:53:54',NULL,NULL,'2025-10-29 22:54:16'),(307,1,'admin','admin','2025-10-29 22:54:23','2025-10-30 02:13:20','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 06:54:23',NULL,NULL,'2025-10-30 02:13:20'),(308,1,'admin','admin','2025-10-30 02:16:44','2025-10-30 02:32:22','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 10:16:44',NULL,NULL,'2025-10-30 02:32:22'),(309,1,'admin','admin','2025-10-30 02:33:17','2025-10-30 02:36:00','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 10:33:17',NULL,NULL,'2025-10-30 02:36:00'),(310,1,'admin','admin','2025-10-30 02:37:01','2025-10-30 02:39:19','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 10:37:01',NULL,NULL,'2025-10-30 02:39:19'),(311,1,'admin','admin','2025-10-30 02:42:05','2025-10-30 02:47:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 10:42:05',NULL,NULL,'2025-10-30 02:47:13'),(312,1,'admin','admin','2025-10-30 02:49:47','2025-10-30 02:52:47','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 10:49:47',NULL,NULL,'2025-10-30 02:52:47'),(313,1,'admin','admin','2025-10-30 02:54:07','2025-10-30 02:59:37','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 10:54:07',NULL,NULL,'2025-10-30 02:59:36'),(314,1,'admin','admin','2025-10-30 03:00:10','2025-10-30 03:07:37','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 11:00:10',NULL,NULL,'2025-10-30 03:07:36'),(315,1,'admin','admin','2025-10-30 03:09:20','2025-10-30 03:11:18','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 11:09:20',NULL,NULL,'2025-10-30 03:11:17'),(316,1,'admin','admin','2025-10-30 03:11:31','2025-10-30 04:33:58','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 11:11:31',NULL,NULL,'2025-10-30 04:33:58'),(317,1,'admin','admin','2025-10-30 04:34:20','2025-10-30 04:44:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 12:34:20',NULL,NULL,'2025-10-30 04:44:14'),(318,1,'admin','admin','2025-10-30 04:45:36','2025-10-30 04:49:50','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 12:45:36',NULL,NULL,'2025-10-30 04:49:50'),(319,1,'admin','admin','2025-10-30 04:52:26','2025-10-30 04:56:01','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 12:52:26',NULL,NULL,'2025-10-30 04:56:01'),(320,1,'admin','admin','2025-10-30 04:56:51','2025-10-30 04:58:26','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-30 12:56:51',NULL,NULL,'2025-10-30 04:58:26'),(321,14,'testv5','user','2025-10-30 04:58:38','2025-10-30 05:17:24','manual','cleanup',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\"]','2025-10-30 12:58:38',NULL,NULL,'2025-10-30 05:17:23'),(322,1,'admin','admin','2025-10-31 00:31:59','2025-10-31 03:50:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 08:31:59',NULL,NULL,'2025-10-31 03:50:24'),(323,1,'admin','admin','2025-10-31 03:51:54','2025-10-31 03:53:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 11:51:54',NULL,NULL,'2025-10-31 03:53:43'),(324,1,'admin','admin','2025-10-31 03:54:02','2025-10-31 03:54:48','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 11:54:02',NULL,NULL,'2025-10-31 03:54:47'),(325,15,'testv6','supervisor','2025-10-31 03:54:57','2025-10-31 03:55:19','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.delete\", \"users.activate\"]','2025-10-31 11:54:57',NULL,NULL,'2025-10-31 03:55:18'),(326,1,'admin','admin','2025-10-31 03:55:26','2025-10-31 03:57:49','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 11:55:26',NULL,NULL,'2025-10-31 03:57:48'),(327,15,'testv6','supervisor','2025-10-31 03:57:59','2025-10-31 03:58:13','manual','manual',0,'[\"users.view\"]','2025-10-31 11:57:59',NULL,NULL,'2025-10-31 03:58:12'),(328,1,'admin','admin','2025-10-31 03:58:19','2025-10-31 03:58:44','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 11:58:19',NULL,NULL,'2025-10-31 03:58:44'),(329,15,'testv6','supervisor','2025-10-31 03:58:54','2025-10-31 03:59:08','manual','manual',0,'[\"users.view\", \"users.create\"]','2025-10-31 11:58:54',NULL,NULL,'2025-10-31 03:59:08'),(330,1,'admin','admin','2025-10-31 03:59:17','2025-10-31 04:00:29','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 11:59:17',NULL,NULL,'2025-10-31 04:00:29'),(331,1,'admin','admin','2025-10-31 04:00:37','2025-10-31 04:02:40','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:00:37',NULL,NULL,'2025-10-31 04:02:40'),(332,15,'testv6','supervisor','2025-10-31 04:02:54','2025-10-31 04:03:15','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.activate\", \"users.deactivate\"]','2025-10-31 12:02:54',NULL,NULL,'2025-10-31 04:03:15'),(333,1,'admin','admin','2025-10-31 04:03:26','2025-10-31 04:04:13','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:03:26',NULL,NULL,'2025-10-31 04:04:13'),(334,15,'testv6','supervisor','2025-10-31 04:04:22','2025-10-31 04:05:54','manual','manual',0,'[\"users.view\", \"users.create\", \"users.edit\", \"users.activate\", \"users.deactivate\", \"roles.view\"]','2025-10-31 12:04:22',NULL,NULL,'2025-10-31 04:05:53'),(335,1,'admin','admin','2025-10-31 04:06:01','2025-10-31 04:08:37','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:06:01',NULL,NULL,'2025-10-31 04:08:37'),(336,15,'testv6','supervisor','2025-10-31 04:08:48','2025-10-31 04:09:18','manual','manual',0,'[\"roles.view\"]','2025-10-31 12:08:48',NULL,NULL,'2025-10-31 04:09:18'),(337,1,'admin','admin','2025-10-31 04:09:26','2025-10-31 04:10:22','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:09:26',NULL,NULL,'2025-10-31 04:10:21'),(338,15,'testv6','supervisor','2025-10-31 04:10:32','2025-10-31 04:10:51','manual','manual',0,'[\"roles.view\", \"inventory.view\"]','2025-10-31 12:10:32',NULL,NULL,'2025-10-31 04:10:51'),(339,15,'testv6','supervisor','2025-10-31 04:11:02','2025-10-31 04:11:51','manual','manual',0,'[\"roles.view\", \"inventory.view\"]','2025-10-31 12:11:02',NULL,NULL,'2025-10-31 04:11:51'),(340,1,'admin','admin','2025-10-31 04:11:58','2025-10-31 04:12:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:11:58',NULL,NULL,'2025-10-31 04:12:58'),(341,1,'admin','admin','2025-10-31 04:26:10','2025-10-31 04:31:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:26:10',NULL,NULL,'2025-10-31 04:31:14'),(342,1,'admin','admin','2025-10-31 04:31:38','2025-10-31 04:54:47','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 12:31:38',NULL,NULL,'2025-10-31 04:54:46'),(343,1,'admin','admin','2025-10-31 05:13:02','2025-10-31 05:18:01','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 13:13:02',NULL,NULL,'2025-10-31 05:18:01'),(344,1,'admin','admin','2025-10-31 05:33:03','2025-10-31 05:34:34','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 13:33:03',NULL,NULL,'2025-10-31 05:34:34'),(345,15,'testv6','supervisor','2025-10-31 05:34:42','2025-10-31 05:34:59','manual','manual',0,'[\"roles.view\", \"inventory.view\"]','2025-10-31 13:34:42',NULL,NULL,'2025-10-31 05:34:59'),(346,1,'admin','admin','2025-10-31 05:35:10','2025-10-31 05:39:59','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 13:35:10',NULL,NULL,'2025-10-31 05:39:58'),(347,1,'admin','admin','2025-10-31 05:45:41','2025-10-31 05:49:01','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 13:45:41',NULL,NULL,'2025-10-31 05:49:01'),(348,1,'admin','admin','2025-10-31 06:01:57','2025-10-31 06:02:26','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 14:01:57',NULL,NULL,'2025-10-31 06:02:25'),(349,1,'admin','admin','2025-10-31 14:24:34','2025-10-31 16:26:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-10-31 22:24:34',NULL,NULL,'2025-10-31 16:26:12'),(350,1,'admin','admin','2025-10-31 16:26:21','2025-10-31 16:47:12','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 00:26:21',NULL,NULL,'2025-10-31 16:47:12'),(351,1,'admin','admin','2025-10-31 16:47:28',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 00:47:28',NULL,NULL,'2025-10-31 16:47:27'),(352,1,'admin','admin','2025-10-31 17:08:55','2025-10-31 17:11:17','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:08:55',NULL,NULL,'2025-10-31 17:11:16'),(353,1,'admin','admin','2025-10-31 17:11:27','2025-10-31 17:11:49','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:11:27',NULL,NULL,'2025-10-31 17:11:48'),(354,1,'admin','admin','2025-10-31 17:14:29','2025-10-31 17:16:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:14:29',NULL,NULL,'2025-10-31 17:16:35'),(355,1,'admin','admin','2025-10-31 17:16:43','2025-10-31 17:18:19','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:16:43',NULL,NULL,'2025-10-31 17:18:19'),(356,1,'admin','admin','2025-10-31 17:24:27','2025-10-31 17:24:40','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:24:27',NULL,NULL,'2025-10-31 17:24:40'),(357,1,'admin','admin','2025-10-31 17:28:13','2025-10-31 17:29:42','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:28:13',NULL,NULL,'2025-10-31 17:29:42'),(358,1,'admin','admin','2025-10-31 17:30:10','2025-10-31 17:31:56','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:30:10',NULL,NULL,'2025-10-31 17:31:56'),(359,1,'admin','admin','2025-10-31 17:32:17','2025-10-31 17:33:10','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:32:17',NULL,NULL,'2025-10-31 17:33:09'),(360,1,'admin','admin','2025-10-31 17:33:21','2025-10-31 17:33:42','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:33:21',NULL,NULL,'2025-10-31 17:33:41'),(361,1,'admin','admin','2025-10-31 17:33:51','2025-10-31 17:34:19','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:33:51',NULL,NULL,'2025-10-31 17:34:19'),(362,1,'admin','admin','2025-10-31 17:34:27','2025-10-31 17:38:54','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:34:27',NULL,NULL,'2025-10-31 17:38:53'),(363,16,'testv7','admin','2025-10-31 17:39:14','2025-10-31 17:40:39','manual','manual',0,'[\"*\"]','2025-11-01 01:39:14',NULL,NULL,'2025-10-31 17:40:38'),(364,16,'testv7','supervisor','2025-10-31 17:40:49','2025-10-31 17:41:41','manual','manual',0,'[\"users.view\", \"inventory.view\", \"inventory.reports\", \"inventory.export\", \"sales.view\", \"sales.create\", \"sales.reports\", \"sales.export\", \"dashboard.view\", \"dashboard.stats\", \"reports.sales\", \"reports.inventory\"]','2025-11-01 01:40:49',NULL,NULL,'2025-10-31 17:41:41'),(365,1,'admin','admin','2025-10-31 17:41:52','2025-10-31 18:04:45','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 01:41:52',NULL,NULL,'2025-10-31 18:04:45'),(366,1,'admin','admin','2025-10-31 18:05:06','2025-10-31 19:06:08','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 02:05:06',NULL,NULL,'2025-10-31 19:06:07'),(367,1,'admin','admin','2025-10-31 19:06:17','2025-10-31 19:06:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 03:06:17',NULL,NULL,'2025-10-31 19:06:34'),(368,1,'admin','admin','2025-10-31 19:08:48','2025-10-31 19:48:32','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 03:08:48',NULL,NULL,'2025-10-31 19:48:32'),(369,1,'admin','admin','2025-10-31 19:50:41','2025-10-31 22:57:10','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 03:50:41',NULL,NULL,'2025-10-31 22:57:09'),(370,1,'admin','admin','2025-10-31 22:58:10','2025-11-01 00:52:18','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 06:58:10',NULL,NULL,'2025-11-01 00:52:17'),(371,1,'admin','admin','2025-11-01 02:40:23','2025-11-01 03:07:14','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 10:40:23',NULL,NULL,'2025-11-01 03:07:14'),(372,1,'admin','admin','2025-11-01 03:07:24','2025-11-01 03:08:21','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 11:07:24',NULL,NULL,'2025-11-01 03:08:21'),(373,1,'admin','admin','2025-11-01 03:35:05','2025-11-01 04:29:34','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 11:35:05',NULL,NULL,'2025-11-01 04:29:33'),(374,1,'admin','admin','2025-11-01 04:29:48','2025-11-01 04:39:16','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 12:29:48',NULL,NULL,'2025-11-01 04:39:15'),(375,1,'admin','admin','2025-11-01 04:39:31','2025-11-01 04:44:45','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 12:39:31',NULL,NULL,'2025-11-01 04:44:44'),(376,1,'admin','admin','2025-11-01 04:45:35','2025-11-01 04:54:09','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 12:45:35',NULL,NULL,'2025-11-01 04:54:08'),(377,1,'admin','admin','2025-11-01 04:54:23','2025-11-01 04:55:27','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-01 12:54:23',NULL,NULL,'2025-11-01 04:55:27'),(378,1,'admin','admin','2025-11-02 02:46:31','2025-11-02 02:50:04','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 10:46:31',NULL,NULL,'2025-11-02 02:50:03'),(379,1,'admin','admin','2025-11-02 02:51:07','2025-11-02 04:10:28','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 10:51:07',NULL,NULL,'2025-11-02 04:10:28'),(380,1,'admin','admin','2025-11-02 04:15:53','2025-11-02 04:16:40','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 12:15:53',NULL,NULL,'2025-11-02 04:16:39'),(381,1,'admin','admin','2025-11-02 04:17:14','2025-11-02 04:19:44','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 12:17:14',NULL,NULL,'2025-11-02 04:19:43'),(382,15,'testv6','supervisor','2025-11-02 04:19:59','2025-11-02 04:20:04','manual','manual',0,'[\"roles.view\", \"inventory.view\"]','2025-11-02 12:19:59',NULL,NULL,'2025-11-02 04:20:04'),(383,1,'admin','admin','2025-11-02 04:25:53','2025-11-02 04:47:24','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 12:25:53',NULL,NULL,'2025-11-02 04:47:23'),(384,1,'admin','admin','2025-11-02 04:47:38','2025-11-02 04:57:35','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 12:47:38',NULL,NULL,'2025-11-02 04:57:34'),(385,1,'admin','admin','2025-11-02 04:57:45','2025-11-02 04:59:39','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 12:57:45',NULL,NULL,'2025-11-02 04:59:38'),(386,1,'admin','admin','2025-11-02 05:06:42','2025-11-02 05:07:11','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 13:06:42',NULL,NULL,'2025-11-02 05:07:10'),(387,1,'admin','admin','2025-11-02 05:21:25','2025-11-02 05:29:15','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 13:21:25',NULL,NULL,'2025-11-02 05:29:15'),(388,1,'admin','admin','2025-11-02 05:53:21','2025-11-02 05:58:44','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 13:53:21',NULL,NULL,'2025-11-02 05:58:43'),(389,1,'admin','admin','2025-11-02 06:00:33','2025-11-02 06:04:02','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 14:00:33',NULL,NULL,'2025-11-02 06:04:01'),(390,1,'admin','admin','2025-11-02 06:06:41','2025-11-02 06:14:18','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 14:06:41',NULL,NULL,'2025-11-02 06:14:18'),(391,15,'testv6','user','2025-11-02 06:14:33','2025-11-02 06:14:46','manual','manual',0,'[\"reports.basic\", \"reports.full\"]','2025-11-02 14:14:33',NULL,NULL,'2025-11-02 06:14:46'),(392,1,'admin','admin','2025-11-02 06:15:00','2025-11-02 06:31:34','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 14:15:00',NULL,NULL,'2025-11-02 06:31:33'),(393,1,'admin','admin','2025-11-02 06:31:44','2025-11-02 06:32:00','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 14:31:44',NULL,NULL,'2025-11-02 06:31:59'),(394,1,'admin','admin','2025-11-02 07:09:17','2025-11-02 07:09:27','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 15:09:17',NULL,NULL,'2025-11-02 07:09:27'),(395,1,'admin','admin','2025-11-02 07:22:33','2025-11-02 07:22:40','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 15:22:33',NULL,NULL,'2025-11-02 07:22:40'),(396,1,'admin','admin','2025-11-02 07:24:14','2025-11-02 07:24:43','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-02 15:24:14',NULL,NULL,'2025-11-02 07:24:43'),(397,1,'admin','admin','2025-11-02 18:43:11',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 02:43:11',NULL,NULL,'2025-11-02 18:43:11'),(398,1,'admin','admin','2025-11-02 19:57:36','2025-11-02 19:57:53','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 03:57:36',NULL,NULL,'2025-11-02 19:57:52'),(399,1,'admin','admin','2025-11-02 19:59:41','2025-11-02 20:00:54','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 03:59:41',NULL,NULL,'2025-11-02 20:00:53'),(400,1,'admin','admin','2025-11-02 20:09:49','2025-11-02 20:10:06','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 04:09:49',NULL,NULL,'2025-11-02 20:10:06'),(401,1,'admin','admin','2025-11-02 21:02:05','2025-11-02 21:02:15','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:02:05',NULL,NULL,'2025-11-02 21:02:15'),(402,1,'admin','admin','2025-11-02 21:06:09','2025-11-02 21:10:55','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:06:09',NULL,NULL,'2025-11-02 21:10:54'),(403,1,'admin','admin','2025-11-02 21:13:09','2025-11-02 21:13:51','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:13:09',NULL,NULL,'2025-11-02 21:13:50'),(404,1,'admin','admin','2025-11-02 21:17:40','2025-11-02 21:22:13','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:17:40',NULL,NULL,'2025-11-02 21:22:13'),(405,1,'admin','admin','2025-11-02 21:21:04',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:21:04',NULL,NULL,'2025-11-02 21:21:04'),(406,1,'admin','admin','2025-11-02 21:22:21',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:22:21',NULL,NULL,'2025-11-02 21:22:20'),(407,1,'admin','admin','2025-11-02 21:43:18',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:43:18',NULL,NULL,'2025-11-02 21:43:17'),(408,1,'admin','admin','2025-11-02 21:44:03',NULL,'manual',NULL,1,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:44:03',NULL,NULL,'2025-11-02 21:44:02'),(409,1,'admin','admin','2025-11-02 21:50:21','2025-11-02 21:51:39','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:50:21',NULL,NULL,'2025-11-02 21:51:38'),(410,1,'admin','admin','2025-11-02 21:53:05','2025-11-02 21:54:28','manual','manual',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 05:53:05',NULL,NULL,'2025-11-02 21:54:28'),(411,1,'admin','admin','2025-11-02 22:00:35','2025-11-02 22:01:18','manual','cleanup',0,'{\"all_modules\": true, \"super_admin\": true}','2025-11-03 06:00:35',NULL,NULL,'2025-11-02 22:01:17');
/*!40000 ALTER TABLE `user_sessions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `system_config`
--

DROP TABLE IF EXISTS `system_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `config_key` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `config_value` text COLLATE utf8mb4_unicode_ci,
  `config_type` enum('string','integer','float','boolean','json') COLLATE utf8mb4_unicode_ci DEFAULT 'string',
  `description` text COLLATE utf8mb4_unicode_ci,
  `is_public` tinyint(1) DEFAULT '0' COMMENT 'Si usuarios normales pueden verlo',
  `is_editable` tinyint(1) DEFAULT '1' COMMENT 'Si se puede modificar desde la UI',
  `category` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'general',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key` (`config_key`),
  KEY `idx_config_key` (`config_key`),
  KEY `idx_category` (`category`),
  KEY `idx_config_type` (`config_type`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Configuraciones del sistema';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_config`
--

LOCK TABLES `system_config` WRITE;
/*!40000 ALTER TABLE `system_config` DISABLE KEYS */;
INSERT INTO `system_config` VALUES (1,'app_name','Sistema POS Avanzado','string','Nombre de la aplicación',1,1,'general','2025-09-29 05:42:46','2025-09-29 05:42:46'),(2,'app_version','2.0.0','string','Versión de la aplicación',1,0,'general','2025-09-29 05:42:46','2025-09-29 05:42:46'),(3,'company_name','Mi Empresa POS','string','Nombre de la empresa',1,1,'company','2025-09-29 05:42:46','2025-09-29 05:42:46'),(4,'company_address','Av. Principal 123, Lima','string','Dirección de la empresa',1,1,'company','2025-09-29 05:42:46','2025-09-29 05:42:46'),(5,'company_phone','(01) 234-5678','string','Teléfono de la empresa',1,1,'company','2025-09-29 05:42:46','2025-09-29 05:42:46'),(6,'company_email','info@miempresa.com','string','Email de la empresa',1,1,'company','2025-09-29 05:42:46','2025-09-29 05:42:46'),(7,'currency_code','PEN','string','Código de moneda',1,1,'financial','2025-09-29 05:42:46','2025-09-29 05:42:46'),(8,'currency_symbol','S/.','string','Símbolo de moneda',1,1,'financial','2025-09-29 05:42:46','2025-09-29 05:42:46'),(9,'tax_rate','18.0','float','Tasa de impuestos (%)',1,1,'financial','2025-09-29 05:42:46','2025-09-29 05:42:46'),(10,'decimal_places','2','integer','Decimales para precios',1,1,'financial','2025-09-29 05:42:46','2025-09-29 05:42:46'),(11,'session_timeout','3600','integer','Tiempo de sesión en segundos',0,1,'security','2025-09-29 05:42:46','2025-09-29 05:42:46'),(12,'max_login_attempts','3','integer','Intentos máximos de login',0,1,'security','2025-09-29 05:42:46','2025-09-29 05:42:46'),(13,'backup_enabled','true','boolean','Backup automático habilitado',0,1,'system','2025-09-29 05:42:46','2025-09-29 05:42:46'),(14,'next_sale_number','1','integer','Próximo número de venta',0,0,'sales','2025-09-29 05:42:46','2025-09-29 05:42:46'),(15,'receipt_footer','Gracias por su compra','string','Pie de página del recibo',1,1,'sales','2025-09-29 05:42:46','2025-09-29 05:42:46'),(16,'system_initialized','true','boolean','Sistema inicializado',0,0,'system','2025-09-29 05:42:46','2025-09-29 05:42:46'),(17,'install_date','2025-09-29 00:42:46','string','Fecha de instalación',0,0,'system','2025-09-29 05:42:46','2025-09-29 05:42:46');
/*!40000 ALTER TABLE `system_config` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:03


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `test_connection`
--

DROP TABLE IF EXISTS `test_connection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_connection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_connection`
--

LOCK TABLES `test_connection` WRITE;
/*!40000 ALTER TABLE `test_connection` DISABLE KEYS */;
INSERT INTO `test_connection` VALUES (1,'Conexion MySQL exitosa','2025-09-29 06:05:23');
/*!40000 ALTER TABLE `test_connection` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:04


CREATE DATABASE  IF NOT EXISTS `pos_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pos_system`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pos_system
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Temporary view structure for view `sales_detail`
--

DROP TABLE IF EXISTS `sales_detail`;
/*!50001 DROP VIEW IF EXISTS `sales_detail`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `sales_detail` AS SELECT 
 1 AS `id`,
 1 AS `sale_number`,
 1 AS `sale_date`,
 1 AS `total_amount`,
 1 AS `status`,
 1 AS `payment_method`,
 1 AS `cashier_username`,
 1 AS `cashier_name`,
 1 AS `customer_name`,
 1 AS `customer_document`,
 1 AS `items_count`,
 1 AS `total_items_qty`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `sales_detail`
--

/*!50001 DROP VIEW IF EXISTS `sales_detail`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sales_detail` AS select `s`.`id` AS `id`,`s`.`sale_number` AS `sale_number`,`s`.`sale_date` AS `sale_date`,`s`.`total_amount` AS `total_amount`,`s`.`status` AS `status`,`s`.`payment_method` AS `payment_method`,`u`.`username` AS `cashier_username`,`u`.`full_name` AS `cashier_name`,coalesce(`c`.`name`,'Cliente Genérico') AS `customer_name`,coalesce(`c`.`document_number`,'00000000') AS `customer_document`,count(`si`.`id`) AS `items_count`,sum(`si`.`quantity`) AS `total_items_qty` from (((`sales` `s` join `users` `u` on((`s`.`user_id` = `u`.`id`))) left join `customers` `c` on((`s`.`customer_id` = `c`.`id`))) left join `sale_items` `si` on((`s`.`id` = `si`.`sale_id`))) group by `s`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Dumping events for database 'pos_system'
--

--
-- Dumping routines for database 'pos_system'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-02 17:24:05


