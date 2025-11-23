import json
import boto3

sns = boto3.client("sns")

# Esta função será chamada pela AWS quando um alerta precisar ser enviado
def lambda_handler(event, context):

    # Aqui estamos recebendo o "evento" do sensor ou IA

    print("Evento recebido:", event)

    # Pegando o valor do evento
    critico = event.get("critico", False)

    # Se não for crítico → não manda alerta
    if not critico:
        return {"status": "ok", "msg": "nada crítico"}

    # Mensagem que vai ser enviada
    mensagem = json.dumps(event)

    # ARN do tópico
    SNS_TOPIC_ARN = "ARN_DO_SEU_SNS_AQUI"

    # Envia alerta
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=mensagem,
        Subject="ALERTA CRÍTICO DETECTADO"
    )

    return {"status": "alerta_enviado"}
