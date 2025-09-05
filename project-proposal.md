# CSE 7319 - Software Architecture & Design Project Proposal

**Project Option:** Option 1 - Microservices Architecture

## Project Title
**LinkedIn influencer: Automated Content Curation Platform**

## Project Overview

### 1. Main Functions

- **Automated Content Discovery**: Scrape multiple technology-focused subreddits (r/entrepreneur, r/ChatGPT, r/VibeCoding, r/programming, r/startups) to identify trending posts based on upvotes, comments, and engagement metrics
- **Intelligent Content Curation**: Filter and rank posts based on relevance, engagement potential, and professional appropriateness for LinkedIn audiences
- **AI-Powered Content Transformation**: Convert Reddit discussions and insights into professional LinkedIn post formats with proper tone, hashtags, and call-to-actions

### 2. Expected Results
- Consistent social media presence with 5-7 high-quality posts per week
- Aggregated insights on trending tech topics and successful LinkedIn content patterns
- Demonstrate scalable microservices architecture handling real-time data processing, AI integration, and multi-platform API interactions

### 3. Technology Stack & Architecture

**Initial Architecture (Monolithic Python Application)**
- **Primary Language**: Python
- **Database**: MongoDB (containerized within Kubernetes environment)
- **UI Framework**: Streamlit
- **Deployment**: Kubernetes cluster

**Core Services**
1. **Scraper Service**: Extracts top posts and engagement metrics from target subreddits, stores structured data in MongoDB
2. **Content Generation Service**: Retrieves post data from MongoDB, performs LLM API calls to transform content into LinkedIn-appropriate formats, stores generated content with source attribution
3. **UI Service**: Streamlit web application providing content review, editing, and publishing interface

**Future Extensibility**
- **LaTeX Compiler Service**: Generate PDF poster variants of curated content
- **Analytics Service**: Track post performance and engagement metrics
- **Scheduling Service**: Automated posting and content calendar management
- **Email Service**: Newsletter distribution and notifications using Redis-backed message queues for asynchronous processing

### 4. Project Timeline

**Project Duration**: September 5, 2025 - October 3, 2025 (4 weeks)

**Week 1 (Sept 5-11): Business Logic Discovery**
- Manually execute the complete content curation workflow end-to-end
- Document each step: Reddit browsing, post selection criteria, content transformation process
- Record decision-making patterns and quality filters used during manual curation
- Define data requirements and business rules based on manual process observations

**Week 2 (Sept 12-18): Foundation & Core Services**
- Set up Kubernetes environment and MongoDB deployment
- Implement Reddit scraper service based on documented manual process
- Develop content generation service with LLM integration using recorded transformation patterns
- Create MongoDB schemas for posts and generated content

**Week 3 (Sept 19-25): Integration & UI Development**
- Build Streamlit UI incorporating manual workflow insights
- Integrate all services and replicate documented end-to-end process
- Test automated workflow against manual baseline for quality validation

**Week 4 (Sept 26-Oct 3): Optimization & Documentation**
- Performance testing and workflow refinement
- Complete project documentation including manual process findings
- Final testing comparing automated vs manual results
- Project presentation preparation with workflow evolution narrative

## Project Design

### 1. Primary Architecture Style

**Microservices Architecture** is the primary architectural approach for this project. This choice is driven by:

- **Service Independence**: Each service (scraper, content generation, UI) can be developed, deployed, and scaled independently
- **Technology Flexibility**: Future services (LaTeX compiler, email service) can use different technologies while maintaining loose coupling
- **Scalability**: Individual services can scale based on demand (e.g., scaling content generation during peak usage)
- **Fault Isolation**: Failure in one service doesn't cascade to others
- **Development Agility**: Supports the iterative approach of starting with manual processes and gradually automating

### 2. Architecture Diagrams

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        subgraph "Core Services"
            RS[Reddit Scraper Service]
            CG[Content Generation Service]
            UI[Streamlit UI Service]
        end
        
        subgraph "Data Layer"
            DB[(MongoDB)]
        end
    end
    
    subgraph "External APIs"
        Reddit[Reddit API]
        LLM[LLM API OpenAI/Anthropic]
    end
    
    RS --> |Extract posts & metrics| DB
    DB --> |Retrieve post data| CG
    CG --> |Store generated content| DB
    DB --> |Display content| UI
    
    RS --> Reddit
    CG --> LLM
```

### 3. Prototype Screens


**Content Review & Edit Screen**
```
┌─────────────────────────────────────────────────────────┐
│ Post Editor                               [Back] [Save] │
├─────────────────────────────────────────────────────────┤
│ Original Reddit Post Preview:                          │
│ r/entrepreneur • 1.2k upvotes • 89 comments            │
│ "Just raised our Series A - here's what I learned..."   │
├─────────────────────────────────────────────────────────┤
│ Generated LinkedIn Post:                                │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 🚀 Key lessons from a successful Series A raise:   │ │
│ │                                                     │ │
│ │ • Timing is everything - market conditions matter  │ │
│ │ • Your team story sells as much as your product    │ │
│ │ • Due diligence prep can make or break the deal    │ │
│ │                                                     │ │
│ │ What's been your experience with fundraising?      │ │
│ │                                                     │ │
│ │ #Startups #Fundraising #Entrepreneurship           │ │
│ └─────────────────────────────────────────────────────┘ │
│ [🤖 Regenerate] [📅 Schedule for 2:00 PM] [📤 Post Now] │
└─────────────────────────────────────────────────────────┘
```

## Project Implementation Plan

### Platform & Tools
- **Primary Language**: Python 3.11+
- **Web Framework**: Streamlit (UI)
- **Database**: MongoDB with PyMongo driver
- **Container Platform**: Docker
- **Orchestration**: Kubernetes
- **APIs**: 
  - Reddit API (PRAW library)
  - OpenAI/Anthropic API for content generation
  - LinkedIn API for posting
- **Development Tools**: 
  - Poetry for dependency management
  - pytest for testing
  - Black/Ruff for code formatting
  - GitHub Actions for CI/CD

### Deployment
- **Containerization**: Docker containers for each service
- **Orchestration**: Kubernetes cluster deployment
- **Database**: MongoDB deployed as StatefulSet in Kubernetes
- **Networking**: Service mesh for inter-service communication
- **Monitoring**: Basic logging and health checks

### Team Roles
**Individual Project** - All components will be developed by the project owner