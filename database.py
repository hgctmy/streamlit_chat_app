import sqlite3


def create_connection(db_file):
    """ SQLiteデータベースへの接続を設定 """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def init_db(conn):
    """ データベース内にテーブルを作成（存在しない場合） """
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS chat_history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                request TEXT NOT NULL,
                                response TEXT NOT NULL
                            ); """
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)


def fetch_response(conn, request):
    """ リクエストに基づいてレスポンスを検索し、存在する場合はレスポンスを返す """
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM chat_history WHERE request=?", (str(request),))
    response = cursor.fetchone()
    return response[0] if response else None


def insert_chat_pair(conn, request, response):
    """ チャットペアをデータベースに追加 """
    sql = ''' INSERT INTO chat_history(request, response)
              VALUES(?, ?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (str(request), response))
    conn.commit()


def get_gpt_response(prompt):
    response = "recieved:" + prompt
    return response


def main(request_text):
    database = "chat_gpt.db"
    conn = create_connection(database)
    if conn:
        init_db(conn)
        response = fetch_response(conn, request_text)
        if response:
            return response
        else:
            response = get_gpt_response(request_text)
            insert_chat_pair(conn, request_text, response)
            return response


if __name__ == '__main__':
    request = "Hello, how are you?"
    print(main(request))
