import openai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "Your API Key"

# Function to interact with OpenAI API
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert project planner assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return str(e)

# API Endpoint
@app.route('/generate_project_plan', methods=['POST'])
def generate_project_plan():
    data = request.json
    project_type = data['project_type']
    timeline = data['project_timeline']
    team_size = data['project_team_size']
    languages = data['project_languages']
    sprints = data['project_sprints']

    # Generate Prompt for OpenAI API
    prompt = f"""
    Based on the following project details:
    - Project Type: {project_type}
    - Project Timeline: {timeline} days
    - Team Size: {team_size}
    - Languages: {', '.join(languages)}
    - Number of Sprints: {sprints}

    1. Generate suitable project KPIs (Key Performance Indicators) such as velocity, burndown rate, and defect rate.
    2. Provide Gantt chart details with tasks, start dates, and end dates for each sprint.
    3. Recommend employee criteria for the project, including roles and required skills.
    4. Suggest sprint breakdowns with example tasks for each sprint.
    """

    # Call OpenAI API
    response = generate_response(prompt)

    # Parse the response
    try:
        # Use a structured approach to handle JSON responses (depends on your prompt design)
        response_dict = eval(response)  # Use `json.loads()` if the response is valid JSON
    except Exception as e:
        response_dict = {"error": str(e), "raw_response": response}

    return jsonify(response_dict)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
