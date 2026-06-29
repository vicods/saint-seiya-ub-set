"""
Gerador de cards.json para a versão estática do painel Saint Seiya MTG.

Uso:
    python scripts/generate_cards_json.py

Roda a partir da raiz do projeto (onde está assets/). Escaneia
assets/cards/{common,uncommon,rare,mythic,ink}/ e escreve assets/cards.json
com a lista de cartas no mesmo formato que a API antiga retornava em
/api/cards -- então o front-end muda muito pouco, só troca fetch("/api/cards")
por fetch("assets/cards.json").

Rode este script sempre que adicionar, remover ou renomear um arquivo de
carta, e faça commit do cards.json atualizado junto com as imagens. Sem
isso, o GitHub Pages vai continuar servindo a lista antiga.

Convenção de nome esperada (igual ao server.py antigo):
    {raridade}_{cor}_{tipo}_{slug-do-nome}.png

Exemplos:
    common_b_creature_annihilation-basilisk.png
    common_c_artifact_apprentices-gear.png
    rare_bw_creature_saga.png
    mythic_wubrg_enchantment_past-holy-war.png
    ink_w_instant_deicide-promo.png
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
CARDS_DIR = ROOT / "assets" / "cards"
OUTPUT_FILE = ROOT / "assets" / "cards.json"

RARITIES = ["common", "uncommon", "rare", "mythic"]
SPECIAL_RARITIES = ["ink", "token"]
ALL_RARITIES = RARITIES + SPECIAL_RARITIES

NAME_PATTERN = re.compile(
    r"^(?P<rarity>common|uncommon|rare|mythic|ink|token)_"
    r"(?P<color>[wubrgc]+|colorless)_"
    r"(?P<type>[a-z]+)_"
    r"(?P<slug>.+)\.(png|jpg|jpeg|webp)$",
    re.IGNORECASE,
)

COLOR_ORDER = "WUBRG"

TYPE_RANK = {
    "creature": 0,
    "instant": 1,
    "sorcery": 2,
    "enchantment": 3,
    "artifact": 4,
    "land": 5,
}


def normalize_color(raw):
    raw = raw.upper()
    if raw == "C" or raw == "COLORLESS":
        return "C"
    return "".join(c for c in COLOR_ORDER if c in raw)


def slug_to_title(slug):
    return " ".join(w.capitalize() for w in slug.split("-"))


def scan_cards():
    cards = []
    skipped = []

    if not CARDS_DIR.exists():
        print(f"AVISO: {CARDS_DIR} não existe ainda.")
        return cards, skipped

    for rarity_dir in CARDS_DIR.iterdir():
        if not rarity_dir.is_dir():
            continue
        for f in rarity_dir.iterdir():
            if not f.is_file() or f.name.startswith("."):
                continue
            m = NAME_PATTERN.match(f.name)
            if not m:
                skipped.append(f.name)
                continue

            color = normalize_color(m.group("color"))
            cards.append({
                "filename": f.name,
                # path relativo à raiz do site publicado no GitHub Pages
                "path": f"assets/cards/{rarity_dir.name}/{f.name}",
                "rarity": m.group("rarity").lower(),
                "color": color,
                "colorCount": len(color) if color != "C" else 0,
                "type": m.group("type").lower(),
                "slug": m.group("slug").lower(),
                "name": slug_to_title(m.group("slug")),
            })

    rarity_rank = {r: i for i, r in enumerate(ALL_RARITIES)}
    cards.sort(key=lambda c: (
        rarity_rank.get(c["rarity"], 99),
        c["color"],
        TYPE_RANK.get(c["type"], 50),
        c["name"],
    ))

    return cards, skipped


def main():
    cards, skipped = scan_cards()

    output = {
        "cards": cards,
        "skipped": skipped,
        "total": len(cards),
        "generatedAt": __import__("datetime").datetime.now().isoformat(),
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n=== cards.json gerado ===")
    print(f"Total de cartas: {len(cards)}")
    if skipped:
        print(f"Arquivos ignorados (nome fora do padrão): {len(skipped)}")
        for s in skipped[:10]:
            print(f"  - {s}")
        if len(skipped) > 10:
            print(f"  ... e mais {len(skipped) - 10}")
    print(f"\nSalvo em: {OUTPUT_FILE}")
    print("Lembre de fazer commit deste arquivo junto com as imagens novas.\n")


if __name__ == "__main__":
    main()
