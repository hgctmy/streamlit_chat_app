from googleapiclient.discovery import build
# import json

GOOGLE_API_KEY = "AIzaSyAkoYXiXqkcv_Cpd21IUD_mVN8xERyVMgk"
GOOGLE_CSE_ID = "91cb76eb2a47d4e66"


def search_google(keyword, num=3) -> dict:
    """Google検索を行い、レスポンスを辞書で返す"""
    search_service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
    response = search_service.cse().list(
        q=keyword,
        cx=GOOGLE_CSE_ID,
        lr='lang_ja',
        num=num,
        start=1
    ).execute()
    # response_json = json.dumps(response, ensure_ascii=False, indent=4)

    # ファイルに書き出す必要がなければ、以下のブロックは省略できます
    '''with open("response.json", mode='w', encoding="utf-8") as f:
        f.write(response_json)
    '''
    return response["items"]


if __name__ == '__main__':
    keyword = input("検索キーワードを入力してください：")
    print(search_google(keyword))
