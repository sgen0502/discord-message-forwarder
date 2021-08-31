from discord.ext import commands
import discord
from os import getenv
import traceback
import re

bot = commands.Bot(command_prefix='/')
guild = discord.Guild

# Values from env
token = getenv('DISCORD_BOT_TOKEN')
botName = getenv('BOT_NAME')
adminIds = getenv('ADMIN_IDS')
target_channels = getenv('TARGET_CHANNEL_IDS')
stat_permitted_channels = getenv('STAT_PERMITTED_CHANNELS')
autoMuteUsName = "AutoMuteUs"

# DEBUG VALUES
# botName = "LPE - 戦績BOT"
# adminIds = "764399156050919465, 766830246917046283, 779988796388671529"
# target_channels = "835968913513644042"
# stat_permitted_channels = "835945734229721168"


def admin_ids_to_mention(input_ids):
    return " ".join(list(map(lambda s: f'<@!{s.strip()}>', input_ids.split(","))))


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def my_stats(ctx):
    await ctx.send(f"{ctx.author.mention}が戦績の申請をしました。")
    await ctx.send(f'.au stats {ctx.author.mention}')


@bot.event
async def on_message(message):
    if ('.au st' in message.content and message.author.name != botName) and str(message.channel.id) not in stat_permitted_channels:
        await message.delete()

        mention = admin_ids_to_mention(adminIds)
        await message.channel.send(f"{message.author.mention} /my_stats以外での無許可な戦績確認は禁止されています。 この行為は運営へMentionされます。 {mention}")
    elif str(message.channel.id) in target_channels and message.author.name == autoMuteUsName:
        try:
            await message.delete()
            player_id = re.sub(r'^[\s\S]*?<@\!(\w+)>[\s\S]*?$', r'\1', message.embeds[0].description)
            user = await bot.fetch_user(int(player_id))
            channel = await user.create_dm()
            await channel.send(embed=message.embeds[0])
            await message.channel.send(f"{user.mention}のDMへ戦績が送られました。")
        except:
            await message.channel.send("戦績を取得中にエラーが発生しました。問題が続くようならNonaNekoに連絡してください。")
    else:
        await bot.process_commands(message)


bot.run(token)
