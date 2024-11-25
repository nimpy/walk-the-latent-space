import os
import json

import openai
from openai import OpenAI


openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()


def openai_call_wrapper_return_json(messages):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={ "type": "json_object" },
        messages=messages,
        temperature=0.0,
    )
    print("OpenAI response:\n", response.choices[0].message.content)
    try:
        response_dict = json.loads(response.choices[0].message.content)
    except json.decoder.JSONDecodeError as e:
        print("There was an error with parsing the json response in openai_call_wrapper_return_json(). The response was:", response.choices[0].message.content)
        raise e
    return response_dict


def openai_call_wrapper(messages):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0.0,
    )
    return response.choices[0].message.content
