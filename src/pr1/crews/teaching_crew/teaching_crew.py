from typing import List
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class TeachingCrew:
    def __init__(self, topic: str):
        self.topic = topic

    # 1. Define the agents
    @agent
    def hasnain_ali(self) -> Agent:
        return Agent(
            role="Hasnain Ali",
            goal=f"You are a teaching assistant who is teaching a class about {self.topic}.",
            backstory=f"You are a teaching assistant who is teaching a class about {self.topic}.",
            verbose=True,
        )

    # 2. Define the tasks
    @task
    def describe_topic(self) -> Task:
        return Task(
            description=f"You are a teaching assistant who is teaching a class about {self.topic}.",
            expected_output=f"The students will have mastered the topic: {self.topic}.",
            agent=self.hasnain_ali(),  # Calling the method to return an agent instance
            verbose=True,
        )

    # 3. Define the crew
    @crew
    def get_crew(self) -> Crew:
        return Crew(
            agents=[self.hasnain_ali()],  # Calling the method to return an agent instance
            tasks=[self.describe_topic()],  # Calling the method to return a task instance
            verbose=True,
        )
