import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock bpy before importing operators
mock_bpy = MagicMock()
class MockOperator:
    pass
mock_bpy.types.Operator = MockOperator
sys.modules["bpy"] = mock_bpy

# Fix relative import issue by creating a temporary copy
if os.path.exists("operators.py"):
    with open("operators.py", "r") as f:
        content = f.read()

    # Simple replace to make it importable as standalone
    content = content.replace("from . import utils", "import utils")

    with open("operators_test_temp.py", "w") as f:
        f.write(content)

    # Add current directory to sys.path to find the generated file
    sys.path.append(os.getcwd())

    # Import the modified module
    import operators_test_temp
else:
    raise FileNotFoundError("operators.py not found")

class TestPerformance(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        # Cleanup temporary file
        if os.path.exists("operators_test_temp.py"):
            os.remove("operators_test_temp.py")

    def setUp(self):
        self.operator = operators_test_temp.CONJURE_OT_Generate()
        self.operator._queue = MagicMock()

        self.mock_context = MagicMock()
        self.mock_area = MagicMock()
        self.mock_area.type = "VIEW_3D"
        self.mock_context.screen.areas = [self.mock_area]
        self.mock_context.scene.conjure = MagicMock()

        self.mock_event = MagicMock()
        self.mock_event.type = "TIMER"

    def test_no_redraw_on_empty_queue(self):
        """Verify that tag_redraw is NOT called when queue is empty."""
        # Queue is empty
        self.operator._queue.empty.side_effect = [True]
        self.operator._queue.get_nowait.side_effect = Exception("Queue is empty")

        self.mock_area.tag_redraw.reset_mock()

        self.operator.modal(self.mock_context, self.mock_event)

        self.mock_area.tag_redraw.assert_not_called()

    def test_redraw_on_message_processed(self):
        """Verify that tag_redraw IS called when a message is processed."""
        # Queue has one item
        # First check false (not empty), second check true (empty)
        self.operator._queue.empty.side_effect = [False, True]
        self.operator._queue.get_nowait.return_value = ("INFO", "Test Message", "")

        self.mock_area.tag_redraw.reset_mock()

        self.operator.modal(self.mock_context, self.mock_event)

        self.mock_area.tag_redraw.assert_called()

if __name__ == "__main__":
    unittest.main()
