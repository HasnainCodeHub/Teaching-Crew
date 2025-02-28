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
from fpdf import FPDF


st.title("Welcome to Teaching Assistant")



import streamlit as st
from fpdf import FPDF
import os

# User input
user_input = st.text_area("Enter your topic", height=150)

if st.button("Generate Topic"):
    if not user_input.strip():  # Check if input is empty or just spaces
        st.error("Please enter a valid topic.")
    else:
        st.write(f"Generating Content for {user_input}")
        with st.spinner("Generating Content..."):
            try:
                # Fetch response
                result = TeachingCrew(user_input).get_crew().kickoff()
                response = result.raw
                
                if not response:  # Ensure response is not empty
                    st.error("No content generated. Please try again with a different topic.")
                else:
                    st.write(response)
                    file_name = "content.pdf"
                    
                    try:
                        # Create PDF instance
                        class PDF(FPDF):
                            def header(self):
                                self.set_font("Arial", "B", 14)
                                self.cell(0, 10, "Generated PDF", ln=True, align="C")
                                self.ln(5)

                        pdf = PDF()
                        pdf.set_auto_page_break(auto=True, margin=15)
                        pdf.add_page()
                        
                        # Set font
                        pdf.set_font("Arial", "", 12)
                        
                        # Proper formatting for structured text
                        for line in response.split("\n"):
                            if line.startswith("# "):  # Title
                                pdf.set_font("Arial", "B", 16)
                                pdf.cell(0, 10, line[2:], ln=True, align="C")
                                pdf.ln(5)
                            elif line.startswith("## "):  # Module
                                pdf.set_font("Arial", "B", 14)
                                pdf.cell(0, 10, line[3:], ln=True)
                                pdf.ln(3)
                            elif line.startswith("### "):  # Section
                                pdf.set_font("Arial", "B", 12)
                                pdf.cell(0, 10, line[4:], ln=True)
                            elif line.startswith("* "):  # Bullet Points
                                pdf.set_font("Arial", "", 12)
                                pdf.cell(10)  # Indentation
                                pdf.multi_cell(0, 10, "- " + line[2:])  # Replace • with -
                            elif line.startswith("    * "):  # Sub-bullet points
                                pdf.set_font("Arial", "", 12)
                                pdf.cell(20)  # More Indentation
                                pdf.multi_cell(0, 10, "  - " + line[6:])  # Replace • with -
                            else:
                                pdf.set_font("Arial", "", 12)
                                pdf.multi_cell(0, 10, line)

                        # Save PDF file
                        pdf.output(file_name, "F")

                        # Read the PDF in binary mode for download
                        with open(file_name, "rb") as f:
                            st.download_button(
                                label="Download Content as PDF",
                                data=f,
                                file_name=file_name,
                                mime="application/pdf",
                            )

                    except Exception as e:
                        st.error(f"An error occurred while generating the PDF: {str(e)}")
                    
                    finally:
                        # Clean up file after download
                        if os.path.exists(file_name):
                            os.remove(file_name)
            
            except Exception as e:
                st.error(f"An error occurred while generating content: {str(e)}")



# up

























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
