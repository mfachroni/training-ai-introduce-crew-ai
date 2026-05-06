from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from testflow.tools.tool_prophet import ToolProphet

@CrewBase
class ProphetCrew():
    """ProphetCrew crew for time-series forecasting"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def forecaster_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['forecaster_agent'], # type: ignore[index]
            verbose=True,
            tools=[ToolProphet()]
        )

    @task
    def forecasting_task(self) -> Task:
        return Task(
            config=self.tasks_config['forecasting_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ProphetCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
