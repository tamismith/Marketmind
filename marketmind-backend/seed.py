from datetime import datetime, timedelta
from marketmind import create_app
from marketmind.extensions import db
from marketmind.models.user import User
from marketmind.models.business_profile import BusinessProfile
from marketmind.models.campaign import Campaign
from marketmind.models.generated_content import GeneratedContent
from marketmind.models.brand_memory import BrandMemory

app = create_app()

GLOWSKIN_CONTENT = [
    {
        "description": "Promote our new hydrating serum for summer",
        "variant_a": "Your skin deserves to glow. Our new hydrating serum is crafted for real skin, real moments. Feel confident in your own light this summer.",
        "variant_b": "New: GlowSkin Hydrating Serum. Clinically tested. 94% saw results in 7 days. Shop now and transform your routine.",
        "eval_a": {"tone": "very_positive", "tone_label": "Very Positive", "tone_category": "positive", "score": 0.82, "vad": {"valence": 0.82, "arousal": 0.45, "arousal_label": "Moderate", "dominance": 0.38, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Highly enthusiastic and uplifting.", "energy_summary": "Moderate energy.", "voice_summary": "Balanced voice."}},
        "eval_b": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.61, "vad": {"valence": 0.61, "arousal": 0.31, "arousal_label": "Low", "dominance": 0.62, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Warm and encouraging.", "energy_summary": "Calm and measured.", "voice_summary": "Confident and purposeful."}},
        "selected": "A",
        "platform": "Instagram",
    },
    {
        "description": "Winter skincare campaign — dry skin awareness",
        "variant_a": "Winter is hard on your skin. Wrap it in warmth with GlowSkin's deeply nourishing moisturiser. Because glowing skin doesn't take a season off.",
        "variant_b": "Combat dry skin this winter. GlowSkin Moisturiser — dermatologist approved, fragrance-free. Get yours before the cold sets in.",
        "eval_a": {"tone": "very_positive", "tone_label": "Very Positive", "tone_category": "positive", "score": 0.78, "vad": {"valence": 0.78, "arousal": 0.41, "arousal_label": "Moderate", "dominance": 0.35, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Warm and uplifting.", "energy_summary": "Moderate energy.", "voice_summary": "Balanced voice."}},
        "eval_b": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.55, "vad": {"valence": 0.55, "arousal": 0.28, "arousal_label": "Low", "dominance": 0.65, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Confident."}},
        "selected": "A",
        "platform": "Instagram",
    },
    {
        "description": "Introduce GlowSkin loyalty programme",
        "variant_a": "Every purchase brings you closer to glowing rewards. Join the GlowSkin loyalty programme and let your skin journey earn you more.",
        "variant_b": "Join GlowSkin Rewards. Earn points on every order. Redeem for free products. Sign up today.",
        "eval_a": {"tone": "very_positive", "tone_label": "Very Positive", "tone_category": "positive", "score": 0.76, "vad": {"valence": 0.76, "arousal": 0.38, "arousal_label": "Moderate", "dominance": 0.33, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Enthusiastic.", "energy_summary": "Moderate.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.58, "vad": {"valence": 0.58, "arousal": 0.29, "arousal_label": "Low", "dominance": 0.68, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Assertive."}},
        "selected": "A",
        "platform": "Email",
    },
    {
        "description": "Flash sale — 20% off all products this weekend",
        "variant_a": "This weekend only — treat yourself to the glow you deserve. 20% off everything at GlowSkin. Your skin will thank you.",
        "variant_b": "Flash Sale: 20% off all GlowSkin products. This weekend only. Use code GLOW20 at checkout.",
        "eval_a": {"tone": "very_positive", "tone_label": "Very Positive", "tone_category": "positive", "score": 0.80, "vad": {"valence": 0.80, "arousal": 0.52, "arousal_label": "High", "dominance": 0.36, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Uplifting.", "energy_summary": "High energy.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.60, "vad": {"valence": 0.60, "arousal": 0.44, "arousal_label": "Moderate", "dominance": 0.70, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Positive.", "energy_summary": "Moderate.", "voice_summary": "Assertive."}},
        "selected": "A",
        "platform": "Instagram",
    },
    {
        "description": "New SPF50 sunscreen launch",
        "variant_a": "Sun-kissed, not sun-damaged. GlowSkin SPF50 keeps you radiant and protected all day. Wear it like a second skin.",
        "variant_b": "Introducing GlowSkin SPF50. Broad spectrum protection. Lightweight formula. No white cast. Available now.",
        "eval_a": {"tone": "very_positive", "tone_label": "Very Positive", "tone_category": "positive", "score": 0.79, "vad": {"valence": 0.79, "arousal": 0.43, "arousal_label": "Moderate", "dominance": 0.34, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Uplifting.", "energy_summary": "Moderate.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.57, "vad": {"valence": 0.57, "arousal": 0.30, "arousal_label": "Low", "dominance": 0.66, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Positive.", "energy_summary": "Calm.", "voice_summary": "Assertive."}},
        "selected": "A",
        "platform": "Facebook",
    },
    {
        "description": "Customer testimonial campaign",
        "variant_a": "Real skin. Real results. Real people. Hear what our customers are saying about their GlowSkin journey.",
        "variant_b": "Over 10,000 five-star reviews. See why customers trust GlowSkin. Read their stories.",
        "eval_a": {"tone": "very_positive", "tone_label": "Very Positive", "tone_category": "positive", "score": 0.77, "vad": {"valence": 0.77, "arousal": 0.40, "arousal_label": "Moderate", "dominance": 0.32, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Warm.", "energy_summary": "Moderate.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.62, "vad": {"valence": 0.62, "arousal": 0.33, "arousal_label": "Low", "dominance": 0.64, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Confident."}},
        "selected": "B",
        "platform": "LinkedIn",
    },
]

FINTRUST_CONTENT = [
    {
        "description": "Launch campaign for FinTrust business account",
        "variant_a": "Your business finances deserve a partner you can trust. FinTrust Business Account — built for growth, designed for clarity.",
        "variant_b": "Open a FinTrust Business Account today. No monthly fees. Real-time analytics. FSCS protected. Apply in 10 minutes.",
        "eval_a": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.52, "vad": {"valence": 0.52, "arousal": 0.28, "arousal_label": "Low", "dominance": 0.55, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Confident."}},
        "eval_b": {"tone": "neutral", "tone_label": "Neutral", "tone_category": "neutral", "score": 0.12, "vad": {"valence": 0.12, "arousal": 0.22, "arousal_label": "Low", "dominance": 0.78, "dominance_label": "Very Assertive"}, "explanation": {"tone_summary": "Balanced and objective.", "energy_summary": "Calm.", "voice_summary": "Commanding."}},
        "selected": "B",
        "platform": "LinkedIn",
    },
    {
        "description": "Promote FinTrust savings account interest rate",
        "variant_a": "Make your money work as hard as you do. FinTrust Savings — competitive rates, zero hassle, total peace of mind.",
        "variant_b": "4.8% AER. FinTrust Savings Account. FSCS protected up to £85,000. Start saving in minutes.",
        "eval_a": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.54, "vad": {"valence": 0.54, "arousal": 0.30, "arousal_label": "Low", "dominance": 0.52, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Warm.", "energy_summary": "Calm.", "voice_summary": "Confident."}},
        "eval_b": {"tone": "neutral", "tone_label": "Neutral", "tone_category": "neutral", "score": 0.08, "vad": {"valence": 0.08, "arousal": 0.20, "arousal_label": "Low", "dominance": 0.80, "dominance_label": "Very Assertive"}, "explanation": {"tone_summary": "Objective.", "energy_summary": "Calm.", "voice_summary": "Commanding."}},
        "selected": "B",
        "platform": "LinkedIn",
    },
    {
        "description": "FinTrust app download campaign",
        "variant_a": "Banking on the go, finally done right. The FinTrust app puts full control of your finances in your pocket.",
        "variant_b": "Download the FinTrust app. Manage accounts, track spending, transfer funds. Rated 4.9 on the App Store.",
        "eval_a": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.50, "vad": {"valence": 0.50, "arousal": 0.29, "arousal_label": "Low", "dominance": 0.50, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "neutral", "tone_label": "Neutral", "tone_category": "neutral", "score": 0.10, "vad": {"valence": 0.10, "arousal": 0.21, "arousal_label": "Low", "dominance": 0.76, "dominance_label": "Very Assertive"}, "explanation": {"tone_summary": "Objective.", "energy_summary": "Calm.", "voice_summary": "Commanding."}},
        "selected": "B",
        "platform": "Facebook",
    },
    {
        "description": "FinTrust fraud protection feature launch",
        "variant_a": "Sleep soundly knowing FinTrust has your back. Our 24/7 fraud protection monitors every transaction so you never have to worry.",
        "variant_b": "24/7 fraud monitoring. Instant alerts. Zero liability policy. FinTrust keeps your money safe. Learn more.",
        "eval_a": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.48, "vad": {"valence": 0.48, "arousal": 0.26, "arousal_label": "Low", "dominance": 0.48, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Reassuring.", "energy_summary": "Calm.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "neutral", "tone_label": "Neutral", "tone_category": "neutral", "score": 0.09, "vad": {"valence": 0.09, "arousal": 0.19, "arousal_label": "Low", "dominance": 0.79, "dominance_label": "Very Assertive"}, "explanation": {"tone_summary": "Objective.", "energy_summary": "Calm.", "voice_summary": "Commanding."}},
        "selected": "B",
        "platform": "Email",
    },
    {
        "description": "FinTrust business loan product",
        "variant_a": "Your next big move deserves the right financial backing. FinTrust Business Loans — flexible terms, fast decisions, real support.",
        "variant_b": "FinTrust Business Loans. Up to £500k. Decision in 24 hours. Competitive rates. Apply now.",
        "eval_a": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.51, "vad": {"valence": 0.51, "arousal": 0.27, "arousal_label": "Low", "dominance": 0.53, "dominance_label": "Assertive"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Confident."}},
        "eval_b": {"tone": "neutral", "tone_label": "Neutral", "tone_category": "neutral", "score": 0.07, "vad": {"valence": 0.07, "arousal": 0.18, "arousal_label": "Low", "dominance": 0.82, "dominance_label": "Very Assertive"}, "explanation": {"tone_summary": "Objective.", "energy_summary": "Calm.", "voice_summary": "Commanding."}},
        "selected": "B",
        "platform": "LinkedIn",
    },
    {
        "description": "Year-end financial review campaign",
        "variant_a": "A new year is a fresh start for your finances. Let FinTrust help you plan smarter and save better in the year ahead.",
        "variant_b": "Year-end financial review. FinTrust advisors available now. Book a free 30-minute session. Secure your 2026 finances.",
        "eval_a": {"tone": "positive", "tone_label": "Positive", "tone_category": "positive", "score": 0.53, "vad": {"valence": 0.53, "arousal": 0.25, "arousal_label": "Low", "dominance": 0.49, "dominance_label": "Balanced"}, "explanation": {"tone_summary": "Encouraging.", "energy_summary": "Calm.", "voice_summary": "Balanced."}},
        "eval_b": {"tone": "neutral", "tone_label": "Neutral", "tone_category": "neutral", "score": 0.11, "vad": {"valence": 0.11, "arousal": 0.20, "arousal_label": "Low", "dominance": 0.77, "dominance_label": "Very Assertive"}, "explanation": {"tone_summary": "Objective.", "energy_summary": "Calm.", "voice_summary": "Commanding."}},
        "selected": "B",
        "platform": "Email",
    },
]


def seed():
    with app.app_context():

        # --- GlowSkin ---
        if not User.query.filter_by(email="glowskin@demo.com").first():
            glow_user = User(email="glowskin@demo.com", credits=200, subscription_tier="pro")
            glow_user.set_password("Demo1234!")
            db.session.add(glow_user)
            db.session.flush()

            db.session.add(BusinessProfile(
                user_id=glow_user.id,
                business_name="GlowSkin",
                industry="Beauty & Skincare",
                target_audience="Women aged 20-40 interested in natural skincare",
                region="UK",
                website="www.glowskin.co.uk",
            ))

            glow_campaign = Campaign(
                user_id=glow_user.id,
                name="Summer Glow 2026",
                goal="Drive product awareness and online sales",
                target_valence=0.75,
                target_arousal=0.45,
                target_dominance=0.35,
            )
            db.session.add(glow_campaign)
            db.session.flush()

            base_date = datetime.utcnow() - timedelta(days=30)
            for i, c in enumerate(GLOWSKIN_CONTENT):
                created = base_date + timedelta(days=i * 4)
                eval_a = c["eval_a"].copy()
                eval_b = c["eval_b"].copy()
                selected_eval = eval_a if c["selected"] == "A" else eval_b
                selected_eval["vad_alignment"] = {"valence": 0.88, "arousal": 0.91, "dominance": 0.85, "overall": 0.88}

                db.session.add(GeneratedContent(
                    user_id=glow_user.id,
                    content_type="text",
                    description=c["description"],
                    original_prompt=f"Business: GlowSkin\nPlatform: {c['platform']}\nDescription: {c['description']}",
                    variant_a_text=c["variant_a"],
                    variant_b_text=c["variant_b"],
                    variant_a_eval_json=eval_a,
                    variant_b_eval_json=eval_b,
                    selected_variant=c["selected"],
                    campaign_id=glow_campaign.id,
                    created_at=created,
                ))

            db.session.add(BrandMemory(
                user_id=glow_user.id,
                preferred_tone="very_positive",
                style_notes="Warm, personal, emotionally resonant. Uses soft imagery and relatable moments.",
                cta_preferences="Discover your glow",
                preferred_creativity=0.83,
                learned_valence=0.79,
                learned_arousal=0.43,
                learned_dominance=0.35,
                selection_count=6,
            ))

            print("GlowSkin seeded.")
        else:
            print("GlowSkin already exists, skipping.")

        # --- FinTrust ---
        if not User.query.filter_by(email="fintrust@demo.com").first():
            fin_user = User(email="fintrust@demo.com", credits=200, subscription_tier="pro")
            fin_user.set_password("Demo1234!")
            db.session.add(fin_user)
            db.session.flush()

            db.session.add(BusinessProfile(
                user_id=fin_user.id,
                business_name="FinTrust",
                industry="Financial Services",
                target_audience="UK SMEs and professionals aged 30-55",
                region="UK",
                website="www.fintrust.co.uk",
            ))

            fin_campaign = Campaign(
                user_id=fin_user.id,
                name="Q2 Acquisition 2026",
                goal="Drive account sign-ups and product awareness",
                target_valence=0.1,
                target_arousal=0.2,
                target_dominance=0.8,
            )
            db.session.add(fin_campaign)
            db.session.flush()

            base_date = datetime.utcnow() - timedelta(days=30)
            for i, c in enumerate(FINTRUST_CONTENT):
                created = base_date + timedelta(days=i * 4)
                eval_a = c["eval_a"].copy()
                eval_b = c["eval_b"].copy()
                selected_eval = eval_a if c["selected"] == "A" else eval_b
                selected_eval["vad_alignment"] = {"valence": 0.92, "arousal": 0.89, "dominance": 0.94, "overall": 0.92}

                db.session.add(GeneratedContent(
                    user_id=fin_user.id,
                    content_type="text",
                    description=c["description"],
                    original_prompt=f"Business: FinTrust\nPlatform: {c['platform']}\nDescription: {c['description']}",
                    variant_a_text=c["variant_a"],
                    variant_b_text=c["variant_b"],
                    variant_a_eval_json=eval_a,
                    variant_b_eval_json=eval_b,
                    selected_variant=c["selected"],
                    campaign_id=fin_campaign.id,
                    created_at=created,
                ))

            db.session.add(BrandMemory(
                user_id=fin_user.id,
                preferred_tone="neutral",
                style_notes="Professional, data-driven, concise. Leads with facts and figures.",
                cta_preferences="Apply now",
                preferred_creativity=0.17,
                learned_valence=0.10,
                learned_arousal=0.21,
                learned_dominance=0.79,
                selection_count=6,
            ))

            print("FinTrust seeded.")
        else:
            print("FinTrust already exists, skipping.")

        db.session.commit()
        print("Done.")


if __name__ == "__main__":
    seed()
