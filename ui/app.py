import streamlit as st
import os
import io
import pandas as pd
import time

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from logic.load_file import load_file
from logic.time_translate_04 import time_translate
from logic.download_file import to_excel_xlsxwriter
from logic.download_file import to_excel_fast_numpy
from logic.download_file import to_csv_fast

# ★ 高速 xlsxwriter 版 Excel 変換関数
#def to_excel_xlsxwriter(df):
#    output = io.BytesIO()
    
#    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
#        df.to_excel(writer, index=False, sheet_name='Sheet1')
#    return output.getvalue()

    

def main():
    st.title("勤怠データチェックアプリ")

    uploaded_file = st.file_uploader(
        "CSVまたはExcelファイルをアップロードしてください",
        type=["csv", "xlsx", "xlsm"]
    )

    # ★ タイマー開始
    start = time.time()

    if uploaded_file is not None:
        st.success("ファイルを読み込みました")

        # ★ タイマー開始
        start = time.time()
        
        df = load_file(uploaded_file)
        st.write("df.shape:", df.shape)

        
        # df2 = time_translate(df)

        # ★ ここで Excel バイト列を作る（高速）
        # st.write("Making download file with xlsxwriter")
        # excel_bytes = to_excel_xlsxwriter(df2)
        st.write("Translating time to numerics ...")
        final_array, headers = time_translate(df)

        # st.write("Making download file with fast_numpy")
        # excel_bytes = to_excel_fast_numpy(final_array, headers)

        st.write("Making download file with to_csv_fast")
        csv_bytes = to_csv_fast(final_array, headers)

        base_name = os.path.splitext(uploaded_file.name)[0]
        download_name = f"{base_name}_output.xlsx"
        
        st.download_button(
            label="CSVでダウンロード",
            data=csv_bytes,
            file_name=f"{base_name}_output.csv",
            mime="text/csv"
        )

        
        # ★ タイマー終了
        end = time.time() 
        elapsed = end - start

        # ★ 結果表示
        st.info(f"処理時間: {elapsed:.2f} 秒")
        
 

        # ★ ダウンロードボタン
        # st.download_button(
        #    label="変換ファイルをダウンロード",
        #    data=excel_bytes,
        #    file_name=download_name,
        #    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        # )


if __name__ == "__main__":
    main()
