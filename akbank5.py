
'''
Elindeki malzemeleri söylediğin ya da dolabının fotoğrafını çekip ordaki malzemeleri algılayan
ve ona göre sana tarif önerisi yapan bir program.

'''

import streamlit as st
from PIL import Image
from ultralytics import YOLO

# === SAYFA AYARLARI ===
st.set_page_config(page_title="🍳 Lezzet Defteri", page_icon="🍲", layout="wide")
st.title("🍴 Lezzet Defteri – Görsel Tanıma Destekli Tarif Asistanı")
st.markdown("### Elindeki malzemeleri yaz veya fotoğraf yükle – sana uygun tarifleri bulayım! 👩‍🍳")

# === YOLOv8 MODELİ ===
@st.cache_resource
def yukle_model():
    return YOLO("yolov8n.pt")  # küçük ve hızlı model

model = yukle_model()

# === ALTERNATİF MALZEMELER ===
alternatifler = {
    "yoğurt": ["süt + limon", "krema"],
    "tereyağı": ["margarin", "zeytinyağı"],
    "beyaz peynir": ["lor peyniri", "labne"],
    "yumurta": ["muz püresi", "chia tohumu"],
    "süt": ["badem sütü", "hindistan cevizi sütü"],
    "şeker": ["bal", "hurma püresi"],
    "un": ["tam buğday unu", "yulaf unu"],
    "krema": ["süt + tereyağı"]
}

# === TARİFLER ===

tarifler = {
    "Börekler": {
        "Peynirli Börek": {
            "malzemeler":["yufka", "beyaz peynir", "maydanoz", "sıvı yağ", "yumurta", "süt", "tuz"],
            "adimlar":["Yufkayı ser.","Peynir ve maydanozu karıştır.","Yufkayı katla, yağla ve pişir."]
        },
        "Patatesli Börek": {
            "malzemeler":["yufka", "patates", "soğan", "sıvı yağ", "tuz", "karabiber", "pul biber", "yumurta"],
            "adimlar":["Patatesleri haşla ve ezin.","Soğanı kavur, patatesle karıştır.","Yufkayı aç, harcı koy, katla ve pişir."]
        },
        "Ispanaklı Börek": {
            "malzemeler":["yufka", "ıspanak", "soğan", "beyaz peynir", "sıvı yağ", "tuz", "yumurta"],
            "adimlar":["Ispanak ve soğanı kavur.","Peynirle karıştır.","Yufkayı aç, harcı koy, katla ve pişir."]
        },
        "Su Böreği": {
            "malzemeler":["yufka", "peynir", "maydanoz", "tereyağı", "yumurta", "süt", "tuz"],
            "adimlar":["Yufkaları haşla ve kat kat yerleştir.","Peynirli harcı ekle.","Fırında pişir."]
        },
        "Sigara Böreği": {
            "malzemeler":["yufka", "beyaz peynir", "maydanoz", "sıvı yağ"],
            "adimlar":["Peynirli harcı yufkaya koy.","Sigara şeklinde sar.","Kızart."]
        }
    },
    "Kurabiyeler": {
        "Un Kurabiyesi": {
            "malzemeler":["un", "pudra şekeri", "margarin", "vanilin"],
            "adimlar":["Malzemeleri karıştır.","Hamuru şekillendir.","Fırında pişir."]
        },
        "Çikolatalı Kurabiye": {
            "malzemeler":["un", "şeker", "tereyağı", "yumurta", "kakao", "kabartma tozu", "damla çikolata"],
            "adimlar":["Malzemeleri karıştır.","Hamuru şekillendir.","Fırında pişir."]
        },
        "Kakaolu Kurabiye": {
            "malzemeler":["un", "tereyağı", "şeker", "yumurta", "kakao", "kabartma tozu", "vanilin"],
            "adimlar":["Malzemeleri karıştır.","Hamuru şekillendir.","Fırında pişir."]
        },
        "Cevizli Kurabiye": {
            "malzemeler":["un", "tereyağı", "şeker", "yumurta", "ceviz", "kabartma tozu"],
            "adimlar":["Malzemeleri karıştır.","Hamuru şekillendir.","Fırında pişir."]
        },
        "Elmalı Kurabiye": {
            "malzemeler":["un", "tereyağı", "yumurta", "kabartma tozu", "şeker", "elma", "tarçın", "ceviz"],
            "adimlar":["Elma ve tarçını karıştır.","Hamuru hazırlayıp şekil ver.","Fırında pişir."]
        },
        "Kurabiye": {
            "malzemeler":["yumurta","şeker","yağ","un","vanilya"],
            "adimlar":["Malzemeleri karıştır.","Hamuru şekillendir.","Fırında pişir."]
        }
    },
    "Tatlılar": {
        "Islak Kek": {
            "malzemeler":["un","kakao","şeker","süt","yumurta","yağ","kabartma tozu","vanilya"],
            "adimlar":["Yumurta ve şekeri çırp.","Sıvı malzemeleri ekle.","Un, kakao ve kabartma tozunu ekle.","Fırında 180°C’de pişir."]
        },
        "Trileçe": {
            "malzemeler":["un","yumurta","şeker","süt","karamel","krema"],
            "adimlar":["Yumurtaları ve şekeri çırp.","Un ekleyip karıştır.","Fırında pişir.","Sütlü karışımı dök, üzerine karamel ekle."]
        },
        "Sütlaç": {
            "malzemeler":["pirinç","süt","şeker","nişasta","vanilin"],
            "adimlar":["Süt ve pirinci pişir.","Nişasta ve şekeri ekle.","Koyulaşınca kaselere dök."]
        },
        "Muhallebi": {
            "malzemeler":["süt","şeker","nişasta","un","tereyağı","vanilin"],
            "adimlar":["Süt ve nişastayı karıştır.","Şekeri ekle, pişir.","Tereyağı ve vanilini ekle."]
        },
        "Revani": {
            "malzemeler":["yumurta","şeker","yoğurt","irmik","un","kabartma tozu","şerbet"],
            "adimlar":["Yumurtaları çırp.","Malzemeleri karıştır.","Fırında pişir.","Şerbeti dök."]
        },
        "Profiterol": {
            "malzemeler":["un","tereyağı","yumurta","su","krem şanti","çikolata"],
            "adimlar":["Hamuru hazırla ve pişir.","Krem şantiyi ekle.","Üzerine çikolata dök."]
        },
        "Magnolia": {
            "malzemeler":["süt","şeker","nişasta","yumurta","bisküvi","muz","vanilin"],
            "adimlar":["Puding yap gibi pişir.","Bisküvi ve muz ile kat kat yerleştir.","Soğuyunca servis et."]
        },
        "Puding": {
            "malzemeler":["süt","şeker","kakao","nişasta","vanilin"],
            "adimlar":["Malzemeleri pişirerek karıştır.","Koyulaşınca servis et."]
        },
        "Kazandibi": {
            "malzemeler":["süt","şeker","pirinç unu","vanilin","tereyağı"],
            "adimlar":["Malzemeleri karıştır.","Pişir ve karamelize et.","Servis et."]
        },
        "Kek": {
            "malzemeler":["yumurta","süt","şeker","yağ","un","vanilya","kabartma tozu","kakao"],
            "adimlar":["Malzemeleri karıştır.","Fırına ver.","Pişir ve soğut."]
        }
    },
    "Yemekler": {
        "Köfte": {
            "malzemeler":["kıyma","yumurta","galeta unu","tuz","karabiber","soğan"],
            "adimlar":["Soğanı rendele.","Kıymayı, yumurtayı, galeta ununu ve baharatları ekle.","Yoğur ve şekil ver.","Kızart veya fırınla."]
        },
        "Tavuk Sote": {
            "malzemeler":["tavuk","biber","domates","soğan","tuz","yağ"],
            "adimlar":["Tavuğu doğra.","Sebzeleri kavur.","Tavuğu ekle ve pişir."]
        },
        "Peynirli Makarna":{
            "malzemeler":["makarna","peynir","tereyağı","süt","tuz"],
            "adimlar":["Makarnayı haşla.","Peynir ve tereyağı ile karıştır.","Servis et."]
        },
        "Kremalı Tavuk Makarna":{
            "malzemeler":["makarna","tavuk","krema","tuz","karabiber","yağ"],
            "adimlar":["Tavuğu pişir.","Makarnayı ekle ve kremayla karıştır.","Servis et."]
        },
        "Menemen":{
            "malzemeler":["yumurta","domates","biber","tuz","soğan"],
            "adimlar":["Sebzeleri kavur.","Yumurtayı ekle ve karıştır.","Servis et."]
        },
        "Karnıyarık":{
            "malzemeler":["patlıcan","kıyma","soğan","domates","biber","tuz","yağ"],
            "adimlar":["Patlıcanları kızart.","Kıymalı harcı hazırla.","Patlıcanlara doldur ve pişir."]
        },
        "Musakka":{
            "malzemeler":["patlıcan","kıyma","soğan","domates","tuz","yağ"],
            "adimlar":["Patlıcanları kızart.","Kıymalı harcı hazırla.","Katmanlayıp pişir."]
        },
        "Karnabahar Graten":{
            "malzemeler":["karnabahar","süt","un","tereyağı","kaşar","tuz","karabiber"],
            "adimlar":["Karnabaharı haşla.","Beşamel sosu hazırla.","Fırına ver."]
        }
    }
}


# === KATEGORİ SEÇİMİ ===
kategori = st.sidebar.selectbox("🍱 Kategori Seç:", list(tarifler.keys()))
tarif_adi = st.sidebar.selectbox("🍰 Tarif Seç:", list(tarifler[kategori].keys()))
tarif = tarifler[kategori][tarif_adi]

col1, col2 = st.columns([1, 2])
with col1:
    gorsel = tarif["gorsel"] if tarif["gorsel"] else "https://via.placeholder.com/400x300.png?text=Gorsel+Yok"
    st.image(gorsel, use_container_width=True)
with col2:
    st.subheader(tarif_adi)
    st.markdown("### 🧾 Malzemeler:")
    st.write(", ".join(tarif["malzemeler"]))

st.markdown("### 👩‍🍳 Yapılış Adımları:")
for i, adim in enumerate(tarif["adimlar"], 1):
    st.markdown(f"{i}. {adim}")

st.divider()

# === FOTOĞRAFTAN MALZEME TANIMA (YOLOv8) ===
st.subheader("📸 Görüntüden Malzeme Tanıma")
uploaded_file = st.file_uploader("Bir fotoğraf yükle:", type=["jpg", "png", "jpeg"])
taninan_malzemeler = []

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Yüklenen Görsel", use_container_width=True)
    with st.spinner("🧠 Görsel analiz ediliyor..."):
        results = model.predict(source=image, imgsz=320, conf=0.25, verbose=False)
        for r in results:
            if hasattr(r, 'boxes'):
                names = [r.names[int(cls)] for cls in r.boxes.cls]
                taninan_malzemeler.extend(names)
    if taninan_malzemeler:
        taninan_malzemeler = list(set(taninan_malzemeler))
        st.success(f"Tespit edilen nesneler: {', '.join(taninan_malzemeler)}")
    else:
        st.warning("Hiç nesne tespit edilmedi.")

st.divider()

# === ELİNDEKİ MALZEMELERE GÖRE TARİF BUL ===
st.subheader("🥣 Elindekilere Göre Tarif Önerisi")
malzeme_girdisi = st.text_input("Elindeki malzemeleri yaz (örn: un, süt, yumurta):")

if st.button("🔎 Tarifleri Bul"):
    girilen = [m.strip().lower() for m in malzeme_girdisi.split(",") if m.strip()]
    if taninan_malzemeler:
        girilen.extend([m.lower() for m in taninan_malzemeler])
    if not girilen:
        st.error("Lütfen en az bir malzeme gir veya fotoğraf yükle!")
    else:
        uygun_tarifler = []
        for kat, kat_tarifleri in tarifler.items():
            for ad, veri in kat_tarifleri.items():
                tarif_malz = set(veri["malzemeler"])
                eslesen = tarif_malz & set(girilen)
                eksik = tarif_malz - set(girilen)
                oran = round(len(eslesen) / len(tarif_malz) * 100, 1)
                uygun_tarifler.append((ad, oran, veri["gorsel"], eksik, veri["adimlar"]))
        uygun_tarifler.sort(key=lambda x: x[1], reverse=True)
        st.subheader("🍽️ Uygun Tarifler:")
        for ad, oran, gorsel, eksik, adimlar in uygun_tarifler[:5]:
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    gorsel = gorsel if gorsel else "https://via.placeholder.com/400x300.png?text=Gorsel+Yok"
                    st.image(gorsel, caption=f"{ad} (%{oran})", use_container_width=True)
                with col2:
                    st.write(f"✅ **Uygunluk Oranı:** %{oran}")
                    if eksik:
                        st.write("⚠️ Eksik Malzemeler:", ", ".join(eksik))
                        for malz in eksik:
                            if malz in alternatifler:
                                st.info(f"💡 {malz} yerine şunları kullanabilirsin: {', '.join(alternatifler[malz])}")
                    else:
                        st.success("Tüm malzemeler mevcut! 🎉")
                    st.markdown("**👩‍🍳 Yapılış Adımları:**")
                    for i, adim in enumerate(adimlar, 1):
                        st.markdown(f"{i}. {adim}")
                st.markdown("---")

st.caption("👩‍🍳 Afiyet Olsun!")


