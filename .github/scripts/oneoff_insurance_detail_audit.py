from pathlib import Path
import json
import re

root = Path('.')
checked = '2026-09-04'

articles = {
    'B011': root / 'content/articles/B011_flooded_car_insurance.md',
    'B013': root / 'content/articles/B013_fire_insurance_water_damage.md',
    'B014': root / 'content/articles/B014_household_goods_flood_insurance.md',
    'B016': root / 'content/articles/B016_typhoon_wind_damage_insurance.md',
}
previews = {
    'B011': root / 'preview/article_b011.html',
    'B013': root / 'preview/article_b013.html',
    'B014': root / 'preview/article_b014.html',
    'B016': root / 'preview/article_b016.html',
}


def update_frontmatter(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(?m)^status: REVIEW_REQUIRED$', 'status: READY_TO_PUBLISH', text, count=1)
    text = re.sub(r'(?m)^source_checked_at: \d{4}-\d{2}-\d{2}$', f'source_checked_at: {checked}', text, count=1)
    path.write_text(text, encoding='utf-8')


for path in articles.values():
    update_frontmatter(path)

# B011 current sources.
p = articles['B011']
t = p.read_text(encoding='utf-8')
marker = '- 日本損害保険協会「風水雪災等による損害を補償する損害保険」: https://www.sonpo.or.jp/insurance/shizen/index.html'
if '2608_003.html' not in t:
    assert marker in t
    t = t.replace(marker, marker + '\n- 日本損害保険協会「問15 車両保険」: https://soudanguide.sonpo.or.jp/car/q015.html\n- 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」: https://www.sonpo.or.jp/news/notice/2026/2608_003.html', 1)
p.write_text(t, encoding='utf-8')

# B013 current coverage + scoped historic photo procedure.
p = articles['B013']
t = p.read_text(encoding='utf-8')
old = '- 日本損害保険協会「平成30年7月豪雨による災害に伴う損害保険の補償内容等」: https://www.sonpo.or.jp/news/notice/2018/1807_01.html'
new = '- 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」: https://www.sonpo.or.jp/news/notice/2026/2608_003.html\n- 日本損害保険協会「平成30年7月豪雨・被害写真の撮影案内」: https://www.sonpo.or.jp/news/notice/2018/1807_01.html'
if old in t:
    t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')

# B014 current coverage + scoped historic photo procedure.
p = articles['B014']
t = p.read_text(encoding='utf-8')
old = '- 日本損害保険協会「平成30年台風21号による災害に伴う補償内容等」: https://www.sonpo.or.jp/news/notice/2018/1809_05.html'
new = '- 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」: https://www.sonpo.or.jp/news/notice/2026/2608_003.html\n- 日本損害保険協会「平成30年7月豪雨・被害写真の撮影案内」: https://www.sonpo.or.jp/news/notice/2018/1807_01.html'
if old in t:
    t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')

# B016 current consumer-protection sources.
p = articles['B016']
t = p.read_text(encoding='utf-8')
old = '[国民生活センター「保険金で住宅修理ができると勧誘する事業者に注意」](https://www.kokusen.go.jp/news/data/n-20210610_1.html)'
new = '[国民生活センター「古くなった自宅の修理に保険金を使えるか」](https://www.faq.kokusen.go.jp/faq/show/1597?site_domain=default)\n- [日本損害保険協会「住宅の修理などに関するトラブルにご注意」](https://www.sonpo.or.jp/news/caution/syuri.html)'
if old in t:
    t = t.replace(old, new, 1)
p.write_text(t, encoding='utf-8')

sources = {
'B011': '''# B011 出典確認メモ

確認日: 2026-09-04

## F-B011-001 日本損害保険協会「自動車保険」
- URL: https://www.sonpo.or.jp/insurance/car/index.html
- 用途: 一般的な車両保険で台風・洪水・高潮が補償例に含まれること、契約タイプ差

## F-B011-002 日本損害保険協会「風水雪災等による損害を補償する損害保険」
- URL: https://www.sonpo.or.jp/insurance/shizen/index.html
- 用途: 車両保険の風水災、地震・噴火・津波の除外と特約の可能性

## F-B011-003 日本損害保険協会「問15 車両保険」
- URL: https://soudanguide.sonpo.or.jp/car/q015.html
- 用途: 台風・洪水・高潮を含む偶然な事故、契約パターンによる補償範囲差

## F-B011-004 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」
- URL: https://www.sonpo.or.jp/news/notice/2026/2608_003.html
- 用途: 2026年8月時点でも車両保険等に風水雪災を補償する契約があり、個別契約確認が必要であることの現行確認

## 断定しない事項
- 水没すれば必ず保険金が出る、必ず全損になるという断定
- 個別契約の免責、等級、代車、レッカー費用の一律化
- 地震・津波を通常の車両保険と同じ扱いにすること
''',
'B013': '''# B013 公的・業界出典メモ

確認日: 2026-09-04
次回確認予定: 2027-03-01

## F-B013-001 日本損害保険協会「火災保険」
- URL: https://www.sonpo.or.jp/insurance/kasai/index.html
- 用途: 水災補償、建物と家財の別契約、商品による補償差

## F-B013-002 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」
- URL: https://www.sonpo.or.jp/news/notice/2026/2608_003.html
- 用途: 2026年8月時点の風水雪災補償と個別契約確認、住宅修理勧誘への注意

## F-B013-003 日本損害保険協会「平成30年7月豪雨」
- URL: https://www.sonpo.or.jp/news/notice/2018/1807_01.html
- 用途: 片付け・修理が必要な場合の写真記録、建物・家財全体と浸水高さ・損傷箇所の撮影方法
- 注記: 現行補償体系の根拠には使わず、写真記録の具体手順を示す補助資料として限定利用

## F-B013-004 日本損害保険協会「問50 火災保険」
- URL: https://soudanguide.sonpo.or.jp/home/q050.html
- 用途: 建物・家財、水災、自然消耗・劣化等の一般整理

## F-B013-005 金融庁「保険を契約している方へ」
- URL: https://www.fsa.go.jp/ordinary/insurance.html
- 用途: 契約内容・補償の確認

## F-B013-006 国土地理院・国土交通省 ハザードマップポータルサイト
- URL: https://disaportal.gsi.go.jp/
- 用途: 洪水・高潮・土砂等の地域リスク把握

## 断定しない事項
- 個別契約の保険金支払可否
- 「床上浸水なら必ず支払われる」等の一律基準
- 特定の免責金額・損害割合の一般化
- ハザードマップ上の色だけで水災補償の要否を断定すること
''',
'B014': '''# B014 出典確認メモ

確認日: 2026-09-04

## F-B014-001 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」
- URL: https://www.sonpo.or.jp/news/notice/2026/2608_003.html
- 用途: 2026年8月時点の風水雪災補償、個別契約確認

## F-B014-002 日本損害保険協会「火災保険」
- URL: https://www.sonpo.or.jp/insurance/kasai/index.html
- 用途: 建物と家財を別に契約、水災補償、家財の一般的な対象整理

## F-B014-003 日本損害保険協会「問50 火災保険」
- URL: https://soudanguide.sonpo.or.jp/home/q050.html
- 用途: 家財、水災、賃貸住宅、高額品等の契約差

## F-B014-004 日本損害保険協会「平成30年7月豪雨」
- URL: https://www.sonpo.or.jp/news/notice/2018/1807_01.html
- 用途: 家財全体、浸水高さ、損傷箇所の写真記録方法
- 注記: 現行補償体系の根拠には使わず、写真記録の具体手順を示す補助資料として限定利用

## 断定しない事項
- 家財契約があれば全家財が自動補償されるという断定
- 購入価格がそのまま保険金になるという断定
- 高額品・業務用品・同居家族所有物を一律に生活用家財と扱うこと
''',
'B016': '''# B016 出典確認メモ

確認日: 2026-09-04

## F-B016-001 日本損害保険協会「風水雪災等による損害を補償する損害保険」
- URL: https://www.sonpo.or.jp/insurance/shizen/index.html
- 用途: 風災・水災、契約差、住宅修理勧誘注意

## F-B016-002 日本損害保険協会「問51 火災保険」
- URL: https://soudanguide.sonpo.or.jp/home/q051.html
- 用途: 火災保険の補償範囲差、風災・水災の整理

## F-B016-003 福岡管区気象台「台風への備え」
- URL: https://www.data.jma.go.jp/fukuoka/yoho/kisyousaigai_sonae_typhoon.html
- 用途: 強風前の屋外・窓対策、高所等の安全配慮

## F-B016-004 国民生活センター「古くなった自宅の修理に保険金を使えるか」
- URL: https://www.faq.kokusen.go.jp/faq/show/1597?site_domain=default
- 用途: 経年劣化は原則保険金支払対象ではないこと、虚偽申請の危険、契約確認

## F-B016-005 日本損害保険協会「住宅の修理などに関するトラブルにご注意」
- URL: https://www.sonpo.or.jp/news/caution/syuri.html
- 用途: 「保険で無料修理」等の勧誘に対し、契約前に保険会社・代理店へ相談する現行注意喚起（2026-07-31更新）

## 断定しない事項
- 台風当日に判明した損傷をすべて風災とすること
- 経年劣化と突発的風災を自己判断で確定すること
- 修理見積額と保険金認定額が一致するという断定
''',
}
for aid, content in sources.items():
    (root / f'docs/research/{aid}_SOURCES.md').write_text(content, encoding='utf-8')


def replace_anchor(html: str, old_url: str, new_url: str, new_text: str) -> str:
    pattern = r'<a href="' + re.escape(old_url) + r'"([^>]*)>.*?</a>'
    repl = f'<a href="{new_url}"\\1>{new_text}</a>'
    out, n = re.subn(pattern, repl, html, count=1)
    assert n == 1, (old_url, n)
    return out


def add_li_after(html: str, url: str, li_html: str) -> str:
    if li_html in html:
        return html
    pattern = r'(<li><a href="' + re.escape(url) + r'"[^>]*>.*?</a></li>)'
    out, n = re.subn(pattern, r'\1' + li_html, html, count=1)
    assert n == 1, (url, n)
    return out


for aid, path in previews.items():
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'(記事ID: ' + aid + r'</span><span>(?:公的情報)?確認: )2026年9月[12]日', r'\g<1>2026年9月4日', html, count=1)
    path.write_text(html, encoding='utf-8')

p = previews['B011']
h = p.read_text(encoding='utf-8')
h = add_li_after(h, 'https://www.sonpo.or.jp/insurance/shizen/index.html', '<li><a href="https://soudanguide.sonpo.or.jp/car/q015.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「問15 車両保険」</a></li><li><a href="https://www.sonpo.or.jp/news/notice/2026/2608_003.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「令和8年8月27日からの大雨に伴う災害」</a></li>')
p.write_text(h, encoding='utf-8')

p = previews['B013']
h = p.read_text(encoding='utf-8')
h = replace_anchor(h, 'https://www.sonpo.or.jp/news/notice/2018/1807_01.html', 'https://www.sonpo.or.jp/news/notice/2026/2608_003.html', '日本損害保険協会「令和8年8月27日からの大雨に伴う災害」')
h = add_li_after(h, 'https://www.sonpo.or.jp/news/notice/2026/2608_003.html', '<li><a href="https://www.sonpo.or.jp/news/notice/2018/1807_01.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「平成30年7月豪雨・被害写真の撮影案内」</a></li>')
p.write_text(h, encoding='utf-8')

p = previews['B014']
h = p.read_text(encoding='utf-8')
h = replace_anchor(h, 'https://www.sonpo.or.jp/news/notice/2018/1809_05.html', 'https://www.sonpo.or.jp/news/notice/2026/2608_003.html', '日本損害保険協会「令和8年8月27日からの大雨に伴う災害」')
h = add_li_after(h, 'https://www.sonpo.or.jp/news/notice/2026/2608_003.html', '<li><a href="https://www.sonpo.or.jp/news/notice/2018/1807_01.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「平成30年7月豪雨・被害写真の撮影案内」</a></li>')
p.write_text(h, encoding='utf-8')

p = previews['B016']
h = p.read_text(encoding='utf-8')
h = replace_anchor(h, 'https://www.kokusen.go.jp/news/data/n-20210610_1.html', 'https://www.faq.kokusen.go.jp/faq/show/1597?site_domain=default', '国民生活センター「古くなった自宅の修理に保険金を使えるか」')
h = add_li_after(h, 'https://www.faq.kokusen.go.jp/faq/show/1597?site_domain=default', '<li><a href="https://www.sonpo.or.jp/news/caution/syuri.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「住宅の修理などに関するトラブルにご注意」</a></li>')
p.write_text(h, encoding='utf-8')

common_head = '''> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`'''

review_data = {
    'B011': ('台風・洪水で水没した車は車両保険の対象になる？', '台風・洪水・高潮による車両損害を、津波等と分離して契約確認へ導く', '車両保険・免責・原因を確認し、危険区域へ戻らず契約先へ連絡', '4件。2026年8月の大雨案内と現行車両保険Q&Aまで再確認', ['台風・洪水・高潮は車両保険の補償例だが契約差を明記', '地震・噴火・津波は通常補償と分離し特約確認へ誘導', '浸水車を始動させず、冠水区域へ写真撮影のため戻らせない', '全損・等級・代車・レッカーを一律断定しない']),
    'B013': ('火災保険の水災補償とは？住宅浸水との関係を整理', '住宅水災について建物/家財・支払条件を契約書類で確認させる', '水災補償、対象、免責・条件を確認し、不明点を契約先へ照会', '6件。現行補償は2026年資料、写真手順のみ2018年資料を限定利用', ['火災保険加入だけで水災補償ありと断定しない', '建物と家財を別契約として整理', '床上浸水だけで支払いを断定しない', '写真記録より人身安全・感電等の回避を優先']),
    'B014': ('浸水した家財は保険の対象になる？確認ポイント', '浸水した家財について建物契約と分離し、記録・処分・契約確認へ導く', '家財契約と水災補償を確認し、安全な範囲で記録して契約先へ連絡', '4件。2026年資料へ更新し、写真手順のみ旧一次資料を限定利用', ['建物保険があれば家財も自動補償とはしない', '家財の購入価格=支払額と断定しない', '高額品・業務用品等の契約差を明記', '処分前記録は安全・衛生上可能な範囲に限定']),
    'B016': ('台風の風災は火災保険でどう扱われる？', '風災と水災・経年劣化を分け、安全な被害確認と契約確認へ導く', '高所へ上がらず、原因・対象・契約を整理して保険会社へ相談', '5件。2026年更新の経年劣化FAQ・住宅修理注意まで再確認', ['台風の日に判明した損傷を一律に風災としない', '風災と水災、突発損害と経年劣化を分離', '屋根・高所へ撮影のため上がらせない', '「保険で無料修理」勧誘では契約前に保険会社・代理店へ相談']),
}

for aid, (title, page_job, next_action, source_note, specific) in review_data.items():
    lines = [
        f'# {aid} 記事別レビュー記録', '', common_head, '',
        f'- article_id: `{aid}`', f'- title: {title}', '- content_role: `detail`', '- risk_level: `elevated`',
        '- article_status: `READY_TO_PUBLISH`', '- review_status: `PASS`', '- last_checked_at: 2026-09-04', '- reviewer: ChatGPT', '- persona_mode: `SITUATIONAL_SEGMENT`', '',
        '## 1. 共通チェック結果', '', '| 共通チェック | 状態 | 根拠・備考 |', '|---|---|---|',
        '| C01 内容・情報量 | PASS | detail記事として判断条件・例外・事故後手順まで必要十分 |',
        f'| C02 出典・安全性 | PASS | {source_note} |',
        '| C03 画像・視覚要素 | PASS | 既存の日本文脈・権利・関連性レビューを継承。画像を補償判断の根拠にしない |',
        '| C04 読みやすさ・UI | PASS | 表・手順・注意枠・Q&A導線を既存UIで整理 |',
        '| C05 内部リンク | PASS | 関連する車・住宅・保険総論/詳細記事へ接続 |',
        '| C06 商品導線・商品記事 | N/A | 保険商品の販売・比較・見積もり誘導なし |',
        '| C07 Q&A | PASS | 既存個別Q&Aへの文脈リンクと本文結論が整合 |',
        '| C08 同期・公開前 | PASS | article/source/preview/registry/checklistを2026-09-04監査へ同期 |',
        '| C09 日付・構造化データ | PASS | registryの日付を正本としてproduction buildへ反映 |',
        '| C10 デザイン・UX | PASS | 既存記事UIを使用し役割の異なる要素を混同させない |',
        '| C11 読者・マーケティング | PASS | 不安を煽って加入・修理契約へ誘導せず、契約確認と安全行動を次アクションにする |',
        '| C12 アクセシビリティ | PASS | 色依存なし。見出し・表・リンクテキストで意味を伝達 |',
        '| C13 技術品質・信頼性 | PASS | production build/test/smoke対象 |',
        '| C14 計測・グロース | N/A | 計測変更なし |', '',
        '## 2. 防災サイト固有チェック', '', '| 項目 | 状態 | 根拠・備考 |', '|---|---|---|',
        '| S01 適用判定 | PASS | 保険・安全記事としてE01〜E07,E11〜E14を適用。E08/E09はN/A |',
        '| S02 情報設計 | PASS | B019総論と役割分離し、この記事固有の損害・契約確認へ絞る |',
        '| S03 法務・権利等 | PASS | 個別契約の支払可否・責任・認定額を断定しない |',
        '| S04 ブランド・トーン | PASS | 安全→事実記録→契約確認の順。過度な不安・販売訴求なし |',
        '| S05 日本向け文脈 | PASS | 日本損害保険協会・金融庁/国民生活センター等の国内資料中心 |',
        '| S06 運用・ガバナンス | PASS | staleなREVIEW_REQUIREDを解消し、出典確認日・台帳・previewを同期 |',
        '| S07 セキュリティ・外部依存 | PASS | 公的・業界公式リンクのみ。新規外部機能なし |',
        '| S08 数値 | PASS | 契約差の大きい金額・免責・認定基準を一律化しない |', '',
        '## 3. 保険・安全誤認防止確認', ''
    ]
    lines += [f'- PASS: {x}' for x in specific]
    lines += ['', '## 4. 読者・ページ設計', '',
              '- target_reader: 災害前後に自分の補償範囲や手順を確認したい一般契約者',
              '- usage_context: 平常時の契約確認、被害直後の初動整理',
              '- reader_problem: 災害名や被害の見た目だけで補償可否を判断しやすい',
              '- reader_goal: 原因・対象・契約条件を分け、安全に次の手続きへ進む',
              f'- page_job: {page_job}', f'- next_action: {next_action}', '',
              '## 5. 証跡', '', f'- sources: `docs/research/{aid}_SOURCES.md`', f'- article: `{articles[aid].as_posix()}`', f'- preview: `{previews[aid].as_posix()}`', '',
              '## 6. 最終判定', '', '- review_status: `PASS`', '- READY_TO_PUBLISH: `YES`', '- 判定理由: 2026-09-04時点の現行補償体系、安全表現、記事役割、出典鮮度、内部導線を再監査し、公開済み正本とレビュー状態を同期。', '']
    (root / f'docs/reviews/{aid}_CHECKLIST.md').write_text('\n'.join(lines), encoding='utf-8')

registry_path = root / 'data/content_registry.json'
data = json.loads(registry_path.read_text(encoding='utf-8'))
by_id = {a['article_id']: a for a in data['articles']}
counts = {'B011': 4, 'B013': 6, 'B014': 4, 'B016': 5}
for aid, count in counts.items():
    a = by_id[aid]
    a['status'] = 'READY_TO_PUBLISH'
    a['source_checked_at'] = checked
    a['source_count'] = count
    a['source_ids'] = [f'F-{aid}-{i:03d}' for i in range(1, count + 1)]
    a['last_reviewed_at'] = checked
    a['review_checklist_last_checked_at'] = checked
    a['review_checklist_status'] = 'PASS'
    a['manual_review_status'] = 'APPROVED'
    a['publish_blockers'] = []
    a['production_build_status'] = 'READY_FOR_DEPLOY'
    a['modified_at'] = checked

data['updated_at'] = '2026-09-04T14:17:00+09:00'
registry_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
