import logging
import os

import azure.functions as func
from autogen_agentchat.base import TaskResult
from autogen_agentchat.teams import BaseGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from agents.team_orchestrator import get_team

logging.getLogger("autogen_core").setLevel(logging.WARNING)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

model_client = AzureOpenAIChatCompletionClient(
    azure_endpoint=os.environ.get("AOAI_ENDPOINT"),
    api_key=os.environ.get("AIF_API_KEY"),
    model=os.environ.get("AIF_DEPLOYMENT_CHAT_MODEL"),
    azure_deployment=os.environ.get("AIF_DEPLOYMENT_CHAT"),
    api_version=os.environ.get("AIF_API_VERSION"),
    temperature=0.6,
)


def format_message(message: str):
    return message.replace('"TERMINATE"', '').replace('**TERMINATE**', '').replace('TERMINATE', (''))


@app.route(route="chat", methods=["POST"])
async def chat(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    task = req_body.get("task")

    if not task:
        return func.HttpResponse(
            "Please pass a task in the request body",
            status_code=400
        )

    team: BaseGroupChat = get_team(model_client)
    stream = team.run_stream(task=task)
    task_result_content = ""
    async for chunk in stream:
        if isinstance(chunk, TaskResult):
            # 最終回答が返ってきた場合
            task_result_content = chunk.messages[-1].content
            logging.info(f">>>>>>>> STOP REASON: {chunk.stop_reason}\n")
        else:
            # 中間結果が返ってきた場合
            logging.info(f"-------------- {chunk.source} ({chunk.type}) --------------\n{chunk.content}\n")

    return func.HttpResponse(
        format_message(task_result_content),
        status_code=200
    )
