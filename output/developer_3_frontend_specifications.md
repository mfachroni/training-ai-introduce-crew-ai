Berikut adalah **Dokumen Spesifikasi Teknis Frontend** untuk Sistem Monitoring Dokumen Supplier. Sebagai Senior Frontend Developer, saya telah menerjemahkan PRD dan Arsitektur Sistem menjadi rencana implementasi teknis yang mendetail untuk platform Web (Laravel) dan Mobile (Flutter).

---

# Spesifikasi Teknis Frontend: Sistem Monitoring Dokumen Supplier

## 1. Arsitektur Frontend Umum
Sistem ini menggunakan pendekatan **Hybrid Frontend**, di mana Laravel Blade digunakan untuk manajemen administratif yang kompleks (Web Admin), dan Flutter digunakan untuk monitoring real-time serta akses cepat (Mobile App).

### Tech Stack:
*   **Web Admin:** Laravel 10/11, Tailwind CSS, Alpine.js (untuk reaktivitas ringan), dan Blade Templating.
*   **Mobile App:** Flutter (Stable Channel), Provider/BLoC (State Management), Dio (HTTP Client).

---

## 2. Spesifikasi Web Admin (Laravel)

Web Admin difokuskan pada efisiensi input data (CRUD) dan pengelolaan repository dokumen.

### A. Struktur Komponen (Hierarchy)
Saya akan menerapkan konsep **Modular Blade Components** untuk memastikan *reusability*.

**1. Layout Components (`/resources/views/components/layout`)**
*   `AppLayout`: Wrapper utama (Sidebar, Navbar, Footer).
*   `AdminSidebar`: Navigasi berdasarkan role (Staff, Manager, Admin, Audit).
*   `TopNavbar`: User profile, Notification Dropdown, Search Bar.

**2. Shared UI Components (`/resources/views/components/ui`)**
*   `StatusBadge`: Komponen label dinamis ( Hijau: Valid, Kuning: Warning, Merah: Expired).
*   `DataTable`: Tabel dengan fitur sorting, pagination, dan filter.
*   `FormInput`: Standardized input field dengan validasi error Laravel.
*   `ModalConfirmation`: Modal untuk aksi hapus/update dokumen.

**3. Page-Specific Components (`/resources/views/pages`)**
*   **Supplier Management:** `SupplierList`, `SupplierForm`, `SupplierDetail`.
*   **Document Repository:** `DocumentUploadForm`, `DocumentPreviewer`, `DocumentHistoryLog`.
*   **Dashboard:** `StatCard` (Aggregate data), `ExpiringChart` (Grafik dokumen akan expired).

### B. State Management & Data Flow (Web)
Karena menggunakan Server-Side Rendering (SSR) dengan Laravel Blade:
*   **Server-State:** State dikelola oleh Laravel Controller dan dikirim melalui View Data.
*   **Client-State:** Menggunakan **Alpine.js** untuk state ringan di browser (misal: buka/tutup modal, toggle dropdown, filter tabel tanpa reload).
*   **File Handling:** Menggunakan `multipart/form-data` untuk upload dokumen langsung ke Storage Laravel.

---

## 3. Spesifikasi Mobile App (Flutter)

Aplikasi mobile difokuskan pada *Executive Summary*, Notifikasi, dan Preview Dokumen.

### A. Struktur Komponen & Folder (Clean Architecture)
Saya akan menerapkan struktur folder berdasarkan fitur (**Feature-first folder structure**).

```text
lib/
├── core/                # Utilitas global, konstanta, tema, network_client (Dio)
├── shared/              # Widget yang digunakan berulang (CustomButton, StatusChip)
├── features/
│   ├── auth/            # Login, Logout, Session Management
│   ├── dashboard/      # Ringkasan status (Valid, Warning, Expired)
│   ├── monitoring/      # List dokumen yang akan expired, Search Supplier
│   ├── notifications/  # Notification Center, Push Notification Logic
│   └── document_view/   # PDF Viewer, Signed URL Handler
└── main.dart
```

### B. Hierarki Widget (Component Hierarchy)
*   **Dashboard Page**
    *   `SummaryCardGrid` $\rightarrow$ `SummaryCard` (Card warna-warni untuk status).
    *   `QuickActionList` $\rightarrow$ List akses cepat ke dokumen kritis.
*   **Monitoring Page**
    *   `SearchHeader` $\rightarrow$ TextField dengan filter kategori.
    *   `DocumentList` $\rightarrow$ `DocumentTile` (Menampilkan nama supplier, type doc, dan countdown expiry).
*   **Notification Page**
    *   `NotificationList` $\rightarrow$ `NotificationItem` (Badge unread/read).
*   **Document Detail Page**
    *   `PDFPreviewWindow` $\rightarrow$ Integrasi `flutter_pdfview`.
    *   `DocumentMetadata` $\rightarrow$ Detail tanggal terbit dan kedaluwarsa.

### C. State Management (Flutter)
Saya memilih **BLoC (Business Logic Component)** untuk skala produksi karena pemisahan logika yang sangat jelas (Event $\rightarrow$ Bloc $\rightarrow$ State).

*   **AuthBloc:** Mengelola token JWT/Sanctum, status login, dan persistensi user di `shared_preferences`.
*   **DashboardBloc:** Mengambil data aggregasi statistik dari `/dashboard/summary`.
*   **DocumentBloc:** Mengelola list dokumen, status filtering, dan fetch Signed URL untuk preview.
*   **NotificationBloc:** Menangani stream notifikasi dari Firebase Cloud Messaging (FCM) dan mengupdate status *read/unread*.

---

## 4. Strategi Integrasi Frontend $\rightarrow$ Backend

### A. Komunikasi Data
*   **Web $\rightarrow$ Laravel:** Request via Standard HTTP Post/Get melalui Route Laravel.
*   **Mobile $\rightarrow$ Laravel:** Konsumsi REST API menggunakan `Dio`.
    *   **Interceptor:** Menambahkan Header `Authorization: Bearer {token}` secara otomatis.
    *   **Error Handler:** Mapping response 401 (Unauthorized) untuk otomatis trigger `AuthBloc` logout.

### B. Penanganan Dokumen (Security)
Frontend **TIDAK AKAN** menyimpan URL file secara permanen. Alurnya adalah:
1. Flutter/Web meminta akses file $\rightarrow$ `/documents/{id}`.
2. Backend mengirimkan **Temporary Signed URL** (valid 15 menit).
3. Frontend menampilkan file menggunakan URL tersebut.
4. Setelah URL expired, frontend harus meminta ulang Signed URL.

---

## 5. Matriks Pemetaan UI/UX

| Fitur | Implementasi Web (Laravel) | Implementasi Mobile (Flutter) | State Management |
| :--- | :--- | :--- | :--- |
| **Input Supplier** | Form Lengkap $\rightarrow$ Blade Component | (Read Only / Detail View) | Server-Side |
| **Upload Dokumen** | Drag & Drop File Upload $\rightarrow$ Livewire/Blade | (Tidak Tersedia/Read-only) | Server-Side |
| **Monitoring Status**| Table View $\rightarrow$ Filterable $\rightarrow$ Export Excel | Summary Cards $\rightarrow$ Vertical List | BLoC / Alpine.js |
| **Notifikasi** | Notification Bell $\rightarrow$ Dropdown | Push Notification $\rightarrow$ FCM $\rightarrow$ List Page | BLoC / Session |
| **Preview Dokumen** | PDF Embed $\rightarrow$ Browser Viewer | `flutter_pdfview` $\rightarrow$ Fullscreen Mode | BLoC (Signed URL) |

## 6. Definisi Warna State (UI Theme)
Untuk konsistensi antara Web dan Mobile, saya menetapkan standar warna status:
*   **Valid (Green):** Web: `#10B981` (Emerald 500) | Mobile: `Colors.green`
*   **Warning (Yellow):** Web: `#F59E0B` (Amber 500) | Mobile: `Colors.amber`
*   **Expired (Red):** Web: `#EF4444` (Red 500) | Mobile: `Colors.red`