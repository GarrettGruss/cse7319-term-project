from typing import List, Optional, Dict, Any
from ..service.reddit_service import RedditService
from ..service.llm_service import LLMService
from ..model.models import RedditSubmission, RedditComment, PostSummary, LLMResponse


class PostController:
    """Controller for handling post retrieval and LLM generation workflow"""

    def __init__(self):
        """Initialize the controller with required services"""
        self.reddit_service = RedditService()
        self.llm_service = LLMService()

    def get_random_post_with_llm_response(
        self,
        subreddits: Optional[List[str]] = None,
        limit: int = 10,
        min_comments: int = 10,
        top_n_comments: int = 10,
        custom_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Get a random Reddit post and generate LLM response

        Args:
            subreddits: List of subreddits to search (uses default if None)
            limit: Maximum submissions to fetch per subreddit
            min_comments: Minimum comments required
            top_n_comments: Number of top comments to include
            custom_prompt: Custom prompt for LLM (uses default LinkedIn prompt if None)
            model: LLM model to use
            temperature: Temperature for generation

        Returns:
            Dict containing submission, comments, post_summary, and llm_response

        Raises:
            Exception: If no suitable posts found or LLM generation fails
        """
        # Default subreddits if none provided
        if subreddits is None:
            subreddits = [
                'mcp', 'vibecoding', 'buildinpublic', 'aws',
                'LlamaFarm', 'AgentsOfAI', 'ClaudeAI', 'Buildathon'
            ]

        try:
            # Step 1: Get random submission
            submission = self.reddit_service.select_random_submission(
                subreddits=subreddits,
                limit=limit,
                min_comments=min_comments
            )

            # Step 2: Get submission with all comments
            submission_data, comments = self.reddit_service.get_submission_with_comments(
                submission_id=submission.id
            )

            # Step 3: Generate structured post summary
            post_summary = self.reddit_service.generate_post_summary(
                submission=submission_data,
                comments=comments,
                top_n_comments=top_n_comments
            )

            # Step 4: Generate LLM response
            llm_response = self.llm_service.generate_linkedin_post(
                post_summary=post_summary,
                custom_prompt=custom_prompt,
                model=model,
                temperature=temperature
            )

            # Return complete result
            return {
                "submission": submission_data,
                "comments": comments,
                "post_summary": post_summary,
                "llm_response": llm_response,
                "metadata": {
                    "total_comments": len(comments),
                    "top_comments_used": min(top_n_comments, len(comments)),
                    "subreddit_searched": submission_data.subreddit,
                    "generation_timestamp": llm_response.timestamp
                }
            }

        except Exception as e:
            raise Exception(f"Failed to generate post with LLM response: {e}")

    def get_multiple_posts_with_responses(
        self,
        count: int,
        subreddits: Optional[List[str]] = None,
        limit: int = 10,
        min_comments: int = 10,
        top_n_comments: int = 10,
        custom_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple posts with LLM responses

        Args:
            count: Number of posts to generate
            subreddits: List of subreddits to search
            limit: Maximum submissions to fetch per subreddit
            min_comments: Minimum comments required
            top_n_comments: Number of top comments to include
            custom_prompt: Custom prompt for LLM
            model: LLM model to use
            temperature: Temperature for generation

        Returns:
            List of dictionaries containing post data and LLM responses
        """
        results = []
        for i in range(count):
            try:
                result = self.get_random_post_with_llm_response(
                    subreddits=subreddits,
                    limit=limit,
                    min_comments=min_comments,
                    top_n_comments=top_n_comments,
                    custom_prompt=custom_prompt,
                    model=model,
                    temperature=temperature
                )
                results.append(result)
            except Exception as e:
                print(f"Error generating post {i+1}: {e}")
                continue

        return results