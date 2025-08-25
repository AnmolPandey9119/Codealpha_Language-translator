import requests
import json
import os

LANGUAGES = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
    'ko': 'Korean', 'zh': 'Chinese (Simplified)', 'ar': 'Arabic', 'hi': 'Hindi',
    'bn': 'Bengali', 'pa': 'Punjabi', 'te': 'Telugu', 'mr': 'Marathi',
    'ta': 'Tamil', 'ur': 'Urdu', 'gu': 'Gujarati'
}

def clear_screen():
    """Clears the terminal screen."""

    if os.name == 'nt':
        _ = os.system('cls')
    
    else:
        _ = os.system('clear')

def print_languages():
    """Prints the available languages in a formatted way."""
    print("--- Available Languages ---")
    
    sorted_languages = sorted(LANGUAGES.items(), key=lambda item: item[1])
    
    
    lang_list = [f"{code}: {name}" for code, name in sorted_languages]
    midpoint = (len(lang_list) + 1) // 2
    col1 = lang_list[:midpoint]
    col2 = lang_list[midpoint:]
    
    for i in range(midpoint):
        line = f"{col1[i]:<30}" 
        if i < len(col2):
            line += col2[i]
        print(line)
    print("-" * 27)


def get_language_choice(prompt_message):
    """
    Prompts the user to select a language and validates the input.
    
    Args:
        prompt_message (str): The message to display to the user.

    Returns:
        tuple: A tuple containing the language code and language name.
    """
    while True:
        code = input(prompt_message).lower().strip()
        if code in LANGUAGES:
            return code, LANGUAGES[code]
        else:
            print(f"Invalid code '{code}'. Please choose from the list above.")


def call_gemini_api(prompt, api_key):
    """
    Makes a POST request to the Gemini API to get the translation.

    Args:
        prompt (str): The full prompt for the API, including the text to translate.
        api_key (str): The user's Google AI API key.

    Returns:
        str: The translated text, or an error message if the API call fails.
    """
    if not api_key:
        return "Error: API key is missing. Please provide a valid API key in the script."

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  
        
        result = response.json()
        
        text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
        
        if text:
            return text.strip().strip('"')
        else:
            return "Error: Could not extract translation from API response."

    except requests.exceptions.HTTPError as e:
        return f"Error: An HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error: A network error occurred: {e}"
    except (KeyError, IndexError):
        return "Error: Invalid API response structure."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def main():
    """
    Main function to run the translation tool.
    """

    api_key = "AIzaSyAI98Ff1S16VYwTTBJvPuONs21ilczUaFg"
    
    while True:
        clear_screen()
        print("=============================")
        print("    Language Translator ")
        print("=============================")
        print_languages()

        source_code, source_name = get_language_choice("Enter the source language code (e.g., 'en'): ")
        target_code, target_name = get_language_choice("Enter the target language code (e.g., 'es'): ")
        
        print(f"\nTranslating from {source_name} to {target_name}.")
        text_to_translate = input("Enter the text you want to translate:\n> ")

        if not text_to_translate.strip():
            print("No text entered. Please try again.")
            continue

        
        prompt = f'Translate the following text from {source_name} to {target_name}: "{text_to_translate}"'
        
        print("\nTranslating...")
        
        translated_text = call_gemini_api(prompt, api_key)
        
        print("\n--- Translation Result ---")
        print(translated_text)
        print("--------------------------\n")

        
        again = input("Translate another text? (y/n): ").lower().strip()
        if again != 'y':
            print("Exiting translator. Goodbye!")
            break

if __name__ == "__main__":
    main()
