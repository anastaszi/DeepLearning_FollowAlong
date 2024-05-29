import json
import uuid

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    return None

### UI UTILS ###
def fill_example_data(session_data):
    research_agents = load_json('data/research_example.json')["agents"]
    research_tasks = load_json('data/research_example.json')["tasks"]
    research_variables = load_json('data/research_example.json')["variables"]
    if research_agents and isinstance(research_agents, list) and len(research_agents) > 0:
        session_data.agents = research_agents
        session_data.warnings['no_agents'] = False
    if research_tasks and isinstance(research_tasks, list) and len(research_tasks) > 0:
        session_data.tasks = research_tasks
        session_data.warnings['no_tasks'] = False
    if research_variables and isinstance(research_variables, list) and len(research_variables) > 0:
        session_data.variables = research_variables
## AGENT UTILS ##

def add_agent(index, agents, warnings):
    agents.append({
        'id': str(uuid.uuid4()), # Add a unique id to each agent
        'name': f'Agent {index + 1}',
        'role': '',
        'backstory': '',
        'goal': '',
        'allow_delegation': True,
        'verbose': True
    })
    warnings['no_agents'] = False

def remove_agent(index, agents):
    agents.pop(index)

def attach_agents(agents, crew, warnings):
    if not agents or list(agents) == []:
        warnings['no_agents'] = True
        return
    crew['agents'].append(agents[0]['name'])

def deattach_agent(index, crew):
    crew['agents'].pop(index)

## TASK UTILS ##

def add_tasks(index, tasks, warnings):
    tasks.append({
        'id': str(uuid.uuid4()),
        'name': f'Task {index + 1}',
        'description': '',
        'expected_output': '',
        'agent_id': '',
        'tools': []
    })
    warnings['no_tasks'] = False

def remove_task(index, tasks):
    tasks.pop(index)  

def attach_tasks(tasks, crew, warnings):
    if not tasks or list(tasks) == []:
        warnings['no_tasks'] = True
        return
    crew['tasks'].append(tasks[0]['name'])


def deattach_task(index, crew):
    crew['tasks'].pop(index)

## VARIABLE UTILS ##
def add_variable(variables):
    variables.append({
        'name': '',
        'value': ''
    })

def remove_variable(index, variables):
    variables.pop(index)