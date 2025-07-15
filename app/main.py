from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model



def main():

    # API key'i oku
    groq_api_key = os.getenv("GROQ_API_KEY")

    # ChatGroq modelini başlat
    model = init_chat_model("llama3-8b-8192", model_provider="groq")


    while True:

        # Kullanıcıdan mesaj al
        user_message = input("Mesajınız: ")

        if user_message == 'çık':
            break

        # Modelden cevap al
        response = model.invoke([HumanMessage(content=str(user_message))])

        print("Chatbot:", response.content)



   

if __name__ == '__main__':
    print('Project is started.')

    # .env'den değişkenleri yükle
    load_dotenv()

    main()
