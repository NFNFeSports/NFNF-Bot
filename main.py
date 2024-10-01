import discord
import requests
import asyncio
import pandas as pd

# Insira o token do bot aqui
TOKEN = os.getenv('DISCORD_TOKEN')  # Substitua pelo seu token
CHANNEL_ID = 1290630295892004875  # Substitua pelo ID do seu canal

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

# Simulação de chamada para a API, modifique conforme necessário
def get_match_data():
    # Simulação de dados de partida
    return {
        "teams": [
            {"name": "Team A", "kills": 10, "placement": 1},
            {"name": "Team B", "kills": 5, "placement": 2},
            {"name": "Team C", "kills": 3, "placement": 3},
        ]
    }

def calculate_scores(match_data):
    teams_scores = {}
    kill_leader = {"name": "", "kills": 0}

    for team in match_data["teams"]:
        kills = team["kills"]
        placement = team["placement"]
        team_points = 12 - placement + kills  # Exemplo de pontuação
        teams_scores[team["name"]] = {"points": team_points, "kills": kills}

        if kills > kill_leader["kills"]:
            kill_leader["name"] = team["name"]
            kill_leader["kills"] = kills

    return teams_scores, kill_leader

async def post_scores_to_discord(teams_scores, kill_leader):
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        scores_message = "Pontuações atuais:\n"
        for team, stats in teams_scores.items():
            scores_message += f"{team}: {stats['points']} pontos ({stats['kills']} kills)\n"
        scores_message += f"\n**Kill Leader atual**: {kill_leader['name']} ({kill_leader['kills']} kills)"
        await channel.send(scores_message)

@client.event
async def on_ready():
    print(f'{client.user} está conectado ao Discord!')
    while True:
        match_data = get_match_data()
        teams_scores, kill_leader = calculate_scores(match_data)
        await post_scores_to_discord(teams_scores, kill_leader)
        await asyncio.sleep(600)  # Espera 10 minutos

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!teste'):
        await message.channel.send('O bot está funcionando!')

client.run(TOKEN)
