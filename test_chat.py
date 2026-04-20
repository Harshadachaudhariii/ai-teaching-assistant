# # from backend.services.chat_service import generate_chat_response

# # # common message
# # messages = [
# #     {"role": "user", "content": "Explain machine learning in simple terms"}
# # ]


# # print("🟢 Testing Phi-3 Mini (Fast Mode)...\n")
# # response2 = generate_chat_response(messages, mode="fast")
# # print("Response:\n", response2)


# from backend.services.rag_service import generate_rag_response

# query = "What is HTML?"

# response = generate_rag_response(query)

# print(response)
# for test add backend. 
from backend.services.chat_service import generate_chat_response
import time

# Test input
messages = [
    {"role": "user", "content": "write a code to calculate the factorial of a number in python"}
]

print("🟢 Testing EchoAI with timing...\n")

def test_mode(mode_name):
    print(f"🔹 Testing {mode_name}...\n")

    start_time = time.time()

    response = generate_chat_response(messages, speed=mode_name)

    end_time = time.time()
    total_time = end_time - start_time

    print("Response:\n", response)
    print(f"⏱️ Time Taken: {total_time:.2f} seconds\n")
    print("-" * 50)


# Run tests
test_mode("default")   # phi3-mini
# test_mode("fast")      # phi3-mini
# test_mode("smart")     # llama3