# Issue #18 — Phase 2 驗證與 Self-Review Evidence

日期：2026-11-06（Asia/Taipei）。執行者／唯一 accountable Builder：Codex。
實作 Commit：`d32c5b57d4f5313a247fa34db547d08463c078a5`。
比較基準：`7e530cdc818044ae4f760a021a331f888f993e43`。
授權：[AUTHORIZATION.md](AUTHORIZATION.md)；核准 Plan 固定 SHA：`70acc21a5d15a9061c8b2a896b5b9a9987cda7cd`。

## 已執行檢查

| 方法 | 實際結果 | 限制 |
|---|---|---|
| `python3 -m unittest discover -s scripts -p 'test_*.py'` | PASS，27 tests，exit 0 | 不代表所有函式式測試都被發現 |
| `python3 scripts/test_merge_lifecycle.py` | PASS，3 組；runner 回報 6+7+3 情境，exit 0 | 離線邏輯測試，未執行真實 Merge |
| `python3 scripts/test_two_defects_fix.py` | PASS，6 項，exit 0 | 模擬 API 參數與歸檔文字處理，非真實 API 寫入 |
| 既有 venv `python -m mkdocs build --strict --site-dir /tmp/clh-issue18-site` | PASS，MkDocs 1.6.1，exit 0 | docs/development 頁面不在 nav 的既有 INFO 保留；不新增導覽；非教材品質驗收 |
| 建置 HTML 結構讀取 | PASS，安裝說明含表頭＋8 資料列及分工文字 | 非瀏覽器視覺驗收；根目錄 README 不在 MkDocs 輸入內 |
| `git diff --check` | PASS | 僅空白與 patch 格式 |
| 下列一次性 Python 檢查 | PASS，YAML、使用到的官方 schema 子集、契約、路徑保留、授權規則保留 | 非 GitHub 官方驗證服務；不宣稱完整未使用 schema 支援 |

Schema 依 2026-11-06 重新讀取的 GitHub 官方文件核對：
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema

檢查含頂層必要欄位／型別、名稱及 ID 唯一性、markdown／textarea 支援屬性、必填布林、無預填成果，另比對本案欄位契約。只解析 YAML 不算 schema 完成。GitHub 表單目前尚未合併，實際 chooser／render／必填行為為 PENDING。

## 一次性檢查原文與輸出

以下為本次在 `/tmp/issue18-verify.py` 執行的檢查原文，保存作為 Evidence，不新增正式 scripts/tests 或 CI。可將程式碼存至暫存路徑，在本 Repo 根目錄以已安裝 PyYAML 的 Python 執行。

```python
from pathlib import Path
import re,subprocess,sys,yaml
BASE='7e530cdc818044ae4f760a021a331f888f993e43'
APPROVED='70acc21a5d15a9061c8b2a896b5b9a9987cda7cd'
class UniqueLoader(yaml.SafeLoader): pass
def mapping(loader,node,deep=False):
    out={}
    for k,v in node.value:
        key=loader.construct_object(k,deep=deep)
        assert key not in out, f'重複 YAML key: {key}'
        out[key]=loader.construct_object(v,deep=deep)
    return out
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
def parse(s): return yaml.load(s,Loader=UniqueLoader)
paths=['.github/ISSUE_TEMPLATE/01-agent-task.yml','.github/ISSUE_TEMPLATE/02-learning-record.yml']
forms=[parse(Path(p).read_text()) for p in paths]
assert len({f['name'] for f in forms})==2
for path,form in zip(paths,forms):
    assert set(form)=={'name','description','title','body'}
    assert all(isinstance(form[k],str) and form[k].strip() for k in ('name','description','title'))
    assert isinstance(form['body'],list) and form['body']
    ids=[];labels=[]
    for field in form['body']:
        assert isinstance(field,dict)
        if field['type']=='markdown':
            assert set(field)=={'type','attributes'}
            assert set(field['attributes'])=={'value'} and isinstance(field['attributes']['value'],str)
        else:
            assert field['type']=='textarea' and set(field)=={'type','id','attributes','validations'}
            assert re.fullmatch('[A-Za-z0-9_-]+',field['id'])
            assert set(field['attributes']) <= {'label','description','placeholder','value','render'}
            assert field['attributes']['label'].strip()
            assert all(isinstance(v,str) for v in field['attributes'].values())
            assert 'value' not in field['attributes'], '不得預填成果'
            assert set(field['validations'])=={'required'} and type(field['validations']['required']) is bool
            ids.append(field['id']);labels.append(field['attributes']['label'])
    assert len(ids)==len(set(ids)) and len(labels)==len(set(labels))
    print('PASS YAML／schema 使用子集：',path,'；欄位數',len(ids))
def contract(f): return [(x['id'],x['type'],x['validations']['required']) for x in f['body'] if x['type']!='markdown']
old=parse(subprocess.check_output(['git','show',BASE+':'+paths[0]],text=True))
assert contract(forms[0])==contract(old)
assert contract(forms[0])==[(x,'textarea',i<4) for i,x in enumerate(['what','why','acceptance','boundary','references'])]
expected=['subject-course-unit','learning-objectives','source-materials','v2-consolidation','v3-code-first','content-quality-evidence','v2-v3-integration','publication-archive']
assert contract(forms[1])==[(x,'textarea',i<3) for i,x in enumerate(expected)]
assert parse(Path('.github/ISSUE_TEMPLATE/config.yml').read_text())=={'blank_issues_enabled':False}
print('PASS：工程欄位契約維持；學習八欄位 3 必填／5 選填；兩入口與設定')
sys.path.insert(0,'scripts')
from merge_lifecycle import verify_pr_issue_linkage
assert verify_pr_issue_linkage('Issue: #18\n工程變更',18)[0]
assert not verify_pr_issue_linkage('Issue: #180\n',18)[0]
print('PASS：既有 PR／Issue 關聯精確比對，無須更動既有 Issue')
allowed=set(paths+['.github/ISSUE_TEMPLATE/config.yml','.github/PULL_REQUEST_TEMPLATE.md','GOVERNANCE.md','AGENTS.md','INSTALL.md','README.md','docs/development/ISSUE_TEMPLATE_INSTALL.md'])
basefiles=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE],text=True).splitlines()
for f in basefiles:
    if f in allowed or f.startswith('records/ISSUE-18/'): continue
    assert Path(f).read_bytes()==subprocess.check_output(['git','show',BASE+':'+f]), f
assert Path('records/ISSUE-18/PLAN.md').read_bytes()==subprocess.check_output(['git','show',APPROVED+':records/ISSUE-18/PLAN.md'])
print('PASS：授權以外基準檔案逐檔位元組一致；已核准 Plan 原貌保留')
gov=Path('GOVERNANCE.md').read_text();oldgov=subprocess.check_output(['git','show',BASE+':GOVERNANCE.md'],text=True)
assert gov.split('## 驗證與 Merge\n')[1].split('## Rollback')[0]==oldgov.split('## 驗證與 Merge\n')[1].split('## Rollback')[0]
assert 'Merge 不代表部署授權。Pages 僅有手動入口，執行仍需另行授權；不要求合併前先部署同一 commit。' in gov
print('PASS：既有 Merge／Auto-Merge 及 Deployment 授權規範保留')
pattern=re.compile(r'Claude|Codex|Builder|ChatGPT|V2|V3|Auto.?Merge|自動.*(合併|部署)|deploy|部署|教材.*(創作|實作)|cross.review|opposite.agent|對等|交叉審查',re.I)
rows=['實作工作樹文件搜尋證據；歷史與 archive 排除，docs/development 的 archived-banner 命中供分類而非改寫。']
for f in sorted(set(basefiles)|allowed):
    if f.startswith(('records/','archive/')) or not f.endswith(('.md','.yml','.yaml')):continue
    for i,line in enumerate(Path(f).read_text().splitlines(),1):
        if pattern.search(line):rows.append(f'{f}:{i}:{line}')
Path('/tmp/issue18-matches-after.txt').write_text('\n'.join(rows)+'\n')
print('PASS：已產生逐行文件搜尋，需搭配人工語意判讀')
print('工具：Python',sys.version.split()[0],'PyYAML',yaml.__version__)
```

```text
PASS YAML／schema 使用子集： .github/ISSUE_TEMPLATE/01-agent-task.yml ；欄位數 5
PASS YAML／schema 使用子集： .github/ISSUE_TEMPLATE/02-learning-record.yml ；欄位數 8
PASS：工程欄位契約維持；學習八欄位 3 必填／5 選填；兩入口與設定
PASS：既有 PR／Issue 關聯精確比對，無須更動既有 Issue
PASS：授權以外基準檔案逐檔位元組一致；已核准 Plan 原貌保留
PASS：既有 Merge／Auto-Merge 及 Deployment 授權規範保留
PASS：已產生逐行文件搜尋，需搭配人工語意判讀
工具：Python 3.12.3 PyYAML 6.0.3
```

## 文件一致性判讀

重新列舉現行 Markdown／YAML 並搜尋全部既定關鍵詞；實際逐行輸出見 [MATCHES-AFTER.txt](MATCHES-AFTER.txt)。與原 [Documentation Consistency Matrix](DOCUMENTATION-CONSISTENCY.md) 對照如下；原調查文件未覆寫。

| 原 Matrix 對象 | 本次完成事項／保留理由 | 判定 |
|---|---|---|
| README 角色／stack／內容所有權／V2/V3 | 單一工具中立 Builder；ChatGPT＋Human 創作與核准；GitHub／MkDocs 分工；學習紀錄不強制 PR | PASS |
| README 流程／圖／英文摘要／Issue-first／Merge 清單 | 修正早開 Draft、條件 Plan／Result、授權及現在 head 審查；摘要以繁體中文表述 | PASS |
| README 部署流程 | 手動入口與獨立授權；Self-Review 發現末段仍有舊步驟，提交前已修正 | PASS |
| README 教材規範、v3.1 OS、bootstrap 狀態、roadmap | 無關教學與歷史狀態未改寫；未宣稱新部署驗收 | 保留 |
| GOVERNANCE | 工具中立、唯一責任、分工／學習、交接與再確認；既有風險、Merge／Auto-Merge／Deployment 規範保留 | PASS |
| AGENTS | 同一分工、責任、交接、新 head／base／scope／risk 規範；其他規則保留 | PASS |
| Engineering Task | 保留五個 ID／順序／型別／必填；改工程用途與忠實匯入範例；明示兩工具相同規則 | PASS |
| Learning Record | 八主題、3 必填／5 選填；成果可後續 Comments；無成功預填；不強制工程 PR | PASS |
| config | 僅註解改兩入口，blank_issues_enabled 仍 false | PASS |
| PR Template | 唯一 Builder、選填學習參考、已核准內容參考及交接／重驗欄；授權分離維持 | PASS |
| Issue Forms 安裝說明 | 兩種入口、欄位契約、內容權責、Self-Review、交接、schema 與 UI 分離 | PASS |
| INSTALL | 舊套件／對等 Agent／先複製再核准流程已修正；Claude 相容性段落原樣保留；不授予設定權限 | PASS |
| docs/index、五個 subject index、mkdocs.yml | 無矛盾操作規定且在 scope 外；逐檔位元組相同 | 保留 |
| 四份 workflows、scripts/tests | 逐檔位元組相同；schema／文件修改不重跑真實 Merge／Close／Deploy | 保留 |
| docs/development 三份 ARCHIVED 文件、archive/**、其他 records/** | 原文與證據皆逐檔位元組相同；搜尋命中不作現行規則 | 保留 |

剩餘關鍵詞包括合法工具名稱、既有授權禁令、工具相容性、OS Framework v3.1 及已明確標示 archived 的歷史內容；沒有為追求零命中而重寫歷史。README Mermaid 已逐行檢視節點、引用及授權順序；GitHub 原生 Mermaid 瀏覽器呈現 NOT RUN，未以 MkDocs 成功冒充此項。

## Builder Handoff 桌上情境檢查

此處是 Codex 對文字規則的情境核對，沒有發生實際 Builder 交接，也不是獨立 Review。

| 情境 | 檢查到的規則與應有結果 | 判定 |
|---|---|---|
| Claude Code → Codex、head 不變 | 仍須前後 Builder／完整 SHA／base／scope／risk／已完成／未完成／Evidence／Blockers；接手者重新確認目前 head 與授權 | PASS |
| Codex → Claude Code、head 不變 | 完全相同規則，不因工具品牌豁免 | PASS |
| 任一交接後 head 改變 | 新 head 重新 Self-Review，舊結論不得直接沿用 | PASS |
| base／scope／risk 改變 | 評估影響，重大變動依既有規定修訂 Plan／重新取得授權 | PASS |
| 舊 Evidence 存在但授權不明 | 僅可作待核對來源，不自動移轉 Human 授權；確認前不能放行 | PASS |
| Learning Issue 無 Repository 變更 | 可以僅用 Comments 記錄進度，無工程 PR 必填要求 | PASS |

## 未執行／不適用項目

- `test_final_findings.py` 整體 runner：NOT RUN。包含歷史 PR #12 readback 及已停止自動 recovery 的舊期望；不是本次文件變更驗收，不改寫歷史測試。
- `test_human_review_corrections.py` 整體 runner：NOT RUN。包含舊 recovery 授權模擬／歷史文件期望；相關現行 linkage／concurrency 基線以既有已執行測試及 byte 比對覆蓋。
- `test_runtime_cleanup.py` 整體 runner：NOT RUN。含舊 sed 實作模擬；目前歸檔文字 helper 使用 Template，已執行 six defect tests；不宣稱這些歷史 runner 都通過。
- GitHub 表單實際 UI：PENDING，需另行授權合併後才能驗證預設分支入口。瀏覽器視覺檢查：NOT RUN；本次完成來源與 HTML 結構核對。
- 教材內容／來源品質驗收：未執行，無教材創作或匯入；僅核對角色與來源權責文字。
- 真實 Merge／Close／Deployment：NOT RUN，明確未獲授權。未進行任何 workflow_dispatch。

## Self-Review 結論與 Fresh-Context Challenge

Codex 已核對實作差異、九個路徑、欄位／必填、角色權責、交接雙向情境、所有 Matrix 處置、授權規範保留、實作前 Plan／Human 授權順序。此為 Builder Self-Review，不宣稱獨立 Review、原生 APPROVED 或 Human 驗收。

Fresh-Context Challenge 本次省略：此變更僅限有明確固定 SHA 授權的文件／表單；已採官方 schema 核對、逐檔 scope 比對、現行授權段落比對與交接情境檢查，未改執行權限或工作流。現有剩餘 UI／視覺限制明列且維持 Draft 等待 Human；沒有 Human 指定 challenge。若後續 scope、risk、head 或 Human 要求改變，重新評估，不以本理由免除必要檢查。

結論：本地工程驗證通過，未發現授權範圍內未解實作缺陷。最終 head 的 CI、Result 後紀錄順序檢查與遠端 readback 由 PR 最終 Evidence 綁定；未確認前不可視為全部完成。即使所有工程檢查通過，本次仍不得 Ready／Merge／Close／Deploy。
