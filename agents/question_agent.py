from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm_config import get_llm

class QuestionAgent:
    def __init__(self, api_key):
        self.llm = get_llm(api_key)

    def generate_questions(self, gaps):
        print("Question Agent: Formulating clarifying questions...")
        
        system_prompt = """
        You are a Client Consultant.
        Based on the identified Gaps & Risks, formulate professional, polite, and technical follow-up questions to ask the client.
        No need to ask questions in cases where already everything is clearly specified.
        
        Output Format: A list of questions in Markdown.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Identified Gaps:\n{gaps}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"gaps": gaps})
        return result