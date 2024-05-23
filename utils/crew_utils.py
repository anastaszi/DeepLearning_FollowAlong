import crewai
from crewai import Agent, Task, Crew
import langchain_openai
from langchain_openai import ChatOpenAI


def compile_crew(session_data):
    llm = ChatOpenAI(openai_api_key=session_data.api_key, model=session_data.selected_model_name)
    crew_agents = []
    crew_tasks = []
    for agent_id in session_data.crew['agents']:
        agent = next((agent for agent in session_data.agents if agent['id'] == agent_id), None)
        crew_agents.append({
            'id': agent['id'],
            'agent': Agent(
            role=agent['role'],
            goal=agent['goal'],
            backstory=agent['backstory'],
            allow_delegation=agent['allow_delegation'],
            verbose=agent['verbose'], 
            llm=llm
        )})
    for task_id in session_data.crew['tasks']:
        task = next((task for task in session_data.tasks if task['id'] == task_id), None)
        task_agent = next((agent for agent in crew_agents if agent['id'] == task['agent_id']), None)
        crew_tasks.append(Task(
            description=task['description'],
            expected_output=task['expected_output'],
            agent=task_agent['agent']
        ))
    if len(crew_agents) == 0 or len(crew_tasks) == 0:
        session_data.warnings['crew'] = 'Crew must have at least one agent and one task.'
        return
    session_data.warnings['crew'] = None
    crew = Crew(
        agents=[agent['agent'] for agent in crew_agents],
        tasks=crew_tasks,
        verbose=session_data.crew['verbose']
    )
    session_data.results = crew.kickoff(inputs={variable['name']: variable['value'] for variable in session_data.variables})
    return