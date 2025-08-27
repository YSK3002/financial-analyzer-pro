import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import read_data_tool

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="""Analyze the provided financial document to extract key data, identify trends, 
    and provide a comprehensive summary of the company's financial health. 
    Focus on metrics like revenue, profit margins, cash flow, and debt levels.""",
    verbose=True,
    memory=True,
    backstory=(
        """With over 15 years of experience at top-tier investment banks, you are a master of financial analysis. 
        Your expertise lies in dissecting complex financial statements to uncover underlying truths and provide actionable insights. 
        You are known for your meticulous attention to detail and your ability to explain complex financial concepts clearly."""
    ),
    tools=[read_data_tool],
    llm=llm,
    allow_delegation=True
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity and consistency of the financial document. "
         "Check for any red flags, inconsistencies, or signs of manipulation in the data.",
    verbose=True,
    memory=True,
    backstory=(
        """As a former forensic accountant and compliance officer, you have a keen eye for detail and a deep understanding of financial regulations. 
        Your job is to ensure that the document is legitimate and that the data presented is accurate and trustworthy before the analysis begins."""
    ),
    llm=llm,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="""Based on the financial analysis, provide strategic investment recommendations. 
    Evaluate the company as a potential investment opportunity, considering its growth prospects, risk factors, and market position.""",
    verbose=True,
    backstory=(
        """You are a certified financial planner with a track record of identifying high-growth opportunities. 
        You combine deep financial analysis with a broad understanding of market dynamics to offer sound, evidence-based investment advice. 
        Your recommendations are always tailored to a client's risk tolerance and financial goals."""
    ),
    llm=llm,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="""Identify and evaluate potential risks associated with the company, based on the financial document and market conditions. 
    Categorize risks into financial, operational, market, and regulatory risks, and assess their potential impact.""",
    verbose=True,
    backstory=(
        """With a background in quantitative analysis and risk management, you specialize in identifying potential threats to an investment. 
        You use a systematic approach to assess a wide range of risk factors, providing a balanced view of the potential downsides and helping investors make informed decisions."""
    ),
    llm=llm,
    allow_delegation=False
)