# Dokumen Teknis Detail: Sistem Monitoring Dokumen Supplier

Dokumen ini merupakan konsolidasi akhir yang menggabungkan arsitektur sistem, desain database, spesifikasi API, serta rencana implementasi frontend untuk pengembangan **Sistem Monitoring Dokumen Supplier & Notifikasi Masa Aktif**.

---

## 1. High-Level Architecture (Arsitektur Sistem)

Sistem ini menggunakan arsitektur **Client-Server** dengan pendekatan **API-First**. Backend dibangun menggunakan Laravel untuk mengelola bisnis logika dan admin panel, sementara Flutter digunakan sebagai aplikasi mobile untuk monitoring eksekutif dan notifikasi real-time.

### Komponen Infrastruktur:
*   **Backend Engine:** Laravel 10/11 (PHP 8.2+).
*   **Database:** PostgreSQL (untuk konsistensi data dan dukungan query kompleks).
*   **Mobile Client:** Flutter (Stable Channel) menggunakan State Management BLoC.
*   **Task Scheduler:** Laravel Scheduler (Cron Job) untuk scanning harian.
*   **Queue & Cache:** Redis (untuk pengiriman email massal dan optimasi request).
*   **File Storage:** AWS S3 atau Local Secure Storage dengan akses via *Signed URLs*.
*   **Notification Gateway:** SMTP (Email) dan Firebase Cloud Messaging (FCM) untuk Push Notifications.

**Alur Data:**
`User (Web/Mobile)` $\rightarrow$ `Nginx/Load Balancer` $\rightarrow$ `Laravel API` $\rightarrow$ `PostgreSQL` $\rightarrow$ `Storage (S3/Local)`
$\downarrow$
`Laravel Scheduler` $\rightarrow$ `Redis Queue` $\rightarrow$ `SMTP/FCM` $\rightarrow$ `User Device`

---

## 2. Desain Database (Database Schema)

### A. Tabel User & Akses
*   **`users`**: `id (PK)`, `username`, `password`, `email`, `full_name`, `role (enum: admin, staff, manager, audit)`, `created_at`, `updated_at`.

### B. Tabel Inti (Core)
*   **`supplier_categories`**: `id (PK)`, `category_name (string)`.
*   **`suppliers`**: `id (PK)`, `company_name (string)`, `address (text)`, `category_id (FK)`, `pic_name (string)`, `pic_contact (string)`, `status (active/inactive)`, `created_at`, `updated_at`.
*   **`document_types`**: `id (PK)`, `document_name (string)`, `default_validity_days (int)`, `is_mandatory (boolean)`.

### C. Tabel Manajemen Dokumen
*   **`supplier_documents`**: `id (PK)`, `supplier_id (FK)`, `document_type_id (FK)`, `file_path (string)`, `issue_date (date)`, `expiry_date (date)`, `uploaded_by (FK $\rightarrow$ users)`, `status (enum: valid, warning, expired)`, `created_at`, `updated_at`.
*   **`document_logs`**: `id (PK)`, `document_id (FK)`, `action (string)`, `old_expiry_date (date)`, `new_expiry_date (date)`, `changed_by (FK)`, `created_at`.

### D. Tabel Notifikasi
*   **`notifications`**: `id (PK)`, `user_id (FK)`, `document_id (FK)`, `message (text)`, `type (reminder/escalation)`, `is_read (boolean)`, `sent_at (timestamp)`.

---

## 3. Spesifikasi API & Logika Bisnis

### 3.1 Standar API
*   **Protokol:** REST API | **Format:** JSON | **Auth:** Laravel Sanctum (Bearer Token).
*   **Base URL:** `https://api.monitoring-dokumen.com/api/v1`

### 3.2 Daftar Endpoint Utama
| Modul | Endpoint | Method | Deskripsi |
| :--- | :--- | :--- | :--- |
| **Auth** | `/auth/login` | `POST` | Login & generate token |
| **Supplier** | `/suppliers` | `GET/POST` | List & Tambah supplier |
| **Supplier** | `/suppliers/{id}` | `GET/PUT` | Detail & Update supplier |
| **Dokumen** | `/documents/upload`| `POST` | Upload file & set expiry date |
| **Dokumen** | `/documents/{id}` | `GET` | Generate Signed URLสำหรับ preview |
| **Dashboard**| `/dashboard/summary`| `GET` | Statistik (Valid, Warning, Expired) |
| **Notif** | `/notifications` | `GET/PATCH`| List notifikasi & Mark as read |

### 3.3 Early Warning System (EWS) & Eskalasi
1.  **Scheduler:** Setiap pukul 01:00 AM, sistem menjalankan `php artisan schedule:run`.
2.  **Scanning Logic:** Query dokumen dengan `expiry_date` pada H-90, H-60, H-30.
3.  **Trigger:**
    *   **Staff:** Email reminder otomatis via Redis Queue.
    *   **Manager:** Push Notification via FCM jika dokumen sudah berstatus `expired` (T < 0).
4.  **Logika Eskalasi:** Jika dokumen expired $> 7$ hari tanpa update, sistem mengirimkan alert prioritas tinggi (`HIGH`) ke role Manager.

---

## 4. Implementasi Frontend

### 4.1 Web Admin (Laravel + Blade)
Difokuskan untuk pengelolaan data berat (Input/Upload).
*   **Tech Stack:** Laravel Blade, Tailwind CSS, Alpine.js.
*   **Komponen Utama:** `DataTable` untuk monitoring, `DocumentUploadForm` dengan validasi MIME (PDF/JPG), dan `Export Engine` (Laravel Excel).
*   **Security:** File disimpan di private storage; akses diberikan melalui controller proxy.

### 4.2 Mobile App (Flutter)
Difokuskan untuk monitoring cepat dan alert real-time.
*   **Tech Stack:** Flutter, BLoC (State Management), Dio (HTTP Client), `flutter_pdfview`.
*   **Fitur Utama:** 
    *   **Executive Dashboard:** Ringkasan jumlah dokumen expired menggunakan `fl_chart`.
    *   **Notification Center:** Real-time alert melalui `firebase_messaging`.
    *   **Document Viewer:** Preview dokumen menggunakan Temporary Signed URL.
*   **Clean Architecture:** Folder dibagi menjadi `core`, `shared`, dan `features`.

---

## 5. Matriks Konsolidasi Teknologi

| Fitur PRD | Backend (Laravel) | Mobile (Flutter) | Logic / State |
| :--- | :--- | :--- | :--- |
| **Profil Supplier** | CRUD $\rightarrow$ PostgreSQL | Detail View Page | Server-Side |
| **Digital Repository**| Storage Facade (S3) | PDF Viewer $\rightarrow$ Signed URL | BLoC |
| **Auto-Notification** | Scheduler $\rightarrow$ Redis $\rightarrow$ SMTP | Push Notification $\rightarrow$ FCM | Event-Driven |
| **Executive Dashboard**| Aggregation Query $\rightarrow$ JSON | StatCards $\rightarrow$ fl\_chart | BLoC |
| **Export Report** | Laravel Excel (XLSX/CSV) | (Tidak tersedia) | Server-Side |
| **Eskalasi Manager** | Conditional Trigger (T < 0) | High-Priority UI Alert | Event-Driven |

### Standar Warna UI (Consistency):
*   **Valid:** `#10B981` (Emerald/Green)
*   **Warning:** `#F59E0B` (Amber/Yellow)
*   **Expired:** `#EF4444` (Red)