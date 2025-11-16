import chatbot 
import subprocess

def user_prompt():
    client = chatbot.loadAI()
   
    memory = []
    
    
    while True:
        
        prompt = input("")
        
        memory.append({"role": "user", "content": prompt})
        
    
        if prompt == "stop": 
            break
        response = chatbot.response(client, prompt, memory)
        memory.append({"role": "assitant", "content": response})
        
        print(response)
        lines = response.split("\n")
        for line in lines:
            if "python3" in line:
                python, command = line.split()
                if input("Press N to cancel") == "N":
                    pass
                else:
                    subprocess.run([python, command])
                
                
            
            
        
    

user_prompt()