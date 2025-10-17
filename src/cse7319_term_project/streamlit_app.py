import streamlit as st
import os
import dotenv
from controller.post_controller import PostController

# Load environment variables from .env file
dotenv.load_dotenv()

# Page config
st.set_page_config(
    page_title="Reddit to LinkedIn Generator", page_icon="🔄", layout="wide"
)


# Initialize controller
@st.cache_resource
def get_controller():
    return PostController()


def main():
    st.title("🔄 Reddit to LinkedIn Post Generator")
    st.markdown("Generate LinkedIn posts from trending Reddit discussions")

    # Check for environment variables
    required_vars = [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USERNAME",
        "GEMINI_API_KEY",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        st.error(f"Missing environment variables: {', '.join(missing_vars)}")
        st.info("Please set these in your .env file")
        return

    # Main generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(
            "🎲 Generate Random Post", type="primary", use_container_width=True
        ):
            generate_post()


def generate_post():
    """Generate and display a random post with LLM response"""
    controller = get_controller()

    with st.spinner("🔍 Finding a random Reddit post..."):
        try:
            result = controller.get_random_post_with_llm_response()
            display_results(result)
        except Exception as e:
            st.error(f"❌ Error generating post: {str(e)}")


def display_results(result):
    """Display the generated results in an organized layout"""
    submission = result["submission"]
    comments = result["comments"]
    llm_response = result["llm_response"]
    metadata = result["metadata"]

    # Generated Content - Front and Center
    st.markdown("## 🎯 Generated LinkedIn Post")
    st.markdown("---")

    # Display the generated content in a prominent box
    st.markdown(
        f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #0066cc;
            margin: 20px 0;
        ">
            {llm_response.content.replace("\n", "<br>")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Copy button for the generated content
    st.code(llm_response.content, language="text")

    st.markdown("---")

    # Source Information
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📊 Post Metadata")
        st.write(f"**Subreddit:** r/{submission.subreddit}")
        st.write(f"**Score:** {submission.score}")
        st.write(f"**Total Comments:** {metadata['total_comments']}")
        st.write(f"**Comments Analyzed:** {metadata['top_comments_used']}")
        st.write(f"**Generated:** {llm_response.timestamp}")

    with col2:
        st.markdown("### 🤖 Generation Settings")
        st.write(f"**Model:** {llm_response.model_used}")
        st.write(f"**Post ID:** {submission.id}")

    # Original Submission
    with st.expander(f"📝 Original Post: {submission.title}", expanded=False):
        st.markdown(f"**r/{submission.subreddit}** • Score: {submission.score}")
        if submission.body:
            st.markdown("**Post Content:**")
            st.write(submission.body)
        else:
            st.info("This post has no body text (link post)")

    # Comments Section
    with st.expander(f"💬 Comments ({len(comments)} total)", expanded=False):
        if comments:
            # Sort comments by score for display
            sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)

            # Display top comments
            st.markdown("**Top Comments:**")
            for i, comment in enumerate(sorted_comments[:10]):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**u/{comment.author}**")
                        st.write(comment.body)
                    with col2:
                        st.metric("Score", comment.score)
                        if comment.children:
                            st.caption(f"{len(comment.children)} replies")
                    st.markdown("---")
        else:
            st.info("No comments found")

    # Raw Data (for debugging)
    with st.expander("🔧 Raw Data (Debug)", expanded=False):
        st.json(
            {
                "submission": submission.model_dump(),
                "metadata": metadata,
                "total_comments": len(comments),
            }
        )


if __name__ == "__main__":
    main()
