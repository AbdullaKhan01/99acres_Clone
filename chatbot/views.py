from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@csrf_exempt
def chat_with_ai(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        user_msg = data.get("message", "")

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_msg},
            ],
        )

        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})

    except Exception as e:
        print("Groq Error:", e)
        return JsonResponse({"reply": "⚠️ Server error, please try again later."})
