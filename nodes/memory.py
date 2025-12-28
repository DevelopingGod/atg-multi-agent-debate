from difflib import SequenceMatcher

def check_coherence(state):
    """
    Rounds Controller & Logic Validator.
    Checks for repetition and increments round count.
    """
    messages = state["messages"]
    latest_msg = messages[-1].content
    
    # 1. Repetition Check (Simple Semantic Overlap)
    for msg in messages[:-1]:
        similarity = SequenceMatcher(None, latest_msg, msg.content).ratio()
        if similarity > 0.85: # Threshold for repetition
            print(f"!! WARNING: High similarity detected ({similarity:.2f}). Possible repetition.")
            # In a real app, you might trigger a regeneration here.
    
    # 2. Increment Round
    new_count = state["round_count"] + 1
    
    return {"round_count": new_count}