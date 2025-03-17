import openai
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

# Set your OpenAI API key
openai.api_key = "Your API Key"


def generate_response(prompt):
    """
    Function to send a prompt to OpenAI API and retrieve a response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert project planner assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return str(e)


def generate_complex_kpis(team_size, sprints, timeline):
    """
    Generate realistic KPIs for a software engineering project.
    """
    # Average story points per sprint
    velocity = random.randint(20, 50) * team_size

    # Cycle time: avg. time (in hours) to complete a task
    cycle_time = round(random.uniform(4, 12), 2)

    # Code coverage: percentage of code covered by automated tests
    code_coverage = random.randint(60, 95)

    # Defect rate: defects per 1,000 lines of code
    defect_rate = round(random.uniform(0.5, 5.0), 2)

    # Sprint predictability: completed work vs. planned work
    predictability = round(random.uniform(0.8, 1.0), 2) * 100  # Percentage

    # Burn rate: cost per sprint (assume $1,000 per team member per sprint)
    burn_rate = team_size * 1000 * sprints

    return {
        "velocity": f"{velocity} story points per sprint",
        "cycle_time": f"{cycle_time} hours per task",
        "code_coverage": f"{code_coverage}%",
        "defect_rate": f"{defect_rate} defects per 1,000 LOC",
        "sprint_predictability": f"{predictability}%",
        "burn_rate": f"${burn_rate} total cost"
    }


def create_gantt_chart_days(gantt_data):
    """
    Create a Gantt chart with days (Day 1, Day 5, etc.) as the x-axis.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, task in enumerate(gantt_data):
        # Convert "Day X" to day numbers
        start_day = int(task["Start"].split(" ")[1])
        end_day = int(task["End"].split(" ")[1])

        # Plot each task as a horizontal bar
        ax.barh(task["Task"], end_day - start_day, left=start_day, color="skyblue")

    # Formatting the chart
    ax.set_xlabel("Days")
    ax.set_ylabel("Tasks")
    ax.set_title("Gantt Chart")
    ax.grid(True)

    plt.tight_layout()
    plt.savefig("gantt_chart_days.png")
    plt.close()
    print("Gantt chart saved as gantt_chart_days.png")


def create_burndown_chart(timeline, sprints):
    """
    Create a burndown chart based on timeline and sprints.
    """
    sprint_days = timeline // sprints
    x = [i * sprint_days for i in range(sprints + 1)]
    ideal_burndown = [timeline - i for i in x]
    actual_burndown = [timeline - (i + 1) * sprint_days + (i * random.randint(-2, 2)) for i in range(sprints + 1)]

    plt.figure(figsize=(10, 6))
    plt.plot(x, ideal_burndown, label="Ideal Burndown", marker="o", linestyle="--")
    plt.plot(x, actual_burndown, label="Actual Burndown", marker="o")
    plt.xlabel("Days")
    plt.ylabel("Work Remaining")
    plt.title("Burndown Chart")
    plt.legend()
    plt.grid(True)
    plt.savefig("burndown_chart.png")
    plt.close()
    print("Burndown chart saved as burndown_chart.png")


def main():
    # Input project details
    project_details = {
        "project_type": "Web Development",
        "project_timeline": 90,  # in days
        "project_team_size": 5,
        "project_languages": ["Python", "JavaScript"],
        "project_sprints": 5
    }

    # Generate complex KPIs
    kpis = generate_complex_kpis(
        team_size=project_details["project_team_size"],
        sprints=project_details["project_sprints"],
        timeline=project_details["project_timeline"]
    )
    print("\nGenerated KPIs:")
    print(json.dumps(kpis, indent=4))

    # Create a JSON-specific prompt for OpenAI API
    prompt = f"""
    Based on the following project details:
    - Project Type: {project_details['project_type']}
    - Project Timeline: {project_details['project_timeline']} days
    - Team Size: {project_details['project_team_size']}
    - Languages: {', '.join(project_details['project_languages'])}
    - Number of Sprints: {project_details['project_sprints']}

    Return the following details as a JSON object:
    {{
        "GanttChartDetails": [
            {{
                "Task": "Task description",
                "Start": "Day X",
                "End": "Day Y"
            }}
        ],
        "EmployeeCriteria": [
            {{
                "role": "Role of the employee",
                "skills": ["List of required skills"]
            }}
        ],
        "SprintBreakdown": {{
            "Sprint 1": ["List of tasks for Sprint 1"],
            "Sprint 2": ["List of tasks for Sprint 2"],
            "Sprint 3": ["List of tasks for Sprint 3"],
            "Sprint 4": ["List of tasks for Sprint 4"],
            "Sprint 5": ["List of tasks for Sprint 5"]
        }}
    }}
    """

    # Get the response from OpenAI API
    response = generate_response(prompt)

    # Attempt to parse the response as JSON
    try:
        response_data = json.loads(response)
    except json.JSONDecodeError:
        response_data = {"error": "Failed to parse response as JSON", "raw_response": response}

    # Print results
    if "error" in response_data:
        print("Error:", response_data["error"])
        print("Raw Response:", response_data["raw_response"])
    else:
        print("\nGenerated Project Plan:")
        print(json.dumps(response_data, indent=4))

        # Save Gantt chart details to a CSV and generate Gantt chart
        if "GanttChartDetails" in response_data:
            gantt_details = response_data["GanttChartDetails"]
            df = pd.DataFrame(gantt_details)
            df.to_csv("gantt_chart_details.csv", index=False)
            print("\nGantt chart details saved to gantt_chart_details.csv")
            create_gantt_chart_days(gantt_details)

        # Generate Burndown Chart
        create_burndown_chart(
            timeline=project_details["project_timeline"],
            sprints=project_details["project_sprints"]
        )


if __name__ == "__main__":
    main()
