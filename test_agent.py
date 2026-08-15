from app.services.agent import SmartDocAgent

agent = SmartDocAgent()

question = "What is machine learning?"

answer = agent.answer_question(
    question
)

print(answer)