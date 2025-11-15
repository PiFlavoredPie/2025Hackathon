import chatbot 

def user_prompt():
    client = chatbot.loadAI()
    
    prompt = input("Hello! What is your first command?")
    
    response = chatbot.response(client, prompt)
    memory = [response, prompt] 
    print(response)
    while True:
        prompt = input("")
        if prompt == "stop": 
            break
        response = chatbot.response(client, prompt, memory)
        memory = [response, prompt]
        print(response)
        
    

user_prompt()