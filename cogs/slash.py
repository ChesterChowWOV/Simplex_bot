# Slash commands
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ui import Button, View
from discord import Option, SlashCommand
import json
import random
import qrcode
import os
from simpcalc import simpcalc

calculator = simpcalc.Calculate()


def mic(ctx):
    return ctx.author.id == 481377376475938826

cogs = []
for i in os.listdir("cogs/"):
    if i == "__pycache__":
        pass
    else:
        print(i[:-3])
        
class CodeInput(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.code = None

        self.add_item(
            discord.ui.InputText(
                label="Please enter the code", style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        self.code = self.children[0].value
        return await interaction.response.send_message(
            "Running code now...", ephemeral=True
        )

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="invite", description="Creates 10 day invite for this server")
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_age=10)
        await ctx.respond(link)

    @commands.slash_command(name="botinvite", description="Invite simplex to your server :)")
    async def botinvite(self, ctx):
        await ctx.respond(embed=discord.Embed(title="Invite **'Simplex'?** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    
    @slash_command(name="suggest", description="Suggest something for Simplex")
    async def suggest(self, ctx, suggestion: Option(str, "The suggestion", required=True)):
        sid = await self.client.fetch_channel(908969607266730005)
        em = discord.Embed(
            title= "Suggestion:",
            description=f"By: {ctx.author.name}\n\n{suggestion}",
            color=discord.Color.random()
        )
        x = await sid.send(embed=em, content=ctx.author.id)
        await x.add_reaction("✅")
        await x.add_reaction("❌")
        
        await ctx.respond("Thank you for you suggestion!")

    @commands.slash_command(name="ping", description="shows you the bots ping")
    async def ping(self, ctx):
        await ctx.respond(f"{round(self.client.latency * 1000)}ms")

    @commands.slash_command(name="rps", description="Plays rock paper scissors with the bot")
    async def rps(self, ctx, rps: str):
        choices = ["rock", "paper", "scissors"]
        cpu_choice = random.choice(choices)
        em = discord.Embed(title="Rock Paper Scissors")
        rps = rps.lower()
        if rps == 'rock':
            if cpu_choice == 'rock':
                em.description = "It's a tie!"
            elif cpu_choice == 'scissors':
                em.description = "You win!"
            elif cpu_choice == 'paper':
                em.description = "You lose!"

        elif rps == 'paper':
            if cpu_choice == 'paper':
                em.description = "It's a tie!"
            elif cpu_choice == 'rock':
                em.description = "You win!"
            elif cpu_choice == 'scissors':
                em.description = "You lose!"

        elif rps == 'scissors':
            if cpu_choice == 'scissors':
                em.description = "It's a tie!"
            elif cpu_choice == 'paper':
                em.description = "You win!"
            elif cpu_choice == 'rock':
                em.description = "You lose!"

        else:
            em.description = "Invalid Input"

        em.add_field(name="Your Choice", value=rps)
        em.add_field(name="Bot Choice", value=cpu_choice)
        await ctx.respond(embed=em)


    
    @slash_command(name="reload", description="reloads a cog")
    @commands.check(mic)
    async def reload(self, ctx, extension:Option(str, "Cog Name", required=True, choices=cogs)):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.respond(embed=embed)

    @slash_command()
    async def donations(self,ctx):
        em = discord.Embed(title = 'Donation', description = 'Donate to the bot to help keep it running by covering my monthly costs. Anything extra that gets donated will be saved for future projects and to help fund uni. It may not be much to you by anything means a lot to me. Thank you for your kindness', color = 0x8BE002)
        em.add_field(name="Buy me a coffee", value="[Click here](https://www.buymeacoffee.com/Michaelrbparker)")
        em.add_field(name="Monaro", value="43rsynRD1qtCA1po9myFsc7ti5havFcXUZPdSZuMexU4DnEyno55TE16eWqFkMLMbwZ7DuRW4ow5kcWzQQYu96NH7XMk6cE")
        em.add_field(name="BTC",value="bc1qlp29r6llr8g6afpnwpdcdwlkawk7svzyw24emf")
        
        
        await ctx.respond(embed = em)
 
    @slash_command(name="emojify", description="Converts text to emojis")
    async def emojify(self, ctx, *, text: str):
        """
        Turns text into emojis
        """
        text = text.lower()
        emojis = []
        for char in text:
            if char.isdecimal():
                num_to_emoji = {
                    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
                    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"
                }
                emojis.append(f":{num_to_emoji.get(char)}:")

            elif char.isalpha():
                emojis.append(f":regional_indicator_{char}:")
    
            elif char in "?!#+-":
                special_char_to_emoji = {
                    "?": "question", "!": "exclamation", "#": "hash",
                    "+": "heavy_plus_sign", "-": "heavy_minus_sign"
                }
                emojis.append(f":{special_char_to_emoji.get(char)}:")
            
            else:
                emojis.append(char)

        await ctx.respond("".join(emojis))

    @slash_command(name="qrcode", description = "Generate a QR code")
    async def qrcode_slash(self, ctx, *, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(url))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",
                            back_color="white").convert('RGB')
        img.save('qrcode.png')
        await ctx.respond(file=discord.File('qrcode.png'))

    @slash_command(name="avatar")
    async def avatar(self, ctx, *, member):
        
        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar.url)

        await ctx.respond(embed=message)

    @slash_command(name="calc", description = "Calculate something")
    async def _calc_slash(self, ctx, *, equation):
        calc = simpcalc.Calculate()
        ans = await calc.calculate(equation)
        await ctx.send(f"The equation is: {equation}\nThe answer is: {ans}")


    @commands.slash_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def zprol(self, ctx):
        modal = CodeInput(title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.code is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://zprol.epicpix.ga/api/v1/run",
                json={"code": modal.code},
            ) as resp:
                response = await resp.json()
            if resp.status != 200:
                em = discord.Embed(
                    title="zProl",
                    description="Something went wrong!\n(API probably had a skill issue)",
                    color=discord.Color.blue(),
                )
                return await ctx.respond(embed=em)
            
        desc = "```\n"
        if response["compilation"]["stdout"] != "":
            desc += "stdout:\n" + response["compilation"]["stdout"]
        if response["compilation"]["stderr"] != "":
            desc += "\n\nstderr:\n" + response["compilation"]["stdout"]

        em = discord.Embed(
            title="Output",
            color=discord.Color.blue(),
            description=desc + "\n```",
        )
        if response["run"] is not None or response["run"] != "":
            em.add_field(name="Run:", value=response["run"])

        await ctx.respond(embed=em)

    @commands.slash_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ricklang(self, ctx):
        modal = CodeInput(title="Code Input")
        await ctx.send_modal(modal)
        await modal.wait()

        if modal.code is None:
            return await ctx.respond("Invalid Input", ephemeral=True)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.fusionsid.xyz/api/runcode",
                json={"code": modal.code, "language": "rickroll_lang"},
            ) as resp:
                response = await resp.json()
            if resp.status != 200:
                em = discord.Embed(
                    title="Rickroll-Lang",
                    description="Something went wrong!\n(API probably had a skill issue)",
                    color=discord.Color.blue(),
                )
                await ctx.respond(embed=em)

        em = discord.Embed(
            title="Output",
            color=discord.Color.blue(),
            description=f"""```\n{response['stdout']}\n```""",
        )

        await ctx.respond(embed=em)

def setup(client):
    client.add_cog(Slash(client))
