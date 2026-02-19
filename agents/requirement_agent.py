from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm_config import get_llm

class RequirementAgent:
    def __init__(self, api_key):
        self.llm = get_llm(api_key)

    def analyze(self, transcript):
        print("Requirement Agent: Extracting structured data...")
        
        # System Prompt: Defines the persona and the output format
        system_prompt = """
        You are an expert Senior Business Analyst. 
        Your task is to analyze a client-vendor conversation transcript and extract a structured Requirement Document.
        
        You must identify:
        1. Project Overview
        2. Business Goals
        3. Functional Requirements
        4. Non-Functional Requirements
        5. Assumptions
        
        Output Format: Markdown.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Here is the transcript:\n\n{transcript}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"transcript": transcript})
        return result