class VoiceIQError(Exception):
    pass

class AgentError(VoiceIQError):
    pass

class ToolError(VoiceIQError):
    pass

class OrderNotFoundError(ToolError):
    pass

class BedrockError(VoiceIQError):
    pass

