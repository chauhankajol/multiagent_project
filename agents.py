
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools_agent import web_search, scaraper_content
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ============================================================
# 1st AGENT - SEARCH AGENT
# ============================================================

def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search]
    )


# ============================================================
# 2nd AGENT - READER / SCRAPER AGENT
# ============================================================

def build_read_agent():

    return create_agent(
        model=llm,
        tools=[scaraper_content]
    )


# ============================================================
# WRITER CHAIN
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert research writer.

Write clear, insightful, structured, factual and professional
research reports.
"""
    ),

    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings
  - Minimum 3 well-explained points
- Conclusion
- Sources
  - List all URLs found in the search results

Be detailed, factual and professional.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ============================================================
# CRITIC CHAIN
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a sharp and constructive research critic.
Be honest, specific and strict while evaluating the report.
"""
    ),

    (
        "human",
        """
Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()

