from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class SpecDetailerCrew():
    """SpecDetailerCrew crew for detailing PRD documents"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def qa_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_specialist'], # type: ignore[index]
            verbose=True
        )

    @agent
    def technical_architect(self) -> Agent:
        return Agent(
            config=self.technical_architect_config['technical_architect'] if hasattr(self, 'technical_architect_config') else self.agents_config['technical_architect'], # type: ignore[index]
            verbose=True
        )

    @agent
    def technical_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_architect'], # type: ignore[index]
            verbose=True
        )

    @task
    def user_story_task(self) -> Task:
        return Task(
            config=self.tasks_config['user_story_task'], # type: ignore[index]
        )

    @task
    def edge_case_task(self) -> Task:
        return Task(
            config=self.tasks_config['edge_case_task'], # type: ignore[index]
        )

    @task
    def technical_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_design_task'], # type: ignore[index]
        )

    @task
    def final_spec_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_spec_task'], # type: ignore[index]
            output_file='detailed_prd_document.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SpecDetailerCrew crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
