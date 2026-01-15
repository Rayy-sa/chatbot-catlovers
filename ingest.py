
import psycopg2
from psycopg2.extras import execute_values
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# 1. Konfigurasi
API_KEY = "AIzaSyBrYaHxfT0QOIgqVwUfeheOxgHE3xYyvZQ"
DB_PARAMS = "postgresql://array:123456@127.0.0.1:5435/catlovers_db"

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=API_KEY)

knowledge_data = [
    {"cat": "Nutrisi & Makanan","text": "Makanan basah memiliki kelebihan: kandungan air tinggi (75-80%) yang membantu hidrasi kucing, lebih mudah dicerna, aroma lebih menarik untuk kucing, dan cocok untuk kucing dengan masalah ginjal. Kekurangannya: lebih mahal, cepat basi jika tidak dihabiskan, harus disimpan di kulkas setelah dibuka, dan tidak membantu membersihkan gigi. Ideal dikombinasikan dengan makanan kering untuk nutrisi seimbang."},
    {"cat": "Nutrisi & Makanan","text": "Makanan kering untuk kucing memiliki beberapa kelebihan: lebih ekonomis dan tahan lama, membantu membersihkan gigi kucing, mudah disimpan tanpa pendingin, dan praktis untuk pemberian makan otomatis. Namun ada kekurangannya: kandungan air rendah (8-10%), dapat menyebabkan dehidrasi jika kucing kurang minum. Rekomendasi: berikan 2-3 kali sehari sesuai berat badan, pastikan air minum selalu tersedia."},
    {"cat": "Nutrisi & Makanan","text": "Makanan basah memiliki kelebihan: kandungan air tinggi (75-80%) yang membantu hidrasi kucing, lebih mudah dicerna, aroma lebih menarik untuk kucing, dan cocok untuk kucing dengan masalah ginjal. Kekurangannya: lebih mahal, cepat basi jika tidak dihabiskan, harus disimpan di kulkas setelah dibuka, dan tidak membantu membersihkan gigi. Ideal dikombinasikan dengan makanan kering untuk nutrisi seimbang."},
    {"cat": "Nutrisi & Makanan","text": "Nutrisi penting untuk kucing: Protein minimal (26%) untuk kucing dewasa dan (30%) untuk anak kucing. Taurin adalah asam amino esensial untuk kesehatan jantung dan mata. Lemak minimal (9%) untuk energi dan kesehatan bulu. Air: kucing perlu 60ml air per kg berat badan per hari. Vitamin dan mineral seperti Vitamin A, D, E, kalsium, dan fosfor penting untuk tulang dan sistem imun."},
    {"cat": "Nutrisi & Makanan","text": "Makanan berbahaya untuk kucing yang harus dihindari: Cokelat mengandung theobromine yang beracun. Bawang merah dan bawang putih merusak sel darah merah. Susu sapi karena banyak kucing dewasa lactose intolerant. Anggur dan kismis dapat menyebabkan gagal ginjal. Kafein beracun untuk kucing. Tulang ayam dapat menyebabkan tersedak atau luka dalam."},
    {"cat": "Kesehatan & Vaksinasi","text": "Vaksinasi Tricat/F3 melindungi dari Feline Panleukopenia, Calicivirus, dan Rhinotracheitis. Jadwal: usia 8-9 minggu (pertama), 12 minggu (kedua), kemudian booster tahunan. Vaksinasi ini melindungi dari virus mematikan yang menyerang sistem pencernaan dan pernapasan kucing."},
    {"cat": "Kesehatan & Vaksinasi","text": "Vaksinasi Rabies diberikan pada usia 16 minggu dengan booster tahunan. Vaksinasi ini melindungi dari virus rabies yang mematikan dan dapat menular ke manusia. Vaksinasi rabies sangat penting terutama jika kucing sering keluar rumah atau berinteraksi dengan hewan lain."},
    {"cat": "Kesehatan & Vaksinasi","text": "Vaksinasi opsional untuk kucing: Chlamydia untuk kucing yang sering berinteraksi dengan kucing lain. Feline Leukemia Virus (FeLV) untuk kucing yang keluar rumah atau tinggal di multi-cat household. Konsultasikan dengan dokter hewan untuk menentukan vaksinasi yang diperlukan."},
    {"cat": "Kesehatan & Vaksinasi","text": "Tanda-tanda kucing sehat: mata jernih dan cerah, hidung lembab dan bersih, bulu mengkilap dan tidak rontok berlebihan, nafsu makan baik, aktif dan responsif, berat badan stabil, dan buang air normal. Perhatikan perubahan pada tanda-tanda ini untuk deteksi dini masalah kesehatan."},
    {"cat": "Perilaku & Pelatihan", "text": "Perawatan litter box: Buang kotoran minimal 2x sehari. Ganti semua pasir dan cuci kotak setiap minggu. Kucing sangat bersih, jika kotak kotor mereka akan pipis sembarangan. Jangan letakkan dekat mesin cuci, area ramai, atau sudut sempit yang menakutkan."},
    {"cat": "Perilaku & Pelatihan", "text": "Mengatasi kucing pipis sembarangan: Periksa kebersihan litter box, cek apakah ada masalah kesehatan seperti ISK, evaluasi perubahan di rumah yang bisa menyebabkan stress, tambah jumlah litter box, dan bersihkan area yang dikotori dengan enzymatic cleaner. Jangan hukum kucing karena ini kontraproduktif."},
    {"cat": "Perilaku & Pelatihan","text": "Alasan kucing mencakar: mengasah dan merawat kuku, menandai teritorial karena ada kelenjar di telapak kaki, peregangan otot, dan melepas stress serta energi. Ini adalah perilaku alami yang tidak bisa dihilangkan, hanya dialihkan ke tempat yang tepat."},
    {"cat": "Perilaku & Pelatihan","text": "Solusi mencakar furnitur: Sediakan scratching post yang kokoh dan tinggi (minimal 75cm), letakkan di area favorit kucing, gunakan bahan sisal, kardus, atau karpet. Sediakan beberapa di lokasi berbeda. Latih dengan meletakkan catnip di scratching post, beri pujian dan reward saat menggunakannya. Potong kuku setiap 2-3 minggu. Jangan pernah declawing karena merupakan amputasi yang menyakitkan."},
    {"cat": "Perilaku & Pelatihan","text": "Bahasa tubuh kucing - Ekor: Ekor tegak berarti senang, ramah, siap berinteraksi. Ekor mengibas cepat berarti kesal, frustrasi, jangan ganggu. Ekor di antara kaki berarti takut atau cemas. Ekor membesar seperti sikat botol berarti sangat ketakutan atau agresif."},
    {"cat": "Perilaku & Pelatihan","text": "Bahasa tubuh kucing - Telinga dan mata: Telinga tegak maju berarti penasaran dan waspada. Telinga ke belakang berarti marah, defensif, siap menyerang. Pupil melebar bisa berarti takut, excited, atau mode berburu."},
    {"cat": "Perilaku & Pelatihan","text": "Sosialisasi anak kucing: Periode kritis adalah usia 2-7 minggu. Perkenalkan berbagai orang, suara, dan pengalaman positif. Lakukan handling lembut setiap hari. Bermain dengan mainan interaktif. Sosialisasi yang baik di periode ini akan menghasilkan kucing dewasa yang percaya diri dan ramah."},
    {"cat": "Panduan Perawatan","text": "Menyisir bulu kucing: Untuk bulu pendek 1-2x seminggu, bulu panjang setiap hari. Gunakan sisir gigi lebar, slicker brush, atau sisir kutu. Mulai dari kepala ke ekor, berhati-hati di area sensitif. Manfaatnya: mengurangi hairball, mencegah bulu kusut, deteksi dini masalah kulit, dan bonding time dengan kucing."},
    {"cat": "Panduan Perawatan","text": "Memandikan kucing: Frekuensi setiap 4-6 minggu atau saat sangat kotor. Kucing membersihkan diri sendiri sehingga tidak perlu terlalu sering. Gunakan air hangat dan shampo khusus kucing (pH balanced). Hindari area mata, telinga, dan hidung. Bilas hingga bersih dan keringkan dengan handuk atau hair dryer suhu rendah. Mulai saat masih kecil agar terbiasa."},
    {"cat": "Panduan Perawatan","text": "Memotong kuku kucing: Lakukan setiap 2-3 minggu menggunakan gunting kuku khusus kucing. Tekan telapak lembut agar kuku keluar, potong hanya bagian putih/transparan, hindari quick (bagian pink berisi pembuluh darah). Jika berdarah gunakan styptic powder. Lakukan saat kucing rileks atau mengantuk, beri reward setelahnya."},
    {"cat": "Panduan Perawatan","text": "Kebersihan telinga kucing: Periksa setiap minggu, bersihkan jika perlu (setiap 2-4 minggu). Gunakan ear cleaner khusus kucing atau NaCl 0.9%. Teteskan ke lubang telinga, pijat pangkal telinga, biarkan kucing menggelengkan kepala, lap bagian luar dengan kapas. JANGAN masukkan cotton bud ke dalam telinga. Ke dokter jika ada kotoran berlebihan, bau tidak sedap, atau kucing sering menggaruk telinga."},
    {"cat": "Panduan Perawatan","text": "Kebersihan gigi kucing: Penting untuk mencegah karang gigi, gingivitis, dan penyakit periodontal. Sikat gigi ideal 2-3x seminggu menggunakan sikat gigi jari atau sikat kecil dengan pasta gigi khusus kucing (jangan pasta gigi manusia). Alternatif: dental treats, mainan dental, makanan kering, atau air additive. Scaling di dokter hewan setiap 1-2 tahun jika diperlukan."},
    {"cat": "Panduan Perawatan","text": "Kebersihan mata kucing: Lap kotoran mata dengan kapas basah air hangat, bersihkan dari sudut dalam ke luar. Gunakan kapas berbeda untuk setiap mata. Sedikit kotoran di sudut mata saat bangun tidur adalah normal. Tidak normal jika ada kotoran berlebihan berwarna kuning/hijau, mata merah dan berair terus, mata tertutup atau bengkak, atau selaput putih menutup mata."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing selalu jatuh dengan empat kaki dan tidak pernah terluka. FAKTA: Kucing memiliki righting reflex, tapi tetap bisa terluka parah atau mati dari ketinggian. Jatuh dari lantai 2-7 paling berbahaya karena kucing tidak punya cukup waktu untuk posisi landing yang benar."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing tidak butuh perhatian dan mandiri total. FAKTA: Kucing butuh stimulasi mental, interaksi sosial, dan perhatian. Mereka bisa kesepian dan stress jika diabaikan. Kucing adalah hewan sosial yang membentuk ikatan dengan pemiliknya."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing yang dimandulkan akan jadi gemuk dan malas. FAKTA: Penambahan berat badan terjadi karena metabolisme berubah setelah sterilisasi, tapi bisa dikontrol dengan diet yang tepat dan olahraga. Manfaat sterilisasi jauh lebih besar daripada risiko obesitas yang bisa dicegah."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing hitam membawa sial. FAKTA: Takhayul tanpa dasar ilmiah. Di beberapa budaya seperti Jepang dan Inggris, kucing hitam justru dianggap pembawa keberuntungan. Warna bulu tidak mempengaruhi kepribadian atau membawa nasib."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing bisa melihat hantu atau makhluk gaib. FAKTA: Kucing memiliki pendengaran dan penglihatan superior yang mendeteksi gerakan kecil dan suara ultrasonic yang manusia tidak bisa dengar atau lihat. Mereka bisa mendengar frekuensi hingga 64 kHz (manusia hanya 20 kHz)."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing punya 9 nyawa. FAKTA: Hanya metafora untuk ketahanan dan kelincahan kucing. Mereka tetap makhluk hidup dengan satu nyawa. Ungkapan ini muncul karena kemampuan kucing bertahan dari situasi berbahaya dan refleks yang luar biasa."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Mendengkur selalu berarti kucing senang. FAKTA: Kucing juga mendengkur saat sakit, stress, atau kesakitan sebagai mekanisme self-soothing atau self-healing. Perhatikan konteks dan tanda-tanda lain untuk memahami kondisi kucing."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Kucing dan anjing selalu musuhan. FAKTA: Dengan sosialisasi yang tepat sejak kecil, kucing dan anjing bisa hidup harmonis bahkan berteman baik. Banyak rumah tangga sukses memelihara kedua hewan ini bersama-sama."},
    {"cat": "Mitos vs Fakta","text": "MITOS: Whisker (kumis) kucing boleh dipotong. FAKTA: JANGAN PERNAH memotong whisker! Whisker adalah sensor penting untuk navigasi, keseimbangan, dan orientasi ruang. Memotongnya membuat kucing disorientasi dan kesulitan bergerak di ruang gelap."},
    {"cat": "Perilaku & Pelatihan","text": "Mendengkur pada kucing bisa memiliki arti berbeda tergantung konteks. Kucing mendengkur saat merasa senang dan nyaman, tetapi juga bisa mendengkur saat sakit atau stress sebagai mekanisme self-soothing. Beberapa penelitian menunjukkan frekuensi dengkuran (25-150 Hz) dapat membantu penyembuhan tulang dan mengurangi rasa sakit."},
    {"cat": "Perilaku & Pelatihan","text": "Menggigit pada kucing memiliki arti berbeda. Gigitan halus biasanya adalah bentuk main-main atau kasih sayang (love bite). Gigitan keras berarti kucing sudah mencapai batas kesabaran dan meminta untuk berhenti diganggu. Jika kucing menggigit saat dibelai, mungkin terjadi overstimulation - berhenti membelai dan beri ruang."}
]

# Data terstruktur untuk Jenis Kucing (cat_breeds)
breeds_data = [
    (
      "Aegean",
      "Bulu pendek hingga semi panjang, pola bicolor dan tricolor",
      "Yunani",
      "Ramah, sosial, dan suka air"
    ),
    (
      "American Bobtail",
      "Ekor pendek alami, bulu pendek/semi panjang, tubuh semi cobby",
      "Amerika Serikat",
      "Penyayang, mudah beradaptasi, dan playful"
    ),
    (
      "American Curl",
      "Telinga melengkung ke belakang, bulu pendek/panjang",
      "Amerika Serikat",
      "Ramah, penasaran, dan penyayang"
    ),
    (
      "American Wirehair",
      "Bulu bertekstur kasar seperti kawat (rex)",
      "Amerika Serikat",
      "Santai, ramah, dan mudah beradaptasi"
    ),
    (
      "Arabian Mau",
      "Bulu pendek, tubuh medium hingga besar, warna putih, hitam, atau tabby coklat",
      "Mesir",
      "Setia, aktif, dan ramah dengan keluarga"
    ),
    (
      "Ashera",
      "Tubuh besar, bulu pendek dengan pola spotted, hybrid serval",
      "Amerika Serikat",
      "Eksotis, aktif, dan memerlukan perhatian khusus"
    ),
    (
      "Balinese",
      "Bulu semi panjang, tubuh oriental, pola colorpoint",
      "Amerika Serikat",
      "Vokal, sosial, dan penyayang"
    ),
    (
      "Bombay",
      "Bulu pendek hitam solid mengkilap, mata emas, menyerupai panther mini",
      "Amerika Serikat",
      "Ramah, sosial, dan suka perhatian"
    ),
    (
      "British Longhair",
      "Bulu semi panjang, tubuh medium hingga besar, wajah bulat",
      "Inggris",
      "Tenang, penyayang, dan mudah bergaul"
    ),
    (
      "Burmese",
      "Bulu pendek mengkilap, tubuh medium, mata emas",
      "Myanmar (Burma)",
      "Ramah, suka bermain, dan sangat penyayang"
    ),
    (
      "Burmilla",
      "Bulu pendek dengan shaded silver, mata hijau ekspresif",
      "Inggris",
      "Lembut, playful, dan sosial"
    ),
    (
      "Chartreux",
      "Bulu pendek biru solid tebal seperti wol, tubuh kokoh",
      "Perancis",
      "Tenang, pendiam, dan setia"
    ),
    (
      "Chausie",
      "Tubuh besar dan atletis, bulu pendek, pola ticked, hybrid kucing hutan",
      "Perancis",
      "Aktif, atletis, dan suka bermain"
    ),
    (
      "Cornish Rex",
      "Bulu keriting pendek (rex), tubuh ramping, telinga besar",
      "Inggris",
      "Energik, playful, dan suka berinteraksi"
    ),
    (
      "Devon Rex",
      "Bulu keriting rex, tubuh ramping, telinga sangat besar, wajah pixie-like",
      "Inggris",
      "Sangat sosial, playful, dan suka dipangku"
    ),
    (
      "Egyptian Mau",
      "Bulu pendek dengan pola spotted alami, tubuh medium hingga besar",
      "Mesir",
      "Aktif, setia, dan cepat berlari"
    ),
    (
      "Exotic Shorthair",
      "Bulu pendek tebal, wajah flat seperti Persia",
      "Amerika Serikat",
      "Tenang, penyayang, dan mudah dirawat"
    ),
    (
      "Havana Brown",
      "Bulu pendek coklat solid, tubuh medium, mata hijau",
      "Inggris",
      "Ramah, cerdas, dan suka interaksi"
    ),
    (
      "Himalayan",
      "Bulu panjang, wajah flat, pola colorpoint seperti Siamese",
      "Inggris",
      "Tenang, manis, dan butuh perawatan grooming rutin"
    ),
    (
      "Japanese Bobtail",
      "Ekor pendek seperti pompon, bulu pendek/panjang",
      "Jepang",
      "Aktif, vokal, dan ramah"
    ),
    (
      "Korat",
      "Bulu pendek biru-abu solid, tubuh semi cobby, mata hijau",
      "Thailand",
      "Tenang, setia, dan sensitif"
    ),
    (
      "Manx",
      "Tidak memiliki ekor atau ekor sangat pendek, bulu pendek",
      "Inggris",
      "Playful, cerdas, dan setia"
    ),
    (
      "Nebelung",
      "Bulu semi panjang biru solid, tubuh ramping",
      "Amerika Serikat",
      "Lembut, pemalu dengan orang asing, setia pada keluarga"
    ),
    (
      "Ocicat",
      "Bulu pendek dengan pola spotted seperti ocelot, tubuh besar",
      "Amerika Serikat",
      "Aktif, sosial, dan mudah dilatih"
    ),
    (
      "Oriental Shorthair",
      "Tubuh ramping oriental, bulu pendek, telinga besar, berbagai warna",
      "Amerika Serikat",
      "Vokal, energik, dan butuh perhatian"
    ),
    (
      "Peterbald",
      "Tubuh oriental, tidak berbulu (hairless) atau bulu tipis",
      "Rusia",
      "Ramah, energik, dan suka kehangatan"
    ),
    (
      "Savannah",
      "Tubuh sangat besar, bulu pendek spotted, hybrid serval, kaki panjang",
      "Amerika Serikat",
      "Sangat aktif, atletis, cerdas, dan suka bermain air"
    ),
    (
      "Selkirk Rex",
      "Bulu keriting tebal, tubuh medium hingga besar",
      "Amerika Serikat",
      "Penyayang, santai, dan playful"
    ),
    (
      "Siberian",
      "Bulu semi panjang tebal, tubuh besar dan kuat, tahan dingin",
      "Rusia",
      "Ramah, playful, dan hipoalergenik (rendah alergen)"
    ),
    (
      "Singapura",
      "Ukuran sangat kecil, bulu pendek ticked, mata besar",
      "Singapura",
      "Energik, penasaran, dan penyayang"
    ),
    (
      "Snowshoe",
      "Bulu pendek dengan pola colorpoint dan 'sepatu salju' putih di kaki",
      "Amerika Serikat",
      "Ramah, sosial, dan suka bermain"
    ),
    (
      "Somali",
      "Tubuh medium hingga besar, bulu panjang dengan pola ticked, mirip Abyssinian berbulu panjang",
      "Amerika Serikat",
      "Aktif, playful, dan cerdas"
    ),
    (
      "Sokoke",
      "Bulu pendek dengan pola marbled/spotted, tubuh ramping",
      "Kenya",
      "Aktif, cerdas, dan sosial"
    ),
    (
      "Tonkinese",
      "Perpaduan Siamese dan Burmese, tubuh medium, pola mink",
      "Kanada",
      "Sosial, playful, dan penyayang"
    ),
    (
      "Toyger",
      "Pola seperti harimau (striped), bulu pendek, tubuh medium",
      "Amerika Serikat",
      "Ramah, easy-going, dan suka bermain"
    ),
    (
      "Turkish Van",
      "Bulu semi panjang, pola van (putih dengan warna di kepala dan ekor)",
      "Turki",
      "Energik, suka air dan berenang, dan mandiri"
    ),
    (
      "Alpine Lynx",
      "Bulu pendek/semi panjang, tubuh medium, warna putih",
      "Amerika Serikat",
      "Ramah, tenang, dan adaptif"
    ),
    (
      "American Keuda",
      "Bulu pendek, tubuh medium, berbagai warna",
      "Amerika Serikat",
      "Mandiri, cerdas, dan tangguh"
    ),
    (
      "American Longhair",
      "Bulu panjang, tubuh standard, berbagai warna",
      "Amerika Serikat",
      "Ramah, santai, dan mudah bergaul"
    ),
    (
      "American Polydactyl",
      "Memiliki enam jari (polydactyl), bulu pendek/panjang, tubuh medium hingga besar",
      "Amerika Serikat",
      "Ramah, unik, dan mudah beradaptasi"
    ),
    (
      "American Ringtail",
      "Ekor melengkung seperti cincin, bulu semi panjang, tubuh medium hingga besar",
      "Amerika Serikat",
      "Penyayang, playful, dan sosial"
    ),
    (
      "Anatolian",
      "Bulu pendek, tubuh medium, warna alami",
      "Turki",
      "Energik, cerdas, dan suka berburu"
    ),
    (
      "Aphrodite",
      "Tubuh besar, bulu pendek/semi panjang, berbagai warna",
      "Cyprus",
      "Ramah, atletis, dan setia"
    ),
    (
      "Asian",
      "Bulu semi panjang, tubuh medium, pola self, smoke, tabby",
      "Inggris & Amerika Serikat",
      "Lembut, sosial, dan penyayang"
    ),
    (
      "Australian Mist",
      "Bulu pendek, pola spotted/classic tabby/ticked",
      "Australia",
      "Ramah, toleran, dan cocok untuk dalam rumah"
    ),
    (
      "Australian Tiffanie",
      "Bulu semi panjang, mayoritas putih",
      "Australia",
      "Penyayang, tenang, dan mudah bergaul"
    ),
    (
      "Bahraini Dilmun",
      "Bulu pendek, tubuh medium hingga besar, pola spotted/ticked",
      "Saudi Arabia",
      "Ramah, adaptif, dan sosial"
    ),
    (
      "Bambino",
      "Tubuh medium, tidak berbulu (hairless), kaki pendek",
      "Italia",
      "Energik, ramah, dan suka perhatian"
    ),
    (
      "Bramble",
      "Tubuh besar, bulu pendek, pola spotted/ticked/solid/colorpoint",
      "Amerika Serikat",
      "Aktif, cerdas, dan sosial"
    ),
    (
      "Brazilian Shorthair",
      "Bulu pendek, tubuh medium, berbagai warna",
      "Brasil",
      "Ramah, adaptif, dan mandiri"
    ),
    (
      "California Spangled",
      "Bulu pendek dengan pola spotted, berbagai warna",
      "Amerika Serikat",
      "Aktif, cerdas, dan sosial"
    ),
    (
      "Cashmere",
      "Bulu semi panjang, pola tabby/spotted/marbled",
      "Eropa & USA",
      "Aktif, playful, dan ramah"
    ),
    (
      "Ceylon",
      "Bulu pendek dengan pola ticked, mata kuning-hijau",
      "Sri Lanka",
      "Energik, cerdas, dan vokal"
    ),
    (
      "Chantilly",
      "Bulu semi panjang, warna hitam/biru/coklat/lilac",
      "Amerika Serikat & Kanada",
      "Lembut, loyal, dan suka perhatian"
    ),
    (
      "Cheetoh",
      "Tubuh besar, bulu pendek spotted, hybrid",
      "Amerika Serikat",
      "Ramah, energik, dan sosial"
    ),
    (
      "Chinchilla Longhair",
      "Bulu sangat panjang, warna chinchilla/perak",
      "Inggris",
      "Tenang, manis, dan elegan"
    ),
    (
      "Chinese White",
      "Bulu pendek/panjang, warna putih solid",
      "RRC",
      "Ramah, tenang, dan mudah bergaul"
    ),
    (
      "Clippercat",
      "Polydactyl (enam jari), bulu pendek/panjang, berbagai warna",
      "New Zealand",
      "Ramah, unik, dan adaptif"
    ),
    (
      "Colourpoint Shorthair",
      "Tubuh medium, bulu pendek, pola colorpoint",
      "Amerika Serikat",
      "Vokal, sosial, dan penyayang"
    ),
    (
      "Curly Tail",
      "Ekor melengkung, bulu pendek/medium/panjang",
      "Tidak diketahui",
      "Ramah, playful, dan unik"
    ),
    (
      "Cymric",
      "Tidak berekor atau ekor pendek, bulu panjang",
      "Inggris",
      "Playful, cerdas, dan setia"
    ),
    (
      "Desert Lynx",
      "Tubuh medium hingga besar, bulu pendek/semi panjang, pola spotted",
      "Amerika Serikat",
      "Ramah, aktif, dan cerdas"
    ),
    (
      "Domestic Longhair",
      "Bulu medium hingga panjang, tubuh standard, berbagai warna",
      "Tidak diketahui",
      "Bervariasi, umumnya ramah dan adaptif"
    ),
    (
      "Domestic Shorthair",
      "Bulu pendek, tubuh standard, berbagai warna",
      "Tidak diketahui",
      "Bervariasi, umumnya ramah dan mandiri"
    ),
    (
      "Don Sphynx",
      "Tubuh medium, tidak berbulu (hairless)",
      "Rusia",
      "Ramah, sosial, dan hangat"
    ),
    (
      "Dragon Li",
      "Bulu pendek golden brown, pola striped tabby",
      "RRC (Cina)",
      "Ramah, cerdas, dan loyal"
    ),
    (
      "Dwelf",
      "Tubuh kerdil (dwarf), tidak berbulu (hairless)",
      "Amerika Serikat",
      "Energik, playful, dan penyayang"
    ),
    (
      "Elf",
      "Tubuh medium hingga besar, tidak berbulu, telinga melengkung",
      "Amerika Serikat",
      "Ramah, sosial, dan energik"
    ),
    (
      "European Shorthair",
      "Bulu pendek, tubuh medium hingga besar",
      "Swedia & Italia",
      "Mandiri, ramah, dan adaptif"
    ),
    (
      "Exotic Fold",
      "Tubuh cobby, bulu pendek/panjang, telinga melipat",
      "Kanada",
      "Tenang, penyayang, dan manis"
    ),
    (
      "Exotic Longhair",
      "Tubuh cobby, bulu panjang, wajah flat",
      "Amerika Serikat",
      "Tenang, manis, dan penyayang"
    ),
    (
      "Foreign White",
      "Tubuh oriental, bulu pendek, warna putih solid",
      "Inggris",
      "Vokal, energik, dan sosial"
    ),
    (
      "Genetta",
      "Tubuh standard, bulu pendek, pola brown spotted tabby",
      "Amerika Serikat",
      "Playful, energik, dan ramah"
    ),
    (
      "German Rex",
      "Bulu keriting (rex), tubuh medium",
      "Jerman",
      "Ramah, playful, dan penyayang"
    ),
    (
      "Habari",
      "Tubuh besar, bulu pendek spotted, hybrid",
      "Asia",
      "Aktif, cerdas, dan eksotis"
    ),
    (
      "Highland Fold",
      'Tubuh cobby, bulu medium/panjang, telinga melipat',
      'Skotlandia',
      'Tenang, manis, dan penyayang'
    ),
    (
      "Highlander Shorthair",
      'Tubuh medium hingga besar, bulu pendek, pola spotted/solid',
      'Amerika Serikat',
      'Aktif, ramah, dan playful'
    ),
    (
      "Highlander Longhair",
      'Tubuh medium hingga besar, bulu panjang, pola spotted/solid',
      'Amerika Serikat',
      'Ramah, energik, dan sosial'
    ),
    (
      "Jaguarundi Curl",
      'Tubuh medium hingga besar, bulu pendek, pola solid/ticked/spotted',
      'Amerika Utara',
      'Aktif, cerdas, dan unik'
    ),
    (
      "Jambi",
      'Tubuh cobby dan stocky, bulu pendek, warna golden dengan spot gelap',
      'Asia',
      'Ramah, tenang, dan eksotis'
    ),
    (
      "Javanese",
      'Tubuh oriental medium, bulu pendek/semi panjang',
      'Amerika Serikat',
      'Vokal, sosial, dan energik'
    ),
    (
      "Jungala",
      'Tubuh besar, bulu pendek, pola classic tabby',
      'Amerika Serikat',
      'Aktif, cerdas, dan playful'
    ),
    (
      "Jungle",
      'Tubuh besar, bulu pendek, warna sandy brown/reddish/gray, hybrid',
      'Asia Selatan dan Tengah',
      'Wild, energik, dan butuh perhatian khusus'
    ),
    (
      "Junglebob",
      'Tubuh medium hingga besar, bulu pendek/medium/panjang, pola spotted',
      'Amerika Serikat',
      'Aktif, ramah, dan unik'
    ),
    (
      "Kanaani",
      'Tubuh medium hingga besar, bulu pendek, pola spotted',
      'Jerman & Jerusalem',
      'Energik, cerdas, dan mandiri'
    ),
    (
      "Karel Bobtail",
      'Tubuh medium, ekor pendek, bulu pendek/semi panjang, pola spotted tabby',
      'Republik Karelia, Rusia',
      'Ramah, playful, dan adaptif'
    ),
    (
      "Kashmir",
      'Tubuh medium, bulu panjang, warna lilac/coklat',
      'Kanada & Amerika Serikat',
      'Tenang, penyayang, dan manis'
    ),
    (
      "Khao Manee",
      'Bulu pendek, warna putih, mata berlian (heterochromia)',
      'Thailand',
      'Sosial, vokal, dan penyayang'
    ),
    (
      "Kinkalow",
      'Tubuh kerdil (dwarf), bulu pendek/semi panjang, telinga melengkung',
      'Amerika Serikat',
      'Playful, energik, dan ramah'
    ),
    (
      "Kohana",
      'Tubuh oriental, tidak berbulu (hairless)',
      'Hawaii (USA)',
      'Energik, sosial, dan hangat'
    ),
    (
      "Kurilian Bobtail",
      'Tubuh semi cobby, ekor pendek, bulu pendek/panjang',
      'Pulau Kuril, Rusia',
      'Ramah, cerdas, dan suka air'
    ),
    (
      "Lambkin",
      'Tubuh kerdil (dwarf), bulu keriting pendek/panjang',
      'Amerika Serikat',
      'Penyayang, playful, dan manis'
    ),
    (
      "LaPerm",
      'Bulu keriting (rex) pendek/panjang, tubuh kecil hingga moderate',
      'Amerika Serikat',
      'Ramah, penyayang, dan sosial'
    ),
    (
      "Mandalay",
      'Tubuh medium, bulu pendek, warna ebony/chocolate/lavender/blue',
      'Selandia Baru',
      'Ramah, sosial, dan penyayang'
    ),
    (
      "Meerkat",
      'Tubuh medium, bulu pendek',
      'Amerika Utara',
      'Ramah, playful, dan unik'
    ),
    (
      "Mekong Bobtail",
      'Tubuh medium, ekor pendek, bulu pendek, pola colorpoint',
      'Iran, Irak, RRC, Mongolia, Laos, Myanmar, Vietnam',
      'Ramah, loyal, dan vokal'
    ),
    (
      "Minskin",
      'Tubuh semi cobby, bulu pendek/hairless, kaki pendek',
      'Amerika Serikat',
      'Energik, ramah, dan sosial'
    ),
    (
      "Mohave Bobs",
      'Tubuh medium, bulu pendek/semi panjang',
      'Amerika Serikat',
      'Ramah, playful, dan adaptif'
    ),
    (
      "Mojave Spotted",
      'Tubuh medium hingga besar, bulu pendek, pola spotted tabby',
      'Mojave',
      'Aktif, cerdas, dan eksotis'
    ),
    (
      "Mokave",
      'Tubuh besar, bulu pendek, pola spotted',
      'Amerika Serikat',
      'Energik, playful, dan ramah'
    ),
    (
      "Napoleon",
      'Tubuh cobby, bulu pendek/panjang, kaki pendek',
      'Amerika Serikat',
      'Manis, penyayang, dan playful'
    ),
    (
      "Nepalayan",
      'Tubuh medium, bulu pendek/panjang, polydactyl',
      'New Zealand',
      'Ramah, unik, dan adaptif'
    ),
    (
      "Neva Masquerade",
      'Tubuh medium, bulu panjang, pola colorpoint',
      'Rusia',
      'Ramah, playful, dan tahan dingin'
    ),
    (
      "New Zealand",
      'Tubuh medium, bulu pendek/panjang, berbagai warna',
      'New Zealand',
      'Ramah, mandiri, dan adaptif'
    ),
    (
      "Ojos Azules",
      'Tubuh medium, bulu pendek, mata biru',
      'Amerika Serikat',
      'Ramah, lembut, dan unik'
    ),
    (
      "Oriental Bicolour",
      'Tubuh oriental, bulu pendek/panjang, pola bicolour',
      'Amerika Serikat',
      'Vokal, energik, dan sosial'
    ),
    (
      "Oriental Longhair",
      'Tubuh oriental, bulu panjang/semi panjang, berbagai warna',
      'Amerika Serikat',
      'Vokal, sosial, dan energik'
    ),
    (
      "Owyhee Bobs",
      'Tubuh medium hingga besar, bulu pendek/panjang, ekor pendek',
      'Amerika Serikat',
      'Ramah, playful, dan adaptif'
    ),
    (
      "Pantherette",
      'Tubuh besar, bulu pendek, pola black tabby, hybrid',
      'Amerika Serikat',
      'Aktif, eksotis, dan cerdas'
    ),
    (
      "Pixiebob Longhair",
      'Tubuh medium hingga besar, bulu panjang, pola brown spotted tabby',
      'Amerika Serikat',
      'Ramah, loyal, dan dog-like'
    ),
    (
      "Pixiebob Shorthair",
      'Tubuh medium hingga besar, bulu pendek, pola brown spotted tabby',
      'Amerika Serikat',
      'Ramah, cerdas, dan loyal'
    ),
    (
      "Puppykat",
      'Tubuh medium hingga besar, bulu pendek',
      'Amerika Serikat',
      'Ramah, playful, dan seperti anjing'
    ),
    (
      "Ragamuffin",
      'Tubuh cobby, bulu panjang, berbagai warna',
      'Amerika Serikat',
      'Sangat penyayang, tenang, dan docile'
    ),
    (
      "Russian Shorthair",
      'Tubuh medium, bulu pendek, berbagai warna',
      'Rusia',
      'Tenang, cerdas, dan mandiri'
    ),
    (
      "Russian White, Black, Tabby",
      'Tubuh medium, bulu pendek, warna putih/hitam/tabby',
      'Australia',
      'Ramah, cerdas, dan penyayang'
    ),
    (
      "Safari",
      'Tubuh besar, bulu pendek, pola spotted, hybrid',
      'Amerika Serikat',
      'Aktif, eksotis, dan energik'
    ),
    (
      "Scottish Straight Longhair",
      'Tubuh medium, bulu panjang, telinga tegak',
      'Skotlandia',
      'Ramah, tenang, dan penyayang'
    ),
    (
      "Scottish Straight Shorthair",
      'Tubuh medium, bulu pendek, telinga tegak',
      'Skotlandia',
      'Ramah, mudah bergaul, dan playful'
    ),
    (
      "Serengeti",
      'Tubuh besar, bulu pendek, pola spotted',
      'Amerika Serikat',
      'Aktif, vokal, dan energik'
    ),
    (
      "Seychellois",
      'Tubuh oriental, bulu pendek/panjang, warna putih dengan tail hitam',
      'Inggris',
      'Vokal, sosial, dan energik'
    ),
    (
      "Sibella",
      'Tubuh medium hingga besar, bulu semi panjang, berbagai warna plus putih',
      'Amerika Serikat',
      'Tenang, penyayang, dan docile'
    ),
    (
      "Skookum",
      'Tubuh moderate, bulu pendek/keriting, kaki pendek',
      'USA, Europe, New Zealand, Australia',
      'Playful, ramah, dan energik'
    ),
    (
      "Snow-Bobs",
      'Tubuh medium hingga besar, bulu pendek, pola colorpoint snow',
      'Amerika Serikat',
      'Ramah, tenang, dan penyayang'
    ),
    (
      "Snowshoe",
      'Tubuh medium hingga besar, bulu pendek, pola colorpoint dengan kaki putih',
      'Amerika Serikat',
      'Vokal, sosial, dan ramah'
    ),
    (
      "Sokoke",
      'Tubuh medium, bulu pendek, pola classic tabby dengan ticking',
      'Kenya',
      'Aktif, sosial, dan cerdas'
    ),
    (
      "Tasman Manx",
      'Tubuh medium, bulu pendek/panjang, tidak berekor',
      'Australia & New Zealand',
      'Playful, ramah, dan adaptif'
    ),
    (
      "Teacup",
      'Tubuh sangat kecil (dwarf), bulu pendek/panjang',
      'Eropa & USA',
      'Manis, kecil, dan butuh perawatan khusus'
    ),
    (
      "Templecat",
      'Tubuh medium, bulu pendek, pola colorpoint',
      'Birma',
      'Ramah, tenang, dan penyayang'
    ),
    (
      "Tennessee Rex",
      'Tubuh medium hingga besar, bulu keriting (rex)',
      'Amerika Serikat',
      'Ramah, playful, dan energik'
    ),
    (
      "Thai",
      "Tubuh medium, bulu pendek, pola colorpoint",
      'Thailand',
      'Vokal, sosial, dan penyayang'
    ),
    (
      "Thai Lilac",
      'Tubuh medium, bulu pendek, warna lilac',
      'Eropa',
      'Ramah, lembut, dan tenang'
    ),
    (
      "Thai Point",
      'Tubuh medium, bulu pendek, pola blue/lilac point',
      'Thailand',
      'Vokal, sosial, dan ramah'
    ),
    (
      "Tibetan",
      'Tubuh medium, bulu semi panjang, pola colourpoint/mink/white/solid',
      'Belanda',
      'Tenang, penyayang, dan lembut'
    ),
    (
      "ToyBob",
      'Tubuh mini, bulu pendek, pola colorpoint',
      'Rusia',
      'Manis, kecil, dan penyayang'
    ),
    (
      "Turkish Vankedisi",
      'Tubuh medium, bulu semi panjang, warna putih',
      'Turki',
      'Energik, suka air, dan mandiri'
    ),
    (
      "Twisty",
      'Tubuh standard, bulu pendek/semi panjang, kaki pendek',
      'Amerika Serikat, Australia, Eropa',
      'Ramah, unik, dan adaptif'
    ),
    (
      "Ukrainian Levkoy",
      'Tubuh medium, tidak berbulu (hairless), telinga melipat',
      'Ukraina',
      'Ramah, sosial, dan unik'
    ),
    (
      "Ural Rex",
      'Tubuh medium, bulu keriting pendek/medium, warna chocolate/black & white tabby/brown',
      'Rusia',
      'Ramah, playful, dan adaptif'
    ),
    (
      "York Chocolate",
      'Tubuh medium hingga besar, bulu semi panjang, warna chocolate/lavender/white/bicolour',
      'Amerika Serikat',
      'Ramah, tenang, dan penyayang'
    )
]

# Data terstruktur untuk Penyakit (cat_diseases)
diseases_data = [
    (
      "Diare",
      "Feses cair atau lembek, buang air besar lebih sering dari biasanya, kadang disertai muntah, dehidrasi, lemas, kehilangan nafsu makan",
      "Puasa 12-24 jam (tetap berikan air), berikan makanan bland seperti ayam rebus dan nasi, pastikan hidrasi cukup. Konsultasi dokter jika berlanjut lebih dari 24 jam, ada darah dalam feses, atau kucing sangat lemas.",
      "Sedang-Tinggi"
    ),
    (
      "Muntah",
      "Mengeluarkan makanan atau cairan dari mulut, lemas, tidak mau makan, kadang disertai diare, air liur berlebihan",
      "Perhatikan frekuensi dan isi muntahan. Jika muntah hairball sesekali itu normal, berikan hairball paste. Puasa 4-6 jam lalu berikan makanan sedikit-sedikit. Konsultasi dokter jika muntah berulang, ada darah, atau kucing dehidrasi.",
      "Rendah-Tinggi"
    ),
    (
      "Infeksi Saluran Kemih (Feline Lower Urinary Tract Disease/FLUTD)",
      "Sering ke litter box tapi hanya pipis sedikit atau tidak keluar sama sekali, pipis berdarah, mengeong kesakitan saat pipis, menjilati area genital berlebihan, pipis di luar litter box",
      "SEGERA KE DOKTER HEWAN! Ini adalah kondisi darurat terutama pada kucing jantan. Dokter akan memberikan antibiotik, pain relief, dan mungkin memasang kateter. Tingkatkan asupan air, berikan makanan basah, hindari stress.",
      "Tinggi"
    ),
    (
      "Infeksi Telinga (Otitis)",
      "Menggaruk telinga terus-menerus, menggelengkan kepala, kotoran telinga berlebihan berwarna hitam/coklat, bau tidak sedap dari telinga, telinga kemerahan atau bengkak, kepala miring ke satu sisi",
      "Bawa ke dokter untuk pemeriksaan. Jangan bersihkan telinga sendiri jika sudah infeksi. Dokter akan memberikan obat tetes telinga antibiotik atau antijamur. Bersihkan telinga rutin setelah sembuh untuk pencegahan.",
      "Sedang"
    )
]

def insert_all_data():
    try:
        conn = psycopg2.connect(DB_PARAMS)
        cur = conn.cursor()
        print("🚀 Menghubungkan ke database...")

        # Ingest ke cat_knowledge (RAG)
        print("Memasukkan data pengetahuan (vektor)...")
        for item in knowledge_data:
            vector = embeddings_model.embed_query(item['text'])
            cur.execute(
                "INSERT INTO cat_knowledge (content, category, embedding) VALUES (%s, %s, %s)",
                (item['text'], item['cat'], vector)
            )

        # Ingest ke cat_breeds (Data Master)
        print("Memasukkan data jenis kucing...")
        execute_values(cur, 
            "INSERT INTO cat_breeds (name, description, origin, temperament) VALUES %s", 
            breeds_data
        )

        # Ingest ke cat_diseases (Data Master)
        print("Memasukkan data penyakit...")
        execute_values(cur, 
            "INSERT INTO cat_diseases (name, symptoms, treatment_suggestion, danger_level) VALUES %s", 
            diseases_data
        )

        conn.commit()
        print("✅ Semua data berhasil dimasukkan!")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    insert_all_data()
