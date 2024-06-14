
import requests
import json
from datetime import date
import pandas as pd

class GPTAssistant:
    def __init__(self, api_key, url):
        self.API_KEY = api_key
        self.URL = url


    def save_usage(self, response):
        response_json = response.json()
        prompt_tokens = response_json['usage']['prompt_tokens']
        completion_tokens = response_json['usage']['completion_tokens']
        model = response_json.get('model')
        today = date.today()
        with open('api_usage.csv', 'a') as f:
            f.write(f"{model}, {prompt_tokens}, {completion_tokens}, {response.status_code}, {today}\n")


    def get_linear_probabilities(self, log_prob):
        linear_prob = 10 ** log_prob
        return linear_prob


    def check_log_response(self, response, prompt):
        if response.status_code != 200:
            print(f">> Prompt failed: {prompt}")
            raise Exception(f"Failed to get response, status code: {response.status_code}")


    def get_decision_response(self, language, prompt):
        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY
        }

        if language == "english":
            system_prompt = "You are only able to output 1 of 2 words namely \"Yes\" or \"No\". You must use 1 capital letter and after 1 lowercase letter"
        elif language == "dutch":
            system_prompt = "Je kunt alleen 1 van de 2 woorden \"Ja\" of \"Nee\" generen. Je moet en kunt slechts 1 hoofdletter hebben"

        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1,
            "temperature": 0,
            "logprobs": True,
            "top_logprobs": 5,
        }
        
        response = requests.post(self.URL, headers=headers, data=json.dumps(data))
        print(response.json())
        
        # self.check_response(response, prompt) 
        self.save_usage(response)
        return response


    def get_summary_response(self,language, prompt):
        headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY
        }

        if language == "english":
            system_prompt = "Generate a summary with half the length of the original text."
        elif language == "dutch":
            system_prompt = "Genereer een samenvatting met de helft van de lengte van de originele tekst."

        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 260,
            "temperature": 0.7,
        }
        
        response = requests.post(self.URL, headers=headers, data=json.dumps(data))
        # print(response.json())
        
        # self.check_response(response, prompt) 
        self.save_usage(response)
        return response