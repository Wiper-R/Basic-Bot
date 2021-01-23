import config
from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance, fields, Document
from discord.ext import commands
import discord


class Member(Document):
    # class Meta:
    #     tablename = 'member'
    id = fields.ObjectIdField(attribute='_id')
    guild_id = fields.IntegerField(required=True)
    member_id = fields.IntegerField(required=True)
    xp = fields.IntegerField(default=0)
    level = fields.IntegerField(default=0)

    @property
    def guild(self):
        return self.bot.get_guild(self.guild_id)

    @property
    def member(self):
        return self.guild.get_member(self.member_id)


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = AsyncIOMotorClient(config.DATABASE_URL)[config.DATABASE_NAME]
        instance = Instance(self.db)
        g = globals()
        for x in (
            'Member',
        ):
            setattr(self, x, instance.register(g[x]))
            getattr(self, x).bot = bot

    async def fetch_member(self, member: discord.Member) -> Member:
        user = await self.Member.find_one({'guild_id': member.guild.id, 'member_id': member.id})

        if not user:
            user = self.Member(
                guild_id=member.guild.id, member_id=member.id)
            await user.commit()

        return user


def setup(bot):
    bot.add_cog(Database(bot))
