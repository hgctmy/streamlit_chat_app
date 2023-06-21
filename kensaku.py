import os
import re
from llama_index.readers import BeautifulSoupWebReader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from google_api import search_google


def searchfromquestion(question):
    os.environ["OPENAI_API_KEY"] = "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"

    # 質問文からそれに合った検索ワードを出力する
    chat = ChatOpenAI(temperature=0)

    ret = chat([HumanMessage(content="以下の例題にならって、知りたい情報を得るための適切な検索語句を出力してください。\n"
                             "例：「今年のWBCのMVPは誰ですか？」：「WBC 2023 MVP」\n"
                             "例：「初代ポケットモンスターのゲームに登場するポケモンは何種類か知りたい。」：「初代 ポケモン 種類」\n"
                             "例：「Linuxで使えるコマンドとその意味を分かりやすくリストアップしてほしい」：「Linux コマンド 一覧 初心者」\n"
                             f"問題：「{question}」")])

    # ChatGPTの出力は「＜検索ワード＞」となるはずなので、「」の中身を取り出す
    search_query = re.findall('「(.*?)」', f"{ret.content}")[0]

    url_data = search_google(search_query)  # 上位3件取得する

    # URLのみ渡してスクレイピング
    documents = BeautifulSoupWebReader().load_data(urls=[data["link"] for data in url_data])

    max_texts = 500
    documents_text = ""
    references = {}

    for i in range(len(url_data)):
        # 余分な空白や改行を除去
        text = documents[i].text.replace('\n', '').replace("  ", " ").replace("\t", "")
        # テキストの最初の方はサイトのメニュー関連が多いので、テキストの一部だけを抽出するなど前処理をする
        # text = text[len(text)//10:]
        documents_text += f"【文献{i + 1}】{url_data[i]['snippet']}\n{text}"[:max_texts] + "\n"
        references[f"文献{i + 1}"] = {
            "title": url_data[i]['title'],
            "link": url_data[i]['link']
        }
        if len(documents_text) > 3000:
            documents_text = documents_text[:3000]
            break

    ret = chat([HumanMessage(content=f"以下の文献を参考にして、下の質問に簡単に答えてください。\n"
                             f"◆文献リスト\n{documents_text}\n"
                             f"◆質問：{question}\n"
                             f"◆回答："
                             )])

    # ChatGPTの回答を格納
    return ret.content, references


if __name__ == '__main__':
    print(searchfromquestion("ChatGPTってなんですか？"))
