import datetime
import openai
import datetime
import io
import zipfile


def open_file(filepath:str)-> str:
    '''Opens and reads a file'''
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def gpt3_completion(prompt, engine='text-davinci-003', temp=0, 
                    top_p=1.0, tokens=300, freq_pen=0.0, pres_pen=0.0, 
                    ):
    """Performs text completion using OpenAI's text-davinci-003 model"""
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen)
    text = response['choices'][0]['text'].strip()
    return text


def gpt3_chat(message: str, messages:list[dict])-> tuple[str, list]:
    '''Returns GPT's response to the input message and appends it to the messages list'''
    messages.append({"role": "user", "content": message})
    # ChatGPT is powered by gpt-3.5-turbo, OpenAI’s most advanced language model.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": response})
    return str(response), messages


def clean_word_output(word_output:str)-> str:   
    """Cleans a word based on specific rules"""
    if len(word_output.split('"')) > 1:
        word_output = word_output.split('"')[1]
    if len(word_output.split("'")) > 1:
        word_output = word_output.split("'")[1]
    if len(word_output.split(" is ")) > 1:
        word_output = word_output.split(' is ')[1]
    if len(word_output.split(": ")) > 1:
        word_output = word_output.split(': ')[1]
    word_output = word_output.replace('.', '')
    return word_output


def fill_prompt(prompt:str, prompt_filling_dict:dict)-> str:
    """Fill a prompt with predefined elements"""
    for k, v in prompt_filling_dict.items():
        prompt = prompt.replace(k, str(v))
    return prompt


def zip_a_word(document, document_name: str):
    """Zips a Word .docx document"""
    # Create in-memory buffer
    file_stream = io.BytesIO()
    # Save the .docx to the buffer
    document.save(file_stream)
    buf = io.BytesIO()
    # save the document to memory as a file-like object
    doc_file = io.BytesIO()
    document.save(doc_file)
    doc_file.seek(0)
    # create a new zip file in the buffer
    with zipfile.ZipFile(buf, 'w') as zip_file:
        # add the document to the zip file
        zip_file.writestr(f'{document_name}.docx', doc_file.read())
    # get the contents of the buffer as bytes
    zip_data = buf.getvalue()
    return zip_data


def is_valid_url(url: str)-> bool:
    """Checks if a URL is valid"""
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)