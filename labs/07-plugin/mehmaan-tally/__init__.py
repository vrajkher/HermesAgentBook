"""mehmaan-tally plugin — registration. Hermes આ register(ctx) ને startup વખતે એક વાર બોલાવે છે."""
import logging

from . import schemas, tools

logger = logging.getLogger(__name__)
_calls = {"mehmaan_tally": 0}


def _on_post_tool_call(tool_name, args, result, task_id, **kwargs):
    """Hook: દરેક tool call પછી ચાલે (ફક્ત આપણા tool માટે નહીં). Observer: કંઈ બદલતો નથી."""
    if tool_name in _calls:
        _calls[tool_name] += 1
        logger.debug("mehmaan_tally used %d time(s)", _calls[tool_name])


def register(ctx):
    ctx.register_tool(name="mehmaan_tally", toolset="mehmaan", schema=schemas.MEHMAAN_TALLY,
                      handler=tools.mehmaan_tally, emoji="🧮")
    ctx.register_hook("post_tool_call", _on_post_tool_call)
