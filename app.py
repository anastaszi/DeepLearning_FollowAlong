import streamlit as st
import warnings
import crewai
import os
import langchain_openai
from langchain_openai import OpenAI

from crewai import Agent, Task, Crew
from utils import load_json

warnings.filterwarnings("ignore")

# UI utils
def add_agent():
    st.session_state.agents.append({
        'name': '',
        'role': '',
        'backstory': '',
        'goal': '',
        'allow_delegation': False,
        'verbose': True
    })

def add_tasks():
    st.session_state.tasks.append({
        'name': '',
        'description': '',
        'expected_output': '',
        'agent': ''
    })

def remove_agent(index):
    st.session_state.agents.pop(index)

def remove_task(index):
    st.session_state.tasks.pop(index)  

research_agents = load_json('data/research_example.json')["agents"]
research_tasks = load_json('data/research_example.json')["tasks"]

def fill_example_agents():
    if research_agents and isinstance(research_agents, list) and len(research_agents) > 0:
        st.session_state.agents = research_agents

def fill_example_tasks():
    if research_tasks and isinstance(research_tasks, list) and len(research_tasks) > 0:
        st.session_state.tasks = research_tasks

if 'agents' not in st.session_state:
    st.session_state.agents = []
    st.session_state.tasks = []


if not os.environ.get("OPENAI_API_KEY"):
    st.sidebar.warning('Please add your OpenAI API key to environment variables.')
    OPENAI_API_KEY=st.sidebar.text_input('Enter your OpenAI API key', type='password')
else:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


models = load_json('data/models.json')["models"]

name_to_model = {model["name"]: model["model"] for model in models}
selected_model_name = st.sidebar.selectbox('Select a model', list(name_to_model.keys()))
selected_model = name_to_model[selected_model_name]

if not OPENAI_API_KEY:
   st.sidebar.warning('Please add your OpenAI API key to environment variables.')
   st.stop()

llm=OpenAI(api_key=OPENAI_API_KEY, model_name=selected_model)
with st.sidebar:
    st.divider()
    st.subheader('Research Example')
    st.button('Fill example research agents', on_click=fill_example_agents)
    st.button('Fill example research tasks', on_click=fill_example_tasks)
st.code(
'''
    agent = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article "
                "about the topic: {topic}."
                "You collect information that helps the "
                "audience learn something "
                "and make informed decisions. "
                "Your work is the basis for "
                "the Content Writer to write an article on this topic.,"
        allow_delegation=False,
        verbose=True'''
)



for i, agent in enumerate(st.session_state.agents):
    st.subheader(f"Agent #{i + 1}")
    c1, c2 = st.columns([3, 1])
    with c1:
        agent['name'] = st.text_input('Agent name', key=f"agent_name_{i}", value=agent['name'], placeholder="Agent")
        agent['role'] = st.text_input('Agent role', key=f"role_{i}", value=agent['role'], placeholder="Assistant")
        agent['goal'] = st.text_input('Agent goal', key=f"goal_{i}", value=agent['goal'], placeholder="Help users with their queries" )
        agent['backstory'] = st.text_area('Agent backstory', key=f"backstory_{i}", value=agent['backstory'], placeholder="I am a virtual assistant")
    with c2:
        st.caption('Optional attributes')
        agent['allow_delegation'] = st.checkbox('Allow delegation', key=f"delegation_{i}", value=agent['allow_delegation'])
        agent['verbose'] = st.checkbox('Verbose', key=f"verbose_{i}", value=agent['verbose'])
        st.button('➖ Remove agent', on_click=remove_agent, args=(i,), key=f"remove_{i}")

st.button('➕ Add agent', on_click=add_agent)

st.divider()
st.code(
'''
    task = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
        "and noteworthy news on {topic}."
        "2. Identify the target audience, considering "
        "their interests and pain points."
        "3. Develop a detailed content outline including "
        "an introduction, key points, and a call to action."
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)
'''
)


for i, task in enumerate(st.session_state.tasks):
    st.subheader(f"Task #{i + 1}")
    c1, c2 = st.columns([3, 1])
    with c1:
        task['name'] = st.text_input('Agent name', key=f"task_name_{i}", value=task['name'], placeholder="TaskName")
        task['description'] = st.text_area('Task description', key=f"task_description_{i}", value=task['description'], placeholder="Task description")
        task['expected_output'] = st.text_area('Expected output', key=f"expected_output_{i}", value=task['expected_output'], placeholder="Expected output")
    with c2:
        task['agent'] = st.selectbox('Select an agent', [agent['name'] for agent in st.session_state.agents], key=f"task_agent_{i}")
        st.button('➖ Remove task', on_click=remove_task, args=(i,), key=f"remove_task_{i}")

st.button('➕ Add task', on_click=add_tasks)

# Debug information
st.write(st.session_state.agents)

