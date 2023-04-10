import linecache
import os
import tracemalloc

from codenerix_lib.debugger import Debugger


class MemoryTracer(Debugger):
    def memtracer_clean(self):
        tracemalloc.clear_traces()

    def memtracer_top(
        self,
        snapshot=None,
        key_type="lineno",
        limit=10,
        percents=(50, 10),
        onscreen=True,
    ):
        top = None
        answer = {
            "config": {
                "key_type": key_type,
                "limit": limit,
                "percents": percents,
            },
            "top": [],
            "other": None,
            "otherkb": None,
            "total": None,
            "totalkb": None,
        }
        if snapshot is None:
            snapshot = tracemalloc.take_snapshot()

        snapshot = snapshot.filter_traces(
            (
                tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
                tracemalloc.Filter(False, "<unknown>"),
            ),
        )
        top_stats = snapshot.statistics(key_type)

        if onscreen:  # pragma: no cover
            self.debug(
                "Memory Tracer top {} lines:".format(limit),
                color="blue",
            )
        for index, stat in enumerate(top_stats[:limit], 1):
            if index == 1:
                top = stat.size
                color = "red"
            else:
                percent = stat.size / top * 100
                if percent > percents[0]:  # pragma: no cover
                    color = "red"
                elif percent > percents[1]:  # pragma: no cover
                    color = "yellow"
                else:  # pragma: no cover
                    color = "cyan"
            frame = stat.traceback[0]
            # replace "/path/to/module/file.py" with "module/file.py"
            filename = os.sep.join(frame.filename.split(os.sep)[-2:])
            token = {
                "index": index,
                "filename": filename,
                "linenumber": frame.lineno,
                "size": stat.size,
                "sizekb": stat.size / 1024,
                "line": None,
            }
            if onscreen:  # pragma: no cover
                self.debug(
                    "#{}: {}:{}: {:.1f} KiB".format(
                        index,
                        filename,
                        frame.lineno,
                        stat.size / 1024,
                    ),
                    color=color,
                )

            # Save line
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                token["line"] = line
                if onscreen:  # pragma: no cover
                    self.debug("    {}".format(line), color="white")

            answer["top"].append(token)

        other = top_stats[limit:]
        if other:  # pragma: no cover
            size = sum(stat.size for stat in other)
            answer["other"] = size
            answer["otherkb"] = float(size) / 1024.0
            if onscreen:  # pragma: no cover
                self.debug(
                    "{} other: {:.1f} KiB".format(len(other), size / 1024),
                    color="purple",
                )
        total = sum(stat.size for stat in top_stats)
        answer["total"] = total
        answer["totalkb"] = float(total) / 1024.0
        if onscreen:  # pragma: no cover
            self.debug(
                "Total allocated size: {:.1f} KiB".format(total / 1024),
                color="green",
            )

        return answer


tracemalloc.start()
