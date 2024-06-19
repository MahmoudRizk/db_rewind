class ConfigLine:
    def __init__(self, line: str):
        self.original_line = line
        self.line = line

    def get(self) -> str:
        return self.line

    def get_directive_name(self) -> str:
        split_line = self.line.split()
        directive_name = split_line and split_line[0] or ''
        return directive_name[1:] if directive_name.startswith('#') else directive_name

    def enable_directive(self) -> "ConfigLine":
        self.line = self.line[1:] if self.line.startswith('#') else self.line
        return self

    def disable_directive(self) -> "ConfigLine":
        self.line = self.line if self.line.startswith('#') else '#' + self.line
        return self

    def set_directive_value(self, value: any, use_single_quotation: bool) -> "ConfigLine":
        directive_name: str = self.get_directive_name()
        if directive_name:
            _line = f"{directive_name} = " + self._parse_set_directive_value(value, use_single_quotation)
            self.line = self._append_comment_if_any(_line, self._get_line_comment())
        return self
    
    def add_line_break(self) -> None:
        self.line = f"{self.line}\n" 

    def has_directive(self, name: str) -> bool:
        return self.get_directive_name() == name

    def _get_line_comment(self) -> str:
        # Finds second occurrence of '#', then return sub string starting from its occurrence.
        index = self.line.find('#', 1)
        
        # no comment found.
        if index == -1:
            return ''
        
        index = self._get_comment_index_prefixed_with_white_space(index)

        return self.line[index:]

    def _append_comment_if_any(self, line: str, comment: str) -> str:
        if comment:
            line += comment
        return line
    
    def _parse_set_directive_value(self, value: any, use_single_quotation: bool) -> str:
        return f"'{value}'" if use_single_quotation else f"{value}"

    def _get_comment_index_prefixed_with_white_space(self, index: int):
        prev_index = index - 1

        if prev_index >= 0 and self.line[prev_index] in {' ', '\t'}:
            return self._get_comment_index_prefixed_with_white_space(prev_index)
        
        return index
        


