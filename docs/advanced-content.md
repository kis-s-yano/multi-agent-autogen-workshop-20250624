# Advanced contents

さらに発展的な Multi-Agent を実装するための要素とそのドキュメントを紹介します。

## 状態の管理

今回のハンズオンでは、API がコールされるたびに team のインスタンスを生成してタスクの処理を行いました。
そのため、以前の会話履歴はない状態です。
過去の会話履歴も理解してタスクを処理する場合、状態 (State) を管理することで実現できます。

実装方法の詳細は以下になります。

- [Manage State - AutoGen](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)

また、State の管理にあたり補足として team の reset, stop, resume, abort などの挙動も把握しておくとよいです。

詳細は以下になります。

- [Teams - AutoGen](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)


## 人間へのフィードバック

今回のハンズオンで実装したアプリでは、人間からの指示でアプリがタスクを処理しますが、タスクを処理するための情報の不足がある場合、人間に情報を求めたいケースが出てきます。

AutoGen では Human in the loop と表現されており、実装方法の詳細は以下になります。

- [Human-in-the-Loop - AutoGen](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)
