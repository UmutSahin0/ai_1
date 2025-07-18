## 1. **Akıllı Araştırma Asistanı (Research Agent)**

### 🧠 ReAct + Tool + Memory + Redis

### 🔧 Özellikler:

- Web araması (search tool), bilgi özeti (LLM), kaynaklı cevap
- LLM’in her düşünce ve aksiyon adımı loglanır
- Kullanıcı geçmişi (chat history) Redis’te tutulur
- Kullanıcı için farklı sohbetler açılıp devam ettirilebilir.
- Aynı soru tekrar sorulursa cevap cache’den (SQLiteCache) döner

### 💾 Teknik Detaylar:

| Katman | Açıklama |
| --- | --- |
| **Memory** | `ConversationBufferMemory` + Redis backend (LangChain'de desteklenir) |
| **Cache** |  SQLiteCache (önbellekten aynı cevabı verir) |
| **History** | Kullanıcıya ait geçmiş konuşmalar Redis'te saklanır, LLM prompt’una eklenir |
| **Tool** | tool_get_system_time / DuckDuckGoSearchRun |
| **Output** | Markdown veya HTML olarak kaynaklı yanıt döner |

