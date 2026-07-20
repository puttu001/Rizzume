# Home for the OpenAI interview engine, called internally by app/services/
# (no network hop — see architecture discussion on why this stays a module
# rather than its own microservice). Planned modules:
#   question_generator.py   — dynamic question generation
#   followup_logic.py       — follow-up question decisions
#   difficulty_controller.py
#   feedback_generator.py   — final scored feedback
