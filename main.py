import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
load_dotenv()  # Carrega as variáveis do arquivo .env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    if bot.user is not None:
        print(f'Bot conectado como {bot.user.name}')
    else:
        print('Bot conectado, mas bot.user é None')

@bot.command(name='poll', help='Cria uma enquete. Uso: !poll "Pergunta" "Opção1" "Opção2" ...')
async def create_poll(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Você precisa fornecer pelo menos 2 opções para a enquete.")
        return
    
    if len(options) > 10:
        await ctx.send("Você pode fornecer no máximo 10 opções para a enquete.")
        return
    
    # Criando embed para a enquete
    embed = discord.Embed(
        title=f"📊 Enquete: {question}",
        description="\n".join([f"{i+1}. {option}" for i, option in enumerate(options)]),
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Enquete criada por {ctx.author.display_name}")
    
    poll_message = await ctx.send(embed=embed)
    
    # Adicionando reações
    for i in range(len(options)):
        await poll_message.add_reaction(chr(127462 + i))  # Emojis de A, B, C, etc.

@bot.command(name='timerpoll', help='Cria uma enquete com temporizador. Uso: !timerpoll 60 "Pergunta" "Opção1" "Opção2" ...')
async def create_timer_poll(ctx, minutes: int, question, *options):
    if len(options) < 2:
        await ctx.send("Você precisa fornecer pelo menos 2 opções para a enquete.")
        return
    
    if len(options) > 10:
        await ctx.send("Você pode fornecer no máximo 10 opções para a enquete.")
        return
    
    # Criando embed para a enquete
    embed = discord.Embed(
        title=f"⏳ Enquete: {question} (Termina em {minutes} minutos)",
        description="\n".join([f"{i+1}. {option}" for i, option in enumerate(options)]),
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Enquete criada por {ctx.author.display_name}")
    
    poll_message = await ctx.send(embed=embed)
    
    # Adicionando reações
    for i in range(len(options)):
        await poll_message.add_reaction(chr(127462 + i))
    
    # Esperando o tempo especificado
    await asyncio.sleep(minutes * 60)
    
    # Atualizando a mensagem com os resultados
    refreshed_message = await ctx.channel.fetch_message(poll_message.id)
    results = {}
    
    for reaction in refreshed_message.reactions:
        if reaction.emoji in [chr(127462 + i) for i in range(len(options))]:
            option_index = ord(reaction.emoji) - 127462
            results[options[option_index]] = reaction.count - 1  # Subtraindo 1 para remover a reação do bot
    
    # Criando embed de resultados
    result_embed = discord.Embed(
        title=f"🏆 Resultados: {question}",
        description="\n".join([f"**{option}**: {votes} votos" for option, votes in results.items()]),
        color=discord.Color.green()
    )
    result_embed.set_footer(text="Enquete encerrada")
    
    await poll_message.edit(embed=result_embed)

@bot.command(name='clearpolls', help='Limpa todas as enquetes do canal')
@commands.has_permissions(manage_messages=True)
async def clear_polls(ctx, limit: int = 20):
    def is_poll(m):
        return m.author == bot.user and len(m.embeds) > 0 and ("Enquete:" in m.embeds[0].title)
    
    deleted = await ctx.channel.purge(limit=limit, check=is_poll)
    await ctx.send(f"🗑️ {len(deleted)} enquetes removidas.", delete_after=5)

# Inicializar o bot
if __name__ == "__main__":
    import os
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("O token do Discord não foi encontrado. Defina a variável de ambiente DISCORD_TOKEN.")
    bot.run(token)