import pandas as pd


def cloth_recommend(uv_index):
    # Clothing recommendations with corresponding image filenames
    clothing_recommendations = {
        0: (
            "You can wear light and breathable clothing such as short sleeves and shorts. "
            "Ensure to apply sunscreen on exposed areas.",
            "Hat_shortshirt_shortpants",
        ),  # Example image filenames without file extension
        1: (
            "Light clothing like short sleeves and shorts are suitable. "
            "Consider wearing a wide-brimmed hat.",
            "Hat_shortshirt_shortpants",
        ),
        2: (
            "Light clothing like short sleeves and shorts are suitable. "
            "Don't forget to apply sunscreen.",
            "Hat_shortshirt_shortpants",
        ),
        3: (
            "Wear clothing that provides moderate protection such as long sleeves, pants, and a wide-brimmed hat. "
            "Apply sunscreen generously.",
            "Hat_longshirt_longpants",
        ),
        4: (
            "Opt for clothing with sun protection like long sleeves, pants, and a wide-brimmed hat. ",
            "Hat_longshirt_longpants",
        ),
        5: (
            "Choose clothing with strong sun protection such as long sleeves, pants, a wide-brimmed hat, and sunglasses.",
            "Hat_Sunnies_UVprotection_longpants",
        ),
        6: (
            "Wear clothing with maximum sun protection and consider staying indoors or seeking shade during peak sun hours.",
            "Hat_Sunnies_UVprotection_longpants",
        ),
        7: (
            "Stay indoors or wear clothing with maximum sun protection if you need to go outside. "
            "Avoid direct sun exposure.",
            "Hat_Sunnies_UVprotection_longpants",
        ),
        8: (
            "Avoid outdoor activities if possible. If you must go outside, wear clothing with maximum sun protection "
            "and stay in shaded areas.",
            "Hat_Sunnies_UVprotection_longpants",
        ),
        9: (
            "Limit outdoor activities to essential tasks only. Wear clothing with maximum sun protection and avoid sun exposure.",
            "DarkHat_Sunnies_darkUV_darkpants",
        ),
        10: (
            "Avoid outdoor activities. If you need to go outside, wear clothing with maximum sun protection, "
            "seek shade, and limit sun exposure.",
            "DarkHat_Sunnies_darkUV_darkpants",
        ),
        11: (
            "Avoid outdoor activities completely. Stay indoors or wear protective clothing if you need to go outside "
            "for essential tasks.",
            "DarkHat_Sunnies_darkUV_darkpants",
        ),
        12: (
            "Avoid outdoor activities at all costs. Stay indoors and keep all skin covered to prevent sunburn and skin damage.",
            "DarkHat_Sunnies_darkUV_darkpants",
        ),
    }

    recommendation, image_filenames = clothing_recommendations.get(
        uv_index, ("No specific recommendation for this UV index.", None)
    )

    if isinstance(image_filenames, str):  # Check if image_filenames is a string
        return recommendation, ",".join(image_filenames.split("_"))
    else:
        return recommendation, None


def sunscreen_recommend(uv_index, height, weight, activity_type):
    # Calculate usage
    def calculate_sunscreen_usage(uv_index, height, weight, activity_type):
        # Calculate body surface area
        body_surface_area = (0.0061 * height + 0.0124 * weight - 0.0099) * 10000
        # Ratios of different body parts
        body_parts_ratio = {
            "Face": 0.03,
            "Neck": 0.03,
            "Single Arm": 0.09,
            "Single thigh": 0.09,
            "Single calf": 0.09,
            "Chest and Abdomen": 0.18,
            "Back": 0.18,
        }
        # Sunscreen usage factors for different activity types
        activity_factors = {
            "Swimming/Water Activity": 2,
            "High Intensity Sports": 1.5,
            "Low Intensity Sports": 1,
        }
        # Generate a list of sunscreen amounts and corresponding descriptions
        sunscreen_amounts = [
            {"ml": 1, "description": "a green pea"},
            {"ml": 2, "description": "a small grape"},
            {"ml": 3, "description": "a mint leaf"},
            {"ml": 4, "description": "a fingernail size"},
            {"ml": 5, "description": "a teaspoon"},
            {"ml": 6, "description": "a coin diameter"},
            {"ml": 7, "description": "a piece of dragon fruit"},
            {"ml": 8, "description": "an egg size"},
            {"ml": 9, "description": "a palm size"},
            {"ml": 10, "description": "a coin size"},
            {"ml": 11, "description": "a potato size"},
            {"ml": 12, "description": "a strawberry size"},
            {"ml": 13, "description": "a small pear size"},
            {"ml": 14, "description": "an orange size"},
            {"ml": 15, "description": "a banana size"},
        ]

        # Adjust sunscreen usage based on activity type
        activity_factor = activity_factors.get(activity_type, 1)
        # Calculate sunscreen usage for each body part
        sunscreen_usage = {}
        for body_part, ratio in body_parts_ratio.items():
            ml_usage = (
                body_surface_area * ratio * 2 * activity_factor
            ) / 1000  # 将用量从毫克转换为毫升git
            # Find the corresponding description for the sunscreen amount
            for amount in sunscreen_amounts:
                if amount["ml"] >= ml_usage:
                    description = amount["description"]
                    break
            sunscreen_usage[body_part] = {
                "Sunscreen Usage (ml)": ml_usage,
                "Description": description,
            }

        return sunscreen_usage

    # Calculate sunscreen usage based on the selected activity type and UV index value
    sunscreen_usage = calculate_sunscreen_usage(uv_index, height, weight, activity_type)
    return pd.DataFrame.from_dict(sunscreen_usage, orient="index")

