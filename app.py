from langchain.agents import load_tools, initialize_agent, Tool, AgentType
from langchain.utilities.google_search import GoogleSearchAPIWrapper
from langchain.chat_models import ChatOpenAI

import time
from tqdm import tqdm
import gradio as gr

import os
os.environ["OPENAI_API_KEY"] = "XXXXX"
os.environ["GOOGLE_API_KEY"] = "YYYYY"
os.environ["GOOGLE_CSE_ID"] = "ZZZZ"

from logging import getLogger
logger = getLogger(__name__)


def search_llm(query: str, model_name: str):
  llm = ChatOpenAI(temperature=0, model=model_name)
  google_search = GoogleSearchAPIWrapper()
  search_tools = [Tool(
      name = "Google Search",
      func=google_search.run,
      description="最新の話題について答える場合に利用することができます。また、今日の日付や今日の気温、天気、為替レートなど現在の状況についても確認することができます。入力は検索内容です。"
      ),]
  search_agent = initialize_agent(search_tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
  search_result = search_agent.run(f"{query}")
  return search_result

def app(query: str, model_name: str):
  search_result = search_llm(query, model_name)
  logger.info(search_result)
  return search_result

title : str = "デモアプリ"
description : str = "このデモンストレーションは、Gradio（ユーザーインターフェースのライブラリ）を使用しています"
article : str='''このデモンストレーションは、ユーザーインターフェースを作成するためのPythonのライブラリであるGradioを使用しています。
'''

iface1 = gr.Interface(
    fn=app,
    inputs=[
        gr.Textbox(lines=1, placeholder="query Here"),
        gr.Dropdown(["gpt-3.5-turbo-16k", "gpt-4", "gpt-4-0613"]),
        ],
    outputs=["text"],
    cache_examples=True,
    examples=[
        ["ChatGPTでできること", "gpt-3.5-turbo-16k"],
        ["ChatGPTでできること", "gpt-4-0613"],
        ["日本で一番高い山", "gpt-4-0613"],
    ],
    title=title,
    description=description,
    article=article
    )
iface1.queue()
iface1.launch(debug=True)
