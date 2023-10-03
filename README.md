# Board Game Geek Data Analysis Project

This project aims to gather and analyze data from the Board Game Geek (BGG) XML API2, using a combination of technologies including pandasai, langchain, OpenAI, and Streamlit. The end goal is to create a chatbot that can explain and analyze the data in a user-friendly manner.

## Project Overview

1. **Data Gathering**: We use the BGG XML API2 to gather data about board games. This includes data such as game names, user ratings, play counts, and more.

2. **Data Analysis**: We use pandasai and langchain to process and analyze the data. This allows us to gain insights into trends in the board game industry, such as popular games, user preferences, and more.

3. **Chatbot Creation**: We use OpenAI to power a chatbot that can interact with users. The chatbot can answer questions about the data, provide explanations of the analysis results, and more.

4. **User Interface**: We use Streamlit to create a user-friendly interface for the chatbot. This allows users to interact with the chatbot in a natural, conversational manner.

## Getting Started

This project uses Poetry for dependency management. To get started, install Poetry and the project dependencies:

```bash
pip install poetry
poetry install
```

Once the dependencies are installed, you can run the project locally using Streamlit:

```bash
streamlit run bggapi/app.py
```

## Deployment

This application is deployed on Google Cloud using a Kubernetes cluster. Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. 

In our setup, we use a LoadBalancer service, which exposes the application to the internet by assigning it a fixed, external IP address. The application is accessible at [bgg-copilot.com](http://bgg-copilot.com). The deployment process involves building a Docker image of the application, pushing it to the Google Container Registry, and updating the Kubernetes deployment to use the new image. This ensures that the live application is always running the latest version of the code.