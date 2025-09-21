# src/adk/agent_base.py
"""
Agent Development Kit (ADK) - Base Agent Framework
Modular, flexible, model-agnostic framework for agent development
"""

import abc
import logging
import json
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    TIMEOUT = "timeout"

@dataclass
class AgentCapability:
    """Represents an agent capability"""
    name: str
    description: str
    handler: Callable
    input_schema: Dict = field(default_factory=dict)
    output_schema: Dict = field(default_factory=dict)
    requirements: List[str] = field(default_factory=list)

@dataclass
class AgentTool:
    """Represents an agent tool"""
    name: str
    description: str
    function: Callable
    parameters: Dict = field(default_factory=dict)
    model_agnostic: bool = True

@dataclass
class AgentRequest:
    """Standardized agent request"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capability: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AgentResponse:
    """Standardized agent response"""
    request_id: str
    agent_id: str
    status: AgentStatus
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    execution_time_ms: Optional[float] = None

class BaseAgent(abc.ABC):
    """
    ADK Base Agent - Foundation for all agents
    
    Design Principles:
    - Modular: Capabilities and tools are pluggable
    - Flexible: Model-agnostic, deployment-agnostic
    - Software Development: Follows standard dev practices
    - Observable: Built-in logging, metrics, debugging
    """
    
    def __init__(self, agent_id: str, name: str, version: str = "1.0.0"):
        self.agent_id = agent_id
        self.name = name
        self.version = version
        self.status = AgentStatus.IDLE
        self.capabilities: Dict[str, AgentCapability] = {}
        self.tools: Dict[str, AgentTool] = {}
        self.config: Dict[str, Any] = {}
        self.metrics: Dict[str, Any] = {
            "requests_processed": 0,
            "errors": 0,
            "avg_response_time_ms": 0.0
        }
        
        # Initialize agent
        self._setup_logging()
        self._register_capabilities()
        self._register_tools()
        self._initialize()
        
        logger.info(f"ADK Agent initialized: {self.name} v{self.version} [{self.agent_id}]")
    
    def _setup_logging(self):
        """Setup agent-specific logging"""
        self.logger = logging.getLogger(f"adk.{self.agent_id}")
        self.logger.setLevel(logging.INFO)
    
    @abc.abstractmethod
    def _register_capabilities(self):
        """Register agent capabilities - implemented by subclasses"""
        pass
    
    @abc.abstractmethod
    def _register_tools(self):
        """Register agent tools - implemented by subclasses"""
        pass
    
    def _initialize(self):
        """Initialize agent - can be overridden by subclasses"""
        pass
    
    def register_capability(self, capability: AgentCapability):
        """Register a new capability"""
        self.capabilities[capability.name] = capability
        self.logger.info(f"Registered capability: {capability.name}")
    
    def register_tool(self, tool: AgentTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")
    
    def process_request(self, request: AgentRequest) -> AgentResponse:
        """
        Main request processing pipeline
        ADK standardized processing flow
        """
        start_time = datetime.now()
        self.status = AgentStatus.PROCESSING
        
        try:
            # Validate request
            self._validate_request(request)
            
            # Find capability
            if request.capability not in self.capabilities:
                raise ValueError(f"Unknown capability: {request.capability}")
            
            capability = self.capabilities[request.capability]
            
            # Execute capability
            self.logger.info(f"Executing capability: {request.capability}")
            result = capability.handler(request.parameters, request.context)
            
            # Create successful response
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            response = AgentResponse(
                request_id=request.id,
                agent_id=self.agent_id,
                status=AgentStatus.COMPLETED,
                result=result,
                execution_time_ms=execution_time
            )
            
            # Update metrics
            self._update_metrics(execution_time, success=True)
            self.status = AgentStatus.IDLE
            
            return response
            
        except Exception as e:
            # Handle errors
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.error(f"Agent execution error: {str(e)}")
            
            response = AgentResponse(
                request_id=request.id,
                agent_id=self.agent_id,
                status=AgentStatus.ERROR,
                error=str(e),
                execution_time_ms=execution_time
            )
            
            self._update_metrics(execution_time, success=False)
            self.status = AgentStatus.ERROR
            
            return response
    
    def _validate_request(self, request: AgentRequest):
        """Validate incoming request"""
        if not request.capability:
            raise ValueError("Capability is required")
        
        if request.capability not in self.capabilities:
            available = list(self.capabilities.keys())
            raise ValueError(f"Unknown capability '{request.capability}'. Available: {available}")
    
    def _update_metrics(self, execution_time_ms: float, success: bool):
        """Update agent metrics"""
        self.metrics["requests_processed"] += 1
        
        if not success:
            self.metrics["errors"] += 1
        
        # Update average response time
        current_avg = self.metrics["avg_response_time_ms"]
        total_requests = self.metrics["requests_processed"]
        new_avg = ((current_avg * (total_requests - 1)) + execution_time_ms) / total_requests
        self.metrics["avg_response_time_ms"] = round(new_avg, 2)
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information - ADK standard"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "status": self.status.value,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "requirements": cap.requirements
                }
                for cap in self.capabilities.values()
            ],
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "model_agnostic": tool.model_agnostic
                }
                for tool in self.tools.values()
            ],
            "metrics": self.metrics
        }
    
    def health_check(self) -> Dict[str, Any]:
        """ADK standard health check"""
        return {
            "status": "healthy" if self.status != AgentStatus.ERROR else "unhealthy",
            "agent_id": self.agent_id,
            "name": self.name,
            "uptime": "active",
            "capabilities_count": len(self.capabilities),
            "tools_count": len(self.tools),
            "last_request": self.metrics.get("last_request_time", None)
        }

class ModelProvider(abc.ABC):
    """Abstract model provider - enables model-agnostic agents"""
    
    @abc.abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the model"""
        pass
    
    @abc.abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        pass

class GeminiModelProvider(ModelProvider):
    """Gemini model provider for ADK"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Gemini model provider initialized: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Gemini"""
        if not self.model:
            return "Model not available"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            return f"Generation failed: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Gemini model info"""
        return {
            "provider": "google_gemini",
            "model": self.model_name,
            "capabilities": ["text_generation", "analysis"],
            "model_agnostic_compatible": True
        }

class AgentOrchestrator:
    """
    ADK Agent Orchestrator
    Manages multiple agents and their interactions
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, Dict] = {}
        self.logger = logging.getLogger("adk.orchestrator")
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.agent_id] = agent
        self.logger.info(f"Registered agent: {agent.name} [{agent.agent_id}]")
    
    def execute_workflow(self, workflow_name: str, input_data: Dict) -> Dict:
        """Execute a multi-agent workflow"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow = self.workflows[workflow_name]
        results = {}
        
        self.logger.info(f"Executing workflow: {workflow_name}")
        
        for step in workflow.get("steps", []):
            agent_id = step["agent_id"]
            capability = step["capability"]
            
            if agent_id not in self.agents:
                raise ValueError(f"Agent not found: {agent_id}")
            
            agent = self.agents[agent_id]
            
            # Prepare request
            request = AgentRequest(
                capability=capability,
                parameters=step.get("parameters", {}),
                context={"workflow": workflow_name, "previous_results": results}
            )
            
            # Execute
            response = agent.process_request(request)
            results[f"step_{len(results)}"] = response.result
            
            if response.status == AgentStatus.ERROR:
                self.logger.error(f"Workflow step failed: {response.error}")
                break
        
        return {
            "workflow": workflow_name,
            "status": "completed",
            "results": results
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "orchestrator": "active",
            "agents_count": len(self.agents),
            "agents": {
                agent_id: agent.health_check()
                for agent_id, agent in self.agents.items()
            }
        }