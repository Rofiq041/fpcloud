-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 04 Des 2024 pada 03.42
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_merek`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `akun`
--

CREATE TABLE `akun` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `akun`
--

INSERT INTO `akun` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin123', 'admin'),
(2, 'user', 'user', 'user'),
(4, 'irul123', 'irul123', 'user'),
(5, 'rofiq123', 'rofiq123', 'user');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat`
--

CREATE TABLE `chat` (
  `id` int(11) NOT NULL,
  `id_pengirim` int(11) NOT NULL,
  `id_penerima` int(11) NOT NULL,
  `pesan` text NOT NULL,
  `waktu` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `db_mobil`
--

CREATE TABLE `db_mobil` (
  `id_mobil` int(11) NOT NULL,
  `nama_mobil` varchar(255) NOT NULL,
  `warna` varchar(50) NOT NULL,
  `merek` varchar(100) NOT NULL,
  `tipe` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `harga` bigint(20) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `db_mobil`
--

INSERT INTO `db_mobil` (`id_mobil`, `nama_mobil`, `warna`, `merek`, `tipe`, `deskripsi`, `harga`, `image_url`) VALUES
(9, 'BYD Seal R Long Range', 'Mid Blue Sea', 'BYD', 'Perfomance AWD 670km Range', 'Mobil Listrik dengan jarak tempuh yang jauh dalam sekali pengecasan, dan dibekali meson 4 motor 1000hp', 719300000, 'https://static.motor.es/fotos-jato/byd/uploads/byd-seal-6441b4e361e74.jpg'),
(11, 'New Tesla Roadster', 'RED Majic', 'Tesla', 'Super Perfomance Longrange', 'Mobil listrik dengan desain futuristik yang dibekali mesin motor masing masing 1000hp dengan sensasi jambakan setan', 3349500000, 'https://th.bing.com/th/id/OIP.2uQpWB8EMpgac9RTOqy0eQAAAA?w=474&h=266&rs=1&pid=ImgDetMain'),
(12, 'Toyota Camry', 'Hitam', 'Toyota', '2.8 M/T hybird Keyless', 'Mobil Nyaman Semi Elektrik yang Terkesan Luxury Design ', 657600000, 'https://gambarmobil.com/foto/toyota/317194-camry-2-5-v-a-t-2015-facelift-hitam-record-toyota-photo-26-08-22-14-18-48.jpg'),
(13, 'Ford Ranger 4x4 2020', 'Putih', 'Ford', '2.5 A/T 4x4 Double Cab', 'Mobil Multifungsi yang bisa diandalkan untuk mengangkut barang dan bermain', 865000000, 'https://resource.digitaldealer.com.au/image/71480996865437a47ef360029681485_0_0-c.jpg'),
(14, 'Toyota Land Cruiser 300 VXR', 'Silver', 'Toyota', '3.2 Triptonic Transmision', 'Mobil Mewah dengan Fitur yang sangan lengkap dan dibekali Patwal perjalanan', 2547000000, 'https://i.pinimg.com/originals/62/a2/10/62a2106589c6679b0c733f5bd447ded2.jpg'),
(15, 'Honda CRV Turbo', 'Grey', 'Honda', '2,5 Turbo A/T', 'Mobil keluarga dengan 7Seat dan pengalaman menyetir yang menajubkan', 725000000, 'https://hondaengineinfo.com/wp-content/uploads/2022/11/Honda-CRV-2024-Exterior.png'),
(16, 'Mazda 3 Hatchback 2024', 'Grey', 'Mazda', '1,5 A/T Hatchback', 'Mobil dengan Gaya kekinian Menawarkan Fitur sensasi Balap yang nyata bagi pengendara', 573500000, 'https://images.carexpert.com.au/resize/3000/-/app/uploads/2021/09/2022-Mazda-3-G20-Evolve-SP-HERO.jpg'),
(17, 'Suzuki Grand Vitara', 'Blue', 'Suzuki', '2.0 M/T 7 Seater', 'Mobil Semi SUV yang menawarkan Pengalaman Mengendarai yang menajubkan', 351000000, 'https://th.bing.com/th/id/OIP.zo-hiXPKl8q-xKFcwWd7gwHaEJ?w=750&h=420&rs=1&pid=ImgDetMain'),
(18, 'Chevrolet Trailblazer 4x4', 'Kuning', 'Chevrolet', '2.5 A/T 4x4 Diesel', 'Mobil SUV yang Gemar Offroan dan dapat mudah melewati jalan terjal', 472500000, 'https://www.elcarrocolombiano.com/wp-content/uploads/2023/01/20230124-CHEVROLET-TRAILBLAZER-2024-PORTADA-750x460.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `forum_messages`
--

CREATE TABLE `forum_messages` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `pesan` text NOT NULL,
  `role_pengirim` enum('user','admin') NOT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `forum_messages`
--

INSERT INTO `forum_messages` (`id`, `username`, `pesan`, `role_pengirim`, `tanggal`) VALUES
(1, 'admin', 'Selamat datang di forum diskusi!', 'admin', '2024-12-02 09:58:35'),
(2, 'user', 'Terima kasih, admin! Saya ingin bertanya tentang produk ini.', 'user', '2024-12-02 09:58:35');

-- --------------------------------------------------------

--
-- Struktur dari tabel `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'aku123', 'aku123');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `akun`
--
ALTER TABLE `akun`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_pengirim` (`id_pengirim`),
  ADD KEY `id_penerima` (`id_penerima`);

--
-- Indeks untuk tabel `db_mobil`
--
ALTER TABLE `db_mobil`
  ADD PRIMARY KEY (`id_mobil`);

--
-- Indeks untuk tabel `forum_messages`
--
ALTER TABLE `forum_messages`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `akun`
--
ALTER TABLE `akun`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `db_mobil`
--
ALTER TABLE `db_mobil`
  MODIFY `id_mobil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT untuk tabel `forum_messages`
--
ALTER TABLE `forum_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`id_pengirim`) REFERENCES `akun` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`id_penerima`) REFERENCES `akun` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
