# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_chat import message
from openai import OpenAI
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
import create_question
import control_difficulty
import gspread
from google.oauth2.service_account import Credentials


scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file("crafty-student-389707-527f851a906a.json", scopes=scope)
gc = gspread.authorize(credentials)


load_dotenv(join(dirname(__file__), '.env'))

client = OpenAI(
    api_key=os.environ.get("API_KEY"),
)

st.session_state.setdefault('past', ['start'])
st.session_state.setdefault('generated', [])
st.session_state.setdefault('dialog', [])
st.session_state.setdefault('question', [])
st.session_state.setdefault('answers', [])
st.session_state.setdefault('aizuchi', '')
st.session_state.setdefault('assistant1', [])
st.session_state.setdefault('exampletexts', '')
st.session_state.setdefault('kiji', 0)
st.session_state.setdefault('kijitext', '')
st.session_state.setdefault('kijistate', True)
st.session_state.setdefault('end', False)
st.session_state.setdefault('user', control_difficulty.User())
st.session_state.setdefault('user_input', "")
st.session_state.setdefault('worker', "")
st.session_state.setdefault('workbook', None)

st.title("ニュース解説対話インタフェース")
st.markdown("選んだニュースをチャットボットが対話形式で解説してくれます．提示される質問や反応を選んで対話を進めましょう！")
kijilist = ["米中首脳会談", "電通大で「情報I」の問題体験会", "生成AI活用の「ブラック・ジャック」新作完成、仲介AIつくりプロンプトを成形"]
kijisentaku = st.empty()


def first():
    # ログ用スプレッドシート作成
    st.session_state.workbook = gc.create("propose_" + st.session_state.worker)
    ws = st.session_state.workbook.get_worksheet(0)
    ws.append_row(["選ばれた記事", st.session_state.kiji])
    ws.append_row(["現在のユーザの理解度", "質問候補1", "難易度", "質問候補2", "難易度", "質問候補3", "難易度", "選ばれた質問", "難易度"])
    # 説明してもらう文章
    exampletexts1 = "バイデン米大統領は１５日（日本時間１６日）、サンフランシスコ近郊で中国の習近平国家主席と会談した。両首脳は、米中間の誤解や判断ミスによる軍事衝突など不測の事態を回避するため、国防相間を含む軍部同士での対話再開で合意。台湾問題を巡っては、バイデン氏が力による現状変更を行わないよう訴え、習氏は米国による台湾への軍事支援を中止するよう求めた。首脳間の電話による対話チャンネルの開設でも一致した。会談は昨年１１月にインドネシアで行われて以来以来１年ぶり。サンフランシスコ近郊の庭園で行われ、両者の会談は昼食や敷地内の散歩を含めて４時間に上った。バイデン氏は終了後の記者会見で「会談は建設的かつ生産的」で「重要な進展をなした」と強調した。会談冒頭、バイデン氏は、激化する競争や対立をめぐり「首脳同士が誤解せず理解し合うことが最重要だ」としたうえで「競争が紛争に向かわないようにする必要がある」とし、互いの判断ミスが軍事衝突に発展するリスクを回避するため対話の重要性を強調した。習氏も「米中は世界最重要の二国間関係」としたうえで「大国が背を向け合うことは選択肢ではない」「紛争や対立は両国に耐えられない結果をもたらす」と強調した。軍部同士の対話は昨夏のペロシ下院議長（当時）台湾訪問を契機に中国側が中断。米政府高官によると、両首脳は国防相間で、政策対話や軍高官による作戦レベルの対話などを行うことで合意した。会談では、バイデン氏が南シナ海などで中国による米軍機や艦船への妨害行為が増加していることに懸念を表明。米国の「一つの中国」政策と台湾海峡の現状維持の重要性を強調した。中国国営新華社通信によると、習氏は台湾問題について「中米関係の中で最も重要で敏感な問題だ」とした上で「米側は『台湾独立』を支持しない態度を具体的な行動で体現し、台湾を武装させるのをやめ、中国の平和統一を支持すべきだ」とクギを刺した。両首脳は、人工知能（ＡＩ）に関する対話開始や米中間の旅客便の大幅増に取り組むことで合意。米国で、中国が原料を輸出する医療用麻薬フェンタニル乱用が社会問題となっていることを踏まえ、薬物対策で作業部会を設けることでも一致した。"
    exampletexts2 = "再来年１月の大学入学共通テストから「情報Ｉ」が加わるのを前に、個別入試でも導入を予定している国立の電気通信大学で、「情報Ｉ」の試作問題の体験会が開かれました。東京・調布市にある国立の電気通信大学は、再来年１月から大学入学共通テストの出題科目に加わる「情報Ｉ」を、個別入試の選択科目でも導入する予定で、２６日は、オープンキャンパスに参加した高校２年生およそ８０人が本番さながらの環境で試作問題を体験しました。この中では、インターネット上の情報を取得できる仕組みを体系的に整理して解答する問題や、穴あきになったプログラムを関数などを選択して完成させる問題も出されました。大学では「情報Ｉ」の配点を共通テストでは全体の１割にあたる５０点、個別入試で選択すれば、２割にあたる１００点とする予定で、福岡県から参加した生徒は「情報の問題の傾向がわかってよかったです。第一志望なので絶対合格できるよう頑張りたい」と話していました。また２６日は、一部の入試で導入予定の、パソコンなどの端末で受験するシステムの体験も行われていました。電気通信大学の成見哲副学長は「プログラミングの力に加え数学的、論理的な思考力を問う内容にしました。情報技術は入学後も役立つのでデータ処理などの経験を積んでほしい」と話していました。"
    exampletexts3 = "「TEZUKA2023」プロジェクトチームは2023年11月20日、クリエーターが生成AI（人工知能）を活用して制作した漫画「ブラック・ジャック」の新作「TEZUKA2023 ブラック・ジャック 機械の心臓―Heartbeat MarkⅡ」が完成したと発表した。　クリエーターと生成AIの仲介役として、生成AIへのプロンプト（指示文）をユーザーのレベルに依存せずに成形できる「インタラクティブプロンプトAI（仲介AI）」を開発して使用した。新作は11月22日発売の秋田書店「週刊少年チャンピオン 52号」に掲載される。　プロットの生成には、米OpenAI（オープンAI）が提供する大規模言語モデル「GPT-4」とプロット生成用の仲介AIを用いた。仲介AIには過去のブラック・ジャックの作品構造を人の手で分析したデータなどを活用した。クリエーターはAIと何度もやり取りしながらプロットをつくり上げた。プロットだけでなく、シナリオやト書きも同様にAIが生成したが、最終シナリオはそれらを参考に人が制作した。　キャラクター画像の生成には画像生成用の仲介AIと、英Stability AI（スタビリティーAI）が開発した画像生成AIモデル「Stable Diffusion（ステーブルディフュージョン）」を活用した。同生成AIは手塚キャラクター2万枚の顔画像データで追加学習した。生成した複数の画像から人が起用する画像を決定し、その画像を基に人がキャラクターデザインを担当した。　一部では漫画のコマごと生成する試みも行った。こちらもStable Diffusionを活用し、過去のブラック・ジャック4000ページ分のコマデータを追加学習させた。人がAIに漫画のコマ素材を生成するよう指示し、生成されたコマのアングルなどを参考にして作画に反映した。　プロジェクトチームのメンバーには手塚プロダクションの手塚眞取締役と石渡正人氏、日高海氏のほか、慶応義塾大学理工学部の栗原聡教授と橋本敦史特任講師、はこだて未来大学システム情報科学部の村井源教授、電気通信大学人工知能先端研究センターの稲葉通将准教授などが名を連ねた。　プロットやシナリオの制作を担当した映画監督の林海象氏は「ブラック・ジャックは人体が機械であっても治せるのか、治すことを拒否するのかなどの質問をAIにした。『例えば心臓がアンドロイドのようで』などとやり取りした。すると、AIが『機械の心臓』というタイトルを決めた。その心臓の名前は何かと尋ねると、生成AIが『Heartbeat MarkⅡ』と回答した。最初に人間が考えたアイデアとAIが出した回答、まさに人間とAIが合体してつくるような感じで進んだ」と話す。　林氏は「AIは返答が早いから、プロットがすぐできる。会話をしていた感じだ。だんだんAIに感情がわいてきたような気がする。こちらの聞き方がまずいと、子どもみたいに答えなかったり違う答えを出したりする。非常に楽しかった」と振り返った。"

    texts = [exampletexts1, exampletexts2, exampletexts3]
    st.session_state.exampletexts = texts[st.session_state.kiji]
    # 導入文
    st.session_state.assistant1 = [
        {"role": "system", "content": "あなたは便利なアシスタントです．必要に応じて以下の文章を参照して簡潔に答えてください．\n\n###文章###\n" + st.session_state.exampletexts},
        {"role": "user", "content": "まずは文章の導入部分を1文で簡単に述べてください．"}
    ]
    completion1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.assistant1
    )
    a1message = completion1.choices[0].message.content

    st.session_state.dialog.append("解説者：" + a1message)

    # 初めの質問候補を生成
    '''
    with open('prompt_qg.txt') as f:
        qgprompt = f.read()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": qgprompt
            },
            {
                "role": "user",
                "content": "==入力==\n##ニュース記事##\n" + st.session_state.exampletexts + "\n\n##対話履歴##\n" + "\n".join(st.session_state.dialog) + "\n\n==出力=="
            }
        ],
        temperature=0
    )
    question = re.findall(r"質問：(.*)", response.choices[0].message.content)
    st.session_state.question = [create_question.Question(question, i + 1) for i, question in enumerate(question)]
    '''
    st.session_state.question = create_question.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, 1.5)
    st.session_state.generated.append(a1message)


def initfn():
    with kijisentaku.container():
        st.session_state.kijitext = st.radio("選んでください", (kijilist))
        st.session_state.kiji = kijilist.index(st.session_state.kijitext)
        st.session_state.worker = st.text_input("ワーカ名を入力し，エンターキーを押してください。", key="workername")
        if not st.button("ワーカ名を入力し，記事を選択しました．", on_click=lambda: first(), key='first'):
            st.stop()
    st.session_state.kijistate = False


def notinitfn():
    kijisentaku.markdown(st.session_state.kijitext)


if st.session_state.kijistate:
    initfn()
else:
    notinitfn()


# 質問が選ばれたら実行する関数
def click1(i):
    st.session_state.user.add_scores(st.session_state.question[i].score)
    user_score = st.session_state.user.calc_average()
    # ログに追加
    ws = st.session_state.workbook.get_worksheet(0)
    ws.append_row([user_score, st.session_state.question[0].text, st.session_state.question[0].score, st.session_state.question[1].text, st.session_state.question[1].score, st.session_state.question[1].text, st.session_state.question[2].score, st.session_state.question[i].text, st.session_state.question[i].score])

    choice = {"role": "user", "content": st.session_state.question[i].text}  # 質問候補文
    st.session_state.assistant1.append(choice)
    st.session_state.dialog.append("質問者：" + choice["content"])
    # 回答生成
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.assistant1
    )
    # 追加情報
    with open('prompt_add.txt') as f:
        addprompt = f.read()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": addprompt
            },
            {
                "role": "user",
                "content": "==入力==\n##ニュース記事##\n" + st.session_state.exampletexts + "\n\n##対話履歴##\n" + "\n".join(st.session_state.dialog) + "\n\n==出力=="
            }
        ],
        temperature=0
    )
    st.session_state.dialog.append("解説者：" + completion.choices[0].message.content + response.choices[0].message.content[4:])
    st.session_state.generated.append(completion.choices[0].message.content + response.choices[0].message.content[4:])
    st.session_state.past.append(st.session_state.question[i].text)
    if len(st.session_state.past) > 3:
        st.session_state.end = 1
    # 質問生成
    st.session_state.question = create_question.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, user_score)


# 手入力質問されたとき
def on_change():
    if len(st.session_state.user.scores) > 0:
        user_score = st.session_state.user.calc_average()
    else:
        user_score = 2
        # ログに追加
    ws = st.session_state.workbook.get_worksheet(0)
    ws.append_row(["-", "-", "-", "-", "-", "-", "-", st.session_state.user_input, "-"])
    user_input = st.session_state.user_input
    choice = {"role": "user", "content": user_input}  # 質問
    st.session_state.assistant1.append(choice)
    st.session_state.dialog.append("質問者：" + choice["content"])
    # 回答生成
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.assistant1
    )
    # 追加情報
    with open('prompt_add.txt') as f:
        addprompt = f.read()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": addprompt
            },
            {
                "role": "user",
                "content": "==入力==\n##ニュース記事##\n" + st.session_state.exampletexts + "\n\n##対話履歴##\n" + "\n".join(st.session_state.dialog) + "\n\n==出力=="
            }
        ],
        temperature=0
    )
    st.session_state.dialog.append("解説者：" + completion.choices[0].message.content + response.choices[0].message.content[4:])
    st.session_state.generated.append(completion.choices[0].message.content + response.choices[0].message.content[4:])
    st.session_state.past.append(st.session_state.question[i].text)
    if len(st.session_state.past) > 4:
        st.session_state.end = 1
    # 質問生成
    st.session_state.question = create_question.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, user_score)
    st.session_state.user_input = ""


chat_placeholder = st.empty()
chat_initial = st.empty()
with chat_placeholder.container():
    for i in range(len(st.session_state.generated)):
        message(st.session_state.past[i], is_user=True, key=f"{i}_user")
        message(st.session_state.generated[i], key=f"{i}")


button_placeholder = st.empty()


if st.session_state.aizuchi:
    choices = [st.session_state.question[0], st.session_state.question[1], st.session_state.aizuchi]
else:
    choices = [st.session_state.question[i].text for i in range(3)]
with button_placeholder.container():
    st.button(choices[0], key='b1', on_click=lambda: click1(0))
    st.button(choices[1], key='b2', on_click=lambda: click1(1))
    st.button(choices[2], key='b3', on_click=lambda: click1(2))
    st.text_input('したい質問が候補になければこちらから手入力してください', on_change=lambda: on_change(), key="user_input")

end_placeholder = st.empty()


def end_fn():
    with end_placeholder.container():
        if not st.button("終了します", on_click=lambda: finish(), key='reload'):
            st.stop()


def finish():
    ws = st.session_state.workbook.add_worksheet('対話履歴', rows=100, cols=26)
    ws.append_rows(st.session_state.dialog)
    st.session_state.workbook.share('hgctomo@gmail.com', perm_type='user', role='writer')
    st.session_state.past = ['start']
    st.session_state.generated = []
    st.session_state.dialog = []
    st.session_state.question = []
    st.session_state.answers = []
    st.session_state.aizuchi = ''
    st.session_state.assistant1 = []
    st.session_state.exampletexts = ''
    st.session_state.kiji = 0
    st.session_state.kijitext = ''
    st.session_state.kijistate = True
    st.session_state.end = False
    st.session_state.user = control_difficulty.User()
    st.session_state.user_input = ""


if st.session_state.end == True:
    end_fn()
