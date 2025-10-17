import praw
import os
from random import randrange
from typing import List, Optional
from model.models import RedditSubmission, RedditComment, PostSummary, CommentStructure


class RedditService:
    """Service for retrieving Reddit submissions and comments"""

    def __init__(self):
        """Initialize Reddit API client"""
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USERNAME"),
        )

    def select_random_submission(
        self, subreddits: List[str], limit: int = 10, min_comments: int = 10
    ) -> RedditSubmission:
        """
        Select a random submission from specified subreddits with minimum comment threshold

        Args:
            subreddits: List of subreddit names to search
            limit: Maximum number of submissions to fetch per subreddit
            min_comments: Minimum number of comments required

        Returns:
            RedditSubmission: A random submission meeting the criteria

        Raises:
            Exception: If no submissions found matching criteria
        """
        sub = subreddits[randrange(0, len(subreddits))]
        submissions_list = []

        for submission in self.reddit.subreddit(sub).hot(limit=limit):
            if submission.num_comments > min_comments:
                submissions_list.append(
                    RedditSubmission(
                        subreddit=sub,
                        title=submission.title,
                        score=submission.score,
                        id=submission.id,
                        comments=submission.num_comments,
                        body=submission.selftext,
                    )
                )

        if len(submissions_list) > 0:
            return submissions_list[randrange(0, len(submissions_list))]
        else:
            raise Exception(f"No submissions found in {sub} matching filter")

    def extract_comment_recursively(self, comment) -> Optional[RedditComment]:
        """
        Extract comment data including nested replies

        Args:
            comment: PRAW comment object

        Returns:
            RedditComment: Comment data or None if invalid
        """
        if not hasattr(comment, "body"):
            return None

        children_ids = []
        if hasattr(comment, "replies") and comment.replies:
            for reply in comment.replies:
                if hasattr(reply, "body"):
                    children_ids.append(reply.id)

        return RedditComment(
            id=comment.id,
            author=comment.author.name if comment.author else "[deleted]",
            body=comment.body,
            score=comment.score,
            children=children_ids,
        )

    def extract_all_comments_recursively(
        self, comment, all_comments: List[RedditComment]
    ) -> None:
        """
        Recursively extract all comments and their nested replies

        Args:
            comment: PRAW comment object
            all_comments: List to append extracted comments to
        """
        if not hasattr(comment, "body"):
            return

        comment_data = self.extract_comment_recursively(comment)
        if comment_data:
            all_comments.append(comment_data)

        if hasattr(comment, "replies") and comment.replies:
            for reply in comment.replies:
                self.extract_all_comments_recursively(reply, all_comments)

    def get_submission_with_comments(
        self, submission_id: str
    ) -> tuple[RedditSubmission, List[RedditComment]]:
        """
        Get a submission and all its comments

        Args:
            submission_id: Reddit submission ID

        Returns:
            tuple: (RedditSubmission, List of RedditComments)
        """
        submission = self.reddit.submission(id=submission_id)

        # Create submission model
        reddit_submission = RedditSubmission(
            subreddit=submission.subreddit.display_name,
            title=submission.title,
            score=submission.score,
            id=submission.id,
            comments=submission.num_comments,
            body=submission.selftext,
        )

        # Extract all comments
        comments_list = []
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            self.extract_all_comments_recursively(comment, comments_list)

        return reddit_submission, comments_list

    def generate_post_summary(
        self,
        submission: RedditSubmission,
        comments: List[RedditComment],
        top_n_comments: int = 10,
    ) -> PostSummary:
        """
        Generate a structured post summary with top comments

        Args:
            submission: The Reddit submission
            comments: List of all comments
            top_n_comments: Number of top comments to include

        Returns:
            PostSummary: Structured summary for LLM processing
        """
        # Sort comments by score and get top N
        sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)[
            :top_n_comments
        ]

        # Create comment lookup
        comment_lookup = {comment.id: comment for comment in comments}

        def build_comment_structure(comment_data: RedditComment) -> CommentStructure:
            """Build a comment structure with its children"""
            structure = CommentStructure(comment=comment_data.body)

            if comment_data.children:
                children_structures = []
                for child_id in comment_data.children:
                    if child_id in comment_lookup:
                        child_structure = build_comment_structure(
                            comment_lookup[child_id]
                        )
                        children_structures.append(child_structure)
                structure.children = children_structures

            return structure

        # Find top-level comments (not children of others)
        all_child_ids = set()
        for comment in comments:
            all_child_ids.update(comment.children)

        top_level_comments = [c for c in sorted_comments if c.id not in all_child_ids]

        # Build comment structures
        comment_structures = []
        for comment in top_level_comments:
            comment_structure = build_comment_structure(comment)
            comment_structures.append(comment_structure)

        return PostSummary(
            post_title=submission.title,
            post_body=submission.body or "",
            children=comment_structures,
        )
