#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "typer",
#     "rich",
#     "pyyaml",
# ]
# ///
"""
Forge SDD CLI - Setup tool for Specification-Driven Development with Atlassian Forge

Usage:
    uv run forge-sdd-cli.py init --here
    uv run forge-sdd-cli.py check
    uv run forge-sdd-cli.py version

Or install globally:
    uv tool install forge-sdd-cli.py
    forge-sdd init --here
    forge-sdd check
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.tree import Tree
from typer.core import TyperGroup

console = Console()

# Constants
VERSION = "1.0.0"

# ASCII Art Banner
BANNER = """
███████╗ ██████╗ ██████╗  ██████╗ ███████╗    ███████╗██████╗ ██████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝    ██╔════╝██╔══██╗██╔══██╗
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗      ███████╗██║  ██║██║  ██║
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝      ╚════██║██║  ██║██║  ██║
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗    ███████║██████╔╝██████╔╝
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚══════╝╚═════╝ ╚═════╝
"""

TAGLINE = "Specification-Driven Development for Atlassian Forge Apps"


class StepTracker:
    """Track and render hierarchical steps"""

    def __init__(self, title: str):
        self.title = title
        self.steps = []
        self._refresh_cb = None

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return
        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""
            status = step["status"]

            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


class BannerGroup(TyperGroup):
    """Custom group that shows banner before help"""

    def format_help(self, ctx, formatter):
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="forge-sdd",
    help="Setup tool for Forge Specification-Driven Development projects",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


def show_banner():
    """Display the ASCII art banner"""
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided"""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'forge-sdd --help' for usage information[/dim]"))
        console.print()


def check_tool(tool: str) -> bool:
    """Check if a tool is installed"""
    return shutil.which(tool) is not None


def is_git_repo(path: Path = None) -> bool:
    """Check if the specified path is inside a git repository"""
    if path is None:
        path = Path.cwd()

    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo(project_path: Path, quiet: bool = False) -> bool:
    """Initialize a git repository"""
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "feat: Initialize Forge SDD Toolkit"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
    finally:
        os.chdir(original_cwd)


def is_forge_project(path: Path) -> bool:
    """Check if the specified path is a Forge project"""
    manifest = path / "manifest.yml"
    return manifest.exists()


def get_toolkit_root() -> Path:
    """Get the root directory of the toolkit (where resource files are located)
    
    When running from source: returns the directory containing this file
    When installed via pip/uv: searches for forge_sdd_toolkit_data directory
    """
    # Get directory of this module
    module_dir = Path(__file__).parent
    
    # Check if we're in the source repository (has .git, README.md, etc.)
    if (module_dir / ".github").exists() and (module_dir / "prompts").exists():
        return module_dir
    
    # When installed via pip/uv with setuptools data-files,
    # files are placed in forge_sdd_toolkit_data/ subdirectory
    data_dir = module_dir / "forge_sdd_toolkit_data"
    if data_dir.exists():
        return data_dir
    
    # If installed via pip/uv with MANIFEST.in, files might be alongside module
    if (module_dir / ".github").exists():
        return module_dir
        
    # Last resort: try to find the repo root by walking up
    current = module_dir
    search_paths = [str(module_dir)]
    for _ in range(5):  # Don't go too far up
        if (current / ".github").exists() and (current / "prompts").exists():
            return current
        if (current / "forge_sdd_toolkit_data").exists():
            return current / "forge_sdd_toolkit_data"
        search_paths.append(str(current))
        current = current.parent
    
    # If nothing found, return module dir and let the error happen downstream
    console.print(f"[yellow]Warning: Could not find toolkit resources. Searched in:[/yellow]")
    for path in search_paths:
        console.print(f"  - {path}")
    return module_dir



def copy_toolkit_structure(project_path: Path, tracker: Optional[StepTracker] = None) -> dict:
    """Copy toolkit structure to project"""
    toolkit_root = get_toolkit_root()
    stats = {"files": 0, "dirs": 0}

    # Copy .github directory (without prompts first)
    github_source = toolkit_root / ".github"
    github_dest = project_path / ".github"

    if github_source.exists():
        if github_dest.exists():
            # Only remove if we're going to replace it
            # But preserve existing prompts directory
            existing_prompts = github_dest / "prompts"
            has_existing_prompts = existing_prompts.exists()

            if has_existing_prompts:
                # Backup existing prompts temporarily
                import tempfile
                with tempfile.TemporaryDirectory() as tmpdir:
                    temp_prompts = Path(tmpdir) / "prompts"
                    shutil.copytree(existing_prompts, temp_prompts)

                    # Remove .github and recreate
                    shutil.rmtree(github_dest)
                    shutil.copytree(github_source, github_dest,
                                  ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))

                    # Restore prompts
                    github_prompts = github_dest / "prompts"
                    if github_prompts.exists():
                        shutil.rmtree(github_prompts)
                    shutil.copytree(temp_prompts, github_prompts)
            else:
                # No existing prompts, just replace
                shutil.rmtree(github_dest)
                shutil.copytree(github_source, github_dest,
                              ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        else:
            shutil.copytree(github_source, github_dest,
                          ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))

        stats["dirs"] += 1
        stats["files"] += sum(1 for _ in github_dest.rglob('*') if _.is_file())

    # Now copy prompts from prompts/ to .github/prompts/
    prompts_source = toolkit_root / "prompts"
    github_prompts_dest = project_path / ".github" / "prompts"

    if prompts_source.exists():
        # Create .github/prompts/ if it doesn't exist
        github_prompts_dest.mkdir(parents=True, exist_ok=True)

        # Copy each .prompt.md file
        for prompt_file in prompts_source.glob("*.prompt.md"):
            dest_file = github_prompts_dest / prompt_file.name
            shutil.copy2(prompt_file, dest_file)
            stats["files"] += 1

    # Copy other directories INTO forge-sdd/ to centralize toolkit
    # Note: prompts/ are already copied to .github/prompts/ above (GitHub Copilot integration)
    # No need to duplicate them in project root
    
    # Create forge-sdd/ directory
    forge_sdd_dir = project_path / "forge-sdd"
    forge_sdd_dir.mkdir(exist_ok=True)
    stats["dirs"] += 1
    
    other_dirs = [
        ("scripts", "scripts"),
        ("templates", "templates"),
    ]

    for source_name, dest_name in other_dirs:
        source = toolkit_root / source_name
        dest = forge_sdd_dir / dest_name  # Now inside forge-sdd/

        if source.exists():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(source, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
            stats["dirs"] += 1
            stats["files"] += sum(1 for _ in dest.rglob('*') if _.is_file())

    return stats


def create_forge_specs_dir(project_path: Path) -> None:
    """Create forge-sdd/specs/ directory for specifications"""
    specs_dir = project_path / "forge-sdd" / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    (specs_dir / ".gitkeep").touch()


def create_readme_guide(project_path: Path) -> None:
    """Create README-FORGE-SDD.md with usage guide"""
    readme_content = """# Forge SDD Toolkit - Guia de Uso

Este projeto agora está configurado com o **Forge SDD Toolkit** para desenvolvimento orientado por especificações.

## 🚀 Como Usar

### Com GitHub Copilot (Recomendado)

Use os **slash commands** no GitHub Copilot Chat:

#### 1. Criar Especificação (IDEATE)
```
/forge-ideate criar um painel lateral para exibir histórico de mudanças em issues
```

**Output:** Cria especificação em `forge-sdd/specs/001-feature-name/`

#### 2. Criar Plano Técnico (PLAN)
```
/forge-plan
```

**Output:** Cria plano de implementação

#### 3. Implementar Código (IMPLEMENT)
```
/forge-implement
```

**Output:** Implementa código seguindo o plano

#### 4. Testar (TEST)
```
/forge-test
```

**Output:** Valida e testa a implementação

### Sem GitHub Copilot

Use os scripts bash diretamente:

```bash
# Criar nova feature
./forge-sdd/scripts/bash/create-new-feature.sh "nome da funcionalidade"

# Criar plano de implementação
./forge-sdd/scripts/bash/create-implementation-plan.sh
```

## 📂 Estrutura de Diretórios

```
seu-projeto/
├── .github/
│   ├── copilot-instructions.md    # Regras automáticas do Copilot
│   └── prompts/                   # Slash commands (GitHub Copilot)
│       ├── forge-ideate.prompt.md
│       ├── forge-plan.prompt.md
│       ├── forge-implement.prompt.md
│       └── forge-test.prompt.md
└── forge-sdd/                      # 🔧 TOOLKIT CENTRALIZADO
    ├── specs/                      # Especificações criadas
    │   └── ###-feature-name/
    │       ├── feature-spec.md
    │       ├── manifest-updates.md
    │       ├── implementation-plan.md
    │       └── test-results.md
    ├── scripts/                    # Scripts de automação
    │   └── bash/
    │       ├── create-new-feature.sh
    │       └── create-implementation-plan.sh
    └── templates/                  # Templates de documentos
        ├── ideate-template.md
        └── plan-template.md
```

**Nota:** Toda estrutura do toolkit está centralizada em `forge-sdd/` para não poluir o diretório raiz.

## 🔧 Comandos Úteis do Forge CLI

```bash
# Validar manifest e código
forge lint

# Testar localmente
forge tunnel

# Deploy
forge deploy --non-interactive -e development

# Ver logs
forge logs -e development

# Testar function
forge function invoke my-function --payload '{"key":"value"}'
```

## 📚 Documentação

- **Estruturas manifest.yml e templates:** `forge-sdd/templates/manifest-structures.md`
- **GitHub Copilot Instructions:** `.github/copilot-instructions.md`
- **Toolkit README:** Visite o repositório do toolkit

## 🎯 Workflow Recomendado

1. **Especificar** (`/forge-ideate`)
2. **Planejar** (`/forge-plan`)
3. **Implementar** (`/forge-implement`)
4. **Testar** (`/forge-test`)
5. **Deploy** (`forge deploy`)

---

**Desenvolvido com Forge SDD Toolkit** 🚀
"""

    readme_path = project_path / "README-FORGE-SDD.md"
    readme_path.write_text(readme_content, encoding="utf-8")


def make_scripts_executable(project_path: Path) -> None:
    """Make bash scripts executable"""
    scripts_dir = project_path / "forge-sdd" / "scripts" / "bash"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.sh"):
            os.chmod(script, 0o755)


@app.command()
def init(
    here: bool = typer.Option(False, "--here", help="Initialize in current directory"),
    no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
    force: bool = typer.Option(False, "--force", help="Force initialization even if not a Forge project"),
):
    """
    Initialize Forge SDD Toolkit in a Forge project

    This command will:
    1. Check if current directory is a Forge project (has manifest.yml)
    2. Copy toolkit structure (.github, scripts, templates)
    3. Create forge-specs directory
    4. Initialize git repository (optional)
    5. Create usage guide

    Examples:
        forge-sdd init --here
        forge-sdd init --here --no-git
        forge-sdd init --here --force
    """
    show_banner()

    # Determine project directory
    project_path = Path.cwd()
    project_name = project_path.name

    # Check if it's a Forge project
    if not is_forge_project(project_path) and not force:
        console.print(Panel(
            "❌ [red]Not a Forge project[/red]\n\n"
            f"Current directory: [cyan]{project_path}[/cyan]\n\n"
            "This directory doesn't have a [yellow]manifest.yml[/yellow] file.\n"
            "Please run this command in a Forge project directory.\n\n"
            "To create a new Forge app first:\n"
            "  [cyan]forge create -t <template-name> <app-name>[/cyan]\n\n"
            "Or use [yellow]--force[/yellow] to initialize anyway.",
            title="[red]Error[/red]",
            border_style="red",
            padding=(1, 2)
        ))
        raise typer.Exit(1)

    # Display setup info
    forge_status = "✅ Forge project detected" if is_forge_project(project_path) else "⚠️  Not a Forge project (--force used)"
    setup_lines = [
        "[cyan]Forge SDD Toolkit Setup[/cyan]",
        "",
        f"{'Project':<15} [green]{project_name}[/green]",
        f"{'Location':<15} [dim]{project_path}[/dim]",
        f"{'Status':<15} {forge_status}",
    ]
    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    # Check for required tools
    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print("[yellow]Git not found - will skip repository initialization[/yellow]")

    # Initialize project with progress tracking
    tracker = StepTracker("Initialize Forge SDD Toolkit")

    # Pre-add all steps
    tracker.add("toolkit", "Copy toolkit structure")
    tracker.add("specs", "Create forge-specs directory")
    tracker.add("readme", "Create usage guide")
    tracker.add("scripts", "Make scripts executable")
    tracker.add("git", "Initialize/update git repository")
    tracker.add("final", "Finalize")

    from rich.live import Live

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))

        try:
            # Copy toolkit structure
            tracker.start("toolkit")
            stats = copy_toolkit_structure(project_path, tracker)
            tracker.complete("toolkit", f"{stats['files']} files in {stats['dirs']} directories")

            # Create forge-specs directory
            tracker.start("specs")
            create_forge_specs_dir(project_path)
            tracker.complete("specs", "forge-specs/ created")

            # Create README guide
            tracker.start("readme")
            create_readme_guide(project_path)
            tracker.complete("readme", "README-FORGE-SDD.md")

            # Make scripts executable
            tracker.start("scripts")
            make_scripts_executable(project_path)
            tracker.complete("scripts", "bash scripts executable")

            # Git initialization
            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    if init_git_repo(project_path, quiet=True):
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "toolkit ready")

        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"Initialization failed: {e}", title="Failure", border_style="red"))
            raise typer.Exit(1)

    # Final static tree
    console.print(tracker.render())
    console.print("\n[bold green]Toolkit installed successfully![/bold green]")

    # Check for legacy structures from older versions
    legacy_prompts = project_path / "prompts"
    legacy_scripts = project_path / "scripts"
    legacy_templates = project_path / "templates"
    legacy_forge_specs = project_path / "forge-specs"
    
    has_legacy = any([
        legacy_prompts.exists() and (project_path / ".github" / "prompts").exists(),
        legacy_scripts.exists() and (project_path / "forge-sdd" / "scripts").exists(),
        legacy_templates.exists() and (project_path / "forge-sdd" / "templates").exists(),
        legacy_forge_specs.exists()
    ])
    
    if has_legacy:
        console.print()
        console.print(
            "[yellow]⚠️  Legacy Structure Detected[/yellow]\n"
            "[yellow]   Found old toolkit files in project root. New structure uses 'forge-sdd/' directory.[/yellow]\n"
            "[yellow]   You can safely remove these if desired:[/yellow]"
        )
        if legacy_prompts.exists():
            console.print("[yellow]   • prompts/ (now in .github/prompts/)[/yellow]")
        if legacy_scripts.exists():
            console.print("[yellow]   • scripts/ (now in forge-sdd/scripts/)[/yellow]")
        if legacy_templates.exists():
            console.print("[yellow]   • templates/ (now in forge-sdd/templates/)[/yellow]")
        if legacy_forge_specs.exists():
            console.print("[yellow]   • forge-specs/ (now in forge-sdd/specs/)[/yellow]")

    # Next steps
    steps_lines = [
        "1. Open GitHub Copilot Chat in VS Code",
        "2. Start using slash commands:",
        "   • [cyan]/forge-ideate[/cyan] - Create specification",
        "   • [cyan]/forge-plan[/cyan] - Create implementation plan",
        "   • [cyan]/forge-implement[/cyan] - Implement code",
        "   • [cyan]/forge-test[/cyan] - Test implementation",
        "",
        "3. Read the guide: [cyan]README-FORGE-SDD.md[/cyan]",
    ]

    steps_panel = Panel("\n".join(steps_lines), title="Next Steps", border_style="cyan", padding=(1, 2))
    console.print()
    console.print(steps_panel)


@app.command()
def check():
    """Check that required tools are installed"""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    tracker.add("node", "Node.js")
    tracker.add("npm", "npm package manager")
    tracker.add("forge", "Forge CLI")

    # Check each tool
    git_ok = check_tool("git")
    if git_ok:
        tracker.complete("git", "available")
    else:
        tracker.error("git", "not found")

    node_ok = check_tool("node")
    if node_ok:
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            tracker.complete("node", version)
        except:
            tracker.complete("node", "available")
    else:
        tracker.error("node", "not found")

    npm_ok = check_tool("npm")
    if npm_ok:
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            tracker.complete("npm", version)
        except:
            tracker.complete("npm", "available")
    else:
        tracker.error("npm", "not found")

    forge_ok = check_tool("forge")
    if forge_ok:
        try:
            result = subprocess.run(["forge", "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            tracker.complete("forge", version)
        except:
            tracker.complete("forge", "available")
    else:
        tracker.error("forge", "not found")

    console.print(tracker.render())
    console.print()

    if git_ok and node_ok and npm_ok and forge_ok:
        console.print("[bold green]✅ All required tools are installed![/bold green]")
    else:
        console.print("[bold yellow]⚠️  Some tools are missing:[/bold yellow]")
        if not git_ok:
            console.print("  • Install git: [cyan]https://git-scm.com/downloads[/cyan]")
        if not node_ok or not npm_ok:
            console.print("  • Install Node.js (includes npm): [cyan]https://nodejs.org/[/cyan]")
        if not forge_ok:
            console.print("  • Install Forge CLI: [cyan]npm install -g @forge/cli[/cyan]")


@app.command()
def version():
    """Show Forge SDD Toolkit version"""
    console.print(f"\n[cyan]Forge SDD Toolkit[/cyan] version [green]{VERSION}[/green]")
    console.print(f"[dim]Specification-Driven Development for Atlassian Forge[/dim]\n")


@app.command()
def help_commands():
    """Show available slash commands for GitHub Copilot"""
    show_banner()

    console.print("[bold cyan]Available Slash Commands[/bold cyan]\n")

    commands = [
        {
            "command": "/forge-ideate",
            "description": "Create feature specification",
            "example": "/forge-ideate criar um painel para exibir métricas",
            "output": "forge-specs/###-feature-name/feature-spec.md"
        },
        {
            "command": "/forge-plan",
            "description": "Create technical implementation plan",
            "example": "/forge-plan",
            "output": "forge-specs/###-feature-name/implementation-plan.md"
        },
        {
            "command": "/forge-implement",
            "description": "Implement code following the plan",
            "example": "/forge-implement",
            "output": "Code in src/"
        },
        {
            "command": "/forge-test",
            "description": "Test and validate implementation",
            "example": "/forge-test",
            "output": "forge-specs/###-feature-name/test-results.md"
        },
    ]

    for cmd in commands:
        panel_content = f"""[yellow]Example:[/yellow]
  {cmd['example']}

[yellow]Output:[/yellow]
  {cmd['output']}"""

        console.print(Panel(
            panel_content,
            title=f"[cyan]{cmd['command']}[/cyan] - {cmd['description']}",
            border_style="cyan",
            padding=(1, 2)
        ))
        console.print()


def main():
    app()


if __name__ == "__main__":
    main()