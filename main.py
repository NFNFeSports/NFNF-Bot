import discord
import requests
import asyncio
import pandas as pd

# Insira o token do bot aqui
TOKEN = os.getenv('DISCORD_TOKEN')  # Use the secret you just added
# Defina o canal onde o bot vai postar as informações
CHANNEL_ID = 1290630295892004875  # Substitua pelo ID do seu canal

# Dicionário para armazenar equipes e seus jogadores
teams = {}
# Lista para armazenar resultados das partidas
match_results = {}

# Importar intents e criar um objeto intents
intents = discord.Intents.default()
intents.messages = True  # Permitir acesso às mensagens
intents.guilds = True  # Permitir acesso aos guilds (servidores)

client = discord.Client(intents=intents)  # Passar os intents para o Client

# Função para calcular as estatísticas das equipes (pontuação, kill leader, etc)
def calculate_scores():
    teams_scores = {}
    for team, results in match_results.items():
        total_kills = sum(result["kills"] for result in results)
        total_placement_points = sum(result["placement_points"] for result in results)
        
        total_points = total_kills + total_placement_points
        teams_scores[team] = {"points": total_points, "kills": total_kills}

    return teams_scores

# Função para postar as estatísticas no Discord
async def post_scores_to_discord():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        teams_scores = calculate_scores()
        scores_message = "Pontuações atuais:\n"
        for team, stats in teams_scores.items():
            scores_message += f"{team}: {stats['points']} pontos ({stats['kills']} kills)\n"

        await channel.send(scores_message)

@client.event
async def on_message(message):
    # Ignora mensagens enviadas pelo próprio bot
    if message.author == client.user:
        return

    # Comando para registrar uma equipe
    if message.content.startswith('!registrar'):
        team_name = message.content.split(' ')[1]  # Ex: !registrar nome_da_equipa
        if team_name not in teams:
            teams[team_name] = []  # Cria uma nova equipe se não existir
            await message.channel.send(f"Equipe '{team_name}' registrada com sucesso!")
        else:
            await message.channel.send(f"A equipe '{team_name}' já existe.")

    # Comando para adicionar jogadores à equipe
    if message.content.startswith('!adicionar'):
        parts = message.content.split(' ')
        team_name = parts[1]  # Nome da equipe
        player_name = message.author.name  # Nome do jogador que está enviando o comando

        if team_name in teams:
            if player_name not in teams[team_name]:
                teams[team_name].append(player_name)  # Adiciona o jogador à equipe
                await message.channel.send(f"Jogador '{player_name}' adicionado à equipe '{team_name}'.")
            else:
                await message.channel.send(f"Jogador '{player_name}' já está na equipe '{team_name}'.")
        else:
            await message.channel.send(f"A equipe '{team_name}' não existe.")

    # Comando para registrar resultados de uma partida
    if message.content.startswith('!resultados'):
        parts = message.content.split(' ')
        team_name = parts[1]  # Nome da equipe
        kills = int(parts[2])  # Kills da equipe
        placement = int(parts[3])  # Colocação da equipe

        placement_points = {
            1: 12, 2: 9, 3: 7, 4: 5, 5: 4,
            6: 3, 7: 2, 8: 1, 9: 1, 10: 1,
            11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
        }

        if team_name not in match_results:
            match_results[team_name] = []
        
        match_results[team_name].append({
            "kills": kills,
            "placement_points": placement_points.get(placement, 0)
        })

        await message.channel.send(f"Resultados registrados para a equipe '{team_name}': {kills} kills, posição {placement}.")

    # Comando para ver as pontuações atuais
    if message.content.startswith('!pontuacoes'):
        await post_scores_to_discord()

# Evento para quando o bot estiver pronto
@client.event
async def on_ready():
    print(f'{client.user} está conectado ao Discord!')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("O bot está online e pronto para o torneio!")

# Iniciar o bot
client.run(TOKEN)
