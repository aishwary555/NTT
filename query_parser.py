import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key= "")

def extract_filters_from_query(query):
    prompt = f"""
You are a smart assistant for analyzing IoT equipment data.

From the following user query, extract:
- Device ID (e.g., D100, D101, D102)
- Location (e.g., Mumbai, Delhi, Chennai)
- Month (as an integer 1 to 12)

Query:
\"\"\"{query}\"\"\"

Return ONLY a valid JSON object with this structure:
{{
  "device_id": "<Device ID or null>",
  "location": "<Location or null>",
  "month": <Month or null>
}}

⚠️ Do not include ```json, backticks, or explanations.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You extract structured filters from user queries."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        print("📤 GPT Response (raw):", content)

        # Remove markdown code block formatting if GPT returns it
        if content.startswith("```json") or content.startswith("```"):
            content = content.split("```")[1].strip()

        filters = json.loads(content)

        return {
            "device_id": filters.get("device_id"),
            "location": filters.get("location"),
            "month": filters.get("month")
        }

    except Exception as e:
        print("❌ Error parsing GPT response:", e)
        return {"device_id": None, "location": None, "month": None}

