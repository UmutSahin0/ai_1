#General
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

# for conversation history
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

#for cache
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

class DebugInMemoryCache(InMemoryCache):
    def lookup(self, prompt: str, llm_string: str):
        result = super().lookup(prompt, llm_string)
        if result:
            print("✅ Cevap CACHE aracılığı ile üretildi.")
        else:
            print("❌ Cevap LLM aracılığı ile üretildi. ")
        return result


def main():
    # ChatGroq modelini başlat
    model = init_chat_model("llama3-8b-8192", model_provider="groq")

    # Memory oluştur (sadece konuşma geçmişi saklar)
    memory = ConversationBufferMemory()

    # Konuşma zinciri oluştur
    conversation = ConversationChain(
        llm=model,
        memory=memory,
        verbose = True
    )

    while True:

        # Kullanıcıdan mesaj al
        user_message = input("Mesajınız: ")

        if user_message == 'çık':
            break

        # Modelden cevap al - Bu kısım çıkartıldı. Çünkü history tutma eklendi. Bu şekilde invoke yapılınca tutulmuyordu.
        response = model.invoke([HumanMessage(content=str(user_message))])

        # Kullanıcıdan gelen mesajları zincire gönder
        #response = conversation.predict(input=user_message)
        print("Chatbot:", response)



   

if __name__ == '__main__':
    print('Project is started.')

    # .env'den değişkenleri yükle
    load_dotenv()

    # API key'i oku
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # 🔁 CACHE yapılandırması
    set_llm_cache(DebugInMemoryCache())

    main()
