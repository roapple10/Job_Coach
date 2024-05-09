import hashlib
import json
import os
import pickle
from langchain_openai import ChatOpenAI
from groq import Groq 
# import openai as ai




class AiEngine:
    def __init__(self, api_key, is_debug=False):
        self.is_debug = is_debug

        
        self.ai = Groq(    # This is the default and can be omitted
                    api_key=api_key,)
    
        self.models = ["mixtral-8x7b-32768","llama3-8b-8192",]
        self.selected_model = "mixtral-8x7b-32768"
        self.temperature = 0.9
        self.cache = dict()

        if os.path.exists('cache.pkl'):
            with open('cache.pkl', 'rb') as f:
                self.cache = pickle.load(f)
                
    

    def get_prompt_response(self, messages: list) -> str:

        cache_response = self.get_from_cache(messages)
        if cache_response is not None:
            print('cache hit')
            return cache_response

        print('cache miss')
        if self.is_debug:
            print(messages)


    
        chat_completion = self.ai.chat.completions.create(
            #
            # Required parameters
            #
            messages=messages,

            # The language model which will generate the completion.
            model=self.selected_model,

        
            # Optional parameters
            # Controls randomness: lowering results in less random completions.
            # As the temperature approaches zero, the model will become deterministic
            # and repetitive.
            temperature=self.temperature,

            # The maximum number of tokens to generate. Requests can use up to
            # 32,768 tokens shared between prompt and completion.
            # max_tokens=1024,

            # Controls diversity via nucleus sampling: 0.5 means half of all
            # likelihood-weighted options are considered.
            top_p=1,

            # A stop sequence is a predefined or user-specified text string that
            # signals an AI to stop generating content, ensuring its responses
            # remain focused and concise. Examples include punctuation marks and
            # markers like "[end]".
            stop=None,
            # If set, partial message deltas will be sent.
            stream=False,
        )
        result = chat_completion.choices[0].message.content
        if self.is_debug:
            print(result)
        
        

        self.add_to_cache(messages, result)

        return result

    def get_from_cache(self, messages: list) -> str | None:
        md5 = self._md5_messages(messages)
        if md5 in self.cache:
            return self.cache[md5]

        return None

    def add_to_cache(self, messages: list, response: str):
        md5 = self._md5_messages(messages)
        self.cache[md5] = response
        with open('cache.pkl', 'wb') as f:
            pickle.dump(self.cache, f)

    def clear_cache(self):
        self.cache = dict()

    @staticmethod
    def _md5_messages(messages: list) -> str:
        return hashlib.md5(json.dumps(messages).encode('utf-8')).hexdigest()