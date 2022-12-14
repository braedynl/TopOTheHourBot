from typing import Optional

from twitchio import Message
from twitchio.ext.commands import Bot, Context, command

from .rating_aggregator import RatingAggregator

__all__ = ["TopOTheHourBot"]


class TopOTheHourBot(Bot):

    MODERATORS: set[str] = {"braedye", "bytesized_", "emjaye"}

    __slots__ = ()

    def __init__(
        self,
        token: str,
        *,
        prefix: str = '$',
        client_secret: Optional[str] = None,
        initial_channels: Optional[tuple[str, ...]] = None,
        heartbeat: Optional[float] = 30,
        retain_cache: Optional[bool] = True,
        **kwargs,
    ) -> None:
        super().__init__(
            token,
            prefix=prefix,
            client_secret=client_secret,
            initial_channels=initial_channels,
            heartbeat=heartbeat,
            retain_cache=retain_cache,
            **kwargs,
        )
        self.add_cog(RatingAggregator(self))

    @command()
    async def ping(self, ctx: Context) -> None:
        """Respond with pong"""
        await ctx.send(f"{ctx.author.mention} pong")

    @command()
    async def copy(self, ctx: Context, *words: str) -> None:
        """Write a message as the bot, signifying that the message came from
        the command's user
        """
        await ctx.send(f"{ctx.author.mention} (copy): {' '.join(words)}")

    @command()
    async def code(self, ctx: Context, *names: str) -> None:
        """Bulk-mention users to tell them where they can find the bot's source
        code
        """
        names = map(lambda name: name if name.startswith('@') else f"@{name}", names)
        await ctx.send(f"{' '.join(names)} the bot's source code can be found on its Twitch profile Okayge")

    async def event_command_error(self, ctx: Context, error: Exception) -> None:
        """Send the error message of a command to its user"""
        await ctx.send(f"{ctx.author.mention} {error}")

    async def event_message(self, message: Message) -> None:
        """Handle commands if the message came from a bot moderator"""
        if message.echo:
            return
        if message.author.name in self.MODERATORS:
            await self.handle_commands(message)
