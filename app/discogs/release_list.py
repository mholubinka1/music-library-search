from typing import Iterable

from discogs.model import Release


class ReleaseList(list):
    def merge_extend(self, iterable: Iterable[Release]) -> None:
        if not hasattr(iterable, "__iter__"):
            raise TypeError(f"{type(iterable).__name__} object is not iterable")
        for item in iterable:
            duplicate = False
            for r in self:
                if r.master_id == item.master_id:
                    duplicate = True
                    break
            if not duplicate:
                self.append(item)
