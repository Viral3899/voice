import json

from config import settings
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import ToolMessage
from langchain_core.messages.utils import convert_to_messages

from tools import (
    identify_user,
    fetch_slots,
    book_appointment,
    retrieve_appointments,
    cancel_appointment,
    modify_appointment
)


client = ChatGroq(
    model=settings.GROQ_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=0.0,
    max_retries=2
)


def format_tool_message(tool_name, result):
    if tool_name == "identify_user":
        return result.get("message", "User identified")
    if tool_name == "fetch_slots":
        if result.get("success"):
            slots = result.get("available_slots", [])
            date = result.get("date")
            return f"Available slots for {date}: {', '.join(slots) if slots else 'none available'}"
        return result.get("message", "Failed to fetch slots")
    if tool_name == "book_appointment":
        if result.get("success"):
            return f"Booking confirmed ✅ Appointment ID {result.get('appointment_id')}"
        return f"Unable to book appointment: {result.get('message')}"
    if tool_name == "retrieve_appointments":
        appointments = result if isinstance(result, list) else result.get("appointments")
        if appointments:
            return f"Retrieved {len(appointments)} appointments"
        return "No appointments found"
    if tool_name == "cancel_appointment":
        if result.get("success"):
            return "Appointment cancelled ✅"
        return f"Unable to cancel appointment: {result.get('message')}"
    if tool_name == "modify_appointment":
        if result.get("success"):
            return "Appointment updated ✅"
        return f"Unable to modify appointment: {result.get('message')}"
    if tool_name == "end_conversation":
        return result.get("message", "Conversation ended")
    return result.get("message", f"Tool called: {tool_name}")


SYSTEM_PROMPT = """

You are a friendly healthcare AI receptionist.

Your responsibilities:

1. Identify user.

2. Book appointments.

3. Reschedule appointments.

4. Cancel appointments.

5. Retrieve appointments.

Always collect:

- Name

- Phone Number

- Date

- Time

- Intent

Always use tools.

Never hallucinate appointment details.

Always confirm actions clearly.

"""


TOOLS = [

{
"type":"function",

"function":{

"name":"identify_user",

"description":"Create or fetch user",

"parameters":{

"type":"object",

"properties":{

"phone_number":{

"type":"string"

},

"name":{

"type":"string"

}

},

"required":["phone_number"]

}

}

},


{
"type":"function",

"function":{

"name":"fetch_slots",

"description":"Get available slots",

"parameters":{

"type":"object",

"properties":{

"booking_date":{

"type":"string"

}

},

"required":["booking_date"]

}

}

},


{
"type":"function",

"function":{

"name":"book_appointment",

"description":"Book appointment",

"parameters":{

"type":"object",

"properties":{

"user_id":{

"type":"integer"

},

"booking_date":{

"type":"string"

},

"booking_time":{

"type":"string"

}

},

"required":[

"user_id",

"booking_date",

"booking_time"

]

}

}

},


{
"type":"function",

"function":{

"name":"retrieve_appointments",

"description":"Get user appointments",

"parameters":{

"type":"object",

"properties":{

"user_id":{

"type":"integer"

}

},

"required":["user_id"]

}

}

},


{
"type":"function",

"function":{

"name":"cancel_appointment",

"description":"Cancel appointment",

"parameters":{

"type":"object",

"properties":{

"appointment_id":{

"type":"integer"

}

},

"required":["appointment_id"]

}

}

},


{
"type":"function",

"function":{

"name":"modify_appointment",

"description":"Reschedule appointment",

"parameters":{

"type":"object",

"properties":{

"appointment_id":{

"type":"integer"

},

"new_date":{

"type":"string"

},

"new_time":{

"type":"string"

}

},

"required":[

"appointment_id",

"new_date",

"new_time"

]

}

}

}

]


def process_message(

    db,

    message,

    history=None

):

    if history is None:

        history = []


    def normalize_history(history):
        normalized = []
        for item in history:
            role = item.get("role")
            content = item.get("content", "")
            if role == "assistant":
                normalized.append(("assistant", content))
            elif role == "user":
                normalized.append(("human", content))
            elif role == "system":
                normalized.append(("system", content))
            else:
                normalized.append((role, content))
        return normalized

    messages = [("system", SYSTEM_PROMPT)]
    messages.extend(normalize_history(history))
    messages.append(("human", message))

    tool_model = client.bind_tools(TOOLS, tool_choice="auto")
    response = tool_model.invoke(messages)

    if not response.tool_calls:
        return {
            "response": response.content,
            "tool": None
        }

    tool_call = response.tool_calls[0]
    tool_name = tool_call["name"]
    args = tool_call["args"]
    result = None

    if tool_name == "identify_user":
        result = identify_user(db, **args)
    elif tool_name == "fetch_slots":
        result = fetch_slots(db, **args)
    elif tool_name == "book_appointment":
        result = book_appointment(db, **args)
    elif tool_name == "retrieve_appointments":
        result = retrieve_appointments(db, **args)
    elif tool_name == "cancel_appointment":
        result = cancel_appointment(db, **args)
    elif tool_name == "modify_appointment":
        result = modify_appointment(db, **args)

    messages.append(ToolMessage(
        content=json.dumps(result),
        tool_call_id=tool_call.get("id")
    ))

    final_response = tool_model.invoke(messages)
    answer = final_response.content

    return {
        "response": answer,
        "tool": tool_name,
        "tool_result": result,
        "tool_message": format_tool_message(tool_name, result)
    }       