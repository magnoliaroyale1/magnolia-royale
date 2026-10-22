"""Verificações arquiteturais que não dependem de MySQL nem do Flask instalado.

Executar isoladamente: python -m pytest backend/tests/test_arquitetura_estatica.py -q
"""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'services' / 'casos_de_uso'
CONTROLLERS = ROOT / 'controllers'


def test_uma_classe_service_por_arquivo_e_um_caso_de_uso():
    files = list(CASES.rglob('*_service.py'))
    assert len(files) >= 20
    for path in files:
        tree = ast.parse(path.read_text(encoding='utf-8'))
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        assert len(classes) == 1, str(path)
        public_methods = [node.name for node in classes[0].body if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')]
        assert public_methods == ['executar'], (str(path), public_methods)


def test_controllers_apenas_despacham_servicos_sem_sql():
    files = list(CONTROLLERS.glob('*_controller.py'))
    assert len(files) >= 8
    for path in files:
        source = path.read_text(encoding='utf-8')
        assert 'db.session.execute(' not in source
        assert '.query.' not in source
        tree = ast.parse(source)
        assert all(node.bases for node in tree.body if isinstance(node, ast.ClassDef))


def test_models_disponibilizam_crud_da_rubrica():
    tree = ast.parse((ROOT / 'models' / 'base.py').read_text(encoding='utf-8'))
    crud = next(cls for cls in tree.body if isinstance(cls, ast.ClassDef) and cls.name == 'CrudModel')
    assert {'salvar','atualizar','deletar','listar_todos','buscar_por_id'} <= {n.name for n in crud.body if isinstance(n, ast.FunctionDef)}
    assert any(isinstance(base, ast.Attribute) and base.attr == 'Model' for base in crud.bases)


def test_controllers_referenciam_apenas_imports_existentes_de_casos_de_uso():
    prefix = 'backend.services.casos_de_uso.'
    for controller in CONTROLLERS.glob('*_controller.py'):
        tree = ast.parse(controller.read_text(encoding='utf8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith(prefix):
                file = CASES.joinpath(*node.module[len(prefix):].split('.')).with_suffix('.py')
                assert file.is_file(), (controller, file)
                for alias in node.names:
                    assert re.search(r'\bclass\s+'+re.escape(alias.name)+r'\b',file.read_text()),(file,alias.name)


def test_readme_lista_20_funcionalidades():
    t=(ROOT.parent/'README.md').read_text(encoding='utf8')
    part=t.split('## Funcionalidades Implementadas',1)[1].split('### Organização',1)[0]
    found=[line for line in part.splitlines() if re.match(r'^\d+\. \*\*',line)]
    assert len(found)==20, len(found)
