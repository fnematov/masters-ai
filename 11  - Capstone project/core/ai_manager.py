import os

import chromadb
import pandas as pd
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from dotenv import load_dotenv
from autogen.agentchat import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from typing_extensions import Annotated

from .db_manager import SQLiteDBManager

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ Missing OpenAI API Key. Set OPENAI_API_KEY in the .env file.")

llm_config = {"model": "gpt-4o", "api_key": OPENAI_API_KEY}

db_manager = SQLiteDBManager()


def termination_message(message):
    return isinstance(message, dict) and message.get("content", "").strip().upper() == "TERMINATE"


# 🔹 User Proxy Agent (Handles user input)
user_proxy_agent = UserProxyAgent(
    name="User_Proxy",
    system_message="You are the user interacting with the AI sales team.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False,
    default_auto_reply="Reply 'TERMINATE' to end the conversation.",
    is_termination_msg=termination_message,
)

# 🔹 Sales Lead Agent (Main Orchestrator)
sales_lead_agent = AssistantAgent(
    name="Sales_Lead_Agent",
    system_message="""
    You are the Sales Lead Agent. Initiate conversations, ask qualifying questions, and route queries to specialized agents as needed.
    Keep it as soon as simple. You are in the chat. Not email. So, messages should be chat format. Keep them shorter.
    Be professional and friendly. Try to understand customer needs and guide the conversation accordingly. 
    
    Reply 'TERMINATE' to end the conversation.
    """,
    llm_config=llm_config,
    is_termination_msg=termination_message,
)

# 🔹 Product Expert Agent (Accesses Car Database)
product_expert_agent = AssistantAgent(
    name="Product_Expert_Agent",
    system_message="""
    You are the Product Expert Agent. Access the car database to recommend vehicles based on customer preferences and highlight promotions or limited stock.
    Always try to generate messages short. You are in the chat. Not email. So, messages should be chat format. Keep them shorter. 

    Reply 'TERMINATE' to end the conversation.
    """,
    llm_config=llm_config,
    is_termination_msg=termination_message,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_file = f"{current_dir}/../data/car_faq_terms.csv"

df = pd.read_csv(dataset_file)

# Convert each row into a Q&A formatted text chunk
documents = [
    f"Q: {row['question']}\nA: {row['answer']}" for _, row in df.iterrows()
]

# 🔹 Compliance Agent (Policy Enforcement)
compliance_agent = RetrieveUserProxyAgent(
    name="Compliance_Agent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    retrieve_config={
        "task": "qa",
        "docs": documents,  # Pass the processed text instead of file path
        "chunk_token_size": 300,
        "embedding_model": "text-embedding-ada-002",
        "client": chromadb.PersistentClient(path='chroma'),
        "overwrite": True,  # Force re-creation
        "get_or_create": True,  # Ensure collection exists
    },
    code_execution_config=False,  # Disable code execution
    is_termination_msg=termination_message,
)

# 🔹 Closing Agent (Finalizes Deals)
closing_agent = AssistantAgent(
    name="Closing_Agent",
    system_message="""
    You are the Closing Agent. Finalize deals and provide necessary documentation to customers. 
    For complete order need to collect first_name, last_name, email, phone and selected car_id.
    Get all data from user and create order. 
    Always try to generate messages short. You are in the chat. Not email. So, messages should be chat format. Keep them shorter.
    
    Reply 'TERMINATE' to end the conversation.
    """,
    llm_config=llm_config,
    is_termination_msg=termination_message
)

# 🔹 Objection Handler Agent (Resolves Hesitations)
objection_handler_agent = AssistantAgent(
    name="Objection_Handler_Agent",
    system_message="""
    You are the Objection Handler Agent. Address customer concerns and provide reassurance.
    You need to negotiate with customer and try to close the deal.
    Maximum discount is up to 10%.
    Try to give less discount, but if customer insist, you can give up to 10% discount.
    Always keep in mind, you are in the chat. Not email. So, messages should be chat format. Keep them shorter.
    
    Reply 'TERMINATE' to end the conversation.
    """,
    llm_config=llm_config,
    is_termination_msg=termination_message,
)

# 🔹 Initialize GroupChat with all agents
groupchat = GroupChat(
    agents=[
        user_proxy_agent,
        sales_lead_agent,
        product_expert_agent,
        compliance_agent,
        closing_agent,
        objection_handler_agent,
    ],
    messages=[],
    max_round=12,
    speaker_selection_method="auto",
    allow_repeat_speaker=False,
)

# 🔹 Initialize GroupChatManager
agent_manager = GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
    is_termination_msg=termination_message,
)


@user_proxy_agent.register_for_execution()
@product_expert_agent.register_for_llm(description="Get top 5 cars data from database by request.")
def get_car_data(
        make: Annotated[str, "Name of make"] = None,
        model: Annotated[str, "Name of model"] = None,
        year_range: Annotated[str, "Range of years. Should be separated with '-'. Example: 2023-2025"] = None,
        mileage_range: Annotated[str, "Mileage range. Should be separated with '-'. Example: 12000-25000"] = None,
        transmission_type: Annotated[str, "Transmission type: automatic, manual, semi-automatic, robot, etc."] = None,
        fuel_type: Annotated[str, "Fuel type: electric, diesel, petrol, hybrid, etc."] = None,
        msrp_range: Annotated[
            str, "Client price range without currency symbol. Should be separated with '-'. Example: 13000-20000."] = None
):
    """Query the car database for relevant information"""

    # ✅ Parse range values
    year_from, year_to = map(int, year_range.split("-")) if year_range else (None, None)
    mileage_from, mileage_to = map(int, mileage_range.split("-")) if mileage_range else (None, None)
    msrp_from, msrp_to = map(int, msrp_range.split("-")) if msrp_range else (None, None)

    # ✅ Call the database manager with structured filters
    return db_manager.fetch_cars(
        make=make,
        model=model,
        year_from=year_from,
        year_to=year_to,
        mileage_from=mileage_from,
        mileage_to=mileage_to,
        transmission_type=transmission_type,
        fuel_type=fuel_type,
        msrp_from=msrp_from,
        msrp_to=msrp_to
    )


@user_proxy_agent.register_for_execution()
@closing_agent.register_for_llm(description="Creates order and generates contract.")
def create_order(
        car_id: Annotated[int, "Chosen car ID from database. Should be integer. Should provide from product expert agent"],
        first_name: Annotated[str, "First name of the customer"],
        last_name: Annotated[str, "Last name of the customer"],
        phone_number: Annotated[str, "Phone number of the customer"],
        email: Annotated[str, "Email of the customer"]
) -> Annotated[str, "Creates order and generates contract"]:
    """Create a new order in the database"""
    try:
        db_manager.create_order(car_id, first_name, last_name, phone_number, email)
        return "Order created successfully. You can sign contract by url: https://example.com/contract."
    except Exception as e:
        return f"Error creating order: {e}"


def process_message(messages=None):
    """Passes user input to AutoGen's GroupChatManager for intelligent routing."""

    last_agent, last_message = agent_manager.resume(messages)

    result = last_agent.initiate_chat(
        agent_manager,
        message=last_message,
        clear_history=False,
        summary_method="reflection_with_llm",
        summary_args={
            "summary_prompt": (
                """As a Sales Manager your role is generate next message to customer based on your agents result. 
                Review your agents history, summarize and regenerate next message to customer as a professional sales manager.
                Feel yourself as a human.\n\n

                - **Sales Lead Agent**: Introduced the conversation, understood customer needs, and guided the discussion.\n
                - **Product Expert Agent**: Searched the car database and provided vehicle recommendations based on the customer's budget and preferences.\n
                - **Objection Handler Agent**: Addressed customer concerns and provided reassurance about quality, availability, or financing.\n
                - **Compliance Agent**: Ensured that all information provided aligns with company policies and legal requirements.\n
                - **Closing Agent**: Helped finalize the deal, including discussing contracts, next steps, and delivery options.\n\n

                Structure the summary clearly and professionally, ensuring the customer understands the key takeaways and possible next steps.
                Always try to generate messages short. You are in the chat. Not email. So, messages should be chat format. Keep them shorter.
                """
            )
        },
        max_turns=2,
    )

    return result.summary
