import openai 
import pandas as pd
import re


user_api = input("Your API key: ")
user_input = input("Text: ")

prompt = """The input needs to be in Thai, English or Chinese.
            Create only a dictionary designed to be display by a Pandas dataframe(table) after performing the following actions: 
            - Make sure to include three languages.
            - Make sure to includes pinyin for Chinese in brackets immediately after the Chinese scripts.
            1. Extract nouns, verbs, and adjectives from the text, limiting at the total of 50.
            2. Create the first table for each word class, in column 2 with a extracted word and , in columns 3 and 4 with the word 
            translations of the other languages. The columns 5 and 6 give a sentence examples in each language.
            After that, in the last two rows, make five sentences in each language using all the extracted, one row for each language's five sentences.
            - Make sure to follow this format, every row must be of the same length:
              data = {
                "Word Class": ["Noun", ..., "Verb", ..., "Adjective", ...],
                "Extracted Word": [],
                "English Translations": [],
                "Chinese Translations": [],
                "English Examples": [],
                "Chinese Examples": []}
              sentences = {
                "Thai Sentences": [],
                "English Sentences": [],
                "Chinese Sentences": []}
"""

openai.api_key = user_api

completion = openai.ChatCompletion.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": prompt},
    {"role": "user", "content": user_input}
  ]
)



response = completion.choices[0].message["content"]
response = response.replace("```", "").strip()
response = response.replace("python", "").strip()
response = re.sub(r"\n(\s+)sentences", "\nsentences", response)
# print(response)
exec(response)


df_words = pd.DataFrame(data)
df_sentences = pd.DataFrame(sentences)
print(df_words)
print(df_sentences)