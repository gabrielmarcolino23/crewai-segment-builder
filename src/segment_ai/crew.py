from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class SegmentAiCrew():
	"""SegmentAi crew"""

	@agent
	def segment_builder(self) -> Agent:
		llm = LLM(model="gpt-4o", temperature=0.0)
		return Agent(
			config=self.agents_config['segment_builder'],
			verbose=True,
			llm=llm

		)
	
	@task
	def build_segment_task(self) -> Task:
		return Task(
			config=self.tasks_config['build_segment_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SegmentAi crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)