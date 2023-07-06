from kuumuu_bot import *
from main_bot.support import *

# ---------- Auto Mod Error ----------

async def auto_mod_error(ctx : discord.Interaction , error):
    # print(error)
    if isinstance(error, MissingPermissions):
        kuumo = "dao"
        kuumoid = emoji[kuumo]
        await ctx.response.send_message(f"You can't use that command. Want to get punched? <:{kuumo}:{kuumoid}>")
        
    elif error == "InvalidArgument":
        kuumo = "hutao_le"
        kuumoid = emoji[kuumo]
        await ctx.response.send_message(f'You are wrong in some argument of this command. Please check your command <:{kuumo}:{kuumoid}>')
