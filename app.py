import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import time

# =========================================================
# 1. INISIALISASI DATABASE & SISTEM PENYIMPANAN DATA
# =========================================================
def init_db():
    conn = sqlite3.connect('edukomputer.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            skor INTEGER NOT NULL,
            peringatan_tab INTEGER DEFAULT 0,
            waktu_selesai TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def simpan_data(nama, kelas, skor, peringatan_tab, status="Selesai"):
    conn = sqlite3.connect('edukomputer.db')
    c = conn.cursor()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO data_siswa (nama, kelas, skor, peringatan_tab, waktu_selesai, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nama, kelas, skor, peringatan_tab, waktu, status))
    conn.commit()
    conn.close()

def ambil_semua_data():
    conn = sqlite3.connect('edukomputer.db')
    df = pd.read_sql_query("""
        SELECT nama AS 'Nama Siswa', 
               kelas AS 'Kelas', 
               skor AS 'Skor Akhir', 
               peringatan_tab AS 'Jumlah Pindah Tab/Keluar', 
               waktu_selesai AS 'Waktu Selesai', 
               status AS 'Status' 
        FROM data_siswa ORDER BY id DESC
    """, conn)
    conn.close()
    return df

init_db()

# =========================================================
# 2. BANK SOAL 20 NOMOR UNTUK MASING-MASING KELAS
# =========================================================

soal_kelas_7 = [
    {"id": 1, "soal": "1. Sinta ingin memasukkan data suara ke komputer saat belajar online. Perangkat input yang tepat digunakan adalah...", "opsi": ["A. Speaker", "B. Microphone", "C. Monitor", "D. Harddisk", "E. Proyektor"], "kunci": "B. Microphone"},
    {"id": 2, "soal": "2. Komponen hardware yang bertugas sebagai 'Otak' komputer untuk mengolah data adalah...", "opsi": ["A. RAM", "B. Harddisk", "C. CPU (Processor)", "D. Power Supply", "E. Motherboard"], "kunci": "C. CPU (Processor)"},
    {"id": 3, "soal": "3. Perangkat output yang digunakan untuk mencetak dokumen hasil tulisan ke atas kertas adalah...", "opsi": ["A. Scanner", "B. Webcam", "C. Printer", "D. Keyboard", "E. Flashdisk"], "kunci": "C. Printer"},
    {"id": 4, "soal": "4. Saat kamu menggerakkan kursor di layar komputer, perangkat input yang kamu pegang adalah...", "opsi": ["A. Monitor", "B. Mouse / Touchpad", "C. Keyboard", "D. Speaker", "E. Flashdisk"], "kunci": "B. Mouse / Touchpad"},
    {"id": 5, "soal": "5. Urutan alur kerja komputer yang benar dari penerimaan data hingga hasil akhir adalah...", "opsi": ["A. Output ➔ Pemrosesan ➔ Input ➔ Penyimpanan", "B. Input ➔ Pemrosesan ➔ Output / Penyimpanan", "C. Pemrosesan ➔ Input ➔ Output ➔ Storage", "D. Storage ➔ Output ➔ Input ➔ Pemrosesan", "E. Input ➔ Output ➔ Pemrosesan ➔ Storage"], "kunci": "B. Input ➔ Pemrosesan ➔ Output / Penyimpanan"},
    {"id": 6, "soal": "6. Tombol pada keyboard yang digunakan untuk membuat huruf kapital secara terus-menerus adalah...", "opsi": ["A. Enter", "B. Spacebar", "C. Caps Lock", "D. Backspace", "E. Shift"], "kunci": "C. Caps Lock"},
    {"id": 7, "soal": "7. Komponen visual yang menampilkan hasil gambar dan video dari komputer dinamakan...", "opsi": ["A. Scanner", "B. Monitor", "C. Keyboard", "D. Harddisk", "E. RAM"], "kunci": "B. Monitor"},
    {"id": 8, "soal": "8. Perangkat keras yang berfungsi menyimpan dokumen dan foto secara permanen dinamakan...", "opsi": ["A. RAM", "B. Processor", "C. Harddisk / SSD", "D. Power Supply", "E. VGA Card"], "kunci": "C. Harddisk / SSD"},
    {"id": 9, "soal": "9. Bagian fisik komputer yang dapat disentuh dan dilihat secara langsung disebut...", "opsi": ["A. Software", "B. Hardware", "C. Brainware", "D. Firmware", "E. Malware"], "kunci": "B. Hardware"},
    {"id": 10, "soal": "10. Pengguna atau manusia yang mengoperasikan komputer dinamakan...", "opsi": ["A. Software", "B. Hardware", "C. Brainware", "D. Groupware", "E. Freeware"], "kunci": "C. Brainware"},
    {"id": 11, "soal": "11. Alat input yang digunakan untuk mengetik angka dan huruf ke dalam komputer adalah...", "opsi": ["A. Mouse", "B. Joystick", "C. Keyboard", "D. Touchpad", "E. Trackball"], "kunci": "C. Keyboard"},
    {"id": 12, "soal": "12. Perangkat lunak yang bertugas mengelola seluruh sumber daya hardware komputer dinamakan...", "opsi": ["A. Microsoft Word", "B. Operating System (Sistem Operasi)", "C. Antivirus", "D. Google Chrome", "E. Paint"], "kunci": "B. Operating System (Sistem Operasi)"},
    {"id": 13, "soal": "13. Manakah di bawah ini yang merupakan contoh perangkat keras masukan (Input Device)?", "opsi": ["A. Speaker", "B. Printer", "C. Scanner", "D. Monitor", "E. Proyektor"], "kunci": "C. Scanner"},
    {"id": 14, "soal": "14. Manakah di bawah ini yang merupakan contoh perangkat keras keluaran (Output Device)?", "opsi": ["A. Microphone", "B. Mouse", "C. Keyboard", "D. Speaker", "E. Webcam"], "kunci": "D. Speaker"},
    {"id": 15, "soal": "15. Perangkat penyimpanan portabel kecil yang dimasukkan ke port USB komputer dinamakan...", "opsi": ["A. RAM", "B. Harddisk Internal", "C. Flashdisk", "D. ROM", "E. Processor"], "kunci": "C. Flashdisk"},
    {"id": 16, "soal": "16. Kamera kecil yang dipasang untuk mengambil gambar/video diri dinamakan...", "opsi": ["A. Scanner", "B. Webcam", "C. Touchscreen", "D. Sensors", "E. Monitor"], "kunci": "B. Webcam"},
    {"id": 17, "soal": "17. Program aplikasi yang biasa digunakan untuk mengetik tugas makalah adalah...", "opsi": ["A. Microsoft Word", "B. Windows Media Player", "C. Google Chrome", "D. Adobe Reader", "E. WinRAR"], "kunci": "A. Microsoft Word"},
    {"id": 18, "soal": "18. Tombol pada keyboard untuk menghapus satu karakter di sebelah kiri kursor adalah...", "opsi": ["A. Delete", "B. Backspace", "C. Spacebar", "D. Enter", "E. Tab"], "kunci": "B. Backspace"},
    {"id": 19, "soal": "19. Perangkat lunak yang digunakan khusus untuk menjelajahi halaman web di internet adalah...", "opsi": ["A. Web Browser", "B. Antivirus", "C. Operating System", "D. Utility Software", "E. Spreadsheet"], "kunci": "A. Web Browser"},
    {"id": 20, "soal": "20. Kabel yang menyalurkan arus listrik dari stopkontak ke komputer disebut kabel...", "opsi": ["A. LAN", "B. VGA", "C. Power / Daya", "D. HDMI", "E. Audio"], "kunci": "C. Power / Daya"}
]

soal_kelas_8 = [
    {"id": 1, "soal": "1. Memori tempat menyimpan data sementara saat program sedang berjalan di komputer adalah...", "opsi": ["A. Flashdisk", "B. RAM (Random Access Memory)", "C. Harddisk", "D. DVD-ROM", "E. SD Card"], "kunci": "B. RAM (Random Access Memory)"},
    {"id": 2, "soal": "2. Contoh Perangkat Lunak Sistem Operasi (Operating System) adalah...", "opsi": ["A. Microsoft Word", "B. Google Chrome", "C. Windows 11", "D. Adobe Photoshop", "E. CapCut"], "kunci": "C. Windows 11"},
    {"id": 3, "soal": "3. Alat input untuk mengubah dokumen foto fisik menjadi file gambar digital adalah...", "opsi": ["A. Printer", "B. Plotter", "C. Scanner", "D. Projector", "E. Joystick"], "kunci": "C. Scanner"},
    {"id": 4, "soal": "4. Perangkat lunak aplikasi yang dirancang khusus untuk mengolah kata adalah...", "opsi": ["A. Windows Media Player", "B. Microsoft Word", "C. Antivirus Avast", "D. Android OS", "E. WinRAR"], "kunci": "B. Microsoft Word"},
    {"id": 5, "soal": "5. Alat pemindai kode garis pada produk di minimarket dinamakan...", "opsi": ["A. Barcode Reader", "B. Micro Reader", "C. Plotter", "D. OCR Scanner", "E. Touch Sensor"], "kunci": "A. Barcode Reader"},
    {"id": 6, "soal": "6. Memori RAM bersifat Volatile, yang artinya...", "opsi": ["A. Data tersimpan permanen", "B. Data hilang ketika arus listrik dimatikan", "C. Data tidak bisa diubah", "D. Data tersimpan di magnetik", "E. Data terhubung ke internet"], "kunci": "B. Data hilang ketika arus listrik dimatikan"},
    {"id": 7, "soal": "7. Memori komputer yang berisi instruksi bawaan pabrik dan bersifat permanen adalah...", "opsi": ["A. RAM", "B. ROM (Read Only Memory)", "C. Cache Level 3", "D. Virtual Memory", "E. DDR4"], "kunci": "B. ROM (Read Only Memory)"},
    {"id": 8, "soal": "8. Perangkat lunak aplikasi untuk mengolah tabel, rumus angka, dan grafik adalah...", "opsi": ["A. Microsoft Excel", "B. Microsoft Word", "C. Microsoft Powerpoint", "D. Paint", "E. Notepad"], "kunci": "A. Microsoft Excel"},
    {"id": 9, "soal": "9. Sistem operasi terbuka (Open Source) yang bebas dikembangkan adalah...", "opsi": ["A. Windows 10", "B. macOS", "C. Linux", "D. iOS", "E. MS-DOS"], "kunci": "C. Linux"},
    {"id": 10, "soal": "10. Perangkat keras yang memproyeksikan tampilan komputer ke layar besar adalah...", "opsi": ["A. Scanner", "B. Proyektor", "C. Monitor", "D. Printer", "E. Webcam"], "kunci": "B. Proyektor"},
    {"id": 11, "soal": "11. Perangkat lunak yang berfungsi melindungi komputer dari serangan virus adalah...", "opsi": ["A. Operating System", "B. Antivirus", "C. Database", "D. Device Driver", "E. Firmware"], "kunci": "B. Antivirus"},
    {"id": 12, "soal": "12. Perangkat keras penyimpan data dengan piringan magnetik berputar dinamakan...", "opsi": ["A. SSD", "B. Harddisk Drive (HDD)", "C. Flashdisk", "D. SD Card", "E. RAM"], "kunci": "B. Harddisk Drive (HDD)"},
    {"id": 13, "soal": "13. Teknologi penyimpanan modern yang menggunakan chip memori flash berkecepatan tinggi adalah...", "opsi": ["A. Solid State Drive (SSD)", "B. Disket", "C. CD-ROM", "D. Magnetik Tape", "E. DVD-RW"], "kunci": "A. Solid State Drive (SSD)"},
    {"id": 14, "soal": "14. Ekstensi file standar untuk dokumen Microsoft Word terbaru adalah...", "opsi": ["A. .xlsx", "B. .docx", "C. .pptx", "D. .mp3", "E. .jpg"], "kunci": "B. .docx"},
    {"id": 15, "soal": "15. Proses memuat (*loading*) awal sistem operasi saat komputer dinyalakan dinamakan...", "opsi": ["A. Shutting down", "B. Booting", "C. Restarting", "D. Standby", "E. Hibernating"], "kunci": "B. Booting"},
    {"id": 16, "soal": "16. Komponen penyuplai arus listrik ke seluruh komponen komputer adalah...", "opsi": ["A. Motherboard", "B. Power Supply Unit (PSU)", "C. CPU", "D. Heatsink", "E. RAM"], "kunci": "B. Power Supply Unit (PSU)"},
    {"id": 17, "soal": "17. Kombinasi tombol keyboard untuk menyalin (*copy*) teks adalah...", "opsi": ["A. Ctrl + X", "B. Ctrl + C", "C. Ctrl + V", "D. Ctrl + Z", "E. Ctrl + A"], "kunci": "B. Ctrl + C"},
    {"id": 18, "soal": "18. Kombinasi tombol keyboard untuk menempelkan (*paste*) teks adalah...", "opsi": ["A. Ctrl + X", "B. Ctrl + C", "C. Ctrl + V", "D. Ctrl + S", "E. Ctrl + P"], "kunci": "C. Ctrl + V"},
    {"id": 19, "soal": "19. Perangkat lunak penghubung sistem operasi dengan hardware spesifik dinamakan...", "opsi": ["A. Driver Hardware", "B. Utility", "C. Malware", "D. Freeware", "E. Application"], "kunci": "A. Driver Hardware"},
    {"id": 20, "soal": "20. Aplikasi untuk membuat slide materi presentasi adalah...", "opsi": ["A. Microsoft Excel", "B. Microsoft PowerPoint", "C. Microsoft Access", "D. CorelDraw", "E. Photoshop"], "kunci": "B. Microsoft PowerPoint"}
]

soal_kelas_9 = [
    {"id": 1, "soal": "1. Komponen hardware khusus yang mengolah pemrosesan grafis 3D adalah...", "opsi": ["A. Sound Card", "B. VGA Card / GPU", "C. Network Card", "D. Power Supply", "E. ROM"], "kunci": "B. VGA Card / GPU"},
    {"id": 2, "soal": "2. Pernyataan yang BENAR mengenai perbedaan Hardware dan Software adalah...", "opsi": ["A. Hardware berbentuk program, Software berbentuk fisik.", "B. Hardware dapat disentuh fisik, Software adalah instruksi program.", "C. Software adalah alat penyimpanan, Hardware adalah sistem operasi.", "D. Hardware tidak membutuhkan Software.", "E. Software dapat disentuh tangan."], "kunci": "B. Hardware dapat disentuh fisik, Software adalah instruksi program."},
    {"id": 3, "soal": "3. Budi menekan tombol 'A' pada keyboard. Proses lanjutan di sistem adalah...", "opsi": ["A. Huruf 'A' tercetak di printer.", "B. Sinyal biner diproses oleh CPU.", "C. Komputer menyimpan ke Flashdisk.", "D. Speaker mengeluarkan suara.", "E. Komputer restart."], "kunci": "B. Sinyal biner diproses oleh CPU."},
    {"id": 4, "soal": "4. Papan sirkuit elektronik utama tempat terpasangnya komponen komputer dinamakan...", "opsi": ["A. Power Supply", "B. Motherboard", "C. Harddisk Case", "D. Heatsink Fan", "E. Expansion Slots"], "kunci": "B. Motherboard"},
    {"id": 5, "soal": "5. Saat komputer menyala tetapi layar monitor gelap, kendala diduga terjadi pada...", "opsi": ["A. Microphone", "B. Printer", "C. VGA Card / RAM / Kabel Monitor", "D. Flashdisk", "E. Sound Card"], "kunci": "C. VGA Card / RAM / Kabel Monitor"},
    {"id": 6, "soal": "6. Satuan kecepatan pemrosesan data pada Processor (CPU) diukur dalam...", "opsi": ["A. Megabyte (MB)", "B. Gigahertz (GHz)", "C. Gigabyte (GB)", "D. Rpm", "E. Pixel"], "kunci": "B. Gigahertz (GHz)"},
    {"id": 7, "soal": "7. Komponen pendingin kipas di atas Processor dinamakan...", "opsi": ["A. Power Supply", "B. Heatsink Fan", "C. Thermal Paste", "D. Casing Fan", "E. Water Cooler"], "kunci": "B. Heatsink Fan"},
    {"id": 8, "soal": "8. Perangkat keras jaringan untuk menghubungkan kabel LAN ke internet dinamakan...", "opsi": ["A. Sound Card", "B. NIC / LAN Card", "C. VGA Card", "D. TV Tuner", "E. Memory Card"], "kunci": "B. NIC / LAN Card"},
    {"id": 9, "soal": "9. Bagian CPU yang melakukan operasi perhitungan matematika dan logika adalah...", "opsi": ["A. Control Unit (CU)", "B. Arithmetic Logic Unit (ALU)", "C. Register", "D. Cache Memory", "E. Bus"], "kunci": "B. Arithmetic Logic Unit (ALU)"},
    {"id": 10, "soal": "10. Port konektor standar yang paling banyak digunakan untuk transfer data/daya adalah...", "opsi": ["A. Port PS/2", "B. Port USB", "C. Port Parallel", "D. Port Serial", "E. Port VGA"], "kunci": "B. Port USB"},
    {"id": 11, "soal": "11. Kabel digital modern penyuplai sinyal video high definition dan audio sekaligus adalah...", "opsi": ["A. Kabel VGA", "B. Kabel HDMI", "C. Kabel Power", "D. Kabel SATA", "E. Kabel Audio"], "kunci": "B. Kabel HDMI"},
    {"id": 12, "soal": "12. Komputer yang sering mati sendiri saat menjalankan game berat diduga mengalami...", "opsi": ["A. Harddisk Penuh", "B. Overheating (Suhu CPU terlalu panas)", "C. Mouse Rusak", "D. Keyboard Kotor", "E. Monitor Redup"], "kunci": "B. Overheating (Suhu CPU terlalu panas)"},
    {"id": 13, "soal": "13. Sistem operasi Android dikembangkan berbasiskan kernel dari...", "opsi": ["A. Windows", "B. Linux", "C. Unix", "D. MS-DOS", "E. Symbian"], "kunci": "B. Linux"},
    {"id": 14, "soal": "14. Istilah untuk memperbarui program atau sistem operasi ke versi baru dinamakan...", "opsi": ["A. Install", "B. Update / Upgrade", "C. Uninstall", "D. Format", "E. Backup"], "kunci": "B. Update / Upgrade"},
    {"id": 15, "soal": "15. Jenis kabel internal penghubung motherboard dengan SSD/HDD modern adalah...", "opsi": ["A. Kabel ATA / IDE", "B. Kabel SATA", "C. Kabel USB", "D. Kabel LAN", "E. Kabel Coaxial"], "kunci": "B. Kabel SATA"},
    {"id": 16, "soal": "16. Proses membagi ruang penyimpanan harddisk menjadi beberapa drive logis dinamakan...", "opsi": ["A. Formatting", "B. Partitioning (Partisi)", "C. Defragmenting", "D. Scanning", "E. Compressing"], "kunci": "B. Partitioning (Partisi)"},
    {"id": 17, "soal": "17. Tindakan menghapus seluruh data dan menyiapkan ulang sistem berkas dinamakan...", "opsi": ["A. Copying", "B. Formatting", "C. Cleaning", "D. Updating", "E. Downloading"], "kunci": "B. Formatting"},
    {"id": 18, "soal": "18. Bunyi bip (*beep code*) berulang saat pertama komputer dinyalakan menandakan kendala...", "opsi": ["A. Printer", "B. Hardware (RAM / VGA / Power)", "C. Software Aplikasi", "D. Mouse", "E. Sistem Operasi"], "kunci": "B. Hardware (RAM / VGA / Power)"},
    {"id": 19, "soal": "19. Perangkat pencetak dokumen berukuran sangat besar seperti baliho dinamakan...", "opsi": ["A. Dot Matrix", "B. Plotter", "C. Inkjet Printer", "D. Thermal Printer", "E. 3D Printer"], "kunci": "B. Plotter"},
    {"id": 20, "soal": "20. Tindakan membuat salinan cadangan dari data penting dinamakan...", "opsi": ["A. Restore", "B. Backup", "C. Upload", "D. Sync", "E. Import"], "kunci": "B. Backup"}
]

# =========================================================
# 3. KONFIGURASI TAMPILAN & CSS MODERN
# =========================================================
st.set_page_config(
    page_title="EduKomputer PKM - Interaktif", 
    page_icon="🖥️", 
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        padding: 12px 20px;
        border-radius: 12px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

if 'tab_warnings' not in st.session_state:
    st.session_state.tab_warnings = 0

if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

if 'show_countdown' not in st.session_state:
    st.session_state.show_countdown = False

if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False

# NAVIGASI SIDEBAR
st.sidebar.image("https://img.icons8.com/color/96/000000/monitor--v1.png", width=70)
st.sidebar.title("🎮 EduKomputer SMP")
st.sidebar.caption("Sistem Pembelajaran & Evaluasi Cara Kerja Komputer")
st.sidebar.markdown("---")

role = st.sidebar.radio(
    "📌 Pilih Mode Akses System:", 
    ["Siswa (Bermain & Kuis)", "Guru / Pengawas (Dasbor Realtime)"]
)

# ---------------------------------------------------------
# MODE A: DASBOR GURU & PENGAWASAN
# ---------------------------------------------------------
if role == "Guru / Pengawas (Dasbor Realtime)":
    st.title("👨‍🏫 Dasbor Pengawasan & Rekapitulasi Nilai Siswa")
    st.caption("Panel Sistem Integrasi Data Evaluasi Pembelajaran PKM")
    st.markdown("---")
    
    password = st.sidebar.text_input("🔑 Masukkan Kode Akses Guru:", type="password")
    
    if password == "guru123":
        st.success("Akses Diterima! Selamat Datang di Dasbor Pengelolaan Guru.")
        
        col_ref, col_null = st.columns([1, 4])
        with col_ref:
            if st.button("🔄 Perbarui Data Realtime"):
                st.rerun()
            
        df_siswa = ambil_semua_data()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Siswa Mengerjakan", f"{len(df_siswa)} Siswa")
        c2.metric("Rata-Rata Skor Kelas", f"{df_siswa['Skor Akhir'].mean():.1f}" if not df_siswa.empty else "0.0")
        c3.metric("Skor Tertinggi", f"{df_siswa['Skor Akhir'].max()}" if not df_siswa.empty else "0")
        c4.metric("Terdeteksi Pindah Tab/Keluar", f"{len(df_siswa[df_siswa['Jumlah Pindah Tab/Keluar'] > 0])}" if not df_siswa.empty else "0")
        
        st.markdown("### 📊 Tabel Hasil Ujian & Log Aktivitas Siswa")
        st.dataframe(df_siswa, use_container_width=True)
        
        if not df_siswa.empty:
            csv = df_siswa.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Unduh Rekap Laporan Nilai (Format CSV/Excel)",
                data=csv,
                file_name=f"Rekapitulasi_Nilai_PKM_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    else:
        st.warning("Silakan masukkan Kode Akses Guru yang sesuai.")

# ---------------------------------------------------------
# MODE B: APLIKASI UTAMA UNTUK SISWA
# ---------------------------------------------------------
else:
    st.title("🖥️ Game & Evaluasi: Cara Kerja Perangkat Komputer")
    st.caption("Sistem Informasi & Pengenalan Arsitektur Perangkat Keras dan Perangkat Lunak untuk Anak SMP")
    
    # ADVANCED AUDIO ENGINE + PROCTORING DETEKSI KECURANGAN
    st.components.v1.html("""
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
        const targetWin = window.parent || window;

        targetWin.getAudioContext = function() {
            if (!targetWin.audioCtx) {
                targetWin.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (targetWin.audioCtx.state === 'suspended') {
                targetWin.audioCtx.resume();
            }
            return targetWin.audioCtx;
        };

        // 1. SUARA LOGIN (CHIME / JINGLE GAUL)
        targetWin.playLoginSound = function() {
            try {
                const ctx = targetWin.getAudioContext();
                const freqs = [523.25, 659.25, 783.99, 1046.50];
                freqs.forEach((freq, idx) => {
                    setTimeout(() => {
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(freq, ctx.currentTime);
                        gain.gain.setValueAtTime(0.2, ctx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start();
                        osc.stop(ctx.currentTime + 0.3);
                    }, idx * 100);
                });
            } catch(e) {}
        };

        // 2. SUARA EFEK HITUNG MUNDUR "1, 2, 3"
        targetWin.playCountdownTone = function(noteFreq) {
            try {
                const ctx = targetWin.getAudioContext();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(noteFreq, ctx.currentTime);
                gain.gain.setValueAtTime(0.3, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.25);
            } catch(e) {}
        };

        // 3. SUARA PERINGATAN KECURANGAN / PINDAH TAB / KELUAR
        targetWin.playWarningSound = function() {
            try {
                const ctx = targetWin.getAudioContext();
                for (let i = 0; i < 3; i++) {
                    setTimeout(() => {
                        const osc = ctx.createOscillator();
                        const gain = ctx.createGain();
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(800, ctx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.25);
                        gain.gain.setValueAtTime(0.3, ctx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
                        osc.connect(gain);
                        gain.connect(ctx.destination);
                        osc.start();
                        osc.stop(ctx.currentTime + 0.25);
                    }, i * 250);
                }
            } catch(e) {}
        };

        // DETEKSI KECURANGAN KETAT
        if (!targetWin.proctoringInitialized) {
            targetWin.proctoringInitialized = true;
            
            targetWin.addEventListener("blur", function() {
                targetWin.hasLeftTab = true;
            });

            targetWin.document.addEventListener("visibilitychange", function() {
                if (targetWin.document.hidden) {
                    targetWin.hasLeftTab = true;
                }
            });

            targetWin.addEventListener("focus", function() {
                if (targetWin.hasLeftTab) {
                    targetWin.hasLeftTab = false;
                    targetWin.playWarningSound();
                    Swal.fire({
                        icon: 'warning',
                        title: '🚨 PERINGATAN SISTEM PENGAWAS!',
                        html: `
                            <div style="text-align: left; background-color: #fff5f5; padding: 15px; border-radius: 10px; border-left: 5px solid #e53e3e; margin-top: 10px;">
                                <p style="margin: 0; font-weight: bold; color: #c53030;">Aktivitas Mencurigakan Terdeteksi!</p>
                                <p style="margin-top: 5px; color: #4a5568; font-size: 14px;">
                                    Kamu terdeteksi meninggalkan halaman atau membuka tab/browser lain saat kuis berlangsung.
                                </p>
                                <hr style="border: 0; border-top: 1px solid #feb2b2; margin: 10px 0;">
                                <p style="margin: 0; font-size: 13px; color: #742a2a;">
                                    📌 <b>Catatan:</b> Pelanggaran ini dicatat dan dilaporkan ke <b>Dasbor Pengawas Guru</b>.
                                </p>
                            </div>
                        `,
                        confirmButtonText: 'Saya Mengerti & Kembali Mengerjakan',
                        confirmButtonColor: '#dd6b20',
                        allowOutsideClick: false
                    });
                }
            });

            targetWin.addEventListener("beforeunload", function (e) {
                targetWin.playWarningSound();
                var confirmationMessage = '⚠️ Apakah Anda yakin ingin keluar? Ujian yang sedang berjalan tidak akan tersimpan secara utuh.';
                (e || targetWin.event).returnValue = confirmationMessage;
                return confirmationMessage;
            });
        }
        </script>
    """, height=0)

    # 1. REGISTRASI PROFIL SISWA
    if 'siswa_nama' not in st.session_state:
        st.markdown("---")
        st.subheader("📋 Registrasi Peserta Didik")
        st.info("Silakan lengkapi identitas kamu sebelum memulai materi dan kuis interaktif.")
        
        with st.form("form_registrasi"):
            col_a, col_b = st.columns(2)
            with col_a:
                nama = st.text_input("Nama Lengkap Siswa:")
            with col_b:
                kelas = st.selectbox("Tingkat Kelas:", ["Kelas 7 SMP", "Kelas 8 SMP", "Kelas 9 SMP"])
            
            btn_submit = st.form_submit_button("🚀 Simpan Profil & Masuk Pembelajaran")
            if btn_submit and nama:
                st.session_state.siswa_nama = nama
                st.session_state.siswa_kelas = kelas
                st.session_state.play_login_sound = True
                st.rerun()
    else:
        # PANGGIL SUARA LOGIN KETIKA MASUK
        if st.session_state.get('play_login_sound', False):
            st.components.v1.html("<script>(window.parent || window).playLoginSound();</script>", height=0)
            st.session_state.play_login_sound = False

        st.success(f"👤 **Peserta Aktif:** {st.session_state.siswa_nama} | 🏫 **Tingkat:** {st.session_state.siswa_kelas}")
        
        # 2. RINGKASAN MATERI SPESIFIK BERDASARKAN KELAS
        with st.expander(f"📖 BACA MODUL MATERI PEMBELAJARAN LENGKAP - KHUSUS {st.session_state.siswa_kelas} (Klik untuk Buka/Tutup)", expanded=True):
            
            if st.session_state.siswa_kelas == "Kelas 7 SMP":
                st.markdown("""
                ### 🛠️ Modul Pembelajaran Kelas 7: Pengenalan Komputer & Perangkat Fisik (Hardware)

                #### 1. Pengertian Komputer & Sistem Komputer
                Komputer berasal dari bahasa Latin *Computare* yang artinya menghitung. Secara istilah, **Sistem Komputer** adalah sekumpulan perangkat elektronik terintegrasi yang bekerja bersama-sama untuk menerima masukan data (**Input**), mengolah data secara cepat (**Proses**), serta menghasilkan informasi yang akurat (**Output**) untuk pengguna.

                Sistem komputer terdiri dari **3 Elemen Utama**:
                * **Hardware (Perangkat Keras):** Komponen fisik komputer yang wujudnya dapat dilihat, dipegang, dan diraba secara langsung.
                * **Software (Perangkat Lunak):** Program, aplikasi, atau sekumpulan instruksi elektronik yang memberi tahu hardware apa yang harus dikerjakan.
                * **Brainware (Pengguna/Manusia):** Orang yang mengoperasikan dan mengelola komputer (seperti siswa, guru, atau programmer).

                ---

                #### 2. Kategori Perangkat Keras (Hardware) & Fungsinya

                ##### A. Perangkat Masukan (Input Device)
                Perangkat yang digunakan untuk memasukkan data mentah, teks, suara, gambar, atau sinyal perintah dari luar ke dalam sistem komputer:
                * **Keyboard:** Papan ketik berisi huruf (A-Z), angka (0-9), simbol, dan tombol fungsi (`Enter`, `Backspace`, `Caps Lock`, `Shift`).
                * **Mouse & Touchpad:** Alat penunjuk (*pointing device*) untuk menggerakkan kursor visual, mengklik ikon, dan menggulirkan (*scroll*) halaman.
                * **Microphone (Mic):** Merekam gelombang suara fisik pengguna dan mengubahnya menjadi sinyal audio digital.
                * **Scanner:** Memindai dokumen fisik, kertas tugas, atau foto cetak menjadi berkas digital.
                * **Webcam (Web Camera):** Kamera digital kecil yang menangkap gambar/video secara langsung.

                ##### B. Perangkat Pemroses (Processing Unit)
                Perangkat elektronik di dalam casing komputer yang bertugas menganalisis, menghitung, serta mengendalikan aliran data:
                * **CPU / Processor (Central Processing Unit):** Dianggap sebagai **"Otak Komputer"**. Tugas utamanya adalah mengeksekusi seluruh instruksi program.
                * **RAM (Random Access Memory):** Tempat penyimpanan data sementara ketika aplikasi sedang aktif dijalankan.

                ##### C. Perangkat Keluaran (Output Device)
                Perangkat yang berfungsi menampilkan, mencetak, atau menyajikan hasil dari data yang telah diolah oleh CPU:
                * **Monitor:** Layar tampilan yang menyajikan data visual berupa teks, gambar, dan video.
                * **Printer:** Mencetak berkas dokumen digital menjadi cetakan fisik di atas lembaran kertas.
                * **Speaker & Headphone:** Mengubah sinyal digital audio menjadi suara gelombang fisik.
                * **Proyektor (Infokus):** Memproyeksikan tampilan layar komputer ke dinding atau kain putih.

                ##### D. Perangkat Penyimpanan (Storage Device)
                Perangkat yang berfungsi menyimpan berkas, dokumen, dan aplikasi secara permanen meskipun arus listrik dimatikan:
                * **Harddisk Drive (HDD) & Solid State Drive (SSD):** Media penyimpanan internal utama.
                * **Flashdisk:** Media penyimpanan eksternal portabel yang dihubungkan melalui slot port USB.

                ---

                #### 3. Siklus Alur Kerja Komputer
                $$\text{INPUT (Masukan)} \longrightarrow \text{PEMROSESAN (Processing)} \longrightarrow \text{OUTPUT (Keluaran)} \ / \ \text{PENYIMPANAN (Storage)}$$
                """)

            elif st.session_state.siswa_kelas == "Kelas 8 SMP":
                st.markdown("""
                ### 💻 Modul Pembelajaran Kelas 8: Sistem Memori, Sistem Operasi, & Perangkat Lunak Aplikasi

                #### 1. Hirarki & Karaktekstik Sistem Memori Komputer

                ##### A. Memori Utama (Primary Memory)
                * **RAM (Random Access Memory):**
                  * **Sifat:** *Volatile* (Sementara). Seluruh data yang ada di RAM akan hilang secara otomatis ketika arus listrik dimatikan.
                  * **Fungsi:** Menyimpan data dari aplikasi yang **sedang dibuka dan aktif digunakan** agar CPU dapat mengaksesnya dengan cepat.
                * **ROM (Read Only Memory):**
                  * **Sifat:** *Non-Volatile* (Permanen). Data di dalam ROM tidak akan hilang meskipun listrik mati.
                  * **Fungsi:** Menyimpan program instruksi dasar bawaan pabrik (seperti BIOS) saat pertama kali komputer dinyalakan.

                ##### B. Memori Sekunder (Secondary Storage)
                Memori ini digunakan untuk menyimpan seluruh file, sistem operasi, dan game secara permanen (*Non-Volatile*):
                * **Harddisk Drive (HDD):** Menggunakan piringan magnetik berputar (*platter*). Memiliki kapasitas besar dengan harga terjangkau.
                * **Solid State Drive (SSD):** Menggunakan chip memori *flash* tanpa komponen berputar. Kecepatannya jauh lebih tinggi dan hemat daya.
                * **Penyimpanan Portabel:** Flashdisk, Kartu Memori (SD Card), dan External Harddisk.

                ---

                #### 2. Klasifikasi Perangkat Lunak (Software)

                ##### A. Perangkat Lunak Sistem Operasi (Operating System / OS)
                Sistem Operasi adalah perangkat lunak lapisan utama yang menjembatani komunikasi antara pengguna, aplikasi, dan hardware.
                * **Contoh OS Komputer/Laptop:** Microsoft Windows (Windows 10/11), macOS (Apple), Linux (Ubuntu).
                * **Contoh OS Smartphone:** Android (Google), iOS (Apple).

                ##### B. Perangkat Lunak Aplikasi (Application Software)
                Program yang diciptakan untuk membantu pengguna menyelesaikan tugas spesifik:
                * **Pengolah Kata:** Microsoft Word, Google Docs.
                * **Pengolah Angka:** Microsoft Excel, Google Sheets.
                * **Pengolah Presentasi:** Microsoft PowerPoint, Google Slides.
                * **Peramban Web (Web Browser):** Google Chrome, Mozilla Firefox.
                * **Keamanan & Antivirus:** Avast, Windows Defender.
                """)

            else:
                st.markdown("""
                ### 🔬 Modul Pembelajaran Kelas 9: Arsitektur Komputer Lanjut, Grafis, & Troubleshooting

                #### 1. Arsitektur Dalam CPU & Komponen Utama Motherboard

                Central Processing Unit (CPU) terdiri dari beberapa bagian internal utama:
                1. **ALU (Arithmetic Logic Unit):** Melakukan semua operasi perhitungan matematika dan perbandingan logika.
                2. **CU (Control Unit):** Mengatur lalu lintas instruksi dan mengarahkan kerja seluruh komponen komputer.
                3. **Register & Cache Memory:** Memori internal CPU berkecepatan super tinggi untuk menyimpan data sementara.

                Papan Sirkuit Utama (**Motherboard**):
                * **Socket CPU:** Tempat terpasangnya chip Processor.
                * **Slot RAM:** Tempat menancapkan modul RAM (DDR4/DDR5).
                * **Slot PCIe:** Tempat terpasangnya kartu ekspansi seperti **VGA Card / GPU** untuk pengolah visual 3D.
                * **Power Supply Unit (PSU):** Mengubah tegangan listrik AC dari stopkontak menjadi arus DC untuk motherboard.

                ---

                #### 2. Pemecahan Masalah Komputer (Troubleshooting Dasar)

                | Gejala Komputer | Kemungkinan Penyebab Utama | Langkah Solusi |
                | :--- | :--- | :--- |
                | Layar monitor tetap gelap (**No Display**). | RAM longgar/kotor, atau kabel VGA/HDMI tidak rapat. | Bersihkan pin kuningan RAM dengan penghapus lalu pasang kembali kencang. |
                | Komputer sering **mendadak mati sendiri** saat bermain game. | *Overheating* (Suhu CPU terlalu panas akibat kipas mati/pasta kering). | Bersihkan debu kipas Heatsink dan ganti *Thermal Paste* CPU. |
                | Terdengar **suara bip (*beep code*) berulang** saat komputer dinyalakan. | Kesalahan pada proses *POST* hardware (RAM, VGA, atau Power). | Periksa kembali kerapatan RAM dan kartu VGA pada motherboard. |
                """)

        st.markdown("---")
        
        # 3. TOMBOL UNTUK MEMULAI KUIS (SINKRON DENGAN ANIMASI & SUARA 1, 2, 3)
        if not st.session_state.quiz_started and not st.session_state.show_countdown and not st.session_state.quiz_finished:
            st.info("💡 **Petunjuk:** Silakan baca dan pelajari ringkasan materi di atas. Jika kamu sudah siap untuk menjawab 20 soal kuis, tekan tombol di bawah ini untuk memulai hitung mundur (1, 2, 3) dan timer pengerjaan (3 Menit).")
            if st.button("🚀 Saya Sudah Membaca & Siap Mulai Kuis Sekarang!"):
                st.session_state.show_countdown = True
                st.rerun()

        # OVERLAY ANIMASI DAN SUARA "1, 2, 3"
        elif st.session_state.show_countdown:
            st.components.v1.html("""
                <div id="countdown-container" style="
                    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                    background-color: rgba(15, 23, 42, 0.95); z-index: 99999; 
                    display: flex; flex-direction: column; justify-content: center; align-items: center; 
                    font-family: sans-serif; color: white;">
                    <div id="countdown-text" style="font-size: 110px; font-weight: 900; color: #38bdf8; text-shadow: 0 0 20px #0284c7;">3</div>
                    <div style="font-size: 24px; margin-top: 20px; color: #94a3b8; font-weight: bold;">BERSIAP-SIAP MULAI KUIS...</div>
                </div>

                <script>
                const targetWin = window.parent || window;
                const textElem = document.getElementById('countdown-text');
                
                // Urutan Angka & Nada Suara
                const steps = [
                    { num: '1', freq: 440 },
                    { num: '2', freq: 554.37 },
                    { num: '3', freq: 659.25 },
                    { num: 'GO!', freq: 880 }
                ];

                steps.forEach((step, idx) => {
                    setTimeout(() => {
                        textElem.innerHTML = step.num;
                        if (step.num === 'GO!') {
                            textElem.style.color = '#4ade80';
                            textElem.style.textShadow = '0 0 20px #16a34a';
                        }
                        if (targetWin.playCountdownTone) {
                            targetWin.playCountdownTone(step.freq);
                        }
                    }, idx * 750);
                });
                </script>
            """, height=350)
            
            time.sleep(3.2)
            st.session_state.show_countdown = False
            st.session_state.quiz_started = True
            st.rerun()
        
        elif st.session_state.quiz_started and not st.session_state.quiz_finished:
            st.subheader(f"📝 Kuis Evaluasi Khusus {st.session_state.siswa_kelas} (20 Soal)")
            st.warning("⏱️ **Waktu Berjalan!** Waktu pengerjaan kamu adalah **3 Menit (180 Detik)**.")

            # TIMER JS OTOMATIS BERHENTI KETIKA JAWABAN DIKIRIM
            st.components.v1.html("""
                <div style="background-color: #2563eb; color: white; padding: 12px; border-radius: 12px; text-align: center; font-family: sans-serif; font-weight: bold; font-size: 18px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    ⏱️ Sisa Waktu Ujian: <span id="timer" style="color: #fef08a;">03:00</span>
                </div>
                <script>
                var timeLeft = 180;
                var timerElement = document.getElementById('timer');
                var countdown = setInterval(function(){
                    var minutes = Math.floor(timeLeft / 60);
                    var seconds = timeLeft % 60;
                    if (seconds < 10) seconds = "0" + seconds;
                    timerElement.innerHTML = "0" + minutes + ":" + seconds;
                    if (timeLeft <= 0) {
                        clearInterval(countdown);
                        alert("⏱️ Waktu pengerjaan (3 Menit) telah HABIS! Silakan kirim jawaban kamu.");
                    }
                    timeLeft -= 1;
                }, 1000);
                </script>
            """, height=65)

            # PILIH SOAL BERDASARKAN KELAS
            if st.session_state.siswa_kelas == "Kelas 7 SMP":
                soal_aktif = soal_kelas_7
            elif st.session_state.siswa_kelas == "Kelas 8 SMP":
                soal_aktif = soal_kelas_8
            else:
                soal_aktif = soal_kelas_9

            # FORM KUIS DENGAN OPSI A-E
            with st.form("form_kuis_spesifik"):
                jawaban_user = {}
                
                for item in soal_aktif:
                    st.markdown(f"**{item['soal']}**")
                    jawaban_user[item['id']] = st.radio(
                        label="Pilih Jawaban:",
                        options=item['opsi'],
                        index=None,
                        key=f"q_spesifik_{item['id']}"
                    )
                    st.markdown("---")
                
                btn_kirim = st.form_submit_button("🚀 Selesaikan & Kirim Hasil Jawaban ke Dasbor Guru")

            # LOGIKA EVALUASI JAWABAN
            if btn_kirim:
                belum_dijawab = [k for k, v in jawaban_user.items() if v is None]
                
                if belum_dijawab:
                    st.error(f"⚠️ Kamu belum menjawab soal nomor: {', '.join(map(str, belum_dijawab))}. Silakan jawab seluruh soal sebelum mengirim!")
                else:
                    skor_total = 0
                    for item in soal_aktif:
                        if jawaban_user[item['id']] == item['kunci']:
                            skor_total += 5
                    
                    # Simpan Data ke Server Database SQLite
                    simpan_data(
                        nama=st.session_state.siswa_nama,
                        kelas=st.session_state.siswa_kelas,
                        skor=skor_total,
                        peringatan_tab=st.session_state.tab_warnings
                    )
                    
                    st.session_state.quiz_finished = True
                    st.session_state.skor_akhir = skor_total
                    st.session_state.play_success_sound = True
                    st.rerun()

        # TAMPILAN HASIL AKHIR (DENGAN SUARA SELESAI / FANFARE)
        elif st.session_state.quiz_finished:
            if st.session_state.get('play_success_sound', False):
                st.components.v1.html("""
                    <script>
                    const targetWin = window.parent || window;
                    try {
                        const ctx = targetWin.getAudioContext();
                        const freqs = [523.25, 659.25, 783.99, 1046.50];
                        freqs.forEach((f, idx) => {
                            setTimeout(() => {
                                const osc = ctx.createOscillator();
                                const gain = ctx.createGain();
                                osc.type = 'triangle';
                                osc.frequency.setValueAtTime(f, ctx.currentTime);
                                gain.gain.setValueAtTime(0.2, ctx.currentTime);
                                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
                                osc.connect(gain);
                                gain.connect(ctx.destination);
                                osc.start();
                                osc.stop(ctx.currentTime + 0.35);
                            }, idx * 130);
                        });
                    } catch(e) {}
                    </script>
                """, height=0)
                st.session_state.play_success_sound = False

            st.balloons()
            st.success(f"🎉 Selamat {st.session_state.siswa_nama}! Kamu telah menyelesaikan Kuis Evaluasi {st.session_state.siswa_kelas}.")
            
            col_score, col_badge = st.columns(2)
            with col_score:
                st.metric("Total Skor Akhir Kamu", f"{st.session_state.skor_akhir} / 100 Poin")
            with col_badge:
                if st.session_state.skor_akhir >= 85:
                    st.subheader("🏆 Lencana: Master Komputer Muda (Gold)")
                elif st.session_state.skor_akhir >= 70:
                    st.subheader("🥈 Lencana: Teknisi Cerdas (Silver)")
                else:
                    st.subheader("🥉 Lencana: Pemula Komputer (Bronze)")
                    
            st.info("ℹ️ Hasil jawaban dan nilai kamu telah tersimpan secara permanen ke Dasbor Pengawasan Guru. Waktu ujian telah selesai secara otomatis.")