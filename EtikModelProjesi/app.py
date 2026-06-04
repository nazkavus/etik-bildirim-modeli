import streamlit as st
import time
import google.generativeai as genai

# Streamlit Secrets'tan anahtarı güvenli bir şekilde okuyoruz
API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else None

def yz_gerekce_uret(skor, sure, hatalar_listesi):
    if not API_KEY:
        return "Yapay zeka anahtarı sisteme tanımlanmamış. Lütfen kural tabanlı öneriyi dikkate alın."
    try:
        # Eski ve kararlı kütüphane ile yapılandırma
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Sen 'Açıklanabilir Yapay Zeka (XAI)' prensipleriyle çalışan şeffaf bir eğitsel bilişim etiği asistanısın.
        Öğrenci bir mini durum testini tamamladı. Analiz verileri:
        - Başarı Yüzdesi: %{skor}
        - Testi Bitirme Süresi: {sure} saniye
        - Yanlış Yapılan Konular: {hatalar_listesi if hatalar_listesi else 'Yok, hepsi doğru.'}
        
        Görevin:
        Öğrenciye %80 başarı eşiğine göre modül önerisinde bulun (Skor düşükse Temel Modül, yüksekse İleri Düzey Modül).
        Bu kararın arkasındaki gerekçeyi öğrenciye açıklarken 'paternalist' (baskıcı) bir dil kullanma. 
        Öğrencinin kararı ezen aktif bir özne olduğunu hissettiren, şeffaf ve samimi en fazla 3 cümlelik bir metny üret.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Yapay zeka sunucusu şu an yoğun. Kural tabanlı sistem önerisi geçerlidir. (Hata: {e})"

# Sayfa ayarları
st.set_page_config(page_title="Bilişim Etiği - Etik Bildirim Prototipi", page_icon="🤖")
st.title("🤖 Gerçek YZ Destekli Etik Bildirim ve Onay Modeli")
st.write("Bu simülasyon, arka planda canlı Gemini API kullanarak gerekçelerini 'Açıklanabilir YZ (XAI)' ile üretir.")

if "test_bitti" not in st.session_state:
    st.session_state.test_bitti = False
    st.session_state.baslama_zamani = time.time()

# 10.1: KULLANICI ETKİLEŞİMİ
if not st.session_state.test_bitti:
    st.subheader("📝 Bilişim Etiği Mini Tanılama Testi")
    
    soru_1 = st.radio(
        "1. Bir yazılımcının, açık kaynak kodlu bir projeyi kaynak göstermeden ticari bir üründe doğrudan kullanması hangi etik ihlale girer?",
        ["Veri Mahremiyeti İhlali", "Fikri Mülkiyet ve İntihal", "Siber Zorbalık", "Erişilebilirlik Engeli"], index=None
    )
    soru_2 = st.radio(
        "2. Eğitsel bir yapay zeka sisteminin, öğrenci verilerini rızası olmadan reklam şirketlerine satması hangi etik ilkeyi doğrudan çiğner?",
        ["Şeffaflık", "Hesap Verilebilirlik", "Gizlilik ve Veri Mahremiyeti", "Eşitlik/Adalet"], index=None
    )
    soru_3 = st.radio(
        "3. Yapay zeka algoritmalarının aldığı kararların gerekçelerini son kullanıcıya açıklayamaması durumuna ne ad verilir?",
        ["Kara Kutu (Black Box) Problemi", "Veri Önyargısı", "Algoritmik Paternalizm", "Dijital Bölünme"], index=None
    )

    if st.button("Testi Tamamla"):
        if soru_1 and soru_2 and soru_3:
            st.session_state.bitis_zamani = time.time()
            st.session_state.toplam_sure = round(st.session_state.bitis_zamani - st.session_state.baslama_zamani, 1)
            
            hatalar = []
            skor = 0
            
            if "Fikri Mülkiyet" in soru_1: skor += 33.3
            else: hatalar.append("Fikri Mülkiyet (Eksik)")
                
            if "Gizlilik" in soru_2: skor += 33.3
            else: hatalar.append("Veri Mahremiyeti (Eksik)")
                
            if "Kara Kutu" in soru_3: skor += 33.4
            else: hatalar.append("Kara Kutu Problemi (Eksik)")
            
            st.session_state.skor = round(skor, 1)
            st.session_state.hatalar_metni = ", ".join(hatalar)
            
            with st.spinner("Yapay Zeka verilerinizi analiz ediyor..."):
                st.session_state.yz_gerekcesi = yz_gerekce_uret(st.session_state.skor, st.session_state.toplam_sure, st.session_state.hatalar_metni)
            
            st.session_state.test_bitti = True
            st.rerun()
        else:
            st.warning("Lütfen sınıfta hata oluşmaması için tüm soruları cevaplayın!")

# SONUÇ EKRANI
if st.session_state.test_bitti:
    st.success("🎉 Değerlendirme tamamlandı!")
    
    st.subheader("📊 Toplanan Öğrenme Metaverileriniz")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Başarı Skorunuz", value=f"%{st.session_state.skor}")
    with col2:
        st.metric(label="Karar Süreniz", value=f"{st.session_state.toplam_sure} saniye")

    st.markdown("---")
    st.subheader("🤖 Gerçek Zamanlı Üretilen YZ Etik Bildirim Paneli")
    
    onerilen_seviye = "Bilişim Etiği: Temel Modül" if st.session_state.skor <= 66 else "Bilişim Etiği: İleri Düzey Modül"
    st.info(f"**Sistem Önerisi:** {onerilen_seviye}\n\n**Canlı Gerekçe (XAI):**\n\n{st.session_state.yz_gerekcesi}")

    st.markdown("---")
    st.subheader("🔑 10.4 Özerklik Kontrol Alanı")
    
    if "secim_yapildi" not in st.session_state:
        st.session_state.secim_yapildi = False
        st.session_state.kullanici_karari = None

    if not st.session_state.secim_yapildi:
        col3, col4 = st.columns(2)
        with col3:
            if st.button("✅ Öneriyi Kabul Ediyorum", use_container_width=True):
                st.session_state.secim_yapildi = True
                st.session_state.kullanici_karari = "Kabul"
                st.rerun()
        with col4:
            if st.button("❌ Öneriye İtiraz Ediyorum / Kendim Seçeceğim", use_container_width=True):
                st.session_state.secim_yapildi = True
                st.session_state.kullanici_karari = "İtiraz"
                st.rerun()

    if st.session_state.secim_yapildi:
        if st.session_state.kullanici_karari == "Kabul":
            st.success(f"🎯 **Kararınız:** Algoritma önerisini kabul ettiniz. Rızanız doğrultusunda içerikler yükleniyor.")
        elif st.session_state.kullanici_karari == "İtiraz":
            st.warning("⚠️ **Kararınız:** Paternalizmi reddettiniz ve kontrolü elinize aldınız!")
            secilen_manuel_seviye = st.selectbox(
                "Çalışmak istediğiniz modülü kendiniz seçin:",
                ["Modül 1: Fikri Mülkiyet", "Modül 2: Veri Mahremiyeti", "Modül 3: Algoritmik Adalet"]
            )
            st.success(f"🚀 Yolunuz özgür iradenizle güncellendi: {secilen_manuel_seviye}")

        if st.button("🔄 Testi Yeniden Başlat"):
            st.session_state.clear()
            st.rerun()
