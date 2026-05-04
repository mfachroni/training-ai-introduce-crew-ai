Halo, saya Lead QA Engineer. Saya telah menganalisis PRD dan User Stories untuk **Supplier License Management System (SLMS)**. 

Tugas saya adalah mencoba "merusak" sistem ini sebelum satu baris kode pun ditulis. Fokus saya adalah pada skenario di mana user melakukan kesalahan, kegagalan sistem, celah keamanan, dan kondisi aneh (*edge cases*) yang sering terlewatkan oleh tim pengembang.

Berikut adalah **Laporan Komprehensif Edge Cases, Error Handling, dan Strategi Validasi** untuk SLMS.

---

# 🛡️ QA Destructive Analysis Report: Supplier License Management System (SLMS)

## 1. MODUL: Supplier Directory (Direktori Supplier)

| Scenario | Edge Case / Negative Scenario | Expected System Behavior (Validation Rule) |
| :--- | :--- | :--- |
| **Input Data** | Input Nama Perusahaan dengan karakter spesial atau angka (misal: `PT. Maju Mundur 123!@#`). | Sistem harus memvalidasi karakter yang diizinkan. Jika hanya teks, berikan error: "Karakter spesial tidak diizinkan". |
| **Input Data** | Input Email dengan format tidak valid atau domain yang tidak ada (misal: `test@gmail,com` atau `user@company`). | Sistem wajib melakukan validasi regex email. Pesan: "Format email tidak valid". |
| **Duplikasi** | Menambah supplier dengan Nama Perusahaan atau NPWP/Nomor Identitas yang sudah ada di database. | Sistem harus mencegah duplikasi data. Munculkan peringatan: "Supplier dengan nama/identitas ini sudah terdaftar". |
| **Data Management** | Menghapus supplier yang saat ini memiliki dokumen lisensi aktif atau sedang dalam proses kontrak. | Sistem tidak boleh menghapus secara *hard-delete*. Gunakan *soft-delete* atau beri peringatan: "Supplier tidak dapat dihapus karena memiliki dokumen aktif". |
| **Data Management** | Mengedit nama supplier yang sedang terhubung dengan ribuan dokumen lisensi. | Sistem harus memastikan *cascading update* terjadi sehingga semua dokumen tetap merujuk pada supplier yang benar. |

## 2. MODUL: License Repository (Repositori Lisensi)

| Scenario | Edge Case / Negative Scenario | Expected System Behavior (Validation Rule) |
| :--- | :--- | :--- |
| **File Upload** | Menjumlahkan file dengan ekstensi ganda (misal: `dokumen.pdf.exe`) untuk mengelabui sistem. | Sistem harus memvalidasi *MIME Type* file, bukan hanya ekstensi. Tolak file yang bukan benar-benar PDF/JPG/PNG. |
| **File Upload** | Mengunggah file dengan ukuran tepat 5MB atau sedikit di atas 5MB (misal: 5.1MB). | Sistem harus konsisten pada limit. Jika > 5MB, tampilkan: "Ukuran file melebihi batas maksimal 5MB". |
| **File Upload** | Mengunggah file kosong (0 bytes). | Sistem harus menolak file kosong dan memberikan pesan error: "File yang diunggah kosong". |
| **Date Logic** | Mengatur `expiry_date` yang sama dengan `issue_date` (Tanggal Terbit). | Sistem harus memberikan peringatan atau melarang jika kebijakan bisnis mewajibkan masa berlaku minimal 1 hari. |
| **Date Logic** | Mengatur `expiry_date` di masa lalu (Backdated). | Sistem harus menolak (`Block`) input tanggal kadaluarsa yang sudah lewat dari tanggal hari ini. |
| **Concurrency** | Dua user mengunggah versi dokumen yang berbeda untuk supplier yang sama di detik yang sama. | Implementasikan *database locking* atau *queue* untuk memastikan versi dokumen (`n+1`) tidak duplikat. |

## 3. MODUL: Expiration Engine & Notifications

| Scenario | Edge Case / Negative Scenario | Expected System Behavior (Validation Rule) |
| :--- | :--- | :--- |
| **Timezone** | Server berada di UTC, namun user berada di WIB (GMT+7). Perbedaan jam dapat mempengaruhi perhitungan H-30. | Sistem harus menggunakan standar UTC di database dan melakukan konversi ke zona waktu lokal user saat perhitungan sisa hari. |
| **Cron Job** | Cron job gagal berjalan pada pukul 00:00 karena server down atau timeout. | Sistem harus memiliki mekanisme *retry* atau *catch-up* agar notifikasi yang terlewat tetap terkirim saat sistem kembali online. |
| **Notification** | Email pengingat terkirim ke alamat email yang sudah tidak aktif atau *mailbox full*. | Sistem harus mencatat status pengiriman di `notification_logs` (Sent, Delivered, Bounced/Failed). |
| **Logic Gap** | Dokumen diperbarui (diupload versi baru) tepat setelah email H-14 terkirim. | Sistem harus mengecek kembali status terbaru sebelum mengirim email H-7 agar user tidak menerima pengingat untuk dokumen yang sudah diperbarui. |

## 4. MODUL: Compliance Dashboard & Search

| Scenario | Edge Case / Negative Scenario | Expected System Behavior (Validation Rule) |
| :--- | :--- | :--- |
| **Performance** | Jumlah data supplier mencapai puluhan ribu, melakukan pencarian dengan keyword umum (misal: "PT"). | Implementasikan *pagination* dan *indexing* pada database agar query tidak *timeout* dan tetap di bawah 2 detik. |
| **Filter Logic** | Menggunakan filter rentang tanggal yang terbalik (Tanggal Mulai > Tanggal Akhir). | Sistem harus memvalidasi input tanggal. Jika terbalik, sistem otomatis menukar atau memberikan error: "Rentang tanggal tidak valid". |
| **Real-time** | Widget dashboard tidak terupdate setelah admin melakukan "Approve" dokumen. | Implementasikan *cache invalidation* atau *real-time update* (via Websocket/Polling) agar angka widget sinkron. |

## 5. MODUL: Supplier Portal (Self-Service)

| Scenario | Edge Case / Negative Scenario | Expected System Behavior (Validation Rule) |
| :--- | :--- | :--- |
| **Security** | Supplier mencoba mengakses dokumen supplier lain dengan mengubah ID di URL (misal: `/supplier/101` menjadi `/supplier/102`). | **Kritikal:** Implementasikan *Authorization Check*. Sistem harus memvalidasi apakah `User_ID` yang login memiliki akses ke `Supplier_ID` tersebut. Jika tidak, tampilkan 403 Forbidden. |
| **Security** | Supplier mencoba mengunggah script berbahaya (XSS/SQL Injection) melalui nama file atau field input. | Lakukan *sanitization* pada semua input. Gunakan *prepared statements* dan filter karakter berbahaya pada nama file. |
| **Workflow** | Supplier mengunggah dokumen baru berkali-kali dalam waktu singkat (spamming update). | Implementasikan *rate limiting* pada API upload untuk mencegah server overload. |

## 6. MODUL: Approval Workflow & Integration

| Scenario | Edge Case / Negative Scenario | Expected System Behavior (Validation Rule) |
| :--- | :--- | :--- |
| **Workflow** | Dua Manager mencoba melakukan "Approve" dan "Reject" pada dokumen yang sama secara bersamaan. | Terapkan *Optimistic Locking*. User kedua akan menerima pesan: "Dokumen ini telah diperbarui oleh user lain, silakan refresh halaman". |
| **Integration** | ERP mengirimkan data supplier yang tidak lengkap atau format yang rusak via API. | API SLMS harus memiliki validasi skema yang ketat (misal: JSON Schema). Jika data tidak valid, kembalikan response `400 Bad Request` dengan detail error. |
| **Integration** | API ERP down saat proses sinkronisasi dua arah. | Implementasikan *Dead Letter Queue* (DLQ) atau log kegagalan. Sistem harus dapat mengulang proses sinkronisasi yang gagal setelah koneksi pulih. |

---

### 🚀 Summary Strategi Validasi Final (QA Checklist)

1.  **Input Validation:** Semua field wajib memiliki validasi sisi klien (Frontend) dan sisi server (Backend).
2.  **File Security:** Scan semua file yang diunggah untuk malware dan validasi *magic numbers* (bukan hanya ekstensi).
3.  **Access Control:** Pastikan prinsip *Least Privilege*. Supplier $\neq$ Procurement Officer $\neq$ Admin.
4.  **Data Integrity:** Gunakan *Transactions* (ACID) saat melakukan update status dokumen agar tidak ada data yang "menggantung" jika terjadi crash.
5.  **Audit Trail:** Pastikan setiap perubahan data (Edit/Delete/Approve) mencatat: `Who`, `When`, `What` (Old Value $\rightarrow$ New Value).