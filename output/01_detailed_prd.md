# Dokumen Spesifikasi Detail: Supplier License Management System (SLMS)

**Versi:** 1.0  
**Status:** Final  
**Peran Terlibat:** Senior Business Analyst, Lead QA Engineer, Senior Technical Architect

---

## 1. Pendahuluan
Dokumen ini merupakan spesifikasi komprehensif untuk pembangunan **Supplier License Management System (SLMS)**. Sistem ini dirancang untuk mengelola basis data supplier dan memantau masa berlaku dokumen lisensi secara otomatis guna memitigasi risiko kepatuhan (*compliance*) perusahaan.

---

## 2. User Stories & Acceptance Criteria
Pembagian fitur dilakukan menggunakan metode MoSCoW untuk menentukan prioritas pengembangan.

### 🟢 PRIORITY 1: MUST HAVE (MVP)

#### 2.1 Supplier Directory (Direktori Supplier)
*   **User Story 1.1: Menambah Supplier Baru**
    *   **Deskripsi:** Sebagai Procurement Officer, saya ingin dapat menambahkan data supplier baru ke dalam sistem, sehingga saya memiliki basis data supplier yang terpusat.
    *   **Acceptance Criteria:**
        *   Sistem menyediakan form input dengan field: Nama Perusahaan (Wajib), Alamat (Wajib), Kontak Person (Wajib), Email Kontak (Wajib & validasi format email), dan Kategori Supplier (Dropdown).
        *   Sistem memberikan pesan sukses setelah data berhasil disimpan.
        *   Sistem memberikan pesan error jika ada field wajib yang kosong.
*   **User Story 1.2: Mengelola Data Supplier**
    *   **Deskripsi:** Sebagai Procurement Officer, saya ingin dapat melihat, mengedit, dan menghapus data supplier, sehingga informasi supplier tetap up-to-date.
    *   **Acceptance Criteria:**
        *   Terdapat halaman daftar supplier dalam bentuk tabel yang menampilkan ringkasan informasi.
        *   User dapat mengklik tombol "Edit" untuk memperbarui informasi supplier.
        *   User dapat menghapus supplier (dengan konfirmasi pop-up sebelum eksekusi).
        *   Perubahan data tersimpan secara real-time di database.

#### 2.2 License Repository (Repositori Lisensi)
*   **User Story 2.1: Mengunggah Dokumen Lisensi**
    *   **Deskripsi:** Sebagai Procurement Officer, saya ingin mengunggah file lisensi untuk supplier tertentu, sehingga dokumen tersimpan secara digital.
    *   **Acceptance Criteria:**
        *   User dapat memilih supplier dari daftar sebelum mengunggah dokumen.
        *   Form upload mencakup field: Nama Lisensi (misal: SIUP, NIB), Nomor Lisensi (Wajib), Tanggal Terbit (Date Picker), dan Tanggal Kedaluwarsa (Date Picker).
        *   Sistem hanya menerima format file tertentu (PDF, JPG, PNG) dengan batas ukuran maksimal 5MB.
        *   Sistem memvalidasi agar `expiry_date` tidak boleh lebih kecil dari tanggal hari ini.
        *   File tersimpan secara aman di Object Storage dan URL tersimpan di database.

#### 2.3 Expiration Engine (Mesin Penghitung Kedaluwarsa)
*   **User Story 3.1: Perhitungan Sisa Hari Otomatis**
    *   **Deskripsi:** Sebagai Sistem, saya ingin menghitung selisih hari antara tanggal hari ini dan tanggal kedaluwarsa dokumen, sehingga status kepatuhan dapat ditentukan.
    *   **Acceptance Criteria:**
        *   Sistem menjalankan logika pengurangan: `Sisa Hari = Tanggal Expired - Tanggal Hari Ini`.
        *   Jika `Sisa Hari < 0`, status otomatis menjadi **Expired**.
        *   Jika `Sisa Hari` berada dalam rentang 1-30 hari, status otomatis menjadi **Expiring Soon**.
        *   Jika `Sisa Hari > 30`, status otomatis menjadi **Active**.

#### 2.4 Automated Notifications (Notifikasi Otomatis)
*   **User Story 4.1: Pengiriman Email Pengingat Berkala**
    *   **Deskripsi:** Sebagai Procurement Officer, saya ingin menerima email pengingat otomatis saat dokumen supplier mendekati tanggal expired, sehingga saya bisa segera meminta pembaruan.
    *   **Acceptance Criteria:**
        *   Sistem menjalankan *Cron Job* setiap hari pukul 00:00.
        *   Email pengingat terkirim otomatis pada threshold: H-30, H-14, dan H-7 sebelum `expiry_date`.
        *   Isi email mencakup: Nama Supplier, Nama Lisensi, Tanggal Expired, dan Link menuju detail supplier.
        *   Sistem mencatat log pengiriman email dalam tabel `notification_logs`.

#### 2.5 Compliance Dashboard (Dashboard Kepatuhan)
*   **User Story 5.1: Visualisasi Status Kepatuhan (Widget)**
    *   **Deskripsi:** Sebagai Vendor Manager/Compliance, saya ingin melihat ringkasan jumlah dokumen yang Aktif, Hampir Expired, dan Expired pada dashboard, sehingga saya bisa memantau risiko secara cepat.
    *   **Acceptance Criteria:**
        *   Terdapat 3 widget kartu (Card): "Active", "Expiring Soon", dan "Expired".
        *   Angka pada widget harus sinkron secara real-time dengan database.
        *   Widget dapat diklik untuk mengarahkan user ke daftar detail dokumen dengan status tersebut.

### 🔵 PRIORITY 2: SHOULD HAVE (EFFICIENCY)

#### 2.6 Document Versioning (Versi Dokumen)
*   **User Story 6.1: Riwayat Pembaruan Dokumen**
    *   **Acceptance Criteria:** Dokumen lama ditandai `is_current = false`, dokumen baru menjadi `is_current = true` dengan versi `n+1`. Tersedia tab "History" untuk audit trail.

#### 2.7 Advanced Search & Filter
*   **User Story 7.1: Pencarian dan Penyaringan Data**
    *   **Acceptance Criteria:** Pencarian berdasarkan Nama Supplier/No Lisensi; Filter berdasarkan Status, Kategori, dan Rentang Tanggal. Response time < 2 detik.

#### 2.8 Basic Supplier Portal (Portal Mandiri Supplier)
*   **User Story 8.1: Upload Mandiri oleh Supplier**
    *   **Acceptance Criteria:** Login khusus supplier, isolasi data (hanya melihat milik sendiri), dokumen baru masuk status `Pending` untuk verifikasi admin.

#### 2.9 Export Report
*   **User Story 9.1: Ekspor Daftar Dokumen ke Format File**
    *   **Acceptance Criteria:** Tombol ekspor ke `.xlsx` atau `.pdf` dengan kolom detail supplier dan status expired.

### 🟡 PRIORITY 3: COULD HAVE (SCALABILITY)

#### 2.10 Approval Workflow
*   **User Story 10.1: Verifikasi Dokumen oleh Legal/Manager**
    *   **Acceptance Criteria:** Alur `Pending` $\rightarrow$ `Approve` (Active) atau `Reject` (Rejected dengan alasan).

#### 2.11 ERP Integration
*   **User Story 11.1: Sinkronisasi Data Supplier via API**
    *   **Acceptance Criteria:** Endpoint API untuk sinkronisasi data supplier dari ERP perusahaan secara dua arah.

#### 2.12 Multi-channel Alert
*   **User Story 12.1: Notifikasi WhatsApp/Push Notification**
    *   **Acceptance Criteria:** Integrasi WA Business API untuk alert H-14 dan H-7.

---

## 3. Analisis Edge Case & Mitigasi QA

| Modul | Skenario Edge Case / Risiko | Ekspektasi Perilaku Sistem (Mitigasi) |
| :--- | :--- | :--- |
| **Supplier Directory** | Input karakter spesial pada nama PT atau email tidak valid. | Validasi regex ketat; Error message: "Format email tidak valid". |
| | Duplikasi Nama Perusahaan/NPWP. | Blokir input duplikat; Pesan: "Supplier sudah terdaftar". |
| | Penghapusan supplier yang punya dokumen aktif. | Implementasi *soft-delete*; peringatan dokumen aktif. |
| **License Repository** | File dengan ekstensi ganda (misal: `doc.pdf.exe`). | Validasi *MIME Type/Magic Bytes* (bukan sekadar ekstensi). |
| | File kosong (0 bytes) atau > 5MB. | Tolak file; Pesan: "Ukuran file tidak valid". |
| | `expiry_date` di masa lalu (backdated). | Blokir input tanggal kadaluarsa yang sudah lewat. |
| **Engine & Notif** | Perbedaan Timezone (UTC vs WIB). | Simpan UTC di DB, konversi ke lokal di Frontend. |
| | Kegagalan Cron Job (Server Down). | Mekanisme *retry* atau *catch-up* setelah sistem online. |
| **Dashboard** | Performance query data puluhan ribu supplier. | Indexing kolom `company_name` dan `expiry_date`; Pagination. |
| **Supplier Portal** | ID Manipulation (akses supplier lain via URL). | **Kritis:** Authorization Check `User_ID == Supplier_ID`. |
| | Upload script berbahaya (XSS/SQLi). | Sanitasi input & *prepared statements*. |
| **Integration** | API ERP down atau data korup. | JSON Schema validation; Dead Letter Queue (DLQ) untuk retry. |

---

## 4. Technical Design Document (LLD)

### 4.1 Database Schema (PostgreSQL)

#### Table: `suppliers`
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `supplier_id` | UUID | PK | ID unik supplier. |
| `company_name` | VARCHAR(255)| Not Null, Indexed| Nama resmi perusahaan. |
| `contact_email` | VARCHAR(100) | Not Null, Unique| Email untuk notifikasi & login. |
| `category_id` | INT | FK $\to$ `categories`| Kategori supplier. |
| `deleted_at` | TIMESTAMP | Nullable | Untuk *soft-delete*. |

#### Table: `licenses`
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `license_id` | UUID | PK | ID unik lisensi. |
| `supplier_id` | UUID | FK $\to$ `suppliers`| Relasi ke supplier. |
| `license_type` | VARCHAR(50) | Not Null | Misal: SIUP, NIB. |
| `current_version_id`| UUID | FK $\to$ `license_versions`| Penunjuk versi terbaru. |

#### Table: `license_versions`
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `version_id` | UUID | PK | ID unik versi. |
| `license_id` | UUID | FK $\to$ `licenses`| Relasi ke lisensi. |
| `expiry_date` | DATE | Not Null, Indexed| Tanggal kadaluarsa. |
| `file_url` | TEXT | Not Null | Path ke Object Storage. |
| `version_number` | INT | Not Null | Urutan versi (1, 2, 3...). |
| `is_current` | BOOLEAN | Default True | Penanda versi aktif. |
| `status` | ENUM | 'Pending', 'Active', 'Rejected', 'Expired'| Status validasi. |

### 4.2 Logic Flow & Pseudo-code

**1. Expiration Logic:**
```typescript
function calculateComplianceStatus(expiryDate: Date): Status {
    const diffDays = Math.ceil((expiryDate.getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
    if (diffDays < 0) return "EXPIRED";
    if (diffDays <= 30) return "EXPIRING_SOON";
    return "ACTIVE";
}
```

**2. Versioning Logic (Transaction):**
- `BEGIN TRANSACTION`
- `UPDATE license_versions SET is_current = false WHERE license_id = {id}`
- `INSERT INTO license_versions (version_number = max+1, is_current = true, ...)`
- `UPDATE licenses SET current_version_id = {new_id} WHERE license_id = {id}`
- `COMMIT`

### 4.3 Core API Endpoints

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/suppliers` | Officer | Tambah supplier baru. |
| `GET` | `/api/suppliers` | Officer, Mgr | List supplier (filter & pagination). |
| `POST` | `/api/licenses/upload` | Officer, Supplier| Upload versi lisensi baru. |
| `PATCH` | `/api/licenses/verify` | Manager | Approve/Reject dokumen pending. |
| `GET` | `/api/dashboard/stats` | Officer, Mgr | Data agregat untuk widget dashboard. |
| `GET` | `/api/reports/export` | Officer, Mgr | Ekspor laporan ke CSV/PDF. |

---

## 5. Final Validation Checklist
- [ ] Validasi Frontend & Backend pada semua input field.
- [ ] Verifikasi MIME Type file (Magic Bytes) untuk keamanan upload.
- [ ] Pengetesan Authorization (Role-Based Access Control) untuk Supplier Portal.
- [ ] Audit Trail: Setiap perubahan mencatat `Who`, `When`, `What`.
- [ ] Pengujian Cron Job untuk notifikasi H-30, H-14, H-7.
