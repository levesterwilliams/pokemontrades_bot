import openai
import os

class GPT35TurboClient:
    def __init__(self, secret_key, model_name):
        if not isinstance(secret_key, str) or not isinstance(model_name, str):
            raise TypeError("String is expected as an argument for "
                            "GPT35TurboClient.")

        openai.api_key = secret_key
        os.environ['OPENAI_API_KEY'] = openai.api_key
        self._finetuned_model = model_name

    def generate_jsonstring(self, prompt):
        client = openai.OpenAI()
        if not isinstance(prompt, str):
            raise TypeError("String is expected as the argument for 'prompt'.")

        system_message = {"role": "system",
                          "content": "Generate a JSON string that describes a Pokémon trade or giveaway, including sender's and receiver's Pokémon details such as the name, IV, gender, ability, hidden ability, region, language, and form of each Pokemon."}
        response = client.chat.completions.create(
            model=self._finetuned_model,
            messages=[
                system_message,
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["###"]
        )
        return response.choices[0].message.content.strip()