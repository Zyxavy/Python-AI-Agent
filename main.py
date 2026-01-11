import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.prompts import system_prompt
from tools.call_function import available_functions
from tools.call_function import call_function
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def main():
    try:
        load_dotenv();
        api_key = os.environ.get("GEMINI_API_KEY")
    
    except Exception as e:
        printf(f"Error: {e}");

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt))

    if args.verbose:
        print(f"User prompt: {args}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} ")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)

    else:
        print(response.text)

    if response.function_calls:
            for function in response.function_calls:

                function_call_result = call_function(function)

                if not function_call_result.parts:
                    raise Exception("Error: empty .parts")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Error: Should be an object")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Error: Invalid response")
                
                function_results = [function_call_result.parts[0]]
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
           

if __name__ == "__main__":
    main()
