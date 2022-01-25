from discord.ext import commands
import discord
from dislash import slash_commands
import utils
import json

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _shop(self, ctx):
        if not self.bot.db.users.is_in(id=ctx.author.id):
            return await ctx.send("あなたはゲームを始めていません！storyコマンドでゲームを開始してください！")
        if (udata:=self.bot.db.users.search(id=ctx.author.id)[0][2]) < 3:
            return await utils.RequireFault(ctx)
        if udata == 3:  # チュートリアル
            e = discord.Embed(title="ショップ - チュートリアル", description="お店へようこそ！案内人のマスダです！\nこの街には1個のお店が存在するようですね...\nセーフィ生活店というところに行ってみましょう！")
            menu = utils.EasyMenu("お店を選択", "お店を選択してください", **{"セーフイ生活店":"1"})
            msg = await ctx.send(embed=e, components=[menu])
            inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)
            e = discord.Embed(title="セーフイ生活店 - チュートリアル", description="この店に来るのが初めてなので、まずはただの棒を買ってみましょう！今回だけ特別にタダで渡します！")
            menu = utils.EasyMenu("アイテムを選択", "アイテムを選択してください", **{"ただの棒":"1"})
            await msg.edit(embed=e, components=[menu])
            inter = await msg.wait_for_dropdown(lambda i:i.author == ctx.author)
            if not self.bot.db.item.is_in(id=ctx.author.id):
                data = json.dumps({"1":1})
                self.bot.db.item.add_item(ctx.author.id, data)
            e = discord.Embed(title="セーフイ生活店 - チュートリアル", description="しっかり商品を購入できましたね！おめでとう！\n```diff\n! ミッションクリア !\n```")
            await msg.edit(embed=e, components=[])
            self.bot.db.users.update_item(f"id={ctx.author.id}", story=4)
        else:
            if self.bot.version == "0.2":
                # バージョンロック
                return await ctx.send("現在絶賛開発中...")
            for i in self.bot.itemdata:
                pass


    @slash_commands.command(description="お買い物をします。")
    async def shop(self, inter):
        await self._shop(inter)


    @commands.command(name="shop")
    async def c_shop(self, ctx):
        await self._shop(ctx)


def setup(bot):
    bot.add_cog(Shop(bot))