# Product Requirement Document (PRD): Supplier License Management System (SLMS)

**Versi:** 1.0  
**Status:** Final  
**Peran:** Senior Product Manager  
**Tanggal:** 24 Mei 2024  

---

## 1. Ringkasan Eksekutif (Executive Summary)
**Supplier License Management System (SLMS)** adalah platform berbasis web yang dirancang untuk mengelola dokumen lisensi supplier secara terpusat. Masalah utama yang diselesaikan adalah tingginya risiko operasional dan hukum ketika supplier bekerja dengan dokumen yang kedaluwarsa tanpa disadari oleh perusahaan. SLMS mengotomatisasi pelacakan masa berlaku dokumen dan memberikan sistem pengingat proaktif untuk memastikan kepatuhan administratif secara berkelanjutan.

### 1.1 Visi Produk
*"Menjadi pusat kendali kepatuhan administrasi supplier yang memastikan kelangsungan operasional bisnis melalui manajemen dokumen yang terorganisir dan sistem peringatan dini yang proaktif, guna meminimalisir risiko hukum dan operasional akibat dokumen lisensi yang tidak valid."*

### 1.2 Tujuan Utama
*   Digitalisasi seluruh dokumen lisensi supplier.
*   Menghilangkan ketergantungan pada pemantauan manual (Excel/Reminder kalender).
*   Menyediakan visibilitas *real-time* terhadap status kepatuhan supplier melalui dashboard.
*   Mengurangi risiko *downtime* operasional akibat dokumen yang expired.

---

## 2. Target Pengguna & Personalisasi
| Peran | Kebutuhan Utama | Pain Point |
| :--- | :--- | :--- |
| **Procurement Officer** | Mengelola input data dan pembaruan dokumen. | Lupa mengecek tanggal expired karena banyaknya jumlah supplier. |
| **Vendor Manager** | Memvalidasi kelayakan supplier. | Sulit menemukan dokumen terbaru saat audit mendadak. |
| **Legal/Compliance** | Memastikan kepatuhan regulasi. | Risiko hukum jika supplier menggunakan dokumen ilegal/expired. |
| **Administrator** | Pengaturan sistem dan manajemen akses. | Kesulitan mengatur siapa yang boleh mengedit dokumen sensitif. |

---

## 3. Spesifikasi Fitur (Feature Set)

Fitur dikelola menggunakan metode MoSCoW untuk menentukan prioritas pengembangan.

### 3.1 Priority 1: Must Have (MVP)
| Fitur | Deskripsi | Kriteria Penerimaan (Acceptance Criteria) |
| :--- | :--- | :--- |
| **Supplier Directory** | Basis data utama supplier (Nama, Alamat, Kontak, Kategori). | User dapat menambah, mengedit, dan melihat daftar supplier. |
| **License Repository** | Form upload dokumen dengan field: Nama, No. Lisensi, Tgl Terbit, Tgl Expired. | File tersimpan dengan aman; input tanggal divalidasi (tidak boleh masa lalu). |
| **Expiration Engine** | Logika otomatis penghitungan sisa hari menuju tanggal kedaluwarsa. | Sistem dapat menghitung selisih hari antara hari ini dan `expiry_date`. |
| **Automated Notifications** | Email pengingat otomatis pada H-30, H-14, dan H-7. | Email terkirim tepat waktu kepada admin/PIC terkait. |
| **Compliance Dashboard** | Widget status: Aktif, Hampir Expired, dan Expired. | Angka pada widget sinkron dengan data real-time di database. |

### 3.2 Priority 2: Should Have (Efficiency)
| Fitur | Deskripsi | Kriteria Penerimaan |
| :--- | :--- | :--- |
| **Document Versioning** | Update dokumen tanpa menghapus riwayat versi lama. | Tersedia tab "History" untuk melihat dokumen versi sebelumnya. |
| **Advanced Search & Filter** | Pencarian berdasarkan status, kategori, atau rentang tanggal. | Hasil pencarian muncul dalam < 2 detik dengan filter yang akurat. |
| **Basic Supplier Portal** | Akses terbatas supplier untuk upload mandiri. | Supplier hanya bisa mengakses dokumen milik perusahaannya sendiri. |
| **Export Report** | Ekspor daftar dokumen expired ke Excel/PDF. | File yang diekspor mengandung semua kolom informasi yang relevan. |

### 3.3 Priority 3: Could Have (Scalability)
| Fitur | Deskripsi | Kriteria Penerimaan |
| :--- | :--- | :--- |
| **Approval Workflow** | Status: `Pending` $\rightarrow$ `Verified` $\rightarrow$ `Active`. | Dokumen tidak dianggap "Aktif" sebelum disetujui oleh Legal/Manager. |
| **ERP Integration** | API Integration dengan sistem pengadaan perusahaan. | Data supplier di ERP otomatis tersinkron dengan SLMS. |
| **Multi-channel Alert** | Notifikasi via WhatsApp atau Push Notification. | Notifikasi diterima di perangkat mobile secara real-time. |

---

## 4. Desain Pengalaman Pengguna (UX Specification)

### 4.1 Strategi Desain
Mengadopsi **Enterprise Dashboard Pattern** yang fokus pada efisiensi data.
*   **Layout:** Sidebar navigasi permanen di sisi kiri.
*   **Kepadatan Data:** Medium Density (optimasi ruang untuk tabel besar).
*   **Responsivitas:** Utama di Desktop, Adaptive di Tablet.

### 4.2 Alur Kerja Utama (User Flow)
1. **Input:** `Add Supplier` $\rightarrow$ `Upload License` $\rightarrow$ `Set Expiry Date` $\rightarrow$ `Save`.
2. **Monitoring:** `Sistem Scan Daily` $\rightarrow$ `Detect Threshold (H-30)` $\rightarrow$ `Send Email Alert`.
3. **Update:** `User Receive Email` $\rightarrow$ `Open Supplier Detail` $\rightarrow$ `Upload New Version` $\rightarrow$ `Update Date` $\rightarrow$ `Status Active`.

### 4.3 Elemen Antarmuka Kunci
*   **Status Badge:** Hijau (`Active`), Kuning (`Expiring Soon`), Merah (`Expired`).
*   **Control Center:** Card-based KPI di bagian atas dashboard.
*   **Document Vault:** Tabel dengan thumbnail preview PDF dan tombol aksi cepat (*Renew/View*).
*   **Date Picker:** Kalender interaktif untuk mencegah kesalahan input tanggal.

---

## 5. Spesifikasi Teknis (Technical Specification)

### 5.1 Stack Teknologi
*   **Frontend:** React.js / Next.js, Tailwind CSS, Zustand/Redux.
*   **Backend:** Node.js (NestJS) atau Python (FastAPI).
*   **Database:** PostgreSQL (Data Relasional).
*   **Storage:** AWS S3 / Google Cloud Storage (Object Storage untuk dokumen).
*   **Infrastructure:** Docker, Kubernetes, Cron Jobs untuk scheduler.

### 5.2 Model Data (Skema Ringkas)
*   **`users`**: `id, username, email, role, password_hash`.
*   **`suppliers`**: `id, company_name, category, contact_email, status`.
*   **`licenses`**: `id, supplier_id, license_name, license_number, issue_date, expiry_date, file_url, version, is_current, status`.
*   **`notification_logs`**: `id, license_id, sent_at, threshold_day, status`.

### 5.3 Logika Sistem Kritis
1.  **Cron Job Scheduler:** Berjalan setiap pukul 00:00. Menjalankan query untuk mencari lisensi yang masuk threshold $\rightarrow$ Memicu pengiriman email via SendGrid/AWS SES.
2.  **Versioning Logic:** Saat dokumen baru diunggah, sistem mengubah `is_current = false` pada dokumen lama dan membuat record baru dengan `version = n+1` dan `is_current = true`.
3.  **Security:** Implementasi Role-Based Access Control (RBAC). File dokumen diakses melalui *Presigned URL* (URL sementara) untuk mencegah akses ilegal.

---

## 6. Matriks Keberhasilan (Success Metrics)
| Metrik | Target | Cara Mengukur |
| :--- | :--- | :--- |
| **Compliance Rate** | 100% dokumen aktif | Persentase dokumen `Active` vs `Expired` di dashboard. |
| **Renewal Lead Time** | $\le 7$ hari sebelum expired | Waktu antara notifikasi H-7 dan upload dokumen baru. |
| **Admin Efficiency** | Penurunan jam kerja manual | Survei internal waktu yang dihabiskan untuk cek dokumen. |
| **Zero Breach** | 0 kejadian operasional terhenti | Jumlah laporan kegagalan audit/operasional akibat lisensi expired. |