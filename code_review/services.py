import subprocess

from code_review.utils import CustomDict


class LintersService:
    _linters = [
        # 'pylint',
        'flake8',
        'bandit',
    ]
    _formats_commands = {
        'flake8': ['--format={template}'],
        'bandit': ['--format', 'custom', '--msg-template', '{template}']
    }
    _formats_templates = {
        'flake8': '"{filename}:%(row)d:%(col)d: %(code)s[flake8] %(text)s"',
        'bandit': '"{filename}:{line}: {test_id}[bandit]: {severity}: {msg}"',
    }

    @classmethod
    def check_files(cls, files):
        results = []

        for linter in cls._linters:
            for file in files:
                template = cls._get_format(linter, file.name)
                linter_result = subprocess.run(
                    [linter, file.file.path, *template],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

                results.append({
                    'log_text': str(linter_result.stdout),
                    'file_id': file.pk,
                    'user_id': file.user_id,
                    'linter': linter
                })

        return results

    @classmethod
    def _get_format(cls, linter, filename):
        # returned format template commands list
        format_command = cls._formats_commands.get(linter, '')
        format_template = cls._formats_templates.get(linter, '')
        if not format_template or not format_command:
            raise KeyError(f'Key {linter} not found')

        format_template = format_template.format_map(CustomDict(filename=filename))
        result = [
            command.format(template=format_template) for command in format_command
        ]

        return result
