# Technical Specification Document: Supplier License Management System (SLMS)

Dokumen ini mendefinisikan arsitektur teknis, model data, dan desain API untuk aplikasi **Supplier License Management System (SLMS)**. Sebagai Senior System Architect, saya merancang sistem ini dengan prinsip *scalability*, *maintainability*, dan *reliability*, mengingat risiko operasional yang tinggi jika terjadi kegagalan dalam pelacakan lisensi.

---

## 1. Arsitektur Sistem (High-Level Architecture)

Sistem akan dibangun menggunakan arsitektur **Decoupled Client-Server** dengan pendekatan **Monolithic Modular** (untuk mempercepat development MVP namun tetap mudah dipisah menjadi microservices di masa depan).

### 1.1 Diagram Arsitektur (Deskripsi Tekstual)
1.  **Frontend Layer (Presentation):**
    *   **Technology:** React.js atau Next.js (untuk performa routing yang cepat dan SEO-friendly jika diperlukan).
    *   **State Management:** Redux Toolkit atau Zustand untuk mengelola status global (user session, notification counts).
    *   **UI Framework:** Tailwind CSS dengan HeadlessUI atau Ant Design untuk komponen Enterprise Dashboard yang konsisten.

2.  **API Layer (Application):**
    *   **Technology:** Node.js (Express/NestJS) atau Python (FastAPI/Django).
    *   **Authentication:** JWT (JSON Web Token) dengan sistem Role-Based Access Control (RBAC).
    *   **Scheduler:** Cron Jobs (Node-cron atau Celery) yang berjalan setiap pukul 00:00 untuk mengecek tanggal kedaluwarsa dan memicu notifikasi.

3.  **Data Layer (Persistence):**
    *   **Database:** PostgreSQL (Relational DB) untuk menjaga integritas data antara Supplier dan Lisensi.
    *   **Object Storage:** AWS S3, Google Cloud Storage, atau MinIO untuk menyimpan file fisik dokumen (PDF, JPG, PNG).

4.  **Integration Layer (Third-Party):**
    *   **Email Service:** SendGrid, Mailgun, atau AWS SES untuk pengiriman email otomatis.
    *   **Storage API:** API untuk manajemen upload/download file.

---

## 2. Model Data (Data Schemas)

Saya menggunakan pendekatan relasional untuk memastikan konsistensi data. Berikut adalah skema database yang diusulkan:

### 2.1 Table: `users`
Menyimpan informasi pengguna sistem dan hak akses.
| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | Unique identifier |
| `username` | String | Unique, Not Null | Login identifier |
| `email` | String | Unique, Not Null | Email for notifications |
| `password_hash` | String | Not Null | Encrypted password |
| `role` | Enum | Not Null | Admin, Procurement, Legal, Manager |
| `created_at` | Timestamp | Default Now() | Entry date |

### 2.2 Table: `suppliers`
Menyimpan profil dasar supplier.
| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | Unique identifier |
| `company_name` | String | Not Null | Nama perusahaan supplier |
| `category` | String | Not Null | Kategori (misal: Logistics, IT, Raw Material) |
| `address` | Text | - | Alamat kantor |
| `contact_person` | String | - | Nama PIC supplier |
| `contact_email` | String | Unique | Email PIC supplier |
| `status` | Enum | Default 'Active' | Status supplier (Active, Blacklisted, Inactive) |
| `created_at` | Timestamp | Default Now() | Entry date |

### 2.3 Table: `licenses`
Menyimpan informasi dokumen lisensi.
| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | Unique identifier |
| `supplier_id` | UUID | FK $\rightarrow$ suppliers | Relasi ke supplier |
| `license_name` | String | Not Null | Nama dokumen (misal: NIB, SIUP, NPWP) |
| `license_number` | String | Not Null | Nomor resmi lisensi |
| `issue_date` | Date | Not Null | Tanggal penerbitan |
| `expiry_date` | Date | Not Null | Tanggal kedaluwarsa |
| `file_url` | String | Not Null | Path/URL ke Object Storage |
| `version` | Integer | Default 1 | Versi dokumen |
| `is_current` | Boolean | Default True | Flag untuk versi terbaru |
| `status` | Enum | Default 'Pending' | Verified, Rejected, Active, Expired |
| `created_at` | Timestamp | Default Now() | Entry date |

### 2.4 Table: `notification_logs`
Audit trail untuk setiap email pengingat yang dikirim.
| Column | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK | Unique identifier |
| `license_id` | UUID | FK $\rightarrow$ licenses | Dokumen yang memicu alert |
| `sent_at` | Timestamp | Default Now() | Waktu pengiriman |
| `threshold_day` | Integer | - | H-30, H-14, atau H-7 |
| `status` | Enum | Not Null | Delivered, Failed |

---

## 3. Desain API (High-Level API Design)

API akan mengikuti standar **RESTful API** dengan format JSON.

### 3.1 Supplier Management
| Method | Endpoint | Description | Role |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/suppliers` | List semua supplier (dengan filter & pagination) | All |
| `POST` | `/api/suppliers` | Tambah supplier baru | Admin, Procurement |
| `GET` | `/api/suppliers/{id}` | Detail profil supplier & list lisensi | All |
| `PUT` | `/api/suppliers/{id}` | Update data supplier | Admin, Procurement |
| `DELETE`| `/api/suppliers/{id}` | Soft delete supplier | Admin |

### 3.2 License Management
| Method | Endpoint | Description | Role |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/licenses` | List seluruh lisensi (untuk Document Vault) | All |
| `POST` | `/api/licenses` | Upload lisensi baru (Multipart/form-data) | Procurement, Supplier |
| `PUT` | `/api/licenses/{id}` | Perbarui informasi lisensi (Updating expiry) | Admin, Procurement |
| `POST` | `/api/licenses/{id}/renew` | Upload versi baru (Auto-archive versi lama) | Procurement, Supplier |
| `PATCH` | `/api/licenses/{id}/verify` | Ubah status $\rightarrow$ Verified | Legal, Manager |

### 3.3 Dashboard & Reports
| Method | Endpoint | Description | Role |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/dashboard/stats` | Get count: Active, Expiring Soon, Expired | All |
| `GET` | `/api/dashboard/critical` | List 5 dokumen paling kritis (closest expiry) | All |
| `GET` | `/api/reports/export` | Generate CSV/PDF list dokumen expired | Manager, Admin |

---

## 4. Logika Sistem (Core Logic & Workflow)

### 4.1 Expiration Tracking Engine (Cron Job)
Sistem tidak menunggu request user untuk mendeteksi kedaluwarsa. Engine ini bekerja di background:
1. **Query:** `SELECT * FROM licenses WHERE is_current = true AND expiry_date - CURRENT_DATE IN (30, 14, 7)`.
2. **Loop:** Untuk setiap hasil, cari email user/procurement yang bertanggung jawab.
3. **Action:** Kirim email melalui Integration Layer $\rightarrow$ Catat di `notification_logs`.
4. **Auto-Update:** Jika `expiry_date < CURRENT_DATE`, ubah status lisensi otomatis menjadi `Expired`.

### 4.2 Versioning Logic
Ketika fungsi `renew` dipanggil:
1. Set `is_current = false` pada dokumen lama dengan `license_name` yang sama untuk `supplier_id` tersebut.
2. Insert record baru dengan `version = version_lama + 1` dan `is_current = true`.
3. Dokumen lama tetap tersimpan di DB dan Storage sebagai *Audit Trail*.

### 4.3 File Storage Strategy
Untuk keamanan dan efisiensi:
*   **File Naming:** Menggunakan UUID untuk menghindari tabrakan nama file (`supplierId_licenseId_timestamp.pdf`).
*   **Access:** File disimpan secara *Private* di S3. API akan menghasilkan *Presigned URL* dengan masa berlaku singkat (misal 15 menit) saat user ingin melakukan preview dokumen.