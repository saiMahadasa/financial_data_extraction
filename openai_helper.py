import openai
import json
import pandas as pd
from secret_key import openai_key
openai.api_key = openai_key



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
        return pd.DataFrame(data.items() , columns = ["Measure" , "Value"])
    except (json.JSONDecodeError , IndexError):
        pass

    return pd.DataFrame({
        "Measure" : ["Company Name" , "Stock Symbol", "Revenue" , "Net Income" , "EPS"],
        "Value" : ["" , "" , "" , "", ""]
    })



if __name__ == '__main__':
    text = '''
    Tesla
 reported weaker-than-expected earnings for the second quarter as automotive sales dropped for a second straight period. The stock slid more than 8% in extended trading.

Earnings per share: 52 cents adjusted vs 62 cents expected, per LSEG consensus estimates.
Revenue: $25.50 billion vs. $24.77 billion expected by LSEG
Revenue increased 2% from $24.93 billion a year earlier, Tesla said in an investor deck on Tuesday. But automotive revenue dropped 7% to $19.9 billion from $21.27 billion in the same quarter a year ago. Auto revenue included regulatory credits of $890 million, more than triple the figure from last year.

The company said it “recognized record regulatory credit revenues in Q2,” pointing to the fact that other automakers are “still behind on meeting emissions requirements.”

After a rocky first half of the year that saw Tesla cut more than 10% of headcount, the company reported better-than-expected deliveries for the second quarter earlier this month. However, deliveries were still down from a year earlier for a second straight period.


CEO Elon Musk said, in opening remarks on Tuesday’s earnings call that Tesla will host a robotaxi unveiling event on Oct. 10 Originally, he said the event would take place on Aug. 8.

Musk was asked in the Q&A portion of the call when shareholders can expect “the first robotaxi ride.”

“I would be shocked if we cannot do it next year,” Musk said, after first noting that his predictions have been “overly optimistic in the past.”

Musk has been promising since about 2016 that Tesla will turn its existing EVs into self-driving vehicles with software updates, which the company calls Full Self-Driving. Tesla is separately working on a CyberCab dedicated robotaxi.

On Tuesday’s call, Musk said he doesn’t foresee regulatory hurdles to rolling out Tesla’s self-driving technology to a broad market in the U.S. and beyond.

He also referred to Waymo’s commercial robotaxi services as “limited” and “fragile.” Tesla’s system, he said, should be able to work anywhere in the world, not just in a geographically-limited area.

As of April, NBC News first reported, Tesla hadn’t contacted regulators in the states of Arizona, California and Nevada, to apply for the licenses and permits needed to test autonomous vehicles without a human driver at the wheel, or to run a commercial robotaxi service.

A deserted array of Tesla charging stations is viewed on June 19, 2024 in Kettleman City, California.
A deserted array of Tesla charging stations in Kettleman City, California, on June 19, 2024.
George Rose | Getty Images
Tesla remains the top seller of electric vehicles in the U.S. by far, but is losing market share to a growing number of rivals due in part to its aging lineup of sedans and SUVs and the impact of Musk’s incendiary and political commentary.

During the quarter, Tesla offered discounts and other incentives, including subsidized financing deals, in China and the U.S. to spur demand. Those deals hit the company’s profitability, with its adjusted earnings margin falling to 14.4% from 18.7% in the second quarter of 2023.

Tesla shares are down about 0.5% for the year at Tuesday’s close, while the Nasdaq is up about 20% over that stretch.

Rival automakers saw a 33% year-over-year jump in fully electric vehicle sales in the U.S. during the first half of 2024, while Tesla sales dropped by 9.6% in that time frame, according to data tracked by Cox Automotive, InsideEVs reported.

Net income at Tesla declined 45% to $1.48 billion, or 42 cents a share, in the second quarter from $2.7 billion, or 78 cents a share, a year earlier.

Revenue in Tesla’s energy generation and storage business, which sells and installs big backup batteries for residential, commercial and utility use, almost doubled from the same quarter a year ago to just over $3 billion. The company said its Megapack and Powerwall “achieved record deployment” in the period.

Of late, Musk has been in the headlines more for his political views than for Tesla’s performance.

Musk has reportedly said he is planning to pledge about $45 million a month to a newly formed political action committee backing former President Donald Trump, but has yet to donate to that group as of the end of June, according to its latest quarterly financial filing. Musk publicly endorsed Trump after the assassination attempt at a political rally on July 13.


While only 13% of Republican and right-leaning voters are interested in purchasing a fully electric vehicle this year, according to Pew Research, 45% of Democratic and left-leaning voters are very or somewhat interested.

During the second quarter, Tesla increased production of its newest model EV — the angular, steel Cybertruck — which the company now says is “on track to achieve profitability by end of year.”

In 2021, Musk also began to promise that Tesla would develop and produce humanoid robots capable of factory work and potentially other tasks. On Monday, Musk said in a post on X that he expects Tesla will have some of these robots working in its factories next year with more available for use by other companies in 2026.

Tesla has “paused” its plans to build cars in Mexico. “Trump has said he will put heavy tariffs on vehicles produced in Mexico,” Musk said. He added that the company is increasing production at its existing factories, and plans to manufacture its robotaxi and Optimus at its headquarters in Austin, Texas.

Capital expenditures in the quarter increased 10% from a year ago to $2.27 billion. The company said it incurred $600 million in expenses for artificial intelligence infrastructure.
    '''
    df = extractFinancialData(text)
    print(df.to_string())