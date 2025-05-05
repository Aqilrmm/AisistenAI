#################################################
# agent/agent_factory.py
#################################################

import logging
from typing import List, Optional
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from ..config import OLLAMA_MODEL, OLLAMA_BASE_URL, LLM_TEMPERATURE, LLM_STREAMING
from ..tools.dynamic_tool_loader import get_enabled_tools
from .prompt_templates import PREFIX_TEMPLATE, SUFFIX_TEMPLATE

logger = logging.getLogger(__name__)

def create_agent(tools: Optional[List[Tool]] = None):
    """
    Membuat agent dengan tools yang diberikan atau menggunakan tools default
    """
    try:
        # Inisialisasi LLM
        llm = OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=LLM_TEMPERATURE,
            streaming=LLM_STREAMING
        )
        
        # Dapatkan tools jika tidak ada yang diberikan
        if tools is None:
            tools = get_enabled_tools()
            
        # Inisialisasi agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            agent_kwargs={
                "prefix": PREFIX_TEMPLATE,
                "suffix": SUFFIX_TEMPLATE,
                "input_variables": ["input", "agent_scratchpad"]
            }
        )
        
        logger.info(f"Agent created with {len(tools)} tools")
        return agent
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise