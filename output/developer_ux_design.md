Berikut adalah spesifikasi UX dan desain antarmuka yang mendalam untuk **Supplier License Management System (SLMS)** yang dirancang khusus untuk platform Web.

---

# UX Design Specification: Supplier License Management System (SLMS)

## 1. Strategi Desain Platform Web
Karena aplikasi ini bersifat administratif dan melibatkan manajemen data yang kompleks (tabel, dokumen, dan filter), pendekatan desain yang digunakan adalah **Enterprise Dashboard Pattern**.

**Karakteristik Utama:**
*   **Layout:** Menggunakan *Sidebar Navigation* untuk akses cepat antar modul.
*   **Density:** *Medium Density* (Keseimbangan antara ruang putih agar tidak melelahkan mata, namun tetap mampu menampilkan banyak data dalam satu layar).
*   **Responsivitas:** Fokus utama pada Desktop (Browser), namun menggunakan *Adaptive Grid* agar tetap fungsional saat diakses melalui Tablet.
*   **Interaksi:** Memaksimalkan penggunaan *Keyboard Shortcuts* (untuk input cepat) dan *Bulk Actions* (untuk manajemen dokumen massal).

---

## 2. Architecture & User Journey Maps

### A. User Flow: Registrasi Supplier & Upload Dokumen (Core Path)
`Login` $\rightarrow$ `Dashboard` $\rightarrow$ `Supplier Directory` $\rightarrow$ `Add New Supplier` $\rightarrow$ `Upload License Document` $\rightarrow$ `Set Expiry Date` $\rightarrow$ `Save`.

### B. User Flow: Monitoring & Pembaruan (Maintenance Path)
`Notification Email` $\rightarrow$ `Login` $\rightarrow$ `Dashboard (Expiring Soon Widget)` $\rightarrow$ `Supplier Detail` $\rightarrow$ `Upload New Version Document` $\rightarrow$ `Update Expiry Date` $\rightarrow$ `Status Change to Active`.

---

## 3. Detail Kebutuhan Antarmuka (Interface Requirements)

### A. Navigation Structure
Sistem navigasi menggunakan **Permanent Left Sidebar** yang terdiri dari:
*   **Dashboard:** Ringkasan status kepatuhan.
*   **Supplier Management:** Daftar seluruh supplier dan profil mereka.
*   **Document Vault:** Repositori semua dokumen lisensi (Cross-supplier view).
*   **Reports:** Export data dan analisis tren kedaluwarsa.
*   **Settings:** Pengaturan threshold notifikasi (H-30, H-14, H-7) dan manajemen user.

### B. Key Screens & UI Requirements

#### 1. Dashboard (The Control Center)
*   **Visual Indicators (KPI Cards):**
    *   Total Suppliers (Angka)
    *   Active Licenses (Hijau)
    *   Expiring Soon $\le 30$ days (Kuning - *Clickable to filter*)
    *   Expired Licenses (Merah - *Urgent/Clickable to filter*)
*   **Urgent Table:** Tabel "Top 5 Critical Expirations" yang menampilkan nama supplier, jenis dokumen, dan sisa hari (countdown).
*   **Quick Action Button:** Tombol mengapung/atas untuk "Add New Supplier".

#### 2. Supplier Directory (Data Table)
*   **UI Elements:**
    *   *Search Bar* dengan *Auto-suggest*.
    *   *Filter Chip*: Berdasarkan kategori supplier atau status validitas dokumen.
    *   *Data Table*: Kolom Nama, Kategori, Kontak, Status Kepatuhan (Icon $\checkmark$ atau $\times$), dan Action Button (View/Edit).
*   **Interaction:** Baris tabel yang dapat diklik untuk masuk ke *Supplier Detail Page*.

#### 3. Supplier Detail & Document Repository (The Heart of SLMS)
*   **Header Section:** Profil singkat supplier (Nama, Alamat, Kontak).
*   **Document Tabs:** Memisahkan dokumen berdasarkan kategori (misal: Legal, Pajak, Teknis).
*   **License Card/Row:** Setiap dokumen ditampilkan dalam baris yang berisi:
    *   Nama Dokumen & Nomor Lisensi.
    *   Thumbnail dokumen (Preview PDF/Image).
    *   Tanggal Terbit & Tanggal Kedaluwarsa.
    *   **Status Badge:** `Active` (Hijau), `Expiring Soon` (Kuning), `Expired` (Merah).
*   **Upload Modal:** Form pop-up untuk upload dokumen dengan validasi input tanggal (Date Picker) dan drag-and-drop file area.

#### 4. Versioning System (Audit Trail)
*   **UI Approach:** Saat user mengunggah dokumen baru untuk lisensi yang sama, dokumen lama tidak dihapus tetapi dipindahkan ke tab **"History/Archived"**.
*   **Requirement:** Menampilkan label "Current Version" pada dokumen terbaru dan "Obsolete" pada versi lama.

---

## 4. Platform-Specific UX Considerations (Web Optimization)

### A. Accessibility & Usability
*   **Color Contrast:** Penggunaan warna Merah (Error/Expired) dan Hijau (Success/Active) harus disertai dengan **Icon** (misal: tanda seru atau centang) untuk membantu pengguna dengan buta warna.
*   **Empty States:** Memberikan ilustrasi dan instruksi yang jelas saat layar kosong (misal: "Belum ada supplier yang dokumennya kedaluwarsa. Bagus!").
*   **Confirmation Dialogs:** Munculkan konfirmasi sebelum menghapus supplier atau dokumen untuk mencegah kehilangan data secara tidak sengaja.

### B. Form Optimization
*   **Inline Validation:** Error message muncul secara real-time saat user mengisi tanggal kedaluwarsa yang sudah lewat atau mengunggah format file yang tidak didukung.
*   **Date Picker:** Menggunakan kalender interaktif dengan penandaan batas tanggal minimum (tidak boleh sebelum tanggal terbit).

### C. Notification Experience
*   **Email Templates:** Desain email yang *actionable* (berisi tombol langsung "Update Document" yang mengarah ke halaman spesifik di web).
*   **In-App Notification:** Bell icon di pojok kanan atas yang menampilkan list peringatan terbaru.

---

## 5. Ringkasan Komponen UI (Technical Checklist)

| Komponen | Spesifikasi Web | Prioritas |
| :--- | :--- | :--- |
| **Sidebar** | Collapsible, Permanent Left | High |
| **Data Table** | Sortable, Filterable, Pagination | High |
| **Status Badge** | Color-coded (Green, Yellow, Red) | High |
| **Date Picker** | Range Selection & Single Date | High |
| **File Upload** | Drag & Drop area, Max file size limit | High |
| **Modals** | Centered overlay untuk Add/Edit data | Medium |
| **Export Button** | Dropdown trigger (CSV, PDF, XLSX) | Medium |
| **Search Bar** | Top-level Global Search | Medium |