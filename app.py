import streamlit as st
import json
import os
from datetime import datetime
import concurrent.futures
import logging
import sys

from writer.ai.agent import Agent
from writer.model import AgentInput
from writer.searchengine.tavily_engine import TavilySearchEngine
from writer.utils.export import get_excel_data
from writer.utils.logging_config import get_logger, is_running_in_docker

# Get logger for this module
logger = get_logger(__name__)

# Set page configuration
st.set_page_config(
    page_title="AI Content Writer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the path for storing content history
HISTORY_FILE = "./history/content.json"

# Function to load content history
def load_history():
    logger.debug(f"Loading content history from {HISTORY_FILE}")
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                logger.info(f"Loaded {len(history)} content items from history")
                return history
        except Exception as e:
            logger.error(f"Error loading history: {str(e)}")
            st.error(f"Error loading history: {str(e)}")
            return []
    else:
        logger.info(f"History file {HISTORY_FILE} not found, returning empty history")
    return []


# Function to save content history
def save_history(history):
    logger.debug(f"Saving {len(history)} content items to {HISTORY_FILE}")
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
            logger.info(f"Successfully saved history to {HISTORY_FILE}")
    except Exception as e:
        logger.error(f"Error saving history: {str(e)}")
        st.error(f"Error saving history: {str(e)}")



# Function to delete content from history
def delete_content(content_id):
    logger.info(f"Deleting content with ID: {content_id}")
    history = load_history()
    original_length = len(history)
    history = [content for content in history if content["id"] != content_id]
    
    if len(history) == original_length:
        logger.warning(f"Content with ID {content_id} not found in history")
    else:
        logger.info(f"Successfully removed content with ID {content_id}")
        save_history(history)
        
    st.session_state.history = history
    if st.session_state.selected_content and st.session_state.selected_content.get("id") == content_id:
        logger.debug("Resetting selected content and showing form")
        st.session_state.selected_content = None
        st.session_state.show_form = True


# Function to generate content
def generate_content(campaign, content_subject, target_audience):
    logger.info(f"Generating content for subject: '{content_subject}', campaign: '{campaign}'")
    try:
        # Use search engine to get content about the subject
        logger.debug(f"Searching for content about: {content_subject}")
        search_engine = TavilySearchEngine()
        search_result = search_engine.search(query=content_subject)
        logger.info(f"Retrieved {len(search_result) if isinstance(search_result, list) else 1} search results")

        # Create input object
        agent_input = AgentInput(
            article_content=str(search_result),
            target_audience=target_audience
        )
        logger.debug("Created agent input with search results and target audience")

        # Create the three different agents
        logger.debug("Creating content generation agents")
        blog_agent = Agent.create_blog_agent()
        linkedin_agent = Agent.create_linkedin_agent()
        x_agent = Agent.create_x_agent()

        # Process content with all agents in parallel
        logger.info("Starting parallel content generation with all agents")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit all tasks and store the futures
            blog_future = executor.submit(blog_agent.process, agent_input)
            linkedin_future = executor.submit(linkedin_agent.process, agent_input)
            x_future = executor.submit(x_agent.process, agent_input)

            # Wait for all futures to complete and get their results
            logger.debug("Waiting for all agent processing to complete")
            blog_content = blog_future.result()
            linkedin_content = linkedin_future.result()
            x_content = x_future.result()
            logger.info("All agents completed content generation successfully")

        # Create content object
        content_id = datetime.now().strftime("%Y%m%d%H%M%S")
        logger.debug(f"Creating content object with ID: {content_id}")
        content = {
            "id": content_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campaign": campaign,
            "content_subject": content_subject,
            "target_audience": target_audience,
            "blog_content": blog_content,
            "linkedin_content": linkedin_content,
            "x_content": x_content
        }

        # Load existing history
        history = load_history()

        # Add new content to history
        history.append(content)
        logger.info(f"Added new content to history (now {len(history)} items)")

        # Save updated history
        save_history(history)
        logger.info(f"Content generation completed successfully for '{content_subject}'")

        return content
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}", exc_info=True)
        st.error(f"Error generating content: {str(e)}")
        return None


# Function to display content
def display_content(content):
    if content:
        logger.debug(f"Displaying content with subject: {content.get('content_subject', 'Unknown')}")
        st.title(content["content_subject"])
        st.markdown("---")

        # Display campaign and target audience
        st.write(f"**Campaign:** {content['campaign']}")
        st.write(f"**Target Audience:** {content['target_audience']}")

        st.markdown("---")

        # Display LinkedIn content
        st.subheader("LinkedIn")
        st.write(content["linkedin_content"])

        st.markdown("---")

        # Display X content
        st.subheader("X")
        st.write(content["x_content"])

        st.markdown("---")

        # Display Blog content
        st.subheader("Blog")
        st.write(content["blog_content"])
        
        logger.info(f"Successfully displayed content: {content.get('content_subject', 'Unknown')}")
    else:
        logger.warning("Attempted to display content but no content was provided")


# Initialize session state
logger.debug("Initializing session state")
if 'history' not in st.session_state:
    logger.debug("Loading history into session state")
    st.session_state.history = load_history()

if 'selected_content' not in st.session_state:
    logger.debug("Initializing selected_content as None")
    st.session_state.selected_content = None

if 'show_form' not in st.session_state:
    logger.debug("Initializing show_form as True")
    st.session_state.show_form = True


# Function to handle new content button click
def new_content_click():
    logger.info("New content button clicked")
    st.session_state.show_form = True
    st.session_state.selected_content = None


# Function to handle history item click
def history_item_click(content_id):
    logger.info(f"History item clicked: {content_id}")
    history = st.session_state.history
    for content in history:
        if content["id"] == content_id:
            logger.debug(f"Found content with ID {content_id}, setting as selected content")
            st.session_state.selected_content = content
            st.session_state.show_form = False
            break
    else:
        logger.warning(f"Content with ID {content_id} not found in history")


# Main layout
logger.debug("Setting up main application layout")
# Header with title and new button on the same line
cols = st.columns([4, 1])
with cols[0]:
    st.title("AI Content Writer")
with cols[1]:
    # Add some vertical space to align with the title
    st.write("")
    st.button("New Content", on_click=new_content_click, key="new_button", type="primary", use_container_width=True)

# Main content area with sidebar
col1, col2 = st.columns([1, 3])

# Sidebar with history
with col1:
    # History header and Export button in a row with right-aligned export button
    cols = st.columns([3, 1])
    
    # History subheader in first column
    with cols[0]:
        st.subheader("History")
    
    # Export button in second column (right-aligned)
    with cols[1]:
        if st.session_state.history:
            # Get Excel data and filename
            excel_data, filename = get_excel_data(st.session_state.history)
            
            # Use download_button with the data
            st.download_button(
                label="↓️",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="export_button",
                type="secondary",
                use_container_width=True,
                help="Export content to excel file"
            )
        else:
            # Disabled button if no history
            st.button("Export", key="export_button", type="primary", disabled=True, use_container_width=True)

    # Display history items
    for content in st.session_state.history:
        # Create a horizontal layout with two elements side by side
        cols = st.columns([5, 1])
        
        # Content subject button (left-aligned)
        with cols[0]:
            st.button(
                content["content_subject"],
                key=f"history_{content['id']}",
                on_click=history_item_click,
                args=(content["id"],),
                use_container_width=True
            )
        
        # Delete button (right-aligned)
        with cols[1]:
            st.button(
                "🗑️",
                key=f"delete_{content['id']}",
                on_click=delete_content,
                args=(content["id"],),
                help="Delete this content"
            )

# Main content area
logger.debug("Setting up main content area")
with col2:
    if st.session_state.show_form:
        logger.debug("Showing content creation form")
        st.subheader("Create Content")

        # Create form for input
        with st.form(key="content_form"):
            campaign = st.text_input("Campaign")
            content_subject = st.text_input("Content Subject")
            target_audience = st.text_input("Target Audience")

            # Initialize loading state if not exists
            if 'is_loading' not in st.session_state:
                logger.debug("Initializing is_loading state to False")
                st.session_state.is_loading = False

            submit_button = st.form_submit_button(label="Create", disabled=st.session_state.is_loading)

            if submit_button:
                logger.info("Content creation form submitted")
                st.session_state.is_loading = True
                if not campaign or not content_subject or not target_audience:
                    logger.warning("Form submitted with missing fields")
                    st.error("Please fill in all fields")
                else:
                    logger.info(f"Starting content generation for '{content_subject}'")
                    with st.spinner("Generating content..."):
                        content = generate_content(campaign, content_subject, target_audience)

                        # Reset loading state
                        st.session_state.is_loading = False

                        if content:
                            logger.info("Content generated successfully, updating UI")
                            st.session_state.history = load_history()
                            st.session_state.selected_content = content
                            st.session_state.show_form = False
                            logger.debug("Triggering page rerun to display new content")
                            st.rerun()
                        else:
                            logger.error("Content generation failed")
    else:
        logger.debug("Displaying selected content")
        display_content(st.session_state.selected_content)

# Log application startup complete
logger.info("AI Content Writer application initialized successfully")
