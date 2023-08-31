import streamlit as st
import requests
import openai

# Set up OpenAI API key
openai.api_key = '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'

def fetch_product_info_and_improve(asin, marketplace):
    params = {
        'api_key': '5CCE0A4BA6C546C7987E63B21915AA99',
        'amazon_domain': marketplace,
        'asin': asin,
        'type': 'product'
    }

    api_result = requests.get('https://api.asindataapi.com/request', params)
    data = api_result.json()

    # Parsing the JSON to extract key details
    product = data.get("product", {})
    product_title = product.get("title", "N/A")
    description = product.get("description", "N/A")
    bullet_points = product.get("feature_bullets_flat", "N/A")

    original_output = f"Product Title: {product_title}\nDescription: {description}\nBullet Points: {bullet_points}"

    # Improve the content with OpenAI
    prompt_text = (f"Based on the provided Amazon detail page content, please improve the following:\n"
                   f"(i) Product Title: {product_title}\n"
                   f"(ii) Product Description: {description}\n"
                   f"(iii) Bullet Points: {bullet_points}\n"
                   f"\nPlease provide a revised (i) title, (ii) description, and (iii) bullet points.")
    
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt_text,
            max_tokens=300
        )
        improved_output = response.choices[0].text.strip()

    except openai.error.OpenAiError:
        improved_output = "Error occurred with OpenAI. Please try again later."

    return original_output, improved_output

# Streamlit App Layout
st.title('ASIN Product Info Fetcher & Improver')

# User input
asin = st.text_input("Enter ASIN:")
marketplace = st.selectbox("Select Marketplace", ["amazon.co.uk", "amazon.de", "amazon.fr", "amazon.it", "amazon.es", "amazon.nl"])

if st.button('Fetch & Improve'):
    original_output, improved_output = fetch_product_info_and_improve(asin, marketplace)
    
    # Display results
    st.subheader("Original Product Info")
    st.write(original_output)
    
    st.subheader("Improved Detail Page Content")
    st.write(improved_output)
