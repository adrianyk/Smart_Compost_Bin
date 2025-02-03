def compost_recommendation(co2, tvoc, temperature, moisture):
    recommendations = []
    compact_summary = set()  # Use a set to avoid duplicate actions
    turn_compost = False

    # Air Quality Sensor (CO₂ & TVOCs)
    if co2 > 2000:
        recommendations.append("CO₂ is too high, indicating poor aeration and anaerobic activity.")
        recommendations.append("➡️ Suggested: Turn compost, add dry browns, reduce wet greens.")
        compact_summary.add("Turn compost")
        compact_summary.add("Add browns")
        turn_compost = True
    elif 400 <= co2 <= 1500:
        recommendations.append("✅ CO₂ is within the normal range.")

    if tvoc > 500:
        recommendations.append("TVOCs are too high, indicating gas buildup and potential odor issues.")
        recommendations.append("➡️ Suggested: Turn compost, balance greens & browns.")
        compact_summary.add("Turn compost")
        turn_compost = True

    # Temperature Sensor
    if temperature > 70:
        recommendations.append("🔥 Temperature is too high! Beneficial microbes may start dying.")
        recommendations.append("➡️ Suggested: Add more brown materials (dry leaves, cardboard) to cool down.")
        compact_summary.add("Add browns")
        turn_compost = True
    elif 55 <= temperature <= 65:
        recommendations.append("✅ Temperature is in the ideal decomposition range.")
    elif 45 <= temperature < 55:
        recommendations.append("⚠️ Temperature is slowing down, decomposition is less efficient.")
        recommendations.append("➡️ Suggested: Turn compost to aerate, check moisture levels.")
        compact_summary.add("Turn compost")
        turn_compost = True
    elif 40 <= temperature < 45:
        recommendations.append("❄️ Microbial activity is too low.")
        recommendations.append("➡️ Suggested: Turn compost, add nitrogen-rich greens (food scraps, grass).")
        compact_summary.add("Turn compost")
        compact_summary.add("Add greens")
        turn_compost = True
    elif temperature < 15:
        recommendations.append("🥶 Temperature is too low, decomposition is nearly stopped.")
        recommendations.append("➡️ Suggested: Add more greens, insulate bin with tarp.")
        compact_summary.add("Add greens")
        compact_summary.add("Insulate bin")
        turn_compost = True

    # Moisture Sensor
    if moisture > 70:
        recommendations.append("💦 Moisture is too high, leading to anaerobic conditions and bad odors.")
        recommendations.append("➡️ Suggested: Add dry browns (shredded newspaper, sawdust), turn compost.")
        compact_summary.add("Turn compost")
        compact_summary.add("Add browns")
        turn_compost = True
    elif 40 <= moisture <= 60:
        recommendations.append("✅ Moisture level is ideal.")
    elif moisture < 30:
        recommendations.append("🌱 Compost is too dry, microbial activity may slow down.")
        recommendations.append("➡️ Suggested: Add water, mix with wet greens.")
        compact_summary.add("Add water")
        compact_summary.add("Add greens")
        turn_compost = True

    # Convert lists to formatted strings with line breaks
    return {
        "detailed_explanation": "\n".join(recommendations),
        "compact_summary": ", ".join(compact_summary),
        "turn_compost": turn_compost
    }

# Example Test Case
example_data = compost_recommendation(co2=2500, tvoc=600, temperature=50, moisture=25)
print("📋 **Detailed Explanation:**\n" + example_data["detailed_explanation"])
print("\n📝 **Compact Summary:** " + example_data["compact_summary"])
print("\n🔄 **Turn Compost?** " + ("✅ Yes" if example_data["turn_compost"] else "❌ No"))