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
import math  # ✅ Added math module

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
    for(let i=0;i<numStars;i++){
        stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*2+1,
                    dx: (Math.random()-0.5)*0.3, dy: (Math.random()-0.5)*0.3, alpha: Math.random()});
    }
    function draw() {
        ctx.fillStyle = '#0a0b1c';
        ctx.fillRect(0,0,canvas.width,canvas.height);
        for(let s of stars){
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
            ctx.fillStyle = "rgba(0,255,255,"+s.alpha+")";
            ctx.fill();
            s.x += s.dx; s.y += s.dy;
            s.alpha += (Math.random()-0.5)*0.02;
            if(s.alpha<0)s.alpha=0;
            if(s.alpha>1)s.alpha=1;
            if(s.x<0)s.x=canvas.width;
            if(s.x>canvas.width)s.x=0;
            if(s.y<0)s.y=canvas.height;
            if(s.y>canvas.height)s.y=0;
        }
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    <style>
    body, [data-testid="stAppViewContainer"] {
        background-color: #0a0b1c;
        color: #00f9ff;
        font-family: 'Orbitron', 'Trebuchet MS', monospace;
        text-shadow: 0 0 6px #00f9ff, 0 0 12px #00cfff;
        overflow-x:hidden;
    }
    h1,h2,h3,h4,h5,h6 { color:#00f9ff !important; text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff,0 0 24px #00aaff; }
    p,div,span,label { color:#a0f0ff !important; text-shadow:0 0 4px #00f9ff; }
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, #00f0ff, #0066ff);
        color:#02121b;
        border-radius:10px;padding:8px 14px;
        font-weight:700;font-family:'Orbitron', monospace;
        box-shadow:0 8px 24px rgba(0,120,255,0.12);
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .stButton>button:hover, .stDownloadButton>button:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(0,120,255,0.2); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(4,6,20,0.95), rgba(8,12,35,0.95)); color:#EAF9FF; }
    pre, code { background: rgba(0,20,40,0.4); color: #00f9ff; text-shadow:0 0 4px #00f9ff; }
    </style>
    """
    st.markdown(canvas_html, unsafe_allow_html=True)

# =============================
# Utilities: sentence splitting and improved summaries
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
    if not sentences:
        return text

    word_freq = Counter()
    for s in sentences:
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
        for w in words:
            if w not in STOPWORDS and len(w) > 2:
                word_freq[w] += 1
    if not word_freq:
        return " ".join(sentences[:max_sentences])

    max_freq = max(word_freq.values())
    for w in list(word_freq.keys()):
        word_freq[w] /= max_freq

    scored = []
    for idx, s in enumerate(sentences):
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
        score = sum(word_freq.get(w, 0.0) for w in words)
        length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
        position_boost = 1.1 if idx < 3 else 1.0
        scored.append((score / length_penalty * position_boost, idx, s))

    scored.sort(key=lambda x: (-x[0], x[1]))
    top = sorted(scored[:max_sentences], key=lambda x: x[1])
    if as_bullets:
        return "\n".join([f"- {s}" for _, _, s in top])
    return " ".join([s for _, _, s in top])

# =============================
# Python code analyzer and summarizer
# =============================
def analyze_python(code: str, summary_length: int = 5):
    report = {
        "functions": [],
        "classes": [],
        "imports": [],
        "purpose_summary": "",
        "errors": [],
        "warnings": [],
        "suggestions": [],
        "fixes": []
    }

    for line in code.splitlines():
        l = line.strip()
        if l.startswith("def "):
            report["functions"].append(l.split("(")[0][4:].strip())
        elif l.startswith("class "):
            report["classes"].append(l.split("(")[0][6:].strip().rstrip(":"))
        elif l.startswith("import ") or l.startswith("from "):
            report["imports"].append(l)

    report["purpose_summary"] = summarize_code_purpose(code, max_items=summary_length)
    return report

def summarize_code_purpose(code: str, max_items: int = 5) -> str:
    return summarize_text_advanced(code, max_sentences=max_items)

# =============================
# Heuristic AI-generated code detector
# =============================
def detect_ai_generated_code(code: str) -> dict:
    features = {}
    lines = code.splitlines()
    code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    comment_lines = [ln for ln in lines if ln.strip().startswith("#")]

    total = max(1, len(lines))
    features["comment_density"] = len(comment_lines) / total

    normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
    counts = Counter(normalized)
    repeated = sum(c for c in counts.values() if c > 1)
    features["repeated_line_ratio"] = repeated / max(1, len(code_lines))

    score = 20 * features["comment_density"] + 50 * features["repeated_line_ratio"]
    score = min(100, score)

    label = "Likely AI-generated" if score > 50 else "Likely human-written"

    return {"score": round(score, 1), "label": label, "features": features}

# =============================
# URL fetching
# =============================
def fetch_from_url(url: str) -> str:
    try:
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        ct = resp.headers.get("Content-Type", "")
        if "text/plain" in ct or url.lower().endswith((".py", ".txt", ".md")):
            return resp.text
        if "text/html" in ct:
            soup = BeautifulSoup(resp.text, "html.parser")
            for s in soup(["script", "style", "noscript"]):
                s.extract()
            return soup.get_text(separator="\n")
        return resp.text
    except Exception as e:
        return f"❌ Error fetching URL: {str(e)}"

# =============================
# Copy button
# =============================
def copy_button(label: str, text: str, key: str):
    if text is None:
        text = ""
    b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    html_button = f"""
        <button onclick="navigator.clipboard.writeText(atob('{b64}'))"
                style="background:transparent;border:1px solid rgba(255,255,255,0.06);
                       color: #EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
                       font-weight:700;box-shadow:0 6px 18px rgba(0,120,255,0.06);">
            📋 {label}
        </button>
    """
    st.markdown(html_button, unsafe_allow_html=True)

# =============================
# Main app
# =============================
def main():
    set_canvas_stars()
    st.title("🌌 TechNova — Study & Code Assistant")
    st.caption("Summarize documents, analyze Python code, detect AI-generated code — neon starry UI")

    tab1, tab2, tab3 = st.tabs(["📄 Document Summarizer", "💻 Code Analyzer", "🌐 URL Fetch & Explain"])

    with tab1:
        st.subheader("Summarize Documents")
        text_input = st.text_area("Paste text here:", height=200)
        uploaded_file = st.file_uploader("Or upload a document (.txt, .md)", type=["txt", "md"])
        length = st.slider("Summary length (sentences)", 1, 12, 5)
        as_bullets = st.checkbox("Return bullet outline", value=False)

        if st.button("Summarize Document"):
            content = ""
            if uploaded_file:
                try:
                    content = uploaded_file.read().decode("utf-8")
                except Exception:
                    content = uploaded_file.read().decode("latin-1")
            elif text_input.strip():
                content = text_input
            if content:
                summary = summarize_text_advanced(content, max_sentences=length, as_bullets=as_bullets)
                with st.expander("📌 Summary", expanded=True):
                    st.write(summary)
                    copy_button("Copy Summary", summary, key="doc_copy")
                    st.download_button("⬇️ Download Summary", summary, "document_summary.txt", mime="text/plain")

    with tab2:
        st.subheader("Analyze Python Code")
        code_input = st.text_area("Paste Python code here:", height=220)
        uploaded_code = st.file_uploader("Or upload a Python file (.py)", type=["py"])
        length_code = st.slider("Code purpose summary length (items)", 1, 8, 4, key="code_len")

        if st.button("Analyze Code"):
            code_str = ""
            if uploaded_code:
                try:
                    code_str = uploaded_code.read().decode("utf-8")
                except Exception:
                    code_str = uploaded_code.read().decode("latin-1")
            elif code_input.strip():
                code_str = code_input
            if code_str:
                report = analyze_python(code_str, summary_length=length_code)
                ai_det = detect_ai_generated_code(code_str)

                with st.expander("📊 Code Analysis Report", expanded=True):
                    st.write(report)
                    st.write("🤖 AI Detection:", ai_det)
                    copy_button("Copy Report", str({"analysis": report, "ai_detection": ai_det}), key="code_copy")
                    st.download_button("⬇️ Download Code Report", str({"analysis": report, "ai_detection": ai_det}), "code_analysis.txt", mime="text/plain")

    with tab3:
        st.subheader("Fetch, Summarize & Explain from URL")
        url_input = st.text_input("Enter a URL:")

        if st.button("Fetch & Analyze URL"):
            if url_input.strip():
                data = fetch_from_url(url_input.strip())
                if data.startswith("❌ Error"):
                    st.error(data)
                else:
                    is_code = url_input.strip().lower().endswith(".py") or ("def " in data or "class " in data)
                    if is_code:
                        report = analyze_python(data, summary_length=5)
                        ai_det = detect_ai_generated_code(data)
                        with st.expander("💻 URL Code Analysis", expanded=True):
                            st.write({"analysis": report, "ai_detection": ai_det})
                            copy_button("Copy Report", str({"analysis": report, "ai_detection": ai_det}), key="url_code_copy")
                            st.download_button("⬇️ Download Code Report", str({"analysis": report, "ai_detection": ai_det}), "url_code_analysis.txt")
                    else:
                        summary = summarize_text_advanced(data, max_sentences=5, as_bullets=False)
                        with st.expander("📌 URL Document Summary", expanded=True):
                            st.write(summary)
                            copy_button("Copy Summary", summary, key="url_summary_copy")
                            st.download_button("⬇️ Download Summary", summary, "url_summary.txt")

if __name__ == "__main__":
    main()
