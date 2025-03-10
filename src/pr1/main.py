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
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📚 Welcome to Hasnain's Agentia World</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🌟 An AI Powered Teacher </h2>", unsafe_allow_html=True)
suggested_queries = [
    "Agentic AI",
    "Generative AI",
    "Machine Learning",
    "Medical Science",
    "Finance",
]

st.write("### Suggested Topics:")
for query in suggested_queries:
    st.write(f"- {query}")
user_input = st.text_input("🖋️ Enter your topic")

if st.button("✨ Generate Content"):
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













st.sidebar.title("Description:")
st.sidebar.info(
    """
    🎓 Welcome to Hasnain's Teaching Assistant – an AI-powered content generator designed to simplify learning material creation. 
    
    This intelligent assistant leverages **Crew AI with Gemini Flash 2.0** to generate well-structured educational content based on your topic.
    
    🔹 **How It Works:**
    
    1️⃣ **Enter a Topic** – Provide a subject or concept for content generation.  
    2️⃣ **AI-Powered Content Generation** – The system processes your request with specialized AI agents:  
        
        ✍️ **Content Creator Agent** – Generates structured educational material.  
        🧐 **Content Reviewer Agent** – Enhances clarity and coherence.  
    
    3️⃣ **Instant Output & Download** – View the content instantly and download it as a **TXT file** for further use.
    
    🚀 **Features:**
    
    ✅ Generates structured learning content (titles, modules, bullet points)  
    ✅ Supports diverse topics across multiple domains  
    ✅ AI-assisted quality review for clear and concise content  
    ✅ Quick topic suggestions for inspiration  
    ✅ One-click download as a **TXT file** 📥  
    
    Start creating high-quality educational content with AI! 🚀
    """
)



st.sidebar.markdown("### Connect with Hasnain")
st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/hasnain-ali-developer/)")
st.sidebar.write("[GitHub](https://github.com/HasnainCodeHub)")
st.sidebar.write("[Instagram](https://www.instagram.com/i_hasnainaliofficial/)")
st.sidebar.write("[Facebook](https://www.facebook.com/hasnainazeem.hasnainazeem.1)")









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
