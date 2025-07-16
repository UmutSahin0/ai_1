#General
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

# for conversation history
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.memory.chat_message_histories import RedisChatMessageHistory

#for cache
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache



from langchain.agents import initialize_agent, AgentType
from tool import tool_get_system_time
from langchain_community.tools import DuckDuckGoSearchRun


from langchain.cache import SQLiteCache

class DebugSQLiteCache(SQLiteCache):
    def lookup(self, prompt: str, llm_string: str):
        result = super().lookup(prompt, llm_string)
        if result is None:
            print("❌ Cache MISS")
        else:
            print("✅ Cache HIT")
        return result

    def update(self, prompt: str, llm_string: str, response):
        print("💾 Storing result in cache")
        return super().update(prompt, llm_string, response)



# Şu anda kapatıldı. Çünkü InMemoryCache yerine SQLiteCache yapısına geçildi.
# class DebugInMemoryCache(InMemoryCache):
#     def lookup(self, prompt: str, llm_string: str):
#         result = super().lookup(prompt, llm_string)
#         if result:
#             print("✅ Cevap CACHE aracılığı ile üretildi.")
#         else:
#             print("❌ Cevap CACHE aracılığı ile üretilmedi. ")
#         return result


def main():
    # ChatGroq modelini başlat
    model = init_chat_model("llama3-8b-8192", model_provider="groq")

    #Redis ile history tutmak için
    history = RedisChatMessageHistory(
    url="redis://localhost:6379",
    session_id="chat-1"
    )

    # Memory oluştur (sadece konuşma geçmişi saklar)
    memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=history , return_messages=True)
    search = DuckDuckGoSearchRun()
    
    # 🛠️ Araçları tanımla   
    tools = [tool_get_system_time,search]


    # 🧠 Agent başlat
    agent = initialize_agent(
        tools=tools,
        llm=model,
        memory=memory,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION  ,
        verbose=True,
    )

    while True:

        # Kullanıcıdan mesaj al
        user_message = input("Mesajınız: ")

        if user_message == 'çık':
            break

        # Modelden cevap al - Bu kısım çıkartıldı. Çünkü history tutma eklendi. Bu şekilde invoke yapılınca tutulmuyordu.
        #response = model.invoke([HumanMessage(content=str(user_message))])

        # Kullanıcıdan gelen mesajları zincire gönder
        response = agent.run(input=user_message)
        print("Chatbot:", response)



   

if __name__ == '__main__':
    print('Project is started.')

    # .env'den değişkenleri yükle
    load_dotenv()

    # API key'i oku
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # 🔁 CACHE yapılandırması
    #set_llm_cache(DebugInMemoryCache())  Kalıcı cache'e geçildiği için şu anda iptal edildi.
    set_llm_cache(DebugSQLiteCache(database_path="../cache/.langchain_cache.db"))

    main()
