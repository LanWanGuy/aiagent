import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not set")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

parser = argparse.ArgumentParser(description="Ask a question to the AI agent")
parser.add_argument("question", type=str, help="The question to ask")
args = parser.parse_args()

messages = [
    {
        "role": "user",
        "content": args.question,
    }
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages
)

if response.usage != None:
    print (f"Prompt tokens: {response.usage.prompt_tokens}")
    print (f"Response tokens: {response.usage.completion_tokens}")
else:
    raise RuntimeError("No usage data available")


print(response.choices[0].message.content)
