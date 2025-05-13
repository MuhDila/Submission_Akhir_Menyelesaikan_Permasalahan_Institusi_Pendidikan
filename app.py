import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("model/rf_model.pkl")

# Judul aplikasi
st.title("Prediksi Status Mahasiswa")
st.write("Masukkan data mahasiswa untuk memprediksi apakah akan Dropout, Enrolled, atau Graduate.")

# Form input user
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Usia saat mendaftar", min_value=15, max_value=70, value=18)
        admission_grade = st.slider("Nilai ujian masuk", 0, 200, 130)
        gender = st.selectbox("Jenis Kelamin", options=[0, 1], format_func=lambda x: "Perempuan" if x==0 else "Laki-laki")
        debtor = st.selectbox("Status Utang", options=[0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        enrolled1 = st.slider("Mata kuliah semester 1 diambil", 0, 10, 6)
        approved1 = st.slider("Mata kuliah semester 1 disetujui", 0, 10, 5)
        grade1 = st.slider("Nilai semester 1", 0.0, 20.0, 12.0)
    with col2:
        enrolled2 = st.slider("Mata kuliah semester 2 diambil", 0, 10, 6)
        approved2 = st.slider("Mata kuliah semester 2 disetujui", 0, 10, 5)
        grade2 = st.slider("Nilai semester 2", 0.0, 20.0, 12.0)
        displaced = st.selectbox("Mahasiswa Perantau", options=[0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        scholarship = st.selectbox("Penerima Beasiswa", options=[0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        tuition_paid = st.selectbox("Pembayaran UKT Lancar", options=[0, 1], format_func=lambda x: "Tidak" if x==0 else "Ya")
        submit = st.form_submit_button("Prediksi")

# Prediksi
if submit:
    # Susun data input sebagai dataframe
    input_df = pd.DataFrame([{
        'Marital_status': 1,
        'Application_mode': 17,
        'Application_order': 1,
        'Course': 9238,
        'Daytime_evening_attendance': 1,
        'Previous_qualification': 1,
        'Previous_qualification_grade': 130,
        'Nacionality': 1,
        'Mothers_qualification': 19,
        'Fathers_qualification': 19,
        'Mothers_occupation': 4,
        'Fathers_occupation': 4,
        'Admission_grade': admission_grade,
        'Displaced': displaced,
        'Educational_special_needs': 0,
        'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition_paid,
        'Gender': gender,
        'Scholarship_holder': scholarship,
        'Age_at_enrollment': age,
        'International': 0,
        'Curricular_units_1st_sem_credited': 0,
        'Curricular_units_1st_sem_enrolled': enrolled1,
        'Curricular_units_1st_sem_evaluations': enrolled1,
        'Curricular_units_1st_sem_approved': approved1,
        'Curricular_units_1st_sem_grade': grade1,
        'Curricular_units_1st_sem_without_evaluations': 0,
        'Curricular_units_2nd_sem_credited': 0,
        'Curricular_units_2nd_sem_enrolled': enrolled2,
        'Curricular_units_2nd_sem_evaluations': enrolled2,
        'Curricular_units_2nd_sem_approved': approved2,
        'Curricular_units_2nd_sem_grade': grade2,
        'Curricular_units_2nd_sem_without_evaluations': 0,
        'Unemployment_rate': 10.2,
        'Inflation_rate': 1.4,
        'GDP': 2.5
    }])

    # Prediksi
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]

    label_map = {0: 'Dropout', 1: 'Enrolled', 2: 'Graduate'}
    st.success(f"Prediksi Status Mahasiswa: {label_map[prediction]}")

    # Tampilkan probabilitas
    st.write("### Probabilitas Prediksi:")
    st.write({
        'Dropout': round(proba[0], 2),
        'Enrolled': round(proba[1], 2),
        'Graduate': round(proba[2], 2)
    })
