import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Modeli yükle
model = joblib.load('eniyi.joblib')

# Eğitimde kullanılan özellik isimleri
feature_names = [
    'Yıl', 'Kilometre', 'Motor Hacmi', 'Güç (HP)', 
    'Marka_Ford', 'Marka_Honda', 'Marka_Mercedes', 'Marka_Nissan', 'Marka_Tesla', 'Marka_Toyota',
    'Marka_Volkswagen', 'Marka_BMW', 'Marka_Audi', 'Model_Civic', 'Model_Focus', 'Model_Model 3', 
    'Model_320i', 'Model_C-Class', 'Model_A4', 'Model_Golf', 'Yakıt Türü_Dizel', 'Yakıt Türü_Elektrikli', 
    'Yakıt Türü_Hibrit', 'Vites Türü_Manuel', 'Renk_Gri', 'Renk_Kırmızı', 'Renk_Mavi', 
    'Renk_Siyah', 'Durum_İkinci El'
]

# Kullanıcı arayüzü tasarımı
st.title("Araba Fiyat Tahmin Uygulaması")
st.write("Lütfen aracınızın özelliklerini girin:")

# Kullanıcı girişleri
marka = st.selectbox("Marka", ['Toyota', 'Ford', 'Tesla', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Honda', 'Nissan'])
modeli = st.selectbox("Model", ['Corolla', 'Focus', 'Model 3', '320i', 'C-Class', 'A4', 'Golf', 'Civic', 'Altima'])
yil = st.slider("Üretim Yılı", 2000, 2024, 2018)
km = st.number_input("Kilometre", 0, 300000, 50000)
yakit = st.selectbox("Yakıt Türü", ['Benzin', 'Dizel', 'Elektrikli', 'Hibrit'])
vites = st.selectbox("Vites Türü", ['Otomatik', 'Manuel'])
motor_hacmi = st.slider("Motor Hacmi (Litre)", 1.0, 4.0, 1.6)
guc = st.slider("Güç (HP)", 60, 400, 120)
renk = st.selectbox("Renk", ['Beyaz', 'Gri', 'Siyah', 'Mavi', 'Kırmızı'])
durum = st.selectbox("Durum", ['Sıfır', 'İkinci El'])

# Tahmin düğmesi
if st.button("Fiyat Tahmin Et"):
    # Giriş verilerini birleştirme
    input_data = {
        'Yıl': yil,
        'Kilometre': km,
        'Motor Hacmi': motor_hacmi,
        'Güç (HP)': guc
    }

    # Markayı dummy değişkenlere çevirme
    marka_listesi = ['Ford', 'Honda', 'Mercedes', 'Nissan', 'Tesla', 'Toyota', 'Volkswagen', 'BMW', 'Audi']
    for mark in marka_listesi:
        input_data[f'Marka_{mark}'] = 1 if marka == mark else 0

    # Modeli dummy değişkenlere çevirme
    model_listesi = ['Civic', 'Focus', 'Model 3', '320i', 'C-Class', 'A4', 'Golf']
    for mod in model_listesi:
        input_data[f'Model_{mod}'] = 1 if modeli == mod else 0

    # Yakıt türünü dummy değişkenlere çevirme
    yakit_listesi = ['Dizel', 'Elektrikli', 'Hibrit']
    for fuel in yakit_listesi:
        input_data[f'Yakıt Türü_{fuel}'] = 1 if yakit == fuel else 0

    # Vites türünü dummy değişkenlere çevirme
    input_data['Vites Türü_Manuel'] = 1 if vites == 'Manuel' else 0

    # Renk dummy değişkenlerine çevirme
    renk_listesi = ['Gri', 'Kırmızı', 'Mavi', 'Siyah']
    for color in renk_listesi:
        input_data[f'Renk_{color}'] = 1 if renk == color else 0

    # Durum dummy değişkenine çevirme
    input_data['Durum_İkinci El'] = 1 if durum == 'İkinci El' else 0

    # DataFrame oluşturma
    input_df = pd.DataFrame([input_data])

    # Eksik kolonları ekleme (eğer varsa)
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0

    # Kolonları sıraya göre ayarlama
    input_df = input_df[feature_names]

    # Modeli kullanarak tahmin yapma
    prediction = model.predict(input_df)

    # Tahmini gösterme
    st.write(f"Arabanızın tahmini fiyatı: {prediction[0]:.2f} TL")
