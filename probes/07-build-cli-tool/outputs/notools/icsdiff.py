#!/usr/bin/env python3
"""icsdiff: diff two iCalendar files and print what changed.

Usage: python icsdiff.py OLD.ics NEW.ics

Exit status: 0 no differences, 1 differences found, 2 parse/read error.
"""
import re
import sys
from datetime import date, datetime, timedelta


class ParseError(Exception):
    pass


# ---------------------------------------------------------------------------
# Low-level iCalendar syntax
# ---------------------------------------------------------------------------

def unfold(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    for line in lines:
        if line[:1] in (" ", "\t") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return [l for l in out if l.strip() != ""]


def split_unquoted(s, sep):
    parts, cur, quoted = [], [], False
    for c in s:
        if c == '"':
            quoted = not quoted
            cur.append(c)
        elif c == sep and not quoted:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    parts.append("".join(cur))
    return parts


def parse_line(line):
    """Split a content line into (NAME, {PARAM: [values]}, value)."""
    quoted = False
    idx = -1
    for i, c in enumerate(line):
        if c == '"':
            quoted = not quoted
        elif c == ":" and not quoted:
            idx = i
            break
    if idx < 0:
        raise ParseError(f"missing ':' in content line: {line!r}")
    head, value = line[:idx], line[idx + 1:]
    parts = split_unquoted(head, ";")
    name = parts[0].strip().upper()
    if not name or not re.fullmatch(r"[A-Za-z0-9-]+", name):
        raise ParseError(f"bad property name in content line: {line!r}")
    params = {}
    for p in parts[1:]:
        if "=" not in p:
            raise ParseError(f"bad parameter {p!r} in content line: {line!r}")
        k, v = p.split("=", 1)
        vals = [x.strip().strip('"') for x in split_unquoted(v, ",")]
        params[k.strip().upper()] = vals
    return name, params, value


def unescape_text(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt in ("n", "N"):
                out.append("\n")
            elif nxt in (",", ";", "\\"):
                out.append(nxt)
            else:
                out.append(c)
                out.append(nxt)
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


# ---------------------------------------------------------------------------
# Date/time values
# ---------------------------------------------------------------------------

class TimeValue:
    __slots__ = ("dt", "all_day", "utc", "tzid")

    def __init__(self, dt, all_day, utc, tzid):
        self.dt = dt
        self.all_day = all_day
        self.utc = utc
        self.tzid = tzid

    def fmt(self):
        if self.all_day:
            return self.dt.strftime("%Y-%m-%d")
        return self.dt.strftime("%Y-%m-%d %H:%M")

    def sort_key(self):
        d = self.dt
        if self.all_day:
            return (d.year, d.month, d.day, 0, 0, 0)
        return (d.year, d.month, d.day, d.hour, d.minute, d.second)

    def cmp_key(self):
        return (self.all_day, self.dt, self.utc, self.tzid)


def parse_time(value, params, prop):
    v = value.strip()
    tzid = params.get("TZID", [None])[0]
    vtype = params.get("VALUE", [None])[0]
    if vtype is not None:
        vtype = vtype.upper()
    if vtype == "DATE" or (vtype is None and len(v) == 8 and v.isdigit()):
        try:
            d = datetime.strptime(v, "%Y%m%d").date()
        except ValueError:
            raise ParseError(f"bad DATE value in {prop}: {value!r}")
        return TimeValue(d, True, False, None)
    if vtype not in (None, "DATE-TIME"):
        raise ParseError(f"unsupported VALUE={vtype} in {prop}")
    utc = v.endswith("Z") or v.endswith("z")
    core = v[:-1] if utc else v
    dt = None
    for f in ("%Y%m%dT%H%M%S", "%Y%m%dT%H%M"):
        try:
            dt = datetime.strptime(core, f)
            break
        except ValueError:
            continue
    if dt is None:
        raise ParseError(f"bad DATE-TIME value in {prop}: {value!r}")
    return TimeValue(dt, False, utc, None if utc else tzid)


_DUR_RE = re.compile(
    r"([+-])?P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?"
)


def parse_duration(value):
    v = value.strip()
    m = _DUR_RE.fullmatch(v)
    if not m or not any(m.groups()[1:]):
        raise ParseError(f"bad DURATION value: {value!r}")
    sign, w, d, h, mi, s = m.groups()
    td = timedelta(
        weeks=int(w or 0), days=int(d or 0), hours=int(h or 0),
        minutes=int(mi or 0), seconds=int(s or 0),
    )
    return -td if sign == "-" else td


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class Event:
    __slots__ = ("uid", "rid", "start", "end", "summary", "location")

    def __init__(self, uid, rid, start, end, summary, location):
        self.uid = uid
        self.rid = rid
        self.start = start
        self.end = end
        self.summary = summary
        self.location = location

    def key(self):
        return (self.uid, self.rid)

    def sort_key(self):
        sk = self.start.sort_key() if self.start is not None else (0, 0, 0, 0, 0, 0)
        return (sk, self.summary, self.uid, self.rid or "")

    def header(self):
        return f"{fmt_opt(self.start)} {self.summary}".rstrip()


def fmt_opt(tv):
    return tv.fmt() if tv is not None else "(none)"


def build_event(props):
    first = {}
    for name, params, value in props:
        first.setdefault(name, (params, value))
    if "UID" not in first:
        raise ParseError("VEVENT without UID")
    uid = first["UID"][1].strip()
    if not uid:
        raise ParseError("VEVENT with empty UID")

    rid = None
    if "RECURRENCE-ID" in first:
        p, v = first["RECURRENCE-ID"]
        tv = parse_time(v, p, "RECURRENCE-ID")
        rid = tv.fmt() + ("Z" if tv.utc else "")

    start = end = None
    if "DTSTART" in first:
        p, v = first["DTSTART"]
        start = parse_time(v, p, "DTSTART")
    if "DTEND" in first:
        p, v = first["DTEND"]
        end = parse_time(v, p, "DTEND")
    elif "DURATION" in first and start is not None:
        dur = parse_duration(first["DURATION"][1])
        if start.all_day:
            end = TimeValue(start.dt + timedelta(days=dur.days), True, False, None)
        else:
            end = TimeValue(start.dt + dur, False, start.utc, start.tzid)

    summary = unescape_text(first.get("SUMMARY", ({}, ""))[1]).strip()
    location = unescape_text(first.get("LOCATION", ({}, ""))[1]).strip()
    return Event(uid, rid, start, end, summary, location)


def parse_events(text):
    lines = unfold(text)
    events = []
    stack = []
    cur = None
    saw_calendar = False
    for line in lines:
        name, params, value = parse_line(line)
        if name == "BEGIN":
            comp = value.strip().upper()
            if not comp:
                raise ParseError("BEGIN without component name")
            if comp == "VCALENDAR":
                saw_calendar = True
            if comp == "VEVENT":
                if cur is not None:
                    raise ParseError("nested VEVENT")
                cur = []
            stack.append(comp)
            continue
        if name == "END":
            comp = value.strip().upper()
            if not stack or stack[-1] != comp:
                raise ParseError(f"unexpected END:{comp}")
            stack.pop()
            if comp == "VEVENT":
                events.append(build_event(cur))
                cur = None
            continue
        if cur is not None and stack and stack[-1] == "VEVENT":
            cur.append((name, params, value))
    if stack:
        raise ParseError(f"unterminated BEGIN:{stack[-1]}")
    if not saw_calendar:
        raise ParseError("no VCALENDAR component found")
    return events


def load(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise ParseError(f"{path}: {e}")
    try:
        events = parse_events(text)
    except ParseError as e:
        raise ParseError(f"{path}: {e}")
    result = {}
    for ev in events:
        result[ev.key()] = ev
    return result


# ---------------------------------------------------------------------------
# Diff
# ---------------------------------------------------------------------------

def time_cmp(tv):
    return None if tv is None else tv.cmp_key()


def diff_event(old, new):
    changes = []
    if time_cmp(old.start) != time_cmp(new.start):
        changes.append(("start", fmt_opt(old.start), fmt_opt(new.start)))
    if time_cmp(old.end) != time_cmp(new.end):
        changes.append(("end", fmt_opt(old.end), fmt_opt(new.end)))
    if old.summary != new.summary:
        changes.append(("summary", old.summary, new.summary))
    if old.location != new.location:
        changes.append(("location", old.location, new.location))
    return changes


def main(argv):
    if len(argv) != 3:
        print("usage: python icsdiff.py OLD.ics NEW.ics", file=sys.stderr)
        return 2
    try:
        old = load(argv[1])
        new = load(argv[2])
    except ParseError as e:
        print(f"icsdiff: {e}", file=sys.stderr)
        return 2

    added = sorted((new[k] for k in new if k not in old), key=Event.sort_key)
    removed = sorted((old[k] for k in old if k not in new), key=Event.sort_key)
    changed = []
    for k, ev in old.items():
        if k in new:
            ch = diff_event(ev, new[k])
            if ch:
                changed.append((ev, ch))
    changed.sort(key=lambda item: item[0].sort_key())

    out = []
    if added:
        out.append("ADDED")
        for ev in added:
            out.append(f"  {ev.header()}")
    if removed:
        out.append("REMOVED")
        for ev in removed:
            out.append(f"  {ev.header()}")
    if changed:
        out.append("CHANGED")
        for ev, ch in changed:
            out.append(f"  {ev.header()}")
            for field, a, b in ch:
                out.append(f"    {field}: {a} -> {b}")

    if not out:
        return 0
    sys.stdout.write("\n".join(out) + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
