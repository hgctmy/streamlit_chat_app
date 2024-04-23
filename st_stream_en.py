# -*- coding: utf-8 -*-
import streamlit as st
from openai import OpenAI
import create_question_en
import control_difficulty
import database
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


st.session_state.setdefault('dialog', [])
st.session_state.setdefault('question', [])
st.session_state.setdefault('assistant1', [])
st.session_state.setdefault('exampletexts', '')
st.session_state.setdefault('kiji', 0)
st.session_state.setdefault('kijitext', '')
st.session_state.setdefault('kijistate', True)
st.session_state.setdefault('end', False)
st.session_state.setdefault('user', control_difficulty.User())
st.session_state.setdefault('user_input', "")
st.session_state.setdefault('openai_model', "gpt-4-turbo-2024-04-09")
st.session_state.setdefault('messages', [])
st.session_state.setdefault('worker', "")
st.session_state.setdefault('conn', None)


st.title("News commentary interactive interface 2")
st.markdown("The chatbot will explain the selected news in an interactive format. Select the questions you want to ask and let the dialogue proceed.")
kijilist = ["①Brightest-ever cosmic explosion solved but new mysteries sparked", "②上川外相、「ポスト岸田」へじわり　女性首相に期待、発信力課題", "③米専門家「金正恩委員長、戦争決めたようだ…朝鮮戦争直前以来最も危険」", "④日銀 大規模金融緩和策転換するかどうか見極めに 難しい判断も"]
kijisentaku = st.empty()

chat_placeholder = st.empty()


def initfn():
    st.session_state.conn = database.create_connection("gpt.db")
    database.init_db(st.session_state.conn)
    with kijisentaku.container():
        st.session_state.kijitext = st.radio("Please select the specified article", (kijilist))
        st.session_state.kiji = kijilist.index(st.session_state.kijitext)
        st.session_state.worker = st.text_input("Enter the worker name and press enter.", key="workername")
        if st.button("I selected an article, typed in the worker name and pressed enter.", key='first'):
            # 説明してもらう文章
            exampletexts1 = "Researchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard."
            exampletexts2 = "【ワシントン時事】支持率低迷に苦しむ岸田内閣で、昨年９月に就任した上川陽子外相の評価が徐々に高まっている。精力的な外国訪問を通じて存在感をアピール。「ポスト岸田」候補の一人に浮上した。与党内では、初の女性首相への期待も出始めている。\n\n　上川氏は１２日（日本時間１３日）、米ワシントンでブリンケン国務長官と会談。会談後、上川氏は記者団に対し「法の支配に基づく自由で開かれた国際秩序を維持・強化するため、日米が連携することで一致した」と説明した。\n　これに先立ち、ロシアとの戦闘が続くウクライナを訪問。クレバ外相との会談は空襲警報下で行われたが、上川氏は「慌てる様子もなく、毅然（きぜん）としていた」（外務省幹部）という。\n　昨年１２月の時事通信の世論調査で、首相にふさわしい自民党の国会議員を尋ねたところ、上川氏は３．１％で６位に入った。石破茂元幹事長ら「常連組」にこそ及ばなかったが、現職の岸田文雄首相の１．６％を上回った。\n　上川氏は衆院当選７回で、岸田派所属の７０歳。法相を３回務めるなど実務能力の高さに定評はあったが、外相に就任するまで首相候補と目されることはなかった。\n　自民党派閥の政治資金規正法違反事件で、世論の「政治とカネ」の問題に対する視線は厳しい。公明党関係者は「上川氏なら清廉潔白な感じがある。女性首相は選挙の顔にもなる」と期待。自民党閣僚経験者も「派手さはないが、能力は高い」と評価する。\n　ただ、上川氏は記者会見や国会審議で、官僚の用意した答弁を読み上げることが多い。当意即妙なやりとりは苦手とされ、情報発信が課題となりそうだ。自民党関係者は「上川氏がどういう主張なのか全く知らない。首相を目指すなら幅広い政策発信が必要だ」と注文を付けた。"
            exampletexts3 = "「韓米、勝利しても意味ない」\n　北朝鮮が南北関係に対して荒々しい言葉を次々と並べている中、金正恩（キム・ジョンウン）国務委員長が戦争を決心したものとみられると、米国専門家らが主張した。\n\n　北朝鮮問題の権威者であるミドルベリー国際問題研究所のロバート・カーリン研究員とジークフリード・ヘッカー博士は11日、北朝鮮専門メディア「38ノース」への共同寄稿で、「朝鮮半島の状況は1950年6月初め以来、最も危険だ」とし、現在が朝鮮戦争直前の状況に近いと述べた。\n\n　カーリン研究員とヘッカー博士は「あまりにも衝撃的に聞こえるかもしれない」としつつも、「私たちは、彼の祖父が1950年にそうしたように、金正恩が戦争をするという戦略的決断を下したとみている」と明らかにした。さらに「金正恩がいつ、どのように引き金を引くか分からない」としながらも、戦争の危険性は、米国と韓国などが日常的に行ってきた警告をはるかに越えるレベルだと診断した。\n\n　彼らは、北朝鮮政権がこの30年間追求してきた米国との関係正常化に対する期待を捨て、昨年初めから武力使用について直接言及し始めたことを、このような判断の根拠に挙げた。\n\n　北朝鮮は金日成（キム・イルソン）主席以来、3代にわたり最高指導者が中国とロシアに対する緩衝手段として米国との関係正常化を進め、1994年にジュネーブ合意を成功させ、合意破棄後もその目標を捨てなかったが、2018年と2019年に当時のドナルド・トランプ大統領と金委員長の首脳会談が物別れに終わった後、これまでの路線を捨てたということだ。また、金委員長は、祖父と父親が果たせなかった目標を、威信をかけて推進し、史上初の朝米首脳会談にまで漕ぎつけたが、米国に大きく無視されたと指摘した。\n\n　彼らは、朝米関係正常化に向けた努力が失敗に終わった責任が誰にあるのかではなく、「北朝鮮がそのような目標を完全に放棄したことで、朝鮮半島をめぐる戦略的状況がどれほど大きく変わったのか」が極めて重要だと述べた。\n\n　さらに、北朝鮮が中国とロシア側へと「戦略的な方向転換」を決めたのは、米国が国際舞台で衰退しているという判断を働いたと分析した。中国との関係改善には大きな進展は見られないが、ロシアとは昨年の朝ロ首脳会談を機にした軍事分野の協力などが成果として現れているとみた。このようなことから、北朝鮮は世界情勢が自分たちに有利に進んでいると判断し、「韓国問題に対する軍事的解決策」に傾くようになったというのが彼らの説明だ。\n\n二人の専門家はこのような状況の中で、北朝鮮高官たちが2023年初めから戦争準備について発言するようになったと指摘した。金委員長が昨年8月に「祖国統一を成し遂げるための革命戦争準備」を語り、先月には南北関係を「敵対的な二国間関係」と表現したのがその例だ。彼らは、北朝鮮メディアに登場する「戦争準備」というテーマは、従来の虚勢とは思えないと述べた。\n\n　彼らは、北朝鮮政権が戦争を開始すれば、韓国と米国が自分たちを完全に破壊できるのに、果たして危険を冒すだろうかという反論もあり得るとした。だが、北朝鮮政権は他の選択肢がもう使えないと判断しているとみられるとし、「歴史は、他に良い選択肢がないと確信した人々が、最も危険なゲームを試みても良いかもしれないという考えを抱く場合もあることを示している」と述べた。\n\n　また韓米は、「徹底した抑制力」を強調するなど、金委員長が現状を破壊できないようにしながら、北朝鮮政権の完全な破壊を公言しているが、そのような考えは致命的な結果をもたらすかもしれないと述べた。彼らは、北朝鮮は韓国全域と事実上日本とグアムの両方を打撃できる核弾頭50～60基を保有しているとし、戦争が勃発すれば「韓米が勝利しても、その結果は意味のないものであろう」とし、「荒廃した焼野原が見渡す限りずっと広がるだろう」と警告した。"
            exampletexts4 = "日銀はことし、長期にわたって続けてきた大規模な金融緩和策を転換するかどうかの見極めに入ります。賃金の上昇を伴った2％の物価安定目標が達成できるという見通しが立つことが政策転換の前提となりますが、国内外の経済をめぐる不確実性が依然高い中で日銀は難しい判断を迫られることになります。\n\n日銀の植田総裁は先月26日、NHKのインタビューで今後の政策判断のポイントとしてことしの春闘での賃上げの動向とこれまでの賃金上昇の物価への波及という2点をあげたうえで、春闘での賃上げの水準については去年（2023年）と同じかそれを少し上回る水準が望ましいとの考えを示しました。\n\nことしの春闘で大手企業の賃上げの状況は3月の集中回答日までにおおむね出そろいますが、中小企業の賃上げの動向が把握できるのはさらに先になります。\n\nこのため、日銀がどのタイミングで企業全体の賃上げの状況を見極めて政策を判断するのかに市場の関心が集まっていました。\n\nこれについて植田総裁はNHKのインタビューに対し、「完全に中小企業の賃金データが出たり決定がなされたりしていなくても他の中小企業の指標で、例えば収益が好調である。あるいはそのバックにある消費や投資が好調でこれがうまく好循環を生み出すということがあればある程度、前もっての判断ができるかと思う」と述べ、中小企業の賃上げの結果が出そろわなくても関連するデータを踏まえて前もって判断することは可能だという考えを示しました。\n\n日銀がことし金融緩和策を転換し、マイナス金利政策を解除すればおよそ17年ぶりの利上げとなりますが、能登半島地震の経済への影響やアメリカの金融政策の方向性など国内外の経済をめぐる不確実性が依然高い中、日銀は難しい判断を迫られることになります。"
            texts = [exampletexts1, exampletexts2, exampletexts3, exampletexts4]
            st.session_state.exampletexts = texts[st.session_state.kiji]
            # 導入文
            st.session_state.assistant1 = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\nResearchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard."
                },
                {
                    "role": "user",
                    "content": "Briefly describe the introduction to the news article in two sentence."
                }
            ]
            kijisentaku.markdown(st.session_state.kijitext)
            with chat_placeholder.container():
                with st.chat_message("assistant"):
                    a1message = database.fetch_response(st.session_state.conn, st.session_state.assistant1)
                    if a1message:
                        st.write(a1message)
                    else:
                        stream = client.chat.completions.create(
                            model=st.session_state["openai_model"],
                            messages=st.session_state.assistant1,
                            stream=True,
                            temperature=0
                        )
                        a1message = st.write_stream(stream)
                        database.insert_chat_pair(st.session_state.conn, st.session_state.assistant1, a1message)
                st.session_state.messages.append({"role": "assistant", "content": a1message})
                st.session_state.dialog.append("**commentator:** " + a1message)
                # 初めの質問候補を生成
                st.session_state.question = create_question_en.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, 1.5)
                st.session_state.kijistate = False


def notinitfn():
    kijisentaku.markdown(st.session_state.kijitext)


if st.session_state.kijistate:
    initfn()
else:
    notinitfn()

button_placeholder = st.empty()

with chat_placeholder.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def click(i):
    with chat_placeholder.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.session_state.messages.append({"role": "user", "content": choices[i]})
        st.session_state.dialog.append("**questioner:** " + choices[i])
        st.session_state.user.add_scores(st.session_state.question[i].score)
        user_score = st.session_state.user.calc_average()
        with st.chat_message("user"):
            st.markdown(choices[i])
        with st.chat_message("assistant"):
            message = [
                {
                    "role": "system",
                    "content": "==instruction==\nGiven a news the history of the dialogue between the commentator and the questioner about the content of the news article as input, please create a two-sentence statement by the commentator following the dialogue. The content should be an answer to the question and additional information that introduces the next topic.\n\n==Input example==\n##news article##\nResearchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard.\n\n##dialogue about news article content##\n**commentator:** Artificial intelligence is now playing a crucial role in managing and preventing power outages as demand for electricity surges globally.\n\n**questioner:** What role is AI playing in the management of electricity grids according?\n\n**commentator:**  AI is being used to predict electricity supply and demand, helping to optimize when batteries should charge and discharge. Additionally, AI helps in detecting infrastructural damage and potential hazards like animal intrusions that could lead to power outages.\n\n**questioner:** Can you elaborate on how AI predicts electricity supply and demand specifically and how this information helps manage battery storage systems?\n\n==Output example==\nAI utilizes advanced algorithms and machine learning to analyze historical data and real-time inputs from various sources, such as weather patterns, consumer behavior, and energy production rates. This predictive capability allows grid operators to anticipate periods of high demand or low supply, strategically managing battery storage to either store excess energy during low demand or release energy during peak times, thus maintaining grid stability and efficiency."
                },
                {
                    "role": "user",
                    "content": "==Input==\n##news article##\n" + st.session_state.exampletexts + "\n\n##dialogue about news article content##\n" + "\n".join(st.session_state.dialog) + "\n\n==Output=="
                }
            ]
            answer = database.fetch_response(st.session_state.conn, message)
            if answer:
                st.write(answer)
            else:
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=message,
                    stream=True,
                    temperature=0
                )
                answer = st.write_stream(stream)
                database.insert_chat_pair(st.session_state.conn, message, answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.dialog.append("**commentator:** " + answer)
        if len(st.session_state.messages) > 5:
            st.session_state.end = 1
        # 質問生成
        st.session_state.question = create_question_en.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, user_score)


def on_change():
    with chat_placeholder.container():
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        user_input = st.session_state.user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.dialog.append("**questioner:** " + user_input)
        if len(st.session_state.user.scores) > 0:
            user_score = st.session_state.user.calc_average()
        else:
            user_score = 2
        user_score = st.session_state.user.calc_average()
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            message = [
                {
                    "role": "system",
                    "content": "==instruction==\nGiven a news the history of the dialogue between the commentator and the questioner about the content of the news article as input, please create a two-sentence statement by the commentator following the dialogue. The content should be an answer to the question and additional information that introduces the next topic.\n\n==Input example==\n##news article##\nResearchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard.\n\n##dialogue about news article content##\n**commentator:** Artificial intelligence is now playing a crucial role in managing and preventing power outages as demand for electricity surges globally.\n\n**questioner:** What role is AI playing in the management of electricity grids according?\n\n**commentator:**  AI is being used to predict electricity supply and demand, helping to optimize when batteries should charge and discharge. Additionally, AI helps in detecting infrastructural damage and potential hazards like animal intrusions that could lead to power outages.\n\n**questioner:** Can you elaborate on how AI predicts electricity supply and demand specifically and how this information helps manage battery storage systems?\n\n==Output example==\nAI utilizes advanced algorithms and machine learning to analyze historical data and real-time inputs from various sources, such as weather patterns, consumer behavior, and energy production rates. This predictive capability allows grid operators to anticipate periods of high demand or low supply, strategically managing battery storage to either store excess energy during low demand or release energy during peak times, thus maintaining grid stability and efficiency."
                },
                {
                    "role": "user",
                    "content": "==Input==\n##news article##\n" + st.session_state.exampletexts + "\n\n##dialogue about news article content##\n" + "\n".join(st.session_state.dialog) + "\n\n==Output=="
                }
            ]
            answer = database.fetch_response(st.session_state.conn, message)
            if answer:
                st.write(answer)
            else:
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=message,
                    stream=True,
                    temperature=0
                )
                answer = st.write_stream(stream)
                database.insert_chat_pair(st.session_state.conn, message, answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.dialog.append("**commentator:** " + answer)
        if len(st.session_state.messages) > 5:
            st.session_state.end = 1
        # 質問生成
        st.session_state.question = create_question_en.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, user_score)
        st.session_state.user_input = ""


if len(st.session_state.question) > 2:
    choices = [st.session_state.question[i].text for i in range(3)]
    with button_placeholder.container():
        st.button(choices[0], key='b1', on_click=lambda: click(0))
        st.button(choices[1], key='b2', on_click=lambda: click(1))
        st.button(choices[2], key='b3', on_click=lambda: click(2))
        st.text_input("If you don't see the question you want to ask, please enter it manually here.", on_change=lambda: on_change(), key="user_input")

end_placeholder = st.empty()


def end_fn():
    with end_placeholder.container():
        if not st.button("Exit", on_click=lambda: finish(), key='reload'):
            st.stop()


def finish():
    st.session_state.dialog = []
    st.session_state.question = []
    st.session_state.assistant1 = []
    st.session_state.exampletexts = ''
    st.session_state.kiji = 0
    st.session_state.kijitext = ''
    st.session_state.kijistate = True
    st.session_state.end = False
    st.session_state.user_input = ""
    st.session_state.user = control_difficulty.User()
    st.session_state.openai_model = "gpt-4-turbo-2024-04-09"
    st.session_state.messages = []
    st.session_state.worker = ""


if st.session_state.end is True:
    end_fn()
