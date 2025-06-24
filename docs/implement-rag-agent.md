# Self-paced handson: Company Rules Agent の変更

## 📝ここで学ぶこと

- Tool Calling (Function Calling) を使った実践的な Agent の実装の基礎

## ⚗️Company Rules Agent の変更

agents フォルダー内にある "campany_rules_agent.py" を開きます。
ここで実装されている `AssistantAgent` は、system_message に「常に、「該当する社内規程はありません」と返答します。」に定義されている通り、単調な回答しか返さない Agent になっています。

これを、実際に社内規程を調べて、該当する社内規程を返す Agent に変更します。既存のコードを消して以下のコードに置き換えます。

※ コードの解説は後述します。

```python
import json
import os

import requests
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import FunctionTool

COMPANY_RULES_RAG_ENDPOINT: str = os.environ.get("COMPANY_RULES_RAG_ENDPOINT")

def get_asnwer_from_company_rules_rag(question: str) -> str:
    """会社の規程に関連する情報を取得できます"""
    body = {
        "question": question,
    }
    response = requests.post(
        COMPANY_RULES_RAG_ENDPOINT,
        data=json.dumps(body, ensure_ascii=False),
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.text

def get_compay_rules_agent(model_client: ChatCompletionClient) -> AssistantAgent:
    company_rules_rag_tool = FunctionTool(
        get_asnwer_from_company_rules_rag,
        description="会社の規程 (正社員や正社員以外の就業規則, 出張旅費, 賃金, 退職金, 福利厚生, 特定個人情報取扱など) に関連する情報を取得できます"
    )

    return AssistantAgent(
        name="CompanyRulesAgent",
        description="会社の規程 (正社員や正社員以外の就業規則, 出張旅費, 賃金, 退職金, 福利厚生, 特定個人情報取扱など) に関連する質問に回答するエージェント",
        model_client=model_client,
        tools=[company_rules_rag_tool],
        system_message="""tool: company_rules_rag_tool を使用して会社の規程に関する質問に対する回答を取得することができます。
主に以下に関する質問に回答ができます。

- "出張旅費規程": 出張旅費(目的, 適用範囲, 留意事項,  出張の区分, 出張旅費の構成, 出張の区分による出張旅費の支給基準, 出張申請・仮払い, 出張報告・旅費の清算, 旅費の分担, 出張中の傷病・災害, 出発・帰着の場所, 交通手段, 日当, 交通費, 宿泊費, 研修費, その他費用, 外貨建て旅費の円換算, 旅費の減額・不支給)
- "就業規則": 総則(目的, 従業員の定義, 適用範囲, 規則遵守の義務), 服務(服務規律, 営業秘密・個人情報の管理, 通勤方法, 兼業の届出), 人事(採用, 採用選考, 内定取消事由, 採用時の提出書類, 試用期間, 正社員への転換, 派遣社員からの採用, 労働条件の明示, 人事異動, 休職, 休職期間, 復職), 定年、退職及び解雇(定年, 退職, 解雇, 解雇の予告, 解雇の制限), 労働時間、休憩及び休日(所定労働時間, 始業・終業の時刻及び休憩時間, フレックスタイム制, 専門業務型裁量労働制, 出張時の勤務時間及び旅費, 欠勤・遅刻・早退・私用外出, 休日, 休日の振替, 時間外・休日労働, 時間外・休日労働の事前承認, 代休, 適用除外), 休暇及び休業(年次有給休暇, 採用時特別休暇, 慶弔休暇, 産前産後の休業, 母性健康管理のための休暇等, 育児・介護休業、子の看護休暇等, 育児時間, 生理休暇, 公民権行使等休暇), 賃金及び退職金(賃金・賞与, 退職金, 出張旅費), 福利厚生(福利厚生), 懲戒(懲戒の種類, けん責、減給、出勤停止又は降職, 諭旨解雇又は懲戒解雇, 損害賠償), 教育(教育訓練), 安全衛生及び労災補償(遵守義務, 健康診断, 安全衛生教育, 災害補償), 知的財産(職務発明)
- "特定個人情報取扱規程": 総則(目的, 適用範囲, 定義, 利用目的, 会社が行う個人番号関係事務の範囲, 特定個人情報責任者, 事務取扱担当者), 特定個人情報の取扱い(安全管理の原則, 遵守事項, 教育研修, 個人番号の提供および収集, 本人確認), 保管及び廃棄等(情報の開示と訂正, 特定個人情報の廃棄, 特定個人情報の外部提供), 危機管理(危機管理対応, 危機管理対応, 懲戒及び損害賠償, 苦情・相談窓口, 法令との関係, 改廃)
- "特定個人情報取扱規程補足資料 保存期間": 本書について(（参考）特定個人情報の廃棄), 国税関係(法定の保管義務, 対応), 雇用保険関係(法定の保管義務, 対応), 労災保険関係(法定の保管義務, 対応), 社会保険関係(法定の保管義務, 対応)
- "短時間正社員 就業規則": 総則(目的, 適用範囲), 人事(利用事由, 雇用契約期間, 常勤正社員への復帰), 労働時間、始業就業の時刻、休憩時間および休日(労働時間, 時間外労働, 始業・終業の時刻, 休憩時間, 休日), 賃金・賞与・退職金(賃金, 賞与, 退職金), その他(年次有給休暇, 社会保険・労働保険の加入)
- "賃金規程": 総則(目的, 適用範囲, 賃金の構成, 賃金の支払と控除, 賃金計算期間及び支払日, 端数処理, 昇給・降給, 賃金請求権の時効, 手当の届け出及び不正受給), 正社員の賃金(本章の適用範囲, 賃金の支払形態, 基本給, 職能給, 業務手当, 役職手当, 通勤手当, 住宅手当, 所定外労働手当, 賃金の日割り計算, 休職・休暇・欠勤等による賃金の減額), 臨時社員及び嘱託社員の賃金(本章の適用範囲, 賃金の支払形態, 基本給, 職能給, 業務手当, 役職手当, 通勤手当, 住宅手当, 所定外労働手当, 休職・休暇・欠勤等による賃金の減額), 賞与(賞与の支給, 計算対象期間, 賞与の決定)
- "退職金規程": 総則(目的, 退職金の支給範囲), 退職金共済(退職金共済契約, 退職金共済契約の時期, 掛金, 掛金の納付停止, 退職金の額, 退職金の減額, 退職金の支給方法)
- "福利厚生規程": 福利厚生(目的, 適用範囲, 不正受給, 慶弔見舞金, 社内懇親会補助, 書籍購入補助, セミナー補助, 予防接種補助)
"""
    )

```

### コードの解説

前提として...

- 会社規定の RAG は事前に用意してあり、今回はその API をコールするのみになります。
- 会社規程の RAG の実装は今回のワークショップではスコープ外ですが、トレーナーによって開発した API になりますので興味がありましたらトレーナーまでご質問ください。
- 実際に利用した社内規程のドキュメントはコンテンツの repo 内に含まれています。

コードの概要は以下になります。

#### get_asnwer_from_company_rules_rag

- RAG の API をコールして回答を返す関数です。

#### get_compay_rules_agent()

- 最初に Function Calling で利用する tool を FunctionTool で初期化したのが `company_rules_rag_tool` になります。
- あとは、tools を指定して AssistantAgent を初期化しているだけです。
  - system_message には、Function Calling で利用する tool の説明と、どのような質問に回答できるかを記載しています。ここで何が質問できるかを細かく記載していますが、これは会社規程のデータソースから index を作る際に、プログラムで抽出したデータです。
  - AssistantAgent の初期化時に指定可能な `reflect_on_tool_use` はデフォルト値の False のため省略されています。この設定の場合は、Tool Calling の結果をそのまま回答します。この値が True の場合は、Tool Calling の結果をもとに AssistantAgent の model client で回答を生成する動作となります。コールする Tool の回答の特性に応じて `reflect_on_tool_use` を使い分けます。

## ⚗️デバッグ実行

ターミナルでコマンド: `func start` を入力してデバッグ実行し、rest-local.http を開いて以下のような質問をしてみましょう。

```text
私は正社員です。出発地は東京で、目的地は名古屋市で3月5日から3泊で出張計画を立ててください
```

会社規程では、出張場所に応じた宿泊費の定義、交通費の定義、社員の区分での日当の違いなどが書かれています。

デバッグログを確認すると、以前とは異なり、Tool Calling (Function Calling) の実行によりベントのログが表示され、実際に RAG の API をコールしていることがわかります。
ここで会社規程の情報を取得し、後続のエージェントではその情報を加味した出張計画が作成されたことが確認できるはずです。

### 補足

Tool Calling (Function Calling) の基本的な情報は、以下のドキュメントをご参照ください。

- [Using Tools - Agents - AutoGen](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html#using-tools)

また、補足として `AssistantAgent` class の詳細は以下のドキュメントになります。`AssistantAgent` について気になることがある際はこのドキュメントを参考になります。

- [autogen_agentchat.agents — AutoGen](https://microsoft.github.io/autogen/stable//reference/python/autogen_agentchat.agents.html)

<br>

---

[📋 目次へ戻る](../README.md) | [⏭️ 次へ進む: Azure Functions へのデプロイ](./deploy-to-function-app.md)


