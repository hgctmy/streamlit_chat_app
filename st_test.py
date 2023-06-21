# -*- coding: utf-8 -*-
import streamlit as st

st.title("ニュース解説チャットボット")
st.header("選んだニュースをチャットボットが対話形式で解説してくれます．提示される質問や反応を選んで対話を進めましょう！")

kiji = st.radio("記事を選んでください\n1. 記事1のタイトル\n2. 記事2のタイトル", (1, 2))
if not st.checkbox("記事を選択しました．"):
    st.stop()

st.text("ChatGPT:")
i = 0
while True:
    st.text(i)
    i += 1
    check = st.checkbox("選択完了", key=i)
    st.markdown("っっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっっkっっっっっっっっっっっっっっっっっっk")
    if not check:
        st.stop()
    i += 1
    if st.checkbox("対話を終了", key=i):
        break
