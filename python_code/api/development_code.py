from agents import (GuardAgent,
                    ClassificationAgent,
                    DetailsAgent,
                    AgentProtocol,
                    RecommendationAgent
                    )
from typing import Dict                    
import os
import sys
import pathlib
folder_path = pathlib.Path(__file__).parent.resolve()

def main():
    pass
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()

    agent_dict: Dict[str,AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "recommendation_agent": RecommendationAgent(
                                    os.path.join(folder_path, "recommendation_objects/apriori_recommendations.json"),
                                    os.path.join(folder_path, "recommendation_objects/popularity_recommendation.csv")
                               )
    }


    messages = []
    while True:
        # os.system('cls' if os.name == 'nt' else 'clear')

        print("\n\n Print Messages ...............")
        for message in messages:
            print(f"{message['role']}:{message['content'] }")

        # Get user input 
        prompt=input("User: ")
        message.append({'role':'user', 'content':prompt})

        # Get Guard Agent's response
        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            continue

        # Get Classification Agent's response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent["memory"]["classification_decision"]    
        print("Chosen Agent: ", chosen_agent)

        # Get the response from the chosen agent
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)

        messages.append(response)

if __name__ == '__main__':
    main()
   