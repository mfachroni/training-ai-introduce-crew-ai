Sebagai Senior System Architect, saya telah menganalisis PRD tersebut. Sistem ini membutuhkan reliabilitas tinggi pada bagian *scheduler* (untuk pengecekan kedaluwarsa) dan keamanan penyimpanan dokumen.

Berikut adalah **Dokumen Arsitektur Teknis dan Desain Database** untuk Sistem Monitoring Dokumen Supplier.

---

# Dokumen Arsitektur Teknis: Sistem Monitoring Dokumen Supplier

## 1. High-Level Architecture (Arsitektur Tingkat Tinggi)

Sistem akan mengadopsi arsitektur **Client-Server** dengan pendekatan **API-First**. Laravel akan bertindak sebagai *Backend Engine* dan *Admin Panel*, sementara Flutter akan bertindak sebagai *Mobile Client* untuk monitoring cepat dan notifikasi.

### Komponen Utama:
*   **Backend (Laravel 10/11):**
    *   **RESTful API:** Menyediakan endpoint untuk aplikasi Flutter.
    *   **Web Admin Dashboard:** Portal manajemen utama untuk Staff Procurement dan Manager.
    *   **Task Scheduler:** Menggunakan *Laravel Scheduler* untuk memindai dokumen yang akan kedaluwarsa setiap hari.
    *   **Notification Engine:** Integrasi dengan SMTP Email dan Push Notifications (FCM).
*   **Mobile App (Flutter):**
    *   **Dashboard Viewer:** Visualisasi status dokumen untuk Manager.
    *   **Notification Center:** Menerima alert *real-time*.
    *   **Document Previewer:** Melihat dokumen PDF/JPG secara cepat.
*   **Infrastructure:**
    *   **Web Server:** Nginx/Apache.
    *   **Database:** PostgreSQL (Disarankan untuk integritas data yang lebih baik).
    *   **File Storage:** AWS S3 atau Local Secure Storage (untuk penyimpanan file dokumen).
    *   **Cache/Queue:** Redis (untuk menangani antrian pengiriman email massal agar tidak terjadi *timeout*).

### Diagram Alur Infrastruktur (Deskriptif):
`User (Web/Mobile)` $\rightarrow$ `Load Balancer/Nginx` $\rightarrow$ `Laravel Application` $\rightarrow$ `Redis (Queue)` $\rightarrow$ `SMTP Mail Server`
$\downarrow$
`Laravel Application` $\leftrightarrow$ `PostgreSQL Database` $\leftrightarrow$ `S3 Bucket (Storage Dokumen)`

---

## 2. Desain Database (Database Schema)

Saya menggunakan pendekatan relasional untuk menjamin konsistensi data (*Strong Consistency*).

### A. Tabel User & Akses
*   **`users`**: Menyimpan data pengguna sistem.
    *   `id` (PK), `username`, `password`, `email`, `full_name`, `role` (enum: admin, staff, manager, audit), `created_at`, `updated_at`.

### B. Tabel Inti (Core)
*   **`suppliers`**: Data profil supplier.
    *   `id` (PK), `company_name` (string), `address` (text), `category_id` (FK), `pic_name` (string), `pic_contact` (string), `status` (active/inactive), `created_at`, `updated_at`.
*   **`supplier_categories`**: Kategori supplier (misal: Konstruksi, IT, Alat Tulis).
    *   `id` (PK), `category_name` (string).
*   **`document_types`**: Katalog jenis dokumen.
    *   `id` (PK), `document_name` (string), `default_validity_days` (int), `is_mandatory` (boolean).

### C. Tabel Manajemen Dokumen
*   **`supplier_documents`**: Menghubungkan supplier dengan dokumen yang mereka miliki.
    *   `id` (PK), `supplier_id` (FK), `document_type_id` (FK), `file_path` (string), `issue_date` (date), `expiry_date` (date), `uploaded_by` (FK $\rightarrow$ users), `status` (enum: valid, warning, expired), `created_at`, `updated_at`.
*   **`document_logs`**: Riwayat pembaruan dokumen (untuk kebutuhan Audit).
    *   `id` (PK), `document_id` (FK), `action` (string), `old_expiry_date` (date), `new_expiry_date` (date), `changed_by` (FK), `created_at`.

### D. Tabel Notifikasi
*   **`notifications`**: Log notifikasi yang dikirim.
    *   `id` (PK), `user_id` (FK), `document_id` (FK), `message` (text), `type` (reminder/escalation), `is_read` (boolean), `sent_at` (timestamp).

### Relasi Antar Tabel:
1.  `supplier_categories` $\xrightarrow{1:N}$ `suppliers`
2.  `suppliers` $\xrightarrow{1:N}$ `supplier_documents`
3.  `document_types` $\xrightarrow{1:N}$ `supplier_documents`
4.  `users` $\xrightarrow{1:N}$ `supplier_documents` (sebagai pengunggah)
5.  `supplier_documents` $\xrightarrow{1:N}$ `document_logs`
6.  `users` $\xrightarrow{1:N}$ `notifications`

---

## 3. Komponen Teknis & Implementasi Fitur

### 3.1 Early Warning System (EWS) Logic
Untuk mengimplementasikan fitur H-90, H-60, H-30, saya akan menggunakan **Cron Job Laravel**.

*   **Logic:**
    Setiap pukul 01:00 AM, sistem menjalankan perintah `php artisan schedule:run`.
    Sistem menjalankan query:
    `SELECT * FROM supplier_documents WHERE expiry_date = TODAY + 90 days OR TODAY + 60 days OR TODAY + 30 days`.
*   **Action:**
    1.  Update `status` dokumen menjadi 'warning'.
    2.  Push ke `Redis Queue` untuk mengirim email ke Staff Procurement.
    3.  Insert data ke tabel `notifications` untuk tampilan di Flutter.

### 3.2 Eskalasi Manager
Jika `expiry_date` < `TODAY` dan status belum diperbarui menjadi 'valid' (dengan file baru), sistem akan memicu trigger eskalasi yang mengirimkan notifikasi khusus ke user dengan role `Manager`.

### 3.3 Digital Repository Strategy
*   **File Naming:** File akan disimpan dengan format `{supplier_id}_{doc_type_id}_{timestamp}.pdf` untuk menghindari duplikasi.
*   **Security:** File tidak boleh diakses publik. Akses dokumen harus melalui *Signed URL* atau *Controller Proxy* di Laravel yang mengecek hak akses user terlebih dahulu.

### 3.4 Mobile Integration (Flutter)
*   **State Management:** Menggunakan `Provider` atau `Bloc` untuk mengelola status notifikasi.
*   **API Consumption:** Menggunakan package `dio` untuk komunikasi dengan Laravel REST API.
*   **Push Notifications:** Menggunakan `firebase_messaging` untuk mengirim alert *real-time* ke smartphone Manager/Staff.

---

## 4. Matriks Pemetaan Fitur ke Teknologi

| Fitur PRD | Implementasi Backend (Laravel) | Implementasi Mobile (Flutter) |
| :--- | :--- | :--- |
| Profil Supplier | CRUD Controller $\rightarrow$ PostgreSQL | Detail View Page |
| Katalog Dokumen | Management Table $\rightarrow$ PostgreSQL | (Read-Only) |
| Digital Repository | Storage Facade $\rightarrow$ S3/Local | PDF Viewer Package |
| Auto Notification | Laravel Scheduler $\rightarrow$ Redis $\rightarrow$ Mail | Push Notification $\rightarrow$ Notification Center |
| Executive Dashboard | Aggregation Query $\rightarrow$ JSON API | Charts (fl_chart) $\rightarrow$ Summary Dashboard |
| Export Report | Laravel Excel / Maatwebsite | (Not Required) |
| Alur Eskalasi | Conditional Logic in Scheduler | High-Priority Alert UI |