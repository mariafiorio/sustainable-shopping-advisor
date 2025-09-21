# Agentic AI Architecture Diagram

## System Overview

```mermaid
graph TB
    subgraph "Google Kubernetes Engine (GKE)"
        subgraph "Online Boutique Microservices"
            OB[Online Boutique<br/>Frontend]
            PS[Product Catalog<br/>Service]
            CS[Cart Service]
            RS[Recommendation<br/>Service]
        end
    end
    
    subgraph "Agentic AI System"
        subgraph "Sustainable Advisor Agent"
            SA[Sustainable Advisor<br/>Port 5002]
            MCP[MCP Client<br/>Model Context Protocol]
            WI[Widget Interface<br/>Static Server]
        end
        
        subgraph "Recommender Agent"
            RA[Recommender Agent<br/>Port 5001]
            A2A[A2A Server<br/>Agent-to-Agent]
            ML[ML Ranking<br/>Algorithm]
        end
    end
    
    subgraph "Client Layer"
        BM[Bookmarklet<br/>JavaScript Widget]
        WEB[Widget Demo<br/>Interface]
        USER[End User<br/>Browser]
    end
    
    subgraph "Future Integrations"
        GEMINI[Google Gemini<br/>AI Platform]
        ADK[Agent Development<br/>Kit]
        VTX[Vertex AI<br/>ML Platform]
    end
    
    %% Primary Data Flow
    USER --> WEB
    USER --> BM
    BM --> SA
    WEB --> SA
    SA --> MCP
    MCP --> OB
    MCP --> PS
    
    %% Agent Communication
    SA --> A2A
    A2A --> RA
    RA --> ML
    ML --> A2A
    A2A --> SA
    
    %% Future Connections
    SA -.-> GEMINI
    RA -.-> ADK
    ML -.-> VTX
    
    %% Styling
    classDef agentBox fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef k8sBox fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef clientBox fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef futureBox fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5
    
    class SA,MCP,WI,RA,A2A,ML agentBox
    class OB,PS,CS,RS k8sBox
    class BM,WEB,USER clientBox
    class GEMINI,ADK,VTX futureBox
```

## Communication Protocols

### Model Context Protocol (MCP)
```mermaid
sequenceDiagram
    participant SA as Sustainable Advisor
    participant MCP as MCP Client
    participant OB as Online Boutique
    
    SA->>MCP: Get Product Data
    MCP->>OB: HTTP Request (Port 8081)
    OB-->>MCP: Product Information
    MCP-->>SA: Structured Data
    SA->>SA: Sustainability Analysis
```

### Agent-to-Agent (A2A)
```mermaid
sequenceDiagram
    participant SA as Sustainable Advisor
    participant A2A as A2A Protocol
    participant RA as Recommender Agent
    participant ML as ML Engine
    
    SA->>A2A: Recommendation Request
    A2A->>RA: Forward Request
    RA->>ML: Process Ranking
    ML-->>RA: Scored Results
    RA-->>A2A: Recommendations
    A2A-->>SA: Final Response
```

## Technology Stack

### Core Components
- **Google Kubernetes Engine**: Container orchestration
- **Flask APIs**: Microservice architecture
- **Python 3.9+**: Backend development
- **JavaScript ES6+**: Frontend interactions
- **Docker**: Containerization

### AI/ML Technologies
- **Agentic AI**: Multi-agent coordination
- **Model Context Protocol**: Structured communication
- **Agent-to-Agent**: Direct agent communication
- **Machine Learning**: Ranking algorithms

### Future Integrations
- **Google Gemini**: Advanced AI capabilities
- **Vertex AI**: ML model training
- **Cloud Functions**: Serverless processing
- **BigQuery**: Analytics and insights

## Deployment Architecture

```mermaid
graph LR
    subgraph "Development"
        DEV[Local Development<br/>localhost:5001-5002]
    end
    
    subgraph "Google Cloud Platform"
        subgraph "GKE Cluster"
            K8S[Kubernetes<br/>Deployment]
            LB[Load Balancer<br/>External IP]
        end
        
        subgraph "Cloud Services"
            CB[Cloud Build<br/>CI/CD]
            AR[Artifact Registry<br/>Container Images]
            GCP[GCP APIs<br/>Integration]
        end
    end
    
    subgraph "Client Access"
        PUB[Public URL<br/>External Access]
        BMK[Bookmarklet<br/>Any Website]
    end
    
    DEV --> CB
    CB --> AR
    AR --> K8S
    K8S --> LB
    LB --> PUB
    PUB --> BMK
    
    classDef devBox fill:#e3f2fd,stroke:#0277bd,stroke-width:2px
    classDef cloudBox fill:#f1f8e9,stroke:#388e3c,stroke-width:2px
    classDef clientBox fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class DEV devBox
    class K8S,LB,CB,AR,GCP cloudBox
    class PUB,BMK clientBox
```

## Data Flow

1. **User Interaction**: User visits e-commerce site and activates bookmarklet
2. **Widget Injection**: JavaScript widget injects into the current page
3. **MCP Communication**: Sustainable Advisor requests product data via MCP
4. **A2A Processing**: Recommendation request sent to Recommender Agent
5. **ML Analysis**: Multi-factor ranking with sustainability scoring
6. **Response Delivery**: Recommendations displayed in elegant widget interface

This architecture demonstrates true agentic AI with autonomous agents, structured communication protocols, and scalable cloud deployment.