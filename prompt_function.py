from typing import List

def prompt_for_dominant_flavors(flavors: List[str]):
    flavor_prompts = {
        "Savory": """
        FLAVOR PROFILE: SAVORY (GURIH).
        OBJECTIVE: Create a rich, full-bodied taste that stimulates the appetite.
        KEY INGREDIENTS: Use garlic, onions, shallots, meat stocks, or savory herbs (rosemary, thyme, sage).
        TECHNIQUE: Focus on seasoning depth. If cooking meat/veg, ensure proper browning (Maillard reaction) to enhance natural savoriness.
        BALANCE RULE: The dish should be hearty but not overly salty. It must feel 'complete' on the palate.
        """,

        "Spicy": """
        FLAVOR PROFILE: SPICY (PEDAS).
        OBJECTIVE: Deliver a prominent heat sensation (capsaicin) that lingers.
        KEY INGREDIENTS: MUST include chili peppers (fresh, dried, or powder), hot sauce, peppercorns, ginger, or paprika.
        TECHNIQUE: Infuse the heat early in the cooking process (e.g., sautéing chilies) or use it as a finishing touch (chili oil).
        BALANCE RULE: The heat should be strong but not overpower the actual flavor of the main ingredients. It should be edible, not painful.
        """,

        "Sweet": """
        FLAVOR PROFILE: SWEET (MANIS).
        OBJECTIVE: Highlight sugary or natural sweetness notes.
        KEY INGREDIENTS: Sugar (white/brown), honey, maple syrup, sweet soy sauce, or naturally sweet vegetables (corn, carrots, sweet potato).
        TECHNIQUE:
        - If Savory Dish: Create a glaze or caramelized coating (e.g., Teriyaki, BBQ, Honey-Butter).
        - If Dessert: Maximize the sweetness but balance with a pinch of salt.
        BALANCE RULE: Do not make it cloying. If it's a main course, balance the sugar with savory or salty elements.
        """,

        "Sour": """
        FLAVOR PROFILE: SOUR (ASAM).
        OBJECTIVE: Create a bright, zesty, and acidic taste profile.
        KEY INGREDIENTS: Citrus juice/zest (lemon, lime), vinegar (rice, apple cider, balsamic), tamarind, yogurt, or tomatoes.
        TECHNIQUE: Add acidic elements at the end of cooking to keep the flavor fresh and sharp.
        BALANCE RULE: Use acidity to cut through fat or richness. Avoid making the dish taste like pure vinegar; it must be refreshing.
        """,

        "Umami": """
        FLAVOR PROFILE: UMAMI (GURIH MENDALAM).
        OBJECTIVE: Maximize the 'fifth taste' (glutamates) for a deep, lingering savoriness.
        KEY INGREDIENTS: Soy sauce, fish sauce, oyster sauce, miso, mushrooms (shiitake), tomatoes, parmesan cheese, or seaweed.
        TECHNIQUE: Layer multiple umami sources. Reduce liquids to concentrate the flavor.
        BALANCE RULE: Umami ingredients are often salty. Reduce added salt to prevent the dish from becoming inedible.
        """,

        "Salty": """
        FLAVOR PROFILE: SALTY (ASIN).
        OBJECTIVE: Enhance and elevate the natural flavors of the ingredients through salinity.
        KEY INGREDIENTS: Sea salt, kosher salt, soy sauce, salted fish, cured meats (bacon), olives, or capers.
        TECHNIQUE: Season gradually throughout the cooking process, not just at the end.
        BALANCE RULE: The saltiness must be bold but controlled. Avoid over-salting to the point of dehydration.
        """,

        "Bitter": """
        FLAVOR PROFILE: BITTER (PAHIT).
        OBJECTIVE: Introduce a sophisticated, earthy bitterness.
        KEY INGREDIENTS: Dark leafy greens (kale, mustard greens), bitter melon, coffee, dark chocolate, matcha, or citrus pith.
        TECHNIQUE: Cook greens properly to tame the harshness, or pair bitter elements with fat/cream.
        BALANCE RULE: Bitterness must be balanced with fat, sweet, or acid. It should be pleasant complexity, not offensive.
        """
    }
    
    return "\n".join([flavor_prompts[flavor] for flavor in flavors])

def prompt_for_cook_method(method: str):
    cooking_method_prompts = {
        "Surprise Me (Any Method)": """COOKING METHOD STRATEGY: CHEF'S CHOICE. 
        Analyze the provided ingredients and determine the absolute best cooking technique to highlight their natural flavors. 
        You have full creative freedom. Choose a method that balances texture and taste perfectly. 
        Explain briefly why you chose this specific method for these ingredients.""",

        "Fry (Deep/Pan)": """COOKING METHOD STRATEGY: FRYING. 
        The user specifically requested a FRIED dish. 
        Focus on creating a crispy, golden-brown exterior while keeping the inside juicy/tender. 
        Provide specific tips on oil temperature or batter consistency if applicable. 
        Make sure the result is crunchy and satisfying.""",

        "Sauté / Stir-fry": """COOKING METHOD STRATEGY: SAUTÉING / STIR-FRYING. 
        The user wants a quick, high-heat cooking method. 
        Focus on 'Wok Hei' (breath of the wok) or caramelization. 
        Ensure the vegetables remain crisp-tender and the proteins are seared beautifully. 
        Emphasize the timing of adding ingredients so nothing gets overcooked.""",

        "Boil / Soup": """COOKING METHOD STRATEGY: BOILING / SOUP-MAKING. 
        The user wants a liquid-based dish or something boiled. 
        Focus on the depth of the broth or the infusion of flavors into the water. 
        If it's a soup, ensure the seasoning is balanced. 
        If it's boiled (like pasta or blanching), ensure the texture is al dente or perfectly cooked, not mushy.""",

        "Steam": """COOKING METHOD STRATEGY: STEAMING. 
        The user requests a gentle cooking method. 
        Focus on preserving the natural sweetness, nutrients, and delicate texture of the ingredients. 
        Avoid heavy oils. Suggest a dipping sauce or light seasoning to complement the clean flavors of the steamed food.""",

        "Bake / Roast": """COOKING METHOD STRATEGY: BAKING / ROASTING. 
        The user wants to use the oven. 
        Focus on dry heat cooking. Aim for caramelization, roasting aromatics, or baking distinct textures (like fluffy breads or tender roasts). 
        Provide instructions on oven temperature (in Celsius and Fahrenheit) and timing to avoid burning.""",

        "Grill / BBQ": """COOKING METHOD STRATEGY: GRILLING / BBQ. 
        The user wants smoky, charred flavors. 
        Focus on the marinade and the reaction of food to direct fire/heat. 
        Mention how to achieve grill marks or a nice crust. 
        If the user is indoors, suggest using a grill pan to mimic the effect.""",

        "Raw / Salad": """COOKING METHOD STRATEGY: NO-COOK / RAW PREPARATION. 
        The user does NOT want to cook with heat. 
        Focus on knife skills (julienne, dice, slice) and assembly. 
        The flavor relies entirely on freshness and the dressing/sauce. 
        Ensure the instructions focus on cleanliness and texture combinations (crunchy vs soft)."""
    }

    return cooking_method_prompts[method]

def prompt_for_extra_ingredients(allow: bool):
    """
    Generates ingredient constraints based on user permission.
    """
    if allow:
        return (
            "INGREDIENT FLEXIBILITY: You are ALLOWED to suggest additional ingredients "
            "(such as herbs, spices, aromatics, or complementary vegetables) "
            "that are not listed by the user, if they significantly enhance the dish."
        )
    else:
        return (
            "INGREDIENT CONSTRAINT: Use ONLY the ingredients provided by the user. "
            "Do NOT assume the user has other items. "
            "Exception: Basic seasoning (salt, pepper, water) is allowed."
        )

def prompt_for_healthier_food(healthy: bool):
    """
    Generates dietary constraint instructions based on user preference.
    """
    if healthy:
        return (
            "DIETARY REQUIREMENT: The user requested a HEALTHY meal. "
            "Strictly prioritize low-calorie cooking methods (e.g., steaming, boiling, air-frying). "
            "Minimize the use of oil, sugar, and sodium. Suggest nutritional alternatives if applicable."
        )
    else:
        # Default behavior: focus on taste
        return (
            "DIETARY PREFERENCE: Focus on maximizing flavor and taste comfort. "
            "Standard cooking methods are acceptable."
        )


def prompt_for_recipe_type(
    languages: str,
    current_ingredients: str, 
    output_of_cook_method: str, 
    output_of_dominant_flavors: str, 
    output_of_healthier_food: str, 
    output_of_extra_ingredients: str
):
    return f"""
        You are an expert Chef. 
        Create a simple, direct recipe based on these inputs:
        1. INGREDIENTS: [ "{current_ingredients}" ]
        2. METHOD: {output_of_cook_method}
        3. FLAVOR: {output_of_dominant_flavors}
        4. DIET: {output_of_healthier_food}
        5. EXTRA ITEMS: {output_of_extra_ingredients}

        ---
            
        LANGUAGE & FORMATTING RULES (STRICT):
        1. **Target Language**: The user has selected: **{languages}**.
        2. **Translate Everything**: You MUST translate ALL headers, labels, and content into **{languages}**.
           - Example: If Indonesian, use "Bahan-bahan" instead of "Ingredients".
           - Example: If Indonesian, use "Instruksi" instead of "Instructions".
        3. **No Preamble**: Start directly with the Recipe Name.

        ---
            
        OUTPUT FORMAT RULES (STRICT):
        1. **No Preamble**: Do NOT say "Here is your recipe" or explain the dish. Start directly with the Recipe Name.
        2. **No Analysis**: Do NOT output "Phase 1" or ingredient analysis.
        3. **Structure**: STRICTLY follow the structure below, BUT translate the headers (like 'Ingredients', 'Instructions') to **{languages}**.

        OUTPUT STRUCTURE (Translate headers to {languages}):

        [Recipe Name]

        [Header for Ingredients in {languages}]:
        - [Quantity] [Ingredient]
        - [Quantity] [Ingredient]

        [Header for Instructions in {languages}]:
        Step 1: [Short, direct instruction]
        Step 2: [Short, direct instruction]
        Step 3: [Short, direct instruction]
        """