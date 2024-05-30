import crewai
from crewai import Agent, Task, Crew
import langchain_openai
from langchain_openai import ChatOpenAI
import langchain_groq
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool,ScrapeWebsiteTool, WebsiteSearchTool

#from crewai_tools import SerperDevTool,ScrapeWebsiteTool, WebsiteSearchTool


class CustomCrew:
    def __init__(self, 
                 api_key, 
                 model_name,
                 provider, 
                 all_agents, 
                 crew_agents, 
                 all_tasks, 
                 crew_tasks, 
                 variables, 
                 verbose, 
                 logging_callback=None
                 ):
        self.llm = self.__choose_llm(provider, api_key, model_name)
        self.agents = self.__add_agents(all_agents, crew_agents)
        self.tasks = self.__add_tasks(all_tasks, crew_tasks)
        self.variables = self.__add_variables(variables)
        self.verbose = verbose
        self.logging_callback = logging_callback

    def __choose_llm(self, provider, api_key, model_name):
        if provider.lower() == 'openai':
            return ChatOpenAI(openai_api_key=api_key, model=model_name)
        elif provider.lower() == 'groq':
            return ChatGroq(groq_api_key=api_key, model_name=model_name)

    def __add_agents(self, all_agents, crew_agents):
        agents_objs = []
        for agent_id in crew_agents:
            agent = next((agent for agent in all_agents if agent['id'] == agent_id), None)
            agents_objs .append({
                'id': agent['id'],
                'agent': Agent(
                role=agent['role'],
                goal=agent['goal'],
                backstory=agent['backstory'],
                allow_delegation=agent['allow_delegation'],
                verbose=agent['verbose'], 
                llm=self.llm,
            )})
        return agents_objs 
    
    def __add_tasks(self, all_tasks, crew_tasks):
        tasks_objs = []
        for task_id in crew_tasks:
            task = next((task for task in all_tasks if task['id'] == task_id), None)
            task_agent = next((agent for agent in self.agents if agent['id'] == task['agent_id']), None)
            tools = []
            for tool in task['tools']:
                tool_instance = None
                if tool['id'] == 'serper_dev_tool':
                    tool_instance = SerperDevTool()
                elif tool['id'] == 'scrape_website_tool':
                    tool_instance = ScrapeWebsiteTool(**{param_id: param_value for param in tool['parameters'] for param_id, param_value in param.items()})
                elif tool['id'] == 'website_search_tool':
                    tool_instance = WebsiteSearchTool(**{param_id: param_value for param in tool['parameters'] for param_id, param_value in param.items()})
                tools.append(tool_instance)
            tasks_objs.append(Task(
                description=task['description'],
                expected_output=task['expected_output'],
                agent=task_agent['agent'], 
                tools=tools
            ))
        return tasks_objs
    
    def __add_variables(self, variables):
        return {variable['name']: variable['value'] for variable in variables}
        
    def run(self):
        crew = Crew(
            agents=[agent['agent'] for agent in self.agents],
            tasks=self.tasks,
            verbose=self.verbose, 
            step_callback=self.logging_callback
        )
        results = crew.kickoff(inputs=self.variables)
        return results

