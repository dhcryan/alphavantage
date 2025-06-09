import os
import asyncio
from alphavantage_mcp_server.api import fetch_quote
from agents.alphavantage_agent import AlphavantageAgent
from agents.analysis_agent import AnalysisAgent

async def main():
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHAVANTAGE_API_KEY is not set in the environment variables.")

    alphavantage_agent = AlphavantageAgent(api_key)
    analysis_agent = AnalysisAgent()

    print("Welcome to the Alphavantage Chatbot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chatbot. Goodbye!")
            break

        financial_data = await alphavantage_agent.fetch_data(user_input)
        analysis_result = analysis_agent.analyze(financial_data)

        print(f"Bot: {analysis_result}")

if __name__ == "__main__":
    asyncio.run(main())