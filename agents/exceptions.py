class AgentError(Exception):
    """Base exception for the AI agent."""


class LLMError(AgentError):
    """Raised when an LLM request fails."""


class CodeExecutionError(AgentError):
    """Raised when generated code fails to execute."""


class StateValidationError(AgentError):
    """Raised when agent state is invalid."""