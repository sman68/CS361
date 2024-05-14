
## Instructions
### Instructions
        1. **Clone this repository:**
            ```bash
            git clone <repository_url>
            cd <repository_directory>
            ```

        2. **Set up the virtual environment and install dependencies:**
            ```bash
            python -m venv venv
            source venv/bin/activate  # On Windows use `venv\Scripts\activate`
            pip install -r requirements.txt
            ```

        3. **Run the your main program:**
            

        4. **Run the average calculator microservice:**
            ```bash
            python average_calculator.py
            ```

### Contact
For any questions or issues, please contact Steven Pamplin at spamplin@gmail.com.


## Communication Contract

### Microservice: Average Calculator

    The average calculator microservice provides endpoints to calculate daily, weekly, and monthly averages of numerical data.

#### Request Data from the Microservice

    To request data from the average calculator, you need to send an HTTP POST request to the appropriate endpoint with the data in JSON format.

##### Endpoints

1. **Calculate Daily Average**
    - **URL:** `http://localhost:5000/average/daily`
    - **Method:** POST
    - **Data Format:**
        ```json
        {
            "data": [
                {
                    "date": "YYYY-MM-DD HH:MM:SS",
                    "amount": <int>
                },
                ...
            ]
        }
        ```
    - **Example Call (Python):**
        ```python
        import requests

        url = 'http://localhost:5000/average/daily'
        data = {
            "data": [
                {"date": "2024-05-08 14:49:01", "amount": 800},
                {"date": "2024-05-08 14:48:52", "amount": 1000}
            ]
        }
        response = requests.post(url, json=data)
        print(response.json())
        ```

2. **Calculate Weekly Average**
    - **URL:** `http://localhost:5000/average/weekly`
    - **Method:** POST
    - **Data Format:** (Same as above)
    - **Example Call (Python):**
        ```python
        import requests

        url = 'http://localhost:5000/average/weekly'
        data = {
            "data": [
                {"date": "2024-05-08 14:49:01", "amount": 800},
                {"date": "2024-05-08 14:48:52", "amount": 1000}
            ]
        }
        response = requests.post(url, json=data)
        print(response.json())
        ```

3. **Calculate Monthly Average**
    - **URL:** `http://localhost:5000/average/monthly`
    - **Method:** POST
    - **Data Format:** (Same as above)
    - **Example Call (Python):**
        ```python
        import requests

        url = 'http://localhost:5000/average/monthly'
        data = {
            "data": [
                {"date": "2024-05-08 14:49:01", "amount": 800},
                {"date": "2024-05-08 14:48:52", "amount": 1000}
            ]
        }
        response = requests.post(url, json=data)
        print(response.json())
        ```

#### Receive Data from the Microservice

    The response from the microservice will be a JSON object containing the average inumerical data for the requested period.

- **Response Format:**
    ```json
    {
        "average": <float>
    }
    ```

- **Example Response:**
    ```json
    {
        "average": 900.0
    }
    ```

### UML Sequence Diagram

Below is the UML sequence diagram that illustrates how requesting and receiving data from the average calculator microservice works.

```plaintext
+-----------+         +-------------------+
|   Client  |         |   Average Service |
+-----------+         +-------------------+
      |                         |
      |    POST /average/daily  |
      |------------------------>|
      |                         |
      |       Calculate Daily Average        |
      |                         |
      |                         |
      |     JSON Response       |
      |<------------------------|
      |                         |
