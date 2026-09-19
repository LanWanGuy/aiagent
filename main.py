import os, argparse, json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


def main():

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
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": args.question,
        }
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if response.usage == None:
            raise RuntimeError("No usage data available")

        if args.verbose:
            # print (f"User prompt: {args.question}")
            # print (f"Prompt tokens: {response.usage.prompt_tokens}")
            # print (f"Response tokens: {response.usage.completion_tokens}")
            message = response.choices[0].message
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function_args = json.loads(tool_call.function.arguments or "{}")
                    result_message = call_function(tool_call, function_args)
                    if not result_message["content"]:
                        raise RuntimeError(f"Function {tool_call.function.name} returned no content")
                    else:
                        print(f"-> {result_message['content']}")
            else:
                print(message)
        else:
            message = response.choices[0].message
            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    function_args = json.loads(tool_call.function.arguments or "{}")
                    result_message = call_function(tool_call, function_args)
                    if not result_message["content"]:
                        raise RuntimeError(f"Function {tool_call.function.name} returned no content")
                    messages.append(result_message)
            else:
                messages.append(message)
                print(str(message.content))
                break

if __name__ == "__main__":
    main()
