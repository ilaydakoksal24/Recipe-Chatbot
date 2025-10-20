# Recipe-Chatbot
Streamlit ve YOLOv8 kullanarak geliştirilen bir tarif öneri uygulaması.Kullanıcılar elindeki malzemeleri yazar veya fotoğraf yükler, sistem uygun yemek tariflerini önerir.

## Özellikler

- Tarifleri kategori bazlı listeleme (Börekler, Kurabiyeler, Tatlılar, Yemekler)
- Malzemelere göre uygun tarifleri önerme
- Eksik malzemeler için alternatif öneriler
- Fotoğraflardan malzeme tanıma (YOLOv8)
- Kullanımı kolay web arayüzü (Streamlit)

## Kurulum

1. Repo’yu klonlayın:

```bash
git clone https://github.com/kullaniciadi/lezzet-defteri.git
cd lezzet-defteri

2. Sanal ortam oluşturup aktif edin:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt

4. YOLOv8 modelini indirin:
```bash
wget https://ultralytics.com/assets/models/yolov8n.pt

5. Uygulamayı başlatın:
```bash
streamlit run akbank5.py

