import requests


def correct_transcription(transcription):
    url = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "22ec84421ec24230a3638d1b51e3a7dc"  # Replace YOUR_API_KEY with your actual API key
    }

    data = {
        "messages": [
            {"role": "user", "content": f"Correct this text: {transcription}"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the response is successful
    if response.status_code == 200:
        corrected_text = response.json()["choices"][0]["message"]["content"]
        return corrected_text
    else:
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response.json()}")
        return None
