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