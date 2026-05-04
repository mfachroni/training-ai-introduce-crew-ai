Sebagai Senior Backend Developer, saya telah menerjemahkan dokumen arsitektur sistem menjadi spesifikasi teknis yang detail. Fokus utama saya adalah memastikan integritas data, keamanan dokumen, dan efisiensi pengiriman notifikasi melalui integrasi Laravel (Backend/Web Admin) dan Flutter (Mobile Client).

Berikut adalah **Dokumen Spesifikasi API dan Logika Bisnis Backend** untuk Sistem Monitoring Dokumen Supplier.

---

# Spesifikasi API & Logika Bisnis: Sistem Monitoring Dokumen Supplier

## 1. Standar Umum API
*   **Protokol:** REST API
*   **Format Data:** JSON (Request & Response)
*   **Autentikasi:** Laravel Sanctum (Token-based)
*   **Base URL:** `https://api.monitoring-dokumen.com/api/v1`
*   **Header Wajib:** 
    *   `Accept: application/json`
    *   `Authorization: Bearer {token}`

---

## 2. Definisi Endpoint API

### A. Modul Autentikasi & Pengguna
| Endpoint | Method | Deskripsi | Request Body | Response (Success) |
| :--- | :--- | :--- | :--- | :--- |
| `/auth/login` | `POST` | Autentikasi user & generate token | `email, password` | `token, user_object` |
| `/auth/logout` | `POST` | Menghapus session token | - | `{"message": "Logged out"}` |
| `/user/profile` | `GET` | Mengambil profil user aktif | - | `user_detail` |

### B. Modul Manajemen Supplier (Admin/Staff)
| Endpoint | Method | Deskripsi | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `/suppliers` | `GET` | List semua supplier (with filter) | `search, category_id` | `list_suppliers` |
| `/suppliers` | `POST` | Tambah supplier baru | `company_name, address, category_id, pic_name, pic_contact` | `supplier_object` |
| `/suppliers/{id}` | `GET` | Detail supplier & daftar dokumen | - | `supplier_detail + documents` |
| `/suppliers/{id}` | `PUT` | Update data supplier | `company_name, ...` | `updated_supplier` |
| `/suppliers/{id}` | `DELETE`| Hapus supplier (Soft Delete) | - | `{"message": "Deleted"}` |

### C. Modul Manajemen Dokumen (Repository)
| Endpoint | Method | Deskripsi | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `/documents/types`| `GET` | List katalog jenis dokumen | - | `list_doc_types` |
| `/documents/upload`| `POST` | Upload dokumen supplier | `supplier_id, doc_type_id, issue_date, expiry_date, file` | `doc_object` |
| `/documents/{id}` | `GET` | Get secure link for preview | - | `signed_url / stream` |
| `/documents/{id}` | `PUT` | Update/Renew dokumen | `expiry_date, file (optional)` | `updated_doc` |

### D. Modul Monitoring & Notifikasi (Mobile/Manager)
| Endpoint | Method | Deskripsi | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `/dashboard/summary`| `GET` | Statistik dokumen (Valid, Warning, Expired) | - | `counts {valid, warning, expired}` |
| `/notifications` | `GET` | List notifikasi untuk user | `page` | `list_notifications` |
| `/notifications/{id}`| `PATCH` | Tandai notifikasi sudah dibaca | - | `{"status": "read"}` |
| `/monitoring/expiring`| `GET` | List dokumen yang akan expired (H-90/60/30) | `days_threshold` | `list_expiring_docs` |

---

## 3. Format Request & Response (Contoh JSON)

### Contoh Upload Dokumen (`POST /documents/upload`)
**Request (Multipart/form-data):**
```json
{
  "supplier_id": 10,
  "document_type_id": 2,
  "issue_date": "2023-01-01",
  "expiry_date": "2024-01-01",
  "file": [File Binary]
}
```
**Response (201 Created):**
```json
{
  "status": "success",
  "data": {
    "id": 105,
    "supplier_name": "PT. Maju Jaya",
    "document_name": "SIUP",
    "expiry_date": "2024-01-01",
    "status": "valid",
    "file_url": "https://storage.com/docs/10_2_16890.pdf"
  }
}
```

---

## 4. Core Business Logic Flow (Backend Logic)

### 4.1 Alur Pengecekan Kedaluwarsa (The Scheduler)
Sistem menggunakan **Laravel Task Scheduling** yang berjalan setiap hari pada pukul 01:00 AM.

1.  **Query Scanning:** Sistem memindai tabel `supplier_documents` untuk mencari dokumen dengan `expiry_date` yang tepat berada pada rentang:
    *   `T+90 hari`, `T+60 hari`, `T+30 hari`, dan `T < 0` (Expired).
2.  **Status Transition:**
    *   Jika masuk range H-90 s/d H-1 $\rightarrow$ Ubah `status` menjadi `warning`.
    *   Jika `expiry_date` < `today` $\rightarrow$ Ubah `status` menjadi `expired`.
3.  **Notification Dispatch:**
    *   **Level Staff:** Kirim Email Reminder via Redis Queue (SMTP).
    *   **Level Manager:** Jika status = `expired`, kirim Push Notification via Firebase (FCM).
    *   **Logging:** Catat setiap peringatan ke dalam tabel `notifications`.

### 4.2 Alur Pengelolaan Dokumen (Digital Repository)
Untuk menjaga keamanan file, backend tidak akan memberikan akses langsung ke folder `/storage`.

1.  **Upload Process:** File di-rename menjadi `{supplier_id}_{doc_type_id}_{timestamp}.pdf` $\rightarrow$ Simpan di Private Storage $\rightarrow$ Simpan path di database.
2.  **Access Process:** 
    *   Flutter meminta file $\rightarrow$ Laravel mengecek Role User.
    *   Jika diizinkan $\rightarrow$ Laravel generate **Temporary Signed URL** (valid selama 15 menit) $\rightarrow$ Flutter mendownload/preview file.

### 4.3 Logika Eskalasi Manager
1.  Sistem mendeteksi dokumen dengan status `expired` yang belum diperbarui selama $> 7$ hari.
2.  Trigger `EscalationEvent` $\rightarrow$ Mengirimkan notifikasi dengan priority `HIGH` ke user dengan role `Manager`.
3.  Notifikasi mencantumkan: Nama Supplier, Jenis Dokumen, dan Lama Keterlambatan.

---

## 5. Implementasi Flutter (Frontend Integration)

### 5.1 Data Flow di Mobile
*   **State Management:** Menggunakan `BLoC` atau `Provider`.
    *   `AuthBloc`: Menangani session token.
    *   `DocumentBloc`: Menangani fetch data summary dan list dokumen.
    *   `NotificationBloc`: Handle real-time update dari FCM.
*   **API Client:** `Dio` dengan Interceptor untuk menambahkan `Authorization: Bearer {token}` secara otomatis pada setiap request.

### 5.2 UI Logic
*   **Color Coding:**
    *   Green: `status == 'valid'`
    *   Yellow: `status == 'warning'`
    *   Red: `status == 'expired'`
*   **Document Viewer:** Menggunakan `flutter_pdfview` untuk menampilkan dokumen dari Signed URL.

## 6. Matriks Validasi Data

| Field | Validasi Backend (Laravel) | Catatan |
| :--- | :--- | :--- |
| `expiry_date` | `required \| date \| after:issue_date` | Tgl kadaluarsa harus setelah tgl terbit. |
| `file` | `required \| file \| mimes:pdf,jpg,png \| max:5120` | Max 5MB, hanya file dokumen/gambar. |
| `role` | `required \| in:admin,staff,manager,audit` | Memastikan role sesuai dengan enum. |
| `supplier_id`| `exists:suppliers,id` | Memastikan supplier terdaftar di DB. |