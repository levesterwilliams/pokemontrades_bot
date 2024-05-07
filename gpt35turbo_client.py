import openai
import os

class GPT35TurboClient:
    def __init__(self, secret_key, model_name):
        """
        Constructor to initialize GPT35TurboClient.

        Args:
            secret_key (string): API key for GPT35Turbo.
            model_name (string): Finetuned model name for GPT35Turbo.

        Raise:
            ValueError: If secret_key or model_name is not a string
        """
        if not isinstance(secret_key, str) or not isinstance(model_name, str):
            raise TypeError("String is expected as an argument for "
                            "GPT35TurboClient.")

        openai.api_key = secret_key
        os.environ['OPENAI_API_KEY'] = openai.api_key
        self._finetuned_model = model_name

    def generate_jsonstring(self, prompt):
        """
        Generate a JSON-formatted string that can be used as input for data
        parsing in main application.

        Args:
            prompt (str): The prompt is input for finetuned GPT 3.5 turbo model.

        Returns:
            str: The JSON-formatted string.

        Raise:
            ValueError: If the prompt is not a string.

        Note:
            The client/caller of the method must catch and handle errors
            associated with invoking OpenAI API requests.
        """
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
