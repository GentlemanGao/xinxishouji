import streamlit as st
import pandas as pd
import os

st.title("用户信息收集系统")
st.write("请填写以下信息，完成后点击提交。")

# --- 1. 创建输入表单 ---
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

        st.success("提交成功！")
    else:
        st.error("请至少填写姓名和联系电话。")

# --- 3. 管理员下载区域 (新增功能) ---
st.divider()  # 画一条分割线
st.subheader("管理员后台")

# 只有当文件存在时，才显示下载按钮
if os.path.isfile(file_name):
    st.write(f"当前已收集数据，点击下方按钮下载：")

    # 读取文件用于下载
    with open(file_name, "rb") as file:
        btn = st.download_button(
            label="📥 下载 Excel 文件",
            data=file,
            file_name="user_info.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # 为了方便你看，还是展示一下表格
    df_show = pd.read_excel(file_name)
    st.dataframe(df_show)
else:
    st.info("暂无数据。")