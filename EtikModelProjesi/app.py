import streamlit as st
import time
from google import genai

# !!! BURAYA GOOGLE AI STUDIO'DAN ALDIĞIN API ANAHTARINI YAPIŞTIR !!!
API_KEY = "AQ.Ab8RN6KyefGN3q9iw5V0CVr2Km9YRvs_wrO9_UxlIxImkPbZfQ"

# Yapay Zeka İstemcisini Başlatma
def yz_gerekce_uret(skor, sure, hatalar):
    try:
        client = genai.Client(api_key=API_KEY)
        
        # YZ'ye projemizin etik ilkelerini ve öğrenci verilerini içeren bir Prompt hazırlıyoruz
        prompt = f"""
        Sen 'Açıklanabilir Yapay Zeka (XAI)' ve 'Etik Bildirim ve Onay Modeli' prensipleriyle çalışan şeffaf bir eğitsel asistansın.
        Bir öğrenci Bilişim Etiği testini tamamladı. Verileri aşağıdadır:
        - Başarı Skoru: %{skor}
        - Testi Bitirme Süresi: {sure} saniye
        - Yapılan Hatalar: {hatalar if hatalar else 'Hata yok, tam puan.'}
        
        Görevin:
        Öğrenciye %80 başarı eşiğine göre bir seviye önerisinde bulun (Skor düşükse Temel Seviye, yüksekse İleri Seviye).
        En önemlisi, bu önerinin arkasındaki ALGORİTMİK GEREKÇEYİ (XAI) öğrenciye açıkla. 
        Metni yazarken 'paternalist' (otoriter/baskıcı) bir dil kullanma. Öğrencinin bir 'karar verici özne' olduğunu unutma.
        Gerekçeyi doğrudan öğrenciye hitap ederek (en fazla 3-4 cümleyle) samimi ve akademik bir dille yaz.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Yapay zeka bağlantısında bir pürüz oluştu, ancak kural tabanlı öneri geçerlidir. (Hata: {e})"

# Sayfa ayarları ve başlık
st.set_page_config(page_title="Bilişim Etiği - Canlı YZ Destekli Etik Bildirim", page_icon="🤖")
st.title("YZ Destekli Etik Bildirim ve Onay Modeli")
st.write("Bu simülasyon, arka planda canlı Gemini API kullanarak gerekçelerini 'Açıklanabilir YZ (XAI)' ile üretir.")

# Oturum hafızasını başlatalım
if "test_bitti" not in st.session_state:
    st.session_state.test_bitti = False
    st.session_state.baslama_zamani = time.time()

# 10.1: MİNİ TEST ARABİRİMİ
if not st.session_state.test_bitti:
    st.subheader("Bilişim Etiği Mini Tanılama Testi")
    
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
            if soru_1 == "Fikri Mülkiyet ve İntihal": skor += 33.3
            else: hatalar.append("Fikri Mülkiyet Sorusu (Yanlış)")
                
            if soru_2 == "Gizlilik ve Veri Mahremiyeti": skor += 33.3
            else: hatalar.append("Veri Mahremiyeti Sorusu (Yanlış)")
                
            if soru_3 == "Kara Kutu (Black Box) Problemi": skor += 33.4
            else: hatalar.append("Kara Kutu Sorusu (Yanlış)")
            
            st.session_state.skor = round(skor, 1)
            st.session_state.hatalar_metni = ", ".join(hatalar)
            
            # İŞTE BURASI SİHİRLİ NOKTA: Canlı YZ'yi çağırıp gerekçeyi ürettiriyoruz
            with st.spinner("Yapay Zeka metaverilerinizi analiz ediyor ve etik bildirim hazırlıyor..."):
                st.session_state.yz_gerekcesi = yz_gerekce_uret(st.session_state.skor, st.session_state.toplam_sure, st.session_state.hatalar_metni)
            
            st.session_state.test_bitti = True
            st.rerun()
        else:
            st.warning("Lütfen tüm soruları cevaplayın!")

# RESULTS & AX CONTROL AREA
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
    
    # Sabit metin yerine yukarıda Gemini'ın ürettiği dinamik açıklamayı basıyoruz!
    onerilen_seviye = "Bilişim Etiği: Temel Modül" if st.session_state.skor <= 66 else "Bilişim Etiği: İleri Düzey Modül"
    st.info(f"**Sistem Önerisi:** {onerilen_seviye}\n\n**Gemini API Tarafından Üretilen Canlı Gerekçe (XAI):**\n\n{st.session_state.yz_gerekcesi}")

    st.markdown("---")
    st.subheader("Özerklik Kontrol Alanı")
    
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
            st.success(f"🎯 **Kararınız:** Algoritma önerisini kabul ettiniz. Rızanızla yönlendiriliyorsunuz.")
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
