from openai import AzureOpenAI
import os
import json
import datetime


endpoint = os.environ['AOAI_ENDPOINT']
key = os.environ['AOAI_KEY']
api_version = "2024-02-01"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=key
)


model_settings = {
    "temperature": 1,
    "top_p": 0.95,
    "max_tokens": 1000,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": None
}

messages = []
system_message = "You are an AI assistant that helps people learn about the Azure OpenAI Service. You are a non-native english speaker."
messages.append({"role": "system", "content": system_message})

prompt = input("Enter your prompt: ")

messages.append({"role": "user", "content": prompt})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=model_settings['temperature'],
    max_tokens=model_settings['max_tokens'],
    top_p=model_settings['top_p'],
    frequency_penalty=model_settings['frequency_penalty'],
    presence_penalty=model_settings['presence_penalty']
)

print(response)

response_text = response.choices[0].message.content
messages.append({"role": "assistant", "content": response_text})
prompt = input("Enter your prompt: ")

messages.append({"role": "user", "content": prompt})

# Appending on the customer information

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=model_settings['temperature'],
    max_tokens=model_settings['max_tokens'],
    top_p=model_settings['top_p'],
    frequency_penalty=model_settings['frequency_penalty'],
    presence_penalty=model_settings['presence_penalty']
)