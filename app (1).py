import streamlit as st
import ollama

system_prompt = f"""
                    "you are  a AI java script tutor.who helps student to learn java Script from scratch,
                    you teach them all the topics in java Script step by step  and make sure that they learn what you are teaching them by doing a quick test on the topic you have covered """

def chat(user_prompt, model):
    stream = ollama.chat(
        model=model,
        messages=[        {"role": "system", "content": "You are an AI java Script tutor who helps students learn java Script from scratch."},
        {"role": "system", "content": "You teach them all the topics in java Script step by step and make sure that they learn what you are teaching them by doing a quick test on the topic you have covered."},
        {"role": "system", "content": "This is the syllabus from which you need to teach: Introduction to java Script, Data Structures, Loops, Functions, Error Handling, File Operations, Libraries like NumPy and Pandas. Teach them in detail so that even if someone is not from this background, they understand it well."},
        {"role": "system", "content": "after completing the each and every topic ask them the 3-4 questions about that topics to test their knowledge if they dont answer correctly give them the right answer and help them improve"},
        {"role": "system", "content": "Follow the syllabus step by step strictly."},
            {'role': 'assistant', 'content': system_prompt},
                  {'role': 'user', 'content': f"Model being used is {model}.{user_prompt}"}]+st.session_state.messages,
        stream=True,
    )

    return stream

# handles stream response back from LLM
def stream_parser(stream):
    for word in stream:
        yield word['message']['content']


st.set_page_config(
    page_title="java Script AI TUTOR",
    initial_sidebar_state="expanded"
)


# Set the desired image size
image_width = 300  # You can adjust this value to resize the image
image_height = 300  # You can adjust this value to resize the image

# Center-align an image
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(r"C:\Users\USER\Downloads\Logo.png", ### change the image location before deploying with your logo 
             caption="", 
            
             use_container_width=False)

st.title("🤖java Script AI Tutor")

# sets up sidebar nav widgets
with st.sidebar:   
    st.markdown("# Chat Options")
    
   
    model = st.selectbox('What model would you like to use?',["llama3.2","deepseek-r1:8b","gemma3:latest"])

### initializing an empty list to store the messages

if "messages" not in st.session_state:
    st.session_state.messages = []

## display the previous messages from the list to the user
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("What would you like to ask?"):
    # Display user prompt in chat message widget
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # adds user's prompt to session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner('Generating response...'):
        # retrieves response from model
        llm_stream = chat(user_prompt, model=model)

        # streams the response back to the screen
        stream_output = st.write_stream(stream_parser(llm_stream))

        # appends response to the message list
        st.session_state.messages.append({"role": "assistant", "content": stream_output})
