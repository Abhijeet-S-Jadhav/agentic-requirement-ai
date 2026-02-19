from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm_config import get_llm

class AmbiguityAgent:
    def __init__(self, api_key):
        self.llm = get_llm(api_key)

    def analyze_gaps(self, transcript, requirements):
        print("Ambiguity Agent: Detecting risks and missing info...")
        
        system_prompt = """
        You are a QA Lead and Risk Analyst.
        Review the Transcript and the Extracted Requirements.
        
        Your Goal: Identify vague, ambiguous, or missing requirements that could cause project failure.
        Look for phrases like "I think", "maybe", "sort of", or technical gaps (e.g., missing security specs, unspecified scale).
        
        Output Format: A bulleted list of "Gaps & Risks".
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "TRANSCRIPT:\n{transcript}\n\nEXTRACTED REQ:\n{requirements}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"transcript": transcript, "requirements": requirements})
        return result