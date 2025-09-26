from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class RedditSubmission(BaseModel):
    """Model for Reddit submission data"""
    subreddit: str = Field(..., description="The subreddit name")
    title: str = Field(..., description="The submission title")
    score: int = Field(..., description="The submission score (upvotes - downvotes)")
    id: str = Field(..., description="The Reddit submission ID")
    comments: int = Field(..., description="Number of comments on the submission")
    body: Optional[str] = Field(None, description="The submission body text (selftext)")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RedditComment(BaseModel):
    """Model for Reddit comment data with hierarchical structure"""
    id: str = Field(..., description="The comment ID")
    author: str = Field(..., description="The comment author username")
    body: str = Field(..., description="The comment text content")
    score: int = Field(..., description="The comment score (upvotes - downvotes)")
    children: List[str] = Field(default_factory=list, description="List of child comment IDs")

    def calculate_engagement_score(self, reply_weight: int = 10) -> int:
        """Calculate engagement score: score + (number of replies * weight)"""
        return self.score + (len(self.children) * reply_weight)


class CommentStructure(BaseModel):
    """Model for hierarchical comment structure used in YAML generation"""
    comment: str = Field(..., description="The comment text")
    children: Optional[List['CommentStructure']] = Field(default_factory=list, description="Nested child comments")


class PostSummary(BaseModel):
    """Model for the complete post summary structure"""
    post_title: str = Field(..., description="The Reddit post title")
    post_body: str = Field(..., description="The Reddit post body content")
    children: List[CommentStructure] = Field(default_factory=list, description="Top-level comments with their nested structure")


class LLMRequest(BaseModel):
    """Model for LLM API requests"""
    prompt: str = Field(..., description="The prompt to send to the LLM")
    context: str = Field(..., description="The YAML context containing post and comments")
    model: str = Field(default="gemini-2.5-pro", description="The LLM model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature parameter for generation")


class LLMResponse(BaseModel):
    """Model for LLM API responses"""
    content: str = Field(..., description="The generated content from the LLM")
    model_used: str = Field(..., description="The actual model that generated the response")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the response was generated")


# Enable forward references for recursive models
CommentStructure.model_rebuild()