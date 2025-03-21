import os
from typing import Dict, Any, Tuple, List
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightGenAgent:
    """Agent responsible for generating insights and questions based on dataset profile summaries"""
    
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.system_message = {
            "role": "system",
            "content": """You are an expert data analyst. Your task is to:
            1. Generate THREE meaningful insight from the dataset profile summary
            2. Choose THREE relevant question from this list of critical questions:
               - What is the main goal of the dashboard? (Understand their objective)
               - What type of data have they uploaded? (Understand the data structure — list, timeline, reviews, etc.)
               - What kind of analysis do they want? (See what happened, understand why, predict future, or suggest actions)
               - What numbers or facts matter most? (Key metrics or facts they want to track)
               - How do they want to see the information? (Charts, tables, timelines — visual preferences)
               - Do they want filters to focus on certain products, regions, or time periods?
               - Who will use this dashboard? (Just them, their team, their manager — audience matters)
            
            The question you choose should be relevant to the insight you generate.
            The three questions must cover the most of the context of the list of critical questions above.
            
            Format your response EXACTLY as:
            <INSIGHT_1>: <your insight> </INSIGHT_1>
            <QUESTION_1>: <selected question> </QUESTION_1>
            <INSIGHT_2>: <your insight> </INSIGHT_2>
            <QUESTION_2>: <selected question> </QUESTION_2>
            <INSIGHT_3>: <your insight> </INSIGHT_3>
            <QUESTION_3>: <selected question> </QUESTION_3>
            """
        }

    def generate_insight_and_question(self, profile_summary: str) -> Tuple[List[str], List[str]]:
        """Generate insights and relevant questions using OpenAI"""
        try:
            # Create user message with the profile summary
            user_message = {
                "role": "user",
                "content": f"Based on this dataset profile summary, generate three insights and create three relevant open-ended questions which are connected to the insights:\n\n{profile_summary}"
            }
            
            # Call OpenAI API with proper message structure
            response = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "", 
                    "X-Title": "",
                },
                model="mistralai/mistral-small-3.1-24b-instruct:free",
                messages=[
                    self.system_message,
                    user_message
                ],
                temperature=0.6,
                max_tokens=2048,
                top_p=1
            )
            
            # Parse response
            content = response.choices[0].message.content
            insights = []
            questions = []
            
            # More robust parsing using string markers
            for tag_type in ['INSIGHT', 'QUESTION']:
                for i in range(1, 4):  # We expect exactly 3 of each
                    start_tag = f'<{tag_type}_{i}>:'
                    end_tag = f'</{tag_type}_{i}>'
                    
                    try:
                        start_idx = content.find(start_tag)
                        if start_idx == -1:
                            logger.error(f"Could not find start tag {start_tag}")
                            continue
                            
                        end_idx = content.find(end_tag, start_idx)
                        if end_idx == -1:
                            logger.error(f"Could not find end tag {end_tag}")
                            continue
                            
                        # Extract the text between start_tag and end_tag
                        text = content[start_idx + len(start_tag):end_idx].strip()
                        
                        if tag_type == 'INSIGHT':
                            insights.append(text)
                        else:
                            questions.append(text)
                            
                    except Exception as e:
                        logger.error(f"Error parsing {tag_type}_{i}: {str(e)}")
            
            # Validate we got the expected number of insights and questions
            if len(insights) != 3 or len(questions) != 3:
                logger.warning(f"Expected 3 insights and 3 questions, but got {len(insights)} insights and {len(questions)} questions")
            
            return insights, questions

        except Exception as e:
            logger.error(f"Error generating insights and questions: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    example_summary = """
   ### Dataset Overview  
- **Time Range**: Both `date_start` and `date_end` are placeholders (same timestamp), indicating no temporal dimension.  
- **Observations**: 5,000 records with **no missing values or duplicates**.  
- **Variables**: 20 columns (1 Text, 13 Numeric, 6 Categorical).  
- **Size**: ~800 KB (efficient for analysis).  

---

### Time Series Characteristics  
- **No time-indexed data**; dataset is static.  

---

### Data Quality  
- **No missing values**, duplicates, or outliers detected.  
- **Key Alerts**:  
  - `[Student_ID]` is unique (as expected for an ID column).  
  - `[Projects_Completed]`, `[Certifications]`, and `[Job_Offers]` have **significant zero-values** (9.3%, 16.3%, and 17%, respectively).  

---

### Variable Analysis  
#### Key Columns:  
| Variable                | Type       | Range/Values                          | Key Stats                          |  
|-------------------------|------------|---------------------------------------|------------------------------------|  
| **Age**                 | Numeric    | 18–29 (mean: 23.4)                    | Narrow range, slightly right-skewed |  
| **Gender**              | Categorical| Male, Female, Other                   | Imbalanced (e.g., "Other" may be rare) |  
| **SAT_Score**           | Numeric    | 900–1600 (mean: 1,254)                | Broad spread, normal-like distribution |  
| **University_Ranking**  | Numeric    | 1–1000 (mean: 504)                    | High variance, skewed toward lower ranks |  
| **Starting_Salary**     | Numeric    | $25k–$101k (mean: $50.6k)             | Median $50.3k, right-skewed         |  
| **Career_Satisfaction** | Numeric    | 1–10 (mean: 5.58)                     | Centered around average satisfaction |  

#### Notable Distributions:  
- **Certifications** and **Job_Offers**: Zero-values may indicate lack of participation or missing data (needs domain context).  
- **University_GPA** and **High_School_GPA**: Both centered around 3.0 on a 4.0 scale.  
- **Entrepreneurship**: Highly imbalanced (92.5% "No").  

---

### Relationships  
- **Potential Correlations to Explore**:  
  - **SAT_Score** ↔ **University_Ranking** (higher SAT scores might correlate with better university rankings).  
  - **University_GPA** ↔ **Job_Offers/Starting_Salary** (academic performance likely impacts career outcomes).  
  - **Soft_Skills_Score** ↔ **Networking_Score** ↔ **Career_Satisfaction** (soft skills and networking may drive satisfaction).  
- **Chi-Squared Alerts**:  
  - **Gender** and **Current_Job_Level** show significant imbalance (p-value = 0.0), suggesting potential bias or stratification.  

---

### Potential Issues & Recommendations  
#### Data Quality:  
1. **Zero-Value Handling**:  
   - Investigate why **Projects_Completed**, **Certifications**, and **Job_Offers** have zeros (e.g., non-participation vs. missing data).  
2. **Categorical Encoding**:  
   - Convert ordinal categories like **Years_to_Promotion** (currently "Categorical") to numeric for analysis.  
   - Encode **Field_of_Study** and **Current_Job_Level** (e.g., one-hot encoding).  

#### Transformations:  
1. **Normalization/Scaling**:  
   - Normalize **SAT_SUniversitycore** and_R **anking** for comparisons.  
2. **Feature Engineering**:  
   - Create composite metrics (e.g., `Total_Achievements = Projects + Certifications`).  
   - Bin **University_Ranking** into tiers (e.g., top 100, 101–500, etc.).  

3. **Address Imbalance**:  
   - For **Entrepreneurship** (92.5% "No"), use oversampling or class weights in models.  

#### Next Steps:  
- Compute **correlation matrices** to identify relationships.  
- Validate if **University_Ranking** is ranked (lower = better) or scaled (higher = better).  
- Explore **multicollinearity** between GPA scores, SAT, and career outcomes.  

---

This dataset is clean but requires careful interpretation of categorical encodings and zero-values. Focus on relationships between academic metrics (GPA, SAT, university rank) and career outcomes (salary, job offers, satisfaction).

    """
    
    agent = InsightGenAgent()
    insights, questions = agent.generate_insight_and_question(example_summary)
    for i, (insight, question) in enumerate(zip(insights, questions), 1):
        print(f"\nInsight {i}: {insight}")
        print(f"Question {i}: {question}")