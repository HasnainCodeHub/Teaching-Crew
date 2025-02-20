from crewai.flow.flow import Flow ,start,listen
from litellm import completion 
from dotenv import load_dotenv,find_dotenv

from pr1.crews.teaching_crew.teaching_crew import TeachingCrew





_: bool = load_dotenv(find_dotenv())



class AgenticFlow(Flow):

    @start()
    def generate_topic(self):
        response = completion(
            model="gemini/gemini-2.0-flash-exp",
            messages=[
                {
                    "role":"user",
                    "content":"""
                    Share The Most trending Topic for 2025 In AI World No need to give any other information just the topic.
                    """
                }
            ],
            max_tokens=100,
            temperature=0.5
        )
        self.state["topic"] = response["choices"][0]["message"]["content"]
        print(f"Step 1 Generated Topic: {self.state['topic']}")




    @listen(generate_topic)
    def generate_content(self):
        print("Generating Content")
        result = TeachingCrew(topic=self.state["topic"]).get_crew().kickoff()
        print(result.raw)
        self.state["content"] = result.raw


    @listen(generate_content)
    def save_as_file(self):
        with open("content.md", "w") as f:
            f.write(self.state["content"])
        print("Content Saved")

def kickoff():
    flow = AgenticFlow()
    flow.kickoff()


