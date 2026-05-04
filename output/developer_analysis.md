Sebagai Senior Product Manager, saya telah menganalisis kebutuhan pengguna Anda. Permintaan "mencatat dokumen lisensi supplier dan pengingat masa berlaku" menunjukkan adanya *pain point* utama berupa risiko operasional dan hukum jika supplier bekerja dengan dokumen yang kedaluwarsa.

Berikut adalah definisi produk terstruktur untuk pengembangan aplikasi tersebut.

---

# Product Definition: Supplier License Management System (SLMS)

## 1. Product Vision
**"Menjadi pusat kendali kepatuhan administrasi supplier yang memastikan kelangsungan operasional bisnis melalui manajemen dokumen yang terorganisir dan sistem peringatan dini yang proaktif, guna meminimalisir risiko hukum dan operasional akibat dokumen lisensi yang tidak valid."**

## 2. Target Audience
*   **Procurement/Purchasing Officer:** Pengguna utama yang menginput data dan memantau masa berlaku dokumen.
*   **Vendor Management Manager:** Pihak yang memvalidasi kelayakan supplier berdasarkan kelengkapan dokumen.
*   **Legal/Compliance Officer:** Pihak yang memastikan semua supplier mematuhi regulasi pemerintah/perusahaan.
*   **Administrator:** Pengelola sistem dan hak akses pengguna.

## 3. Core Features (Prioritized)

Saya membagi fitur ini ke dalam tiga fase prioritas menggunakan metode MoSCoW (Must have, Should have, Could have) untuk memastikan peluncuran MVP (*Minimum Viable Product*) yang efektif.

### Priority 1: Must Have (Kebutuhan Dasar/MVP)
Fitur yang wajib ada agar aplikasi dapat berfungsi sesuai permintaan utama pengguna.

| Fitur | Deskripsi | Manfaat |
| :--- | :--- | :--- |
| **Supplier Directory** | Manajemen data dasar supplier (Nama perusahaan, Alamat, Kontak, Kategori Supplier). | Sebagai basis data utama untuk mengaitkan dokumen dengan supplier tertentu. |
| **License Document Repository** | Form upload dokumen lisensi disertai kolom: Nama Dokumen, Nomor Lisensi, Tanggal Terbit, dan **Tanggal Kedaluwarsa**. | Digitalisasi dokumen agar tidak tercecer dan mudah dicari. |
| **Expiration Tracking Engine** | Sistem yang secara otomatis menghitung sisa hari menuju tanggal kedaluwarsa dokumen. | Mengidentifikasi dokumen yang akan segera tidak aktif secara *real-time*. |
| **Automated Email Notifications** | Sistem pengiriman email pengingat otomatis kepada admin/user pada H-30, H-14, dan H-7 sebelum dokumen expired. | Memastikan tidak ada dokumen yang terlewat untuk diperbarui. |
| **Dashboard Status** | Halaman utama yang menampilkan ringkasan: Jumlah dokumen aktif, dokumen yang hampir expired, dan dokumen yang sudah expired. | Memberikan visibilitas instan terhadap risiko kepatuhan. |

### Priority 2: Should Have (Peningkatan Efisiensi)
Fitur yang sangat penting untuk meningkatkan pengalaman pengguna dan efisiensi kerja.

| Fitur | Deskripsi | Manfaat |
| :--- | :--- | :--- |
| **Document Versioning** | Kemampuan untuk mengunggah dokumen baru sebagai pembaruan dari dokumen lama tanpa menghapus riwayat dokumen sebelumnya. | Menjaga audit trail dan riwayat pembaruan lisensi. |
| **Advanced Search & Filter** | Filter berdasarkan status (Aktif/Expired), kategori supplier, atau rentang tanggal kedaluwarsa. | Mempercepat pencarian dokumen di antara ratusan supplier. |
| **Supplier Portal (Basic)** | Akses terbatas bagi supplier untuk mengunggah sendiri dokumen pembaruan mereka. | Mengurangi beban administratif tim procurement dalam menginput data. |
| **Export Report** | Fitur ekspor daftar dokumen yang akan expired ke format Excel atau PDF. | Memudahkan pelaporan kepada manajemen atau tindak lanjut manual ke supplier. |

### Priority 3: Could Have (Nilai Tambah/Future Scale)
Fitur tambahan yang dapat dikembangkan setelah sistem stabil.

| Fitur | Deskripsi | Manfaat |
| :--- | :--- | :--- |
| **Approval Workflow** | Alur verifikasi dokumen yang diunggah (Pending $\rightarrow$ Verified/Rejected) sebelum status menjadi "Aktif". | Menjamin validitas dokumen yang masuk sebelum dianggap sah. |
| **Integration with ERP** | Integrasi API dengan sistem pengadaan atau ERP perusahaan yang sudah ada. | Sinkronisasi data supplier secara otomatis. |
| **Multi-level Notification** | Notifikasi melalui WhatsApp atau Push Notification selain email. | Meningkatkan kecepatan respon terhadap dokumen yang expired. |

---

## 4. Summary of User Flow (Alur Kerja Utama)
1. **Input:** User menambahkan data Supplier $\rightarrow$ User mengunggah dokumen lisensi dengan tanggal expired.
2. **Monitoring:** Sistem secara otomatis memantau tanggal expired setiap hari.
3. **Alerting:** Sistem mengirimkan email pengingat saat mencapai threshold waktu (misal: 30 hari sebelum expired).
4. **Update:** User/Supplier mengunggah dokumen baru $\rightarrow$ Sistem memperbarui tanggal expired $\rightarrow$ Status kembali menjadi "Aktif".