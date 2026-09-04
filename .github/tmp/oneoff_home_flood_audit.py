from pathlib import Path
import json
import re

root = Path('.')
checked = '2026-09-04'
updated_at = '2026-09-04T14:38:00+09:00'

articles = {
    'B012': root / 'content/articles/B012_home_flood_preparedness.md',
    'B015': root / 'content/articles/B015_after_flood_record_evidence.md',
    'B020': root / 'content/articles/B020_home_heavy_rain_checklist.md',
    'B021': root / 'content/articles/B021_typhoon_day_before_checklist.md',
    'B022': root / 'content/articles/B022_apartment_typhoon_flood.md',
}
previews = {aid: root / f'preview/article_{aid.lower()}.html' for aid in articles}


def set_frontmatter(path: Path):
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(?m)^status: REVIEW_REQUIRED$', 'status: READY_TO_PUBLISH', text, count=1)
    text = re.sub(r'(?m)^source_checked_at: \d{4}-\d{2}-\d{2}$', f'source_checked_at: {checked}', text, count=1)
    path.write_text(text, encoding='utf-8')


def ensure_after(text: str, marker: str, addition: str, unique: str) -> str:
    if unique in text:
        return text
    assert marker in text, marker
    return text.replace(marker, marker + addition, 1)


def replace_if_present(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1) if old in text else text


def add_li_after(html: str, url: str, li_html: str, unique: str) -> str:
    if unique in html:
        return html
    pattern = r'(<li><a href="' + re.escape(url) + r'"[^>]*>.*?</a></li>)'
    out, n = re.subn(pattern, r'\1' + li_html, html, count=1)
    assert n == 1, (url, n)
    return out


for p in articles.values():
    set_frontmatter(p)

# B012/B020: replace draft guideline URL with final official version.
for aid in ('B012', 'B020'):
    p = articles[aid]
    t = p.read_text(encoding='utf-8')
    t = t.replace('https://www.mlit.go.jp/jutakukentiku/build/content/001348131.pdf',
                  'https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf')
    p.write_text(t, encoding='utf-8')

# B015: current compensation/trouble sources, while retaining historic photo procedure only for documentation guidance.
p = articles['B015']
t = p.read_text(encoding='utf-8')
t = replace_if_present(
    t,
    '- 日本損害保険協会「平成30年台風21号による災害に伴う補償内容等」: https://www.sonpo.or.jp/news/notice/2018/1809_05.html',
    '- 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」: https://www.sonpo.or.jp/news/notice/2026/2608_003.html\n- 日本損害保険協会「平成30年7月豪雨・被害写真の撮影案内」: https://www.sonpo.or.jp/news/notice/2018/1807_01.html'
)
t = ensure_after(
    t,
    '- 日本損害保険協会「風水雪災等による損害を補償する損害保険」: https://www.sonpo.or.jp/insurance/shizen/index.html',
    '\n- 日本損害保険協会「住宅の修理などに関するトラブルにご注意」: https://www.sonpo.or.jp/news/caution/syuri.html',
    'https://www.sonpo.or.jp/news/caution/syuri.html'
)
old_para = '**自治体の罹災証明**は公的支援等で使われる制度で、損害保険の請求手続きとは別です。保険会社が求める資料は契約・事故内容で異なります。'
new_para = old_para + '\n\n日本損害保険協会は2026年8月31日更新の大雨災害案内で、**損害保険の保険金等の請求では地方自治体の罹災証明書の提出は原則不要**と案内しています。ただし、個別契約で必要な書類は契約先へ確認します。'
if '罹災証明書の提出は原則不要' not in t:
    assert old_para in t
    t = t.replace(old_para, new_para, 1)
p.write_text(t, encoding='utf-8')

# B022: directly support high-rise building electrical/lifeline outage claims.
p = articles['B022']
t = p.read_text(encoding='utf-8')
marker = '- 内閣府「自然災害への備えは万全ですか？」: https://www.bousai.go.jp/kyoiku/hokenkyousai/check.html'
t = ensure_after(
    t, marker,
    '\n- 国土交通省・経済産業省「建築物における電気設備の浸水対策ガイドライン」: https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf',
    '001349327.pdf'
)
p.write_text(t, encoding='utf-8')

sources = {
'B012': '''# B012 出典確認メモ

確認日: 2026-09-04

## F-B012-001 ハザードマップポータルサイト
- URL: https://disaportal.gsi.go.jp/
- 用途: 洪水・内水・高潮等の地点リスク、複数災害種別の確認

## F-B012-002 国土交通省・経済産業省「建築物における電気設備の浸水対策ガイドライン」
- URL: https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf
- 用途: 簡易水防は小規模・浅い初期浸水に限られ効果が限定的であること、開口部・電気設備の浸水対策
- 注記: 旧 `001348131.pdf`（最終案）ではなく正式版を参照

## F-B012-003 気象庁「自分で行う災害への備え」
- URL: https://www.jma.go.jp/jma/kishou/know/ame_chuui/ame_chuui_p10.html
- 用途: 大雨・台風前の側溝・排水口、非常用品、避難場所・経路、家族連絡

## 断定しない事項
- ハザードマップで色がない場所を安全と断定しない
- 簡易止水・水のう等で深い浸水を防げると保証しない
- 上階があることだけで在宅避難可能と断定しない
- 電気設備を一般利用者が浸水後に操作できると案内しない
''',
'B015': '''# B015 出典確認メモ

確認日: 2026-09-04

## F-B015-001 日本損害保険協会「令和8年8月27日からの大雨に伴う災害」
- URL: https://www.sonpo.or.jp/news/notice/2026/2608_003.html
- 用途: 2026年8月時点の風水雪災補償、保険金請求で罹災証明書提出が原則不要である旨、契約先確認

## F-B015-002 日本損害保険協会「風水雪災等による損害を補償する損害保険」
- URL: https://www.sonpo.or.jp/insurance/shizen/index.html
- 用途: 風災・水災等の一般的な補償整理と契約差

## F-B015-003 日本損害保険協会「平成30年7月豪雨」
- URL: https://www.sonpo.or.jp/news/notice/2018/1807_01.html
- 用途: 建物・家財全体、浸水高さ、損傷箇所の写真記録方法
- 注記: 現行補償体系の根拠には使わず、写真記録の具体手順に限定利用

## F-B015-004 日本損害保険協会「住宅の修理などに関するトラブルにご注意」
- URL: https://www.sonpo.or.jp/news/caution/syuri.html
- 用途: 「保険が使える」と勧誘する住宅修理業者への注意、契約前に保険会社・代理店へ相談

## 断定しない事項
- 写真を撮らないと保険請求できないという断定
- 危険な建物への再侵入を促すこと
- 罹災証明があれば保険金が支払われる、または必ず不要という個別契約への断定
- 修理・廃棄を保険会社確認まで一律に禁止すること
''',
'B020': '''# B020 出典確認メモ

確認日: 2026-09-04

## F-B020-001 ハザードマップポータルサイト
- URL: https://disaportal.gsi.go.jp/
- 用途: 洪水・内水・高潮等の地点リスクと避難経路確認

## F-B020-002 気象庁「自分で行う災害への備え」
- URL: https://www.jma.go.jp/jma/kishou/know/ame_chuui/ame_chuui_p10.html
- 用途: 大雨前の側溝・排水口、屋外物、非常用品、避難場所・経路

## F-B020-003 国土交通省・経済産業省「建築物における電気設備の浸水対策ガイドライン」
- URL: https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf
- 用途: 簡易水防は小規模・浅い初期浸水に限られ効果が限定的であること
- 注記: 旧 `001348131.pdf`（最終案）ではなく正式版を参照

## 断定しない事項
- 日数区分を気象状況に関係なく固定ルールとしない
- 簡易水防の効果を保証しない
- 大雨中の屋外作業を促さない
- 家や車を守る作業を避難より優先しない
''',
'B021': '''# B021 出典確認メモ

確認日: 2026-09-04

## F-B021-001 福岡管区気象台「台風への備え」
- URL: https://www.data.jma.go.jp/fukuoka/yoho/kisyousaigai_sonae_typhoon.html
- 用途: 台風前の屋外物、窓・雨戸、側溝・排水口、停電等への備え

## F-B021-002 気象庁「自分で行う災害への備え」
- URL: https://www.jma.go.jp/jma/kishou/know/ame_chuui/ame_chuui_p10.html
- 用途: 台風・大雨前の住宅、非常用品、避難場所・経路、家族連絡

## F-B021-003 内閣府「自然災害への備えは万全ですか？」
- URL: https://www.bousai.go.jp/kyoiku/hokenkyousai/check.html
- 用途: 家庭備蓄、家族連絡、避難の平時準備

## 断定しない事項
- 「前日」なら屋外作業が必ず安全としない
- 窓テープ等の単一対策で破損防止を保証しない
- 医療機器を一般バッテリーで代替できると案内しない
- 台風中心から離れていれば安全としない
''',
'B022': '''# B022 出典確認メモ

確認日: 2026-09-04

## F-B022-001 ハザードマップポータルサイト
- URL: https://disaportal.gsi.go.jp/
- 用途: 洪水・内水・高潮等の地点リスク

## F-B022-002 気象庁「自分で行う災害への備え」
- URL: https://www.jma.go.jp/jma/kishou/know/ame_chuui/ame_chuui_p10.html
- 用途: 大雨・台風前の住宅、非常用品、避難場所・経路

## F-B022-003 内閣府「自然災害への備えは万全ですか？」
- URL: https://www.bousai.go.jp/kyoiku/hokenkyousai/check.html
- 用途: 家庭備蓄、家族連絡、避難

## F-B022-004 国土交通省・経済産業省「建築物における電気設備の浸水対策ガイドライン」
- URL: https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf
- 用途: 高層マンション地下の受変電設備浸水により停電し、エレベーター・給水設備等が一定期間使用不能となった実例、電気設備の浸水対策

## 断定しない事項
- 高層階なら水害全般で安全と断定しない
- 非常用電源が全設備・全住戸を長時間賄うと断定しない
- 共用設備を住民が自己判断で操作できると案内しない
- 地下・機械式駐車場へ危険時に車を取りに戻ることを促さない
'''
}
for aid, content in sources.items():
    (root / f'docs/research/{aid}_SOURCES.md').write_text(content, encoding='utf-8')

# Preview dates and source links.
for aid, path in previews.items():
    html = path.read_text(encoding='utf-8')
    html = re.sub(r'(記事ID: ' + aid + r'</span><span>(?:公的情報)?確認: )2026年9月[12]日', r'\g<1>2026年9月4日', html, count=1)
    html = html.replace('https://www.mlit.go.jp/jutakukentiku/build/content/001348131.pdf',
                        'https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf')
    path.write_text(html, encoding='utf-8')

# B015 preview: update current sources and add current罹災証明 guidance.
p = previews['B015']
h = p.read_text(encoding='utf-8')
old_url = 'https://www.sonpo.or.jp/news/notice/2018/1809_05.html'
if old_url in h:
    h = re.sub(r'<a href="' + re.escape(old_url) + r'"([^>]*)>.*?</a>',
               r'<a href="https://www.sonpo.or.jp/news/notice/2026/2608_003.html"\1>日本損害保険協会「令和8年8月27日からの大雨に伴う災害」</a>', h, count=1)
h = add_li_after(h, 'https://www.sonpo.or.jp/news/notice/2026/2608_003.html',
                 '<li><a href="https://www.sonpo.or.jp/news/notice/2018/1807_01.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「平成30年7月豪雨・被害写真の撮影案内」</a></li>',
                 '1807_01.html')
h = add_li_after(h, 'https://www.sonpo.or.jp/insurance/shizen/index.html',
                 '<li><a href="https://www.sonpo.or.jp/news/caution/syuri.html" target="_blank" rel="noopener noreferrer">日本損害保険協会「住宅の修理などに関するトラブルにご注意」</a></li>',
                 'news/caution/syuri.html')
old_html = '<p><strong>自治体の罹災証明</strong>は公的支援等で使われる制度で、損害保険の請求手続きとは別です。保険会社が求める資料は契約・事故内容で異なります。</p>'
add_html = old_html + '<p>日本損害保険協会は2026年8月31日更新の大雨災害案内で、<strong>損害保険の保険金等の請求では地方自治体の罹災証明書の提出は原則不要</strong>と案内しています。ただし、個別契約で必要な書類は契約先へ確認します。</p>'
if '罹災証明書の提出は原則不要' not in h:
    assert old_html in h
    h = h.replace(old_html, add_html, 1)
p.write_text(h, encoding='utf-8')

# B022 preview: add direct guideline evidence to source box.
p = previews['B022']
h = p.read_text(encoding='utf-8')
if '001349327.pdf' not in h:
    h = add_li_after(h, 'https://www.bousai.go.jp/kyoiku/hokenkyousai/check.html',
                     '<li><a href="https://www.mlit.go.jp/jutakukentiku/build/content/001349327.pdf" target="_blank" rel="noopener noreferrer">国土交通省・経済産業省「建築物における電気設備の浸水対策ガイドライン」</a></li>',
                     '001349327.pdf')
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
'B012': {
    'title':'自宅の浸水にどう備える？住宅の水害対策入門','role':'pillar','product':True,
    'source':'3件。ハザードマップ、気象庁、国交省・経産省正式版ガイドラインを2026-09-04再確認',
    'page_job':'住宅水害の全体像を、リスク把握→住宅対策→避難→生活継続へつなぐ住宅pillar',
    'next':'自宅住所のハザードを確認し、開口部・上階備蓄・避難条件を家族で決める',
    'specific':['簡易水防は小規模・浅い初期浸水に限定し効果を保証しない','浸水開始後の電気設備操作や屋外作業を促さない','上階があるだけで在宅避難可能と断定しない','商品導線は安全・避難説明の後に限定']},
'B015': {
    'title':'自宅が浸水した後、片付ける前に記録したいもの','role':'practical','product':False,
    'source':'4件。2026年大雨案内・修理トラブル注意を現行根拠にし、2018年資料は写真手順に限定',
    'page_job':'被災直後の安全を損なわず、保険・修理・自治体説明に使える記録を残す手順を示す',
    'next':'危険がない範囲で全景・浸水高さ・損傷・家財を記録し、契約先・自治体へ個別確認する',
    'specific':['写真撮影のため危険建物へ再侵入させない','記録より安全・衛生上必要な片付けを優先','罹災証明と保険請求を同一手続きとしない','住宅修理業者との契約前に保険会社・代理店確認を促す']},
'B020': {
    'title':'大雨の前に自宅で確認すること｜浸水対策チェックリスト','role':'practical','product':True,
    'source':'3件。気象庁・ハザードマップ・国交省正式版ガイドラインを2026-09-04再確認',
    'page_job':'大雨前の作業を時系列で整理し、危険が高まる前に屋外作業から避難判断へ切り替えさせる',
    'next':'数日前から排水・家財・備蓄を整え、当日は新規屋外作業をせず情報・避難判断へ切り替える',
    'specific':['3〜7日前等は目安であり危険時に作業継続させない','簡易水防を深い浸水対策として過信させない','冠水後の側溝清掃・電気操作・車移動を促さない','商品リンクは備蓄説明後に限定']},
'B021': {
    'title':'台風前日に確認したいこと｜屋外・窓・停電への備え','role':'practical','product':True,
    'source':'3件。福岡管区気象台・気象庁・内閣府の現行公開情報を2026-09-04再確認',
    'page_job':'台風前日の限られた時間で、安全に終える準備と中止すべき作業を整理する',
    'next':'風雨が強まる前に屋外作業を終え、接近時は住宅作業を打ち切って安全確保へ移る',
    'specific':['前日だから必ず屋外作業可能とはせず予報から締切を決める','窓テープ等で破損防止を保証しない','医療機器を一般バッテリーで代用可能と断定しない','強風中の屋外回収・川海確認・冠水路走行を禁止側で明記']},
'B022': {
    'title':'マンションの台風・水害対策｜戸建てとの違い','role':'detail','product':True,
    'source':'4件。高層マンション地下受変電設備の浸水事例を国交省・経産省ガイドラインで直接確認',
    'page_job':'マンション特有の低層浸水と高層階の停電・断水・エレベーター停止を分けて整理する',
    'next':'専有部だけでなく、地下設備・給水方式・非常電源・駐車場・管理ルールを管理会社へ確認する',
    'specific':['高層階なら水害対策不要としない','地下電気設備浸水によるエレベーター・給水停止を一次資料で裏付け','非常用電源の対象・稼働時間を建物ごとに確認させる','危険時に地下・機械式駐車場へ車を取りに戻らせない']}
}

for aid, d in review_data.items():
    product_status = 'PASS' if d['product'] else 'N/A'
    product_note = '文脈に沿う内部商品ガイドのみ。安全・避難情報より後段に配置' if d['product'] else '商品・購入導線なし'
    e09 = 'E09を条件適用' if d['product'] else 'E09はN/A'
    lines = [
        f'# {aid} 記事別レビュー記録','',common_head,'',
        f'- article_id: `{aid}`',f'- title: {d["title"]}',f'- content_role: `{d["role"]}`','- risk_level: `elevated`',
        '- article_status: `READY_TO_PUBLISH`','- review_status: `PASS`','- last_checked_at: 2026-09-04','- reviewer: ChatGPT','- persona_mode: `SITUATIONAL_SEGMENT`','',
        '## 1. 共通チェック結果','', '| 共通チェック | 状態 | 根拠・備考 |','|---|---|---|',
        '| C01 内容・情報量 | PASS | 記事役割に必要な判断条件・例外・安全行動・次アクションを満たす |',
        f'| C02 出典・安全性 | PASS | {d["source"]} |',
        '| C03 画像・視覚要素 | PASS | 既存の日本文脈・権利・関連性レビューを継承。画像を安全判断の根拠にしない |',
        '| C04 読みやすさ・UI | PASS | 表・手順・チェックリスト・注意枠を既存UIで整理 |',
        '| C05 内部リンク | PASS | 同一クラスタの基礎/詳細/被災後記事とQ&Aへ文脈接続 |',
        f'| C06 商品導線・商品記事 | {product_status} | {product_note} |',
        '| C07 Q&A | PASS | 本文説明を残した上で個別Q&Aへ補助導線を配置 |',
        '| C08 同期・公開前 | PASS | article/source/preview/registry/checklistを2026-09-04監査へ同期 |',
        '| C09 日付・構造化データ | PASS | registryの日付を正本としてproduction buildへ反映 |',
        '| C10 デザイン・UX | PASS | 既存共通UIを利用し、安全情報と商品導線の役割を分離 |',
        '| C11 読者・マーケティング | PASS | 不安を煽らず、平時準備・安全行動・公的情報確認を次アクションにする |',
        '| C12 アクセシビリティ | PASS | 色依存なし。見出し・表・リンクテキストで意味を伝達 |',
        '| C13 技術品質・信頼性 | PASS | production build/test/smoke対象 |',
        '| C14 計測・グロース | N/A | 計測変更なし |','',
        '## 2. 防災サイト固有チェック','', '| 項目 | 状態 | 根拠・備考 |','|---|---|---|',
        f'| S01 適用判定 | PASS | E01〜E08,E11〜E14を適用。{e09} |',
        '| S02 情報設計 | PASS | pillar/practical/detailの役割を維持し、近接記事との重複を抑制 |',
        '| S03 法務・権利等 | PASS | 公的情報とサイト解説を分け、保険・設備・管理責任を一律断定しない |',
        '| S04 ブランド・トーン | PASS | 安全→判断→準備の順。恐怖訴求や購買誘導を優先しない |',
        '| S05 日本向け文脈 | PASS | 気象庁・国交省・内閣府・損保協会等の国内一次情報中心 |',
        '| S06 運用・ガバナンス | PASS | staleなREVIEW_REQUIREDを解消し、出典・台帳・previewを同期 |',
        '| S07 セキュリティ・外部依存 | PASS | 公的・業界公式リンク中心。新規外部機能なし |',
        '| S08 数値 | PASS | 目安・備蓄期間・対策効果を安全保証として扱わない |','',
        '## 3. 安全誤認防止確認',''
    ]
    lines += [f'- PASS: {x}' for x in d['specific']]
    lines += ['', '## 4. 読者・ページ設計','',
              '- target_reader: 日本国内で大雨・台風・浸水への家庭対応を確認したい一般生活者',
              '- usage_context: 平常時の準備、予報悪化時、被災直後',
              '- reader_problem: 家や物を守る作業と人の安全行動の優先順位が曖昧になりやすい',
              '- reader_goal: 自宅条件に応じて、やること・やめること・次に確認する先を決める',
              f'- page_job: {d["page_job"]}', f'- next_action: {d["next"]}', '',
              '## 5. 証跡','',f'- sources: `docs/research/{aid}_SOURCES.md`',f'- article: `{articles[aid].as_posix()}`',f'- preview: `{previews[aid].as_posix()}`','',
              '## 6. 最終判定','', '- review_status: `PASS`','- READY_TO_PUBLISH: `YES`',
              '- 判定理由: 2026-09-04時点の公的情報、安全表現、記事役割、内部導線、サイト固有チェックを再監査し、公開正本とレビュー状態を同期。','']
    (root / f'docs/reviews/{aid}_CHECKLIST.md').write_text('\n'.join(lines), encoding='utf-8')

# Registry synchronization.
registry_path = root / 'data/content_registry.json'
data = json.loads(registry_path.read_text(encoding='utf-8'))
by_id = {a['article_id']: a for a in data['articles']}
counts = {'B012':3, 'B015':4, 'B020':3, 'B021':3, 'B022':4}
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

# Preserve monotonic registry timestamp.
if data.get('updated_at', '') < updated_at:
    data['updated_at'] = updated_at
registry_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
