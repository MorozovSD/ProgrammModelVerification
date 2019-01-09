import re


class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return '\n'.join(st)

    def __repr__(self):
        s = self.parts_str().replace('\n', '\n\t')
        return str(self.type) + '\n\t' + re.sub(r'^', '', s)

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts