# -*- coding: utf-8 -*-
import os
import streamlit as st
import openai
import kensaku
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(join(dirname(__file__), '.env'))
openai.api_key = os.environ.get("API_KEY")


st.title("ニュース解説チャットボット")
st.header("選んだニュースをチャットボットが対話形式で解説してくれます．提示される質問や反応を選んで対話を進めましょう！")

kiji = st.radio("記事を選んでください\n1. 記事1のタイトル\n2. 記事2のタイトル", (1, 2))
if not st.checkbox("記事を選択しました．"):
    st.stop()

# 説明してもらう文章
# exampletexts = "くらやみ祭り（くらやみまつり）は、主に5月3日〜6日にかけて東京都府中市の大國魂神社（武蔵国の国府である当地の総社）で行われる例大祭で、武蔵国の「国府祭」を起源としており、東京都指定無形民俗文化財となっている。期間中は約70万人の人出で賑わう。古く武蔵国の国府で行われた国府祭を由来とする、長い伝統と格式を誇る大國魂神社の「例大祭」である。室町時代の文書には「五月会」と記録があり、江戸中から見物人が多く訪れていた。その後は、地域住民の祭礼へと発展していった。かつて街の明かりを消した深夜の暗闇の中で行われていたため「くらやみ祭」と呼ばれるようになった。「江戸名所図会」という江戸時代の観光案内においては、江戸近郊で盛大に続けられている古い祭りとして紹介され「五月五日六所宮祭礼之図」が掲載されている。また、幕末に来日したスイスの外交官アンベールはくらやみ祭りの詳細な記録を残しており、「LA MATSOURI DE ROKSA-MIA:RETOUR TEMPLE APRES LA PURIFICATION DES LIEUX SACRES」には祭りのイラストが掲載されている。府中市の中心部を六張もの大太鼓と八基の神輿が回る壮大な祭として知られている。"

exampletexts = "対話式AIの「ChatGPT」に対してプライバシー侵害などの懸念が出ていることから、開発したアメリカのベンチャー企業は、子どもを保護するため利用者は18歳以上とするなど安全対策の強化方針を示しました。\nまるで人間が書いたかのような自然な文章を作成できる「ChatGPT」は世界で利用が急速に広がっています。一方で、プライバシー侵害への懸念からイタリアの当局がこの対話式AIを一時的に使用禁止にする措置をとり、ほかのヨーロッパ各国も同じような措置をとる可能性が指摘されています。\nこうした中「ChatGPT」を開発した「オープンAI」は、公式ブログを通じて安全対策の強化方針を示しました。\nこの中で、AIが学習するデータには個人情報も含まれているものの可能なかぎり削除していると説明したほか、AIが作成する回答については暴力などを含む内容は生成されないようにしているとしています。\n最新のソフトはこれまでのものと比較して、許可していない内容の回答をする可能性が82％低くなったと説明しています。\nさらに子どもの保護を重要な課題の1つとしてあげており、利用者は18歳以上、または保護者の許可を得た13歳以上にかぎり、今後、年齢を確認する仕組みの導入を検討しています。"
assistant_1 = [
    {"role": "system", "content": "あなたは便利なアシスタントです．以下の文章を参照して答えてください．\n\n###文章###\n" + exampletexts},
    {"role": "user", "content": "まずは文章の導入部分を1文で簡単に述べてください．"}
]
# 記事の説明文を生成
completion1 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=assistant_1
)
a1message = completion1.choices[0].message.content

dialog = [a1message]

# 初めの質問候補を生成
assistant_tmp = [
    {"role": "system", "content": "あなたは便利なアシスタントです．"},
    {"role": "user", "content": "###指示###\n以下の文章について，質問文の候補を3つ作成してください．フォーマットは番号つきリストとします．\n\n###文章###\n" + a1message}
]
completion_tmp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=assistant_tmp
)
question = completion_tmp.choices[0].message.content

st.text("ChatGPT:")
st.text(a1message)
aizuchi = ''
i = 0
while True:
    if aizuchi:
        choices = [question.split("\n")[0][2:], question.split("\n")[1][2:], aizuchi]
    else:
        choices = [question.split("\n")[i][2:] for i in range(3)]
    user_input = st.radio("候補", choices)
    check = st.checkbox("選択完了", key=i)
    if not check:
        st.stop()
    i += 1
    if st.checkbox("対話を終了"):
        break
    # 質問に答えてもらう
    choice = {"role": "user", "content": user_input}  # 質問候補文
    assistant_1.append(choice)
    dialog.append(choice["content"])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=assistant_1
    )
    st.text("ChatGPT:")
    if "ません" in completion.choices[0].message.content:
        st.text("検索しています")
        result = kensaku.searchfromquestion(user_input)
        st.text(result)
        dialog.append(result)
    else:
        st.text(completion.choices[0].message.content)
        dialog.append(completion.choices[0].message.content)
    completion2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは便利なアシスタントです．必要に応じて以下の文章を参照しながら指示に従ってください．\n\n###文章###\n" + exampletexts},
            {"role": "user", "content": "###指示###\n以下の対話に自然に続く質問を2つ作成してください．フォーマットは番号つきリストとします．\n\n###対話###\n" + "\n".join(dialog)}
        ]
    )
    question = completion2.choices[0].message.content
    completion3 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは便利なアシスタントです．"},
            {"role": "user", "content": "###指示###\n以下の対話に自然に続く相槌を1文で作成してください．\n\n###対話###\n" + "\n".join(dialog)}
        ]
    )
    aizuchi = completion3.choices[0].message.content
