"""StyleAI recommendation engine.

This module is intentionally independent from Flask. The current version combines
user selections with simple image metadata so the full product flow works without
an external paid AI API. Replace get_recommendation() with a vision/LLM call later
if you want true image understanding.
"""
from pathlib import Path


def _image_note(image_path):
    if not image_path:
        return ""
    path = Path(image_path)
    if not path.exists():
        return ""
    size_mb = path.stat().st_size / (1024 * 1024)
    return f"Your uploaded photo ({size_mb:.1f} MB) was received successfully."


def get_recommendation(occasion, outfit_type, color, image_path=None):
    occasion_key = occasion.strip().lower()
    type_key = outfit_type.strip().lower()
    color_key = color.strip().lower()
    color_name = color.strip().title()

    occasion_data = {
        "college": ("College-ready", "Keep it youthful, comfortable and easy to wear throughout the day."),
        "casual": ("Smart Casual", "Use relaxed pieces with clean proportions and simple accessories."),
        "party": ("Party Ready", "Use one statement element and sharper styling so the outfit stands out."),
        "formal": ("Polished Formal", "Choose a clean silhouette, restrained accessories and polished footwear."),
        "wedding": ("Wedding Guest", "Aim for a refined festive look with coordinated colors and dressier footwear."),
        "office": ("Office Ready", "Keep the outfit professional, structured and understated."),
    }
    title_prefix, occasion_advice = occasion_data.get(
        occasion_key, ("Personalized Look", "Balance comfort, fit and color coordination for the occasion.")
    )

    outfit_data = {
        "t-shirt": "Wear the T-shirt with well-fitted jeans or chinos and clean sneakers.",
        "shirt": "Pair the shirt with tailored trousers or dark jeans and loafers or minimal sneakers.",
        "jacket": "Layer the jacket over a simple top and keep the bottom half clean and fitted.",
        "jeans": "Balance the jeans with a clean shirt or T-shirt and footwear appropriate for the occasion.",
        "traditional": "Choose coordinated traditional pieces with a clean silhouette and simple accessories.",
        "formal": "Use a fitted formal shirt or blazer combination with tailored trousers and polished shoes.",
    }
    outfit_advice = outfit_data.get(type_key, "Choose well-fitted pieces and keep the overall silhouette balanced.")

    color_data = {
        "white": "White is highly versatile; combine it with navy, black, denim or muted neutrals.",
        "black": "Black gives a sharp base; add one lighter or textured element for contrast.",
        "blue": "Blue works especially well with white, beige, grey and darker denim.",
        "red": "Let red be the focal color and keep the remaining pieces neutral.",
        "green": "Green pairs naturally with beige, white, black and earthy neutrals.",
        "beige": "Beige works naturally with white, brown, olive, navy and black.",
        "grey": "Grey is easy to layer; combine it with white, black, navy or one accent color.",
        "pink": "Balance pink with white, navy, grey or beige for a clean result.",
    }
    color_advice = color_data.get(color_key, f"Use {color_name} as the main color and keep the other pieces neutral.")

    accessories = {
        "college": "Minimal watch, clean sneakers and a simple backpack.",
        "casual": "Simple watch, clean sneakers and one understated accessory.",
        "party": "A watch, subtle bracelet and clean statement footwear.",
        "formal": "Classic watch, leather belt and polished shoes; keep accessories minimal.",
        "wedding": "Elegant watch, coordinated belt/shoes and one tasteful accessory.",
        "office": "Classic watch, matching belt and clean formal shoes.",
    }.get(occasion_key, "A simple watch and minimal accessories matched to the occasion.")

    image_note = _image_note(image_path)
    summary = (
        f"For a {occasion} setting, the strongest direction is a {color_name} {outfit_type.lower()} look. "
        f"{occasion_advice} {image_note}"
    )

    return {
        "title": f"{title_prefix} {outfit_type.title()} Look",
        "summary": summary,
        "outfit": outfit_advice,
        "color": color_advice,
        "occasion": occasion_advice,
        "accessories": accessories,
        "nextStep": "Try the combination, check the fit in the mirror, then adjust footwear or one accessory to match your personality.",
    }
