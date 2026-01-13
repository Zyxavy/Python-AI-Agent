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

cur_loops = 0

def main():
    try:
        load_dotenv();
        api_key = os.environ.get("GEMINI_API_KEY")
    
    except Exception as e:
        print(f"Error: {e}");
        return

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for cur_loops in range(20):

        response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt))

        if response.candidates and response.candidates[0].content:
            messages.append(response.candidates[0].content)

        if args.verbose:
            print(f"User prompt: {args}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} ")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls:
                for function in response.function_calls:

                    function_call_result = call_function(function)

                    messages.append(function_call_result)

                    if args.verbose:
    
                        try:
                            if (function_call_result.parts and function_call_result.parts[0].function_response and 
                                function_call_result.parts[0].function_response.response):

                                result = function_call_result.parts[0].function_response.response
                                print(f"Function result: {result}")

                        except Exception as e:
                            print(f"Error displaying function result: {e}")

        else:
            if response.text:
                print(response.text)
            break

    if cur_loops >= 20:
        print("Maximum loops reached(20)")
        return 1
    
    return 0

if __name__ == "__main__":
    main()
