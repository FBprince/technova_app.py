# # ORIGINAL CODE

# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast

# # =============================
# # 🌌 Canvas Star Background + Neon Text
# # =============================
# def set_canvas_stars():
#     canvas_html = """
#     <canvas id="star-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1000;"></canvas>
#     <script>
#     const canvas = document.getElementById('star-canvas');
#     const ctx = canvas.getContext('2d');
#     function resize() {
#         canvas.width = window.innerWidth;
#         canvas.height = window.innerHeight;
#     }
#     window.addEventListener('resize', resize);
#     resize();
#     const numStars = 80;
#     const stars = [];
#     for(let i=0;i<numStars;i++){
#         stars.push({
#             x: Math.random()*canvas.width,
#             y: Math.random()*canvas.height,
#             r: Math.random()*2+1,
#             dx: (Math.random()-0.5)*0.3,
#             dy: (Math.random()-0.5)*0.3,
#             alpha: Math.random()
#         });
#     }
#     function draw() {
#         ctx.fillStyle = '#0a0b1c';
#         ctx.fillRect(0,0,canvas.width,canvas.height);
#         for(let s of stars){
#             ctx.beginPath();
#             ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
#             ctx.fillStyle = "rgba(0,255,255,"+s.alpha+")";
#             ctx.fill();
#             s.x += s.dx;
#             s.y += s.dy;
#             s.alpha += (Math.random()-0.5)*0.02;
#             if(s.alpha<0)s.alpha=0;
#             if(s.alpha>1)s.alpha=1;
#             if(s.x<0)s.x=canvas.width;
#             if(s.x>canvas.width)s.x=0;
#             if(s.y<0)s.y=canvas.height;
#             if(s.y>canvas.height)s.y=0;
#         }
#         requestAnimationFrame(draw);
#     }
#     draw();
#     </script>
#     <style>
#     body, [data-testid="stAppViewContainer"] {
#         background-color: #0a0b1c;
#         color: #00f9ff;
#         font-family: 'Orbitron', 'Trebuchet MS', monospace;
#         text-shadow: 0 0 6px #00f9ff, 0 0 12px #00cfff;
#         overflow-x:hidden;
#     }
#     h1,h2,h3,h4,h5,h6 { color:#00f9ff !important; text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff,0 0 24px #00aaff; }
#     p,div,span,label { color:#a0f0ff !important; text-shadow:0 0 4px #00f9ff; }
#     .stButton>button, .stDownloadButton>button {
#         background: linear-gradient(90deg, #00f0ff, #0066ff);
#         color:#02121b;
#         border-radius:10px;padding:8px 14px;
#         font-weight:700;font-family:'Orbitron', monospace;
#         box-shadow:0 8px 24px rgba(0,120,255,0.12);
#         transition: transform .15s ease, box-shadow .15s ease;
#     }
#     .stButton>button:hover, .stDownloadButton>button:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(0,120,255,0.2); }
#     [data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(4,6,20,0.95), rgba(8,12,35,0.95)); color:#EAF9FF; }
#     pre, code { background: rgba(0,20,40,0.4); color: #00f9ff; text-shadow:0 0 4px #00f9ff; }
#     </style>
#     """
#     st.markdown(canvas_html, unsafe_allow_html=True)

# # =============================
# def safe_sentence_split(text: str):
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return pattern.split(text)

# def paragraph_summary(text: str, max_sentences: int = 5):
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     summary_lines = []
#     for para in paragraphs:
#         sentences = safe_sentence_split(para)
#         if sentences:
#             summary_lines.append(sentences[0].strip())
#         if len(summary_lines) >= max_sentences:
#             break
#     return " ".join(summary_lines) if summary_lines else text

# # =============================
# def analyze_python(code: str, summary_length: int = 5):
#     report = {
#         "functions": [],
#         "classes": [],
#         "imports": [],
#         "purpose_summary": "",
#         "errors": [],
#         "warnings": [],
#         "suggestions": []
#     }

#     # Extract imports, functions, classes
#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             report["functions"].append(l.split("(")[0][4:].strip())
#         elif l.startswith("class "):
#             report["classes"].append(l.split("(")[0][6:].strip())
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     report["purpose_summary"] = paragraph_summary(" ".join(safe_sentence_split(code)), max_sentences=summary_length)

#     # Syntax checking
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["suggestions"].append("Check indentation, missing colons, parentheses, or quotes.")
#         return report

#     # Static runtime checks
#     defined_vars = set()
#     called_funcs = set()
#     class FuncVisitor(ast.NodeVisitor):
#         def visit_FunctionDef(self, node):
#             defined_vars.add(node.name)
#             self.generic_visit(node)
#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 called_funcs.add(node.func.id)
#             self.generic_visit(node)
#         def visit_Assign(self, node):
#             for target in node.targets:
#                 if isinstance(target, ast.Name):
#                     defined_vars.add(target.id)
#             self.generic_visit(node)
#         def visit_BinOp(self, node):
#             if isinstance(node.op, (ast.Div, ast.Mod)):
#                 if isinstance(node.right, ast.Constant) and node.right.value == 0:
#                     report["warnings"].append(f"Possible division by zero at line {node.lineno}")
#             self.generic_visit(node)
#     FuncVisitor().visit(tree)

#     # Undefined function calls
#     for func in called_funcs:
#         if func not in defined_vars and func not in dir(__builtins__):
#             report["warnings"].append(f"Call to undefined function '{func}' detected")

#     # General suggestions
#     if not report["errors"]:
#         if report["warnings"]:
#             report["suggestions"].append("Review the warnings above and fix variable or function usage.")
#         else:
#             report["suggestions"].append("No obvious syntax or runtime issues detected. Test your logic.")

#     return report

# # =============================
# def fetch_from_url(url: str) -> str:
#     try:
#         resp = requests.get(url, timeout=12)
#         resp.raise_for_status()
#         ct = resp.headers.get("Content-Type", "")
#         if "text/plain" in ct or url.lower().endswith((".py", ".txt", ".md")):
#             return resp.text
#         if "text/html" in ct:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             for s in soup(["script", "style", "noscript"]):
#                 s.extract()
#             return soup.get_text(separator="\n")
#         return resp.text
#     except Exception as e:
#         return f"❌ Error fetching URL: {str(e)}"

# # =============================
# def copy_button(label: str, text: str, key: str):
#     if text is None: text = ""
#     b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     html_button = f"""
#         <button onclick="navigator.clipboard.writeText(atob('{b64}'))"
#                 style="background:transparent;border:1px solid rgba(255,255,255,0.06);
#                        color: #EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
#                        font-weight:700;box-shadow:0 6px 18px rgba(0,120,255,0.06);">
#             📋 {label}
#         </button>
#     """
#     st.markdown(html_button, unsafe_allow_html=True)

# # =============================
# def main():
#     set_canvas_stars()
#     st.title("🌌 TechNova — Study & Code Assistant")
#     st.caption("Summarize documents, analyze Python code with smart debugging, fetch & explain URLs — neon starry UI")

#     tab1, tab2, tab3 = st.tabs(["📄 Document Summarizer", "💻 Code Analyzer", "🌐 URL Fetch & Explain"])

#     # ----------------------------
#     with tab1:
#         st.subheader("Summarize Documents")
#         text_input = st.text_area("Paste text here:", height=200)
#         uploaded_file = st.file_uploader("Or upload a document (.txt, .md)", type=["txt", "md"])
#         length = st.slider("Summary length (paragraphs)", 1, 10, 3)

#         if st.button("Summarize Document"):
#             content = ""
#             if uploaded_file:
#                 try: content = uploaded_file.read().decode("utf-8")
#                 except: content = uploaded_file.read().decode("latin-1")
#             elif text_input.strip(): content = text_input
#             if not content: st.warning("Paste text or upload a file.")
#             else:
#                 summary = paragraph_summary(content, max_sentences=length)
#                 st.markdown("### 📌 Summary")
#                 st.write(summary)
#                 copy_button("Copy Summary", summary, key="doc_copy")
#                 st.download_button("⬇️ Download Summary", summary, "document_summary.txt", mime="text/plain")

#     # ----------------------------
#     with tab2:
#         st.subheader("Analyze Python Code with Smart Debugging")
#         code_input = st.text_area("Paste Python code here:", height=220)
#         uploaded_code = st.file_uploader("Or upload a Python file (.py)", type=["py"])
#         length_code = st.slider("Summary length (sentences)", 1, 8, 3, key="code_len")

#         if st.button("Analyze Code"):
#             code_str = ""
#             if uploaded_code:
#                 try: code_str = uploaded_code.read().decode("utf-8")
#                 except: code_str = uploaded_code.read().decode("latin-1")
#             elif code_input.strip(): code_str = code_input
#             if not code_str: st.warning("Paste code or upload a Python file.")
#             else:
#                 report = analyze_python(code_str, summary_length=length_code)
#                 st.markdown("### 📊 Code Analysis Report")
#                 st.markdown("**Functions:**")
#                 st.write(", ".join(report["functions"]) if report["functions"] else "_none_")
#                 st.markdown("**Classes:**")
#                 st.write(", ".join(report["classes"]) if report["classes"] else "_none_")
#                 st.markdown("**Imports:**")
#                 if report["imports"]: 
#                     for imp in report["imports"]: st.code(imp)
#                 else: st.write("_none_")
#                 st.markdown("**Purpose summary:**"); st.write(report["purpose_summary"] or "_No summary available_")
#                 st.markdown("**Errors Detected:**")
#                 if report["errors"]: 
#                     for err in report["errors"]: st.error(err)
#                 else: st.write("_No syntax errors detected_")
#                 st.markdown("**Warnings / Runtime Issues:**")
#                 if report["warnings"]:
#                     for w in report["warnings"]: st.warning(w)
#                 else: st.write("_No obvious runtime issues detected_")
#                 st.markdown("**Debugging Suggestions:**")
#                 if report["suggestions"]:
#                     for sug in report["suggestions"]: st.info(sug)

#                 copy_button("Copy Report", str(report), key="code_copy")
#                 st.download_button("⬇️ Download Code Report", str(report), "code_analysis.txt", mime="text/plain")

#     # ----------------------------
#     with tab3:
#         st.subheader("Fetch, Summarize & Explain from URL")
#         url_input = st.text_input("Enter a URL:")

#         if st.button("Fetch & Analyze URL"):
#             if not url_input.strip(): st.warning("Please enter a valid URL.")
#             else:
#                 data = fetch_from_url(url_input.strip())
#                 if data.startswith("❌ Error"): st.error(data)
#                 else:
#                     st.markdown("### 📄 Content Preview")
#                     st.code(data[:1200] + ("..." if len(data) > 1200 else ""), language="text")
#                     is_code = url_input.strip().lower().endswith(".py") or ("def " in data or "class " in data)
#                     if is_code:
#                         st.markdown("### 💻 Code Analysis with Smart Debugging")
#                         report = analyze_python(data, summary_length=5)
#                         st.json(report)
#                         copy_button("Copy Report", str(report), key="url_code_copy")
#                         st.download_button("⬇️ Download Code Report", str(report), "url_code_analysis.txt")
#                     else:
#                         st.markdown("### 📌 Document Summary")
#                         summary = paragraph_summary(data, max_sentences=5)
#                         st.write(summary)
#                         copy_button("Copy Summary", summary, key="url_summary_copy")
#                         st.download_button("⬇️ Download Summary", summary, "url_summary.txt")

# # =============================
# if __name__ == "__main__":
#     main()
















import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import base64
import ast
from collections import Counter

# =============================
# 🌌 Canvas Star Background + Neon Text
# =============================
def set_canvas_stars():
    canvas_html = """
    <canvas id="star-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1000;"></canvas>
    <script>
    const canvas = document.getElementById('star-canvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();
    const numStars = 80;
    const stars = [];
    for(let i=0;i<numStars;i++){stars.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*2+1,dx:(Math.random()-0.5)*0.3,dy:(Math.random()-0.5)*0.3,alpha:Math.random()});}
    function draw(){ctx.fillStyle='#0a0b1c';ctx.fillRect(0,0,canvas.width,canvas.height);for(let s of stars){ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle="rgba(0,255,255,"+s.alpha+")";ctx.fill();s.x+=s.dx;s.y+=s.dy;s.alpha+=(Math.random()-0.5)*0.02;if(s.alpha<0)s.alpha=0;if(s.alpha>1)s.alpha=1;if(s.x<0)s.x=canvas.width;if(s.x>canvas.width)s.x=0;if(s.y<0)s.y=canvas.height;if(s.y>canvas.height)s.y=0;}requestAnimationFrame(draw);}
    draw();
    </script>
    <style>
    body, [data-testid="stAppViewContainer"] {background-color: #0a0b1c;color: #00f9ff;font-family: 'Orbitron', monospace;text-shadow: 0 0 6px #00f9ff;}
    h1,h2,h3,h4,h5,h6 {color:#00f9ff !important;text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff,0 0 24px #00aaff;}
    p,div,span,label {color:#a0f0ff !important;text-shadow:0 0 4px #00f9ff;}
    .stButton>button, .stDownloadButton>button {background: linear-gradient(90deg, #00f0ff, #0066ff);color:#02121b;border-radius:10px;padding:8px 14px;font-weight:700;box-shadow:0 8px 24px rgba(0,120,255,0.12);}
    .stButton>button:hover, .stDownloadButton>button:hover {transform: translateY(-3px); box-shadow: 0 16px 36px rgba(0,120,255,0.2);}
    [data-testid="stSidebar"] {background: linear-gradient(180deg, rgba(4,6,20,0.95), rgba(8,12,35,0.95)); color:#EAF9FF;}
    pre, code {background: rgba(0,20,40,0.4); color: #00f9ff; text-shadow:0 0 4px #00f9ff;}
    </style>
    """
    st.markdown(canvas_html, unsafe_allow_html=True)

# =============================
# Utilities
# =============================
STOPWORDS = set(
    "a an and are as at be but by for if in into is it no not of on or such that the their then there these they this to was will with you your from our we he she his her its were been being than also can could should would may might have has had do does did done just over under more most other some any each many few those them which who whom whose where when why how".split()
)

def safe_sentence_split(text: str):
    pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
    return [s.strip() for s in pattern.split(text) if s.strip()]

def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
    sentences = []
    for para in paragraphs:
        sentences.extend(safe_sentence_split(para))
    if not sentences: return text

    word_freq = Counter()
    for s in sentences:
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
        for w in words:
            if w not in STOPWORDS and len(w) > 2: word_freq[w] += 1
    if not word_freq: return " ".join(sentences[:max_sentences])

    max_freq = max(word_freq.values())
    for w in list(word_freq.keys()): word_freq[w] /= max_freq

    scored = []
    for idx, s in enumerate(sentences):
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
        score = sum(word_freq.get(w, 0.0) for w in words)
        length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
        position_boost = 1.1 if idx < 3 else 1.0
        scored.append((score / length_penalty * position_boost, idx, s))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = sorted(scored[:max_sentences], key=lambda x: x[1])
    if as_bullets: return "\n".join([f"- {s}" for _, _, s in top])
    return " ".join([s for _, _, s in top])

# =============================
# Python code analyzer
# =============================
def analyze_python(code: str):
    report = {"functions": [], "classes": [], "imports": [], "purpose_summary": "", "errors": [], "warnings": [], "fixes": []}
    for line in code.splitlines():
        l = line.strip()
        if l.startswith("def "): report["functions"].append(l.split("(")[0][4:].strip())
        elif l.startswith("class "): report["classes"].append(l.split("(")[0][6:].strip().rstrip(":"))
        elif l.startswith("import ") or l.startswith("from "): report["imports"].append(l)
    report["purpose_summary"] = summarize_text_advanced(code, max_sentences=5)
    try: tree = ast.parse(code)
    except SyntaxError as e:
        report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
        report["fixes"].append("Check indentation, missing colons, parentheses, or quotes.")
        return report
    class Analyzer(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    report["warnings"].append(f"Mutable default argument in function '{node.name}' at line {node.lineno}")
                    report["fixes"].append(f"Use None as default and create new objects inside '{node.name}'.")
            self.generic_visit(node)
        def visit_ExceptHandler(self, node):
            if node.type is None:
                report["warnings"].append(f"Bare except detected at line {node.lineno}")
                report["fixes"].append("Catch specific exceptions instead of bare except.")
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                report["warnings"].append(f"Exception swallowed with pass at line {node.lineno}")
                report["fixes"].append("Handle the exception or log it; avoid silent failures.")
            self.generic_visit(node)
    Analyzer().visit(tree)
    return report

# =============================
# AI vs Human detector
# =============================
def detect_ai_generated_code(code: str) -> dict:
    lines = [ln for ln in code.splitlines()]
    code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    features = {}
    total = max(1, len(lines))
    features["comment_density"] = len(comment_lines) / total
    normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
    counts = Counter(normalized)
    repeated = sum(c for c in counts.values() if c > 1)
    features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    docstring_like = re.findall(r'\"\"\"(.*?)\"\"\"|\'\'\'(.*?)\'\'\'', code, flags=re.S)
    docstrings = [d[0] or d[1] for d in docstring_like]
    templated_docs = sum(1 for d in docstrings if re.match(r"(?i)\s*(this function|returns|parameters)\b", d.strip()))
    features["templated_doc_ratio"] = (templated_docs / max(1, len(docstrings))) if docstrings else 0.0
    generic_names = {"data","result","results","temp","value","values","item","items","input","output","res"}
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
    generic_count = sum(1 for t in tokens if t in generic_names)
    features["generic_name_density"] = generic_count / max(1, len(tokens))
    words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", code)]
    trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]
    trigram_counts = Counter(trigrams)
    repeating_trigram_ratio = sum(1 for c in trigram_counts.values() if c > 1) / max(1, len(trigram_counts))
    features["repeating_trigram_ratio"] = repeating_trigram_ratio
    score = (
        35 * features["repeating_trigram_ratio"] +
        20 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
        20 * features["repeated_line_ratio"] +
        15 * features["templated_doc_ratio"] +
        10 * min(1.0, features["generic_name_density"] * 20)
    )
    score = max(0.0, min(100.0, score))
    if score >= 65: label = "Likely AI-generated"
    elif score >= 45: label = "Unclear / Mixed"
    else: label = "Likely human-written"
    reasons = []
    if features["repeating_trigram_ratio"] > 0.08: reasons.append("High repeated phrasing patterns.")
    if features["repeated_line_ratio"] > 0.06: reasons.append("Notable repetition of similar lines.")
    if features["templated_doc_ratio"] > 0.4: reasons.append("Docstrings appear templated.")
    if features["comment_density"] < 0.03 or features["comment_density"] > 0.4: reasons.append("Atypical comment density.")
    if features["generic_name_density"] > 0.02: reasons.append("Frequent use of generic variable names.")
    return {"score": round(score,1), "label": label, "reasons": reasons, "features": features}

# =============================
# Fetch from URL
# =============================
def fetch_from_url(url: str) -> str:
    try:
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        if "text/html" in resp.headers.get("Content-Type",""):
            soup = BeautifulSoup(resp.text,"html.parser")
            for s in soup(["script","style","noscript"]): s.extract()
            return soup.get_text(separator="\n")
        return resp.text
    except Exception as e: return f"❌ Error fetching URL: {str(e)}"

# =============================
# Copy button
# =============================
def copy_button(label: str, text: str):
    if text is None: text = ""
    b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    html_button = f"""
        <button onclick="navigator.clipboard.writeText(atob('{b64}'))"
                style="background:transparent;border:1px solid rgba(255,255,255,0.06);
                       color: #EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
                       font-weight:700; margin:3px;">{label}</button>
    """
    st.markdown(html_button, unsafe_allow_html=True)

# =============================
# Main App
# =============================
st.set_page_config(page_title="Technova AI Toolkit", layout="wide")
set_canvas_stars()
st.title("🚀 Technova AI Toolkit")
st.write("Advanced AI-powered tools: Document Summarizer, Code Analyzer, AI vs Human Scanner, URL Fetch & Explain")

tabs = st.tabs(["Document Summarizer","Code Analyzer","AI vs Human Scanner","URL Fetch & Explain"])

# Document Summarizer
with tabs[0]:
    st.subheader("Document Summarizer")
    doc_text = st.text_area("Paste text here:", height=200)
    doc_file = st.file_uploader("Or upload a text file (.txt, .md)", type=["txt","md"])
    doc_url = st.text_input("Or enter a URL to fetch content:")
    if st.button("Summarize Document"):
        content = doc_file.read().decode("utf-8", errors="ignore") if doc_file else (fetch_from_url(doc_url.strip()) if doc_url.strip() else doc_text)
        if content:
            summary = summarize_text_advanced(content, max_sentences=6, as_bullets=True)
            with st.expander("📂 Summary (click to expand)"): st.markdown(summary)
            copy_button("Copy Summary", summary)
            st.download_button("Download Summary", summary.encode("utf-8"), "summary.txt")
        else: st.warning("Provide text via paste, upload, or URL.")

# Code Analyzer
with tabs[1]:
    st.subheader("Code Analyzer")
    code_text = st.text_area("Paste Python code here:", height=200)
    code_file = st.file_uploader("Or upload Python file (.py)", type=["py"])
    code_url = st.text_input("Or enter a URL to fetch code:")
    if st.button("Analyze Code"):
        code_str = code_file.read().decode("utf-8", errors="ignore") if code_file else (fetch_from_url(code_url.strip()) if code_url.strip() else code_text)
        if code_str:
            report = analyze_python(code_str)
            with st.expander("📂 Code Summary / Purpose"): st.markdown(report["purpose_summary"]); copy_button("Copy Summary", report["purpose_summary"])
            with st.expander("⚠️ Errors"): [st.markdown(f"- {e}") for e in report["errors"]]
            with st.expander("⚠️ Warnings & Suggestions"): [st.markdown(f"- {w}") for w in report["warnings"]]
            with st.expander("💡 Fixes / Recommendations"): [st.markdown(f"- {f}") for f in report["fixes"]]
            st.download_button("Download Report", str(report).encode("utf-8"), "code_report.txt")
        else: st.warning("Provide code via paste, upload, or URL.")

# AI vs Human Scanner
with tabs[2]:
    st.subheader("AI vs Human Scanner")
    ai_text = st.text_area("Paste text or code here:", height=200)
    ai_file = st.file_uploader("Or upload a file (.txt,.md,.py)", type=["txt","md","py"])
    ai_url = st.text_input("Or enter a URL to fetch content:")
    if st.button("Detect AI / Human Likelihood"):
        content = ai_file.read().decode("utf-8", errors="ignore") if ai_file else (fetch_from_url(ai_url.strip()) if ai_url.strip() else ai_text)
        if content:
            result = detect_ai_generated_code(content)
            with st.expander(f"📊 Likelihood: {result['label']} (Score: {result['score']}%)"):
                st.markdown("**Reasons / Indicators:**"); [st.markdown(f"- {r}") for r in result["reasons"]]
                st.markdown("**Detailed Features:**"); [st.markdown(f"- {k}: {v}") for k,v in result["features"].items()]
            copy_button("Copy Result", str(result))
            st.download_button("Download Result", str(result).encode("utf-8"), "ai_vs_human.txt")
        else: st.warning("Provide text/code via paste, upload, or URL.")

# URL Fetch & Explain
with tabs[3]:
    st.subheader("URL Fetch & Explain")
    url_input = st.text_input("Enter any URL:")
    if st.button("Fetch & Explain"):
        if url_input.strip():
            content = fetch_from_url(url_input.strip())
            summary = summarize_text_advanced(content, max_sentences=6, as_bullets=True)
            with st.expander("📂 Fetched Content (click to expand)"): st.markdown(content)
            with st.expander("📂 Summary (click to expand)"): st.markdown(summary)
            copy_button("Copy Summary", summary)
            st.download_button("Download Summary", summary.encode("utf-8"), "url_summary.txt")
        else: st.warning("Enter a valid URL.")


