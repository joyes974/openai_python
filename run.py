import openai 
import sys
  
# assigning API KEY to initialize openai environment 
openai.api_key = ''

def completion(PROMPT, MaxToken=50, outputs=3):
    response = openai.Completion.create( 
        # model name used here is text-davinci-003 
        # there are many other models available under the  
        # umbrella of GPT-3 
        model="text-davinci-003", 
        # passing the user input  
        prompt=PROMPT, 
        # generated output can have "max_tokens" number of tokens  
        max_tokens=MaxToken, 
        # number of outputs generated in one call 
        n=outputs 
    ) 
    # creating a list to store all the outputs 
    output = list() 
    for k in response['choices']: 
        output.append(k['text'].strip()) 
    # returning the output
    return output

def completion_with_files(input_file, output_file, MaxToken=3000, outputs=1):
    # Read the prompt from the input file
    with open(input_file, 'r') as file:
        prompt = file.read()

    response = openai.Completion.create( 
        # model name used here is text-davinci-003 
        # there are many other models available under the  
        # umbrella of GPT-3 
        model="gpt-3.5-turbo-instruct", 
        # passing the user input  
        prompt=prompt, 
        # generated output can have "max_tokens" number of tokens  
        max_tokens=MaxToken, 
        # number of outputs generated in one call 
        n=outputs 
        # temperature=0.7
        #temperature=0
    ) 
    

    # creating a list to store all the outputs 
    output = list() 
    for k in response['choices']: 
        output.append(k['text'].strip()) 

    #convert the list to string
    output = '\n'.join(output)

    # Write the reply to the output file
    with open(output_file, 'w') as file:
        file.write(output)

# re write the completion_with_files function for ChatCompletion endpoints
def chat_completion_with_files(input_file, output_file, MaxToken=3000, outputs=1):
    # Read the prompt from the input file
    with open(input_file, 'r') as file:
        prompt = file.read()

    response = openai.ChatCompletion.create( 
        # model name used here is text-davinci-003 
        # there are many other models available under the  
        # umbrella of GPT-3 
        model="gpt-3.5-turbo", 
        # passing the user input  
        messages=[{"role": "system", "content": prompt}], 
        # generated output can have "max_tokens" number of tokens  
        max_tokens=MaxToken, 
        # number of outputs generated in one call 
        n=outputs 
        # temperature=0.7
        #temperature=0
    ) 

    # creating a list to store all the outputs 
    output = list() 
    for k in response['choices']: 
        output.append(k['message']['content'].strip()) 

    #convert the list to string
    output = '\n'.join(output)

    # Write the reply to the output file
    with open(output_file, 'w') as file:
        file.write(output)

def dynamic_completion_with_files(input_file, output_file, MaxToken=3000, outputs=1):
    age_group = ["Age 18-29", "Age 30-49", "Age 50-64", "Age 65+"]
    question = "How much, if at all, do you worry about being the victim of a violent crime?"
    # initialize an empty set
    pair = set()
    for age in age_group:
        # Read the prompt from the input file
        with open(input_file, 'r') as file:
            prompt = file.read()

        # prompt has 3 variable in string format, we need to replace them with the actual values. variables are {{$question}}, {{g1}}, {{g2}}. g1 and g2 are the age groups and we need to replace them with the actual age group. We need to pass the combination of 2 age group every time to compare between each age group.
        prompt = prompt.replace("{{$g1}}", age)
        prompt = prompt.replace("{{$question}}", question)        
        for age2 in age_group:
            # skip if the current comparison pair is already compared
            if frozenset([age, age2]) in pair:
                continue                        
            # skip the same age group
            if age == age2:
                continue
            prompt = prompt.replace("{{$g2}}", age2)           

            response = openai.Completion.create( 
                # model name used here is text-davinci-003 
                # there are many other models available under the  
                # umbrella of GPT-3 
                model="gpt-3.5-turbo-instruct", 
                # passing the user input  
                prompt=prompt, 
                # generated output can have "max_tokens" number of tokens  
                max_tokens=MaxToken, 
                # number of outputs generated in one call 
                n=outputs 
                # temperature=0.7
                #temperature=0
            ) 

            # creating a list to store all the outputs 
            output = list() 
            for k in response['choices']: 
                output.append(k['text'].strip()) 

            #convert the list to string
            output = '\n'.join(output)

            # Write the reply to the output file
            with open(output_file, 'a') as file:
                file.write(output + "\n\n")

            # store the pair of age group in a set
            pair.add(frozenset([age, age2]))

# rewrite the dynamic_completion_with_files function for ChatCompletion endpoints
def dynamic_chat_completion_with_files(input_file, output_file, MaxToken=3000, outputs=1):
    age_group = ["Age 18-29", "Age 30-49", "Age 50-64", "Age 65+"]
    question = "How much, if at all, do you worry about being the victim of a violent crime?"
    # initialize an empty set
    pair = set()
    for age in age_group:
        # Read the prompt from the input file
        with open(input_file, 'r') as file:
            prompt = file.read()

        # prompt has 3 variable in string format, we need to replace them with the actual values. variables are {{$question}}, {{g1}}, {{g2}}. g1 and g2 are the age groups and we need to replace them with the actual age group. We need to pass the combination of 2 age group every time to compare between each age group.
        prompt = prompt.replace("{{$g1}}", age)
        prompt = prompt.replace("{{$question}}", question)        
        for age2 in age_group:
            # skip if the current comparison pair is already compared
            if frozenset([age, age2]) in pair:
                continue                        
            # skip the same age group
            if age == age2:
                continue
            prompt = prompt.replace("{{$g2}}", age2)           

            response = openai.ChatCompletion.create( 
                # model name used here is text-davinci-003 
                # there are many other models available under the  
                # umbrella of GPT-3 
                model="gpt-3.5-turbo", 
                # passing the user input  
                messages=[{"role": "system", "content": prompt}], 
                # generated output can have "max_tokens" number of tokens  
                max_tokens=MaxToken, 
                # number of outputs generated in one call 
                n=outputs 
                # temperature=0.7
                #temperature=0
            ) 

            # creating a list to store all the outputs 
            output = list() 
            for k in response['choices']: 
                output.append(k['message']['content'].strip()) 

            #convert the list to string
            output = '\n'.join(output)

            # Write the reply to the output file
            with open(output_file, 'a') as file:
                file.write(output + "\n\n")



def main():
    # Path: run.py. Accept arguments from command line
    folder = sys.argv[3]
    input_file = folder + '/' + sys.argv[1]
    output_file = folder + '/' + sys.argv[2] 
    
    dynamic_chat_completion_with_files(input_file, output_file)

if __name__ == "__main__":
    main()
        