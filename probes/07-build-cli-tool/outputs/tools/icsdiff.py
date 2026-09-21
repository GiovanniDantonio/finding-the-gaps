#!/usr/bin/env python3
"""Diff two iCalendar files and print what changed.

Usage: python icsdiff.py OLD.ics NEW.ics
"""
import re
import sys
from datetime import date, datetime, timedelta

FIELDS = ("start", "end", "summary", "location")

DURATION_RE = re.compile(
    r"^([+-])?P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$"
)


class ParseError(Exception):
    pass


class Time:
    """A wall-clock time as written in the file (no conversion)."""

    def __init__(self, value, tz):
        self.value = value  # date or naive datetime
        self.tz = tz  # None (floating), "UTC", or a TZID string

    def key(self):
        v = self.value
        if isinstance(v, datetime):
            return (v.date(), v.time())
        return (v, None)

    def __eq__(self, other):
        return isinstance(other, Time) and (self.value, self.tz) == (other.value, other.tz)

    def __hash__(self):
        return hash((self.value, self.tz))

    def text(self, with_tz=False):
        v = self.value
        if isinstance(v, datetime):
            s = v.strftime("%Y-%m-%d %H:%M")
        else:
            s = v.strftime("%Y-%m-%d")
        if with_tz and self.tz:
            s += " " + self.tz
        return s


def unfold(raw):
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    for line in lines:
        if line == "":
            continue
        if line[0] in " \t":
            if not out:
                raise ParseError("continuation line with nothing to continue")
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def parse_line(line):
    """Return (name, params, value) for one content line."""
    i = 0
    n = len(line)
    in_quotes = False
    while i < n:
        c = line[i]
        if c == '"':
            in_quotes = not in_quotes
        elif c == ":" and not in_quotes:
            break
        i += 1
    if i >= n:
        raise ParseError("malformed content line: %r" % line)
    head, value = line[:i], line[i + 1:]
    parts = []
    cur = ""
    in_quotes = False
    for c in head:
        if c == '"':
            in_quotes = not in_quotes
        elif c == ";" and not in_quotes:
            parts.append(cur)
            cur = ""
            continue
        cur += c
    parts.append(cur)
    name = parts[0].strip().upper()
    if not name:
        raise ParseError("malformed content line: %r" % line)
    params = {}
    for p in parts[1:]:
        if "=" not in p:
            raise ParseError("malformed parameter %r in line %r" % (p, line))
        k, v = p.split("=", 1)
        params[k.strip().upper()] = v.strip().strip('"')
    return name, params, value


def unescape_text(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt in "nN":
                out.append("\n")
            elif nxt in "\\,;":
                out.append(nxt)
            else:
                out.append(nxt)
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def parse_time(params, value, prop):
    value = value.strip()
    tzid = params.get("TZID")
    vtype = params.get("VALUE", "DATE-TIME").upper()
    try:
        if vtype == "DATE" or (len(value) == 8 and value.isdigit()):
            d = datetime.strptime(value, "%Y%m%d").date()
            return Time(d, None)
        if vtype != "DATE-TIME":
            raise ValueError("unsupported VALUE=%s" % vtype)
        utc = value.endswith("Z")
        body = value[:-1] if utc else value
        if len(body) == 15:
            dt = datetime.strptime(body, "%Y%m%dT%H%M%S")
        elif len(body) == 13:
            dt = datetime.strptime(body, "%Y%m%dT%H%M")
        else:
            raise ValueError("bad length")
        if utc:
            return Time(dt, "UTC")
        return Time(dt, tzid)
    except ValueError as e:
        raise ParseError("invalid %s value %r (%s)" % (prop, value, e))


def parse_duration(value):
    m = DURATION_RE.match(value.strip())
    if not m or value.strip() in ("P", "PT"):
        raise ParseError("invalid DURATION %r" % value)
    sign, w, d, h, mi, s = m.groups()
    td = timedelta(
        weeks=int(w or 0), days=int(d or 0), hours=int(h or 0),
        minutes=int(mi or 0), seconds=int(s or 0),
    )
    return -td if sign == "-" else td


def build_event(props):
    """props: list of (name, params, value) inside one VEVENT."""
    uid = None
    rid = None
    start = end = None
    duration = None
    summary = location = None
    for name, params, value in props:
        if name == "UID":
            uid = value.strip()
        elif name == "RECURRENCE-ID":
            rid = parse_time(params, value, name)
        elif name == "DTSTART":
            start = parse_time(params, value, name)
        elif name == "DTEND":
            end = parse_time(params, value, name)
        elif name == "DURATION":
            duration = parse_duration(value)
        elif name == "SUMMARY":
            summary = unescape_text(value)
        elif name == "LOCATION":
            location = unescape_text(value)
    if not uid:
        raise ParseError("VEVENT without UID")
    if start is None:
        raise ParseError("VEVENT %s without DTSTART" % uid)
    if end is None and duration is not None:
        v = start.value
        if isinstance(v, date) and not isinstance(v, datetime):
            end = Time(v + timedelta(days=duration.days), None)
        else:
            end = Time(v + duration, start.tz)
    key = (uid, rid.key() if rid is not None else None, rid.tz if rid is not None else None)
    return key, {"start": start, "end": end, "summary": summary, "location": location}


def parse_calendar(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            raw = f.read()
    except OSError as e:
        raise ParseError(str(e))
    except UnicodeDecodeError as e:
        raise ParseError("not valid UTF-8: %s" % e)

    lines = unfold(raw)
    if not lines:
        raise ParseError("empty file")

    events = {}
    stack = []
    current_props = None
    for line in lines:
        name, params, value = parse_line(line)
        if name == "BEGIN":
            comp = value.strip().upper()
            if not stack and comp != "VCALENDAR":
                raise ParseError("expected BEGIN:VCALENDAR, got BEGIN:%s" % comp)
            stack.append(comp)
            if comp == "VEVENT":
                if current_props is not None:
                    raise ParseError("nested VEVENT")
                current_props = []
        elif name == "END":
            comp = value.strip().upper()
            if not stack or stack[-1] != comp:
                raise ParseError("unexpected END:%s" % comp)
            stack.pop()
            if comp == "VEVENT":
                key, ev = build_event(current_props)
                events[key] = ev
                current_props = None
        else:
            if not stack:
                raise ParseError("property outside VCALENDAR: %r" % line)
            if current_props is not None and stack[-1] == "VEVENT":
                current_props.append((name, params, value))
    if stack:
        raise ParseError("unterminated component %s" % stack[-1])
    return events


def sort_key(item):
    key, ev = item
    s = ev["start"]
    d, t = s.key()
    return (d, t is not None, t or datetime.min.time(), key[0], key[1] or (date.min, None))


def header(ev):
    s = ev["start"].text()
    if ev["summary"]:
        return "  %s %s" % (s, ev["summary"].replace("\n", " "))
    return "  " + s


def fmt_field(name, value, other=None):
    if value is None:
        return "(none)"
    if name in ("start", "end"):
        with_tz = isinstance(other, Time) and other.value == value.value and other.tz != value.tz
        return value.text(with_tz)
    return value.replace("\n", " ")


def diff(old, new):
    added = [(k, v) for k, v in new.items() if k not in old]
    removed = [(k, v) for k, v in old.items() if k not in new]
    changed = []
    for k, o in old.items():
        if k not in new:
            continue
        n = new[k]
        lines = []
        for f in FIELDS:
            if o[f] != n[f]:
                lines.append("    %s: %s -> %s" % (f, fmt_field(f, o[f], n[f]), fmt_field(f, n[f], o[f])))
        if lines:
            changed.append((k, o, lines))

    out = []
    if added:
        out.append("ADDED")
        for k, v in sorted(added, key=sort_key):
            out.append(header(v))
    if removed:
        out.append("REMOVED")
        for k, v in sorted(removed, key=sort_key):
            out.append(header(v))
    if changed:
        out.append("CHANGED")
        for k, o, lines in sorted(changed, key=lambda c: sort_key((c[0], c[1]))):
            out.append(header(o))
            out.extend(lines)
    return out


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("usage: python icsdiff.py OLD.ics NEW.ics\n")
        return 2
    try:
        old = parse_calendar(argv[1])
    except ParseError as e:
        sys.stderr.write("%s: %s\n" % (argv[1], e))
        return 2
    try:
        new = parse_calendar(argv[2])
    except ParseError as e:
        sys.stderr.write("%s: %s\n" % (argv[2], e))
        return 2
    lines = diff(old, new)
    if not lines:
        return 0
    sys.stdout.write("\n".join(lines) + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
