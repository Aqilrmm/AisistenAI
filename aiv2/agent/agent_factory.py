import logging
from typing import List, Optional, Dict, Any
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from ..config import OLLAMA_MODEL, OLLAMA_BASE_URL, LLM_TEMPERATURE, LLM_STREAMING
from ..tools.dynamic_tool_loader import get_enabled_tools
from .prompt_templates import REACT_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

def create_agent(tools: Optional[List[Tool]] = None) -> AgentExecutor:
    """
    Membuat agent dengan tools yang diberikan atau menggunakan tools default.
    """
    try:
        llm = OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=LLM_TEMPERATURE,
            streaming=LLM_STREAMING
        )
        if tools is None:
            tools = get_enabled_tools()

        prompt = PromptTemplate(
            template=REACT_PROMPT_TEMPLATE,
            input_variables=["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]
        )

        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        logger.info(f"Agent created with {len(tools)} tools")
        return agent_executor
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise

def run_agent_with_history(agent_executor: AgentExecutor, input_text: str, chat_history: Optional[str] = None) -> Dict[str, Any]:
    """
    Jalankan agen dengan chat history opsional.
    """
    if not chat_history:
        chat_history = "Belum ada riwayat percakapan."

    return agent_executor.invoke({
        "input": input_text,
        "chat_history": chat_history
    })
