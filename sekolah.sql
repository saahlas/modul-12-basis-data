-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2026 at 07:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sekolah`
--

-- --------------------------------------------------------

--
-- Table structure for table `guru`
--

CREATE TABLE `guru` (
  `NIP` varchar(10) NOT NULL,
  `nama_guru` varchar(100) DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `no_telepon` varchar(15) DEFAULT NULL,
  `status` enum('Tetap','Honorer') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guru`
--

INSERT INTO `guru` (`NIP`, `nama_guru`, `jenis_kelamin`, `no_telepon`, `status`) VALUES
('G001', 'Budi Santoso', 'L', '081234567890', 'Tetap'),
('G002', 'Siti Rahayu', 'P', '081234567891', 'Tetap'),
('G003', 'Ahmad Fauzi', 'L', '081234567892', 'Honorer'),
('G004', 'Dewi Lestari', 'P', '081234567893', 'Tetap'),
('G005', 'Eko Prasetyo', 'L', '081234567894', 'Honorer'),
('G006', 'Fitri Handayani', 'P', '081234567895', 'Tetap'),
('G007', 'Arfian Rafi', 'L', '081234567896', 'Tetap'),
('G008', 'Hana Pertiwi', 'P', '081234567897', 'Honorer'),
('G009', 'Irwan Kusuma', 'L', '081234567898', 'Tetap'),
('G010', 'Juliana Putri', 'P', '081234567899', 'Tetap'),
('G011', 'Kevin Aditya', 'L', '081234567800', 'Honorer'),
('G012', 'Lina Marlina', 'P', '081234567801', 'Tetap'),
('G013', 'Mario Teguh', 'L', '081234567802', 'Tetap'),
('G014', 'Nina Agustina', 'P', '081234567803', 'Honorer'),
('G015', 'Omar Bakri', 'L', '081234567804', 'Tetap'),
('G016', 'Raul Lazuardi', 'P', '0895323730137', 'Tetap');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id_jadwal` int(11) NOT NULL,
  `hari` enum('Senin','Selasa','Rabu','Kamis','Jumat') DEFAULT NULL,
  `jam_mulai` time DEFAULT NULL,
  `jam_selesai` time DEFAULT NULL,
  `NIP` varchar(10) DEFAULT NULL,
  `id_kelas` int(11) DEFAULT NULL,
  `id_mapel` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id_jadwal`, `hari`, `jam_mulai`, `jam_selesai`, `NIP`, `id_kelas`, `id_mapel`) VALUES
(1, 'Senin', '07:00:00', '08:30:00', 'G001', 1, 1),
(2, 'Senin', '08:30:00', '10:00:00', 'G002', 2, 2),
(3, 'Senin', '10:00:00', '11:30:00', 'G003', 3, 3),
(4, 'Selasa', '07:00:00', '08:30:00', 'G004', 4, 4),
(5, 'Selasa', '08:30:00', '10:00:00', 'G005', 5, 5),
(6, 'Selasa', '10:00:00', '11:30:00', 'G006', 6, 6),
(7, 'Rabu', '07:00:00', '08:30:00', 'G007', 1, 7),
(8, 'Rabu', '08:30:00', '10:00:00', 'G008', 2, 8),
(9, 'Rabu', '10:00:00', '11:30:00', 'G009', 3, 1),
(10, 'Kamis', '07:00:00', '08:30:00', 'G010', 4, 2),
(11, 'Kamis', '08:30:00', '10:00:00', 'G011', 5, 3),
(12, 'Kamis', '10:00:00', '11:30:00', 'G012', 6, 4),
(13, 'Jumat', '07:00:00', '08:30:00', 'G013', 1, 5),
(14, 'Jumat', '08:30:00', '10:00:00', 'G014', 2, 6),
(15, 'Jumat', '10:00:00', '11:30:00', 'G015', 3, 7);

-- --------------------------------------------------------

--
-- Table structure for table `kelas`
--

CREATE TABLE `kelas` (
  `id_kelas` int(11) NOT NULL,
  `nama_kelas` varchar(20) DEFAULT NULL,
  `tingkat` int(11) DEFAULT NULL,
  `tahun_ajaran` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kelas`
--

INSERT INTO `kelas` (`id_kelas`, `nama_kelas`, `tingkat`, `tahun_ajaran`) VALUES
(1, '10A', 10, '2024/2025'),
(2, '10B', 10, '2024/2025'),
(3, '11A', 11, '2024/2025'),
(4, '11B', 11, '2024/2025'),
(5, '12A', 12, '2024/2025'),
(6, '12B', 12, '2024/2025');

-- --------------------------------------------------------

--
-- Table structure for table `mata_pelajaran`
--

CREATE TABLE `mata_pelajaran` (
  `id_mapel` int(11) NOT NULL,
  `nama_mapel` varchar(100) DEFAULT NULL,
  `jumlah_jam` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mata_pelajaran`
--

INSERT INTO `mata_pelajaran` (`id_mapel`, `nama_mapel`, `jumlah_jam`) VALUES
(1, 'Matematika', 4),
(2, 'Bahasa Indonesia', 4),
(3, 'Bahasa Inggris', 3),
(4, 'IPA', 4),
(5, 'IPS', 3),
(6, 'Fisika', 3),
(7, 'Kimia', 3),
(8, 'Biologi', 3),
(9, 'PJOK', 3);

-- --------------------------------------------------------

--
-- Table structure for table `siswa`
--

CREATE TABLE `siswa` (
  `NIS` varchar(10) NOT NULL,
  `nama_siswa` varchar(100) DEFAULT NULL,
  `jenis_kelamin` enum('L','P') DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `id_kelas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `siswa`
--

INSERT INTO `siswa` (`NIS`, `nama_siswa`, `jenis_kelamin`, `tanggal_lahir`, `alamat`, `id_kelas`) VALUES
('S001', 'Andi Wijaya', 'L', '2007-03-15', 'Jl. Merdeka No.1', 1),
('S002', 'Bella Safitri', 'P', '2007-05-20', 'Jl. Mawar No.2', 1),
('S003', 'Candra Putra', 'L', '2007-07-10', 'Jl. Melati No.3', 2),
('S004', 'Diana Sari', 'P', '2007-09-25', 'Jl. Anggrek No.4', 2),
('S005', 'Eka Saputra', 'L', '2006-01-12', 'Jl. Kenanga No.5', 3),
('S006', 'Fani Oktavia', 'P', '2006-04-18', 'Jl. Dahlia No.6', 3),
('S007', 'Gilang Ramadan', 'L', '2006-06-30', 'Jl. Flamboyan No.7', 4),
('S008', 'Hesti Wulandari', 'P', '2006-08-14', 'Jl. Kamboja No.8', 4),
('S009', 'Ivan Setiawan', 'L', '2005-02-22', 'Jl. Sakura No.9', 5),
('S010', 'Jeni Ratnasari', 'P', '2005-11-05', 'Jl. Tulip No.10', 5),
('S011', 'Kiki Amalia', 'P', '2005-03-17', 'Jl. Lotus No.11', 6),
('S013', 'Maya Sari', 'P', '2007-12-01', 'Jl. Bougenville No.13', 1),
('S014', 'Nando Pratama', 'L', '2006-10-09', 'Jl. Cempaka No.14', 3),
('S015', 'Olivia Susanti', 'P', '2005-08-23', 'Jl. Seruni No.15', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `guru`
--
ALTER TABLE `guru`
  ADD PRIMARY KEY (`NIP`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id_jadwal`),
  ADD KEY `NIP` (`NIP`),
  ADD KEY `id_kelas` (`id_kelas`),
  ADD KEY `id_mapel` (`id_mapel`);

--
-- Indexes for table `kelas`
--
ALTER TABLE `kelas`
  ADD PRIMARY KEY (`id_kelas`);

--
-- Indexes for table `mata_pelajaran`
--
ALTER TABLE `mata_pelajaran`
  ADD PRIMARY KEY (`id_mapel`);

--
-- Indexes for table `siswa`
--
ALTER TABLE `siswa`
  ADD PRIMARY KEY (`NIS`),
  ADD KEY `id_kelas` (`id_kelas`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id_jadwal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `kelas`
--
ALTER TABLE `kelas`
  MODIFY `id_kelas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `mata_pelajaran`
--
ALTER TABLE `mata_pelajaran`
  MODIFY `id_mapel` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`NIP`) REFERENCES `guru` (`NIP`) ON UPDATE CASCADE,
  ADD CONSTRAINT `jadwal_ibfk_2` FOREIGN KEY (`id_kelas`) REFERENCES `kelas` (`id_kelas`) ON UPDATE CASCADE,
  ADD CONSTRAINT `jadwal_ibfk_3` FOREIGN KEY (`id_mapel`) REFERENCES `mata_pelajaran` (`id_mapel`) ON UPDATE CASCADE;

--
-- Constraints for table `siswa`
--
ALTER TABLE `siswa`
  ADD CONSTRAINT `siswa_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `kelas` (`id_kelas`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
