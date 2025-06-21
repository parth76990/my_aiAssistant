import requests
import pyttsx3

# Initialize the pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 200)

def ask_llm_and_speak(user_prompt):
    # Modify the prompt
    modified_prompt = f"{user_prompt}\n(Answer in 30 to 70 words only.)"

    try:
        # Send to local LLM
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "llama3.2:3b",
                "prompt": modified_prompt,
                "stream": False
            }
        )
        generated_response = response.json().get('response', 'Sorry, I have no answer.')
        print("Generated Response:\n", generated_response)

        # Speak the response
        engine.say(generated_response)
        engine.runAndWait()
    except Exception as e:
        print("Error contacting LLM:", e)
        engine.say("I couldn't get the answer from the model.")
        engine.runAndWait()
