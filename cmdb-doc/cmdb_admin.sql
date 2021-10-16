-- MySQL dump 10.14  Distrib 5.5.64-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: cmdb_admin
-- ------------------------------------------------------
-- Server version	5.7.29

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
-- Table structure for table `mg_app_settings`
--

DROP TABLE IF EXISTS `mg_app_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_app_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_app_settings`
--

LOCK TABLES `mg_app_settings` WRITE;
/*!40000 ALTER TABLE `mg_app_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `mg_app_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_components`
--

DROP TABLE IF EXISTS `mg_components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_components` (
  `comp_id` int(11) NOT NULL AUTO_INCREMENT,
  `component_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`comp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_components`
--

LOCK TABLES `mg_components` WRITE;
/*!40000 ALTER TABLE `mg_components` DISABLE KEYS */;
INSERT INTO `mg_components` VALUES (2,'edit_button','0'),(3,'publish_button','0'),(8,'reset_mfa_btn','0'),(9,'reset_pwd_btn','0'),(10,'new_user_btn','0'),(12,'get_token_btn','0'),(13,'web_ssh_btn','0'),(14,'asset_error_log','0');
/*!40000 ALTER TABLE `mg_components` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_functions`
--

DROP TABLE IF EXISTS `mg_functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_functions` (
  `func_id` int(11) NOT NULL AUTO_INCREMENT,
  `func_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uri` varchar(300) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `method_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`func_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_functions`
--

LOCK TABLES `mg_functions` WRITE;
/*!40000 ALTER TABLE `mg_functions` DISABLE KEYS */;
INSERT INTO `mg_functions` VALUES (6,'ss','/login/','ALL','10','2018-03-21 10:29:14','2018-03-20 18:35:24'),(9,'管理员','/','ALL','0','2018-03-21 14:04:59','2018-03-21 14:04:59'),(10,'任务管理员','/task/v2/task/','ALL','0','2019-03-21 10:57:54','2018-03-22 10:09:10'),(12,'修改密码','/mg/v2/accounts/password/','PATCH','0','2019-03-21 11:07:20','2018-03-22 16:27:12');
/*!40000 ALTER TABLE `mg_functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_menus`
--

DROP TABLE IF EXISTS `mg_menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_menus` (
  `menu_id` int(11) NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_menus`
--

LOCK TABLES `mg_menus` WRITE;
/*!40000 ALTER TABLE `mg_menus` DISABLE KEYS */;
INSERT INTO `mg_menus` VALUES (1,'home','0'),(2,'_home','0'),(3,'components','0'),(4,'count_to_page','0'),(5,'tables_page','0'),(6,'usermanage','0'),(7,'user','0'),(8,'role','0'),(9,'functions','0'),(10,'menus','0'),(12,'systemmanage','0'),(13,'system','0'),(14,'systemlog','0'),(18,'cron','0'),(19,'cronjobs','0'),(20,'cronlogs','0'),(22,'task_layout','0'),(23,'commandlist','0'),(24,'argslist','0'),(25,'templist','0'),(26,'order','0'),(27,'taskOrderList','0'),(28,'taskuser','0'),(29,'operation_center','0'),(32,'mysqlAudit','0'),(33,'publishApp','0'),(34,'mysqlOptimize','0'),(35,'resourceApplication','0'),(37,'customTasks','0'),(38,'publishConfig','0'),(39,'codeRepository','0'),(40,'dockerRegistry','0'),(41,'cmdb','0'),(42,'asset_server','0'),(43,'log_audit','0'),(46,'tag_mg','20'),(47,'admin_user','20'),(50,'k8s','20'),(51,'project','20'),(52,'app','20'),(53,'project_publish','20'),(54,'publish_list','0'),(55,'statisticaldata','0'),(56,'statisticalImage','0'),(57,'historyTaskList','0'),(58,'asset_db','0'),(59,'config_center','0'),(60,'project_config_list','0'),(61,'my_config_list','0'),(62,'confd','0'),(63,'confd_project','0'),(64,'confd_config','0'),(65,'devopstools','0'),(66,'prometheus_alert','0'),(68,'tagTree','0'),(69,'event_manager','0'),(70,'password_mycrypy','0'),(72,'proxyInfo','0'),(73,'paid_reminder','0'),(74,'project_manager','0'),(75,'postTasks','0'),(76,'taskCenter','0'),(77,'fault_manager','0'),(78,'assetPurchase','0'),(79,'nodeAdd','0'),(80,'customTasksProxy','0'),(85,'web_ssh','0'),(87,'tag_mg','0'),(88,'assetPurchaseALY','0'),(89,'assetPurchaseAWS','0'),(90,'assetPurchaseQcloud','0'),(91,'domain','0'),(92,'domain_name_manage','0'),(93,'domain_name_monitor','0'),(94,'system_user','0'),(95,'asset_config','0');
/*!40000 ALTER TABLE `mg_menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_role_functions`
--

DROP TABLE IF EXISTS `mg_role_functions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_role_functions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `func_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_role_functions`
--

LOCK TABLES `mg_role_functions` WRITE;
/*!40000 ALTER TABLE `mg_role_functions` DISABLE KEYS */;
/*!40000 ALTER TABLE `mg_role_functions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_role_menus`
--

DROP TABLE IF EXISTS `mg_role_menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_role_menus` (
  `role_menu_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `menu_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`role_menu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_role_menus`
--

LOCK TABLES `mg_role_menus` WRITE;
/*!40000 ALTER TABLE `mg_role_menus` DISABLE KEYS */;
/*!40000 ALTER TABLE `mg_role_menus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_roles`
--

DROP TABLE IF EXISTS `mg_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_roles` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_roles`
--

LOCK TABLES `mg_roles` WRITE;
/*!40000 ALTER TABLE `mg_roles` DISABLE KEYS */;
INSERT INTO `mg_roles` VALUES (1,'woshiceshi','0','2020-03-28 10:37:18');
/*!40000 ALTER TABLE `mg_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_roles_components`
--

DROP TABLE IF EXISTS `mg_roles_components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_roles_components` (
  `role_comp_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comp_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`role_comp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_roles_components`
--

LOCK TABLES `mg_roles_components` WRITE;
/*!40000 ALTER TABLE `mg_roles_components` DISABLE KEYS */;
/*!40000 ALTER TABLE `mg_roles_components` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_user_roles`
--

DROP TABLE IF EXISTS `mg_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_user_roles` (
  `user_role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `utime` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`user_role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_user_roles`
--

LOCK TABLES `mg_user_roles` WRITE;
/*!40000 ALTER TABLE `mg_user_roles` DISABLE KEYS */;
INSERT INTO `mg_user_roles` VALUES (1,'1','2','0','2020-03-28 10:39:55','2020-03-28 10:39:55');
/*!40000 ALTER TABLE `mg_user_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mg_users`
--

DROP TABLE IF EXISTS `mg_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mg_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nickname` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tel` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `wechat` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `no` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `department` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `google_key` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `superuser` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_ip` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mg_users`
--

LOCK TABLES `mg_users` WRITE;
/*!40000 ALTER TABLE `mg_users` DISABLE KEYS */;
INSERT INTO `mg_users` VALUES (1,'admin','c6e0c179f26c124aeaac84bf4a10da59','admin','111111@qq.com','11111111111','','','admin','','0','0','172.21.0.42','2020-03-28 17:43:26','2020-01-01 00:00:00'),(2,'jianxlin','5fc372e8e14a66041bc230ad14672995','jianxlin','linjianxing321@163.com','13333333333','123','111','op','OFTU4UTVIJXFUVT2KBCE22S2GVTHI5BYMRCVSYSTJVBGSY2RKE3WQM2F','10','0','','2020-03-28 12:42:31','2020-03-28 10:38:41');
/*!40000 ALTER TABLE `mg_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_record`
--

DROP TABLE IF EXISTS `operation_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operation_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nickname` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `login_ip` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `method` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uri` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `data` text COLLATE utf8mb4_unicode_ci,
  `ctime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_record`
--

LOCK TABLES `operation_record` WRITE;
/*!40000 ALTER TABLE `operation_record` DISABLE KEYS */;
INSERT INTO `operation_record` VALUES (1,'admin','admin','172.21.0.42','PATCH','/api/mg/v2/accounts/menus/','{\"menu_id\":47}','2020-03-28 10:35:46'),(2,'admin','admin','172.21.0.42','PATCH','/api/mg/v2/accounts/menus/','{\"menu_id\":46}','2020-03-28 10:35:46'),(3,'admin','admin','172.21.0.42','PATCH','/api/mg/v2/accounts/menus/','{\"menu_id\":53}','2020-03-28 10:35:48'),(4,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":16}','2020-03-28 10:35:54'),(5,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":33}','2020-03-28 10:35:56'),(6,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":35}','2020-03-28 10:35:56'),(7,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":36}','2020-03-28 10:35:57'),(8,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":37}','2020-03-28 10:35:57'),(9,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":38}','2020-03-28 10:35:57'),(10,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":39}','2020-03-28 10:35:58'),(11,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":40}','2020-03-28 10:35:58'),(12,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":42}','2020-03-28 10:35:58'),(13,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":43}','2020-03-28 10:35:59'),(14,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":44}','2020-03-28 10:35:59'),(15,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":15}','2020-03-28 10:36:06'),(16,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":45}','2020-03-28 10:36:07'),(17,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":46}','2020-03-28 10:36:07'),(18,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":47}','2020-03-28 10:36:08'),(19,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":48}','2020-03-28 10:36:08'),(20,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":49}','2020-03-28 10:36:08'),(21,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":50}','2020-03-28 10:36:08'),(22,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":51}','2020-03-28 10:36:09'),(23,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":52}','2020-03-28 10:36:09'),(24,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":53}','2020-03-28 10:36:10'),(25,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":54}','2020-03-28 10:36:10'),(26,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":55}','2020-03-28 10:36:11'),(27,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":56}','2020-03-28 10:36:16'),(28,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":57}','2020-03-28 10:36:17'),(29,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":59}','2020-03-28 10:36:17'),(30,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":60}','2020-03-28 10:36:18'),(31,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":61}','2020-03-28 10:36:18'),(32,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":62}','2020-03-28 10:36:18'),(33,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":63}','2020-03-28 10:36:19'),(34,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":64}','2020-03-28 10:36:19'),(35,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":65}','2020-03-28 10:36:19'),(36,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":66}','2020-03-28 10:36:20'),(37,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":67}','2020-03-28 10:36:20'),(38,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":68}','2020-03-28 10:36:20'),(39,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":69}','2020-03-28 10:36:25'),(40,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":70}','2020-03-28 10:36:25'),(41,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":71}','2020-03-28 10:36:26'),(42,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":72}','2020-03-28 10:36:26'),(43,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":73}','2020-03-28 10:36:26'),(44,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":74}','2020-03-28 10:36:26'),(45,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":75}','2020-03-28 10:36:27'),(46,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":75}','2020-03-28 10:36:27'),(47,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":77}','2020-03-28 10:36:28'),(48,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":78}','2020-03-28 10:36:28'),(49,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":79}','2020-03-28 10:36:28'),(50,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":80}','2020-03-28 10:36:29'),(51,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":76}','2020-03-28 10:36:33'),(52,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":81}','2020-03-28 10:36:33'),(53,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":82}','2020-03-28 10:36:34'),(54,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":83}','2020-03-28 10:36:34'),(55,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":84}','2020-03-28 10:36:34'),(56,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":85}','2020-03-28 10:36:34'),(57,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":86}','2020-03-28 10:36:35'),(58,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":87}','2020-03-28 10:36:35'),(59,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":88}','2020-03-28 10:36:35'),(60,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":89}','2020-03-28 10:36:35'),(61,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":89}','2020-03-28 10:36:36'),(62,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":91}','2020-03-28 10:36:36'),(63,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":90}','2020-03-28 10:36:44'),(64,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":92}','2020-03-28 10:36:44'),(65,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":93}','2020-03-28 10:36:45'),(66,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":94}','2020-03-28 10:36:45'),(67,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":95}','2020-03-28 10:36:45'),(68,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":96}','2020-03-28 10:36:45'),(69,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":97}','2020-03-28 10:36:46'),(70,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":98}','2020-03-28 10:36:46'),(71,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":99}','2020-03-28 10:36:46'),(72,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":99}','2020-03-28 10:36:47'),(73,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":101}','2020-03-28 10:36:48'),(74,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":102}','2020-03-28 10:36:48'),(75,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":100}','2020-03-28 10:36:55'),(76,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":103}','2020-03-28 10:36:55'),(77,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":104}','2020-03-28 10:36:56'),(78,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":105}','2020-03-28 10:36:56'),(79,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":106}','2020-03-28 10:36:56'),(80,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":107}','2020-03-28 10:36:57'),(81,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":108}','2020-03-28 10:36:57'),(82,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/func/','{\"func_id\":109}','2020-03-28 10:36:58'),(83,'admin','admin','172.21.0.42','POST','/api/mg/v2/accounts/role/','{\"role_name\":\"woshiceshi\"}','2020-03-28 10:37:17'),(84,'admin','admin','172.21.0.42','POST','/api/mg/v2/accounts/menus/','{\"menu_id\":\"\",\"menu_name\":\"aaa\"}','2020-03-28 10:37:39'),(85,'admin','admin','172.21.0.42','DELETE','/api/mg/v2/accounts/menus/','{\"menu_id\":96}','2020-03-28 10:37:47'),(86,'admin','admin','172.21.0.42','POST','/api/mg/v2/accounts/user/','{\"username\":\"jianxlin\",\"nickname\":\"jianxlin\",\"department\":\"op\",\"wechat\":\"123\",\"tel\":\"13333333333\",\"no\":\"111\",\"email\":\"clayvill@amozon.com\"}','2020-03-28 10:38:41'),(87,'admin','admin','172.21.0.42','PATCH','/api/mg/v2/accounts/user/','{\"user_id\":2,\"key\":\"status\"}','2020-03-28 10:38:47'),(88,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_mfa/','{\"user_list\":[2]}','2020-03-28 10:39:12'),(89,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/components/','{\"comp_id\":14,\"component_name\":\"asset_error_log\"}','2020-03-28 10:39:43'),(90,'admin','admin','172.21.0.42','POST','/api/mg/v2/accounts/role_user/','{\"role_id\":1,\"user_list\":[\"2\"]}','2020-03-28 10:39:55'),(91,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 10:40:33'),(92,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/user/','{\"user_id\":2,\"key\":\"email\",\"value\":\"linjianxing321@163.com\"}','2020-03-28 10:40:50'),(93,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 10:41:03'),(94,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_mfa/','{\"user_list\":[2]}','2020-03-28 10:43:50'),(95,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 10:53:57'),(96,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:18:38'),(97,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:20:23'),(98,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:21:41'),(99,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_mfa/','{\"user_list\":[2]}','2020-03-28 12:21:43'),(100,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:23:15'),(101,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:26:03'),(102,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:26:24'),(103,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:26:43'),(104,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:27:03'),(105,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:29:42'),(106,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_pw/','{\"user_list\":[2]}','2020-03-28 12:42:16'),(107,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/reset_mfa/','{\"user_list\":[2]}','2020-03-28 12:42:30'),(108,'admin','admin','172.21.0.42','PUT','/api/mg/v2/accounts/token/','{\"user_list\":[2]}','2020-03-28 12:42:44'),(109,'admin','admin','172.21.0.42','POST','/api/cmdb2/v1/cmdb/ebs/','','2020-03-28 12:43:19'),(110,'admin','admin','172.21.0.42','POST','/api/save_error_logger','{\"type\":\"script\",\"code\":0,\"mes\":\"this.getRiskyServerList is not a function\",\"url\":\"http://127.0.0.1:8080/cmdb/risky_server\"}','2020-03-28 12:44:36'),(111,'admin','admin','172.21.0.42','POST','/api/save_error_logger','{\"type\":\"script\",\"code\":0,\"mes\":\"this.getRiskyServerList is not a function\",\"url\":\"http://127.0.0.1:8080/cmdb/risky_server\"}','2020-03-28 12:44:37'),(112,'admin','admin','172.21.0.42','POST','/api/save_error_logger','{\"type\":\"script\",\"code\":0,\"mes\":\"this.getRiskyServerList is not a function\",\"url\":\"http://127.0.0.1:8080/cmdb/risky_server\"}','2020-03-28 12:44:38'),(113,'admin','admin','172.21.0.42','POST','/api/cmdb2/v1/cmdb/ebs/','','2020-03-28 12:44:42'),(114,'admin','admin','172.21.0.42','POST','/api/cmdb2/v1/cmdb/ebs/','','2020-03-28 12:44:43'),(115,'admin','admin','172.21.0.42','POST','/api/cmdb2/v1/cmdb/ebs/','','2020-03-28 12:44:43'),(116,'admin','admin','172.21.0.42','POST','/api/cmdb2/v1/cmdb/ebs/','','2020-03-28 13:23:57');
/*!40000 ALTER TABLE `operation_record` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-28  9:50:07
