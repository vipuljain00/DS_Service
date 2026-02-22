# DS_Service (Data Service)

DS_Service is a Python Flask application that acts as the data extraction layer in the Expense Tracker ecosystem. It receives bank SMS messages from the user's device, uses a Mistral LLM (via LangChain) to determine if the message is a bank debit transaction, extracts structured expense data from it, and publishes the extracted data to a Kafka topic (`ExpenseDetails`) for downstream consumption by the ExpenseService.

## Key Features

- **Flask REST API**: Provides a lightweight HTTP endpoint for receiving bank SMS messages.
- **LLM-Powered Data Extraction**: Uses the Mistral AI model (via LangChain) to intelligently parse and extract expense details (amount, merchant, currency, date) from bank messages.
- **Bank SMS Detection**: Includes a utility that uses regex-based keyword matching to identify whether a message is a bank transaction SMS.
- **Kafka Producer**: Publishes extracted expense data to the `ExpenseDetails` Kafka topic for consumption by the ExpenseService.
- **Structured Output**: Uses Pydantic models for validated, structured LLM output.
- **Environment-Based Configuration**: Loads API keys and model configuration from a `.env` file.

## Main Components

- **Application Entry Point**
  - `src/__init__.py`: Sets up the Flask application, Kafka producer, and defines the REST API routes:
    - `POST /v1/ds/message/` — Accepts a bank SMS message, processes it, and publishes extracted expense data to Kafka.
    - `GET /` — Health check endpoint.

- **Services**
  - `MessageService` (`app/service/messageService.py`): Orchestrates the message processing pipeline. Uses `MessageUtil` to check if the message is a bank SMS, then invokes `LLMService` to extract data.
  - `LLMService` (`app/service/llmService.py`): Configures and runs the Mistral AI LLM via LangChain. Uses a `ChatPromptTemplate` to instruct the model to extract structured expense data from bank messages. Outputs data conforming to the `ExpenseDataModal` schema.

- **Data Models**
  - `ExpenseDataModal` (`app/dataModal/ExpenseDataModal.py`): Pydantic model defining the structured output schema for expense data. Fields include:
    - `amount` — Amount of the expense.
    - `merchant` — Merchant name to whom the expense is made.
    - `currency` — Currency of the transaction.
    - `createdAt` — Date and time when the expense was created.

- **Utilities**
  - `MessageUtil` (`app/utils/messageUtil.py`): Provides a regex-based `isBankSms` method that checks for banking-related keywords (e.g., `bank`, `debit`, `credit`, `upi`, `neft`, `imps`, `transfer`, etc.) to determine if a message is a bank transaction SMS.

- **Configuration**
  - `config.py` (`app/config.py`): Placeholder for application configuration.
  - `.env`: Stores environment variables including `MISTRAL_API_KEY` and `MODEL_NAME`.

## Getting Started

1. **Clone the repository**
   `git clone https://github.com/vipuljain00/DS_Service.git`

2. **Set up a Python virtual environment**
   ```bash
   python -m venv dsenv
   source dsenv/bin/activate   # On Linux/Mac
   dsenv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install flask langchain langchain-mistralai pydantic python-dotenv kafka-python
   ```

4. **Configure environment variables**
   Create or update the `.env` file in the project root:
   ```env
   MISTRAL_API_KEY=<your-mistral-api-key>
   MODEL_NAME=mistral-large-latest
   ```

5. **Configure Kafka**
   Update the Kafka bootstrap server address in `src/__init__.py` if needed:
   ```python
   producer = KafkaProducer(
       bootstrap_servers='<kafka-host>:9093',
       value_serializer=lambda v: json.dumps(v).encode('utf-8')
   )
   ```

6. **Run the application**
   ```bash
   python src/__init__.py
   ```
   The server will start on `http://localhost:3000`.

7. **API Usage**
   - Send a bank SMS for processing:
     ```bash
     curl -X POST http://localhost:3000/v1/ds/message/ \
       -H "Content-Type: application/json" \
       -d '{"message": "Your A/C XXXX1234 has been debited by Rs.500.00 on 22-02-2026 at AMAZON. Avl Bal: Rs.10000.00"}'
     ```
   - The service will extract expense details and publish them to the `ExpenseDetails` Kafka topic.

## Technologies Used

- Python
- Flask
- LangChain
- Mistral AI (LLM)
- Pydantic
- Apache Kafka (kafka-python)
- python-dotenv

## License

This project is currently unlicensed.

---
For any queries or contributions, please visit the [GitHub repository](https://github.com/vipuljain00/DS_Service).
