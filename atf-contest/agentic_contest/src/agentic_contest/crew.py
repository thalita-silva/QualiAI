from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CodeInterpreterTool
from tools.custom_tool import DatabricksSQLTool
import os

@CrewBase
class AtfContest():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    def __init__(self,inputs):
        self.databricks_tool = DatabricksSQLTool(
                host=inputs["HOST"],
                token=inputs["TOKEN"],
                warehouse_id=inputs["WAREHOUSEID"]
            )   
    @agent
    def kpi_analyst(self) -> Agent:
        return Agent(config=self.agents_config['kpi_analyst'], verbose=True)

    @agent
    def m_data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['m_data_analyst'],
            tools=[self.databricks_tool,CodeInterpreterTool()],
            verbose=True
        )

    @agent
    def data_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['data_engineer'],
            tools=[self.databricks_tool,CodeInterpreterTool()],
            verbose=True
        )

    @task
    def t_interpret_input(self) -> Task:
        return Task(config=self.tasks_config['t_interpret_input'])

    @task
    def t_map_primary_metrics(self) -> Task:
        return Task(config=self.tasks_config['t_map_primary_metrics'])

    @task
    def t_define_metrics(self) -> Task:
        return Task(config=self.tasks_config['t_define_metrics'])
    @task
    def t_prepare_discovery_queries(self) -> Task:
        return Task(config=self.tasks_config['t_prepare_discovery_queries'])



    @task
    def t_discover_tables(self) -> Task:
        return Task(
            config=self.tasks_config['t_discover_tables'],
            tools=[self.databricks_tool,CodeInterpreterTool()]  
        )
    @task
    def t_list_candidate_tables(self) -> Task:
        return Task(
            config=self.tasks_config['t_list_candidate_tables'],
            tools=[self.databricks_tool,CodeInterpreterTool()]  
        )
    @task
    def t_mapping_result(self) -> Task:
        return Task(config=self.tasks_config['t_mapping_result'])


    @task
    def t_define_query(self) -> Task:
        return Task(
            config=self.tasks_config['t_define_query'],
            tools=[CodeInterpreterTool()]  
        )

    @task
    def t_execute_query(self) -> Task:
        return Task(
            config=self.tasks_config['t_execute_query'],
            tools=[self.databricks_tool]  
        )

    @task
    def t_troubleshoot_query(self) -> Task:
        return Task(
            config=self.tasks_config['t_troubleshoot_query'],
            tools=[self.databricks_tool]
        )
    @task
    def t_troubleshoot_metric(self) -> Task:
        return Task(config=self.tasks_config['t_troubleshoot_metric'])

    @task
    def t_retry_troubleshoot_metric(self) -> Task:
        return Task(
            config=self.tasks_config['t_retry_troubleshoot_metric'],
            tools=[self.databricks_tool]
        )

    @task
    def t_final_result_de(self) -> Task:
        return Task(config=self.tasks_config['t_final_result_de'])

    @task
    def t_final_result_da(self) -> Task:
        return Task(
            config=self.tasks_config['t_final_result_da'],
            tools=[CodeInterpreterTool()]  
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.kpi_analyst(),
                self.m_data_analyst(),
                self.data_engineer()
            ],
            tasks=[
                self.t_interpret_input(),
                self.t_map_primary_metrics(),
                self.t_define_metrics(),
                self.t_prepare_discovery_queries(),
                self.t_list_candidate_tables(),
                self.t_discover_tables(),
                self.t_mapping_result(),
                self.t_define_query(),
                self.t_execute_query(),
                self.t_troubleshoot_query(),
                self.t_troubleshoot_metric(),
                self.t_retry_troubleshoot_metric(),
                self.t_final_result_de(),
                self.t_final_result_da()
            ],
            process=Process.sequential,
            verbose=True
    )

