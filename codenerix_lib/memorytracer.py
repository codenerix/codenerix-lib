import linecache
import os
import tracemalloc

from codenerix_lib.debugger import Debugger


class MemoryTracer(Debugger):

    def memtracer_clean(self):
        tracemalloc.clear_traces()

    def memtracer_top(self, snapshot=None, key_type='lineno', limit=10, percents=(50, 10)):
        top = None
        if snapshot is None:
            snapshot = tracemalloc.take_snapshot()

        snapshot = snapshot.filter_traces((
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        ))
        top_stats = snapshot.statistics(key_type)

        self.debug("Memory Tracer top {} lines:".format(limit), color="blue")
        for index, stat in enumerate(top_stats[:limit], 1):
            if (index == 1):
                top = stat.size
                color = 'red'
            else:
                percent = stat.size / top * 100
                if percent > percents[0]:
                    color = 'red'
                elif percent > percents[1]:
                    color = 'yellow'
                else:
                    color = 'cyan'
            frame = stat.traceback[0]
            # replace "/path/to/module/file.py" with "module/file.py"
            filename = os.sep.join(frame.filename.split(os.sep)[-2:])
            self.debug("#{}: {}:{}: {:.1f} KiB".format(index, filename, frame.lineno, stat.size / 1024), color=color)
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                self.debug('    {}'.format(line), color='white')

        other = top_stats[limit:]
        if other:
            size = sum(stat.size for stat in other)
            self.debug("{} other: {:.1f} KiB".format(len(other), size / 1024), color='purple')
        total = sum(stat.size for stat in top_stats)
        self.debug("Total allocated size: {:.1f} KiB".format(total / 1024), color='green')

tracemalloc.start()
