# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
from streamlit_chat import message
import re
import create_question
import control_difficulty
import gspread
from google.oauth2.service_account import Credentials
import json

service_account_key = json.loads(st.secrets.GoogleKey.json_key)
credentials = Credentials.from_service_account_info(service_account_key)
scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(scoped_credentials)


client = OpenAI(
    api_key=st.secrets.OpenAIAPI.openai_api_key,
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

st.title("ニュース解説対話型インタフェース2")
st.markdown("選んだニュースをチャットボットが対話形式で解説してくれます．提示される質問を選んで対話を進めてください．")
kijilist = ["「衝撃的な解像度、科学者の仕事増えた」クリズム衛星、初画像を公開", "上川外相、「ポスト岸田」へじわり　女性首相に期待、発信力課題", "米専門家「金正恩委員長、戦争決めたようだ…朝鮮戦争直前以来最も危険」", "日銀 大規模金融緩和策転換するかどうか見極めに 難しい判断も"]
kijisentaku = st.empty()


def first():
    # ログ用スプレッドシート作成
    st.session_state.workbook = gc.create("propose_" + st.session_state.worker)
    ws = st.session_state.workbook.get_worksheet(0)
    ws.append_row(["選ばれた記事", st.session_state.kiji])
    ws.append_row(["現在のユーザの理解度", "質問候補1", "難易度", "質問候補2", "難易度", "質問候補3", "難易度", "選ばれた質問", "難易度"])
    # 説明してもらう文章
    exampletexts1 = "昨年9月に打ち上げられた、日米などのエックス線天文衛星「クリズム」が初めて撮影した画像が5日公開された。銀河集団同士の衝突の全体像や、星が爆発した痕跡のガスが含む元素を精細に捉えた。宇宙航空研究開発機構（JAXA）の担当者は会見で「衝撃的な高解像度。桁違いに多い情報が得られ、科学者の仕事が増えてワクワクする」と話した。\n\n\n　天文衛星（宇宙望遠鏡）は地上の望遠鏡と違い大気の影響を受けないため、高精度に観測できる。エックス線は可視光より短い電磁波の一つで、高いエネルギーで熱く激動する天体や現象を捉えるのを得意とする。日本は1979年に打ち上げた「はくちょう」以来、エックス線衛星6基の運用経験を持つ。7基目のクリズムは宇宙空間を吹く高温ガス「プラズマ」の成分や動きを測ることを通じ、100個程度以上の銀河の集団「銀河団」の成り立ちや、さまざまな元素の誕生などの解明につなげるという。\n\n　クリズムは米国が開発した2つの望遠鏡にそれぞれ、広い視野を持つ国産のエックス線CCDカメラ「エクステンド」と、エックス線のエネルギーを詳しく測る日米欧共同開発の分光装置「リゾルブ」を取り付けている。高度約550キロを周回して観測する。\n\n　この日公開されたのは、昨年10月14～24日にエクステンドで撮影した約7億7000万光年の距離にある銀河団「エイベル2319」の画像と、先月4～11日にリゾルブが捉えた、約16万3000光年離れた大マゼラン星雲の超新星残骸「N132D」のガスが含む、元素の種類や量のデータ。超新星残骸とは、星が一生の終わりに爆発した痕跡をいう。\n\n　エクステンドは従来機のカメラの4倍にも及ぶ広視野を強みとし、衝突しつつある銀河団の全体像を捕捉。銀河団が持つプラズマの分布も明瞭に表現した。リゾルブも、2015年まで運用した衛星「すざく」が搭載した装置の30倍の高精度で、ケイ素や硫黄、アルゴンといったさまざまな元素の量や状態を細かく示すことに成功した。\n\n\n　クリズムチームはJAXA宇宙科学研究所（相模原市中央区）で会見。科学研究主宰者の田代信プリンシパルインベスティゲータは「すざくの開発にも携わったが、リゾルブは同じ物を見たとは思えないほどの高解像度で、何度見ても衝撃的。エクステンドの視野は狙った天体以外も捉えるほど広く、何が見えてくるのか非常に楽しみだ」と期待を高めた。\n\n　クリズムは、2016年に運用ミスで失ったエックス線衛星「ひとみ」の代替機として、約277億円（日本負担分。100億円規模とみられる打ち上げ費用を含む）をかけ開発された。月面着陸機「スリム」と共に大型ロケット「H2A」に搭載され、昨年9月7日に打ち上げられた。来月には初期機能確認から定常運用に移行し、科学観測を本格化する。ただリゾルブの保護膜の開放にはまだ成功しておらず、今後、再挑戦する。チームは「仮に膜が覆ったままでも影響は限定的。画期的な成果が期待できる」とみている。\n\n　前島弘則プロジェクトマネージャは、ひとみの事故を受けた改善策を説明。「（失敗を）決して繰り返さない決意をし、システム作りを着実にしており、これまではうまく運用できている。定常運用でもその仕組みでやれば寿命を全うし、良い成果を出せる」と、今後に向け気を引き締めた。\n\n　一方、スリムも順調に航行し先月25日、月上空の周回軌道への投入に成功した。今月20日未明、日本初となる月面軟着陸に挑戦する。\n\n"
    exampletexts2 = "【ワシントン時事】支持率低迷に苦しむ岸田内閣で、昨年９月に就任した上川陽子外相の評価が徐々に高まっている。精力的な外国訪問を通じて存在感をアピール。「ポスト岸田」候補の一人に浮上した。与党内では、初の女性首相への期待も出始めている。\n\n　上川氏は１２日（日本時間１３日）、米ワシントンでブリンケン国務長官と会談。会談後、上川氏は記者団に対し「法の支配に基づく自由で開かれた国際秩序を維持・強化するため、日米が連携することで一致した」と説明した。\n　これに先立ち、ロシアとの戦闘が続くウクライナを訪問。クレバ外相との会談は空襲警報下で行われたが、上川氏は「慌てる様子もなく、毅然（きぜん）としていた」（外務省幹部）という。\n　昨年１２月の時事通信の世論調査で、首相にふさわしい自民党の国会議員を尋ねたところ、上川氏は３．１％で６位に入った。石破茂元幹事長ら「常連組」にこそ及ばなかったが、現職の岸田文雄首相の１．６％を上回った。\n　上川氏は衆院当選７回で、岸田派所属の７０歳。法相を３回務めるなど実務能力の高さに定評はあったが、外相に就任するまで首相候補と目されることはなかった。\n　自民党派閥の政治資金規正法違反事件で、世論の「政治とカネ」の問題に対する視線は厳しい。公明党関係者は「上川氏なら清廉潔白な感じがある。女性首相は選挙の顔にもなる」と期待。自民党閣僚経験者も「派手さはないが、能力は高い」と評価する。\n　ただ、上川氏は記者会見や国会審議で、官僚の用意した答弁を読み上げることが多い。当意即妙なやりとりは苦手とされ、情報発信が課題となりそうだ。自民党関係者は「上川氏がどういう主張なのか全く知らない。首相を目指すなら幅広い政策発信が必要だ」と注文を付けた。"
    exampletexts3 = "「韓米、勝利しても意味ない」\n　北朝鮮が南北関係に対して荒々しい言葉を次々と並べている中、金正恩（キム・ジョンウン）国務委員長が戦争を決心したものとみられると、米国専門家らが主張した。\n\n　北朝鮮問題の権威者であるミドルベリー国際問題研究所のロバート・カーリン研究員とジークフリード・ヘッカー博士は11日、北朝鮮専門メディア「38ノース」への共同寄稿で、「朝鮮半島の状況は1950年6月初め以来、最も危険だ」とし、現在が朝鮮戦争直前の状況に近いと述べた。\n\n　カーリン研究員とヘッカー博士は「あまりにも衝撃的に聞こえるかもしれない」としつつも、「私たちは、彼の祖父が1950年にそうしたように、金正恩が戦争をするという戦略的決断を下したとみている」と明らかにした。さらに「金正恩がいつ、どのように引き金を引くか分からない」としながらも、戦争の危険性は、米国と韓国などが日常的に行ってきた警告をはるかに越えるレベルだと診断した。\n\n　彼らは、北朝鮮政権がこの30年間追求してきた米国との関係正常化に対する期待を捨て、昨年初めから武力使用について直接言及し始めたことを、このような判断の根拠に挙げた。\n\n　北朝鮮は金日成（キム・イルソン）主席以来、3代にわたり最高指導者が中国とロシアに対する緩衝手段として米国との関係正常化を進め、1994年にジュネーブ合意を成功させ、合意破棄後もその目標を捨てなかったが、2018年と2019年に当時のドナルド・トランプ大統領と金委員長の首脳会談が物別れに終わった後、これまでの路線を捨てたということだ。また、金委員長は、祖父と父親が果たせなかった目標を、威信をかけて推進し、史上初の朝米首脳会談にまで漕ぎつけたが、米国に大きく無視されたと指摘した。\n\n　彼らは、朝米関係正常化に向けた努力が失敗に終わった責任が誰にあるのかではなく、「北朝鮮がそのような目標を完全に放棄したことで、朝鮮半島をめぐる戦略的状況がどれほど大きく変わったのか」が極めて重要だと述べた。\n\n　さらに、北朝鮮が中国とロシア側へと「戦略的な方向転換」を決めたのは、米国が国際舞台で衰退しているという判断を働いたと分析した。中国との関係改善には大きな進展は見られないが、ロシアとは昨年の朝ロ首脳会談を機にした軍事分野の協力などが成果として現れているとみた。このようなことから、北朝鮮は世界情勢が自分たちに有利に進んでいると判断し、「韓国問題に対する軍事的解決策」に傾くようになったというのが彼らの説明だ。\n\n二人の専門家はこのような状況の中で、北朝鮮高官たちが2023年初めから戦争準備について発言するようになったと指摘した。金委員長が昨年8月に「祖国統一を成し遂げるための革命戦争準備」を語り、先月には南北関係を「敵対的な二国間関係」と表現したのがその例だ。彼らは、北朝鮮メディアに登場する「戦争準備」というテーマは、従来の虚勢とは思えないと述べた。\n\n　彼らは、北朝鮮政権が戦争を開始すれば、韓国と米国が自分たちを完全に破壊できるのに、果たして危険を冒すだろうかという反論もあり得るとした。だが、北朝鮮政権は他の選択肢がもう使えないと判断しているとみられるとし、「歴史は、他に良い選択肢がないと確信した人々が、最も危険なゲームを試みても良いかもしれないという考えを抱く場合もあることを示している」と述べた。\n\n　また韓米は、「徹底した抑制力」を強調するなど、金委員長が現状を破壊できないようにしながら、北朝鮮政権の完全な破壊を公言しているが、そのような考えは致命的な結果をもたらすかもしれないと述べた。彼らは、北朝鮮は韓国全域と事実上日本とグアムの両方を打撃できる核弾頭50～60基を保有しているとし、戦争が勃発すれば「韓米が勝利しても、その結果は意味のないものであろう」とし、「荒廃した焼野原が見渡す限りずっと広がるだろう」と警告した。"
    exampletexts4 = "日銀はことし、長期にわたって続けてきた大規模な金融緩和策を転換するかどうかの見極めに入ります。賃金の上昇を伴った2％の物価安定目標が達成できるという見通しが立つことが政策転換の前提となりますが、国内外の経済をめぐる不確実性が依然高い中で日銀は難しい判断を迫られることになります。\n\n日銀の植田総裁は先月26日、NHKのインタビューで今後の政策判断のポイントとしてことしの春闘での賃上げの動向とこれまでの賃金上昇の物価への波及という2点をあげたうえで、春闘での賃上げの水準については去年（2023年）と同じかそれを少し上回る水準が望ましいとの考えを示しました。\n\nことしの春闘で大手企業の賃上げの状況は3月の集中回答日までにおおむね出そろいますが、中小企業の賃上げの動向が把握できるのはさらに先になります。\n\nこのため、日銀がどのタイミングで企業全体の賃上げの状況を見極めて政策を判断するのかに市場の関心が集まっていました。\n\nこれについて植田総裁はNHKのインタビューに対し、「完全に中小企業の賃金データが出たり決定がなされたりしていなくても他の中小企業の指標で、例えば収益が好調である。あるいはそのバックにある消費や投資が好調でこれがうまく好循環を生み出すということがあればある程度、前もっての判断ができるかと思う」と述べ、中小企業の賃上げの結果が出そろわなくても関連するデータを踏まえて前もって判断することは可能だという考えを示しました。\n\n日銀がことし金融緩和策を転換し、マイナス金利政策を解除すればおよそ17年ぶりの利上げとなりますが、能登半島地震の経済への影響やアメリカの金融政策の方向性など国内外の経済をめぐる不確実性が依然高い中、日銀は難しい判断を迫られることになります。"
    texts = [exampletexts1, exampletexts2, exampletexts3, exampletexts4]
    st.session_state.exampletexts = texts[st.session_state.kiji]
    # 導入文
    st.session_state.assistant1 = [
        {"role": "system", "content": "あなたは便利なアシスタントです．必要に応じて以下の文章を参照して簡潔に答えてください．\n\n###文章###\n" + st.session_state.exampletexts},
        {"role": "user", "content": "まずは文章の導入部分を1文で簡単に述べてください．"}
    ]
    completion1 = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.assistant1
    )
    a1message = completion1.choices[0].message.content

    st.session_state.dialog.append("解説者：" + a1message)

    # 初めの質問候補を生成
    st.session_state.question = create_question.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, 1.5)
    st.session_state.generated.append(a1message)


def initfn():
    with kijisentaku.container():
        st.session_state.kijitext = st.radio("指定された記事を選んでください", (kijilist))
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
    st.session_state.dialog.append("解説者：" + completion.choices[0].message.content + response.choices[0].message.content)
    st.session_state.generated.append(completion.choices[0].message.content + response.choices[0].message.content)
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
    st.session_state.dialog.append("解説者：" + completion.choices[0].message.content + response.choices[0].message.content)
    st.session_state.generated.append(completion.choices[0].message.content + response.choices[0].message.content)
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
    ws.append_row(st.session_state.dialog)
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
