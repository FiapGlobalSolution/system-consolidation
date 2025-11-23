# Timer-Driven Service Bus Poller (Python Azure Function)

This function app wakes up every 5 minutes (timer trigger), pulls messages from an Azure Service Bus queue using the SDK, optionally saves each event to Azure Cosmos DB (Mongo API), replicates the JSON payloads to an Amazon SQS queue, and can publish threshold alerts to an AWS SNS topic. Each message is logged with helpful metadata and left ready for you to plug in domain-specific processing.

## Prerequisites

1. [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local) with Python worker enabled.
2. Python 3.10+ and a virtual environment (Core Tools creates one automatically inside `.venv`).
3. An Azure Service Bus namespace with a queue and a SAS policy that grants `Listen` (and optionally `Peek`/`Manage`) rights.
4. Azurite or an Azure Storage account for the `AzureWebJobsStorage` setting.

## Local configuration

Update `local.settings.json` with your own values:

- `AzureWebJobsStorage`: set to `UseDevelopmentStorage=true` for Azurite or the connection string of a real storage account.
- `SERVICEBUS_CONNECTION`: the Service Bus connection string (namespace endpoint + key).
- `SERVICEBUS_QUEUE_NAME`: queue name to listen to.
- `SERVICEBUS_MAX_MESSAGE_COUNT` *(optional)*: max messages to drain per run (default `25`).
- `SERVICEBUS_MAX_WAIT_TIME` *(optional)*: seconds to wait for new messages (default `5`).
- `COSMOS_MONGO_ENABLED`: set to `true` to turn on persistence (requires all settings below).
- `COSMOS_MONGO_CONN_STRING`: Cosmos DB Mongo connection string (include `retrywrites=false`).
- `COSMOS_MONGO_DB`: target database name.
- `COSMOS_MONGO_COLLECTION`: collection that already exists with an appropriate partition key.
- `COSMOS_MONGO_PARTITION_FIELD` *(optional)*: document field name that matches your container's partition key (default `partitionKey`).

> ℹ️ Escolha uma chave de partição com alta cardinalidade (por exemplo, `tenantId`, `deviceId` ou outro identificador exclusivo) para distribuir a carga e evitar hot partitions no Cosmos DB.

- `SQS_ENABLED`: set to `true` to activate replication to AWS SQS.
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` *(optional)*: credentials with permission to send to the target queue.
- `AWS_REGION`: region where the queue lives (e.g., `us-east-1`).
- `SQS_QUEUE_URL`: full queue URL from the AWS Console.
- `SQS_BATCH_SIZE` *(optional)*: up to 10 messages per batch (default `10`).
- `SQS_MAX_RETRIES` *(optional)*: number of retry attempts for failed sends (default `3`).

- `SNS_ENABLED`: set to `true` to activate notifications via AWS SNS.
- `SNS_TOPIC_ARN`: destination topic ARN.
- `SNS_SUBJECT` *(optional)*: subject shown on the notification (default `IoT Environmental Alert`).
- `SNS_MIN_HUMIDITY` *(optional)*: humidity threshold in percent (default `20`).
- `SNS_MAX_TEMPERATURE` *(optional)*: temperature threshold in °C (default `32`).
- `SNS_MAX_RETRIES` *(optional)*: number of retry attempts for SNS publishes (default `3`).

- Quando `SQS_ENABLED=true`, cada evento montado é enviado para a fila alvo em formato JSON usando lotes (`SendMessageBatch`). Falhas são tentadas novamente até 3 vezes (configurável via `SQS_MAX_RETRIES`). Não há criptografia adicional além do que o serviço SQS já aplica.
- Quando `SNS_ENABLED=true`, todo documento cujo payload contenha `humidity`/`humidade` abaixo de `SNS_MIN_HUMIDITY` **ou** `temperature`/`temperatura` acima de `SNS_MAX_TEMPERATURE` dispara uma notificação JSON publicada no tópico configurado.

Never commit real secrets. Use `func settings delete <name>` or user-level `local.settings.json` overrides to keep secrets out of source control.

## Install dependencies

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the function locally

```
func start --verbose
```

When the timer fires you should see log output showing the polling attempt. Enqueue a test message (Portal, Service Bus Explorer, or `az servicebus queue message send`) and wait up to the next 5-minute window to observe it being drained.

## Deploying

1. Create a Function App with the Python runtime in your Azure subscription.
2. Configure `SERVICEBUS_CONNECTION`, `SERVICEBUS_QUEUE_NAME`, timer tuning settings, the `COSMOS_MONGO_*` variables (se for persistir), os parâmetros AWS/SQS (se for replicar) e os parâmetros `SNS_*` (se for notificar). Nunca armazene chaves em código.
3. Deploy using `func azure functionapp publish <app-name>` or CI/CD of your choice.
4. Monitor logs via `func azure functionapp logstream <app-name>` or Application Insights.
