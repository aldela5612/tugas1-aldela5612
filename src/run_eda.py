"""Execute EDA cells and store text/rich outputs without starting a Jupyter server."""
from pathlib import Path

import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
from traitlets.config import Config


def main():
    root = Path(__file__).resolve().parents[1]
    path = root / 'notebooks/03_eda_and_insights.ipynb'
    nb = nbformat.read(path, as_version=4)
    config = Config()
    config.HistoryManager.hist_file = ':memory:'
    InteractiveShell.instance(config=config)
    namespace = {'__name__': '__main__'}
    for count, cell in enumerate((c for c in nb.cells if c.cell_type == 'code'), 1):
        print(f'Executing cell {count}', flush=True)
        cell.execution_count = count
        with capture_output() as captured:
            exec(compile(cell.source, str(path), 'exec'), namespace)
        cell.outputs = []
        if captured.stdout:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
        if captured.stderr:
            cell.outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
        for output in captured.outputs:
            cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
    nbformat.validate(nb)
    nbformat.write(nb, path)
    print('All EDA cells completed and outputs saved.', flush=True)


if __name__ == '__main__':
    main()
