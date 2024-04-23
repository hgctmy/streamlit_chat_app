# -*- coding: utf-8 -*-
from openai import OpenAI
import json
import random
import re
import database
import os


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


class Question:
    def __init__(self, text, score):
        self.text = text
        self.score = score


class Questions:
    def __init__(self, questions):
        self.questions = questions


def create_question(dialog, article, user_score):
    conn = database.create_connection("gpt.db")
    database.init_db(conn)
    message1 = [
        {
            "role": "system",
            "content": "You are a helpful assistant.\n"
        },
        {
            "role": "user",
            "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create six candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. Candidate questions should be two each of the following three patterns.\n  - Beginner-level questions(Asking about the meaning of terms, etc.).\n  - General questions. \n  - Detailed questions that an expert would ask. \n3. Output in json format like this.\n{\n  \"Beginner-level questions\": [\n    \"question\",\n    \"question\"\n  ],\n  \"General questions\": [\n    \"question\",\n    \"question\"\n  ],\n  \"Detailed questions\": [\n    \"question\",\n    \"question\"\n  ]\n}\n\n==dialogue history==\n" + dialog
        }
    ]
    response = database.fetch_response(conn, message1)
    if not response:
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            response_format={"type": "json_object"},
            messages=message1,
            temperature=0
        )
        response = response.choices[0].message.content
        database.insert_chat_pair(conn, message1, response)
    question = json.loads(response)
    qbe = question["Beginner-level questions"]
    qge = question["General questions"]
    qde = question["Detailed questions"]
    ql = qge + qde
    q = [str(i + 1) + ql[i] for i in range(4)]
    q = "\n".join(q)
    message2 = [
        {
            "role": "system",
            "content": "==Instructions==\nYou will be given a news article, a conversation history about the article, and questions following the conversation history, so please answer \"answerable\" if the question can be answered based on the content of the article, and \"unanswerable\" if the question cannot be answered based on the content of the article.\n\n==Input example==\n##News article##\nAmid ever increasing demand for electricity, artificial intelligence (AI) is now being used to help prevent power cuts.\n\n\"I woke up in the middle of the night very, very cold,\" remembers Aseef Raihan. \"I pulled out my military sleeping bag, and slept in that overnight for warmth.\n\n\"In the morning I figured out that the power was definitely not on.\"\n\nMr Raihan is describing the scene back in February 2021 when he was stationed in San Antonio, Texas, while serving in the US Air Force.\n\nThat month the state was blasted by winter storm Uri. As temperatures plummeted to -19C, Texans sought to keep warm, sending the demand for electricity sky high.\n\n\nAt the same time, Texas' electricity grid started to unravel. Wind turbines froze over, snow covered solar panels, and a nuclear reactor had to be taken offline as a precaution.\n\nWith not enough electricity to go around, the power went off for more than 4.5 million homes and businesses, first for hours, and then for days on end.\n\n\"Without power, the heating wasn't working at all. And you couldn't use the electric stove or microwave for food,\" recalls Mr Raihan.\n\nIn the end it took more than two weeks for the Texan power grid to return to normal.\n\nGetty Images A worker repairs a power line in Austin, Texas, in February 2021Getty Images\nBack in February 2021 Texan power firms had to race to fix facilities and lines damaged by extremely cold weather\n\nThe storm revealed the fragility of the systems we take for granted to deliver us electricity around the clock.\n\nAnd while not all countries have winters as severe as they can be in North America, demand for electricity is ever increasing around the world. From charging electric cars, to more homes getting air conditioning installed, we are using more and more power in our daily lives.\n\nThis comes at the same time as countries are increasingly moving towards renewable sources of energy, which are more variable in the amount of energy they generate. If the wind doesn't blow, and the sun doesn't shine, then electricity production drops.\n\nAll this led to UK Energy Secretary Claire Coutinho warning last month that the country could face blackouts in the future without new gas powered power stations as \"back up\".\n\nAnother way to make energy systems more resilient is by adding huge batteries to the grid.\n\n\nThe thinking goes that when there is electricity going spare, batteries can charge up, and then release electricity later when there is more demand for power.\n\nThis is an approach that has been taken in Texas.\n\n\"Since the storm we built over five gigawatts of battery storage capacity in Texas in three years, which is really an incredible pace,\" says Dr Michael Webber, professor of energy resources at the University of Texas at Austin. That much energy, he says, is about \"four large nuclear power plants\".\n\nGetty Images A worker pointing to batteries at an energy storage facility in CaliforniaGetty Images\nPower firms in Texas and other US states are building energy storage facilities full of rows and rows of batteries\nHowever, for such batteries to be really useful, they need to know the best time to charge, and the best time to discharge. That means making complex predictions about how much electricity is going to be needed in the future.\n\n\n\"The main thing that makes the biggest difference is weather and electricity demand,\" says Gavin McCormick, founder of the tech start-up WattTime.\n\nHis Oakland, California-based company makes AI software that predicts electricity supply and demand in a given area or region. This information can then tell batteries when to charge and discharge.\n\nThe same information can also be used in homes to help people use mains electricity more cheaply.\n\n\"So if you had an electric vehicle that you need to be ready in eight hours, but it only takes two or three hours to charge, what it can do is it can find the five minute periods all night where there's surplus energy, or maybe there's clean energy,\" Mr McCormick says.\n\n\"It will charge in little spurts at all the best times and still be ready by morning.\"\n\n\nThe AI can make these predictions by analysing weather patterns, holiday dates, work schedules, and even when the football is on. \"Everybody gets up and makes a cup of tea at halftime,\" Mr McCormick says.\n\nAnother company using AI to predict electricity demand is Danish firm Electricity Maps. It focuses its AI on forecasting weather patterns like cloud cover, wind strength, temperature and rainfall.\n\nThis information is used to better understand how much electricity will be generated from wind turbines or solar panels.\n\n\"If you can predict quite accurately in advance how much wind you're going to have in the system, you can plan ahead.\" says Olivier Corradi, the company's founder.\n\n\"One example is Google, where we're providing them forecasts of how clean the grid is going to be in the next couple of hours. They can use that in their data centres to change the time at which they're consuming electricity \"\n\n\nBanner around links to stories about AI\nRead more stories on artificial intelligence\n\nBanner around links to stories about AI\nAI is also now being used to protect the physical infrastructure that carries electricity to our homes.\n\nOne company, Buzz Solutions, uses AI to scan through imagery of electricity cables, pylons and substations, identifying signs of damage such as broken parts or rust.\n\n\nThe system also identifies when trees and other greenery are growing too close to power lines.\n\nNot only can this prevent power outages from damaged lines, but it can also reduce the risk of wildfires, which can be caused from power lines coming into contact with trees as happened in California in recent years.\n\nThe tech can also spot and automatically report to power firm staff another major cause of power outages - wildlife.\n\n\"A lot of times surprisingly, animals get into substations like squirrels and rodents, and they get electrocuted,\" says Buzz Solutions co-founder Vikhyat Chaudhry.\n\n\"Their electrocution sometimes leads to a massive explosion at the substation. Our AI that's deployed at substations, one of the things that they're detecting is animal intrusions including raccoons and squirrels.\"\n\n\n##dialogue about news article content##\n**commentator:** Artificial intelligence is now playing a crucial role in managing and preventing power outages as demand for electricity surges globally.\n\n**questioner:** What role is AI playing in the management of electricity grids according?\n\n**commentator:**  AI is being used to predict electricity supply and demand, helping to optimize when batteries should charge and discharge. Additionally, AI helps in detecting infrastructural damage and potential hazards like animal intrusions that could lead to power outages.\n\n##Questions##\n1. How does AI predict electricity supply and demand?\n2. What technologies are used in AI to detect potential hazards like animal intrusions?\n3. What specific algorithms or models does AI use to forecast electricity demand and optimize battery usage?\n4. Could you detail how AI systems are trained to recognize and respond to different types of infrastructural damage in power grids?\n\n==Output example==\n1. answerable\n2. answerable\n3. unanswerable\n4. unanswerable"
        },
        {
            "role": "user",
            "content": "==Input==\n##News article##\n" + article + "\n\n##dialogue history##\n" + dialog + "##Questions##" + q
        }
    ]
    res = database.fetch_response(conn, message2)
    if not res:
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message2,
            temperature=0,
        )
        res = res.choices[0].message.content
        database.insert_chat_pair(conn, message2, res)
    answer = re.findall(r". (.*)", res)
    answernum = [i if answer[i] == "answerable" else "" for i in range(4)]
    if user_score < 1.5:
        if 0 not in answernum or 1 not in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create two candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. Output in bullet points.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qge = re.findall(r"- (.*?\?)", response)
        return [Question(random.choice(qbe), 1), Question(qge[0], 2), Question(qge[1], 2)]
    elif user_score < 2:
        if 0 in answernum and 2 in answernum:
            return [Question(random.choice(qbe), 1), Question(qge[0], 2), Question(qde[0], 3)]
        elif 0 in answernum and 3 in answernum:
            return [Question(random.choice(qbe), 1), Question(qge[0], 2), Question(qde[1], 3)]
        elif 1 in answernum and 2 in answernum:
            return [Question(random.choice(qbe), 1), Question(qge[1], 2), Question(qde[0], 3)]
        elif 1 in answernum and 3 in answernum:
            return [Question(random.choice(qbe), 1), Question(qge[1], 2), Question(qde[1], 3)]
        elif 2 in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create one candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qge = response
            return [Question(random.choice(qbe), 1), Question(qge, 2), Question(qde[0], 3)]
        elif 3 in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create one candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qge = response
            return [Question(random.choice(qbe), 1), Question(qge, 2), Question(qde[1], 3)]
        elif 0 in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create one candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. The question should be detailed question that an expert would ask.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qde = response
            return [Question(random.choice(qbe), 1), Question(qge[0], 2), Question(qde, 3)]
        elif 1 in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create one candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. The question should be detailed question that an expert would ask.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qde = response
            return [Question(random.choice(qbe), 1), Question(qge[1], 2), Question(qde, 3)]
        else:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article},
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create six candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. Candidate questions should be the following two patterns.\n  - General question(Questions should be answerable through news articles.). \n  - Detailed question that an expert would ask(Questions should be answerable through news articles.). \n4. Output in json format like this.\n{\n \"General question\": \"question\", \n \"Detailed question\": \"question\"\n}\n\n==dialogue history==" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            question = json.loads(response)
            qge = question["General question"]
            qde = question["Detailed question"]
            return [Question(random.choice(qbe), 1), Question(qge, 2), Question(qde, 3)]
    elif user_score < 2.5:
        if 0 not in answernum or 1 not in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create two candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. Output in bullet points.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qge = re.findall(r"- (.*?\?)", response)
        if 2 in answernum:
            return [Question(qge[0], 2), Question(qge[1], 2), Question(qde[0], 3)]
        elif 3 in answernum:
            return [Question(qge[0], 2), Question(qge[1], 2), Question(qde[1], 3)]
        else:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create one candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. The question should be detailed question that an expert would ask.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qde = response
            return [Question(qge[0], 2), Question(qge[1], 2), Question(qde, 3)]
    else:
        if 2 not in answernum or 3 not in answernum:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create two candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n3. The question should be detailed question that an expert would ask.\n4. Output in bullet points.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qde = re.findall(r"- (.*?\?)", response)
        if 0 in answernum:
            return [Question(qge[0], 2), Question(qde[0], 3), Question(qde[1], 3)]
        elif 1 in answernum:
            return [Question(qge[1], 2), Question(qde[0], 3), Question(qde[1], 3)]
        else:
            message = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + article
                },
                {
                    "role": "user",
                    "content": "== Instructions==\nGiven the dialogue history between the commentator and the questioner regarding the content of the news article as input, create one candidate questions to be asked by the questioner following the dialogue history. Subject to the following conditions.\n\n==Conditions==\n1. Candidate question must be a natural follow-up to the dialogue history.\n2. The question should be one that can be answered by the content of the news article.\n\n==dialogue history==\n" + dialog
                }
            ]
            response = database.fetch_response(conn, message)
            if not response:
                response = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=message,
                    temperature=0,
                )
                response = response.choices[0].message.content
                database.insert_chat_pair(conn, message, response)
            qde = response
            return [Question(random.choice(qge), 2), Question(qde[0], 3), Question(qde[1], 3)]


if __name__ == "__main__":
    article = ""
    dialog = ""
    user_score = 1.5
    create_question(dialog, article, user_score)
