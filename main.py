# main.py

import streamlit as st
from langchain_helper import ArticleGenerator
from langchain.callbacks import StreamlitCallbackHandler

import json
import os

# Set page config
st.set_page_config(page_title='Dasho Draft Gen', page_icon=':pencil:', layout='centered', initial_sidebar_state='collapsed')

# Define custom colors for layout
primaryColor = "#4E89AE"
startGradientColor = "#ffaa00"
endGradientColor = "#FFFFFF"
textColor = "#2E5266"
font = "Roboto, sans-serif"
secondaryBackgroundColor = "#fcdede"
buttonColor = "#ffaa00"

custom_css = f"""
<style>
    body {{
        background: linear-gradient(90deg, {startGradientColor}, {endGradientColor});
        color: {textColor};
        font-family: {font};
        line-height: 1.6;
    }}
    .stButton > button {{
        background-color: {buttonColor};
        color: {endGradientColor};
        font-family: {font};
        border-radius: 10px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stTextInput > div > div > input, 
    textarea {{
        color: {textColor};
        border-radius: 10px;
        border: 2px solid {secondaryBackgroundColor}; /* Changed to gradient start color */
        padding: 10px 15px;
    }}
    .css-2trqyj {{
        background-color: rgba(255, 170, 0, 0.1); /* Light version of gradient start color for readability */
        color: {textColor};
        font-family: {font};
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .newest_message {{
        background-color: rgba(78, 137, 174, 0.2);
        padding: 15px;
        border-radius: 15px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.title("Dasho Draft Generator")
st.text("")

# Load presets from file
if os.path.exists('presets.json'):
    with open('presets.json', 'r') as f:
        presets = json.load(f)
else:
    presets = {}

expander_info = st.expander('How Does This Work?', expanded=False)
with expander_info:
    st.write("### **How the Dasho Draft Generator Works**")
    
    st.write("The Dasho Draft Generator is a powerful tool that harnesses the capabilities of AI to craft written content tailored to your needs. Below is an overview of how the application operates:")

    st.markdown("**1. Model Selection**")
    st.write("- Choose between two models: GPT-4o and GPT-4o-Mini.")
    st.write("- GPT-4o (Recommended): More intelligent and creative but runs slower.")
    st.write("- GPT-4o-mini: Faster but less capable than GPT-4o.")

    st.markdown("**2. Token Length Selection**")
    st.write("- Choose between three token lengths: Short, Medium, and Long.")
    st.write("- Short: Good for captions and short descriptions.")
    st.write("- Medium: Good for call-to-action messages and newsletters.")
    st.write("- Long: Good for longer blog posts and articles, as well as short stories and poems.")

    st.markdown("**3. Input Details**")
    st.write("- Provide details like your brand, target audience, content type, topic, and writing style.")
    st.write("- The more accurate your inputs, the better the generated content will align with your expectations.")

    st.markdown("**4. Content Generation**")
    st.write("- Click the 'Generate Draft' button.")
    st.write("- The AI will use your inputs to generate a draft. This process may take a few moments, so your patience is appreciated.")

    st.markdown("**5. Review AI Analysis and First Draft**")
    st.write("- The application will display an AI analysis of your inputs, which gives insights into how the AI perceived your inputs.")
    st.write("- You'll then see the first draft of the content.")

    st.markdown("**6. AI's Second Round of Analysis**")
    st.write("- The AI will critically assess the first draft.")
    st.write("- A second, more refined draft is then presented based on this analysis.")

    st.markdown("**7. Feedback and Revisions**")
    st.write("- If the content isn't quite right, provide feedback in the designated field.")
    st.write("- Click 'Send Feedback', and the AI will generate a new version of the content considering your comments.")

    st.markdown("**8. Feedback Thread**")
    st.write("- This section displays all previous feedback and the AI's corresponding responses.")
    st.write("- It's a great way to track changes and see the evolution of the content.")

    st.write("With these steps, the Dasho Draft Generator ensures that you receive quality written content, tailored to your specific requirements.")

# Initialize session state variables
if 'article_gen' not in st.session_state:
    st.session_state['article_gen'] = None
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = []
if 'outputs' not in st.session_state:
    st.session_state['outputs'] = []
if 'output_generated' not in st.session_state:
    st.session_state['output_generated'] = False
if 'show_output' not in st.session_state:
    st.session_state['show_output'] = True

# Initialize form input session state variables
input_variables = ['brand', 'brand_description', 'content_type', 'platform', 'topic', 'writing_style', 'target_audience', 'additional_instructions', 'selected_model', 'selected_token_length', 'selected_preset', 'preset_name_input']

for var in input_variables:
    if var not in st.session_state:
        if var == 'selected_model':
            st.session_state[var] = 'gpt-4o'
        elif var == 'selected_token_length':
            st.session_state[var] = 'Medium'
        else:
            st.session_state[var] = ''

def load_preset():
    selected_preset = st.session_state['selected_preset']
    if selected_preset and selected_preset in presets:
        preset = presets[selected_preset]
        st.session_state['brand'] = preset.get('brand', '')
        st.session_state['brand_description'] = preset.get('brand_description', '')
        st.session_state['content_type'] = preset.get('content_type', '')
        st.session_state['platform'] = preset.get('platform', '')
        st.session_state['topic'] = preset.get('topic', '')
        st.session_state['writing_style'] = preset.get('writing_style', '')
        st.session_state['target_audience'] = preset.get('target_audience', '')
        st.session_state['additional_instructions'] = preset.get('additional_instructions', '')
        st.session_state['selected_model'] = preset.get('selected_model', 'gpt-4o')
        st.session_state['selected_token_length'] = preset.get('selected_token_length', 'Medium')
    else:
        # Clear the session_state variables
        st.session_state['brand'] = ''
        st.session_state['brand_description'] = ''
        st.session_state['content_type'] = ''
        st.session_state['platform'] = ''
        st.session_state['topic'] = ''
        st.session_state['writing_style'] = ''
        st.session_state['target_audience'] = ''
        st.session_state['additional_instructions'] = ''
        st.session_state['selected_model'] = 'gpt-4o'
        st.session_state['selected_token_length'] = 'Medium'

expander_inputs = st.expander('Inputs', expanded=True)
with expander_inputs:
    # Preset selection
    preset_names = list(presets.keys())
    st.selectbox('Select a Preset:', [''] + preset_names, key='selected_preset', on_change=load_preset)

    model_options = ['gpt-4o', 'gpt-4o-mini']
    st.selectbox('Select Model:', model_options, index=model_options.index(st.session_state['selected_model']) if st.session_state['selected_model'] in model_options else 0, key='selected_model')

    token_length_options = {
        'Short': 150,
        'Medium': 550,
        'Long': 1022
    }
    st.selectbox('Token Length:', list(token_length_options.keys()), index=list(token_length_options.keys()).index(st.session_state['selected_token_length']) if st.session_state['selected_token_length'] in token_length_options else 1, key='selected_token_length')
    st.markdown("---")

    st.text_input('Brand:', st.session_state['brand'], key='brand')
    st.text_input('Brand Description:', st.session_state['brand_description'], key='brand_description')
    content_type_options = ['', 'Article', 'Blog Post', 'Newsletter', 'Infographics', 'Short Story', 'Press Release', 'Product Description', 'Product Review', 'Captions', 'Shortform Video Script', 'Longform Video Script', 'Social Media Post (Full)']
    st.selectbox('Content Type:', sorted(content_type_options), index=sorted(content_type_options).index(st.session_state['content_type']) if st.session_state['content_type'] in content_type_options else 0, key='content_type')
    platform_options = ['General', 'Blog', 'Email', 'Facebook', 'Instagram', 'Twitter', 'Reels', 'Threads', 'LinkedIn', 'TikTok', 'YouTube', 'Pinterest', 'E-Commerce', 'Snapchat', 'Website', 'Document', 'Other']
    st.selectbox('Platform:', platform_options, index=platform_options.index(st.session_state['platform']) if st.session_state['platform'] in platform_options else 0, key='platform')
    st.text_input('Topic:', st.session_state['topic'], key='topic')
    st.text_input('Writing Style:', st.session_state['writing_style'], key='writing_style')
    st.text_input('Target Audience:', st.session_state['target_audience'], key='target_audience')
    st.text_area('Additional Information (Optional):', st.session_state['additional_instructions'], key='additional_instructions')

    st.markdown("---")
    st.text_input('Preset Name (if saving):', st.session_state['preset_name_input'], key='preset_name_input')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Save current inputs as a new preset'):
            if st.session_state['preset_name_input']:
                # Save the current inputs as a new preset
                presets[st.session_state['preset_name_input']] = {
                    'brand': st.session_state['brand'],
                    'brand_description': st.session_state['brand_description'],
                    'content_type': st.session_state['content_type'],
                    'platform': st.session_state['platform'],
                    'topic': st.session_state['topic'],
                    'writing_style': st.session_state['writing_style'],
                    'target_audience': st.session_state['target_audience'],
                    'additional_instructions': st.session_state['additional_instructions'],
                    'selected_model': st.session_state['selected_model'],
                    'selected_token_length': st.session_state['selected_token_length']
                }
                # Save the presets to the file
                with open('presets.json', 'w') as f:
                    json.dump(presets, f)
                st.success(f'Preset "{st.session_state["preset_name_input"]}" saved successfully!')
            else:
                st.error('Please enter a name for your preset.')
    with col2:
        if st.button('Delete selected preset'):
            selected_preset = st.session_state.get('selected_preset', '')
            if selected_preset and selected_preset in presets:
                del presets[selected_preset]
                # Save the presets to the file
                with open('presets.json', 'w') as f:
                    json.dump(presets, f)
                st.success(f'Preset "{selected_preset}" deleted successfully!')
                # Clear the selected_preset
                st.session_state['selected_preset'] = ''
                # Clear the preset_name_input
                st.session_state['preset_name_input'] = ''
            else:
                st.error('No preset selected or preset does not exist.')

    st.markdown("---")

# Use the session_state variables
brand = st.session_state['brand']
brand_description = st.session_state['brand_description']
content_type = st.session_state['content_type']
platform = st.session_state['platform']
topic = st.session_state['topic']
writing_style = st.session_state['writing_style']
target_audience = st.session_state['target_audience']
additional_instructions = st.session_state['additional_instructions']
selected_model = st.session_state['selected_model']
selected_token_length = st.session_state['selected_token_length']

if brand and brand_description and platform and content_type and topic and writing_style and target_audience and st.button('Generate Draft'):
    st.markdown("---")
    if not st.session_state['article_gen']:
        # Initialize the ArticleGenerator object with the selected token length
        st.session_state['article_gen'] = ArticleGenerator(selected_model, content_type, brand, brand_description, platform, topic, writing_style, target_audience, additional_instructions, token_length_options[selected_token_length])
    container = st.empty()  # Use empty to be able to continually update the output
    st_callback = StreamlitCallbackHandler(container)  # Initialize the Streamlit callback handler
    response = st.session_state['article_gen'].generate(st_callback)  # Pass the callback handler to the generate method
    st.session_state['output_generated'] = True
    st.session_state['current_response'] = response
    container.write("")  # Clears the container after use

output_expander = st.expander("Show/Hide Output", expanded=True)

with output_expander:
    if st.session_state['output_generated']:
        response = st.session_state.get('current_response', {})
        st.header("FINAL OUTPUT")

        # Display AI Analysis
        st.subheader("AI Analysis")
        st.write(response['AI_analysis'].strip())

        # Display First Draft
        st.subheader("First Draft")
        st.write(response['first_draft'].strip())

        # Display Second AI Analysis
        st.subheader("AI Analysis of First Draft")
        article_text = response['AI_analysis_2'].strip().split("|")
        for section in article_text:
            st.write(" ", section)

        # Display Second Draft
        st.subheader("Second Draft")
        st.write(response['final_output'].strip())
    
if st.session_state['output_generated']:
    st.markdown("---")
    if 'user_feedback' not in st.session_state:
        st.session_state['user_feedback'] = ''
    user_feedback = st.text_input('Got more follow-up instructions for the AI? Send them here:', value=st.session_state['user_feedback'], key='user_feedback')

    if st.button('Send') and user_feedback:
        # Initialize the Streamlit callback handler and generate the output
        st_callback = StreamlitCallbackHandler(st.empty())  # Initialize the Streamlit callback handler
        new_response = st.session_state['article_gen'].generate_with_feedback(user_feedback, st_callback)  # Pass the callback handler to the generate_with_feedback method

        # Update session state with the new feedback and output
        st.session_state['feedbacks'].append(user_feedback)
        st.session_state['outputs'].append(new_response['final_output_with_feedback'].strip())

        # Clear the feedback input field
        st.session_state['user_feedback'] = ''

# Feedback thread rendering should be done outside st.empty() context
if st.session_state['feedbacks']:
    st.markdown("---")
    st.subheader("Comment Thread")
    
    # Start from the last feedback since it's the newest
    for index, (feedback, output) in enumerate(zip(reversed(st.session_state['feedbacks']), reversed(st.session_state['outputs']))):
        
        if index == 0:  # If it's the newest message
            st.markdown(f'<div class="newest_message"><caption>Feedback: {feedback}</caption><br>Output: {output}</div>', unsafe_allow_html=True)
        else:
            st.caption(f"Comments: {feedback}")
            st.write(f"Output: {output}")
        
    st.markdown("---")
st.write("**Got any feedback to improve this app? Send them to [m.me/fleirecastro](https://www.facebook.com/messages/t/585770910)!**")
st.caption("© 2024 DashoContent. All rights reserved.")
