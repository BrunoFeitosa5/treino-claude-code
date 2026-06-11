const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { z } = require("zod");

const BASE_URL = "https://treino-claude-code.vercel.app";

const servidor = new McpServer({
  name: "mcp-tarefas",
  version: "1.0.0",
});

servidor.tool(
  "listar_tarefas",
  "Lista todas as tarefas cadastradas",
  {},
  async () => {
    const resposta = await fetch(`${BASE_URL}/tarefas`);
    if (!resposta.ok) {
      return { content: [{ type: "text", text: `Erro ao buscar tarefas: ${resposta.status}` }] };
    }
    const tarefas = await resposta.json();

    if (tarefas.length === 0) {
      return { content: [{ type: "text", text: "Nenhuma tarefa cadastrada." }] };
    }

    const lista = tarefas
      .map((t) => `[${t.concluida ? "x" : " "}] ${t.id}. ${t.titulo}`)
      .join("\n");

    return { content: [{ type: "text", text: `Tarefas:\n${lista}` }] };
  }
);

servidor.tool(
  "adicionar_tarefa",
  "Adiciona uma nova tarefa à lista",
  { titulo: z.string().min(1).describe("Título da tarefa") },
  async ({ titulo }) => {
    const resposta = await fetch(`${BASE_URL}/tarefas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ titulo }),
    });
    if (!resposta.ok) {
      return { content: [{ type: "text", text: `Erro ao adicionar tarefa: ${resposta.status}` }] };
    }
    const tarefa = await resposta.json();

    return { content: [{ type: "text", text: `Tarefa "${tarefa.titulo}" adicionada com ID ${tarefa.id}.` }] };
  }
);

servidor.tool(
  "concluir_tarefa",
  "Marca uma tarefa como concluída",
  { id: z.number().int().positive().describe("ID da tarefa") },
  async ({ id }) => {
    const resposta = await fetch(`${BASE_URL}/tarefas/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ concluida: true }),
    });
    if (!resposta.ok) {
      return { content: [{ type: "text", text: `Erro ao concluir tarefa: ${resposta.status}` }] };
    }
    const tarefa = await resposta.json();
    return { content: [{ type: "text", text: `Tarefa "${tarefa.titulo}" marcada como concluída.` }] };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await servidor.connect(transport);
}

main().catch(console.error);
