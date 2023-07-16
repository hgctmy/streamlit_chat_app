# -*- coding: utf-8 -*-
import os
import streamlit as st
import openai
from os.path import join, dirname
from dotenv import load_dotenv
from streamlit_chat import message

load_dotenv(join(dirname(__file__), '.env'))
openai.api_key = os.environ.get("API_KEY")

st.session_state.setdefault('past', ['start'])
st.session_state.setdefault('generated', [])
st.session_state.setdefault('dialog', [])
st.session_state.setdefault('question', [])
st.session_state.setdefault('assistant1', [])
st.session_state.setdefault('exampletexts', '')
st.session_state.setdefault('kiji', 0)
st.session_state.setdefault('kijitext', '')
st.session_state.setdefault('kijistate', True)


st.title("ニュース解説チャットボット")
st.markdown("選んだニュースをチャットボットが対話形式で解説してくれます．提示される質問や反応を選んで対話を進めましょう！")
kijilist = ["祇園祭、ちまきの転売相次ぐ…地元困惑「何してはるんやろ」", "吉田正尚 30歳バースデーで連続マルチヒットは8試合でストップ、ストレートを試合中にアジャストできず", "JR秋田駅前、路上を一面水覆う「内水氾濫」や土砂崩れ", "鈴木拓「はっきり言いますけど大っ嫌い」と言う人物", "ＴＢＳ安住紳一郎アナ ryuchellさん報道での視聴者への配慮が話題「好かれてる理由わかった」「有能」", "浜田雅功 網走刑務所に居る“そっくりさん”の存在明かす「俺やんなあ…ほんまに似てる」", "東京や愛知など20都県に熱中症警戒アラート 今日16日(日)対象", "調布・飛田給に参加型イベントスペース 空き家利用し「みんなの秘密基地」に", "調布花火、有料席販売へ 布田会場は写真撮影エリア設置も", "大手食品メーカー 植物由来の“うなぎのかば焼き”を開発", "「ハリー・ポッター」の体験型施設 6月オープンへ 東京 練馬区"]
kijisentaku = st.empty()


def first():
    # 説明してもらう文章
    ex1 = "京都・祇園祭で 山鉾（やまほこ）ごとに販売される授与品「厄よけちまき」がインターネットで転売されるケースが相次いでいる。発売直後から100本以上が出品され、山鉾を巡行する各町の関係者は「信仰の対象でもあるのに……」と頭を悩ませている。\nちまきは、 藁（わら）や 笹（ささ）などで作られたお守りで、玄関に飾ると災厄を避けられるとされる。宵山期間（14～16日）を中心に各山鉾町が1本1000円程度で販売。34基の山鉾がある山鉾町で10万本以上作られ人気の山鉾では早々に売り切れる。\nフリーマーケットアプリ「メルカリ」では、本格的に販売が始まった14日午前の時点で100本以上が出品された。多くは1本2000～3000円で、同じ出品者が何本も取引しているケースもあった。\nコロナ禍を経て今年の祇園祭は4年ぶりの通常開催で人出が多い上、材料不足や作り手の高齢化で増産が難しいことも背景にあるとみられる。\nカマキリのからくりが人気の 蟷螂（とうろう）山では、転売対策で今年から「1人10本まで」の制限を設けたが、効果は十分ではない。 前祭（さきまつり）の巡行で先頭を進む 長刀（なぎなた）鉾も出品が目立ち、保存会の川那辺健治・専務理事（75）は「ネットで転売するのは個人の自由かもしれないが、『何してはるんやろ』という気持ち」と話す。"
    ex2 = "この日、30歳の誕生日を迎えたレッドソックス・吉田正尚（30）は敵地でのカブス戦に「2番・レフト」で先発出場。吉田は4打数無安打で9試合ぶりのノーヒット、打率は.313となった。カブス・鈴木誠也（28）は「2番・ライト」で先発出場。5打数1安打3三振だった。\nレジェンド・イチローの記録を塗り替え、8試合連続マルチヒット中の吉田は1回の第1打席、カブスの先発は今季9勝を挙げているM.ストローマン（32）、カウント2-1から内角低めのシンカーをファウルにすると球審と笑顔で会話をしていた。そして5球目、外角のストレートを見送ったがストライクの判定。珍しい見逃しの三振に倒れた。\n両チーム無得点で迎えた3回、1死一、二塁で第2打席、カウント1-2と追い込まれると4球目、137キロと手元で動くストレートを打たされセカンドゴロ併殺打。6月29日以来、今季11個目の併殺打でチャンスを潰してしまった。\n6回の第3打席、ここまで打ち取られていたストレートを弾き返したがレフトフライ。カブス・ストローマンのストレートを試合中にアジャスト出来なかった。8回の第4打席はファーストゴロに倒れた。吉田は4打数無安打で9試合ぶりのノーヒット、マルチヒットの連続試合は8でストップ。打率も.313に下がった。チームも敗れ、連勝も6でストップした。"
    ex3 = "普段多くの人が行き交うJR秋田駅前の路上は一面水に覆われていた。記録的な大雨となった秋田県。各地で河川氾濫や下水道から排水しきれず雨水があふれる「内水氾濫」が発生し、秋田市中心部でも広く冠水した。\n秋田駅前では太ももぐらいまで水があふれ、通行人がズボンをたくし上げて歩く様子も見られた。道路に動けなくなった車両が多く取り残されていたり、市内では住民がボートで救助されたりした。駅近くのアンダーパスでは水がたまり、車3台ほどが水没していた。\n同市の三浦初さん（63）は公民館に家族と自主避難した。自宅前の川は氾濫し道路も冠水した。「慌てて出てきたので、泊まる用意はしていない。とにかく早く家に帰りたい」とため息をついた。\n秋田県の佐竹敬久知事は対策会議を開き「目立つのは内水の被害。駐車場などで排水が間に合わず周囲に流れ込んで冠水していた」と話した。\n同市添川では住宅に土砂が流れ込み、建物がめちゃくちゃに。道路は通れない状況になり、現場周辺の電柱が倒れた。4人が医療機関に搬送され、軽傷を負った。"
    ex4 = "お笑いコンビ「ドランクドラゴン」の鈴木拓（47）が、15日までに更新されたYouTubeチャンネル「辛口YouTube塾」に出演。自身のYouTubeチャンネルが伸び悩んでいることについて語った。\n2022年4月にゲーム実況のYouTubeチャンネル「タクゲー!!!」を開設した鈴木だが、現在のチャンネル登録者数は6690人。「芸能人なのに登録者が少なすぎて恥ずかしい」といい「一緒に番組とかやってた、例えば梶原とか、あと馬場ちゃんとか、そいつらがとんでもない数字なのに、俺が桁が違うほど人が少なくて恥ずかしい」と話した。\n人気番組「はねるのトびら」で共演していた「キングコング」の梶原雄太のYouTubeチャンネル「カジサック」はチャンネル登録者数244万人、「ロバート」の馬場裕之のYouTubeチャンネル「馬場ごはん〈ロバート〉Baba's Kitchen」はチャンネル登録者数113万人と人気を博している。\nこれらYouTubeで人気のタレントとコラボするよう勧められると、鈴木は「はっきり言いますけど梶原大っ嫌い」と一言。「ここは一回頭下げて梶原さんに出ていただくっていうのはどうですか？」と説得されるも「切腹します、俺」と拒否した。\n「あそこ（カジサック）に頼ったら、本当スッと10（万人）くらいはいかせていただけるんでしょうけど、なんとか自分でやろうとのたうち回ってる」と意地を見せた鈴木。配信後、自身のツイッターで「NGでは無いですが今コラボさせていただいたらあまりの俺の登録者数で情けないのでしないようにしているということですね」とつづった。\n「聞きようによちゃぁNGなのかな？何せ俺の登録者数が少ないのが恥ずかしい。理由はそれです」といい「まぁ俺の登録者数なんて増えないでしょうけどね」とコメントした。"
    ex5 = "ＴＢＳの安住紳一郎アナウンサーがキャスターを務める「ＴＨＥ ＴＩＭＥ，」で見せた視聴者への気遣いが話題になった。\n午前7時3分から、「ニュース関心度ランキング」というコーナーを放送。番組公式LINEでのアンケートをもとに視聴者の関心度をランキングにして放送するが、この日は前日に明らかになったタレントryuchellさんの急死が1位だった。\n安住アナは「まずは訃報からお伝えします。タレントのryucellさんが昨日、東京都内のマンションでなくなっているのが見つかりました」と伝え、視聴者に落ち着いたトーンで呼びかけた。\n「今から10分ほど、このニュースをお伝えします。悲しいニュースなんでね。ちょっと朝から気分がすぐれないという方は、10分ほどたってから、またテレビの前に戻ってきてほしいと思います」\nあえてテレビの視聴を控える選択も提示した姿勢に、ネットでは高評価。「こういうとこ好き」「計らいかたがよかった」「きちんと事前に説明する安住さんと番組の姿勢を評価します」「安住さんが好かれてる理由がわかった気がする」「有能」などの声が上がった。"
    ex6 = "ダウンタウンの浜田雅功（60）が14日深夜放送のMBSラジオ「ごぶごぶラジオ」で、旅先で出会った自身の“そっくりさん”について語った。\nリスナーから、浜田に似ていると言われた若き日の写真が送られて来たのを受け、「何人かはおるんやろ？自分に似てる人って」と浜田。「俺、タイ行った時、山ほど居てたもん」と語り、ライセンス・井本貴史も「確かに俺も、インドネシア行ったら俺みたいなんいっぱい居ましたわ」と続いた。\nどりあんずからは、後輩らと行った北海道・網走刑務所でのロケでも“浜田の分身”に出会ったことを指摘され、「ああ、おった！おった！あれ、俺やんなあ。あれはほんまに似てる！」と反応した。\nその正体は、網走刑務所内に展示されたかつての受刑者を再現した模型。「あれは絶対、見て作りましたよ？モデル浜田さんや」と言う井本に、「あれはイジられたな、網走に。正座してるやつな…オレンジの」と爆笑だった。"
    ex7 = "環境省と気象庁は、今日7月16日(日)を対象とした熱中症警戒アラートを東京都や愛知県など20都県に発表しました。\n富山県、石川県、福井県、鳥取県、香川県、愛媛県では今年初めての発表です。\n対象地域では特に熱中症のリスクが高くなるため、屋外での長時間の行動を避け、室内ではエアコンを使用し、こまめな水分補給を心がけるなど熱中症予防を万全に行ってください。\n▼熱中症警戒アラートの発表状況 埼玉県 千葉県 東京都 静岡県 愛知県 富山県 石川県 福井県 兵庫県 和歌山県 鳥取県 島根県 徳島県 香川県 愛媛県 長崎県 熊本県 大分県 宮崎県 鹿児島県\n今日16日(日)は関東〜九州の広範囲で晴れて気温が上昇し、35℃以上の猛暑日となるところが多くなる見込みです\n熱中症警戒アラートの対象地域では暑さ指数（WBGT）も高くなり、熱中症のリスクが上昇するところがあるので、エアコンをつけたり、こまめな水分補給・塩分補給を行うなどの対策をしっかりと行ってください。\n熱中症警戒アラートとは\n熱中症警戒アラートは、予想される暑さ指数（WBGT）に応じて発表される情報で、以前発表されていた高温注意情報を置き換えたものです。2021年から全国で本運用が始まりました。\n環境省と気象庁は、暑さ指数が「危険」ランクの中でもさらに重要度の高い暑さ（WBGT：33以上）が予想される場合に「熱中症警戒アラート」を発表することを決めています。\n暑さ指数（WBGT）とは\n暑さ指数（WBGT）は国際的に用いられる指標で、人体の熱収支に与える影響の大きい湿度、日射・輻射など周辺の熱環境、気温の3つの要素から計算されています。\n熱中症患者発生率との相関が気温よりも良好で、暑さ指数が「厳重警戒」ランク以上だと熱中症患者が著しく増加することがわかっています。また、暑さ指数が「危険」ランクの場合は運動は原則中止すべきとされています。"
    ex8 = "調布市が取り組む「調布市エリアリノベーション事業」の一環としてオープンした同施設。同市では、社会問題になっている空き家の利活用を促進するプロジェクトを2020年から進めている。昨年は空き家を使い地域と連携しながら持続可能な事業に関心のある市民を募集し、富士見町に「富士見BASE（ベース）」をオープン。主に子ども向けのアート活動を行う「minglelingo（みんぐるりんご）」と、プラスチック資源のアップサイクルを行う「pebbles（ペブルス）」を中心に、地域の人々が交流する場として活動してきた。\n富士見BASEの契約期間満了に伴い、新たに飛田給の空き家を使い、引き続き両事業者の活動の拠点として同施設をオープン。富士見BASEが子どもたちの居場所となっていたことに価値を感じ、同施設では経済的に持続可能な事業を作り上げることに注力するのではなく、子どもたちの未来に向けた種まきとなるような活動に注力することで、持続可能な社会に貢献することを目指す。\n1階部分は地域に開かれたイベントスペースにして、子どもたちの未来に向けた種まきとなるイベントを募集。イベントスペースで「やりたいこと」「やってほしいこと」について話し合う公開型の「みんなの企画会議」を開催し、イベントと企画者を広く募った。現時点では、「普段と違うワクワク感」を感じてもらいたいと夜に開催する映画上映会、ご近所で交流する場として夕飯を一緒に食べる会、カードゲームイベント、駄菓子屋など、それぞれ異なる思いを持つ市民が中心となってイベントを開催する予定。\n施設名には、「飛田給の箱」という意味に加え、跳び箱のように「勇気を出して高い壁を飛び越える」「一段ずつ『できた』を積み上げる」「周りで見学している人が応援し合う」という意味を込めたと、発案者でまちづくりを研究している共立女子大学の学生。誰もがチャレンジできる「みんなの秘密基地」も目指し、イベントを行いたい個人・団体も随時募集する。\nみんぐるりんごを主宰する西村さん夫妻は「子どもたちへの種まきを通して多世代が交流し、新たなコラボが生まれるのが楽しみ」と話し、ペブルスを主宰する太田風美さんは「空き家に関わる事業者として、社会問題についてもカジュアルに話し合えるような場にできたら」と話す。"
    ex9 = "有料席は3会場に用意。布田会場の土手上部には「布田テーブルS」（4人＝3万2,000円）と「布田イスS」（1人＝6,000円）、土手下部には「布田テーブルA」（4人＝2万8,000円）、「布田ペア」（2人＝1万2,000円）、「布田イスA」（1人＝5,500円）、「布田シート」（4人＝1万7,000円）、「布田升A」（10人＝6万円）、「布田升B」（10人＝5万円）を用意し、会場内に写真撮影エリアも設ける。\n京王多摩川会場は、「多摩川イスSS」（1人＝5,500円）、「多摩川升」（10人＝5万5,000円）、「多摩川イスS」（1人＝5,000円）、「多摩川テーブルA」（4人＝2万6,000円）、「多摩川ペア」（2人＝1万円）、「多摩川イスA」（1人＝4,500円）を用意。電通大グラウンド会場には「映画のまち調布シート」（1人＝3,500円）を用意する。\n実行委員会の伊藤菜々子さんは「有料席は打上場所の間近に設置するため、臨場感抜群の迫力ある花火をぜいたくに楽しむことができる。ぜひ、会場まで足をお運びいただきたい」と話す。\n販売開始時間は10時。市民先行販売は7月13日～19日。一般販売は7月20日から全国にあるセブン‐イレブンのセブンチケットで販売。販売開始時間は10時～。席の位置や購入方法などはホームページで確認できる。「映画のまち調布シート」以外は全て指定席。イオンシネマ・シアタス調布半券サービスとも連携し、9月24日当日か同日より1カ月間、参加店で有料席チケットを提示すると店独自のサービスが受けられる。"
    ex10 = "植物由来の原料を使う「代替食品」は、ますます進化しています。大手食品メーカーがうなぎのかば焼きを再現した商品を開発し、土用の丑（うし）の日にあわせて販売します。\n大手食品メーカーが開発した“うなぎのかば焼き”は、植物由来の原料の大豆たんぱくや植物油脂などを使い、動物由来の原料は使っていません。\n本物のうなぎのかば焼きの食感に近づけるため、白身や皮などを意識した生地を3層に重ねて実際に火であぶって焼き目をつけています。\nさらに、竹炭の粉末を使ってうなぎの皮特有の黒さも表現しています。\n\nうなぎの稚魚のシラスウナギの漁獲量が減少傾向にあることや、海外での需要の高まりなどを背景に、うなぎの価格が上昇していることから、代替食品の開発を進めてきたということです。\n\n価格は1セット1500円で、土用の丑の日にあわせてネット販売をすることにしています。\n\n日清食品ホールディングス食品開発部の中山貴照次長は「この先、うなぎを食べられなくなる日が来るのではないかと危惧して今回の製品をつくった。どれくらい需要があるかを確かめながら幅広く展開することを考えていきたい」と話しています。\n「代替たんぱく質」 市場規模は \n植物由来の原料でつくる代替肉や代替シーフードなど「代替たんぱく質」の市場規模は高い成長が予想されています。\n\n民間のシンクタンクの調査によりますと、代替たんぱく質の世界の市場規模は、メーカーの出荷額ベースの推計で、おととしは4861億円でしたが、2025年には1兆1919億円に拡大し、2030年には、おととしの6.8倍の3兆3113億円に拡大すると予想されています。\n\n世界的な人口の増加による食料不足問題や、飼料や水の消費をめぐって畜産業の環境への影響を懸念する消費者の意識が高まることが背景にあると調査会社はみています。\n\n代替たんぱく質は、海外市場を中心に普及が進んでいましたが、日本でもこのところ大手食品メーカーなどが相次いで参入し、小売店での販売や外食チェーンでの展開も広がり始めています。"
    ex11 = "東京練馬区の「としまえん」の跡地に整備が進められている映画「ハリー・ポッター」の体験型の施設が、ことし6月16日にオープンすることになりました。15日は、施設の一部がメディア向けに初めて公開されました。\n\n映画「ハリーポッター」の世界が体験できる、この施設は「ワーナー ブラザース」が3年前に閉園した東京 練馬区の「としまえん」の跡地の一部に整備を進めています。\n\n建物の広さはおよそ3万平方メートルで、「ハリーポッター」の屋内型の施設としては世界最大の規模になるということです。\n\n15日は現地でイベントが開かれ、オープンがことし6月16日になることが発表されたほか、施設の一部がメディア向けに初めて公開されました。\n\n映画でたびたび登場する場面を再現したセットを歩き回って楽しめることや、主人公さながらにほうきにまたがって空を飛び回っているかのような映像を撮影してもらえることなどが紹介されました。\n「ワーナー ブラザース スタジオジャパン」の松尾俊宏バイスプレジデントは「インバウンドの面で新たなエンタメ施設を東京から発信できることは大きな意味がある。としまえんのように地域の人たちが近くに住んでいることを誇りに思ってもらえるようにしていきたい」と話していました。\n\nハリーポッターの人気にあやかろうと、地元の練馬区もこの施設のオープンに合わせてまちおこしの取り組みを進めています。\n\n地域の住民や商店街などと協力して魔法にちなんだ飲食のメニューを開発したり、店舗に装飾を施したりして、観光客の誘致に取り組んでいきたいとしています。\n企画している「ねりま観光センター」は「長く愛されたとしまえんに代わる新たなシンボルが生まれることはうれしい。魔法の世界観を楽しめる仕掛けづくりに力を入れて地域を盛り上げていきたい」と話していました。"
    texts = [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10, ex11]
    st.session_state.exampletexts = texts[st.session_state.kiji]
    st.session_state.assistant1 = [
        {"role": "system", "content": "あなたは便利なアシスタントです．以下の文章を参照して短く答えてください．\n\n###文章###\n" + st.session_state.exampletexts},
        {"role": "user", "content": "まずは文章の導入部分を1文で簡単に述べてください．"}
    ]
    # 記事の説明文を生成
    completion1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.assistant1
    )
    a1message = completion1.choices[0].message.content

    st.session_state.dialog.append(a1message)

    # 初めの質問候補を生成
    assistant_tmp = [
        {"role": "system", "content": "あなたは便利なアシスタントです．"},
        {"role": "user", "content": "###指示###\n以下の文章について，文章の中に答えのある質問を敬語でいくつか作成してください．文章の重要な部分が含まれることが望ましいです．フォーマットは番号つきリストとします．\n\n###文章###\n" + st.session_state.exampletexts}
    ]
    completion_tmp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=assistant_tmp
    )
    st.session_state.question = [q[2:] for q in completion_tmp.choices[0].message.content.split("\n")] + ["終了します", "-", "-", "-"]
    st.session_state.generated.append(a1message)


def initfn():
    with kijisentaku.container():
        st.session_state.kijitext = st.radio("選んでください", (kijilist))
        st.session_state.kiji = kijilist.index(st.session_state.kijitext)
        if not st.button("記事を選択しました．", on_click=lambda: first(), key='first'):
            st.stop()
    st.session_state.kijistate = False


def notinitfn():
    kijisentaku.markdown(st.session_state.kijitext)


if st.session_state.kijistate:
    initfn()
else:
    notinitfn()


def click(i):
    choice = {"role": "user", "content": st.session_state.question[i]}  # 質問候補文
    st.session_state.assistant1.append(choice)
    st.session_state.dialog.append(choice["content"])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.assistant1
    )
    '''
    if "ません" in completion.choices[0].message.content:
        st.text("検索しています")
        result = kensaku.searchfromquestion(st.session_state.question[i])
        st.session_state.dialog.append(result)
        st.session_state.generated.append(result)
    else:
    '''
    st.session_state.dialog.append(completion.choices[0].message.content)
    st.session_state.generated.append(completion.choices[0].message.content)

    st.session_state.past.append(st.session_state.question.pop(i))


chat_placeholder = st.empty()
chat_initial = st.empty()
with chat_placeholder.container():
    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
        message(st.session_state['generated'][i], key=f"{i}")


button_placeholder = st.empty()


with button_placeholder.container():
    st.button(st.session_state.question[0], key='b1', on_click=lambda: click(0))
    st.button(st.session_state.question[1], key='b2', on_click=lambda: click(1))
    st.button(st.session_state.question[2], key='b3', on_click=lambda: click(2))
