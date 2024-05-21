import streamlit as st
import warnings
import crewai
import os
import langchain_openai
from langchain_openai import OpenAI

from crewai import Agent, Task, Crew
import utils
warnings.filterwarnings("ignore")

if not os.environ.get("OPENAI_API_KEY"):
    st.sidebar.warning('Please add your OpenAI API key to environment variables.')
    OPENAI_API_KEY=st.sidebar.text_input('Enter your OpenAI API key', type='password')
else:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


models = utils.load_json('data/models.json')["models"]
name_to_model = {model["name"]: model["model"] for model in models}
selected_model_name = st.sidebar.selectbox('Select a model', list(name_to_model.keys()))
selected_model = name_to_model[selected_model_name]

llm=OpenAI(api_key=OPENAI_API_KEY, model_name=selected_model)


#st.write('Selected model:', model)