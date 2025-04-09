import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Excel Merger", layout="centered")
st.title("🔗 Excel File Merger")

st.markdown("""
Upload multiple Excel files and specify the column name to merge them by.  
All files should have that column present.
""")

uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx"], accept_multiple_files=True)

join_column = st.text_input("Enter the column name to join on (e.g., 'CustomerID')")

if uploaded_files and join_column:
    try:
        dfs = [pd.read_excel(file) for file in uploaded_files]
        merged_df = dfs[0]

        for df in dfs[1:]:
            merged_df = pd.merge(merged_df, df, on=join_column, how='outer')

        st.success("✅ Files merged successfully!")
        st.dataframe(merged_df)

        # Prepare Excel for download
        output = BytesIO()
        merged_df.to_excel(output, index=False)
        output.seek(0)

        st.download_button("📥 Download Merged File", output, file_name="merged_result.xlsx")

    except Exception as e:
        st.error(f"❌ Error: {e}")
