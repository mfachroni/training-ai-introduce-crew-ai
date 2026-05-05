from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class OutputTextAnalyzer(BaseModel):
    insight: str
    indicator: str
    
class SalesReport(BaseModel):
    report : list[OutputTextAnalyzer]

@CrewBase
class FileAnalyzer():
    """FileAnalyzer crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def agent_file_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_file_analyzer'], # type: ignore[index]
            verbose=True,
            tools=[FileReadTool()],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def file_analyzer_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_analyzer_task'], # type: ignore[index]
            output_json = SalesReport
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FileAnalyzer crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
