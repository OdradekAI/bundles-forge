import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_REL = "../../skills/using-<project-name>/SKILL.md";

const handler = async (event) => {
  const validActions = new Set(["new", "reset"]);
  if (event.type !== "command" || !validActions.has(event.action)) return;

  const skillPath = resolve(__dirname, SKILL_REL);
  let content;
  try {
    content = readFileSync(skillPath, "utf8");
  } catch (err) {
    console.error(
      `[<project-name>] Cannot read bootstrap skill at ${skillPath}: ${err.message}`
    );
    return;
  }
  if (!content) return;

  const ctx =
    "<EXTREMELY_IMPORTANT>\n" +
    "You have <project-name> skills loaded.\n\n" +
    "**Below is the full content of your " +
    "'<project-name>:using-<project-name>' skill. For all other skills, " +
    "use the native skill discovery mechanism:**\n\n" +
    content +
    "\n</EXTREMELY_IMPORTANT>";

  event.messages.push(ctx);
};

export default handler;
