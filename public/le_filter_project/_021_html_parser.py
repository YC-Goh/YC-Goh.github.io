#!/usr/bin/env python3
"""
Affix HTML Parser & CLI
-----------------------
Parses affix HTML files into structured JSON.

Usage examples:
    python affix_parser.py snippet.html
    python affix_parser.py snippet.html --pretty
    python affix_parser.py snippet.html -o output.json
    python affix_parser.py snippet.html --summary
"""

from __future__ import annotations
from dataclasses import dataclass, asdict, field
from bs4 import BeautifulSoup, Tag
from typing import List, Optional, Dict, Any, Union
import json, re, argparse
from pathlib import Path

# ---------- Data Model ----------

@dataclass
class ModifierHeader:
    label: str
    mod_type: Optional[str] = None
    raw_html: Optional[str] = None

@dataclass
class TierRange:
    header_index: int
    raw_text: str
    parsed: Optional[Dict[str, Any]] = None

@dataclass
class Tier:
    number: Union[int, str]
    ranges: List[TierRange]
    raw_html: Optional[str] = None

@dataclass
class RelatedRef:
    kind: str
    name: str
    href: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExtraInfo:
    text: str
    details: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Affix:
    name: str
    type: str
    title: Optional[str]
    href: Optional[str] = None
    id_attr: Optional[str] = None
    requires_level: Optional[int] = None
    applies_to: List[str] = field(default_factory=list)
    headers: List[ModifierHeader] = field(default_factory=list)
    tiers: List[Tier] = field(default_factory=list)
    related: List[RelatedRef] = field(default_factory=list)
    extra_info: List[ExtraInfo] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    raw_html: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# ---------- Utilities ----------

class Text:
    @staticmethod
    def norm(s: Optional[str]) -> str:
        if not s: return ""
        return re.sub(r"\s+", " ", s).strip()

    @staticmethod
    def int_or_none(s: str) -> Optional[int]:
        m = re.search(r"\d+", s or "")
        return int(m.group()) if m else None

class RangeParser:
    RE_NUMBER = r"[-+]?\d+(?:\.\d+)?"
    RE_PERCENT = re.compile(rf"^(?P<min>{RE_NUMBER})(?:\s*to\s*(?P<max>{RE_NUMBER}))?\s*(?P<unit>%?)$")
    RE_TO = re.compile(rf"^(?P<min>{RE_NUMBER})\s*to\s*(?P<max>{RE_NUMBER})(?P<unit>%?)$")

    @classmethod
    def parse(cls, raw: str) -> Optional[Dict[str, Any]]:
        s = Text.norm(raw)
        if not s: return None
        m = cls.RE_TO.match(s)
        if m:
            d = {"min": float(m.group("min")), "max": float(m.group("max"))}
            if m.group("unit"): d["unit"] = "%"
            return d
        m = cls.RE_PERCENT.match(s)
        if m:
            d: Dict[str, Any] = {"value": float(m.group("min"))}
            if m.group("unit"): d["unit"] = "%"
            return d
        try:
            return {"value": float(s)}
        except ValueError:
            return None

# ---------- Extractor ----------

class HtmlAffixExtractor:
    def __init__(self, card: Tag):
        self.card = card

    def extract(self) -> Affix:
        classes = self.card.get("class", [])
        raw_html = str(self.card)

        desc = self.card.select_one(".top-block .item-description")
        name_el = desc.select_one("a.item-name") if desc else None
        title_el = desc.select_one(".affix-title") if desc else None
        type_el = desc.select_one(".item-type.for-affix") if desc else None

        name = Text.norm(name_el.get_text()) if name_el else ""
        href = name_el.get("href") if name_el else None
        id_attr = name_el.get("prefix-id") or name_el.get("suffix-id") if name_el else None
        title = Text.norm(title_el.get_text()) if title_el else None
        type_ = Text.norm(type_el.get_text()) if type_el else ""

        requires_level = None
        lvl_el = self.card.select_one(".item-req")
        if lvl_el:
            requires_level = Text.int_or_none(lvl_el.get_text())

        applies_to = [Text.norm(li.get_text()) for li in self.card.select(".affix-applies-to-list li")]

        extra_info: List[ExtraInfo] = []
        for info_div in self.card.select(".bottom-block .extra-info"):
            text = Text.norm(info_div.get_text(separator=" ", strip=True))
            details_el = info_div.select_one(".extra-info-details")
            details = Text.norm(details_el.get_text()) if details_el else None

            rarity_span = info_div.select_one(".rarity-on-items ~ .with-hover-text.drop-chance")
            hover_text = None
            if rarity_span:
                hover = rarity_span.select_one(".hover-text")
                if hover:
                    hover_text = Text.norm(hover.get_text())
            extra = {}
            if hover_text:
                extra["hover_text"] = hover_text
            extra_info.append(ExtraInfo(text=text, details=details, extra=extra))

        related: List[RelatedRef] = []
        for group in self.card.select(".related-refs .refs-group"):
            title_el = group.find_previous_sibling(lambda x: isinstance(x, Tag) and "refs-title" in x.get("class", []))
            kind_text = Text.norm(title_el.get_text()).lower() if title_el else "unknown"
            kind = "abilities" if "ability" in kind_text else "ailments" if "ailment" in kind_text else "unknown"

            for a in group.select("a"):
                name_ref = Text.norm(a.get_text())
                href_ref = a.get("href")
                extra = {k: a.get(k) for k in a.attrs if k not in {"href", "class"}}
                related.append(RelatedRef(kind=kind, name=name_ref, href=href_ref, extra=extra))

        headers: List[ModifierHeader] = []
        header_row = self.card.select_one(".tier-table .affix.tier-header")
        if header_row:
            for cell in header_row.select(".affix-tier-range"):
                label_parts, mod_type = [], None
                for child in cell.children:
                    if isinstance(child, Tag) and child.name == "span" and "mod-type" in child.get("class", []):
                        mod_type = Text.norm(child.get_text())
                    else:
                        label_parts.append(Text.norm(getattr(child, "string", str(child))))
                label = Text.norm(" ".join([p for p in label_parts if p]))
                headers.append(ModifierHeader(label=label, mod_type=mod_type, raw_html=str(cell)))

        tiers: List[Tier] = []
        for row in self.card.select(".tier-table .affix[tier]"):
            number_text = Text.norm(row.get("tier") or row.select_one(".affix-tier-name").get_text())
            try:
                number = int(number_text)
            except Exception:
                number = number_text or ""
            ranges: List[TierRange] = []
            cells = row.select(".affix-tier-range")
            for idx, cell in enumerate(cells):
                raw_text = Text.norm(cell.get_text())
                parsed = RangeParser.parse(raw_text)
                ranges.append(TierRange(header_index=idx, raw_text=raw_text, parsed=parsed))
            tiers.append(Tier(number=number, ranges=ranges, raw_html=str(row)))

        return Affix(
            name=name, type=type_, title=title, href=href, id_attr=id_attr,
            requires_level=requires_level, applies_to=applies_to,
            headers=headers, tiers=tiers, related=related, extra_info=extra_info,
            classes=list(classes), raw_html=raw_html,
        )

# ---------- Public API ----------

class AffixHTMLParser:
    def __init__(self, html: Optional[str] = None):
        self.soup = BeautifulSoup(html, "html.parser") if html else None

    def parse_html(self, html: str) -> List[Affix]:
        self.soup = BeautifulSoup(html, "html.parser")
        return self._parse_soup(self.soup)

    def parse_file(self, path: Union[str, Path]) -> List[Affix]:
        p = Path(path)
        html = p.read_text(encoding="utf-8")
        return self.parse_html(html)

    @staticmethod
    def _parse_soup(soup: BeautifulSoup) -> List[Affix]:
        affixes: List[Affix] = []
        for card in soup.select(".item-card.item-affix"):
            try:
                affixes.append(HtmlAffixExtractor(card).extract())
            except Exception as e:
                affixes.append(Affix(name=f"__PARSE_ERROR__ {e}", type="", title=None, raw_html=str(card)))
        return affixes

# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(description="Parse affix HTML files into structured JSON")
    parser.add_argument("input_file", type=Path, help="Path to the input HTML file containing affixes")
    parser.add_argument("-o", "--output", type=Path, default=None,
                        help="Output JSON file path (defaults to <input>.json)")
    parser.add_argument("--pretty", action="store_true",
                        help="Pretty-print JSON with indentation")
    parser.add_argument("--summary", action="store_true",
                        help="Print a summary instead of (or in addition to) JSON")
    parser.add_argument("--limit", type=int, default=0,
                        help="If set, show only the first N affix names in the summary")
    parser.add_argument("--no-json", action="store_true",
                        help="Skip writing any JSON output (useful with --summary)")

    args = parser.parse_args()

    affix_parser = AffixHTMLParser()
    affixes = affix_parser.parse_file(args.input_file)

    # Print summary if requested
    if args.summary:
        print("=" * 60)
        print(f"Parsed {len(affixes)} affixes from {args.input_file}")

        # Breakdown by type
        type_counts: Dict[str, int] = {}
        for affix in affixes:
            t = affix.type or "Unknown"
            type_counts[t] = type_counts.get(t, 0) + 1
        print("\nBy type:")
        for t, c in sorted(type_counts.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {t:10s} : {c}")

        # Breakdown by applies-to
        applies_counts: Dict[str, int] = {}
        for affix in affixes:
            for slot in affix.applies_to or ["—"]:
                applies_counts[slot] = applies_counts.get(slot, 0) + 1
        print("\nBy applies-to:")
        for slot, c in sorted(applies_counts.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {slot:15s} : {c}")

        # First N names if limit specified
        if args.limit > 0:
            print(f"\nFirst {args.limit} affix names:")
            for affix in affixes[:args.limit]:
                print(f"  - {affix.name}")
        elif affixes:
            # Fallback: one example
            first = affixes[0]
            print("\nFirst affix example:")
            print(f"  Name       : {first.name!r}")
            print(f"  Type       : {first.type}")
            print(f"  Applies to : {', '.join(first.applies_to) if first.applies_to else '—'}")

        print("=" * 60)

    # Save JSON unless skipped
    if not args.no_json:
        output_path = args.output or args.input_file.with_suffix(".json")
        with output_path.open("w", encoding="utf-8") as f:
            if args.pretty:
                json.dump([a.to_dict() for a in affixes], f, ensure_ascii=False, indent=2)
            else:
                json.dump([a.to_dict() for a in affixes], f, ensure_ascii=False)
        print(f"Saved JSON to {output_path}")

if __name__ == "__main__":
    main()
