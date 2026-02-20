# Centralized Prompt Repository

ASTROLOGY_PROMPT_TEMPLATE = """
Generate astrology-based parenting insight for a child using the following birth details:
Date of Birth: {dob}
Birth Time: {tob}
Birth Place: {place}

Determine Sun Sign and Moon Sign first.

Then provide output strictly in JSON format with the following structure:
{{
  "sun_sign": "Hindi Name (English Name)",  e.g., "Simha (Leo)" or "Kumbh (Aquarius)"
  "moon_sign": "Hindi Name (English Name)"
}}

RULES:
1. TARGET AUDIENCE: Indian Parents. Use simple, warm, and respectful English.
2. SUN/MOON SIGNS: Must be in "Hindi Name (English Name)" format.
"""

INSIGHTS_PROMPT_TEMPLATE = """
Generate in-depth personality traits for a child based on their astrology.

Child Details:
Date of Birth: {dob}
Sun Sign: {sun_sign}
Moon Sign: {moon_sign}

Provide output strictly in JSON format with the following structure:
{{
  "core_personality": [
    {{"trait": "Trait Name", "description": "Description "}}
  ],
  "emotional_needs": [
    {{"need": "Need Name", "description": "Description "}}
  ],
  "strengths": [
    {{"strength": "Strength Name", "description": "Description "}}
  ],
  "growth_areas": [
    {{"area": "Area Name", "description": "Description "}}
  ]
}}

RULES:
1. TARGET AUDIENCE: Indian Parents. Use simple, warm, and respectful English.
2. Keep explanations practical and parenting-focused.
3. Avoid complex words. Use simple words that anyone can understand.
4. Keep tone positive, balanced, and actionable.
5. Provide exactly 5 core personality traits, 5 emotional needs, 5 strengths, and 5 growth areas.
"""

PARENTING_TIPS_PROMPT_TEMPLATE = """
Generate daily parenting tips based on the child's personality.

Child Details:
Age: {age_years} years, {age_months} months
Personality Traits: {personality_traits}
Emotional Needs: {emotional_needs}
Strengths: {strengths}
Growth Areas: {growth_areas}

Provide output strictly in JSON format with the following structure:
{{
  "responsibility": "Give one clear responsibility daily...",
  "appreciation": "...and one moment of appreciation.",
  "balance_advice": "Balance correction with visible praise..."
}}

RULES:
1. Tips must be specific to the child's personality and age.
2. TARGET AUDIENCE: Indian Parents. Use simple, warm, and respectful English.
3. Keep it practical and actionable for today.
"""

DAILY_TASKS_PROMPT_TEMPLATE = """
Generate 5 structured, actionable daily "Missions" for a child. These must be DIRECT COMMANDS that a parent can say to the child.

Child Details:
Age: {age_years} years, {age_months} months

Parenting Focus Today:
- Responsibility: {responsibility_tip}
- Appreciation: {appreciation_tip}
- Balance: {balance_tip}

STRICT INSTRUCTIONS FOR "todo_task":
1. It MUST be a direct command/order that a child can follow immediately.
2. Use strong action verbs like "Put", "Arrange", "Drink", "Say", "Keep", "Finish".
3. NO descriptive sentences like "Encourage him to..." or "Observe if...".
4. The instructions should be simple enough for a {age_years} year old.
5. Context: Indian household (e.g., using terms like "Water bottle", "School bag", "Pranam/Namaste", "Milk").

STARS CALCULATION RULES (Range 10-200):
- EASY (Habits like drinking water, greeting): 10-20 stars.
- MEDIUM (Task involving effort like cleaning table, homework): 30-60 stars.
- HARD (Big independent tasks like cleaning a whole room): 80-150 stars.
- Assign clean numbers (10, 20, 50, 100, etc.).

EXAMPLES OF GOOD TODO_TASKS:
- "Drink one full glass of milk now." | 20 stars
- "Put your dirty school socks in the blue bucket." | 15 stars
- "Arrange all your storybooks neatly on the shelf." | 40 stars
- "Give your finished plate to Mama in the kitchen." | 10 stars
- "Clean your entire study table and put the pens in the stand." | 60 stars

Provide output strictly in JSON format:
{{
  "daily_tasks": [
    {{
      "type": "Discipline Task",
      "title": "Milk Time",
      "description": "Ensuring proper nutrition and habit",
      "todo_task": "Drink your full glass of milk without any fuss.",
      "reward_stars": 20
    }},
    {{
      "type": "Responsibility Task",
      "title": "Laundry Help",
      "description": "Building habit of keeping room clean",
      "todo_task": "Pick up your dirty clothes and put them in the laundry bucket.",
      "reward_stars": 30
    }},
    {{
      "type": "Emotional Maturity Task",
      "title": "Evening Greeting",
      "description": "Teaching respect and social values",
      "todo_task": "Say 'Namaste' or 'Good Evening' to Papa when he comes home.",
      "reward_stars": 15
    }},
    {{
      "type": "Focus Task",
      "title": "Book Organizer",
      "description": "Improving organizational skills",
      "todo_task": "Arrange your school books and notebooks neatly in your bag.",
      "reward_stars": 40
    }},
    {{
      "type": "Confidence Task",
      "title": "Table Cleaner",
      "description": "Taking pride in small household chores",
      "todo_task": "Wipe the dining table clean after your lunch.",
      "reward_stars": 50
    }}
  ]
}}

RULES:
1. Provide exactly 5 tasks.
2. "todo_task" is the MOST IMPORTANT field. It must be a clear command.
3. Language: Simple, warm English suitable for Indian parents.
"""