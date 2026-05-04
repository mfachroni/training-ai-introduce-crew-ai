Berikut adalah dokumen analisis kebutuhan yang telah diklarifikasi berdasarkan input awal. Sebagai Senior Requirement Specialist, saya telah membedah kebutuhan dasar menjadi struktur yang komprehensif untuk memastikan Tim Procurement mendapatkan solusi yang tepat sasaran dan meminimalisir *scope creep*.

---

# Dokumen Analisis Kebutuhan (Requirement Analysis Document)
**Proyek:** Sistem Monitoring Dokumen Supplier & Notifikasi Masa Aktif
**Target Pengguna:** Tim Procurement
**Status:** Draft Analisis Awal

## 1. Pendahuluan
### 1.1 Latar Belakang
Tim Procurement saat ini membutuhkan mekanisme terpusat untuk memantau validitas dokumen legal dan administratif supplier (seperti SIUP, NIB, NPWP, Sertifikat ISO, dll). Ketiadaan sistem monitoring yang terotomatisasi menyebabkan risiko keterlambatan perpanjangan dokumen yang dapat menghambat proses pengadaan, mengganggu kepatuhan (*compliance*), atau menghentikan kerjasama operasional dengan supplier.

### 1.2 Tujuan Utama (Core Objectives)
1. **Digitalisasi Inventaris Dokumen:** Membangun database terpusat untuk menyimpan semua dokumen supplier agar tidak tersebar di berbagai folder atau email.
2. **Mitigasi Risiko Kedaluwarsa:** Mengeliminasi risiko dokumen kedaluwarsa melalui sistem peringatan dini (*early warning system*).
3. **Efisiensi Monitoring:** Mengurangi waktu manual dalam mengecek masa berlaku dokumen satu per satu.
4. **Kepatuhan (Compliance):** Memastikan seluruh supplier yang aktif memiliki dokumen yang valid sesuai standar perusahaan.

---

## 2. Identifikasi Stakeholder
| Stakeholder | Peran | Kepentingan/Kebutuhan Utama |
| :--- | :--- | :--- |
| **Procurement Staff** | User / Operator | Input data dokumen, upload file, dan menerima reminder. |
| **Procurement Manager** | Approver / Monitor | Memantau dashboard kepatuhan supplier secara keseluruhan. |
| **Vendor / Supplier** | External Party | Menyediakan dokumen terbaru (apakah sistem akan terbuka untuk vendor?). |
| **IT/System Admin** | Technical Support | Maintenance sistem, manajemen hak akses, dan konfigurasi email server. |
| **Legal/Compliance** | Auditor | Memastikan dokumen yang tersimpan sesuai dengan regulasi yang berlaku. |

---

## 3. High-Level Scope (Ruang Lingkup)

### 3.1 Fitur Utama (In-Scope)
**A. Manajemen Supplier & Dokumen:**
*   **Database Supplier:** Profil lengkap supplier (Nama, Alamat, Kategori, Kontak).
*   **Katalog Dokumen:** Pengaturan tipe dokumen (misal: NIB, NPWP, TDP) beserta masa berlaku umumnya.
*   **Repository File:** Unggah dan penyimpanan dokumen dalam format digital (PDF/JPG).
*   **Tracking Masa Aktif:** Pencatatan Tanggal Terbit dan Tanggal Kedaluwarsa.

**B. Sistem Reminder (Notifikasi):**
*   **Automated Alerts:** Pengiriman notifikasi otomatis sebelum dokumen habis masa berlakunya (misal: H-90, H-60, H-30).
*   **Multi-Channel Notification:** Notifikasi melalui Email dan/atau Dashboard In-App.
*   **Escalation Path:** Notifikasi ke Manager jika dokumen sudah kedaluwarsa namun belum diperbarui oleh staff.

**C. Dashboard & Reporting:**
*   **Status Overview:** Visualisasi jumlah dokumen yang "Valid", "Akan Kedaluwarsa", dan "Sudah Kedaluwarsa".
*   **Filter & Search:** Pencarian supplier berdasarkan status dokumen atau kategori.
*   **Export Report:** Laporan daftar dokumen yang harus diperbarui untuk dikirimkan ke supplier.

### 3.2 Di Luar Ruang Lingkup (Out-of-Scope)
*   Proses pembayaran/invoicing kepada supplier.
*   Proses tender/quotation management.
*   Verifikasi keaslian dokumen secara otomatis melalui API instansi pemerintah (kecuali ditentukan kemudian).

---

## 4. Pertanyaan Klarifikasi (Hidden Needs Identification)
*Untuk memfinalisasi dokumen teknis, saya memerlukan jawaban atas hal berikut:*

1. **Interaksi Supplier:** Apakah supplier akan mengupload dokumen mereka sendiri melalui portal khusus, atau tetap diinput secara manual oleh tim Procurement?
2. **Kustomisasi Reminder:** Apakah periode reminder (misal H-30) ingin dibuat fleksibel per tipe dokumen atau seragam untuk semua?
3. **Versioning:** Jika dokumen diperbarui, apakah dokumen lama harus tetap disimpan sebagai arsip (*versioning*) atau langsung ditimpa (*overwrite*)?
4. **Integrasi:** Apakah aplikasi ini harus terintegrasi dengan ERP yang sudah ada atau berdiri sendiri (*standalone*)?
5. **Kategori Prioritas:** Apakah ada prioritas dokumen tertentu yang jika kedaluwarsa akan langsung mengunci status supplier menjadi "Non-Aktif"?

---

## 5. Kriteria Keberhasilan (Success Metrics)
*   **Zero Missed Expirations:** Tidak ada dokumen supplier yang kedaluwarsa tanpa diketahui oleh tim Procurement.
*   **Centralized Access:** Pengurangan waktu pencarian dokumen supplier dari hitungan jam/menit menjadi hitungan detik.
*   **Timely Renewal:** Meningkatnya persentase dokumen yang diperbarui sebelum masa berlakunya habis.