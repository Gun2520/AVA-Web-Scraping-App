import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บแอพ
st.set_page_config(page_title="AVA Property Scraper", layout="wide")

# CSS เพื่อปรับ UI ให้สวยงาม
st.markdown("""
<style>
    .stApp {
        background-color: #f9f9f9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# หัวข้อหลัก
st.title("📊 AVA Property Scraper")
st.markdown("### ระบุเงื่อนไขการ scraping เพื่อดึงข้อมูลอสังหาริมทรัพย์")

# ฟอร์มกรอกข้อมูล
col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input("ชื่อโครงการ", placeholder="เช่น บ้านพฤกษา")
    property_type = st.selectbox("ประเภททรัพย์สิน", ["คอนโด", "ทาวน์เฮ้าส์", "บ้านเดี่ยว", "ที่ดิน"])

with col2:
    area_unit = st.radio("หน่วยพื้นที่", ["ตร.วา", "ตร.ม."])
    min_area = st.number_input(f"ขนาดพื้นที่ขั้นต่ำ ({area_unit})", min_value=0.0)
    max_area = st.number_input(f"ขนาดพื้นที่สูงสุด ({area_unit})", min_value=0.0)

st.markdown("### 🌐 เว็บไซต์ที่ต้องการ scrape")
urls = st.text_area("ใส่ URL หลาย URL ได้ เว้นบรรทัด", placeholder="https://ddproperty.com/... \nhttps://baandek.com/... ")

start_button = st.button("🚀 เริ่ม scraping", use_container_width=True)

if start_button:
    if not urls.strip():
        st.warning("กรุณาใส่ URL ที่ต้องการ scrape")
    else:
        st.info("กำลังดึงข้อมูล กรุณารอสักครู่...")

        # สร้างข้อมูลตัวอย่าง
        df = pd.DataFrame({
            'ชื่อโครงการ': ['บ้านพฤกษา', 'สวนคอนโด', 'บ้านสวนงาม', 'บ้านบางกอก', 'คอนโดศรีนคร'],
            'ประเภททรัพย์สิน': ['ทาวน์เฮ้าส์', 'คอนโด', 'บ้านเดี่ยว', 'บ้านเดี่ยว', 'คอนโด'],
            'ราคา': [2700000, 2200000, 3500000, 4500000, 3000000],
            'ขนาดพื้นที่': ['35 ตร.วา', '28 ตร.วา', '50 ตร.วา', '60 ตร.วา', '30 ตร.วา']
        })

        st.success(f"✅ พบข้อมูลทั้งหมด {len(df)} รายการ")

        # แสดงตารางผลลัพธ์
        st.subheader("🔍 ผลลัพธ์การ scraping")
        st.dataframe(df)

        # ปุ่มดาวน์โหลด Excel
        st.download_button(
            label="📥 ดาวน์โหลด Excel",
            data=df.to_excel(index=False),
            file_name="property_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # แสดงสถิติ
        st.markdown("### 📊 สถิติและ Dashboard")

        total_records = len(df)
        avg_price = df['ราคา'].mean()

        col1, col2 = st.columns(2)
        col1.metric("จำนวนประกาศทั้งหมด", total_records)
        col2.metric("ราคาเฉลี่ย (บาท)", f"{avg_price:,.2f}")

        # กราฟราคาต่อตร.วา
        df['พื้นที่'] = df['ขนาดพื้นที่'].str.replace(' ตร.วา| ตร.ม.', '', regex=True).astype(float)
        df['ราคาต่อตร.วา'] = df['ราคา'] / df['พื้นที่']

        fig = px.bar(df, x='ชื่อโครงการ', y='ราคาต่อตร.วา', title='ราคาต่อตร.วา ของแต่ละโครงการ')
        st.plotly_chart(fig)

        # กราฟประเภททรัพย์สิน
        fig2 = px.pie(df, names='ประเภททรัพย์สิน', title='สัดส่วนประเภททรัพย์สิน')
        st.plotly_chart(fig2)
