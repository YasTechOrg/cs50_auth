import disnake
from disnake.ext import commands
import asyncio
import sqlite3

class MyModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components = [
            disnake.ui.TextInput(
                label="شماره تلفن خود به انگلیسی",
                placeholder = "مثال (09111111111)",
                custom_id="phone",
                style=disnake.TextInputStyle.short,
                max_length=11,
            ),

        ]
        super().__init__(title="CS50 Discord Authentication", custom_id="create_tag", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        number_input = inter.text_values.get("phone")
        
        data = sqlite3_check(number_input)
        #print(data)
        Check = False

        try :
            if "phone_number" in data:
                if data["phone_number"] == number_input :
                    if data["Login"] == None and data["Discord_id_name"] == None and data["Discord_id"] == None:

                        embed=disnake.Embed(color=0x14db4c)
                        embed.title = "اطلاعات شما تایید شد"
                        embed.description = f"""سلام , {data['First']} {data['Last']}
                        اطلاعات شما برسی و تایید شد و تا چند ثانیه دیگر سرور برای شما باز خواهد شد
                        """
                        await inter.response.send_message(embed = embed, ephemeral=True)
                        # add and remove roles
                        Add_Role_id = inter.guild.get_role(997142096836304896)
                        Remove_role_id = inter.guild.get_role(997143448484315247)
                        await asyncio.sleep(3)
                        await inter.author.add_roles(Add_Role_id)
                        await inter.author.remove_roles(Remove_role_id)

                        connect = sqlite3.connect("CS50.db")
                        db = connect.cursor()
                        db.execute(f"UPDATE account_user SET Login = 'YES', Discord_id_name = '{inter.author}', Discord_id = '{inter.author.id}' WHERE phone_number = '{number_input}'")
                        connect.commit()
                        connect.close()
                        Check = True

                    else:
                        Check = True
                        embed=disnake.Embed(color=0xe00909)
                        embed.title = " از شماره مورد نظر شمااستفاده شده در صورت نیاز به پشتیبانی اطلاع دهید"
                        await inter.response.send_message(embed = embed, ephemeral=True)

            if not Check:
                embed=disnake.Embed(color=0xe00909)
                embed.title = "متاسفانه مشخصات شما در لیست موجود نمیباشد لطفا به پشتیبانی اطلاع دهید"
                await inter.response.send_message(embed = embed, ephemeral=True)
        except Exception as e:
            #error Log
            channel = inter.guild.get_channel(997858250106089632)
            await channel.send(e)
    # agar api moshkel bokhore ya az discord javab nayad in execute mishe
    async def on_error(self, error: Exception, inter: disnake.ModalInteraction) -> None:
        await inter.response.send_message("مشکلی پیش امده لطفا بعدا تلاش کنید", ephemeral=True)

class button(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @disnake.ui.button(label="Authenticate", style=disnake.ButtonStyle.success)
    async def authenticate(self, button:disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(MyModal())

class check(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # channel lobby
        channel = self.bot.get_channel(997144260501569599)
        await channel.purge(limit = 10)
        embed=disnake.Embed(color=0x14db4c)
        embed.title = "احراز هویت شرکت کنندگان"
        embed.description = "لطفا برای دسترسی به محتوای سرور روی دکمه زیر کلیک کنید"
        await channel.send(embed = embed, view=button())

def sqlite3_check(number_input):
    connect = sqlite3.connect("CS50.db")
    db = connect.cursor()
    db.execute(f"SELECT * FROM account_user WHERE phone_number = '{number_input}';")
    data = db.fetchall()
    row = {}
    for x in data:
        row = {
            "First":None, "Last":None, "phone_number":None, "Login":None, "Discord_id_name":None, "Discord_id":None,
        }
        row["First"] = x[0]
        row["Last"] = x[1]
        row["phone_number"] = x[2]
        row["Login"] = x[3]
        row["Discord_id_name"] = x[4]
        row["Discord_id"] = x[5]
    connect.close()
    return row
    
def setup(bot:commands.Bot):
    bot.add_cog(check(bot))