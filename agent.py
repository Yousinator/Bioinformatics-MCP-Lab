import os
import asyncio
from typing import List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession
from mcp.client.sse import sse_client
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# STUDENT TASK: COMPLETE THE SYSTEM PROMPT
# Add clinical guidelines, safety rules, and persona here.
# ==========================================================
SYSTEM_PROMPT = """
You are a Clinical AI Assistant. 

TOOL USAGE RULES:
- ONLY call a tool if the user's request explicitly requires data from that tool.
- For general greetings (e.g., "Hello", "Hi"), do NOT call any tools. Just respond politely.
- Do not call get_patient_history unless a patient ID (P001, P002, P003) is actually provided.
- If the user's question is general and doesn't need real-time data, answer without tools.
- Do not "hallucinate" tool calls or call them unnecessarily.

AVAILABLE TOOLS AND WHEN TO USE THEM:
1. get_patient_history(patient_id): Fetch records for P001, P002, or P003.
2. book_appointment(patient_id, date, time, department): Schedule visits.
3. get_available_departments(): List hospital departments.
4. lookup_drug_info(drug_name): Real-time FDA data on purpose and warnings.
5. check_drug_interactions(drug_names): NIH RxNorm check for drug pairs.
6. search_medical_literature(query): PubMed search for evidence-based papers.
7. search_medical_knowledge(query): Fast local guideline lookup.

STUDENT GUIDELINES START HERE:
(Add your safety rules, emergency protocols, and instructions below)
"""

class MedicalAgent:
    def __init__(self, groq_api_key: str, langfuse_public_key: str = None, langfuse_secret_key: str = None, langfuse_host: str = None):
        self.groq_api_key = groq_api_key
        
        # CHANGED: Using Llama 3.3 70B for superior clinical reasoning and tool use
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=groq_api_key,
            temperature=0
        )

        self.langfuse_handler = None
        if langfuse_public_key and langfuse_secret_key:
            os.environ["LANGFUSE_PUBLIC_KEY"] = langfuse_public_key
            os.environ["LANGFUSE_SECRET_KEY"] = langfuse_secret_key
            if langfuse_host:
                os.environ["LANGFUSE_HOST"] = langfuse_host
            self.langfuse_handler = CallbackHandler()

        # CHANGED: Points to the Central Lab Server via ngrok
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "REPLACE_WITH_INSTRUCTOR_NGROK_URL")

    async def run_query(self, user_input: str, chat_history: List = None):
        if chat_history is None:
            chat_history = []

        try:
            async with sse_client(self.mcp_server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await load_mcp_tools(session)

                    messages = [SystemMessage(content=SYSTEM_PROMPT)]
                    for msg in chat_history:
                        messages.append(msg)
                    messages.append(HumanMessage(content=user_input))

                    agent = create_react_agent(self.llm, tools)

                    config = {}
                    if self.langfuse_handler:
                        config["callbacks"] = [self.langfuse_handler]

                    result = await agent.ainvoke({"messages": messages}, config=config)

                    final_message = result["messages"][-1]
                    return final_message.content

        except (Exception, BaseExceptionGroup) as e:
            error_msg = str(e)
            return f"Error connecting to Central Lab Server: {error_msg}"
