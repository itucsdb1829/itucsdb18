class QueryList(list):

    def update(self, **kwargs):
        for item in self:
            item.update(**kwargs)

    def first(self):
        if self:
            return self[0]
        return None

    def last(self):
        if self:
            return self[-1]
        return None


