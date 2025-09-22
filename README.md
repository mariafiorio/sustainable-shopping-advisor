# 🌱 Sustainable Shopping Advisor
### AI-Powered External Brain for E-commerce Sustainability | GKE Turns 10 Hackathon 2025

<div align="center">

![GKE](https://img.shields.io/badge/Google_Kubernetes_Engine-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_AI-Gemini_1.5_Flash-34A853?style=for-the-badge&logo=google&logoColor=white)
![ADK](https://img.shields.io/badge/Agent_Development_Kit-ADK-FF6B6B?style=for-the-badge)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-MCP-4ECDC4?style=for-the-badge)
![A2A](https://img.shields.io/badge/Agent_to_Agent-A2A-45B7D1?style=for-the-badge)

**Transform Online Boutique with intelligent sustainability insights using Agentic AI - Zero Code Changes Required**

[🚀 Live Demo](http://35.225.28.200) • [🛍️ Enhanced Boutique](http://34.69.27.233) 

</div>

---

## 🎯 **GKE Turns 10 Hackathon Challenge**

**The Challenge:** Give Microservices an AI Upgrade

**Our Solution:** Built an intelligent "external brain" that supercharges the existing Online Boutique application with sustainability insights, without touching a single line of the original microservice code.

**The Innovation:** Agentic AI architecture using containerized components that interact with existing APIs, creating a smart layer of intelligence that transforms user shopping experience through real-time sustainability analysis.

## 🏗️ **Architecture: External Brain Approach**

```mermaid
graph TB
    subgraph "🌐 Online Boutique (UNTOUCHED)"
        OB[Online Boutique App]
        PC[ProductCatalog Service]
        CS[Cart Service]
        CU[Currency Service]
        FE[Frontend Service]
    end
    
    subgraph "� External AI Brain (NEW CONTAINERIZED COMPONENTS)"
        ADK[Agent Development Kit Framework]
        SA[SustainableAdvisor Agent]
        RA[RecommenderAgent]
        MCP[MCP Server]
        GEMINI[Google AI - Gemini 1.5]
        WIDGET[Universal Widget Layer]
    end
    
    subgraph "🖥️ User Interface Enhancement"
        BOOK[Bookmarklet]
        DEMO[Widget Demo]
    end
    
    BOOK --> WIDGET
    DEMO --> WIDGET
    WIDGET --> SA
    SA <--> RA
    SA --> MCP
    MCP --> PC
    MCP --> CS
    MCP --> CU
    SA --> GEMINI
    
    style ADK fill:#ff6b6b
    style SA fill:#4ecdc4
    style RA fill:#45b7d1
    style GEMINI fill:#34a853
    style OB fill:#f9f9f9,stroke:#999,stroke-dasharray: 5 5
```

### 📊 **Zero-Touch Integration Philosophy**

```
┌─────────────────────────────────────────────────────────────────┐
│                   🌐 User Experience Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  📱 Bookmarklet  │  🎨 Widget Demo  │  🛍️ Online Boutique    │
└─────────────┬───────────────┬───────────────┬───────────────────┘
              │               │               │
              ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────┐
│                � EXTERNAL AI BRAIN (NEW)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    A2A     ┌─────────────────┐             │
│  │ SustainableAdvisor  ◄────────► RecommenderAgent │             │
│  │     Agent          │         │                 │             │
│  │                    │         │  • Promotions   │             │
│  │ • AI Analysis      │         │  • Rankings     │             │
│  │ • Sustainability   │         │  • Preferences  │             │
│  │ • Gemini 1.5       │         │                 │             │
│  └─────────┬───────────┘         └─────────────────┘             │
│            │                                                     │
│            ▼                                                     │
│  ┌─────────────────┐                                             │
│  │  MCP Server     │                                             │
│  │  • API Bridge   │                                             │
│  │  • Data Access  │                                             │
│  │  • Zero Touch   │                                             │
│  └─────────┬───────┘                                             │
└────────────┼─────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│          🏪 Online Boutique (COMPLETELY UNTOUCHED)              │
├─────────────────────────────────────────────────────────────────┤
│  ProductCatalog │ CartService │ CurrencyService │ Frontend       │
└─────────────────────────────────────────────────────────────────┘

💡 Key Insight: Smart containerized components read existing APIs 
   through MCP protocol - no code modifications needed!
```

## 🚀 **Live Deployment & Demo**

| Component | URL | Purpose |
|---------|-----|---------|
| 🎨 **Widget Demo** | http://35.225.28.200 | Interactive sustainability interface & bookmarklet |
| 🛍️ **Online Boutique** | http://34.69.27.233 | Original e-commerce app (completely untouched) |
| 🧠 **SustainableAdvisor API** | http://34.173.133.122 | AI sustainability analysis brain |
| 🎯 **RecommenderAgent API** | http://34.44.25.111 | Intelligent product ranking agent |

## ⭐ **Hackathon Requirements Fulfilled**

### ✅ **Required Technologies**
- **☸️ Google Kubernetes Engine (GKE)**: All containerized components deployed on GKE
- **🤖 Google AI Models**: Gemini 1.5 Flash for natural language sustainability explanations

### ✅ **Optional Technologies Implemented**
- **🔧 Agent Development Kit (ADK)**: Custom framework for building modular AI agents
- **🔗 Model Context Protocol (MCP)**: Server deployed on GKE for API communication  
- **🤝 Agent2Agent (A2A)**: Direct inter-agent communication between SustainableAdvisor and RecommenderAgent

### 🎯 **The "External Brain" Approach**
- **Zero Code Changes**: Original Online Boutique runs completely unmodified
- **Containerized Intelligence**: New smart components deployed alongside existing services
- **API Integration**: MCP server reads existing microservice APIs without touching core code

## 🛠️ **Technology Stack & Implementation**

### **Required Technologies (Hackathon Compliance)**
- **☸️ Google Kubernetes Engine (GKE)**: Container orchestration and deployment platform
- **🤖 Google AI Models**: Gemini 1.5 Flash for intelligent sustainability analysis

### **Optional Technologies Successfully Implemented**
- **🔧 Agent Development Kit (ADK)**: Custom framework for modular agentic AI development
- **🔗 Model Context Protocol (MCP)**: Server-based API communication with existing microservices  
- **🤝 Agent2Agent (A2A)**: Direct inter-agent communication protocol for complex workflows

### **Core Implementation Stack**
```bash
Containerization: Docker + Kubernetes on GKE
Backend:          Python 3.11, Flask, Google AI SDK
AI/ML:            Gemini 1.5 Flash, Custom sustainability scoring
Frontend:         Vanilla JavaScript, HTML5, CSS3
API Integration:  MCP Server, RESTful services
Deployment:       Kubernetes manifests, ConfigMaps, Services
```

## 🚀 **Quick Start: Zero-Touch AI Enhancement**

### **1. Prerequisites**
```bash
# Ensure you have access to:
- Google Kubernetes Engine cluster
- Google AI API key for Gemini 1.5 Flash
- kubectl configured for your cluster
```

### **2. Deploy the External AI Brain**
```bash
# Clone the external brain components
git clone https://github.com/mariafiorio/sustainable-shopping-advisor.git
cd sustainable-shopping-advisor

# Set your Google AI API key
export GOOGLE_API_KEY="your-google-ai-key-here"

# Deploy AI components alongside existing Online Boutique
./scripts/deploy.sh
```

### **3. Experience the Enhancement**
1. **Visit Widget Demo**: http://35.225.28.200
2. **Get Bookmarklet**: Drag the bookmarklet to your browser favorites
3. **Test on Original Boutique**: http://34.69.27.233 (untouched codebase)
4. **Try on**: Click bookmarklet on the Online Boutique

### **4. Verify Zero-Touch Integration**
- Original Online Boutique runs exactly as before
- New AI capabilities accessed through external widget
- No modifications to existing microservice code
- Smart insights delivered through MCP API bridge

## 🎯 **Agent Development Kit (ADK) Framework**

Our custom ADK implementation provides a **modular, scalable foundation** for agentic AI development:

### **🏗️ Core Components**

#### **BaseAgent Class**
```python
class BaseAgent:
    """Foundation for all AI agents with standardized capabilities"""
    - Capability management system
    - Tool integration framework  
    - Health monitoring
    - Error handling & fallbacks
```

#### **Agent Capabilities**
```python
# Each agent has specialized capabilities:
SustainableAdvisor:
  ├── analyze_sustainability    # Product environmental analysis
  ├── calculate_score          # ML-based scoring (0-100)
  ├── get_recommendations      # Top sustainable choices
  └── explain_impact           # AI-generated explanations

RecommenderAgent:
  ├── rank_products           # Multi-factor intelligent ranking
  ├── apply_promotions        # Dynamic discount application
  ├── multi_factor_score      # Weighted scoring algorithm
  └── generate_alternatives   # Similar product suggestions
```

#### **Model-Agnostic Design**
```python
# Easy to swap AI providers:
ModelProvider:
  ├── GeminiProvider          # Google AI integration
  ├── FallbackProvider        # Demo mode for development
  └── [Future: OpenAI, Claude, etc.]
```

### **🔄 Agent-to-Agent (A2A) Communication**
```python
# Orchestrated workflow:
user_request → SustainableAdvisor → RecommenderAgent → final_recommendations

# Each agent processes and enriches data:
1. SustainableAdvisor: Analyzes sustainability (AI + ML)
2. RecommenderAgent: Applies ranking + promotions  
3. Result: Top 3 sustainable products with explanations + discounts
```

## 🌍 **Environmental Impact**

### **Measurable Benefits**
- **🌱 Carbon Footprint Reduction**: Promotes products with 40-60% lower emissions
- **♻️ Waste Reduction**: Highlights recyclable and biodegradable alternatives  
- **🌿 Sustainable Materials**: Identifies organic, renewable, and responsibly sourced products
- **📊 Consumer Education**: AI explanations increase environmental awareness

### **Sustainability Scoring Algorithm**
```python
Factors Considered:
├── Material Composition (40%)     # Organic, recycled, renewable materials
├── Production Process (25%)       # Energy efficiency, waste reduction
├── Transportation (20%)           # Local vs. global supply chains  
├── End-of-Life Impact (15%)       # Recyclability, biodegradability
```

## 🔧 **API Documentation**

### **SustainableAdvisor Agent**
```bash
GET /recommendations
# Returns: Top sustainable products with AI analysis

POST /analyze
# Body: {"products": [...]}
# Returns: Detailed sustainability assessment

GET /health
# Returns: Agent status and capabilities
```

### **RecommenderAgent**
```bash
POST /rank
# Body: {"products": [...], "factors": [...]}
# Returns: Ranked products with multi-factor scoring

POST /promotions
# Body: {"products": [...]}
# Returns: Products with applied sustainable discounts
```

## 🧪 **Testing & Quality**

### **Automated Test Suite**
```bash
# Run complete ADK framework tests
cd src/adk
python test_adk.py

# Expected output:
# 🎯 ADK Framework Test Suite
# ✅ Testing imports...                 PASS
# ✅ Testing agent initialization...    PASS  
# ✅ Testing functionality...           PASS
# ✅ Testing health checks...           PASS
# 🎉 Test Results: 4/4 passed
```

### **Integration Testing**
```bash
# Test full system integration
python main.py

# Validates:
# - Google AI connectivity
# - MCP client integration
# - Agent-to-Agent communication
# - API response accuracy
```

## 🏆 **GKE Turns 10 Hackathon Submission**

### **📋 Project Summary**
**Sustainable Shopping Advisor** transforms the existing Online Boutique microservices application with intelligent sustainability insights through an "external brain" approach. Built entirely as containerized components that enhance the original app without touching its codebase.

**Key Innovation**: Zero-code enhancement using agentic AI architecture where smart agents communicate via A2A protocol and access existing APIs through MCP server integration.

### **✅ Requirements Fulfilled**

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| **Enhance Existing Microservice** | Online Boutique + External AI Brain | ✅ Complete |
| **Zero Code Changes** | Original app completely untouched | ✅ Complete |
| **GKE Deployment** | All containers deployed on GKE cluster | ✅ Complete |
| **Google AI Integration** | Gemini 1.5 Flash with real API calls | ✅ Complete |
| **Agent Development Kit** | Custom ADK framework implemented | ✅ Complete |
| **Model Context Protocol** | MCP server for API communication | ✅ Complete |
| **Agent2Agent Protocol** | A2A communication between agents | ✅ Complete |

### **🎯 Technologies Leveraged**
- **Required**: ☸️ GKE + 🤖 Google AI (Gemini 1.5 Flash)
- **Optional**: 🔧 ADK + 🔗 MCP + 🤝 A2A protocols

### **� Data Sources & Findings**
- **Product Data**: Real-time access via Online Boutique ProductCatalog API
- **Sustainability Metrics**: Custom ML scoring algorithm (material, production, transport impact)
- **AI Insights**: Gemini-generated explanations for environmental benefits
- **Learning**: MCP protocol enables seamless integration without code modifications

### **📊 Architecture Innovation**
Built as containerized "external brain" that reads existing APIs, processes with AI agents, and delivers insights through universal widget - proving microservices can gain intelligence without architectural changes.

## 🎮 **For Judges: Live Testing Guide**

### **🔗 Hosted Project URLs**
- **Main Demo**: http://35.225.28.200 (Widget interface + bookmarklet)
- **Original App**: http://34.69.27.233 (Untouched Online Boutique)
- **API Endpoints**: 
  - SustainableAdvisor: http://34.173.133.122/health
  - RecommenderAgent: http://34.44.25.111/health

### **⚡ Quick Test Scenarios**
1. **Zero-Touch Verification**: Compare original boutique vs enhanced experience
2. **Widget**: Test bookmarklet 
3. **Agent Communication**: Observe A2A protocol in action through API responses
4. **Real-time AI**: See Gemini-powered sustainability explanations

### **🧪 Technical Validation**
```bash
# Test MCP server integration
curl http://34.173.133.122/recommendations

# Verify A2A communication
curl http://34.44.25.111/rank -X POST -H "Content-Type: application/json" -d '{"products":[]}'

# Check containerized deployment
kubectl get pods -l app=sustainable-advisor
```

## 🤝 **Contributing**

### **Development Setup**
```bash
# 1. Clone and setup
git clone https://github.com/mariafiorio/sustainable-shopping-advisor.git
cd sustainable-shopping-advisor

# 2. Install dependencies
pip install -r src/sustainable-advisor/requirements.txt

# 3. Configure environment
cp src/sustainable-advisor/.env.example src/sustainable-advisor/.env
# Edit .env with your Google AI API key

# 4. Run tests
python src/adk/test_adk.py

# 5. Start development server
python main.py
```

### **Adding New Agents**
```python
# Create new agent following ADK patterns:
class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyNewAgent")
        self.add_capability('my_capability', self._my_handler)
        self.add_tool('my_tool', self._my_tool_function)
    
    def _my_handler(self, parameters):
        # Implement your agent logic
        return {'result': 'success'}
```
## 📞 **Hackathon Submission Details**

- **👩‍💻 Developer**: Maria Fiorio
- **� Event**: GKE Turns 10 Hackathon 2025
- **�🌐 Live Demo**: http://35.225.28.200
- **📊 API Health**: http://34.173.133.122/health
- **📧 GitHub**: [github.com/mariafiorio](https://github.com/mariafiorio)
- **🏗️ Repository**: [sustainable-shopping-advisor](https://github.com/mariafiorio/sustainable-shopping-advisor)

---

<div align="center">

![Built for GKE 10th Anniversary](https://img.shields.io/badge/Built_for-GKE_Turns_10_Hackathon-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Zero Code Changes](https://img.shields.io/badge/Zero_Code_Changes-External_Brain_Approach-FF6B6B?style=for-the-badge)
![Agentic AI](https://img.shields.io/badge/Agentic_AI-ADK_MCP_A2A-4ECDC4?style=for-the-badge)

</div>
