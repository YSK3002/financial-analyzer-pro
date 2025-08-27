from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import read_data_tool

verification_task = Task(
    description="""Verify the provided financial document located at '{file_path}'. 
    Check for data consistency, authenticity, and any immediate red flags. 
    Confirm that it is a valid financial report suitable for detailed analysis.""",
    expected_output="A confirmation report stating whether the document is verified as a legitimate financial statement. "
                    "Include a brief summary of the document type and period covered.",
    agent=verifier,
    async_execution=False
)

analysis_task = Task(
    description="""Using the financial document at '{file_path}', conduct a thorough financial analysis. 
    Extract key financial metrics, such as revenue, net income, gross margin, operating margin, cash flow, and total debt.
    Analyze the user's query: {query} and provide insights based on the document.""",
    expected_output="""A detailed financial analysis report including:
    - A summary of the company's performance for the quarter.
    - Key financial figures and year-over-year comparisons.
    - An assessment of the company's profitability, liquidity, and solvency.""",
    agent=financial_analyst,
    tools=[read_data_tool],
    context=[verification_task],
    async_execution=False,
)

investment_task = Task(
    description="""Based on the detailed financial analysis, formulate an investment recommendation.
    Consider the company's financial health, growth potential, and market position. 
    Provide a clear 'buy', 'hold', or 'sell' recommendation with supporting arguments.""",
    expected_output="""A clear investment recommendation report that includes:
    - The investment thesis (buy/hold/sell).
    - Key reasons supporting the recommendation, based on the financial analysis.
    - A discussion of potential rewards and upsides.""",
    agent=investment_advisor,
    context=[analysis_task],
    async_execution=False
)

risk_assessment_task = Task(
    description="""Conduct a comprehensive risk assessment based on the financial document and analysis.
    Identify potential financial, market, and operational risks. 
    Provide an overview of the key risks and their potential impact on the company.""",
    expected_output="""A structured risk assessment report detailing:
    - A list of key identified risks.
    - The potential impact and likelihood of each risk.
    - A summary of the overall risk profile of the company.""",
    agent=risk_assessor,
    context=[analysis_task],
    async_execution=False
)