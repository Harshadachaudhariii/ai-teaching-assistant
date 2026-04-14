# from backend.services.chat_service import generate_chat_response

# # common message
# messages = [
#     {"role": "user", "content": "Explain machine learning in simple terms"}
# ]


# print("🟢 Testing Phi-3 Mini (Fast Mode)...\n")
# response2 = generate_chat_response(messages, mode="fast")
# print("Response:\n", response2)


from backend.services.rag_service import generate_rag_response

query = "What is HTML?"

response = generate_rag_response(query)

print(response)