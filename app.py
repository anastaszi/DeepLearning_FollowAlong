import streamlit as st
import warnings
from utils.ui_utils import load_json, add_agent, add_tasks, remove_agent, remove_task, add_variable, remove_variable, fill_example_data, attach_agents, attach_tasks, deattach_agent, deattach_task
from utils.crew_utils import compile_crew

warnings.filterwarnings("ignore")

## Session state
if 'agents' not in st.session_state or 'tasks' not in st.session_state:
    st.session_state.agents = []
    st.session_state.tasks = []
    st.session_state.crew = {
        'agents': [],
        'tasks': [],
        'verbose': 2
    }
    st.session_state.variables = []
    st.session_state.warnings = {
        'no_agents': False,
        'no_tasks': False, 
        'crew': None
    }
    st.session_state.api_key = ''
    st.session_state.selected_model_name = ''

models = load_json('data/models.json')["models"]

name_to_model = {model["name"]: model["model"] for model in models}
agent_options = [(agent['id'], agent['name']) for agent in st.session_state.agents]
task_options = [(task['id'], task['name']) for task in st.session_state.tasks]


#### UI ####

## Sidebar
with st.sidebar:
    if not st.session_state.api_key:
        if not st.secrets:
            st.session_state.api_key=st.text_input('Enter your OpenAI API key', type='password')
        elif st.secrets["SCOPE"]=='local' and st.secrets["OPENAI_API_KEY"]:
            st.session_state.api_key=st.secrets["OPENAI_API_KEY"]
        else:
            st.write('You can use your own OpenAI API key')
            st.session_state.api_key=st.text_input('Enter your OpenAI API key', type='password')
            st.write("Unless you know a magic word")
            pwd = st.text_input('Enter your password', type='password', label_visibility="collapsed")
            if pwd and pwd == st.secrets["PASSWORD"]:
                st.session_state.api_key = st.secrets["OPENAI_API_KEY"]
            if pwd and pwd != st.secrets["PASSWORD"]:
                st.warning('Wrong password')
        st.warning('Please provide your OpenAI API key')
        st.stop()
    selected_model_name = st.selectbox('Select a model', list(name_to_model.keys()))
    st.session_state.selected_model_name = name_to_model[selected_model_name]
    st.divider()
    st.subheader('Research Example')
    st.button('Fill example data', on_click=fill_example_data, args=(st.session_state,))
## Main content
tab1, tab2, tab3, tab4 = st.tabs(["Crew", "Agents", "Tasks", "Variables"])

with tab1:
    st.header('Crew', divider='rainbow')
    st.write('A crew is a group of agents and tasks that work together to achieve a common goal. It has a verbosity level that determines the amount of information displayed during the crew\'s operation.')
    crew_expander = st.expander('Code example', expanded=False)
    crew_expander.code('''
        agent1 = Agent(
            role="Content Planner",
            goal="Plan engaging and factually accurate content on {topic}",
            backstory="You're working on planning a blog article"
            ...
        task1 = Task(
            description="1. Prioritize the latest trends, key players in the {industry} "
            expected_output="A comprehensive content plan document"
            ...
        )
        crew=Crew(
            agents=[agent1, agent2, agent3],
            tasks=[task1, task2, task3],
            ...
        )
        result = crew.kickoff(inputs={"topic":"AI", "industry": "Tech"}) 
        '''
    )
    st.info('Tasks will be performed sequentially (i.e they are dependent on each other), so the order of the task in the list matters.', icon="ℹ️")

    c1,c2,c3 = st.columns([2,2,1])
    with c1:
        st.caption('Agents')
        for i, agent_id in enumerate(st.session_state.crew['agents']):
                c11, c12 = st.columns([2, 1])
                # Find the index of the current agent ID in agent_options
                selected_agent_index = next((index for index, (id, _) in enumerate(agent_options) if id == agent_id), 0)
                with c11:
                    selected_agent = st.selectbox(
                        'Select an agent',
                        options=agent_options,
                        format_func=lambda x: x[1],
                        index=selected_agent_index,
                        key=f"crew_agent_{i}",
                        label_visibility="collapsed"
                    )
                with c12: 
                    st.button('🗑️', on_click=deattach_agent, args=(i,st.session_state.crew), key=f"deattach_agent_{i}")
                st.session_state.crew['agents'][i] = selected_agent[0]
        if st.session_state.warnings['no_agents']:
            st.warning('You have no agents yet')
        st.button("Attach agents", on_click=attach_agents, key="attach_agents", args=(st.session_state.agents, st.session_state.crew, st.session_state.warnings,))
    with c2:
        st.caption('Tasks')
        for i, task_id in enumerate(st.session_state.crew['tasks']):
                c21, c22 = st.columns([2, 1])
                # Find the index of the current agent ID in agent_options
                selected_tasks_index = next((index for index, (id, _) in enumerate(task_options) if id == task_id), 0)
                with c21:
                    selected_task = st.selectbox(
                        'Select a task',
                        options=task_options,
                        format_func=lambda x: x[1],
                        index=selected_tasks_index,
                        key=f"crew_task_{i}",
                        label_visibility="collapsed"
                    )
                with c22:
                    st.button('🗑️', on_click=deattach_task, args=(i,st.session_state.crew,), key=f"deattach_task_{i}")
                st.session_state.crew['tasks'][i] = selected_task[0]
        if st.session_state.warnings['no_tasks']:
            st.warning('You have no tasks yet')
        st.button("Attach tasks", on_click=attach_tasks, key="attach_tasks", args=(st.session_state.tasks, st.session_state.crew, st.session_state.warnings,))
    with c3:
        st.caption('Verbose')
        st.session_state.crew['verbose'] = st.slider('Select a level of logging', 0, 2, 2)

    st.button('Run crew', on_click=compile_crew, args=(st.session_state, ))
    if st.session_state.warnings['crew']:
        st.warning(st.session_state.warnings['crew'])
    if 'results' in st.session_state:
        st.header('Results', divider='rainbow')
        st.markdown(st.session_state.results)

with tab2:
    st.header('Agents', divider='rainbow')
    st.write('Agents are the entities that perform tasks in a crew. They have roles, goals, and backstories that help them understand their tasks and responsibilities.')
    agent_expander = st.expander('Code example', expanded=False)
    agent_expander.code(
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
            st.button('➖ Remove agent', on_click=remove_agent, args=(i,st.session_state.agents, ), key=f"remove_{i}")
    
    st.button('➕ Add agent', on_click=add_agent, args=(len(st.session_state.agents),st.session_state.agents, st.session_state.warnings, ))

with tab3:
    st.header('Tasks', divider='rainbow')
    st.write('Tasks are the activities that agents perform to achieve their goals. They have descriptions, expected outputs, and are assigned to agents.')
    task_expander = st.expander('Code example', expanded=False)
    task_expander.code(
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
            selected_agent_index = next((index for index, (agent_id, _) in enumerate(agent_options) if agent_id == task['agent_id']), 0)

            task['agent_id'] = st.selectbox(
                'Select an agent',
                options=agent_options,
                format_func=lambda x: x[1],
                index=selected_agent_index,
                key=f"task_agent_{i}"
            )[0]
            #task['agent_id'] = st.selectbox('Select an agent', [agent['name'] for agent in st.session_state.agents], key=f"task_agent_{i}")
            st.button('➖ Remove task', on_click=remove_task, args=(i,st.session_state.tasks, ), key=f"remove_task_{i}")
    st.button('➕ Add task', on_click=add_tasks, args=(len(st.session_state.tasks),st.session_state.tasks, st.session_state.warnings,))

with tab4:
    st.header('Variables/Inputs', divider='rainbow')
    st.info('This is optional step')
    st.write('Specify any inputs/variables you want to include in tasks or agents. These will allow to reuse the same crew for different scenarios.')
    
    for i, variable in enumerate(st.session_state.variables):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            variable['name'] = st.text_input('Variable name', key=f"variable_name_{i}", value=variable['name'], placeholder="Variable", label_visibility="collapsed")
        with c2:
            variable['value'] = st.text_input('Variable value', key=f"variable_value_{i}", value=variable['value'], placeholder="Value", label_visibility="collapsed")
        with c3:
            st.button('🗑️', on_click=remove_variable, args=(i,st.session_state.variables,), key=f"remove_variable_{i}")
    st.button('➕ Add variable', on_click=add_variable, args=(st.session_state.variables,))