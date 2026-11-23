import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from tools import TOOLS, TOOL_BY_NAME


CHAT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
MAX_STEPS = 5
MAX_HISTORY = 12

SYSTEM_PROMPT = """
You are StudyMate, a friendly AI study planner.

Your job is to help students plan their studies.

You can:
1. Help students with study planning.
2. Calculate days remaining until exams.
3. Divide study hours among subjects.
4. Give simple study tips.

Rules:
- Remember previous conversations.
- Use days_until_exam when students ask about exam dates.
- Use split_study_hours when students ask to divide study hours.
- Do not guess calculation results.
- If the input is invalid, politely ask the student to correct it.
- If a question is unrelated to study planning, politely explain that it is outside your purpose.
- Give short and simple answers.
"""


def run_turn(api_key: str, history: list, user_question: str):
    llm = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        google_api_key=api_key,
        temperature=0.2,
    )
    llm_with_tools = llm.bind_tools(TOOLS)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *history[-MAX_HISTORY:],
        HumanMessage(content=user_question),
    ]
    used_tools = []

    for _ in range(MAX_STEPS):
        ai_response = llm_with_tools.invoke(messages)
        messages.append(ai_response)

        if not ai_response.tool_calls:
            answer = ai_response.content
            if isinstance(answer, str):
                return answer, used_tools
            if isinstance(answer, list):
                answer = "\n".join(
                    part.get("text", "")
                    if isinstance(part, dict)
                    else str(part)
                    for part in answer
                )
            return str(answer), used_tools

        for call in ai_response.tool_calls:
            tool_name = call["name"]
            selected_tool = TOOL_BY_NAME.get(tool_name)

            if selected_tool is None:
                tool_result = ToolMessage(
                    content="This tool is not available.",
                    tool_call_id=call["id"],
                )
            else:
                used_tools.append(tool_name)
                try:
                    tool_result = selected_tool.invoke(call)
                except Exception:
                    tool_result = ToolMessage(
                        content="Invalid input. Please check the values and try again.",
                        tool_call_id=call["id"],
                    )

            messages.append(tool_result)

    return "I could not complete that request. Please try again.", used_tools
