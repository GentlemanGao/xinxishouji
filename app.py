import streamlit as st
import pandas as pd
import os

# 设置网页配置
st.set_page_config(page_title="信息收集", layout="centered")

st.title("数字替身：一种面向未知危害消解的APT防御模型（云晓春）")
st.write("请填写以下信息，完成后点击提交。")

# --- 1. 用户填写区域 ---
with st.form("my_form", clear_on_submit=True):
    name = st.text_input("姓名")
    company = st.text_input("单位")
    college = st.text_input("所属学院")
    job_title = st.text_input("职务/职称")
    phone = st.text_input("联系电话")
    submitted = st.form_submit_button("提交信息")

# --- 2. 处理数据保存 ---
file_name = "user_info.xlsx"

if submitted:
    if name and phone:
        new_data = {
            "姓名": [name],
            "单位": [company],
            "所属学院": [college],
            "职务/职称": [job_title],
            "联系电话": [phone]
        }
        df = pd.DataFrame(new_data)
        
        if not os.path.isfile(file_name):
            df.to_excel(file_name, index=False)
        else:
            existing_df = pd.read_excel(file_name)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_excel(file_name, index=False)
            
        st.success("提交成功！谢谢您的配合。")
    else:
        st.error("请至少填写姓名和联系电话。")

# --- 3. 管理员后台 (隐藏在侧边栏) ---
# st.sidebar 是网页左侧的侧边栏区域
st.sidebar.header("管理员登录")
password = st.sidebar.text_input("输入密码查看数据", type="password")

# 这里设置你的密码，比如我设成了 "123456"
MY_SECRET_PASSWORD = "123456"

if password == MY_SECRET_PASSWORD:
    st.sidebar.success("已验证")
    
    st.divider()
    st.subheader("📊 管理员后台数据")
    
    if os.path.isfile(file_name):
        st.write(f"数据文件已生成，点击下方下载：")
        
        # 读取文件用于下载
        with open(file_name, "rb") as file:
            btn = st.download_button(
                label="📥 下载 Excel 文件",
                data=file,
                file_name="user_info.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # 展示数据预览
        st.write("数据预览：")
        df_show = pd.read_excel(file_name)
        st.dataframe(df_show)
    else:
        st.info("暂时还没有用户提交数据。")

