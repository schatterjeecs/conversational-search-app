# conversational-search-app
!Disclaimer : This is just for education purpose, you can extend the code and use in your application as per your requirement.

The application provides a RESTful API that allows clients to upload files (pdf, csv, txt), generates a conversational retrieval model using LangChain and OpenAI, and performs searches on the generated model. It combines file text processing, vectorization, and a conversational retrieval chain to facilitate intelligent question-answering capabilities.

## Local Setup

- Create virtual environment
`python -m venv venv`
- Install the libraries from requirements.txt file
`pip install -r requirements.txt`
- Run the Application
`uvicorn driver:app --reload`

#### Prerequisites
Create token in OpenAPI and replace in .env file

## Code Walkthrough
The provided application is a FastAPI-based web service that incorporates a conversational retrieval model for searching and generating responses. Here's a summary of its main components and functionality:

- The application consists of multiple routes and endpoints, including `/healthcheck`, `/genmodel`, and `/search`.
- It utilizes the `Model` class, which encapsulates the logic for processing PDF documents, creating conversational retrieval chains, and generating responses.
- The `/healthcheck` endpoint performs a basic health check and returns an "OK" message to indicate that the service is running.
- The `/genmodel` endpoint accepts either a list of uploaded PDF files (`pdf_docs`) or a URL (`url`) as parameters. It performs validation checks on the uploaded files' extensions and calls the `model_data` method of the `Model` class to generate a conversational retrieval chain based on the provided data.
- The `/search` endpoint expects a JSON payload containing a search query. It retrieves the query, retrieves the conversational retrieval chain from the `Model` class, and uses it to generate a response to the query. The generated response is appended to a `chat_history` list, and the answer is returned.
- The application includes error handling for various scenarios, such as missing parameters, invalid file extensions, and attempts to use the `/search` endpoint before generating a model.
- The application sets up the FastAPI app, initializes the `Model` object, and establishes environmental variables required for API keys.
- The application leverages Pydantic's `BaseModel` for defining the search query data model.
- The application imports the necessary modules, such as requests and BeautifulSoup, for performing web scraping.
- The web_scrap_to_text method within the Model class is responsible for web scraping. It takes a URL as input, sends a request to the URL using the requests module, and then uses BeautifulSoup to parse the HTML content.
- The method extracts the title and paragraphs from the HTML and returns the concatenated text.


The app defines a DB class, which appears to be a simple in-memory database-like storage mechanism. Here's a summary of the class and its functionality:
- The DB class has an __init__ method that initializes an empty string db_data, which serves as the storage for the data.
- The store_data method takes a data parameter and assigns its value to the db_data attribute. This method overwrites any previously stored data with the new data.
- The get_data method returns the value stored in the db_data attribute, allowing retrieval of the stored data.


In summary, the application supports web scraping functionality by utilizing the requests module to retrieve HTML content from a given URL and BeautifulSoup to parse and extract text from the HTML. The extracted text is incorporated into the model generation process along with the PDF text content.