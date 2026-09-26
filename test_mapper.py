from agents.supply_chain_mapper import supply_chain_mapper


result = supply_chain_mapper(
    "A major flood has disrupted a component supplier in Chennai. "
    "The supplier provides electronic components to Andhra Electronics."
)

print("\n========== SUPPLY CHAIN MAPPER ==========\n")

print("Success:", result["success"])
print("Provider:", result.get("provider"))

print("\nMapped Supply Chain:\n")

print(result.get("data"))
