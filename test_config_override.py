#!/usr/bin/env python3
"""
Тест работы параметра --serena-config
Проверяет, что конфигурация передаётся в SerenaMCPFactory
"""

import sys
import os

# Добавляем src в path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_serena_config_parameter():
    """Проверяем что параметр serena-config передаётся правильно"""

    # Читаем исходный код mcp.py
    mcp_path = os.path.join(os.path.dirname(__file__), 'src', 'serena', 'mcp.py')
    with open(mcp_path, 'r') as f:
        content = f.read()

    # Проверяем что SerenaMCPFactory принимает serena_config_path
    if 'def __init__(self, context: str = DEFAULT_CONTEXT, project: str | None = None, serena_config_path: str | None = None)' in content:
        print("✅ SerenaMCPFactory.__init__ принимает serena_config_path")
    else:
        print("❌ SerenaMCPFactory.__init__ НЕ принимает serena_config_path")
        return False

    # Проверяем что SerenaMCPFactorySingleProcess передаёт параметр в базовый класс
    if 'super().__init__(context=context, project=project, serena_config_path=serena_config_path)' in content:
        print("✅ SerenaMCPFactorySingleProcess передаёт serena_config_path в базовый класс")
    else:
        print("❌ SerenaMCPFactorySingleProcess НЕ передаёт serena_config_path")
        return False

    # Проверяем что в create_mcp_server используется self.serena_config_path
    if 'if self.serena_config_path:' in content and 'config = SerenaConfig.from_config_file(self.serena_config_path)' in content:
        print("✅ create_mcp_server использует self.serena_config_path для загрузки конфигурации")
    else:
        print("❌ create_mcp_server НЕ использует self.serena_config_path")
        return False

    # Проверяем cli.py
    cli_path = os.path.join(os.path.dirname(__file__), 'src', 'serena', 'cli.py')
    with open(cli_path, 'r') as f:
        cli_content = f.read()

    # Проверяем что CLI принимает --serena-config
    if '--serena-config' in cli_content and 'serena_config_path=serena_config' in cli_content:
        print("✅ CLI принимает параметр --serena-config и передаёт его в SerenaMCPFactory")
    else:
        print("❌ CLI НЕ работает с --serena-config правильно")
        return False

    # Проверяем agent.py
    agent_path = os.path.join(os.path.dirname(__file__), 'src', 'serena', 'agent.py')
    with open(agent_path, 'r') as f:
        agent_content = f.read()

    # Ищем строку с порядком применения конфигураций
    if '[self._context, self.serena_config]' in agent_content:
        print("✅ agent.py: Конфигурация применяется ПОСЛЕ контекста (правильный порядок)")
    elif '[self.serena_config, self._context]' in agent_content:
        print("❌ agent.py: Конфигурация применяется ДО контекста (неправильный порядок)")
        return False
    else:
        print("⚠️ agent.py: Не найден порядок применения конфигураций")

    print("\n✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ - параметр --serena-config должен работать!")
    return True

if __name__ == '__main__':
    success = test_serena_config_parameter()
    sys.exit(0 if success else 1)