from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm_config import get_llm

class DiagramAgent:
    def __init__(self, api_key):
        self.llm = get_llm(api_key)

    def generate_diagram(self, requirements):
        system_prompt = """
        You are a Senior System Architect.
        Based on the requirements, generate a System Architecture Diagram using Graphviz DOT syntax.
        
        Rules:
        1. Start the code with 'digraph G {{' and end with '}}'.
        2. Use 'rankdir=LR;' for Left-to-Right layout.
        3. Use simple node attributes: [shape=box, style=filled, fillcolor="#f0f0f0", fontname="Helvetica"].
        4. Define nodes first, then relationships.
        5. Do NOT use complex attributes or HTML labels. Keep it simple.
        6. Return ONLY the DOT code. No markdown ticks.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Requirements:\n{requirements}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        result = chain.invoke({"requirements": requirements})
        
        # Clean up output
        result = result.replace("```dot", "").replace("```graphviz", "").replace("```", "").strip()
        return result