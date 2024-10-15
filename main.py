import openai
import json
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
# from secret_key import openai_key



# openai.api_key = openai_key

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''


def extractFinancialData(text):
    prompt = get_prompt_financial() + text
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    content = response.choices[0].message.content
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except (json.JSONDecodeError, IndexError):
        return pd.DataFrame({
            "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
            "Value": ["", "", "", "", ""]
        })


st.title("Financial Data Extractor")
st.write("Enter a news article to extract financial information:")


text_input = st.text_area("News Article:", height=300)


if st.button("Extract Financial Data"):
    if text_input:
        df = extractFinancialData(text_input)
        st.subheader("Extracted Financial Data")
        st.write(df)
    else:
        st.warning("Please enter a news article.")

if __name__ == '__main__':
    st.write("This app extracts financial data from news articles.")
