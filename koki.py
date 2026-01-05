import streamlit as st
from google import genai
from PIL import Image
from prompt_function import (
    prompt_for_dominant_flavors,
    prompt_for_cook_method,
    prompt_for_extra_ingredients,
    prompt_for_healthier_food,
    prompt_for_recipe_type
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain import hub

def reset_state():
    st.session_state["ingredients_list"] = ""
    st.session_state["generated_recipe"] = "" 

def reset_state_camera():
    st.session_state["ingredients_list"] = ""
    st.session_state["generated_recipe"] = "" 

    this_key = f"camera_input_{st.session_state['camera_key']}"
    if st.session_state.get(this_key) is not None:
        st.session_state["uploader_key"] += 1

def reset_state_upload():
    st.session_state["ingredients_list"] = ""
    st.session_state["generated_recipe"] = "" 

    this_key = f"image_uploader_{st.session_state['uploader_key']}"
    if st.session_state.get(this_key) is not None:
        st.session_state["camera_key"] += 1

def reset_ingredients_function():
    st.session_state["ingredients_list"] = ""
    st.session_state["uploader_key"] += 1
    st.session_state["camera_key"] += 1
    reset_chat_function()

def reset_chat_function():
    st.session_state.pop("agent_executor", None)
    st.session_state.pop("agent_brain", None)
    
    st.session_state["generated_recipe"] = ""
    st.session_state["messages"] = []

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0
if "camera_key" not in st.session_state:
    st.session_state["camera_key"] = 0
if "ingredients_list" not in st.session_state:
    st.session_state["ingredients_list"] = ""
if "generated_recipe" not in st.session_state:
    st.session_state["generated_recipe"] = ""

# Setup Halaman
st.set_page_config(page_title="Chef AI", page_icon="👨‍🍳")
st.title("👨‍🍳 AI Recipe Generator")
detect, generate, guide, faq = st.tabs([
    "1. 🔍 Detect Ingredients", 
    "2. 🍳 Generate Recipe", 
    "3. 📖 How to Use",
    "4. ❓ FAQ & Info"
])

with st.sidebar:
    st.title("👨‍🍳 Navigation")

    st.divider()
    google_api_key = st.text_input("Please input your API Key here first.", type="password", key="input_widget")
    st.session_state["api_key"] = google_api_key

    # Button to clear ingredients only (Hard Reset for Food Data)
    st.button(
        label="🗑️ Clear Ingredients & Restart",
        help="Removes the current list of ingredients and allows you to scan a new image.",
        on_click=reset_ingredients_function  # Masukkan nama fungsimu di sini
    )

    # Button to clear chat history only (Soft Reset)
    st.button(
        label="🔄 Start New Recipe Chat",
        help="Clears the conversation history but KEEPS your current ingredients list.",
        on_click=reset_chat_function  # Masukkan nama fungsimu di sini
    )

    st.divider()
    languages = st.radio(
        "🌐 Select Output Language / Pilih Bahasa",
        ["English", "Indonesian"],
        captions=[
            "International standard format (Global) 🌍",
            "Versi Bahasa Indonesia, lebih melokal 🇮🇩"
        ],
        on_change=reset_state
    )

if st.session_state["api_key"]:
    # Jangan lupa huruf 'f' di depan biar variabel {languages} kebaca!
    prompt = f"""
    Identify all food ingredients visible in this image. 
    Output the result **ONLY** as a bulleted list. 
    Do not include any introductory text, explanations, or concluding remarks.
    Make your answer strictly in {languages} Languages.
    """
    model_id='gemini-2.5-flash'

    client = genai.Client(api_key=st.session_state["api_key"])
else:
    st.warning("Please input your API Key first.")

with detect:
    upload_img = st.file_uploader(label="Upload Your Image Here", type=["jpg", "jpeg", "png", "webp"], on_change = reset_state_upload, key=f"image_uploader_{st.session_state['uploader_key']}")

    st.markdown("---")
    st.write("📸 **Or snap a photo directly:**")
    
    enable = st.checkbox("Enable Camera / Buka Kamera")
    picture = st.camera_input("Take a picture", disabled=not enable, on_change = reset_state_camera, key=f"camera_input_{st.session_state['camera_key']}")

    final_img = None
    if upload_img is not None:
        final_img = upload_img
    if picture is not None:
        final_img = picture

    if final_img is not None:
        img = Image.open(final_img)
        st.image(final_img)

        if st.button("🔍 Detect Ingredients"):
            with st.spinner("Scanning your fridge...", show_time=True):
                try:
                    response = client.models.generate_content(
                        model=model_id,
                        contents=[img, prompt]
                    )

                    st.session_state["ingredients_list"] = response.text
                except Exception as e:
                    # Convert the error object to a string for analysis
                    error_message = str(e)
                    
                    # 1. Check for Quota/Rate Limit issues (Error 429 or 'Quota exceeded')
                    if "429" in error_message or "Quota exceeded" in error_message:
                        st.error("🚨 **Oops! API Quota Exceeded**")
                        st.warning(
                            """
                            **Explanation:** You have reached the free usage limit for the Google Gemini API.
                            
                            **Solutions:**
                            1. Wait for a few minutes (it might be a minute-rate limit).
                            2. Try again tomorrow (if it's a daily limit).
                            """
                        )
                    
                    # 2. Check for Invalid API Key issues (Usually 400 or 403)
                    elif "API key not valid" in error_message:
                        st.error("🔑 **Invalid API Key**")
                        st.info("Please ensure you have entered the correct API Key in the sidebar.")

                    # 3. Handle other technical errors (Network issues, bugs, etc.)
                    else:
                        st.error("⚠️ **Technical Error Occurred**")
                        st.write(f"Error Details: `{error_message}`")
            
            if not st.session_state["ingredients_list"]:
                st.warning("No ingredients detected.")

        if st.session_state["ingredients_list"]:
            ingredients_list = st.session_state["ingredients_list"]
            
            # Kalimat sukses yang lebih 'hidup'
            st.success("✨ Ingredients successfully identified! Ready to cook?")

            ingredients_list = st.session_state["ingredients_list"]
            
            # Header list bahan
            st.markdown("### 🛒 Your Ingredients List:")
            st.markdown(ingredients_list)

            # Expander dengan ajakan yang jelas
            with st.expander("✏️ Need corrections? Click here to Edit"):
                edited_text = st.text_area(
                    # Label instruksi
                    label="Modify the list below:",
                    value=st.session_state["ingredients_list"],
                    height=300,
                    # Help text yang membantu
                    help="You can fix typos, add missing items, or remove wrong ingredients here."
                )

                # Tombol simpan dengan icon centang biar mantap
                if st.button("✅ Save Changes"):
                    st.session_state["ingredients_list"] = edited_text
                    st.rerun()

    else:
        st.info("👋 Hey there! Upload an image above to let the AI analyze it.", icon="ℹ️")

with generate:
    st.markdown("### 🛒 Your Ingredients List:")
    if st.session_state["ingredients_list"] == "":
        st.warning("There is no ingredients. Please upload an image first at **Detect Ingredients**")
    else: 
        st.markdown(st.session_state["ingredients_list"])

    st.divider()

    current_ingredients = st.session_state["ingredients_list"]

    # --- 1. Dominant Flavor (Multiselect) ---
    # Using multiselect allows users to combine complex flavors (e.g., Sweet & Spicy)
    dominant_flavors = st.multiselect(
        label="What is your preferred taste profile?",
        options=[
            "Savory", 
            "Spicy", 
            "Sweet", 
            "Sour", 
            "Umami", 
            "Salty", 
            "Bitter"
        ],
        placeholder="Select one or more flavors (e.g., Savory, Spicy)",
        default = ["Spicy"]
    )
    output_of_dominant_flavors = prompt_for_dominant_flavors(dominant_flavors)

    # --- 2. Cooking Method (Selectbox) ---
    # Providing varied cooking techniques. "Surprise Me" acts as a wildcard.
    cook_method = st.selectbox(
        label="How would you like your meal prepared?",
        options=[
            "Surprise Me (Any Method)",
            "Fry (Deep/Pan)",
            "Sauté / Stir-fry",
            "Boil / Soup",
            "Steam",
            "Bake / Roast",
            "Grill / BBQ",
            "Raw / Salad"
        ]
    )
    output_of_cook_method = prompt_for_cook_method(cook_method)

    # --- 3. Extra Ingredients Permission (Checkbox) ---
    # Boolean logic: True = AI can suggest new items; False = Strict fridge raid.
    allow_extra_ingredients = st.checkbox(
        label="Allow AI to suggest extra ingredients?",
        value=False,  # Default to False (Strict Mode)
        help="Check this if you are willing to buy or add ingredients that are not visible in your input."
    )
    output_of_extra_ingredients = prompt_for_extra_ingredients(allow_extra_ingredients)

    # --- 4. Healthy Mode (Checkbox) ---
    # Boolean logic: True = Prioritize nutrition/low cal; False = Flavor first.
    is_healthy = st.checkbox(
        label="Prioritize healthy options?",
        value=False,
        help="If checked, the AI will suggest low-calorie methods and healthier ingredient substitutions."
    )
    output_of_healthier_food = prompt_for_healthier_food(is_healthy)

    # --- 5. Simple Mode (Checkbox) ---
    # Boolean logic: True = Fast & Easy / Beginner friendly; False = Elaborate / Gourmet.
    is_simple = st.checkbox(
        label="Prefer simple and quick recipes?",
        value=False,
        help="If checked, the AI will generate beginner-friendly recipes with fewer steps and shorter cooking times."
    )
    # Construct the System Prompt based on User Choice (Simple vs Pro)
    prefix_prompt = prompt_for_recipe_type(
        is_simple,                    # Checkbox value (True/False)
        current_ingredients,          # String containing the list of ingredients
        output_of_cook_method,        # String instructions for cooking method
        output_of_dominant_flavors,   # String instructions for flavor profile
        output_of_healthier_food,     # String instructions for dietary goals
        output_of_extra_ingredients   # String instructions for extra ingredients permission
    )

    if ("agent_executor" not in st.session_state) \
        or (getattr(st.session_state, "_last_key", None) != st.session_state["api_key"]) \
        or (getattr(st.session_state, "_last_flavors", None) != dominant_flavors) \
        or (getattr(st.session_state, "_last_method", None) != cook_method) \
        or (getattr(st.session_state, "_last_extra", None) != allow_extra_ingredients) \
        or (getattr(st.session_state, "_last_healthy", None) != is_healthy) \
        or (getattr(st.session_state, "_is_simple", None) != is_simple):

        try:
            # Initialize the LLM (Google Gemini)
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=st.session_state["api_key"],
                temperature=0.7, # Moderate creativity
                verbose=True
            )
            
            # Define tools available to the agent
            tools = [DuckDuckGoSearchRun(name='Search')]
            
            # Pull the standard ReAct prompt template from LangChain Hub
            prompt_agent = hub.pull("hwchase17/react-chat")
            
            # Merge the custom persona instructions with the default agent template
            prompt_agent.template = prefix_prompt + "\n\n" + prompt_agent.template

            # Create the Agent (The Brain: Logic & Reasoning)
            st.session_state.agent_brain = create_react_agent(
                llm,
                tools=tools, 
                prompt=prompt_agent
            )
            
            # Create the Executor (The Body: Action & Memory)
            st.session_state.agent_executor = AgentExecutor(
                agent=st.session_state.agent_brain,
                tools=tools,
                memory= ConversationBufferMemory(memory_key="chat_history"),
                handle_parsing_errors=True # Auto-recover from LLM formatting errors
            )

            # Store current config to detect changes later
            st.session_state._last_key = st.session_state["api_key"]
            st.session_state._last_flavors = dominant_flavors
            st.session_state._last_method = cook_method
            st.session_state._last_extra = allow_extra_ingredients
            st.session_state._last_healthy = is_healthy
            st.session_state._last_simple = is_simple

            # Clear chat history on recipe configuration change for consistency
            st.session_state.pop("messages", None)
            
        except Exception as e:
            error_message = str(e)
            
            # 1. Check for Quota/Rate Limit issues
            if "429" in error_message or "Quota exceeded" in error_message:
                st.error("🚨 **Oops! API Quota Exceeded**")
                st.warning(
                    """
                    **Explanation:** You have reached the free usage limit for the Google Gemini API.
                    
                    **Solutions:**
                    1. Wait for a few minutes.
                    2. Try again tomorrow.
                    """
                )
            
            # 2. Check for Invalid API Key
            elif "API key not valid" in error_message:
                st.error("🔑 **Invalid API Key**")
                st.info("Please ensure you have entered the correct API Key in the sidebar.")

            # 3. Handle other errors
            else:
                st.error("⚠️ **System Error Occurred**")
                st.write(f"Error Details: `{error_message}`")
            
            # Stop the application if initialization fails to prevent further execution
            st.stop()

    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Capture User Input
    if st.session_state["ingredients_list"] == "":
        st.warning("There is no ingredients. Please upload an image first at **Detect Ingredients**")
    else:
        prompt = st.chat_input("What you want to cook today?")

        if prompt:
            # 1. Display User Message
            st.session_state.messages.append({"role": "human", "content": prompt})
            with st.chat_message("human"):
                st.markdown(prompt)

            with st.status("👨‍🍳 Chef is crafting your recipe...", expanded=False) as status:
                try:
                    response = st.session_state.agent_executor.invoke({"input": prompt})
                    
                    if "output" in response and len(response["output"]) > 0:
                        answer = response['output']
                        
                        status.update(label="✅ Recipe Ready to Serve!", state="complete", expanded=False)
                    else:
                        answer = "I'm sorry, I couldn't generate a response."
                        status.update(label="❌ Failed to generate", state="error")

                except Exception as e:
                    error_message = str(e)

                    # 1. Check for Quota/Rate Limit issues
                    if "429" in error_message or "Quota exceeded" in error_message:
                        # Store the long explanation in 'answer' to display it in the chat
                        answer = """🚨 **Oops! API Quota Exceeded**

                        **Explanation:** You have reached the free usage limit for the Google Gemini API.
                        
                        **Solutions:**
                        1. Wait for a few minutes.
                        2. Try again tomorrow.
                        """
                        # Update the status box to Red (Error state)
                        status.update(label="⏳ Quota Exceeded", state="error")
                    
                    # 2. Check for Invalid API Key
                    elif "API key not valid" in error_message:
                        answer = "🔑 **Invalid API Key**\nPlease ensure you have entered the correct API Key in the sidebar."
                        status.update(label="❌ Invalid Key", state="error")

                    # 3. Handle other errors
                    else:
                        answer = f"⚠️ **Technical Error Occurred**\nError Details: `{error_message}`"
                        status.update(label="⚠️ Error Occurred", state="error")

            # 3. Display Assistant Message
            with st.chat_message("ai"):
                st.markdown(answer)
            
            # 4. Save to History
            st.session_state.messages.append({"role": "ai", "content": answer})

with guide:
    st.header("📖 How to use Chef AI")
    st.markdown("""
    Welcome to your personal AI Chef! Follow these simple steps to cook something amazing:

    ### **Step 1: Activate the Chef (API Key)** 🔑
    1.  Look at the **Sidebar** on the left 👈.
    2.  Paste your **Google Gemini API Key** into the input box.
    3.  *Note: The AI cannot see or think without this key!*

    ---

    ### **Step 2: Scan Your Ingredients (Tab 1)** 📸
    1.  Go to the **'🔍 Detect Ingredients'** tab.
    2.  **Upload an image** of your fridge/pantry OR **Take a photo** directly.
    3.  Click **'🔍 Detect Ingredients'**.
    4.  The AI will list what it sees. You can **Edit** the list if something is wrong or missing.
    
    ---

    ### **Step 3: Configure Your Meal (Tab 2)** ⚙️
    1.  Switch to the **'🍳 Generate Recipe'** tab.
    2.  Wait for the **Settings** to appear (detected ingredients must exist first).
    3.  **Customize your preferences**:
        * **Taste:** Sweet, Spicy, Savory?
        * **Method:** Fry, Boil, Steam?
        * **Diet:** Healthy mode?
        * **Mode:** Simple (Quick) or Pro (Detailed)?

    ---

    ### **Step 4: Chat with the Chef** 💬
    1.  Type what you want to cook in the **Chat Box** (e.g., *"Make something spicy with the chicken"*).
    2.  The AI Chef will analyze your request and generate a **Custom Recipe** just for you.
    3.  Enjoy your meal! 🍽️
    """)

    st.info("💡 **Tip:** You can ask the Chef to modify the recipe! Just type: *'Too much salt, make it healthier'* or *'Change chicken to tofu'*.")


with faq:
    st.header("🤖 Tech Trivia & FAQ")
    st.write("Curious about how this AI Chef works? Here are the answers!")

    # Menggunakan Container dengan Border biar rapi kayak 'Kartu'
    with st.container(border=True):
        
        # Q1: API Key
        with st.expander("🔑 What is an Google API Key?"):
            st.markdown("""
            Think of the **API Key** as a **Digital Ticket** or Password. 
            
            * **The Brain:** The AI (Google Gemini) lives in the cloud (Google's servers).
            * **The Connection:** To let this app talk to that powerful brain, it needs permission.
            * **The Key:** Your API Key validates that permission. Without it, the "Chef" has no brain!
            """)

        # Q2: Why Gemini?
        with st.expander("🧠 Why do we use Google Gemini?"):
            st.markdown("""
            **Google Gemini** is one of the smartest AI models available today. 
            It is 'Multimodal', meaning it can see images (your food photos) and understand text (your chat) simultaneously. 
            That's why it's perfect for identifying ingredients and writing recipes!
            """)

        # Q3: Privacy
        with st.expander("🛡️ Is my API Key safe?"):
            st.markdown("""
            **Yes.** * This app runs locally or in your browser session.
            * Your key is used **only** to communicate with Google to generate your specific request.
            * It is **not saved** permanently in any database by this app. Once you refresh the page, it's gone.
            """)

        # Q4: Quota Error
        with st.expander("⚠️ Why did I get a 'Quota Exceeded' error?"):
            st.markdown("""
            Google provides a **Free Tier** for developers, but it has limits (e.g., a certain number of requests per day).
            If you see this error, it means you've used up your free "tokens" for the day. 
            * **Solution:** Wait for a while, or try again tomorrow!
            """)

        # Q5: Persistent Warning Explanation
        with st.expander("⚠️ Why do I see the 'Please input your API Key' warning everywhere?"):
            st.markdown("""
            **It is a Global Reminder.** 
            * Without the API Key, the AI is effectively "offline" or "brainless."
            * We show this warning on every tab to prevent you from trying to upload photos or chat, only to get an error later.
            * **Good News:** As soon as you paste your key in the Sidebar, this warning will **disappear instantly** from all pages!
            """)

        # Q6: Ingredient Accuracy
        with st.expander("🍎 Why did the AI miss some of my ingredients?"):
            st.markdown("""
            **The AI's vision depends on image quality.** 
            * If the photo is dark, blurry, or too cluttered, the AI might miss items.
            * **Tip:** Try to spread out your ingredients on a clear surface and take a well-lit photo.
            * **Solution:** You can always manually add missing items in the text area inside Tab 1!
            """)

        # Q7: Pantry Staples (Assumed Ingredients)
        with st.expander("🧂 Why does the recipe include ingredients I didn't scan?"):
            st.markdown("""
            **The AI assumes you have 'Pantry Staples'.**
            * Even if you only scan a Chicken, the AI knows you can't cook it without basic items like **Oil, Salt, Pepper, or Water**.
            * It adds these automatically to make the recipe tasty and cookable.
            * If the AI suggests something big (like 'Cheese' or 'Wine') that you don't have, check the **'Allow extra ingredients?'** box to False/Off.
            """)

        # Q8: Food Safety Disclaimer
        with st.expander("🚑 Can I trust these recipes 100%?"):
            st.markdown("""
            **Use your Chef's Intuition!** 
            * AI is creative but not perfect. It might occasionally suggest weird combinations or incorrect cooking times.
            * **Safety First:** Always ensure meat is cooked thoroughly, regardless of what the steps say. 
            * If a step seems dangerous or wrong, trust your gut (and taste buds) over the AI.
            """)

        # Q9: Refreshing the Page
        with st.expander("🔄 Why did my chat/recipe disappear when I refreshed?"):
            st.markdown("""
            **This app runs on 'Session State'.**
            * This means the app's memory lives only as long as the tab is open.
            * If you hit **Refresh (F5)**, the app restarts from scratch, and the memory is wiped clean to protect your privacy.
            * **Tip:** Copy-paste your favorite recipes to a notepad before closing the tab!
            """)

        # Q10: Specific Diets (Keto/Vegan/Halal)
        with st.expander("🥦 How do I request specific diets (Keto, Vegan, Halal)?"):
            st.markdown("""
            **You have two ways:**
            1.  **Check the 'Healthy Options' box:** This nudges the AI generally towards better nutrition.
            2.  **Tell the Chat:** The most powerful way is to just type it! 
                * *Example:* "Make this recipe Halal."
                * *Example:* "I am on a Keto diet, no sugar please."
            """)
            
    # Footer manis
    st.info("💡 **Fun Fact:** This application was built using **Python** and **Streamlit**!")