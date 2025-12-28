from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import config
import time

def agent_node(state, agent_name, persona_file):
    """
    Generic function for both agents with RETRY LOGIC and DYNAMIC CONFIG.
    """
    
    # 1. INITIALIZE LLM (Moved inside function to support dynamic Config changes)
    llm = ChatGroq(
        api_key=config.GROQ_API_KEY, 
        model=config.MODEL_NAME, 
        temperature=config.TEMPERATURE # Uses 0.0 if seed is set, else 0.7
    )

    messages = state["messages"]
    
    # 2. LOAD PERSONA
    try:
        with open(f"personas/{persona_file}", "r") as f:
            system_prompt = f.read().strip()
    except FileNotFoundError:
        return {
            "current_speaker": agent_name,
            "latest_content": f"[System Error: {persona_file} not found]",
            "messages": [HumanMessage(content=f"Error: {persona_file} missing")]
        }

    # 3. PREPARE CONTEXT
    # We take the last few messages to give context
    relevant_context = messages[-3:] if len(messages) > 3 else messages

    # 4. CONSTRUCT PROMPT
    # Llama 3 strictly needs the LAST message to be from a Human (User) to trigger a response.
    # We inject a final HumanMessage containing the instruction.
    instruction_text = (
        f"You are the {agent_name}.\n"
        f"Review the context above. The last argument was made by your opponent.\n"
        "Provide a short, sharp counter-argument (max 2 sentences).\n"
        "Do not repeat previous points."
    )

    conversation_chain = [
        SystemMessage(content=system_prompt),
        *relevant_context,
        HumanMessage(content=instruction_text) # <--- FORCE USER PROMPT AT END
    ]
    
    # 5. GENERATE WITH RETRY
    response_content = ""
    response_msg = None
    
    for attempt in range(3):
        try:
            response_msg = llm.invoke(conversation_chain)
            
            if response_msg.content and response_msg.content.strip():
                response_content = response_msg.content
                break
        except Exception as e:
            # Print the actual error to the console so we can see it
            print(f"DEBUG: {agent_name} Attempt {attempt+1} Error: {str(e)}")
            time.sleep(1)
            
    # Fallback
    if not response_content:
        # If it fails, we force a generic response so the debate doesn't die
        response_msg = AIMessage(content=f"I must consider the previous point carefully, but I maintain my stance.")

    # 6. RETURN STATE
    return {
        "current_speaker": agent_name,
        "latest_content": response_msg.content,
        "messages": [response_msg] 
    }

def scientist_node(state):
    return agent_node(state, "Scientist", "scientist.txt")

def philosopher_node(state):
    return agent_node(state, "Philosopher", "philosopher.txt")