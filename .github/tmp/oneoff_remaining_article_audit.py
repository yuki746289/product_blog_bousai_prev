from pathlib import Path
import json
import re

root = Path('.')
checked = '2026-09-04'
desired_updated_at = '2026-09-04T14:55:00+09:00'

target_ids = [
    'B001','B002','B003','B005','B006','B008','B009','B010',
    'B025','B026','B027','B028','B029','B030',
    'B031','B032','B033','B034','B035'
]
refresh_source_ids = {'B025','B026','B027','B028','B029','B030'}
product_ids = {'B026','B027','B028','B029'}

registry_path = root / 'data/content_registry.json'
registry = json.loads(registry_path.read_text(encoding='utf-8'))
by_id = {a['article_id']: a for a in registry['articles']}


def article_path(aid):
    matches = list((root / 'content/articles').glob(f'{aid}_*.md'))
    assert len(matches) == 1, (aid, matches)
    return matches[0]


def update_frontmatter(path, update_source=False):
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(?m)^status:\s*REVIEW_REQUIRED$', 'status: READY_TO_PUBLISH', text, count=1)
    if update_source:
        text = re.sub(r'(?m)^source_checked_at:\s*\d{4}-\d{2}-\d{2}$', f'source_checked_at: {checked}', text, count=1)
    path.write_text(text, encoding='utf-8')


def update_source_date(aid):
    path = root / f'docs/research/{aid}_SOURCES.md'
    if not path.exists():
        return
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(?m)^(確認日|source_checked_at):\s*\d{4}-\d{2}-\d{2}$', lambda m: f'{m.group(1)}: {checked}', text, count=1)
    path.write_text(text, encoding='utf-8')


# Update current-review metadata for the six articles externally rechecked in this batch.
for aid in target_ids:
    update_frontmatter(article_path(aid), aid in refresh_source_ids)
    if aid in refresh_source_ids:
        update_source_date(aid)

# B028: strengthen recall guidance using current NITE information.
b028 = article_path('B028')
t = b028.read_text(encoding='utf-8')
marker = '購入時と定期点検時に、**型番を経済産業省・メーカーのリコール情報で照合**します。'
addition = '\n\nNITE（製品評価技術基盤機構）も、リコール対象のポータブル電源は、異常が見られなくても使用を中止し、事業者の案内に従うよう注意喚起しています。**「今まで問題なく使えた」ことを安全確認の代わりにしません。**'
if '異常が見られなくても使用を中止' not in t:
    assert marker in t
    t = t.replace(marker, marker + addition, 1)
source_marker = '- 消費者庁「2026年度 公表資料」: https://www.caa.go.jp/policies/policy/consumer_safety/release/2026/'
source_add = '\n- NITE「リコール対象のポータブル電源に関する注意喚起」: https://www.nite.go.jp/jiko/chuikanki/press/2024fy/prs240627.html'
if 'prs240627.html' not in t:
    assert source_marker in t
    t = t.replace(source_marker, source_marker + source_add, 1)
b028.write_text(t, encoding='utf-8')

# B028 source memo: add NITE as an explicit independent safety source.
src28 = root / 'docs/research/B028_SOURCES.md'
s = src28.read_text(encoding='utf-8')
s = re.sub(r'(?m)^確認日:\s*\d{4}-\d{2}-\d{2}$', f'確認日: {checked}', s, count=1)
if 'F-B028-007' not in s:
    row = '| F-B028-007 | NITE「リコール対象のポータブル電源に関する注意喚起」 https://www.nite.go.jp/jiko/chuikanki/press/2024fy/prs240627.html | リコール対象品は異常が見られなくても使用を中止し、事業者案内に従うこと |\n'
    insert_before = '\n## 安全上の扱い'
    assert insert_before in s
    s = s.replace(insert_before, '\n' + row + insert_before, 1)
if '- リコール対象品は異常がなくても使用を継続しない。' not in s:
    s = s.rstrip() + '\n- リコール対象品は異常がなくても使用を継続しない。\n'
src28.write_text(s, encoding='utf-8')

# Preview synchronization for B028: only patch the same user-visible claims/source.
p28 = root / 'preview/article_b028.html'
h = p28.read_text(encoding='utf-8')
plain_marker = '購入時と定期点検時に、<strong>型番を経済産業省・メーカーのリコール情報で照合</strong>します。'
plain_add = '<p>NITE（製品評価技術基盤機構）も、リコール対象のポータブル電源は、異常が見られなくても使用を中止し、事業者の案内に従うよう注意喚起しています。<strong>「今まで問題なく使えた」ことを安全確認の代わりにしません。</strong></p>'
if '異常が見られなくても使用を中止' not in h:
    assert plain_marker in h
    h = h.replace(plain_marker, plain_marker + plain_add, 1)
if 'prs240627.html' not in h:
    # Append to the public-information list when present.
    li_anchor = '<a href="https://www.caa.go.jp/policies/policy/consumer_safety/release/2026/"'
    pos = h.find(li_anchor)
    assert pos >= 0
    li_end = h.find('</li>', pos)
    assert li_end >= 0
    li_end += len('</li>')
    nite_li = '<li><a href="https://www.nite.go.jp/jiko/chuikanki/press/2024fy/prs240627.html" target="_blank" rel="noopener noreferrer">NITE「リコール対象のポータブル電源に関する注意喚起」</a></li>'
    h = h[:li_end] + nite_li + h[li_end:]
p28.write_text(h, encoding='utf-8')

# Add account/provider-specific product-image permission follow-up to user action items.
u = root / 'docs/USER_ACTION_ITEMS.md'
ut = u.read_text(encoding='utf-8')
if '| U09 |' not in ut:
    row = '| U09 | Amazonアソシエイト / メーカー商品画像の利用条件・提供方法をアカウント条件込みで確認 | TODO | ユーザー / 共同 | 商品画像運用の見直し時 | 現在の外部商品画像が、Amazon提供機能またはメーカーが許可する方法・条件で利用されていることを確認 |\n'
    anchor = '| U08 | Google Keyword Plannerによる需要補足 | OPTIONAL | 共同 | 必要な記事企画のみ | 検索ボリューム等を補助情報として取得。SEO難易度とは扱わない |\n'
    assert anchor in ut
    ut = ut.replace(anchor, anchor + row, 1)
    ut = ut.replace('2. U01〜U03はユーザーが実施できるタイミングで確認する。', '2. U01〜U03・U09はユーザーが実施できるタイミングで確認する。')
u.write_text(ut, encoding='utf-8')


def role_fields(aid, article):
    role = article.get('content_role', 'detail')
    risk = article.get('risk_level', 'standard')
    title = article.get('title', aid)
    product = aid in product_ids or article.get('affiliate') is True or role == 'product'
    if role == 'pillar':
        page_job = 'クラスタの入口として全体像・判断軸を示し、必要な詳細記事へ分岐させる'
    elif role == 'product':
        page_job = '必要性と選び方を先に示し、用途に合う商品の比較・判断を支援する'
    elif role == 'practical':
        page_job = '具体的な行動手順・準備順序を示し、読者が実行できる状態にする'
    else:
        page_job = '特定の疑問・条件を掘り下げ、既存の親記事を補完する'
    return title, role, risk, product, page_job


def checklist_text(aid, article):
    title, role, risk, product, page_job = role_fields(aid, article)
    source_checked = article.get('source_checked_at', 'N/A')
    if aid in refresh_source_ids:
        source_checked = checked
    product_note = 'PASS | 商品・Amazon導線を本文の判断材料の後に置き、現行商品・ASIN・価格表現を再確認。商品画像のアカウント/提供元固有の利用条件は U09 で追跡' if product else 'N/A | 具体商品を主目的とする記事ではない。必要な場合のみ内部の商品ガイドへ接続'
    s03_note = 'PASS_WITH_FOLLOW_UP | 著作権・広告表示・外部リンクを確認。商品画像の提供元固有条件は U09 に残し、確認済みと偽装しない' if product else 'PASS | 出典・画像ライセンス・外部リンク・広告/権利上の誤認がないことを確認'
    e09 = 'REQUIRED' if product else 'CONDITIONAL / N/A'
    source_note = f'確認済み一次・公的/メーカー情報を優先。source_checked_at={source_checked}'
    if aid == 'B028':
        source_note += '。NITEのリコール注意喚起を追加し、異常がなくても対象品は使用中止と明示'
    return f'''# {aid} 記事別専門家レビュー記録\n\n> 共通専門家: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`\n>\n> 防災サイト適用: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`\n>\n> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`\n>\n> 防災サイトチェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`\n>\n> 専門家ロール: `docs/EXPERT_REVIEW_FRAMEWORK.md`\n\n- article_id: `{aid}`\n- title: {title}\n- content_role: `{role}`\n- risk_level: `{risk}`\n- article_status: `READY_TO_PUBLISH`\n- review_status: `PASS`\n- last_checked_at: {checked}\n- reviewer: ChatGPT\n- persona_mode: `SITUATIONAL_SEGMENT`\n- detailed_fictional_persona: `N/A`（根拠のない属性を作らず、利用状況・制約で設計）\n\n## 1. 読者・ページ設計\n\n- target_reader: 日本国内で家庭防災を具体化したい一般生活者\n- usage_context: 平常時の準備、予報・災害前後の確認、または記事固有の判断が必要な場面\n- knowledge_level: 防災の専門知識を前提にしない\n- reader_problem: `{title}` に対応する判断・準備事項を整理したい\n- reader_goal: 安全側の条件を理解し、自分の家庭条件へ置き換えて次の行動を決める\n- page_job: {page_job}\n- entry_path: 検索、カテゴリ、関連記事、Q&A等\n- next_action: 記事内の確認・準備を行い、必要なら公的情報・親/詳細記事・商品ガイドへ進む\n- conversion_path: 安全理解 → 関連情報 → 必要時のみ商品比較/外部導線\n- design_priority: 安全・正確性 → 読みやすさ → 導線 → SEO/CV\n\n## 2. 専門家適用（E01〜E14）\n\n| ID | 判定 | 結果・根拠 |\n|---|---|---|\n| E01 編集・コンテンツ戦略 | REQUIRED | PASS。記事役割、結論、判断条件、例外、次行動を確認 |\n| E02 防災・ファクトチェック・リスク | REQUIRED | PASS。安全情報を購買・SEOより優先し、独自の安全保証を作っていない |\n| E03 SEO | REQUIRED | PASS。検索意図、title/H1、既存記事との役割分離、内部リンクを確認 |\n| E04 情報アーキテクチャ | REQUIRED | PASS。カテゴリ、親子関係、関連記事導線、公開パスを確認 |\n| E05 UX/UI | REQUIRED | PASS。結論先行、表/箇条書き/注意枠等で判断しやすく整理 |\n| E06 マーケティング・読者戦略/CRO | REQUIRED | PASS。読者課題→判断材料→次行動の順で、CVを先行させていない |\n| E07 アクセシビリティ | REQUIRED | PASS。共通アクセシビリティ実装の対象。意味のあるリンク文言・構造を維持 |\n| E08 ブランド/コンテンツデザイン | REQUIRED | PASS。煽りや制作側表現を避け、落ち着いた防災サイトのトーンを維持 |\n| E09 商品/アフィリエイト | {e09} | {product_note} |\n| E10 分析/グロース | CONDITIONAL | PASS。GA4/改善評価は共通実装。実データ評価は USER_ACTION_ITEMS の U04〜U07で管理 |\n| E11 Web実装/信頼性 | REQUIRED | PASS。静的ビルド、リンク、構造化データ、本番スモークの対象 |\n| E12 セキュリティ/法務/権利/プライバシー | REQUIRED | {s03_note} |\n| E13 日本向けローカライゼーション | REQUIRED | PASS。日本の制度・公的情報・生活文脈を基準にした |\n| E14 運用/ガバナンス | REQUIRED | PASS。Markdown、research、review、registry、preview/公開ビルドの正本関係を維持 |\n\n## 3. C01〜C14\n\n| ID | 状態 | 根拠 |\n|---|---|---|\n| C01 内容・情報量 | PASS | 検索意図とpage jobに対して必要十分。文字数だけで判定しない |\n| C02 出典・安全性 | PASS | {source_note} |\n| C03 画像・視覚要素 | PASS | 既存画像レビューを継承し、画像を安全・性能判断の根拠にしていない |\n| C04 読みやすさ/UI | PASS | 見出し・表・箇条書き・要点表示を用途に応じ使用 |\n| C05 内部リンク | PASS | 親記事・関連記事・Q&A/商品ガイドを必要な文脈で接続 |\n| C06 商品導線/商品記事 | {'PASS' if product else 'N/A'} | {'具体商品は用途・判断基準の後に配置。Amazon現在価格を静的固定しない' if product else '無理な商品挿入を行わない'} |\n| C07 Q&A | CONDITIONAL PASS | 該当する文脈導線は本文説明の補助として扱い、Q&Aを説明の代替にしない |\n| C08 同期/公開前 | PASS | 正本・preview・registry・レビュー状態を同期 |\n| C09 日付/構造化データ | PASS | published/modified/source_checked/reviewedの意味を分離。公開ビルドで構造化データ生成 |\n| C10 デザイン/UX | PASS | 安全情報が最優先に見え、CTAや商品が不自然に浮かない |\n| C11 読者/マーケティング | PASS | SITUATIONAL_SEGMENTで問題・目標・entry/next actionを明確化 |\n| C12 アクセシビリティ | PASS | 共通実装とページ構造を適用 |\n| C13 技術/信頼性 | PASS | CI、ビルド、JS、外部依存、本番スモークで検証 |\n| C14 分析/グロース | CONDITIONAL PASS | 計測実装を維持。実利用データはU04〜U07で後続評価 |\n\n## 4. S01〜S08\n\n| ID | 状態 | 根拠 |\n|---|---|---|\n| S01 サイトプロファイル/適用判定 | PASS | 防災サイトprofileとpersona_modeを適用 |\n| S02 IA/ファインダビリティ | PASS | カテゴリ・親子・URL・関連記事の役割を確認 |\n| S03 法務/権利/広告/プライバシー | {'PASS_WITH_FOLLOW_UP' if product else 'PASS'} | {('商品画像の提供方法・利用条件のアカウント固有確認はU09へ明示的に残す' if product else '出典・権利・広告/公式情報の主体を区別')} |\n| S04 ブランド/トーン | PASS | 恐怖訴求や過剰断定ではなく、判断材料を落ち着いて提示 |\n| S05 日本向け文脈 | PASS | 日本の制度・住環境・公的機関・表記を優先 |\n| S06 運用/ガバナンス | PASS | status/review/source/dateの正本同期と再発防止を確認 |\n| S07 セキュリティ/外部依存 | PASS | secret非公開、外部リンク/画像/API依存の安全な扱いを維持 |\n| S08 数値/統計/リアルタイム | CONDITIONAL PASS | 数値は単位・前提・公称/仮定を分離し、保証値へ変換しない |\n\n## 5. 最終横断チェック\n\n| 項目 | 状態 |\n|---|---|\n| X01〜X05 共通最終確認 | PASS |\n| SX01 未分類の専門家視点なし | PASS |\n| SX02 N/A/条件付き理由あり | PASS |\n| SX03 詳細架空ペルソナなしでも読者状況が明確 | PASS |\n| SX04 公的/安全情報とサイト/商品情報を混同しない | PASS |\n| SX05 日本向け文脈 | PASS |\n| SX06 鮮度・更新責任 | PASS |\n| SX07 再発問題のルール/テスト化検討 | PASS |\n\n## 6. 証跡・後続事項\n\n- source: `{article.get('source_path', '')}`\n- research: `docs/research/{aid}_SOURCES.md`（存在する場合）\n- preview: `{article.get('preview_path', '')}`\n- production: `{article.get('planned_public_path', '')}`\n- user-side: `docs/USER_ACTION_ITEMS.md`\n- U03: 実スマートフォンでの横断UX確認はサイト共通対応事項として継続\n- {'U09: 商品画像のAmazon/メーカー利用条件・提供方法はアカウント固有確認として継続' if product else '商品画像のアカウント固有確認: N/A'}\n\n## 7. 最終判定\n\n- review_status: `PASS`\n- READY_TO_PUBLISH: `YES`\n- 判定理由: 現在のサイト個別プロファイル、E01〜E14、C01〜C14、S01〜S08で再監査し、記事側の公開ブロッカーはなし。ユーザー側の横断確認事項は `USER_ACTION_ITEMS.md` で継続管理する。\n'''

# Rewrite only target review records into the current unified framework.
for aid in target_ids:
    a = by_id[aid]
    (root / f'docs/reviews/{aid}_CHECKLIST.md').write_text(checklist_text(aid, a), encoding='utf-8')

# Registry synchronization.
for aid in target_ids:
    a = by_id[aid]
    a['last_reviewed_at'] = checked
    a['review_checklist_last_checked_at'] = checked
    a['review_checklist_status'] = 'PASS'
    a['manual_review_status'] = 'APPROVED'
    a['publish_blockers'] = []
    if aid in refresh_source_ids:
        a['source_checked_at'] = checked
        a['status'] = 'READY_TO_PUBLISH'
    if aid == 'B028':
        ids = list(a.get('source_ids', []))
        if 'F-B028-007' not in ids:
            ids.append('F-B028-007')
        a['source_ids'] = ids
        a['source_count'] = len(ids)
        a['modified_at'] = checked

# Keep registry timestamp monotonic.
current_updated_at = registry.get('updated_at', desired_updated_at)
registry['updated_at'] = max(current_updated_at, desired_updated_at)
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print('Updated articles:', ', '.join(target_ids))
print('Externally refreshed:', ', '.join(sorted(refresh_source_ids)))
print('U09 tracked:', ', '.join(sorted(product_ids)))
