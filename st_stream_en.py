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
kijilist = ["①Brightest-ever cosmic explosion solved but new mysteries sparked", "②Can AI help solve Japan’s labour shortages?", "③Baltimore sues owner and manager of 'unseaworthy' Dali over bridge collapse", "④Spain to axe 'golden visas' scheme"]
kijisentaku = st.empty()

chat_placeholder = st.empty()


def initfn():
    st.session_state.conn = database.create_connection("gpt.db")
    database.init_db(st.session_state.conn)
    with kijisentaku.container():
        st.session_state.kijitext = st.radio("Please select the specified article", (kijilist))
        st.session_state.kiji = kijilist.index(st.session_state.kijitext)
        st.session_state.worker = st.text_input("Enter the worker id and press enter.", key="workername")
        exampletexts1 = "Researchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard."
        exampletexts2 = "Can AI help solve Japan’s labour shortages?\n\nA shrinking population means Japan has a shortage of workers. Many are hoping that artificial intelligence (AI) can pick up the slack.\n\nIn a country that is known to be obsessed with perfection, damaged or misshapen vegetables and fruits are hard to sell.\n\nAnd if you are a specialist maker of Japanese dumplings, like the brand Osaka Ohsho, then selling a packet of gyoza with some damaged is a big no-no.\n\nBut as demand surged during the pandemic, its parent firm, Eat&Holdings, simply didn't have enough manpower to check every single dumpling, or keep up with demand.\n\nSo it turned to technology for an answer. In January 2023, it opened a high-tech factory equipped with AI-powered cameras trained to detect any faulty gyoza on the production lines.\n\n\nToday this facility makes two dumplings every second. That's twice the speed of the other Osaka Ohsho production sites.\n\n\"By implementing AI, we have reduced the manpower on the manufacturing line by almost 30%,\" says spokeswoman Keiko Handa.\n\nThe firm has also recently launched an AI-powered cooking robot called I-Robo at one of its Tokyo restaurants. As it takes time to train chefs, the company says the technology will help with the labour shortage issue.\n\n\nJapan's labour shortfall is only likely to get worse.\n\n\nThe current population of 124.35 million has been falling for 13 years. And Japan's labour force is expected to continue to decline by 12% from 2022 to 2040, by which time it is estimated that the country will lack 11 million workers.\n\nMeanwhile, Asia's second-biggest economy is already home to the world's oldest population, with 29% of people aged 65 or above.\n\nThe country also has one of the lowest birth-rates in the world, with only 758,631 babies born last year. That is the smallest number since records began in the 19th century.\n\nThe government's efforts to boost its birth rates have met with little success. In the words of Prime Minister Fumio Kishida, his country is \"on the brink of not being able to function\".\n\nSince AI took the world by storm, many have asked if our jobs will be stolen. But for some in Japan, AI cannot arrive fast enough.\n\nFarming is one of the fastest-ageing industries in the country, with the average age of a Japanese farmer now standing at 68.4 years. Here AI is being used to identify different types of diseases, pests and weeds for early detection and prevention.\n\nNihon Nohyaku, which manufactures agricultural chemicals, has developed a smartphone app called Nichino AI. When a farmer takes a picture of struggling crops, the app gives a diagnosis of what is wrong and which pesticide may be needed.\n\n\n\n\"The accuracy rate is about 70 to 80%, so it is not as good as real experts, but better than ordinary farmers,\" says Kentarou Taniguchi from Nihon Nohyaku.\n\n\"The longer we work on this app, the more we realise how excellent the human experts are,\" he explains. \"But the number of experts is falling, so that is where AI tools can come in handy.\"\n\nFarmer Kensuke Takahashi, who has been using the app for three years, agrees that AI is one of the tools that will help modernise the sector. \"The number of farmers is falling sharply like a rollercoaster,\" he says, \"but Japan's total amount of produce is increasing.\"\n\nMr Takahashi acknowledges that there are older farmers who may be sceptical of any new technologies such as AI, but he believes they are helping to increase efficiency levels. \"Once you try out a drone to spray pesticide, you cannot go back to manual spraying,\" he laughs.\n\nWhat about a sector that has always faced a shortage - language teachers?\n\nDespite the government's repeated efforts to increase the number of English speakers, Japan has constantly ranked low in English proficiency, due to the lack of teachers who can effectively speak the language.\n\nTo try to overcome this shortfall, a start-up called Equmenopolis has developed an AI-powered online tool that allows users to have English conversations with its avatar for 15 minutes per session. It has so far been introduced at 50 schools across the country.\n\n\nAt Narita Kokusai High School, on the outskirts of Tokyo, students were asked to use it at home to practice for three months at the end of last year.\n\n\"AI decides what kind of English conversations each student can have and varies its questions,\" teacher Shoko Takiguchi tells the BBC. \"It is difficult to have one-on-one conversations with every student so that was an advantage.\"\n\nAt the end of each conversation, students get feedback in six areas including pronunciation, grammar, fluency and vocabulary.\n\n\"With AI, it is easy to find out what my weakness was, so it was efficient,\" says one of the students, Ko Hanyuan. But asked if he would choose AI over his online tutorial, he says no. Why? It lacks the human touch.\n\nMs Takiguchi agrees: \"It is useful to improve your speaking skills, but I found conversations to be unnatural.\" She adds that the AI is unable to assess the user's reaction, physical condition, or change in tone.\n\nSo it won't replace human teachers? \"AI can not and should not replace English lessons at school or teachers,\" emphasises the school's principal Katsutoshi Fukumizu.\n\nNarita Kokusai High School Narita Kokusai High School classroom.Narita Kokusai High School\nEndorsed by the Japanese government, 50 high schools across the country tried an AI English learning tool\nGovernments in Japan are also experimenting with AI.\n\nFaced with labour shortages, Yokosuka City in Kanagawa prefecture has starting using AI chatbot ChatGPT to help with administrative tasks such as transcribing and summarising meetings.\n\n\"We deal with enormous amount of documents, and it takes a very long time and effort to create those documents,\" says the city's spokesperson Kohei Ota.\n\nThanks to ChatGPT, \"we have calculated after our trial that we save 22,700 hours of work annually,\" he adds.\n\nAt the national government's Digital Agency, which was established in 2021 to overcome inefficiency in public administration, AI is also used to train its staff.\n\n\"There are so many things that we want to do, but our manpower hasn't been able to keep up,\" says Masanori Kusunoki from the agency. He adds that the government is trying to \"explore how we can use AI, and spread the information\" to the private sector.\n\nBut Mr Kusunoki doesn't think that the rise of AI will mean fewer workers are needed.\n\n\nIn a country where changes happen slowly, Japan is embracing the power of AI with less reluctance than others.\n\nThat is because it has looked into every possible solution to tackle the double whammy of an ageing and shrinking population for more than a decade: from robots, to women, the elderly and foreign workers.\n\nWhile AI may help increase the efficiency of the workforce, it is nowhere near ready to replace human workers."
        exampletexts3 = "Baltimore sues owner and manager of 'unseaworthy' Dali over bridge collapse\n\nBaltimore has sued the operators of the container ship that hit and destroyed one of the US city's main bridges last month, killing six people.\n\nThe city says the Dali was \"clearly unseaworthy\" and accuses its owners and manager of negligence.\n\nThe ship's Singapore-based owner and manager have already asked a court to limit their liability.\n\nThe region is reeling from the closure of its busiest maritime transit port after the span collapsed on 26 March.\n\n\"None of this should have happened,\" attorneys representing the Baltimore mayor and city council argued in a federal lawsuit.\n\nThe city is asking the US District Court of Maryland for a jury trial to hold the defendants fully liable.\n\nNaming the Dali's owner, Grace Ocean Private Limited, and its manager, Synergy Marine Private Limited, the suit alleges the Francis Scott Key Bridge's collapse was a direct result of their \"gross negligence, and recklessness, and as a result of the unseaworthiness of the Vessel\".\n\nOn 1 April, Grace Ocean and Synergy Marine petitioned the same federal court in Maryland to cap its responsibility for the incident.\n\nCiting a pre-Civil War maritime law, the pair of companies estimated their liability for the vessel and the cargo's value at $43.6m (£35m).\n\nMonday's court filing from the city of Baltimore rebuts that number as \"substantially less than the amount that will be claimed for losses and damages arising out of the Dali's allision with the Key Bridge\".\n\nThe path taken by the cargo ship - which was exiting the Port of Baltimore under the Key Bridge - is \"no stranger to large freighters\", the city's representatives wrote.\n\nThey said the vessel \"had been experiencing an inconsistent power supply\" that was either not investigated or not fixed.\n\n\"The Dali left port anyway, despite its clearly unseaworthy condition,\" said the lawsuit.\n\nThe filing also says the Dali was manned by \"an incompetent crew that was inattentive to its duties\" and \"lacked proper training\".\n\nOn Friday, port officials opened a third temporary channel for boats to enter and exit the corridor, but these channels can only sustain about 15% of pre-collapse commercial activity.\n\nA fourth channel, that will allow most traffic back into the port, is expected to open by the end of the month.\n\nDarrell Wilson, an attorney who represents Synergy Marine and is also handling media inquiries on behalf of Grace Ocean, told the BBC it would be inappropriate to comment on the litigation while federal investigations into the collapse were ongoing.\n\nSix construction workers who were fixing potholes died when the bridge collapsed. Two of the bodies have yet to be recovered.\n\nWorkers are still extracting thousands of tonnes of debris from the water and from atop the stationary Dali, whose original schedule would have seen it arrive at a Sri Lankan port on Monday.\n\nApart from two of the ship's pilots, 21 crew members - almost all of whom are of Indian origin - remain on the ship. There is no timeline yet for when the crew will disembark or head back to sea."
        exampletexts4 = "Spain to axe 'golden visas' scheme\n\nThe Spanish government has begun the process of eliminating the so-called \"golden visa\" scheme.\n\nUnder the scheme, foreign investors are provided with fast-tracked residency.\n\nAt a Cabinet meeting on Tuesday, ministers agreed to end the awarding of the visa, which can be obtained in exchange for buying property worth €500,000 (£428,000) or more.\n\nThe visa scheme was created in 2013 by the conservative government of Mariano Rajoy.\n\nIt was seen as a way of attracting badly needed foreign investment in the wake of the eurozone crisis, which hit Spain's property sector particularly hard.\n\nA total of 6,200 visas were issued until 2023 for investment in property, according to the organisation Transparency International, although other sources put the number higher.\n\nNearly half of beneficiaries of Spain's Golden Visa - a total of 2,712 - were Chinese, according to Transparency International.\n\nRussians were the next most numerous recipients, with 1,159, followed by Iranians (203), and citizens of the US (179) and the UK (177).\n\nThe \"golden visa\" scheme also provided residency in exchange for investing €2m (£1.7m) or more in state bonds, or for investing in emerging Spanish companies.\n\nHowever, only 6% of visas were awarded for reasons other than the purchase of property, the government said.\n\nPrime Minister Pedro Sánchez said his government's intention to scrap the scheme was intended \"to guarantee that housing is a right and not merely the subject of business speculation\".\n\nHe said that the majority of visas awarded were linked to the purchase of properties in places such as Madrid, Barcelona, Valencia, Málaga, Alicante and the Balearic Islands - all areas where the housing market \"is under enormous pressure and where it is almost impossible for people who live and work in those places and pay their taxes each day to find affordable housing\".\n\nSome areas of the country have been particularly affected by rising rents, such as Ibiza, in the Balearic Islands.\n\nLast year, the government introduced a housing law which aimed to cap rental increases in areas where they have been spiralling.\n\nMr Sánchez's left-wing allies in his coalition government had been calling for an end to the visa system.\n\nHowever, critics say that its elimination will not improve matters.\n\n\"The problem with housing in Spain, both in terms of sales and rental, is not caused by the Golden Visa, but rather by the increasing lack of supply [of housing] and the accelerating growth in demand,\" said Francisco Iñareta, of the Idealista property portal.\n\nHowever, pressure has also come from outside Spain, with the European Commission calling on EU members to clamp down on such schemes, in great part because of security concerns, especially since Russia's invasion of Ukraine.\n\nIn 2022, the UK government ended a scheme allowing wealthy foreign nationals to settle in the country if they brought assets with them.\n\nThe following year, Ireland scrapped its Golden Visa, while Portugal revised its own version of it, no longer allowing residency in exchange for property purchases."
        if st.button("I selected an article, typed in the worker id.", key='first'):
            # 説明してもらう文章
            texts = [exampletexts1, exampletexts2, exampletexts3, exampletexts4]
            st.session_state.exampletexts = texts[st.session_state.kiji]
            # 導入文
            st.session_state.assistant1 = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant.\nPlease follow the instructions, referring to the following news articles\n\n##news article##\n" + st.session_state.exampletexts
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
                for i in range(3):
                    if "**questioner:** " in st.session_state.question[i].text:
                        st.session_state.question[i].text = st.session_state.question[i].text.replace("**questioner:** ", "")
                st.session_state.kijistate = False
            with open(f'logs/log{st.session_state.worker}.txt', mode='w')as f:
                print(f"""{{"選ばれた記事": "{st.session_state.kiji}","質問候補":[""", file=f)


def notinitfn():
    kijisentaku.markdown(st.session_state.kijitext)


if st.session_state.kijistate:
    initfn()
else:
    notinitfn()

end_placeholder = st.empty()

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
        with open(f'logs/log{st.session_state.worker}.txt', mode='a')as f:
            print(f"""{{"現在のユーザの理解度":"{user_score}", "質問候補1":"{st.session_state.question[0].text}", "難易度1": "{st.session_state.question[0].score}", "質問候補2":"{st.session_state.question[1].text}", "難易度2": "{st.session_state.question[1].score}","質問候補3":"{st.session_state.question[2].text}", "難易度3": "{st.session_state.question[2].score}", "選ばれた質問":"{st.session_state.question[i].text}", "難易度":"{st.session_state.question[i].score}"}}, """, file=f)
        with st.chat_message("user"):
            st.markdown(choices[i])
        with st.chat_message("assistant"):
            message = [
                {
                    "role": "system",
                    "content": "==instruction==\nGiven a news the history of the dialogue between the commentator and the questioner about the content of the news article as input, please create a two-sentence statement by the commentator following the dialogue. The content should be an answer to the question and additional information that introduces next main points of the news article.\n\n==Input example==\n##news article##\nResearchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard.\n\n##dialogue about news article content##\n**commentator:** Artificial intelligence is now playing a crucial role in managing and preventing power outages as demand for electricity surges globally.\n\n**questioner:** What role is AI playing in the management of electricity grids according?\n\n**commentator:**  AI is being used to predict electricity supply and demand, helping to optimize when batteries should charge and discharge. Additionally, AI helps in detecting infrastructural damage and potential hazards like animal intrusions that could lead to power outages.\n\n**questioner:** Can you elaborate on how AI predicts electricity supply and demand specifically and how this information helps manage battery storage systems?\n\n==Output example==\nAI utilizes advanced algorithms and machine learning to analyze historical data and real-time inputs from various sources, such as weather patterns, consumer behavior, and energy production rates. This predictive capability allows grid operators to anticipate periods of high demand or low supply, strategically managing battery storage to either store excess energy during low demand or release energy during peak times, thus maintaining grid stability and efficiency."
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
        if len(st.session_state.messages) > 7:
            st.session_state.end = True
        # 質問生成
        st.session_state.question = create_question_en.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, user_score)
        for i in range(3):
            if "**questioner:** " in st.session_state.question[i].text:
                st.session_state.question[i].text = st.session_state.question[i].text.replace("**questioner:** ", "")


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
        with open(f'logs/log{st.session_state.worker}.txt', mode='a')as f:
            print(f"""{{"現在のユーザの理解度":"{user_score}", "質問候補1":"{st.session_state.question[0].text}", "難易度1": "{st.session_state.question[0].score}", "質問候補2":"{st.session_state.question[1].text}, "難易度2":"{st.session_state.question[1].score}","質問候補3":"{st.session_state.question[2].text}", "難易度3": "{st.session_state.question[2].score}", "選ばれた質問":"{st.session_state.user_input}", "難易度":"-"}}, """, file=f)
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            message = [
                {
                    "role": "system",
                    "content": "==instruction==\nGiven a news the history of the dialogue between the commentator and the questioner about the content of the news article as input, please create a two-sentence statement by the commentator following the dialogue. The content should be an answer to the question and additional information that introduces next main points of the news article.\n\n==Input example==\n##news article##\nResearchers have discovered the cause of the brightest burst of light ever recorded.\n\nBut in doing so they have run up against two bigger mysteries, including one that casts doubt on where our heavy elements - like gold - come from.\n\nThe burst of light, spotted in 2022, is now known to have had an exploding star at its heart, researchers say.\n\nBut that explosion, by itself, would not have been sufficient to have shone so brightly.\n\nAnd our current theory says that some exploding stars, known as supernovas, might also produce the heavy elements in the universe such as gold and platinum.\n\nBut the team found none of these elements, raising new questions about how precious metals are produced.\n\nProf Catherine Heymans of Edinburgh University and Scotland's Astronomer Royal, who is independent of the research team, said that results like these help to drive science forward.\n\n\"The Universe is an amazing, wonderful and surprising place, and I love the way that it throws these conundrums at us!\n\n\"The fact that it is not giving us the answers we want is great, because we can go back to the drawing board and think again and come up with better theories,\" she said.\n\nThe explosion was detected by telescopes in October 2022. It came from a distant galaxy 2.4 billion light-years away, emitting light across all frequencies. But it was especially intense in its gamma rays, which are a more penetrating form of X-rays.\n\nThe gamma ray burst lasted seven minutes and was so powerful that it was off the scale, overwhelming the instruments that detected them. Subsequent readings showed that the burst was 100 times brighter than anything that had ever been recorded before, earning it the nickname among astronomers of the Brightest Of All Time or B.O.A.T.\n\nGamma ray bursts are associated with exploding supernovas, but this was so bright that it could not be easily explained. If it were a supernova, it would have had to have been absolutely enormous, according to the current theory.\n\nThe burst was so bright that it initially dazzled the instruments on Nasa's James Webb Space Telescope (JWST). The telescope had only recently become operational, and this was an incredible stroke of luck for astronomers wanting to study the phenomenon because such powerful explosions are calculated to occur once every 10,000 years.\n\nAs the light dimmed, one of JWST's instruments was able to see there had indeed been a supernova explosion. But it had not been nearly as powerful as they expected. So why then had the burst of gamma rays been off the scale?\n\nDr Peter Blanchard, from Northwestern University in Illinois in the US, who co-led the research team, doesn't know. But he wants to find out. He plans to book more time on JWST to investigate other supernova remnants.\n\n\"It could be that these gamma ray bursts and supernova explosions are not necessarily directly linked to each other and they could be separate processes going on,\" he told BBC News.\n\nDr Tanmoy Laskar, from the University of Utah and co-leader of the study, said that the B.O.A.T's power might be explained by the way in which jets of material were being sprayed out, as normally occurs during supernovas. But if these jets are narrow, they produce a more focused and so brighter beam of light.\n\n\"It's like focusing a flashlight's beam into a narrow column, as opposed to a broad beam that washes across a whole wall,\" he said. \"In fact, this was one of the narrowest jets seen for a gamma ray burst so far, which gives us a hint as to why the afterglow appeared as bright as it did\".\n\nTheory rethink\nBut what about the missing gold?\n\nOne theory is that one of the ways heavy elements - such as gold, platinum, lead and uranium - might be produced is during the extreme conditions that are created during supernovas. These are spread across the galaxy and are used in the formation of planets, which is how, the theory goes, the metals found on Earth arose.\n\nThere is evidence that heavy elements can be produced when dead stars, called neutron stars collide, a process called a kilonovae, but it's thought that not enough could be created this way. The team will investigate other supernova remnants to see if heavy elements still can be produced by exploding stars but only under specific conditions.\n\nBut the researchers found no evidence of heavy elements around the exploded star. So, is the theory wrong and heavy elements are produced some other way, or are they only produced in supernovas under certain conditions?\n\n\"Theorists need to go back and look at why an event like the B.O.A.T is not producing heavy elements when theories and simulations predict that they should,\" says Dr Blanchard.\n\n##dialogue about news article content##\n**commentator:** Artificial intelligence is now playing a crucial role in managing and preventing power outages as demand for electricity surges globally.\n\n**questioner:** What role is AI playing in the management of electricity grids according?\n\n**commentator:**  AI is being used to predict electricity supply and demand, helping to optimize when batteries should charge and discharge. Additionally, AI helps in detecting infrastructural damage and potential hazards like animal intrusions that could lead to power outages.\n\n**questioner:** Can you elaborate on how AI predicts electricity supply and demand specifically and how this information helps manage battery storage systems?\n\n==Output example==\nAI utilizes advanced algorithms and machine learning to analyze historical data and real-time inputs from various sources, such as weather patterns, consumer behavior, and energy production rates. This predictive capability allows grid operators to anticipate periods of high demand or low supply, strategically managing battery storage to either store excess energy during low demand or release energy during peak times, thus maintaining grid stability and efficiency."
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
        if len(st.session_state.messages) > 7:
            st.session_state.end = True
        # 質問生成
        st.session_state.question = create_question_en.create_question("\n".join(st.session_state.dialog), st.session_state.exampletexts, user_score)
        for i in range(3):
            if "**questioner:** " in st.session_state.question[i].text:
                st.session_state.question[i].text = st.session_state.question[i].text.replace("**questioner:** ", "")
        st.session_state.user_input = ""


if len(st.session_state.question) > 2:
    choices = [st.session_state.question[i].text for i in range(3)]
    with button_placeholder.container():
        st.button(choices[0], key='b1', on_click=lambda: click(0))
        st.button(choices[1], key='b2', on_click=lambda: click(1))
        st.button(choices[2], key='b3', on_click=lambda: click(2))
        st.text_input("If you don't see the question you want to ask, please enter it manually here.", on_change=lambda: on_change(), key="user_input")


def finish():
    with open(f'logs/log{st.session_state.worker}.txt', mode='a')as f:
        print(f''']"対話履歴":"{st.session_state.dialog}"}}''', file=f)
    st.session_state.conn.close()
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
    st.session_state.conn = None


if st.session_state.end is True:
    with end_placeholder.container():
        if not st.button("Exit", on_click=lambda: finish(), key='reload'):
            st.stop()
