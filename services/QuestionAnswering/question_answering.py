import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient, models as qna


def answer_question(question):
    key = os.environ['AI_LANGUAGE_KEY']
    credential = AzureKeyCredential(key)
    endpoint = os.environ['AI_LANGUAGE_ENDPOINT']
    client = QuestionAnsweringClient(endpoint, credential)

    # Not Custom QA, this is just QA
    # LImited to 5 docs
    
    # For Custom QA - 
    # Azure AI Search - searches for the actual question and answer pair based on the prompt

    faq_path = 'services/QuestionAnswering/SurfacePro9.txt'

    with open(faq_path) as f:
        faq = f.readlines()
    
    input = qna.AnswersFromTextOptions(
        question=question,
        text_documents=faq
    )

    output = client.get_answers_from_text(input)
    answer = output.answers[0]
    print(f"Q: {input.question}")
    print(f"A: {answer.answer}")
    print(f"Confidence Score: {answer.confidence}")


if __name__ == "__main__":
    question = "How heavy is the Surface Pro 9?"
    answer_question(question)

    