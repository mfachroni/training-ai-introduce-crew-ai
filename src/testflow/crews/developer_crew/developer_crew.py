from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class DeveloperCrew():
    """DeveloperCrew crew for generating detailed technical documents"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['system_architect'], # type: ignore[index]
            verbose=True
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'], # type: ignore[index]
            verbose=True
        )

    @task
    def architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['architecture_task'], # type: ignore[index]
        )

    @task
    def api_spec_task(self) -> Task:
        return Task(
            config=self.tasks_config['api_spec_task'], # type: ignore[index]
        )

    @task
    def frontend_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_plan_task'], # type: ignore[index]
        )

    @task
    def technical_doc_consolidation_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_doc_consolidation_task'], # type: ignore[index]
            output_file='detailed_technical_doc.md'
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
