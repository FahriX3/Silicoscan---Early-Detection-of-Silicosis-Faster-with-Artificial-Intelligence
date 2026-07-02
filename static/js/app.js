/**
 * app.js — Silicoscan Frontend Logic
 * =====================================
 * Drag & drop, API integration, results rendering, i18n support.
 */

// ==================== I18N (Bilingual) ====================
const translations = {
    id: {
        // Nav
        "nav.home": "Beranda",
        "nav.about": "Tentang",
        "nav.screening": "Skrining",
        "nav.team": "Tim",
        "nav.contact": "Kontak",
        // Hero
        "hero.label": "Skrining Kesehatan Pekerja Tambang",
        "hero.title1": "Deteksi Dini ",
        "hero.title2": "Silikosis",
        "hero.title3": " Lebih Cepat dengan Kecerdasan Buatan",
        "hero.subtitle": "AI-Driven Early Detection Tool untuk skrining silikosis pada pekerja tambang. Upload foto rontgen dada untuk analisis otomatis menggunakan 2 model AI.",
        "hero.cta_start": "Mulai Skrining →",
        "hero.cta_about": "Pelajari Lebih Lanjut",
        // Features
        "features.tag": "Teknologi",
        "features.title": "Pipeline AI Dua Tahap",
        "features.subtitle": "Dua model deep learning yang saling melengkapi untuk hasil skrining yang komprehensif",
        "features.f1_title": "Segmentasi Paru (U-Net)",
        "features.f1_desc": "Model U-Net dengan backbone ResNet34 memisahkan area paru-paru dari background untuk memfokuskan analisis pada region of interest.",
        "features.f2_title": "Deteksi Lokasi Lesi (YOLO11)",
        "features.f2_desc": "YOLO11 mendeteksi dan menandai lokasi spesifik lesi. Tersedia 2 opsi model: Biasa (3 kelas) dan Full (11 kelas).",
        // How
        "how.tag": "Alur Kerja",
        "how.title": "Cara Kerja Sistem",
        "how.s1_title": "Upload X-Ray",
        "how.s1_desc": "Upload foto rontgen dada (format JPG, PNG). Sistem akan otomatis melakukan pre-processing.",
        "how.s2_title": "Analisis AI",
        "how.s2_desc": "Model AI melakukan segmentasi dan deteksi secara otomatis dalam hitungan detik.",
        "how.s3_title": "Hasil Skrining",
        "how.s3_desc": "Lihat hasil deteksi, tingkat keyakinan AI, dan lokasi abnormalitas yang terdeteksi.",
        // About
        "about.tag": "Tentang Penelitian",
        "about.title": "Deteksi Dini Silikosis pada Pekerja Tambang Menggunakan Pendekatan Kecerdasan Buatan",
        "about.p1": "Penelitian ini dilatarbelakangi oleh tingginya risiko penyakit akibat kerja, khususnya silikosis, pada pekerja tambang yang disebabkan oleh paparan kronis debu silika serta keterbatasan sistem deteksi dini yang masih bergantung pada metode konvensional.",
        "about.p2": "Silikosis merupakan penyakit progresif yang tidak dapat disembuhkan, sehingga deteksi dini menjadi sangat penting untuk mencegah komplikasi lebih lanjut. Model yang dihasilkan diintegrasikan ke dalam prototipe sistem berbasis web yang mampu melakukan prediksi risiko serta mendukung pengambilan keputusan dalam konteks keselamatan dan kesehatan kerja (K3).",
        "about.stat1": "Model AI",
        "about.stat2": "Opsi Model",
        "about.stat3": "Tipe Deteksi Lesi",
        "about.stat4": "Waktu Analisis",
        // Screening
        "screen.tag": "AI Screening",
        "screen.title": "Analisis Rontgen Dada",
        "screen.subtitle": "Upload foto rontgen dada untuk analisis otomatis menggunakan dua model AI",
        "screen.disclaimer": '<strong>Disclaimer — Alat Bantu Skrining</strong>Hasil analisis AI ini bersifat sebagai alat bantu skrining awal dan <strong>bukan</strong> pengganti diagnosis medis profesional. Selalu konsultasikan hasil dengan dokter atau tenaga medis yang berkompeten.',
        "screen.upload_title": "Upload Foto Rontgen Dada",
        "screen.upload_sub": "Drag & drop file atau klik untuk memilih",
        "screen.upload_btn": "Pilih File",
        "screen.analyze": "Mulai Analisis",
        "screen.cancel": "✕",
        "screen.analyzing": "Sedang Menganalisis...",
        "screen.preparing": "Mempersiapkan gambar...",
        "screen.error_detail": "Silakan coba lagi dengan gambar rontgen yang valid",
        "screen.retry": "Coba Lagi",
        "screen.select_model": "Pilih Model Deteksi:",
        "screen.model_biasa": "Model Alpha",
        "screen.model_full": "Model Beta",
        // Team
        "team.tag": "Tim Kami",
        "team.title": "Tim Peneliti",
        "team.subtitle": "Departemen Layanan dan Informasi Kesehatan, Sekolah Vokasi, Universitas Gadjah Mada",
        "team.lead": "Ketua Peneliti",
        "team.researcher": "Peneliti",
        "team.it": "Tim IT",
        "team.dept": "Departemen Layanan dan Informasi Kesehatan",
        "team.dept_it": "Pengembang Sistem & AI Engineer",
        // Partners
        "partners.tag": "Mitra Afiliasi",
        "partners.title": "Mitra Afiliasi",
        "partners.sv": "Sekolah Vokasi UGM",
        // Contact
        "contact.tag": "Hubungi Kami",
        "contact.title": "Hubungi Kami",
        "contact.address_label": "Alamat",
        "contact.phone_label": "Telepon",
        // Footer
        "footer.desc": "AI-Driven Early Detection Tool untuk skrining silikosis pada pekerja tambang. Prototipe sistem berbasis web untuk keselamatan dan kesehatan kerja (K3).",
        "footer.nav": "Navigasi",
        "footer.tech": "Teknologi",
        "footer.rights": "Hak cipta dilindungi.",
        // Results (used in JS)
        "result.confidence": "Tingkat Keyakinan AI",
        "result.total_time": "Total analisis",
        "result.detection_title": "Deteksi Lokasi Lesi",
        "result.areas": "area",
        "result.download": "Download Hasil",
        "result.original": "Gambar Original",
        "result.annotated": "Hasil Deteksi AI",
        "result.masked": "Segmentasi Paru",
        "result.image_analysis": "Gambar Analisis",
        "result.process_detail": "Rincian Proses AI",
        "result.new_analysis": "Analisis Gambar Baru",
        "result.no_detection": "Tidak ada lesi spesifik yang terdeteksi pada threshold saat ini.",
        // Steps
        "step.masking": "Melakukan segmentasi paru-paru...",
        "step.detecting": "Mendeteksi lokasi abnormalitas...",
    },
    en: {
        "nav.home": "Home",
        "nav.about": "About",
        "nav.screening": "Screening",
        "nav.team": "Team",
        "nav.contact": "Contact",
        "hero.label": "Mining Workers Health Screening",
        "hero.title1": "Early Detection of ",
        "hero.title2": "Silicosis",
        "hero.title3": " Faster with Artificial Intelligence",
        "hero.subtitle": "AI-Driven Early Detection Tool for silicosis screening in mining workers. Upload a chest X-ray for automated analysis using 2 AI models.",
        "hero.cta_start": "Start Screening →",
        "hero.cta_about": "Learn More",
        "features.tag": "Technology",
        "features.title": "Two-Stage AI Pipeline",
        "features.subtitle": "Two complementary deep learning models for comprehensive screening results",
        "features.f1_title": "Lung Segmentation (U-Net)",
        "features.f1_desc": "U-Net model with ResNet34 backbone isolates lung areas from the background to focus analysis on the region of interest.",
        "features.f2_title": "Lesion Detection (YOLO11)",
        "features.f2_desc": "YOLO11 detects and marks specific lesion locations. 2 models available: Basic (3 classes) and Full (11 classes).",
        "how.tag": "Workflow",
        "how.title": "How It Works",
        "how.s1_title": "Upload X-Ray",
        "how.s1_desc": "Upload a chest X-ray image (JPG, PNG format). The system will automatically pre-process it.",
        "how.s2_title": "AI Analysis",
        "how.s2_desc": "AI models perform segmentation and detection automatically in seconds.",
        "how.s3_title": "Screening Results",
        "how.s3_desc": "View detection results, AI confidence levels, and detected abnormality locations.",
        "about.tag": "About the Research",
        "about.title": "Early Detection of Silicosis in Mining Workers Using Artificial Intelligence",
        "about.p1": "This research is motivated by the high risk of occupational diseases, particularly silicosis, in mining workers caused by chronic exposure to silica dust and the limitations of early detection systems that still rely on conventional methods.",
        "about.p2": "Silicosis is a progressive and incurable disease, making early detection crucial to prevent further complications. The resulting model is integrated into a web-based prototype system capable of risk prediction and supporting decision-making in the context of occupational safety and health (K3).",
        "about.stat1": "AI Models",
        "about.stat2": "Model Options",
        "about.stat3": "Lesion Detection Types",
        "about.stat4": "Analysis Time",
        "screen.tag": "AI Screening",
        "screen.title": "Chest X-Ray Analysis",
        "screen.subtitle": "Upload a chest X-ray for automated analysis using two AI models",
        "screen.disclaimer": '<strong>Disclaimer — Screening Tool</strong>This AI analysis is intended as an initial screening aid and is <strong>not</strong> a substitute for professional medical diagnosis. Always consult results with a qualified physician.',
        "screen.upload_title": "Upload Chest X-Ray",
        "screen.upload_sub": "Drag & drop file or click to select",
        "screen.upload_btn": "Choose File",
        "screen.analyze": "Analyze",
        "screen.cancel": "✕",
        "screen.analyzing": "Analyzing...",
        "screen.preparing": "Preparing image...",
        "screen.error_detail": "Please try again with a valid chest X-ray image",
        "screen.retry": "Try Again",
        "screen.select_model": "Select Detection Model:",
        "screen.model_biasa": "Model Alpha",
        "screen.model_full": "Model Beta",
        "team.tag": "Our Team",
        "team.title": "Research Team",
        "team.subtitle": "Department of Health Services and Information, Vocational School, Universitas Gadjah Mada",
        "team.lead": "Principal Investigator",
        "team.researcher": "Researcher",
        "team.it": "IT Team",
        "team.dept": "Dept. of Health Services and Information",
        "team.dept_it": "System Developer & AI Engineer",
        "partners.tag": "Affiliating Partners",
        "partners.title": "Affiliating Partners",
        "partners.sv": "Vocational School UGM",
        "contact.tag": "Contact Us",
        "contact.title": "Contact Us",
        "contact.address_label": "Address",
        "contact.phone_label": "Phone",
        "footer.desc": "AI-Driven Early Detection Tool for silicosis screening in mining workers. A web-based prototype system for occupational safety and health (K3).",
        "footer.nav": "Navigation",
        "footer.tech": "Technology",
        "footer.rights": "All rights reserved.",
        "result.confidence": "AI Confidence Level",
        "result.total_time": "Total analysis",
        "result.detection_title": "Lesion Location Detection",
        "result.areas": "areas",
        "result.download": "Download Result",
        "result.original": "Original Image",
        "result.annotated": "AI Detection Result",
        "result.masked": "Lung Segmentation",
        "result.image_analysis": "Analysis Images",
        "result.process_detail": "AI Process Details",
        "result.new_analysis": "Analyze New Image",
        "result.no_detection": "No specific lesions detected at the current threshold.",
        "step.masking": "Segmenting lungs...",
        "step.detecting": "Detecting abnormality locations...",
    },
};

let currentLang = 'id';

function t(key) {
    return (translations[currentLang] && translations[currentLang][key]) || key;
}

function switchLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const val = translations[lang] && translations[lang][key];
        if (val) {
            if (key === 'screen.disclaimer') {
                el.innerHTML = val;
            } else {
                el.textContent = val;
            }
        }
    });
    document.documentElement.lang = lang === 'id' ? 'id' : 'en';
}

function toggleMobileNav() {
    const nav = document.getElementById('navbar-nav');
    const toggle = document.getElementById('nav-toggle');
    const overlay = document.getElementById('mobile-overlay');
    const isOpen = nav.classList.contains('mobile-open');

    if (isOpen) {
        closeMobileNav();
    } else {
        nav.classList.add('mobile-open');
        toggle.classList.add('active');
        if (overlay) overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeMobileNav() {
    const nav = document.getElementById('navbar-nav');
    const toggle = document.getElementById('nav-toggle');
    const overlay = document.getElementById('mobile-overlay');
    nav.classList.remove('mobile-open');
    toggle.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Close mobile menu when a nav link is clicked
document.querySelectorAll('#navbar-nav a').forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            closeMobileNav();
        }
    });
});

// Sync language switchers (desktop ↔ mobile)
function syncLangSwitchers(val) {
    const desktop = document.getElementById('lang-switcher');
    const mobile = document.getElementById('mobile-lang-switcher');
    if (desktop) desktop.value = val;
    if (mobile) mobile.value = val;
}

// Close mobile menu on window resize to desktop
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        closeMobileNav();
    }
});

// ==================== STATE ====================
let selectedFile = null;
let isAnalyzing = false;

// ==================== DOM ====================
const uploadZone = document.getElementById('upload-zone');
const fileInput = document.getElementById('file-input');
const previewSection = document.getElementById('preview-section');
const previewImage = document.getElementById('preview-image');
const previewFilename = document.getElementById('preview-filename');
const previewMeta = document.getElementById('preview-meta');
const btnAnalyze = document.getElementById('btn-analyze');
const btnReset = document.getElementById('btn-reset');
const processingSection = document.getElementById('processing-section');
const resultsSection = document.getElementById('results-section');
const errorCard = document.getElementById('error-card');

// ==================== UPLOAD ====================
uploadZone.addEventListener('click', () => { if (!isAnalyzing) fileInput.click(); });

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
});

uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', () => { uploadZone.classList.remove('dragover'); });
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    const validExts = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!validExts.includes(ext)) { showToast('Format file tidak didukung.', 'error'); return; }
    if (file.size > 30 * 1024 * 1024) { showToast('File terlalu besar (max 30MB)', 'error'); return; }

    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => { previewImage.src = e.target.result; };
    reader.readAsDataURL(file);

    previewFilename.textContent = file.name;
    previewMeta.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB • ${ext.toUpperCase().slice(1)}`;

    uploadZone.style.display = 'none';
    previewSection.classList.add('active');
    resultsSection.classList.remove('active');
    errorCard.classList.remove('active');
    processingSection.classList.remove('active');
}

btnReset.addEventListener('click', resetState);

function resetState() {
    selectedFile = null;
    isAnalyzing = false;
    fileInput.value = '';
    uploadZone.style.display = '';
    previewSection.classList.remove('active');
    processingSection.classList.remove('active');
    resultsSection.classList.remove('active');
    errorCard.classList.remove('active');
    resetSteps();
}

// ==================== ANALYSIS ====================
btnAnalyze.addEventListener('click', startAnalysis);

async function startAnalysis() {
    if (!selectedFile || isAnalyzing) return;
    isAnalyzing = true;
    btnAnalyze.disabled = true;
    btnAnalyze.textContent = '⏳ ...';

    previewSection.classList.remove('active');
    processingSection.classList.add('active');
    resultsSection.classList.remove('active');
    errorCard.classList.remove('active');
    resetSteps();
    await animateStep(0);

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const modelSelect = document.getElementById('model-type');
        if (modelSelect) {
            formData.append('model_type', modelSelect.value);
        }

        const stepPromise = (async () => { await sleep(800); await animateStep(1); })();

        const response = await fetch('/api/analyze', { method: 'POST', body: formData });
        await stepPromise;

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `HTTP ${response.status}`);
        }

        const result = await response.json();
        if (!result.success) throw new Error(result.error || 'Analysis failed');

        if (result.detection && result.detection.performed) {
            completeStep(1);
        } else {
            skipStep(1);
        }

        completeStep(0);
        await sleep(500);
        showResults(result);
    } catch (error) {
        console.error(error);
        showError(error.message);
    } finally {
        isAnalyzing = false;
        btnAnalyze.disabled = false;
        btnAnalyze.textContent = t('screen.analyze');
    }
}

// ==================== STEPS ====================
function resetSteps() {
    for (let i = 0; i <= 1; i++) {
        const c = document.getElementById(`step-circle-${i}`);
        const l = document.getElementById(`step-label-${i}`);
        if (c) { c.className = 'step-circle'; c.innerHTML = ['<i class="fas fa-lungs"></i>', '<i class="fas fa-search-plus"></i>'][i]; }
        if (l) l.className = 'step-label';
    }
    document.querySelectorAll('.step-connector').forEach(c => c.classList.remove('done'));
}

async function animateStep(idx) {
    const c = document.getElementById(`step-circle-${idx}`);
    const l = document.getElementById(`step-label-${idx}`);
    if (c) c.classList.add('active');
    if (l) l.classList.add('active');
    const texts = [t('step.masking'), t('step.detecting')];
    const sub = document.getElementById('processing-subtitle');
    if (sub) sub.textContent = texts[idx] || '';
}

function completeStep(idx) {
    const c = document.getElementById(`step-circle-${idx}`);
    const l = document.getElementById(`step-label-${idx}`);
    if (c) { c.classList.remove('active'); c.classList.add('done'); c.innerHTML = '<i class="fas fa-check"></i>'; }
    if (l) { l.classList.remove('active'); l.classList.add('done'); }
    const conn = document.getElementById(`step-connector-${idx}`);
    if (conn) conn.classList.add('done');
}

function skipStep(idx) {
    const c = document.getElementById(`step-circle-${idx}`);
    const l = document.getElementById(`step-label-${idx}`);
    if (c) { c.classList.remove('active'); c.classList.add('skipped'); c.innerHTML = '—'; }
    if (l) l.classList.remove('active');
}

// ==================== RESULTS ====================
function showResults(result) {
    processingSection.classList.remove('active');
    resultsSection.classList.add('active');
    resultsSection.innerHTML = buildResultsHTML(result);
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function buildResultsHTML(result) {
    const det = result.detection;
    const isNormal = result.is_normal;
    let html = '';

    // Classification
    if (isNormal) {
        html += `
        <div class="result-card">
            <div class="result-header">
                <div class="result-badge success">✅</div>
                <div>
                    <div class="result-title">Paru-paru Normal</div>
                    <div class="result-subtitle">Tidak ada indikasi abnormalitas atau lesi yang terdeteksi oleh AI. Paru-paru terlihat dalam kondisi baik.</div>
                </div>
            </div>
            <div class="time-badge">⏱️ ${t('result.total_time')}: ${(result.total_time_ms / 1000).toFixed(1)}s</div>
        </div>`;
    } else {
        html += `
        <div class="result-card">
            <div class="result-header">
                <div class="result-badge danger">⚠️</div>
                <div>
                    <div class="result-title">Terdeteksi Abnormalitas</div>
                    <div class="result-subtitle">AI mendeteksi adanya indikasi abnormalitas pada area paru-paru. Silakan periksa detail deteksi di bawah ini.</div>
                </div>
            </div>
            <div class="time-badge">⏱️ ${t('result.total_time')}: ${(result.total_time_ms / 1000).toFixed(1)}s</div>
        </div>`;
    }

    // Detection
    if (det.performed) {
        html += `
        <div class="detection-card">
            <div class="detection-header">
                <div class="detection-title">
                    🔍 ${t('result.detection_title')}
                    <span class="detection-count">${det.num_detections} ${t('result.areas')}</span>
                </div>
                ${result.download_id ? `<a href="/api/download/${result.download_id}" class="btn-download" download>${t('result.download')}</a>` : ''}
            </div>
            <div class="image-comparison">
                <div class="image-panel">
                    <div class="image-panel-header">📷 ${t('result.original')}</div>
                    <img src="data:image/jpeg;base64,${result.images.original}" alt="Original" />
                </div>
                <div class="image-panel">
                    <div class="image-panel-header">🔍 ${t('result.annotated')}</div>
                    <img src="data:image/jpeg;base64,${result.images.annotated}" alt="Detection" />
                </div>
            </div>
            ${det.detections.length > 0 ? `
                <div class="detection-list">
                    ${det.detections.map(d => `
                        <div class="detection-item">
                            <div class="detection-color" style="background: ${d.color}"></div>
                            <div>
                                <div class="detection-name">${d.class_label}</div>
                                <div class="detection-conf">Confidence: ${(d.confidence * 100).toFixed(1)}%</div>
                            </div>
                        </div>`).join('')}
                </div>` : `<div style="text-align:center;padding:20px;color:var(--dark-muted);font-size:14px;">${t('result.no_detection')}</div>`}
        </div>`;
    }

    // Steps summary
    html += `
    <div class="result-card">
        <div class="detection-title" style="margin-bottom:12px;">📋 ${t('result.process_detail')}</div>
        <div class="steps-completed">
            ${result.steps.map(s => `
                <div class="step-completed">
                    <span class="step-completed-icon">${s.status === 'success' ? '✅' : '⚠️'}</span>
                    <span>${s.name}: ${s.detail}</span>
                    <span class="step-completed-time">${s.time_ms}ms</span>
                </div>`).join('')}
        </div>
    </div>
    <div style="text-align:center;">
        <button class="btn-new-analysis" onclick="resetState()">${t('result.new_analysis')}</button>
    </div>`;

    return html;
}

// ==================== ERROR ====================
function showError(msg) {
    processingSection.classList.remove('active');
    errorCard.classList.add('active');
    document.getElementById('error-message').textContent = msg;
}

// ==================== TOAST ====================
function showToast(msg, type = 'info') {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = msg;
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 300); }, 4000);
}

// ==================== UTILS ====================
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ==================== SCROLL NAV HIGHLIGHT ====================
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.navbar-nav a');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const top = section.offsetTop - 100;
        if (window.scrollY >= top) current = section.getAttribute('id');
    });
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) link.classList.add('active');
    });
});
