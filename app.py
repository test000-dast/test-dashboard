import streamlit as st
import pandas as pd
import altair as alt

# ตั้งค่าหน้า Dashboard
st.set_page_config(page_title="สรุปข้อมูลสถิติรายเดือนโรงพยาบาลราษีไศล", page_icon="📊", layout="wide")

st.title("📊 สรุปข้อมูลสถิติรายเดือนโรงพยาบาลราษี")

# ✅ ให้ผู้ใช้เลือกอัปโหลดหลายไฟล์
uploaded_files = st.file_uploader("📂 อัปโหลดไฟล์ CSV (หลายไฟล์ได้)", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # **โหลดข้อมูลของแต่ละไฟล์**
        df = pd.read_csv(file)

        if df.empty:
            st.error(f"⚠️ ไฟล์ **{file.name}** ไม่มีข้อมูล!")
            continue

        st.write(f"✅ **ไฟล์: {file.name}**")
        st.write(df.head())

        # **ให้ผู้ใช้เลือกคอลัมน์ X และ Y ของแต่ละไฟล์**
        columns = df.columns.tolist()

        x_axis = st.selectbox(f"📌 เลือกแกน X สำหรับไฟล์: {file.name}", columns, key=f"x_{file.name}")
        y_axis = st.selectbox(f"📌 เลือกแกน Y สำหรับไฟล์: {file.name}", columns, key=f"y_{file.name}")

        # ✅ ให้ผู้ใช้ตั้งชื่อกราฟแต่ละไฟล์
        chart_title = st.text_input(f"📝 ตั้งชื่อกราฟสำหรับไฟล์ {file.name}", f"กราฟของ {file.name}")

        # ✅ ตัวเลือกให้เรียงข้อมูลจากมากไปน้อย
        sort_order = st.checkbox(f"🔽 เรียงจากมากไปน้อย ({file.name})", value=True, key=f"sort_{file.name}")

        if not x_axis or not y_axis:
            st.error(f"⚠️ กรุณาเลือกคอลัมน์ X และ Y สำหรับไฟล์: {file.name}")
        else:
            # ตรวจสอบว่าแกน Y เป็นตัวเลข
            if not pd.api.types.is_numeric_dtype(df[y_axis]):
                st.error(f"⚠️ คอลัมน์ {y_axis} ต้องเป็นตัวเลขเท่านั้น! (ไฟล์ {file.name})")
            else:
                # ✅ เรียงค่าตามแกน Y (ถ้าผู้ใช้เลือกให้เรียง)
                if sort_order:
                    df = df.sort_values(by=y_axis, ascending=False)

                st.write(f"### {chart_title}")  # ใช้ชื่อกราฟจาก input

                option = st.selectbox(f"📊 เลือกประเภทกราฟ ({file.name})", ["แท่ง (Bar Chart)", "เส้น (Line Chart)", "กระจาย (Scatter Plot)"], key=f"chart_{file.name}")

                # ✅ ตรวจสอบว่าแกน X เป็นข้อความหรือไม่
                x_type = 'ordinal' if df[x_axis].dtype == object else 'quantitative'

                if option == "แท่ง (Bar Chart)":
                    bars = alt.Chart(df).mark_bar().encode(
                        x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),  # ✅ บังคับให้เรียง X ตาม DataFrame
                        y=alt.Y(y_axis, type='quantitative')
                    ).properties(title=chart_title, width=800, height=400)

                    text = alt.Chart(df).mark_text(
                        align='center',
                        baseline='bottom',
                        dy=-5,
                        fontSize=12,
                        color='black'
                    ).encode(
                        x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                        y=alt.Y(y_axis, type='quantitative'),
                        text=y_axis
                    )

                    st.altair_chart(bars + text, use_container_width=True)

                elif option == "เส้น (Line Chart)":
                    chart = alt.Chart(df).mark_line().encode(
                        x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                        y=alt.Y(y_axis, type='quantitative')
                    ).properties(title=chart_title, width=800, height=400)
                    st.altair_chart(chart, use_container_width=True)

                else:  # กระจาย (Scatter Plot)
                    chart = alt.Chart(df).mark_circle().encode(
                        x=alt.X(x_axis, type=x_type, sort=df[x_axis].tolist()),
                        y=alt.Y(y_axis, type='quantitative')
                    ).properties(title=chart_title, width=800, height=400)
                    st.altair_chart(chart, use_container_width=True)


