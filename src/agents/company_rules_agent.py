from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient


def get_compay_rules_agent(model_client: ChatCompletionClient) -> AssistantAgent:
    return AssistantAgent(
        name="CompanyRulesAgent",
        description="会社の規程 (正社員や正社員以外の就業規則, 出張旅費, 賃金, 退職金, 福利厚生, 特定個人情報取扱など) に関連する質問に回答するエージェント",
        model_client=model_client,
        system_message="""常に、「該当する社内規程はありません」と返答します。
"""
    )
