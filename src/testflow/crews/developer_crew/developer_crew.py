from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class DeveloperCrew():
    """DeveloperCrew crew for PRD generation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['product_manager'], # type: ignore[index]
            verbose=True
        )

    @agent
    def ux_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['ux_designer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.system_architect_config['system_architect'] if hasattr(self, 'system_architect_config') else self.agents_config['system_architect'], # type: ignore[index]
            verbose=True
        )

    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['system_architect'], # type: ignore[index]
            verbose=True
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
        )

    @task
    def ux_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['ux_design_task'], # type: ignore[index]
        )

    @task
    def technical_spec_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_spec_task'], # type: ignore[index]
        )

    @task
    def prd_compilation_task(self) -> Task:
        return Task(
            config=self.tasks_config['prd_compilation_task'], # type: ignore[index]
            output_file='prd_document.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DeveloperCrew crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
