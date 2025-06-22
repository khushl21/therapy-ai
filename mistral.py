import requests
import json

# Set up the base URL for the local Ollama API
url = "http://localhost:11434/api/chat"

# Define the payload (your input prompt)
payload = {
    "model": "mistral",  # Replace with the model name you're using
    "messages": [{"role": "user", "content": "What is Python?"}]
}

# Send the HTTP POST request with streaming enabled
response = requests.post(url, json=payload, stream=True)

# Check the response status
if response.status_code == 200:
    print("Streaming response from Ollama:")
    for line in response.iter_lines(decode_unicode=True):
        if line:  # Ignore empty lines
            try:
                # Parse each line as a JSON object
                json_data = json.loads(line)
                # Extract and print the assistant's message content
                if "message" in json_data and "content" in json_data["message"]:
                    print(json_data["message"]["content"], end="")
            except json.JSONDecodeError:
                print(f"\nFailed to parse line: {line}")
    print()  # Ensure the final output ends with a newline
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# import ollama

# # Initialize the Ollama client
# client = ollama.Client()

# # Define the model and the input prompt
# model = "mistral"  # Replace with your model name
# prompt = "What is Python?"

# # Send the query to the model
# response = client.generate(model=model, prompt=prompt)

# # Print the response from the model
# print("Response from Ollama:")
# print(response.response)