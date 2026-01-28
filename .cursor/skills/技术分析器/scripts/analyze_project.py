#!/usr/bin/env python3
"""
项目分析器 - 自动分析开源技术并提取核心原理

用法:
    analyze_project.py --project-dir <dir> --output-dir <dir> [--project <name>]

示例:
    analyze_project.py --project-dir project/ --output-dir sumup/
    analyze_project.py --project-dir project/ --output-dir sumup/ --project clawdbot
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def count_files(project_path: Path) -> int:
    """统计项目文件数量（排除node_modules等）"""
    count = 0
    exclude_dirs = {'node_modules', '.git', 'vendor', 'dist', 'build', '.next', '__pycache__'}
    for item in project_path.rglob('*'):
        if item.is_file() and not any(excluded in item.parts for excluded in exclude_dirs):
            count += 1
    return count

def assess_complexity(project_path: Path, metadata: Dict) -> str:
    """评估项目复杂度"""
    file_count = count_files(project_path)
    dep_count = len(metadata.get('tech_stack', []))
    
    # 检查是否有扩展/插件系统
    has_extensions = (project_path / 'extensions').exists() or (project_path / 'plugins').exists()
    has_multiple_modules = (project_path / 'src').exists() and len(list((project_path / 'src').iterdir())) > 5
    
    if file_count < 100 and dep_count < 20 and not has_extensions:
        return 'simple'
    elif file_count < 500 and dep_count < 50:
        return 'medium'
    else:
        return 'complex'

def extract_readme_content(readme_path: Path) -> Dict:
    """提取README的关键内容"""
    content = {
        'description': '',
        'key_features': [],
        'architecture_hints': []
    }
    
    try:
        text = readme_path.read_text(encoding='utf-8', errors='ignore')
        lines = text.split('\n')
        
        # 提取描述（前几段非标题文本）
        description_lines = []
        for line in lines[:50]:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('[') and not line.startswith('!'):
                if len(line) > 20:  # 跳过太短的行
                    description_lines.append(line)
                    if len(description_lines) >= 3:
                        break
        content['description'] = ' '.join(description_lines)[:300]
        
        # 查找关键特性（## Features, ## Highlights等章节）
        in_features = False
        for line in lines:
            if re.match(r'^##+\s*(Features?|Highlights?|特性|特点)', line, re.I):
                in_features = True
                continue
            if in_features and line.startswith('##'):
                break
            if in_features and line.strip().startswith('-'):
                feature = line.strip().lstrip('- ').strip()
                if feature:
                    content['key_features'].append(feature)
                    if len(content['key_features']) >= 5:
                        break
        
        # 查找架构提示（Architecture, How it works等）
        arch_keywords = ['architecture', 'how it works', '架构', '工作原理']
        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in arch_keywords):
                # 提取接下来的几行
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        content['architecture_hints'].append(lines[j].strip())
                        if len(content['architecture_hints']) >= 3:
                            break
                break
    except Exception:
        pass
    
    return content

def extract_architecture_patterns(project_path: Path, metadata: Dict) -> List[str]:
    """提取架构模式"""
    patterns = []
    
    # 检查常见架构模式
    if (project_path / 'extensions').exists() or (project_path / 'plugins').exists():
        patterns.append('插件/扩展系统')
    
    if (project_path / 'gateway').exists() or 'gateway' in str(project_path).lower():
        patterns.append('网关模式')
    
    if (project_path / 'src' / 'channels').exists() or 'channel' in str(project_path).lower():
        patterns.append('多通道架构')
    
    # 检查package.json中的架构提示
    package_json = project_path / 'package.json'
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text())
            if 'workspaces' in data:
                patterns.append('工作区/多包架构')
        except Exception:
            pass
    
    return patterns

def extract_core_principles(project_path: Path, metadata: Dict, readme_content: Dict) -> Dict:
    """提取核心原理"""
    principles = {
        'design_decisions': [],
        'key_abstractions': [],
        'architectural_patterns': extract_architecture_patterns(project_path, metadata),
        'tech_choices': []
    }
    
    # 从README提取设计决策
    if readme_content.get('description'):
        # 查找设计相关的关键词
        desc = readme_content['description'].lower()
        if 'local' in desc or '本地' in desc:
            principles['design_decisions'].append('本地优先设计')
        if 'personal' in desc or '个人' in desc:
            principles['design_decisions'].append('个人化/单用户设计')
        if 'gateway' in desc or '网关' in desc:
            principles['design_decisions'].append('网关控制平面架构')
    
    # 从关键文件提取
    agents_md = project_path / 'AGENTS.md'
    if agents_md.exists():
        try:
            content = agents_md.read_text(encoding='utf-8', errors='ignore')
            if 'workspace' in content.lower():
                principles['key_abstractions'].append('工作区抽象')
            if 'skill' in content.lower():
                principles['key_abstractions'].append('技能系统')
        except Exception:
            pass
    
    # 从技术栈推断技术选型
    tech_stack = metadata.get('tech_stack', [])
    if '@agentclientprotocol' in str(tech_stack):
        principles['tech_choices'].append('Agent Client Protocol (标准化Agent通信)')
    if 'typescript' in str(tech_stack) or 'tsconfig.json' in str(project_path):
        principles['tech_choices'].append('TypeScript (类型安全)')
    
    return principles

def extract_latest_updates(project_path: Path) -> List[str]:
    """提取最新更新"""
    updates = []
    
    changelog = project_path / 'CHANGELOG.md'
    if changelog.exists():
        try:
            content = changelog.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            # 提取前几个版本的关键更新
            for i, line in enumerate(lines[:100]):
                if re.match(r'^##+\s*v?\d+', line):
                    # 找到版本号，提取接下来的更新项
                    for j in range(i+1, min(i+20, len(lines))):
                        if lines[j].strip().startswith('-') or lines[j].strip().startswith('*'):
                            update = lines[j].strip().lstrip('-* ').strip()
                            if update and len(update) > 10:
                                updates.append(update)
                                if len(updates) >= 5:
                                    break
                    if updates:
                        break
        except Exception:
            pass
    
    return updates

def get_project_output_dir(output_dir: Path, project_name: str) -> Path:
    """返回该项目对应的输出子文件夹（文件夹名与项目名相同）"""
    return output_dir / project_name


def generate_core_principles_doc(project_metadata: Dict, principles: Dict, readme_content: Dict, output_dir: Path):
    """生成核心原理文档。output_dir 应为 sumup/<项目名>/"""
    project_name = project_metadata['name']
    
    content = f"""# {project_name} - 核心技术原理

## 概述

{readme_content.get('description', project_metadata.get('description', '项目描述待补充'))}

**项目类型**: {project_metadata.get('type', 'unknown').upper()}
**技术栈**: {', '.join(project_metadata.get('tech_stack', [])[:10]) if project_metadata.get('tech_stack') else '待分析'}

## 核心设计原则

"""
    
    if principles.get('design_decisions'):
        for i, decision in enumerate(principles['design_decisions'], 1):
            content += f"{i}. **{decision}**: 核心设计决策之一\n"
    else:
        content += "（待深入分析核心设计决策）\n"
    
    content += "\n## 关键抽象\n\n"
    if principles.get('key_abstractions'):
        for abstraction in principles['key_abstractions']:
            content += f"- **{abstraction}**: 系统核心抽象\n"
    else:
        content += "（待识别关键抽象）\n"
    
    content += "\n## 架构模式\n\n"
    if principles.get('architectural_patterns'):
        for pattern in principles['architectural_patterns']:
            content += f"- **{pattern}**: 采用的架构模式\n"
    else:
        content += "（待识别架构模式）\n"
    
    content += "\n## 技术选型\n\n"
    if principles.get('tech_choices'):
        for choice in principles['tech_choices']:
            content += f"- {choice}\n"
    else:
        content += f"- 主要技术: {', '.join(project_metadata.get('tech_stack', [])[:5]) if project_metadata.get('tech_stack') else '待分析'}\n"
    
    updates = extract_latest_updates(Path(project_metadata['path']))
    if updates:
        content += "\n## 最新技术更新\n\n"
        for update in updates:
            content += f"- {update}\n"
    
    content += "\n---\n*由技术分析器自动生成。建议进一步审查源代码和文档以完善分析。*\n"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "核心技术原理.md"
    output_file.write_text(content, encoding='utf-8')
    print(f"[OK] 生成 {output_file.relative_to(output_dir.parent)}")

def generate_architecture_doc(project_metadata: Dict, principles: Dict, output_dir: Path):
    """生成架构文档。output_dir 应为 sumup/<项目名>/"""
    project_name = project_metadata['name']
    
    content = f"""# {project_name} - 架构设计

## 系统架构

（待深入分析系统整体架构）

## 组件概述

"""
    
    project_path = Path(project_metadata['path'])
    
    # 识别主要组件
    if (project_path / 'src').exists():
        content += "- **src/**: 核心源代码\n"
    if (project_path / 'extensions').exists():
        content += "- **extensions/**: 扩展/插件系统\n"
    if (project_path / 'gateway').exists():
        content += "- **gateway/**: 网关组件\n"
    if (project_path / 'docs').exists():
        content += "- **docs/**: 文档和架构说明\n"
    
    content += """
## 数据流

（待分析数据如何在系统中流动）

## 扩展点

"""
    
    if principles.get('architectural_patterns') and any('插件' in p or '扩展' in p for p in principles['architectural_patterns']):
        content += "系统支持通过扩展/插件机制进行扩展。\n"
    else:
        content += "（待分析扩展机制）\n"
    
    content += """
## 通信模式

（待分析组件间通信方式）

---
*由技术分析器自动生成。建议进一步审查源代码和文档以完善分析。*
"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "架构设计.md"
    output_file.write_text(content, encoding='utf-8')
    print(f"[OK] 生成 {output_file.relative_to(output_dir.parent)}")

def generate_implementation_doc(project_metadata: Dict, output_dir: Path):
    """生成实现细节文档。output_dir 应为 sumup/<项目名>/"""
    project_name = project_metadata['name']
    
    content = f"""# {project_name} - 实现细节

## 技术栈

{', '.join(project_metadata.get('tech_stack', [])[:20]) if project_metadata.get('tech_stack') else '待分析'}

## 关键依赖

"""
    
    tech_stack = project_metadata.get('tech_stack', [])
    if tech_stack:
        for dep in tech_stack[:15]:
            content += f"- {dep}\n"
    else:
        content += "（待分析）\n"
    
    content += """
## 实现模式

（待分析使用的编码模式和设计模式）

## 构建和部署

（待分析构建和部署流程）

## 配置

（待分析配置机制和选项）

---
*由技术分析器自动生成。建议进一步审查源代码和文档以完善分析。*
"""
    
    output_file = output_dir / f"{safe_name}-实现细节.md"
    output_file.write_text(content, encoding='utf-8')
    print(f"[OK] 生成 {output_file.name}")

def analyze_project(project_dir: Path, output_dir: Path, project_name: Optional[str] = None):
    """主分析函数"""
    print(f"分析项目目录: {project_dir}")
    print(f"输出目录: {output_dir}\n")
    
    if project_name:
        project_path = project_dir / project_name
        if not project_path.exists():
            print(f"[错误] 项目不存在: {project_path}")
            sys.exit(1)
        projects = [project_path]
    else:
        projects = find_projects(project_dir)
        if not projects:
            print(f"[警告] 在 {project_dir} 中未找到项目")
            return
    
    print(f"发现 {len(projects)} 个项目:\n")
    
    for project_path in projects:
        print(f"分析: {project_path.name}")
        metadata = extract_project_metadata(project_path)
        complexity = assess_complexity(project_path, metadata)
        
        print(f"  类型: {metadata['type']}")
        print(f"  复杂度: {complexity}")
        print(f"  有README: {metadata['has_readme']}")
        print(f"  有文档: {metadata['has_docs']}")
        if metadata['tech_stack']:
            print(f"  技术栈: {', '.join(metadata['tech_stack'][:5])}...")
        print()
        
        # 提取内容
        readme_path = project_path / 'README.md'
        readme_content = extract_readme_content(readme_path) if readme_path.exists() else {}
        principles = extract_core_principles(project_path, metadata, readme_content)
        
        # 根据复杂度生成文档
        generate_core_principles_doc(metadata, principles, readme_content, output_dir)
        
        if complexity in ['medium', 'complex']:
            generate_architecture_doc(metadata, principles, output_dir)
        
        if complexity == 'complex':
            generate_implementation_doc(metadata, output_dir)
        
        print()

def find_projects(project_dir: Path) -> List[Path]:
    """发现目录中的项目"""
    projects = []
    if not project_dir.exists():
        return projects
    
    for item in project_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            indicators = ['README.md', 'package.json', 'requirements.txt', 'Cargo.toml', 'go.mod', 'pom.xml']
            if any((item / indicator).exists() for indicator in indicators):
                projects.append(item)
    
    return projects

def extract_project_metadata(project_path: Path) -> Dict:
    """提取项目基本元数据"""
    metadata = {
        'name': project_path.name,
        'path': str(project_path),
        'type': 'unknown',
        'description': '',
        'tech_stack': [],
        'has_readme': False,
        'has_docs': False,
    }
    
    readme_path = project_path / 'README.md'
    if readme_path.exists():
        metadata['has_readme'] = True
        try:
            content = readme_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            for line in lines[:20]:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('['):
                    metadata['description'] = line[:200]
                    break
        except Exception:
            pass
    
    package_json = project_path / 'package.json'
    if package_json.exists():
        metadata['type'] = 'nodejs'
        try:
            data = json.loads(package_json.read_text())
            if 'dependencies' in data:
                metadata['tech_stack'].extend(list(data['dependencies'].keys())[:20])
            if 'devDependencies' in data:
                metadata['tech_stack'].extend(list(data['devDependencies'].keys())[:10])
        except Exception:
            pass
    
    requirements = project_path / 'requirements.txt'
    if requirements.exists() and metadata['type'] == 'unknown':
        metadata['type'] = 'python'
    
    if (project_path / 'docs').exists():
        metadata['has_docs'] = True
    
    return metadata

def main():
    parser = argparse.ArgumentParser(description="分析开源技术并提取核心原理")
    parser.add_argument("--project-dir", required=True, help="包含项目的目录")
    parser.add_argument("--output-dir", required=True, help="输出文档的目录")
    parser.add_argument("--project", help="要分析的特定项目名称（可选，未指定则分析所有）")
    args = parser.parse_args()
    
    project_dir = Path(args.project_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    
    if not project_dir.exists():
        print(f"[错误] 项目目录不存在: {project_dir}")
        sys.exit(1)
    
    analyze_project(project_dir, output_dir, args.project)

if __name__ == "__main__":
    main()
