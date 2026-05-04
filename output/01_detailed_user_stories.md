Sebagai Senior Business Analyst, saya telah membedah PRD **Supplier License Management System (SLMS)** menjadi kumpulan *User Stories* yang detail dan teknis. Saya membagi pengerjaan ini berdasarkan prioritas MoSCoW untuk memastikan tim pengembang memiliki panduan yang jelas untuk setiap sprint.

Berikut adalah breakdown lengkap User Stories dan Acceptance Criteria (AC) dalam Bahasa Indonesia.

---

# 📋 User Stories & Acceptance Criteria: Supplier License Management System (SLMS)

## 🟢 PRIORITY 1: MUST HAVE (MVP)

### 1. Supplier Directory (Direktori Supplier)
**User Story 1.1: Menambah Supplier Baru**
*   **Sebagai** Procurement Officer, **saya ingin** dapat menambahkan data supplier baru ke dalam sistem, **sehingga** saya memiliki basis data supplier yang terpusat.
*   **Acceptance Criteria:**
    *   Sistem menyediakan form input dengan field: Nama Perusahaan (Wajib), Alamat (Wajib), Kontak Person (Wajib), Email Kontak (Wajib & validasi format email), dan Kategori Supplier (Dropdown).
    *   Sistem memberikan pesan sukses setelah data berhasil disimpan.
    *   Sistem memberikan pesan error jika ada field wajib yang kosong.

**User Story 1.2: Mengelola Data Supplier**
*   **Sebagai** Procurement Officer, **saya ingin** dapat melihat, mengedit, dan menghapus data supplier, **sehingga** informasi supplier tetap up-to-date.
*   **Acceptance Criteria:**
    *   Terdapat halaman daftar supplier dalam bentuk tabel yang menampilkan ringkasan informasi.
    *   User dapat mengklik tombol "Edit" untuk memperbarui informasi supplier.
    *   User dapat menghapus supplier (dengan konfirmasi pop-up sebelum eksekusi).
    *   Perubahan data tersimpan secara real-time di database.

---

### 2. License Repository (Repositori Lisensi)
**User Story 2.1: Mengunggah Dokumen Lisensi**
*   **Sebagai** Procurement Officer, **saya ingin** mengunggah file lisensi untuk supplier tertentu, **sehingga** dokumen tersimpan secara digital.
*   **Acceptance Criteria:**
    *   User dapat memilih supplier dari daftar sebelum mengunggah dokumen.
    *   Form upload mencakup field: Nama Lisensi (misal: SIUP, NIB), Nomor Lisensi (Wajib), Tanggal Terbit (Date Picker), dan Tanggal Kedaluwarsa (Date Picker).
    *   Sistem hanya menerima format file tertentu (misal: PDF, JPG, PNG) dengan batas ukuran maksimal 5MB.
    *   Sistem memvalidasi agar `expiry_date` tidak boleh lebih kecil dari tanggal hari ini.
    *   File tersimpan secara aman di Object Storage dan URL tersimpan di database.

---

### 3. Expiration Engine (Mesin Penghitung Kedaluwarsa)
**User Story 3.1: Perhitungan Sisa Hari Otomatis**
*   **Sebagai** Sistem, **saya ingin** menghitung selisih hari antara tanggal hari ini dan tanggal kedaluwarsa dokumen, **sehingga** status kepatuhan dapat ditentukan.
*   **Acceptance Criteria:**
    *   Sistem menjalankan logika pengurangan: `Sisa Hari = Tanggal Expired - Tanggal Hari Ini`.
    *   Jika `Sisa Hari < 0`, status otomatis menjadi **Expired**.
    *   Jika `Sisa Hari` berada dalam rentang 1-30 hari, status otomatis menjadi **Expiring Soon**.
    *   Jika `Sisa Hari > 30`, status otomatis menjadi **Active**.

---

### 4. Automated Notifications (Notifikasi Otomatis)
**User Story 4.1: Pengiriman Email Pengingat Berkala**
*   **Sebagai** Procurement Officer, **saya ingin** menerima email pengingat otomatis saat dokumen supplier mendekati tanggal expired, **sehingga** saya bisa segera meminta pembaruan.
*   **Acceptance Criteria:**
    *   Sistem menjalankan *Cron Job* setiap hari pukul 00:00.
    *   Email pengingat terkirim secara otomatis pada threshold: H-30, H-14, dan H-7 sebelum `expiry_date`.
    *   Isi email harus mencakup: Nama Supplier, Nama Lisensi, Tanggal Expired, dan Link menuju detail supplier di sistem.
    *   Sistem mencatat log pengiriman email (kapan dikirim dan ke siapa) dalam tabel `notification_logs`.

---

### 5. Compliance Dashboard (Dashboard Kepatuhan)
**User Story 5.1: Visualisasi Status Kepatuhan (Widget)**
*   **Sebagai** Vendor Manager/Compliance, **saya ingin** melihat ringkasan jumlah dokumen yang Aktif, Hampir Expired, dan Expired pada dashboard, **sehingga** saya bisa memantau risiko secara cepat.
*   **Acceptance Criteria:**
    *   Terdapat 3 widget kartu (Card) di halaman utama: "Active", "Expiring Soon", dan "Expired".
    *   Angka pada setiap widget harus sinkron secara real-time dengan data di database.
    *   Widget dapat diklik untuk mengarahkan user ke daftar detail dokumen dengan status tersebut.

---

## 🔵 PRIORITY 2: SHOULD HAVE (EFFICIENCY)

### 6. Document Versioning (Versi Dokumen)
**User Story 6.1: Riwayat Pembaruan Dokumen**
*   **Sebagai** Procurement Officer, **saya ingin** mengunggah versi baru dari dokumen lisensi tanpa menghapus versão lama, **sehingga** terdapat audit trail.
*   **Acceptance Criteria:**
    *   Saat user mengunggah dokumen baru untuk lisensi yang sama, dokumen sebelumnya otomatis ditandai sebagai `is_current = false`.
    *   Dokumen baru mendapatkan versi `n+1` dan ditandai sebagai `is_current = true`.
    *   Terdapat tab "History" pada detail supplier yang menampilkan daftar semua versi dokumen beserta tanggal upload-nya.

### 7. Advanced Search & Filter (Pencarian & Filter Lanjut)
**User Story 7.1: Pencarian dan Penyaringan Data**
*   **Sebagai** Procurement Officer, **saya ingin** mencari supplier atau dokumen berdasarkan kategori, status, atau rentang tanggal, **sehingga** saya menemukan data dengan lebih cepat.
*   **Acceptance Criteria:**
    *   Terdapat kolom pencarian yang mampu mencari berdasarkan Nama Supplier atau Nomor Lisensi.
    *   Filter dropdown tersedia untuk: Status (Active/Expiring Soon/Expired) dan Kategori Supplier.
    *   Filter rentang tanggal tersedia untuk mencari dokumen yang expired pada periode tertentu.
    *   Hasil pencarian harus muncul dalam waktu kurang dari 2 detik.

### 8. Basic Supplier Portal (Portal Mandiri Supplier)
**User Story 8.1: Upload Mandiri oleh Supplier**
*   **Sebagai** Supplier, **saya ingin** mengunggah dokumen lisensi terbaru saya sendiri, **sehingga** proses pembaruan dokumen lebih efisien.
*   **Acceptance Criteria:**
    *   Supplier memiliki login khusus dengan hak akses terbatas.
    *   Supplier hanya dapat melihat dan mengunggah dokumen milik perusahaannya sendiri (isolasi data).
    *   Setiap dokumen yang diunggah supplier akan masuk dalam status `Pending` (menunggu verifikasi admin).

### 9. Export Report (Ekspor Laporan)
**User Story 9.1: Ekspor Daftar Dokumen ke Format File**
*   **Sebagai** Compliance Officer, **saya ingin** mengekspor laporan dokumen yang akan/sudah expired ke Excel atau PDF, **sehingga** saya bisa melaporkannya dalam rapat manajemen.
*   **Acceptance Criteria:**
    *   Terdapat tombol "Export" pada halaman daftar dokumen.
    *   User dapat memilih format file (.xlsx atau .pdf).
    *   File hasil ekspor mengandung kolom: Nama Supplier, Nama Lisensi, No Lisensi, Tgl Expired, dan Status.

---

## 🟡 PRIORITY 3: COULD HAVE (SCALABILITY)

### 10. Approval Workflow (Alur Persetujuan)
**User Story 10.1: Verifikasi Dokumen oleh Legal/Manager**
*   **Sebagai** Legal/Manager, **saya ingin** memverifikasi dokumen yang baru diunggah sebelum statusnya menjadi Aktif, **sehingga** validitas dokumen terjamin.
*   **Acceptance Criteria:**
    *   Setiap dokumen baru memiliki status awal `Pending`.
    *   Legal/Manager menerima notifikasi adanya dokumen yang perlu diverifikasi.
    *   Terdapat aksi "Approve" (mengubah status ke `Active`) atau "Reject" (mengubah status ke `Rejected` dengan alasan penolakan).

### 11. ERP Integration (Integrasi ERP)
**User Story 11.1: Sinkronisasi Data Supplier via API**
*   **Sebagai** Administrator, **saya ingin** data supplier di SLMS tersinkronisasi secara otomatis dengan sistem ERP perusahaan, **sehingga** tidak ada redundansi input data.
*   **Acceptance Criteria:**
    *   Sistem menyediakan endpoint API untuk menerima data supplier dari ERP.
    *   Integrasi bekerja dua arah (sinkronisasi saat ada penambahan supplier baru di ERP).
    *   Terdapat log integrasi untuk memantau kegagalan atau keberhasilan sinkronisasi data.

### 12. Multi-channel Alert (Notifikasi Multi-Kanal)
**User Story 12.1: Notifikasi WhatsApp/Push Notification**
*   **Sebagai** Procurement Officer, **saya ingin** menerima pengingat via WhatsApp atau Push Notification di mobile, **sehingga** saya bisa merespons lebih cepat tanpa membuka email.
*   **Acceptance Criteria:**
    *   Sistem terintegrasi dengan WhatsApp Business API atau layanan Push Notification.
    *   Sistem mengirimkan pesan singkat berisi alert saat memasuki threshold H-14 dan H-7.
    *   User dapat memilih kanal notifikasi yang mereka inginkan melalui pengaturan profil.