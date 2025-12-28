import argparse
import time
import random
from langchain_core.messages import HumanMessage
from graph import app, save_dag_image
from nodes.tools import DebateLogger, validate_topic
import config

# --- COLORS FOR UI ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_agent_turn(agent, text):
    color = Colors.CYAN if agent == "Scientist" else Colors.YELLOW
    print(f"\n{color}{Colors.BOLD}[{agent}]{Colors.RESET}")
    print(f"{text.strip()}")

def print_judge(verdict):
    print(f"\n{Colors.RED}{Colors.BOLD}{'='*20} JUDGE VERDICT {'='*20}{Colors.RESET}")
    print(f"{Colors.RED}{verdict}{Colors.RESET}")
    print(f"{Colors.RED}{Colors.BOLD}{'='*55}{Colors.RESET}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run ATG Multi-Agent Debate")
    parser.add_argument("--topic", type=str, help="Topic for the debate (optional)")
    parser.add_argument("--seed", type=int, help="Random seed for deterministic runs")
    parser.add_argument("--log-path", type=str, default="logs", help="Directory to save logs")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # 1. Handle Determinism (Seed)
    if args.seed is not None:
        random.seed(args.seed)
        config.SET_DETERMINISTIC(True) # We will add this to config.py
        print(f"{Colors.BLUE}Deterministic mode enabled (Seed: {args.seed}){Colors.RESET}")
    
    # 2. Setup Logging
    logger = DebateLogger(log_dir=args.log_path)

    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.HEADER}{Colors.BOLD} ATG Multi-Agent Debate System {Colors.RESET}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*50}{Colors.RESET}")

    # 3. Input Handling (CLI Flag or Interactive)
    if args.topic:
        raw_topic = args.topic
    else:
        raw_topic = input(f"{Colors.BOLD}Enter topic for debate: {Colors.RESET}")

    try:
        topic = validate_topic(raw_topic)
    except ValueError as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}")
        return

    logger.log("SYSTEM_START", {"topic": topic, "seed": args.seed})
    save_dag_image()

    # 4. Initialize State
    initial_state = {
        "topic": topic,
        "messages": [HumanMessage(content=f"Topic: {topic}")],
        "round_count": 0,
        "current_speaker": "None",
        "final_verdict": ""
    }

    print(f"\n{Colors.BOLD}Starting debate on:{Colors.RESET} {Colors.GREEN}{topic}{Colors.RESET}")
    time.sleep(1) 

    # 5. Run Graph
    try:
        for event in app.stream(initial_state):
            for node_name, node_state in event.items():
                logger.log("NODE_TRANSITION", {"node": node_name, "state": node_state})
                
                if node_name in ["Scientist", "Philosopher"]:
                    if node_state.get('messages'):
                        print_agent_turn(node_name, node_state['messages'][-1].content)
                        if not args.seed: time.sleep(0.5) # Skip delay if testing
                
                elif node_name == "Judge":
                    verdict = node_state.get('final_verdict')
                    print_judge(verdict)
                    logger.log("FINAL_VERDICT", verdict)
    
    except Exception as e:
        print(f"\n{Colors.RED}Runtime Error: {e}{Colors.RESET}")

    print(f"\n{Colors.BLUE}Debate complete. Log file saved to {logger.filepath}{Colors.RESET}")

if __name__ == "__main__":
    main()