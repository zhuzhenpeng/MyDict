def get_trie():
    """
    生成词典树
    :return:词典树实例
    """
    trie = Trie()
    with open('./local_words', mode='r') as words:
        for word in words:
            trie.insert(word.strip())
    return trie


class Trie:
    """
    字典树
    """

    def __init__(self):
        self._root = dict()  # 每个节点都是{}类型
        self._words = set()

    def insert(self, word):
        """
        插入单词，构造词典树
        """
        self._words.add(word)
        index, node = self._find_last_node(word)
        for char in word[index:]:
            new_node = dict()
            node[char] = new_node
            node = new_node

    def get_relevant(self, prefix):
        """
        根据前缀获得相关单词集并返回
        """
        node = self._find(prefix)
        if node is None:
            return []
        else:
            result = []
            self._search_recursive(node, prefix, result)
            result = [item for item in result if item in self._words]
            if prefix in self._words:
                result.insert(0, prefix)
            return result

    def _find(self, prefix):
        """
        在词典树中根据前缀寻找,返回最后匹配的节点
        如果找不到则返回None
        """
        node = self._root
        layer = 0
        for ch in prefix:
            if ch in node:
                node = node[ch]
                layer += 1
            else:
                break
        if layer != len(prefix):
            return None
        else:
            return node

    def _search_recursive(self, node, prefix, result_set):
        """
        从某个节点开始把相关结果放入结果集中
        """
        for item in node.items():
            word = prefix + item[0]
            result_set.append(word)
            self._search_recursive(item[1], word, result_set)

    def _find_last_node(self, word):
        node = self._root
        index = 0
        while index < len(word):
            char = word[index]
            if char in node:
                node = node[char]
            else:
                break
            index += 1
        return index, node


if __name__ == '__main__':
    tree = Trie()
    with open('./local_words', mode='r') as words:
        for line in words:
            tree.insert(line.strip())
    while True:
        word = input('input a word: ')
        if word == 'q':
            break
        else:
            result = tree.get_relevant(word)
            for i in result:
                print(i, end=' ')
            print()
