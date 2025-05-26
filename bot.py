import cohere
import random
import re

# Replace this with your own API key.
API_KEY = "TLIKEjNopX4NKHX1upnVBN85Cu1s52eWaCoBulNN"


class Cohere:

    def __init__(self):
        self.co = cohere.ClientV2(API_KEY)
        self.system_message = (
            "You are a sentiment analyzer. I want you to classify the given text if it was the following: 'Very negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'. "
            "State the classfication then generate advice based on the classification (don't generate the same one in every run). "
            "Follow this format. Classification: Advice: . NOTE: Always end with a positive note to make the user feel upbeat, be more casual when speaking as if you're a friend.")
        self.full_chunk = ""
        self.res = ""
        self.score = 0
        self.emotion = ""
        self.advice = ""
        self.emotions = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']

    def chat(self, prompt):

        self.advice = ""
        self.emotion = ""
        self.score = 0
        self.full_chunk = ""  # Add this line to reset the chunk

        try:
            self.res = self.co.chat_stream(
                model="command-a-03-2025",
                messages=[
                    {
                        "role": "system",
                        "content": self.system_message
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            self.reg_ex()

        except Exception as e:
            print(e)

    def reg_ex(self):
        for event in self.res:
            if event:
                if event.type == "content-delta":
                    chunk = event.delta.message.content.text
                    self.full_chunk += str(chunk)

        advice_pattern = r"Advice:\s*(.*)"
        advice_match = re.findall(advice_pattern, self.full_chunk)
        self.advice = "".join(advice_match)

        emotion_pattern = r"(Very Negative|Negative|Neutral|Positive|Very Positive)"
        match = re.search(emotion_pattern, self.full_chunk)
        self.emotion = match.group()

    def confidence_score(self, emotion):
        match emotion:
            case 'Very Negative':
                self.score = random.randrange(0, 24)
            case 'Negative':
                self.score = random.randrange(24, 49)
            case 'Neutral':
                self.score = random.randrange(50, 64)
            case 'Positive':
                self.score = random.randrange(65, 80)
            case 'Very Positive':
                self.score = random.randrange(81, 100)
            case '_':
                self.score = 0
                print('Emotion not recognized. Confidence score set to 0.')
