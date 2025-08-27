import re
import json

class Prompt:
    @staticmethod
    def parse_structured_prompts_file(filepath):
        """
        Reads a file containing multiple structured prompts and parses each into a JSON object.
        Prompts are separated by two or more newlines.
        Returns a list of dictionaries (one per prompt).
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Split prompts by 10 or more newlines
        prompt_blocks = re.split(r'\n\s*\n{10,}', content.strip())
        parsed_prompts = []
        for block in prompt_blocks:
            parsed = Prompt.parse_structured_prompt(block)
            parsed_prompts.append(parsed)
        return parsed_prompts

    @staticmethod
    def parse_structured_prompt(text):
        """
        Parses a structured prompt in YAML-like format into a Python dictionary.
        Handles multi-line fields, lists, and simple key-value pairs.
        """
        result = {}
        lines = text.splitlines()
        key = None
        collecting_multiline = False
        multiline_value = []
        for line in lines:
            # Match key: value or key: |
            m = re.match(r'^(\w+):(?:\s*(\|)?)\s*(.*)$', line)
            if m:
                if collecting_multiline and key:
                    result[key] = '\n'.join(multiline_value).rstrip()
                    collecting_multiline = False
                    multiline_value = []
                key, pipe, value = m.groups()
                if pipe == '|':
                    collecting_multiline = True
                    multiline_value = []
                elif value == '':
                    result[key] = None
                else:
                    result[key] = value
            elif collecting_multiline:
                # Remove leading spaces (YAML style)
                multiline_value.append(line[2:] if line.startswith('  ') else line)
            elif line.strip().startswith('- ') and key:
                # List item
                if not isinstance(result.get(key), list):
                    result[key] = []
                result[key].append(line.strip()[2:])
        if collecting_multiline and key:
            result[key] = '\n'.join(multiline_value).rstrip()
        return result

if __name__ == "__main__":
    # Example usage
    file_path = "d:\\Learning\\codegen2\\prompts.txt"
    parsed_prompts = Prompt.parse_structured_prompts_file(file_path)
    for prompt in parsed_prompts:
        prompt_json = json.dumps(prompt)
        print(json.loads(prompt_json).get("prompt"))