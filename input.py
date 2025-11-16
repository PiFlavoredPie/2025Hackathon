import chatbot 

def user_prompt():
    client = chatbot.loadAI()
    memory = []
    prompt = input("Hello! What is your first command?")
    
    response = chatbot.response(client, prompt)
    memory = response
    print(response)
    while True:
        prompt = input("")
        if prompt == "stop": 
            break
        response = chatbot.response(client, prompt, memory)
        memory = response
        print(response)
        
    

user_prompt()