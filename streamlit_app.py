import streamlit as st
import pandas as pd
import openai
import re

st.title("📚 YOUR THAI-ENGLISH-CHINESE VOCAB LEARNING TOOL")
st.write(
    "Provide me with several sentences, I will break them down and give you more examples as to how to use them in context!"
)

if user_api := st.text_input("Your API key: ", type="password"):
    client = openai.OpenAI(api_key=user_api)
    with st.form(key="my_form"):
        user_input = st.text_input("Your text...")
        submitted = st.form_submit_button("Submit")

    if submitted:
        prompt = """The input needs to be in Thai, English or Chinese.
                Your goal is to help learners of these three languages develop understandings of the three at the same time, so be comprehensive in extracting words.
                Create only a dictionary designed to be displayed by a Pandas dataframe(table) after performing the following actions: 
                1. Extract essential nouns, verbs, and adjectives "literally" from the input text, limiting at the total of 50, based on the detected language, since the text is not always in Thai.
                - Make sure to include three languages.
                - Make sure to includes pinyin for Chinese in brackets immediately after the Chinese scripts.
                2. Create the first table for each word class, in column 2 with a extracted word and, in columns 3 and 4 with the word translations of the other languages 
                (for example, if the text is in Thai, give meanings and examples in English and Chinese; in Thai and Chinese for English; and in Thai and English for Chinese.). 
                The columns 5 and 6 give **a single example sentence** in the other two languages for **each of the extracted words**. 
                After that, in the last two rows, make "only five sentences" for each language using all the extracted, one row for each language's five sentences.
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
               Important Notes: 
                - Ensure ‘every row’ in the table has ‘consistent length’ 
                (i.e., same number of columns for each row). 
                - Return only the requested variables. Do not include any extra information that could disrupt the code."""

        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{user_input}"}
        ]
    )
        response = completion.choices[0].message.content
        response = response.replace("```", "").strip()
        response = response.replace("python", "").strip()
        response = re.sub(r"\n(\s+)sentences", "\nsentences", response)
        print(response)
        
        # Error Handling
        try:
            # Create DataFrames
                exec(response)
                df_words = pd.DataFrame(data)
                df_sentences = pd.DataFrame(sentences)

                # Display DataFrames in Streamlit
                st.write(df_words)
                st.write(df_sentences)
                
                del df_words, df_sentences
        except (ValueError, SyntaxError) as e:
            # Handle invalid or unsafe code
            st.error(f"Failed to process the response: {e}")
            st.write("Raw Response:", response)

    