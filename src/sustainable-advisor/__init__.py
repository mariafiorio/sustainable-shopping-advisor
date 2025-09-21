from pydantic import Field

class SustainableAdvisorAgent(Agent):
    mcp_client: MCPClient = Field(default_factory=lambda: MCPClient())
    a2a_client: A2AClient = Field(default_factory=lambda: A2AClient())

    def __init__(self, **kwargs):
        super().__init__(
            name="SustainableAdvisorAgent",
            model="gemini-2.0-flash",
            description="Agente consultor de sustentabilidade que recomenda produtos ecológicos",
            instruction="Filtre produtos sustentáveis e envie para RecommenderAgent para ranking final.",
            **kwargs
        )
