# Product Requirement Document (PRD)
**Proyek:** Sistem Monitoring Dokumen Supplier & Notifikasi Masa Aktif

| Versi | Status | Penulis | Tanggal | Catatan |
| :--- | :--- | :--- | :--- | :--- |
| v1.0 | Draft | Senior Business Analyst | 24 Mei 2024 | Initial PRD based on analysis |

---

## 1. Visi Produk (Product Vision)
Menciptakan ekosistem manajemen dokumen supplier yang terpusat, transparan, dan proaktif guna mengeliminasi risiko operasional akibat dokumen yang kedaluwarsa. Sistem ini bertujuan untuk mentransformasi proses monitoring manual menjadi otomatis, sehingga Tim Procurement dapat fokus pada manajemen strategis daripada administrasi dokumen.

## 2. Tujuan Bisnis (Business Goals)
Tujuan utama dari pengembangan sistem ini adalah:
*   **Mitigasi Risiko Kepatuhan:** Memastikan 100% supplier aktif memiliki dokumen legal yang valid sesuai regulasi perusahaan dan pemerintah.
*   **Keunggulan Operasional:** Mengurangi waktu yang dihabiskan staf Procurement dalam melakukan audit manual masa berlaku dokumen.
*   **Kontinuitas Bisnis:** Menghindari penghentian kerjasama mendadak dengan supplier kritis akibat dokumen yang tidak terperbarui tepat waktu.
*   **Digitalisasi Arsip:** Membangun satu sumber kebenaran (*Single Source of Truth*) untuk seluruh dokumen administrasi supplier.

## 3. Target Pengguna (User Personas)
| Persona | Peran | Kebutuhan Utama |
| :--- | :--- | :--- |
| **Procurement Staff** | Operator | Mengelola input data, mengunggah dokumen, dan menindaklanjuti reminder kedaluwarsa. |
| **Procurement Manager** | Supervisor | Memantau tingkat kepatuhan supplier secara keseluruhan melalui dashboard. |
| **IT Administrator** | Support | Mengelola hak akses pengguna dan konfigurasi sistem notifikasi. |
| **Audit/Legal** | Reviewer | Memastikan kelengkapan dokumen sesuai standar kepatuhan perusahaan. |

## 4. Fitur Utama (Core Features)

### 4.1 Manajemen Database Supplier & Dokumen
Sistem harus mampu mengelola informasi supplier dan dokumen terkait secara terstruktur.
*   **Profil Supplier:** Penyimpanan data dasar (Nama Perusahaan, Alamat, Kategori Supplier, Kontak PIC).
*   **Katalog Tipe Dokumen:** Kemampuan untuk menentukan jenis dokumen (misal: NIB, NPWP, ISO) dan menentukan masa berlaku umum untuk tiap tipe.
*   **Digital Repository:** Fungsi unggah (*upload*) file dalam format PDF/JPG dengan penyimpanan yang terorganisir per supplier.
*   **Tracking Masa Berlaku:** Input tanggal terbit dan tanggal kedaluwarsa untuk setiap dokumen yang diunggah.

### 4.2 Sistem Notifikasi Otomatis (Early Warning System)
Sistem peringatan dini untuk mencegah terlewatnya masa berlaku dokumen.
*   **Trigger Notifikasi:** Pengiriman pengingat otomatis berdasarkan parameter waktu (contoh: H-90, H-60, H-30 sebelum tanggal kedaluwarsa).
*   **Multi-Channel Alert:** Notifikasi dikirimkan melalui Email dan muncul pada *notification center* di dalam aplikasi.
*   **Alur Eskalasi:** Jika dokumen telah melewati tanggal kedaluwarsa dan belum diperbarui, sistem secara otomatis mengirimkan notifikasi eskalasi kepada Procurement Manager.

### 4.3 Dashboard Monitoring & Pelaporan
Visualisasi data untuk pengambilan keputusan cepat.
*   **Executive Dashboard:** Grafik ringkasan status dokumen (Valid, Akan Kedaluwarsa, Kedaluwarsa).
*   **Advanced Filtering:** Pencarian supplier berdasarkan status dokumen, kategori, atau nama.
*   **Export Report:** Kemampuan mengunduh laporan daftar dokumen yang需要 diperbarui dalam format Excel/CSV untuk dikirimkan kepada supplier.

## 5. Alur Kerja Utama (User Workflow)
1. **Input:** Staff Procurement membuat profil supplier $\rightarrow$ Mengunggah dokumen $\rightarrow$ Menginput tanggal kedaluwarsa.
2. **Monitoring:** Sistem melakukan scanning harian terhadap tanggal kedaluwarsa.
3. **Notification:** Sistem mengirim email reminder kepada Staff Procurement saat memasuki periode H-90/60/30.
4. **Update:** Staff meminta dokumen baru dari supplier $\rightarrow$ Mengunggah dokumen terbaru $\rightarrow$ Memperbarui tanggal kedaluwarsa.
5. **Audit:** Manager melihat dashboard untuk memantau supplier mana yang masih memiliki dokumen kedaluwarsa.

## 6. Kriteria Keberhasilan (Success Metrics)
| Metrik | Target | Cara Pengukuran |
| :--- | :--- | :--- |
| **Missed Expiration Rate** | 0% | Jumlah dokumen kedaluwarsa yang tidak terdeteksi oleh sistem. |
| **Search Efficiency** | < 10 detik | Waktu yang dibutuhkan untuk menemukan dokumen spesifik milik supplier. |
| **Renewal Lead Time** | $\ge$ H-30 | Persentase dokumen yang diperbarui sebelum tanggal kedaluwarsa tiba. |

## 7. Batasan & Asumsi (Constraints & Assumptions)
*   **Scope:** Sistem ini hanya fokus pada monitoring dokumen, tidak mencakup proses transaksi keuangan/Pembayaran.
*   **Integrasi:** Saat ini diasumsikan sebagai sistem *standalone* (berdiri sendiri) kecuali ada permintaan integrasi ke ERP.
*   **Input Data:** Dokumen diunggah secara manual oleh internal Procurement (tidak ada portal mandiri untuk supplier pada fase ini).