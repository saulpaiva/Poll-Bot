# Poll Bot - Bot de Enquetes para Discord

Um bot de Discord que permite criar e gerenciar enquetes em seus servidores.

## Funcionalidades

1. **Criação de Enquetes Simples**
   - Comando: `!poll "Pergunta" "Opção1" "Opção2" ...`
   - Cria uma enquete com até 10 opções
   - Os membros votam usando reações

2. **Enquetes com Temporizador**
   - Comando: `!timerpoll minutos "Pergunta" "Opção1" "Opção2" ...`
   - Enquete que encerra automaticamente após o tempo especificado
   - Mostra os resultados finais quando o tempo acaba

3. **Limpeza de Enquetes**
   - Comando: `!clearpolls [limite]`
   - Remove todas as enquetes do canal (requer permissão de gerenciar mensagens)

## Como Configurar

1. Instale as dependências:

pip install -r requirements.txt