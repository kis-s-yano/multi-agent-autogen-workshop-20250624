from autogen_core.models import ChatCompletionClient
from autogen_agentchat.teams import BaseGroupChat, SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

from .planner_agent import get_planner_agent
from .hotel_search_agent import get_hotel_search_agent
from .transport_cost_agent import get_transport_cost_agent
from .summary_agent import get_summary_agent
from .company_rules_agent import get_compay_rules_agent

# https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html#selector-prompt
selector_prompt = """あなたのタスクは、会話の状況に応じて次のタスクを実行する role を選択することです。
## 次の話者の選択ルール

各 role の概要以下です。

{roles}

次のタスクに選択可能な role は以下です。

{participants}

以下のルールに従って、次のを選択してください。

- 会話履歴を確認し、次の会話に最適な role を選択します。role name のみを返してください。
- role は1つだけ選択してください。
- 他の role が作業を開始する前に、"PlannerAgent" にタスクを割り当て、サブタスクを計画してもらうことが必要です。
  - PlannerAgent はサブタスクの計画のみを行います。サブタスクの作業を依頼してはいけません。
- PlannerAgent が計画したサブタスクに応じて、role を選択します。
- タスクを完了するための必要な情報が揃ったと判断したら "SummaryAgent" に最終回答の作成を依頼します。

## 会話履歴

{history}
"""


def get_team(model_client: ChatCompletionClient) -> BaseGroupChat:
    planner_agent = get_planner_agent(model_client)
    compay_rules_agent = get_compay_rules_agent(model_client)
    hotel_search_agent = get_hotel_search_agent(model_client)
    transport_cost_agent = get_transport_cost_agent(model_client)
    summary_agent = get_summary_agent(model_client)

    termination_condition = TextMentionTermination("TERMINATE") | MaxMessageTermination(12)

    team = SelectorGroupChat(
        [planner_agent, compay_rules_agent, hotel_search_agent, transport_cost_agent, summary_agent],
        model_client=model_client,
        termination_condition=termination_condition,
        selector_prompt=selector_prompt,
        allow_repeated_speaker=False
    )

    return team
