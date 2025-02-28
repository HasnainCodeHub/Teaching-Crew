from dotenv import load_dotenv,find_dotenv 
from typing import List
from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
_: bool = load_dotenv(find_dotenv())

@CrewBase
class TeachingCrew:
    def __init__(self, topic: str):
        self.topic = topic

    # 1. Define the agents
    @agent
    def Expert_Teacher(self) -> Agent:
        return Agent(
            role="Expert_Teacher",
            goal=f"""
            You are a Expert Teacher who is teaching a class about {self.topic}.
            You have 20 Years Of Experience In Teaching Any Topic.

                  
            
                """,
            backstory=f"You are a teaching assistant who is teaching a class about {self.topic}. In A professiona;l",
            verbose=True,
        )

    # 2. Define the tasks
    @task
    def describe_topic(self) -> Task:
        return Task(
            description=f"""
            You are a teaching assistant who is teaching a class about {self.topic}.
            You need to describe the topic to the students in a way that they can understand it easily.

            """,
            expected_output=f"The students will have mastered the topic: {self.topic}.",
            agent=self.Expert_Teacher(),  # Calling the method to return an agent instance
            verbose=True,
        )

    # 3. Define the crew
    @crew
    def get_crew(self) -> Crew:
        return Crew(
            agents=[self.Expert_Teacher()],  # Calling the method to return an agent instance
            tasks=[self.describe_topic()],  # Calling the method to return a task instance
            verbose=True,
        )



import streamlit as st
import os

# User input



# 🌟 App Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📚 Welcome to Teaching Assistant</h1>", unsafe_allow_html=True)

user_input = st.text_input("🖋️ Enter your topic")

if st.button("✨ Generate Topic"):
    if not user_input.strip():
        st.error("⚠️ Please enter a valid topic.")
    else:
        st.success(f"📝 Generating Content for **{user_input}**")

        with st.spinner("⏳ Generating Content..."):
            try:
                # Fetch response
                result = TeachingCrew(user_input).get_crew().kickoff()
                response = result.raw

                if not response:
                    st.error("❌ No content generated. Try a different topic.")
                else:
                    # 🖊️ Display Content
                    st.subheader("📜 Generated Content")
                    st.write(response)

                    file_name = "content.txt"

                    try:
                        # ✅ Format Content & Save as TXT
                        with open(file_name, "w", encoding="utf-8") as f:
                            for line in response.split("\n"):
                                if line.startswith("# "):
                                    f.write(f"\n📖 {line[2:]}\n" + "=" * 40 + "\n")
                                elif line.startswith("## "):
                                    f.write(f"\n🔹 {line[3:]}\n" + "-" * 30 + "\n")
                                elif line.startswith("### "):
                                    f.write(f"\n🔸 {line[4:]}\n")
                                elif line.startswith("* "):
                                    f.write(f"   ➤ {line[2:]}\n")
                                elif line.startswith("    * "):
                                    f.write(f"      - {line[6:]}\n")
                                else:
                                    f.write(line + "\n")

                        # ✅ Download Button
                        with open(file_name, "rb") as f:
                            st.download_button(
                                label="📥 Download Content as TXT",
                                data=f,
                                file_name=file_name,
                                mime="text/plain",
                            )

                    except Exception as e:
                        st.error(f"⚠️ Error while saving the TXT file: {e}")

                    finally:
                        # Cleanup file after download
                        if os.path.exists(file_name):
                            os.remove(file_name)

            except Exception as e:
                st.error(f"🚨 Error generating content: {e}")























# For CLI
# from crewai.flow.flow import Flow ,start,listen
# from litellm import completion 

# from pr1.crews.teaching_crew.teaching_crew import TeachingCrew







# class AgenticFlow(Flow):

#     @start()
#     def generate_topic(self):
#         response = completion(
#             model="gemini/gemini-2.0-flash-exp",
#             messages=[
#                 {
#                     "role":"user",
#                     "content":"""
#                     Share The Most trending Topic for 2025 In AI World No need to give any other information just the topic.
#                     """
#                 }
#             ],
#             max_tokens=100,
#             temperature=0.5
#         )
#         self.state["topic"] = response["choices"][0]["message"]["content"]
#         print(f"Step 1 Generated Topic: {self.state['topic']}")




#     @listen(generate_topic)
#     def generate_content(self):
#         print("Generating Content")
#         result = TeachingCrew(topic=self.state["topic"]).get_crew().kickoff()
#         print(result.raw)
#         self.state["content"] = result.raw


#     @listen(generate_content)
#     def save_as_file(self):
#         with open("content.md", "w") as f:
#             f.write(self.state["content"])
#         print("Content Saved")

# # def kickoff():
# #     flow = AgenticFlow()
# #     flow.kickoff()


# For Streamlit
