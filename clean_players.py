# Read players from file
with open("players.txt", "r") as file:
    players_list = file.readlines()

# Remove duplicates while preserving order
cleaned_players = list(dict.fromkeys([player.strip() for player in players_list]))

# Save cleaned list back to file
with open("cleaned_players.txt", "w") as file:
    file.write("\n".join(cleaned_players))

print("✅ Cleaned players list saved to cleaned_players.txt")
