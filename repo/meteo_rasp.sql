-- phpMyAdmin SQL Dump
-- version 4.7.9
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  mer. 10 avr. 2019 à 08:56
-- Version du serveur :  5.7.21
-- Version de PHP :  7.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `meteo_rasp`
--
DROP DATABASE `meteo_rasp`;
CREATE DATABASE IF NOT EXISTS `meteo_rasp` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `meteo_rasp`;

-- --------------------------------------------------------

--
-- Structure de la table `caption`
--

DROP TABLE IF EXISTS `caption`;
CREATE TABLE IF NOT EXISTS `caption` (
  `mac_address` varchar(17) NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`mac_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `caption`
--

INSERT INTO `caption` (`mac_address`, `name`) VALUES
('d6:c6:c7:39:a2:e8', 'interne'),
('d7:ef:13:27:15:29', 'externe'),
('f3:43:ad:d9:8F:5f', 'Jardin');

-- --------------------------------------------------------

--
-- Structure de la table `collect`
--

DROP TABLE IF EXISTS `collect`;
CREATE TABLE IF NOT EXISTS `collect` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  `id_data` int(11) NOT NULL,
  `mac_address` varchar(17) NOT NULL,
  `date` datetime NOT NULL,
  `value` decimal(10,0) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `collect_caption0_FK` (`mac_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `contact`
--

DROP TABLE IF EXISTS `contact`;
CREATE TABLE IF NOT EXISTS `contact` (
  `address` varchar(50) NOT NULL,
  `firstname` varchar(20) NOT NULL,
  `lastname` varchar(20) NOT NULL,
  PRIMARY KEY (`address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `contact`
--

INSERT INTO `contact` (`address`, `firstname`, `lastname`) VALUES
('contact1@gmail.com', 'Prénom1', 'Nom1'),
('contact2@gmail.com', 'Prénom2', 'Nom2'),
('contact3@gmail.com', 'Prénom3', 'Nom3');

-- --------------------------------------------------------

--
-- Structure de la table `data`
--

DROP TABLE IF EXISTS `data`;
CREATE TABLE IF NOT EXISTS `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `unit` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `data`
--

INSERT INTO `data` (`id`, `name`, `unit`) VALUES
(1, 'Température', '°'),
(2, 'Humidité', '%');

-- --------------------------------------------------------

--
-- Structure de la table `recipient`
--

DROP TABLE IF EXISTS `recipient`;
CREATE TABLE IF NOT EXISTS `recipient` (
  `address` varchar(50) NOT NULL,
  `id_threshold` int(11) NOT NULL,
  PRIMARY KEY (`address`,`id_threshold`),
  KEY `recipient_threshold0_FK` (`id_threshold`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `threshold`
--

DROP TABLE IF EXISTS `threshold`;
CREATE TABLE IF NOT EXISTS `threshold` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` decimal(10,0) NOT NULL,
  `higher` tinyint(1) NOT NULL,
  `last_date` datetime DEFAULT NULL,
  `frequency` int(11) NOT NULL,
  `id_Data` int(11) NOT NULL,
  `mac_address` varchar(17) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `threshold_Data_FK` (`id_Data`),
  KEY `threshold_caption0_FK` (`mac_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `collect`
--
ALTER TABLE `collect`
  ADD CONSTRAINT `collect_Data_FK` FOREIGN KEY (`id_data`) REFERENCES `data` (`id`),
  ADD CONSTRAINT `collect_caption0_FK` FOREIGN KEY (`mac_address`) REFERENCES `caption` (`mac_address`);

--
-- Contraintes pour la table `recipient`
--
ALTER TABLE `recipient`
  ADD CONSTRAINT `recipient_contact_FK` FOREIGN KEY (`address`) REFERENCES `contact` (`address`),
  ADD CONSTRAINT `recipient_threshold0_FK` FOREIGN KEY (`id_threshold`) REFERENCES `threshold` (`id`);

--
-- Contraintes pour la table `threshold`
--
ALTER TABLE `threshold`
  ADD CONSTRAINT `threshold_Data_FK` FOREIGN KEY (`id_Data`) REFERENCES `data` (`id`),
  ADD CONSTRAINT `threshold_caption0_FK` FOREIGN KEY (`mac_address`) REFERENCES `caption` (`mac_address`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
