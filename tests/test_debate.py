import unittest
from unittest.mock import MagicMock, patch
from nodes.tools import validate_topic
from nodes.memory import check_coherence
from langchain_core.messages import HumanMessage

class TestDebateSystem(unittest.TestCase):

    def test_topic_validation(self):
        """Test that topic validation rejects short/invalid topics"""
        valid_topic = "Artificial Intelligence"
        self.assertEqual(validate_topic(valid_topic), "Artificial Intelligence")

        with self.assertRaises(ValueError):
            validate_topic("AI") # Too short

    def test_round_counter(self):
        """Test that the round counter increments correctly"""
        # Mock State
        initial_state = {
            "messages": [MagicMock(content="Hello"), MagicMock(content="World")],
            "round_count": 0
        }
        
        # Run function
        new_state = check_coherence(initial_state)
        
        # Assert
        self.assertEqual(new_state["round_count"], 1)

    @patch("nodes.agents.llm")  # <--- PATCH THE GLOBAL OBJECT DIRECTLY
    def test_agent_initialization(self, mock_llm):
        """Test that Agents load without crashing"""
        from nodes.agents import scientist_node
        
        # 1. Setup the Mock Response
        mock_response = MagicMock()
        mock_response.content = "Mock Argument"
        # When .invoke() is called on the llm, return our fake message
        mock_llm.invoke.return_value = mock_response

        # 2. Mock State
        state = {"messages": [], "topic": "Test"}
        
        # 3. Run Node
        result = scientist_node(state)
        
        # 4. Verify
        self.assertEqual(result["current_speaker"], "Scientist")
        self.assertEqual(result["latest_content"], "Mock Argument")

if __name__ == "__main__":
    unittest.main()