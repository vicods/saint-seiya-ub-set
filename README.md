# Saint Seiya — Cosmo Archive (versão estática)

Esta é a versão estática do painel, pronta para publicar no GitHub Pages.
Diferente da versão `cosmo-archive-draft` (que ainda usa `server.py` e
fica como referência obsoleta), aqui não existe nenhum backend rodando —
tudo é lido a partir de `assets/cards.json`, gerado pelo script Python
local sempre que você adicionar/remover cartas.

## Estrutura

```
cosmo-archive/
  index.html          <- página de apresentação do set (abre primeiro)
  archive.html         <- painel com filtros e galeria de cartas
  pack.html            <- simulador de abertura de pack
  assets/
    cards.json          <- gerado pelo script, não edite manualmente
    cards/
      common/
      uncommon/
      rare/
      mythic/
      ink/
    mtg-set-symbol-mythic.png
  scripts/
    generate_cards_json.py
```

## Fluxo de trabalho

1. Adicione/remova/renomeie arquivos de carta dentro de `assets/cards/{raridade}/`,
   seguindo a convenção de nome:
   `{raridade}_{cor}_{tipo}_{slug-do-nome}.png`

2. Rode o script gerador a partir da raiz do projeto:
   ```
   python scripts/generate_cards_json.py
   ```
   Isso reescreve `assets/cards.json` com a lista atualizada.

3. Faça commit de tudo (imagens novas + `cards.json` atualizado) e
   suba para o GitHub.

4. Nas configurações do repositório no GitHub, em **Settings > Pages**,
   selecione a branch e a pasta raiz (`/`) como fonte. O GitHub Pages
   vai publicar `index.html` automaticamente como página inicial.

## O que mudou em relação à versão com servidor Python

- `archive.html` não chama mais `/api/cards` — lê `assets/cards.json` direto.
- `pack.html` não chama mais `/api/simulate-pack` — a lógica de sorteio
  do booster (1 terreno, 10 comuns, 3 incomuns, 1 raro com 1/8 de chance
  de virar mítico) foi portada para JavaScript e roda inteiramente no
  navegador, usando os dados de `cards.json`.
- A mesa de draft com bots (`draft.html`, `deckbuilder.html`) **não foi
  portada** para esta versão, porque depende de estado mutável entre
  jogadores que um site estático não sustenta sozinho. Ela continua
  existindo e funcionando normalmente na pasta `cosmo-archive-draft`,
  que segue precisando do `server.py` local.

## Aviso sobre cache do GitHub Pages

GitHub Pages também faz cache de arquivos estáticos. Se você atualizar
uma carta e a alteração não aparecer no site publicado, force um reload
(Ctrl+Shift+R) ou aguarde alguns minutos — o CDN do GitHub Pages pode
levar um tempo para invalidar o cache de um arquivo já publicado antes.
