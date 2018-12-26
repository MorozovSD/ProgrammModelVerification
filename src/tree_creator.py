from anytree import Node, RenderTree

class TreeCreator:
    parent = None
    childs = None
    pos = 0

    def __init__(self, type, text=None, child1=None, child2=None):
        self.type = type
        self.text = text
        if child1 is not None:
            self.add_child(child1)
        if child2 is not None:
            self.add_child(child2)

    def add_child(self, child):
        if child.parent is not None:
            child.parent.childs.remove(child)
        self.childs.remove(child)
        self.childs.add(child)
        child.parent = self.parent

    def remove_child(self, child):
        self.childs.remove(child)
        if child.parent == self.parent:
            child.parent = None
    
    def get_child(self, index):
        return self.childs[index]
