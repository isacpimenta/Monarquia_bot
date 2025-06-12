import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Monarquia está Online")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # ignora comandos que não existem
    raise error  # relança outros erros


champions_by_lane = {
    "top": [
        "Darius", "Garen", "Camille", "Fiora", "Shen", "Malphite", "Ornn",
        "Irelia", "Sett", "Renekton", "Mordekaiser", "Riven", "Kennen",
        "Rumble", "Teemo", "Jayce", "Aatrox", "Akshan", "Vladimir"
    ],
    "jungle": [
        "Lee Sin", "Kayn", "Warwick", "Elise", "Kha'Zix", "Evelynn",
        "Graves", "Rengar", "Nidalee", "Udyr", "Olaf", "Jarvan IV",
        "Zac", "Sejuani", "Kindred", "Volibear", "Lillia", "Rammus"
    ],
    "mid": [
        "Ahri", "Zed", "Yasuo", "LeBlanc", "Veigar", "Syndra", "Orianna",
        "Talon", "Viktor", "Annie", "Katarina", "Twisted Fate",
        "Fizz", "Cassiopeia", "Galio", "Lux", "Malzahar", "Neeko"
    ],
    "adc": [
        "Jinx", "Kai'Sa", "Ezreal", "Caitlyn", "Ashe", "Miss Fortune",
        "Tristana", "Varus", "Vayne", "Draven", "Aphelios", "Senna",
        "Samira", "Lucian"
    ],
    "support": [
        "Thresh", "Nautilus", "Leona", "Soraka", "Lulu", "Braum", "Alistar",
        "Janna", "Morgana", "Zyra", "Rakan", "Nami", "Seraphine",
        "Yuumi", "Senna", "Pyke"
    ],
}

@bot.command()
async def ola(ctx: commands.Context):
    nome = ctx.author.name
    await ctx.reply(f"Olá, {nome}! Tudo bem?")

@bot.command()
async def sortear(ctx: commands.Context, *, nomes: str):
    import random

    if "," in nomes:
        jogadores = [j.strip() for j in nomes.split(",") if j.strip()]
    else:
        jogadores = [j.strip() for j in nomes.split() if j.strip()]

    random.shuffle(jogadores)
    posicoes = ["🛡️ Top", "🌲 Jungle", "🔥 Mid", "🏹 ADC", "💖 Support"]

    if len(jogadores) >= 10:
        # Calcula quantos múltiplos de 5 cabem
        total_jogadores = (len(jogadores) // 5) * 5
        sobra = len(jogadores) - total_jogadores

        jogadores_utilizados = jogadores[:total_jogadores]
        sobrou = jogadores[total_jogadores:]

        times = [jogadores_utilizados[i:i+5] for i in range(0, total_jogadores, 5)]

        resposta = "**🎮 Sorteio de Times e Posições do LoL:**\n\n"

        for i, time in enumerate(times, start=1):
            cor = "🟥" if i % 2 == 1 else "🟦"
            resposta += f"{cor} **Time {i}**\n"
            for posicao, jogador in zip(posicoes, time):
                resposta += f"{posicao}: {jogador}\n"
            resposta += "\n"

        if sobra > 0:
            resposta += f"👥 Jogadores sem posição (sobrando): {', '.join(sobrou)}"

    else:
        resposta = "**🎮 Sorteio de posições do LoL:**\n\n"
        for posicao, jogador in zip(posicoes, jogadores):
            resposta += f"{posicao}: {jogador}\n"

        extras = jogadores[len(posicoes):]
        if extras:
            resposta += "\n👥 Jogadores sem posição (sobrando):\n"
            resposta += ", ".join(extras)

    await ctx.send(resposta)

VERSAO = "13.12.1" 

def nome_para_imagem(champ_name):
    # Remove espaços, apóstrofos e caracteres especiais, adapta para o formato da Riot
    nome = champ_name.replace("'", "").replace(" ", "")
    return nome

@bot.command()
async def lolChamp(ctx, lane: str = None):
    import random

    lane = lane.lower() if lane else None
    lanes_validas = list(champions_by_lane.keys())

    if lane:
        if lane not in lanes_validas:
            await ctx.send("❌ Lane inválida! Use: top, jungle, mid, adc ou support.")
            return
        campeoes = champions_by_lane[lane]
        escolhido = random.choice(campeoes)
        lanes_texto = lane
    else:
        todas = [champ for lista in champions_by_lane.values() for champ in lista]
        escolhido = random.choice(todas)
        lanes = [l for l, lista in champions_by_lane.items() if escolhido in lista]
        lanes_texto = ", ".join(lanes)

    nome_imagem = nome_para_imagem(escolhido)
    url_img = f"https://ddragon.leagueoflegends.com/cdn/{VERSAO}/img/champion/{nome_imagem}.png"

    embed = discord.Embed(title=f"🎲 Campeão sorteado: {escolhido}", description=f"📍 Lanes: {lanes_texto}")
    embed.set_thumbnail(url=url_img)

    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
