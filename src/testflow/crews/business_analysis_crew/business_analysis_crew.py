from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class BusinessAnalysisCrew():
    """BusinessAnalysisCrew crew for requirement gathering and BA"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def requirement_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['requirement_collector'], # type: ignore[index]
            verbose=True
        )

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'], # type: ignore[index]
            verbose=True
        )

    @task
    def elicitation_task(self) -> Task:
        return Task(
            config=self.tasks_config['elicitation_task'], # type: ignore[index]
        )

    @task
    def prd_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['prd_generation_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BusinessAnalysisCrew crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
