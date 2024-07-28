from groq import Groq
import os
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import ollama
import chromadb
import time


# Initialize the PersistentClient
client = chromadb.PersistentClient(path=".")
collection_name = "docs"
collection = client.get_collection(name=collection_name)

# print(collection.count())


def ota_speech_chat_completion(client, model, user_question, relevant_excerpts):
    """
    This function generates a response to the user's question using a pre-trained model.
    Parameters:
    client (Groq): The Groq client used to interact with the pre-trained model.
    model (str): The name of the pre-trained model.
    user_question (str): The question asked by the user.
    relevant_excerpts (str): A string containing the most relevant excerpts from articles.
    Returns:
    str: A string containing the response to the user's question.
    """

    # Define the system prompt
    system_prompt = '''
    You are teaching Sri Lankan history. Given the user's question and relevant excerpts from
    articles regarding Tamil and Sri Lankan history, provide concise answers in a way understandable
    to someone with no prior knowledge on the subject. When applicable, make use of numeric statistics
    present in the excerpt and provide precise answers. However, do not explicitly mention the excerpt.
    Make sure your tone is serious and informational: no exclamation marks.
    '''

    # Generate a response to the user's question using the pre-trained model
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "User Question: " + user_question},
            {"role": "assistant", "content": relevant_excerpts}
        ],
        model=model
    )

    # Extract the response from the chat completion
    response = chat_completion.choices[0].message.content
    print(f"time: {chat_completion.usage.total_time}")
    print(f"tokens: {chat_completion.usage.total_tokens}")
    return response

def main():
    """
    This is the main function that runs the application. It initializes the Groq client and the embedding model,
    gets user input from the Streamlit interface, retrieves relevant excerpts from articles based on the user's question,
    generates a response to the user's question using a pre-trained model, and displays the response.
    """
    model = 'llama3-8b-8192'

    # Initialize the embedding function
    # embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Initialize the Groq client
    groq_api_key = os.environ.get('GROQ_API_KEY')
    groq_client = Groq(api_key=groq_api_key)
    
    # print("OTA RAG")
    multiline_text = """
    Welcome! Ask me any question about Sri Lankan history and using information from hundreds of news reports, articles, and papers, will answer whatever question you have. I was built to provide specific information from a unbias point of view on historical events.
    """
    print(multiline_text)

    while True:
        # Get the user's question
        user_question = input("Ask a question: ")

        # Generate embedding for the user's question
        response = ollama.embeddings(
            prompt=user_question,
            model="nomic-embed-text"
        )
        query_embedding = response["embedding"]

        # Query the collection for the most relevant documents
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=4
        )
        
        # Extract the relevant excerpts from the results
        data = "\n\n".join(results['documents'][0])
        ident = results['ids'][0]
        print(data)

        if user_question:
            # Generate a response using the pre-trained model
            response = ota_speech_chat_completion(groq_client, model, user_question, data)
            print(response)

if __name__ == "__main__":
    main()
