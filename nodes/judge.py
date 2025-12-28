from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import config

# Initialize Groq LLM for Judging (Temperature 0 for consistency)
llm = ChatGroq(
    api_key=config.GROQ_API_KEY, 
    model=config.MODEL_NAME, 
    temperature=0
)

def judge_node(state):
    messages = state["messages"]
    topic = state["topic"]
    
    # Construct the prompt with the full transcript
    prompt = f"""
    You are an impartial Judge. Review the following debate on the topic: "{topic}".
    
    Transcript:
    {messages}
    
    Task:
    1. Summarize the debate.
    2. Declare a winner (Scientist or Philosopher).
    3. Provide a logical justification.
    
    Output Format:
    Winner: [Name]
    Reason: [Reasoning]
    Summary: [Summary]
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    return {"final_verdict": response.content}