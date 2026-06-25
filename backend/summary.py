import json

from config import settings
from langchain_groq.chat_models import ChatGroq


client = ChatGroq(
    model=settings.GROQ_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=0.2,
    max_retries=2
)


SUMMARY_PROMPT = """

You are an AI assistant that creates structured call summaries for a healthcare appointment system.

From the given conversation, extract and return a JSON object with:

1. user_info:
   - name
   - phone_number (if mentioned)

2. intent:
   - booking / rescheduling / cancellation / inquiry

3. appointments:
   - booked appointments
   - cancelled appointments
   - modified appointments

4. timeline:
   - short step-by-step conversation summary

5. raw_summary:
   - clean human readable paragraph

Rules:
- Be accurate
- Do not hallucinate missing data
- Only use provided conversation
- Return ONLY valid JSON
"""


def generate_summary(

    conversation_history: list

):

    try:

        messages = [

            {

                "role": "system",

                "content": SUMMARY_PROMPT

            },

            {

                "role": "user",

                "content": json.dumps(

                    conversation_history

                )

            }

        ]


        response = client.invoke(messages)
        content = response.content


        try:

            parsed = json.loads(content)

        except:

            parsed = {

                "raw_summary": content

            }


        return {

            "success": True,

            "summary": parsed

        }


    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }   