# Weather and Time Agent

This project implements an AI agent using the `google-adk` framework. The agent can provide current weather and time information for cities worldwide.

## Description

The core of this project is the `weather_time_agent`, which is equipped with two main tools:

1.  **`get_current_time(city)`**: Retrieves the current time for a given city or an IANA timezone (e.g., `America/New_York`). It can resolve ambiguous city names by suggesting a list of possible timezones.
2.  **`get_weather(city)`**: Provides the current weather for a specified city. (Note: This is currently a sample implementation with fixed data.)

This agent is built using `litellm` to connect to a language model and interprets user requests to call the appropriate tools.

## Installation

1.  **Set up the Python virtual environment:**
    ```bash
    make setup
    ```

2.  **Install the required dependencies:**
    ```bash
    make install
    ```

3.  **Add .env into adk_agent folder**
    ```
    LITELLM_MODEL_API_KEY=
    LITELLM_MODEL_API_BASE=
    LITELLM_MODEL_MODEL_NAME=openai/
    ```

## Usage

To start the agent server, run the following command:

```bash
make run
```

This will launch the ADK web interface, where you can interact with the agent.

## Agent Details

-   **Name**: `weather_time_agent`
-   **Description**: An agent designed to answer questions about the time and weather in a city.
-   **Instructions**: The agent is instructed to be a helpful assistant that can handle queries about global time and weather. It attempts to resolve city names to IANA timezones and will ask for clarification if a city name is ambiguous.

### Tools

-   `get_current_time(city: str) -> dict`
-   `get_weather(city: str) -> dict`

## Dependencies

-   `google-adk`
-   `python-dotenv`
-   `litellm`
