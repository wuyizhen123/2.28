PARAMS = {'WellBore': ['id', 'coeff_friction_sliding']}


class String:
    def __init__(self, name, top, bottom, *args, method="bottom_up", **kwargs):
        """
        一个通用的井眼结构的组合 ，比如由许多个不同长度、重量、钢级组成的套管串；或者井身结构
        Parameters
        ----------
        name: str
            组合的名字
        top: float
            某段最上方，也就是最浅的测量深度
        bottom: float
            某段最下方，也就是最深的测量深度
        method: string (default: 'bottom up')
            建立井眼结构组合的方式，bottom up是从井深最深的部分开始，直到最浅的部分；up bottom 相反，从井深最浅的部分开始，直到最深处
        """
        self.name = name
        self.top = top
        self.bottom = bottom
        self.sections = {}
        self.complete = False

        assert method in {"top_down", "bottom_up"}, "Unrecognized method"  # 不用判断？
        self.method = method

    def add_section(self, **kwargs):
        if type(self).__name__ == 'WellBore':
            for param in PARAMS.get('WellBore'):
                assert param in kwargs.keys(), f"Missing parameter {param}"  # 构建井身结构时必需要管串内径（注意裸眼段只需id）、摩阻系数

        elif type(self).__name__ == 'BHA':
            kwargs['density'] = kwargs.get('density', 7.85)  # 构建套管串数据时，先预设管串重量

        if self.method == "top_down":
            self.add_section_top_down(**kwargs)  # 加载井身结构
        elif self.method == "bottom_up":
            self.add_section_bottom_up(**kwargs)  # 加载管串数据

    def add_section_top_down(self, **kwargs):
        """
        sections字典的构造，从top（浅）到down（深）直到最深处与井深相等
        """
        if bool(self.sections) is False:  # 加第一段时
            temp = 0
            top = self.top
        else:
            temp = len(self.sections)  # 加之后的段时
            top = self.sections[temp - 1]['bottom']

        self.sections[temp] = {}  # 字典sections的键是temp，值是一个空字典
        self.sections[temp]['top'] = top

        # 将输入的参数整理值字典sections的temp所指的字典内
        for k, v in kwargs.items():
            self.sections[temp][k] = v

        # 按top值整理字典顺序（因为此时没有bottom值）
        self.sections = {k: v for k, v in sorted(self.sections.items(), key=lambda item: item[1]['top'])}
        # 为什么item索引是1，因为items返回一元组，第0位是原字典键（temp），第一位是字典

        # 重排索引，因为上一步连键值以前换位
        temp = {}
        for i, (k, v) in enumerate(self.sections.items()):
            temp[i] = v

        # 核对数据是否正确合理
        for k, v in temp.items():
            if k == 0:
                assert v['top'] == self.top
            else:
                assert v['top'] == temp[k - 1]['bottom']
            assert v['bottom'] <= self.bottom

        if temp[len(temp) - 1]['bottom'] == self.bottom:  # 判断是否将井眼全部覆盖
            self.complete = True

    def add_section_bottom_up(self, **kwargs):
        if bool(self.sections) is False:
            temp = 0
            bottom = self.bottom
        else:
            temp = len(self.sections)
            bottom = self.sections[0]['top']  # 注意是自下向上

        if bool(kwargs.get('length')):
            top = bottom - kwargs.get('length')
            length = kwargs.get('length')
            if top < self.top:
                top = self.top
                length = bottom - top
        elif bool(kwargs.get('top')):
            length = bottom - kwargs.get('top')
            top = kwargs.get('top')
        else:
            top = self.top
            length = self.sections[0]['top']

        self.sections[temp] = {}
        self.sections[temp]['top'] = top
        self.sections[temp]['bottom'] = bottom
        self.sections[temp]['length'] = length

        for k, v in kwargs.items():
            self.sections[temp][k] = v

        self.sections = {k: v for k, v in sorted(self.sections.items(), key=lambda item: item[1]['bottom'])}

        temp = {}
        for i, (k, v) in enumerate(self.sections.items()):
            temp[i] = v

        number_of_sections = len(temp)
        for k, v in temp.items():
            if k == number_of_sections - 1:
                assert v['bottom'] == self.bottom
            else:
                assert v['bottom'] == temp[k + 1]['top']
            assert v['top'] >= self.top

        if temp[0]['top'] == self.top:
            self.complete = True

        self.sections = temp

    def depth(self, md):
        assert self.top < md <= self.bottom, "Depth out of range"
        string_new = String(self.name, self.top, md, method="bottom_up")
        reached_top = False
        for section in reversed(list(self.sections.keys())):
            if reached_top:
                break
            params = {k: v for k, v in self.sections[section].items()
                      if k not in ['top', 'bottom', 'length', 'buoyancy_factor']}
            string_new.add_section(length=self.sections[section]['length'], **params)
            if string_new.sections[0]['top'] == self.top:
                reached_top = True
        return string_new


class WellBore(String):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BHA(String):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
