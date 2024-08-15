# Tamil-History-AI-Chatbot
A lot of Sri Lankan history isn't pretty, and it isn't largely shared. Due to censorship and media bias, tamil history has been somewhat forgotten. So, as a part of the Ottawa Tamil Association, I have built an AI Chatbot, fed with hundreds of historical news reports, articles, and papers, to help young tamilians educate and learn about their history.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Overview](#project-overview)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Tamil-History-AI-chatbot.git
cd Tamil-History-AI-history-chatbot
```

2. Install the required dependencies:
Ensure you have Python 3.8+ installed. Then, download the dependencies from the requirements.txt file:

3. Set up environment variables:
- Add your GROQ_API_KEY to the .env file:

4. Install ollama:
Follow the instructions on the Ollama GitHub page or the official website to install the ollama CLI tool.

5. Pull the required model:

6. After installing ollama, run the following command to pull the nomic-embed-text model:
```bash
ollama pull nomic-embed-text
```

## Usage

To start the chatbot, simply run the main function:

Once running, you'll be prompted to ask any question related to Sri Lankan history. The chatbot will generate relevant search queries, retrieve information from a document collection, and provide a concise answer.

