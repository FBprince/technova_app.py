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













# CODE 2



(cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF'
diff --git a/technova_app.py b/technova_app.py
--- a/technova_app.py
+++ b/technova_app.py
@@ -0,0 +1,587 @@
+import streamlit as st
+import requests
+from bs4 import BeautifulSoup
+import re
+import base64
+import ast
+from collections import Counter, defaultdict
+import math
+
+
+# =============================
+# 🌌 Canvas Star Background + Neon Text
+# =============================
+def set_canvas_stars():
+    canvas_html = """
+    <canvas id="star-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1000;"></canvas>
+    <script>
+    const canvas = document.getElementById('star-canvas');
+    const ctx = canvas.getContext('2d');
+    function resize() {
+        canvas.width = window.innerWidth;
+        canvas.height = window.innerHeight;
+    }
+    window.addEventListener('resize', resize);
+    resize();
+    const numStars = 80;
+    const stars = [];
+    for(let i=0;i<numStars;i++){
+        stars.push({
+            x: Math.random()*canvas.width,
+            y: Math.random()*canvas.height,
+            r: Math.random()*2+1,
+            dx: (Math.random()-0.5)*0.3,
+            dy: (Math.random()-0.5)*0.3,
+            alpha: Math.random()
+        });
+    }
+    function draw() {
+        ctx.fillStyle = '#0a0b1c';
+        ctx.fillRect(0,0,canvas.width,canvas.height);
+        for(let s of stars){
+            ctx.beginPath();
+            ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
+            ctx.fillStyle = "rgba(0,255,255,"+s.alpha+")";
+            ctx.fill();
+            s.x += s.dx;
+            s.y += s.dy;
+            s.alpha += (Math.random()-0.5)*0.02;
+            if(s.alpha<0)s.alpha=0;
+            if(s.alpha>1)s.alpha=1;
+            if(s.x<0)s.x=canvas.width;
+            if(s.x>canvas.width)s.x=0;
+            if(s.y<0)s.y=canvas.height;
+            if(s.y>canvas.height)s.y=0;
+        }
+        requestAnimationFrame(draw);
+    }
+    draw();
+    </script>
+    <style>
+    body, [data-testid="stAppViewContainer"] {
+        background-color: #0a0b1c;
+        color: #00f9ff;
+        font-family: 'Orbitron', 'Trebuchet MS', monospace;
+        text-shadow: 0 0 6px #00f9ff, 0 0 12px #00cfff;
+        overflow-x:hidden;
+    }
+    h1,h2,h3,h4,h5,h6 { color:#00f9ff !important; text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff,0 0 24px #00aaff; }
+    p,div,span,label { color:#a0f0ff !important; text-shadow:0 0 4px #00f9ff; }
+    .stButton>button, .stDownloadButton>button {
+        background: linear-gradient(90deg, #00f0ff, #0066ff);
+        color:#02121b;
+        border-radius:10px;padding:8px 14px;
+        font-weight:700;font-family:'Orbitron', monospace;
+        box-shadow:0 8px 24px rgba(0,120,255,0.12);
+        transition: transform .15s ease, box-shadow .15s ease;
+    }
+    .stButton>button:hover, .stDownloadButton>button:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(0,120,255,0.2); }
+    [data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(4,6,20,0.95), rgba(8,12,35,0.95)); color:#EAF9FF; }
+    pre, code { background: rgba(0,20,40,0.4); color: #00f9ff; text-shadow:0 0 4px #00f9ff; }
+    </style>
+    """
+    st.markdown(canvas_html, unsafe_allow_html=True)
+
+
+# =============================
+# Utilities: sentence splitting and improved summaries
+# =============================
+STOPWORDS = set(
+    "a an and are as at be but by for if in into is it no not of on or such that the their then there these they this to was will with you your from our we he she his her its were been being than also can could should would may might have has had do does did done just over under more most other some any each many few those them which who whom whose where when why how".split()
+)
+
+
+def safe_sentence_split(text: str):
+    pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
+    return [s.strip() for s in pattern.split(text) if s.strip()]
+
+
+def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
+    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
+    sentences = []
+    for para in paragraphs:
+        sentences.extend(safe_sentence_split(para))
+    if not sentences:
+        return text
+
+    word_freq = Counter()
+    for s in sentences:
+        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
+        for w in words:
+            if w not in STOPWORDS and len(w) > 2:
+                word_freq[w] += 1
+    if not word_freq:
+        return " ".join(sentences[:max_sentences])
+
+    max_freq = max(word_freq.values())
+    for w in list(word_freq.keys()):
+        word_freq[w] /= max_freq
+
+    scored = []
+    for idx, s in enumerate(sentences):
+        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
+        score = sum(word_freq.get(w, 0.0) for w in words)
+        length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
+        position_boost = 1.1 if idx < 3 else 1.0
+        scored.append((score / length_penalty * position_boost, idx, s))
+
+    scored.sort(key=lambda x: (-x[0], x[1]))
+    top = sorted(scored[:max_sentences], key=lambda x: x[1])
+    if as_bullets:
+        return "\n".join([f"- {s}" for _, _, s in top])
+    return " ".join([s for _, _, s in top])
+
+
+def paragraph_summary(text: str, max_sentences: int = 5):
+    return summarize_text_advanced(text, max_sentences=max_sentences, as_bullets=False)
+
+
+# =============================
+# Python code analyzer and summarizer with actionable fixes
+# =============================
+def analyze_python(code: str, summary_length: int = 5):
+    report = {
+        "functions": [],
+        "classes": [],
+        "imports": [],
+        "purpose_summary": "",
+        "errors": [],
+        "warnings": [],
+        "suggestions": [],
+        "fixes": []
+    }
+
+    # Quick structure scrape
+    for line in code.splitlines():
+        l = line.strip()
+        if l.startswith("def "):
+            report["functions"].append(l.split("(")[0][4:].strip())
+        elif l.startswith("class "):
+            report["classes"].append(l.split("(")[0][6:].strip().rstrip(":"))
+        elif l.startswith("import ") or l.startswith("from "):
+            report["imports"].append(l)
+
+    report["purpose_summary"] = summarize_code_purpose(code, max_items=summary_length)
+
+    # Parse AST
+    try:
+        tree = ast.parse(code)
+    except SyntaxError as e:
+        report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
+        report["suggestions"].append("Check indentation, missing colons, parentheses, or quotes.")
+        report["fixes"].append("Fix the syntax at the reported line; ensure matching brackets/quotes and proper indentation.")
+        return report
+
+    # Collect usage info
+    imported_names = set()
+    used_names = set()
+    assigned_names = set()
+    function_defs = []
+    class_defs = []
+
+    class Analyzer(ast.NodeVisitor):
+        def visit_Import(self, node):
+            for alias in node.names:
+                imported_names.add(alias.asname or alias.name.split(".")[0])
+            self.generic_visit(node)
+
+        def visit_ImportFrom(self, node):
+            for alias in node.names:
+                imported_names.add(alias.asname or alias.name)
+            self.generic_visit(node)
+
+        def visit_FunctionDef(self, node):
+            function_defs.append(node)
+            assigned_names.add(node.name)
+            # Mutable defaults
+            for default in node.args.defaults:
+                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
+                    report["warnings"].append(f"Mutable default argument in function '{node.name}' at line {node.lineno}")
+                    report["fixes"].append(f"Use None as default for mutable types in '{node.name}' and create new objects inside the function.")
+            self.generic_visit(node)
+
+        def visit_ClassDef(self, node):
+            class_defs.append(node)
+            assigned_names.add(node.name)
+            self.generic_visit(node)
+
+        def visit_Name(self, node):
+            if isinstance(node.ctx, ast.Load):
+                used_names.add(node.id)
+            if isinstance(node.ctx, ast.Store):
+                assigned_names.add(node.id)
+            self.generic_visit(node)
+
+        def visit_Call(self, node):
+            # Dangerous calls
+            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
+                report["warnings"].append(f"Use of {node.func.id} detected at line {node.lineno}")
+                report["fixes"].append(f"Avoid {node.func.id}; consider safer alternatives or explicit parsing.")
+            self.generic_visit(node)
+
+        def visit_ExceptHandler(self, node):
+            if node.type is None:
+                report["warnings"].append(f"Bare except detected at line {node.lineno}")
+                report["fixes"].append("Catch specific exception classes instead of a bare except.")
+            elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
+                report["warnings"].append(f"Overly broad exception handler '{node.type.id}' at line {node.lineno}")
+                report["fixes"].append("Catch the narrowest relevant exception type.")
+            # 'pass' inside except
+            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
+                report["warnings"].append(f"Exception swallowed with pass at line {node.lineno}")
+                report["fixes"].append("Handle the exception or log it; avoid silent failures.")
+            self.generic_visit(node)
+
+    Analyzer().visit(tree)
+
+    # Unused imports
+    for name in sorted(imported_names):
+        if name not in used_names and name not in {"__future__"}:
+            report["warnings"].append(f"Possibly unused import '{name}'")
+            report["fixes"].append(f"Remove the unused import '{name}'.")
+
+    # Shadowing builtins
+    for name in assigned_names:
+        if name in dir(__builtins__):
+            report["warnings"].append(f"Variable or function '{name}' shadows built-in")
+            report["fixes"].append(f"Rename '{name}' to avoid shadowing built-ins.")
+
+    # Unreachable code (simple): after return/raise in a function
+    for fn in function_defs:
+        seen_terminator = False
+        for node in fn.body:
+            if seen_terminator:
+                report["warnings"].append(f"Unreachable code in function '{fn.name}' after a return/raise at line {getattr(node, 'lineno', '?')}")
+                report["fixes"].append(f"Remove or refactor unreachable code in '{fn.name}'.")
+                break
+            if isinstance(node, (ast.Return, ast.Raise)):
+                seen_terminator = True
+
+    # Missing docstrings
+    if ast.get_docstring(tree) is None:
+        report["warnings"].append("Module is missing a top-level docstring")
+        report["fixes"].append("Add a brief module docstring describing purpose and usage.")
+    for fn in function_defs:
+        if ast.get_docstring(fn) is None:
+            report["warnings"].append(f"Function '{fn.name}' missing a docstring")
+            report["fixes"].append(f"Add a concise docstring for '{fn.name}'.")
+    for cl in class_defs:
+        if ast.get_docstring(cl) is None:
+            report["warnings"].append(f"Class '{cl.name}' missing a docstring")
+            report["fixes"].append(f"Add a concise docstring for class '{cl.name}'.")
+
+    # Call to undefined simple functions
+    defined = {fn.name for fn in function_defs} | {cl.name for cl in class_defs}
+    called = set()
+    class CallVisitor(ast.NodeVisitor):
+        def visit_Call(self, node):
+            if isinstance(node.func, ast.Name):
+                called.add(node.func.id)
+            self.generic_visit(node)
+    CallVisitor().visit(tree)
+    for func in sorted(called):
+        if func not in defined and func not in dir(__builtins__):
+            report["warnings"].append(f"Call to undefined function '{func}' detected")
+            report["fixes"].append(f"Define '{func}' or import it before use.")
+
+    if not report["errors"]:
+        if report["warnings"]:
+            report["suggestions"].append("Review warnings and apply the proposed fixes.")
+        else:
+            report["suggestions"].append("No obvious issues; add tests and run linters for confidence.")
+
+    return report
+
+
+def summarize_code_purpose(code: str, max_items: int = 5) -> str:
+    try:
+        tree = ast.parse(code)
+    except SyntaxError:
+        # fallback to text summary
+        return summarize_text_advanced(code, max_sentences=max_items)
+
+    lines = []
+    mod_doc = ast.get_docstring(tree)
+    if mod_doc:
+        first = mod_doc.strip().splitlines()[0]
+        lines.append(first)
+
+    for node in tree.body:
+        if isinstance(node, ast.ClassDef):
+            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
+            doc = ast.get_docstring(node)
+            if doc:
+                first = doc.strip().splitlines()[0]
+                lines.append(f"Class {node.name}: {first}")
+            else:
+                lines.append(f"Class {node.name} with methods: {', '.join(methods[:6])}")
+        elif isinstance(node, ast.FunctionDef):
+            args = [a.arg for a in node.args.args]
+            doc = ast.get_docstring(node)
+            if doc:
+                first = doc.strip().splitlines()[0]
+                lines.append(f"Function {node.name}({', '.join(args)}): {first}")
+            else:
+                lines.append(f"Function {node.name}({', '.join(args)})")
+
+    if not lines:
+        return summarize_text_advanced(code, max_sentences=max_items)
+    return " \n".join(lines[:max_items])
+
+
+# =============================
+# Heuristic AI-generated code detector
+# =============================
+def detect_ai_generated_code(code: str) -> dict:
+    lines = [ln for ln in code.splitlines()]
+    code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
+    comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
+
+    # Features
+    features = {}
+    total = max(1, len(lines))
+    features["comment_density"] = len(comment_lines) / total
+
+    # Repeated lines ratio
+    normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
+    counts = Counter(normalized)
+    repeated = sum(c for c in counts.values() if c > 1)
+    features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
+
+    # Docstring patterns
+    docstring_like = re.findall(r'\"\"\"(.*?)\"\"\"|\'\'\'(.*?)\'\'\'', code, flags=re.S)
+    docstrings = [d[0] or d[1] for d in docstring_like]
+    templated_docs = sum(1 for d in docstrings if re.match(r"(?i)\s*(this function|returns|parameters)\b", d.strip()))
+    features["templated_doc_ratio"] = (templated_docs / max(1, len(docstrings))) if docstrings else 0.0
+
+    # Generic variable names
+    generic_names = {"data", "result", "results", "temp", "value", "values", "item", "items", "input", "output", "res"}
+    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
+    generic_count = sum(1 for t in tokens if t in generic_names)
+    features["generic_name_density"] = generic_count / max(1, len(tokens))
+
+    # N-gram repetition (rough)
+    words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", code)]
+    trigrams = [tuple(words[i:i+3]) for i in range(len(words)-2)]
+    trigram_counts = Counter(trigrams)
+    repeating_trigram_ratio = sum(1 for c in trigram_counts.values() if c > 1) / max(1, len(trigram_counts))
+    features["repeating_trigram_ratio"] = repeating_trigram_ratio
+
+    # Score (0-100)
+    # Weighted sum; higher implies more AI-like
+    score = (
+        35 * features["repeating_trigram_ratio"] +
+        20 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
+        20 * features["repeated_line_ratio"] +
+        15 * features["templated_doc_ratio"] +
+        10 * min(1.0, features["generic_name_density"] * 20)
+    )
+    score = max(0.0, min(100.0, score))
+
+    # Label and reasons
+    if score >= 65:
+        label = "Likely AI-generated"
+    elif score >= 45:
+        label = "Unclear / Mixed"
+    else:
+        label = "Likely human-written"
+
+    reasons = []
+    if features["repeating_trigram_ratio"] > 0.08:
+        reasons.append("High repeated phrasing patterns across the code body.")
+    if features["repeated_line_ratio"] > 0.06:
+        reasons.append("Notable repetition of similar lines.")
+    if features["templated_doc_ratio"] > 0.4:
+        reasons.append("Docstrings appear templated.")
+    if features["comment_density"] < 0.03 or features["comment_density"] > 0.4:
+        reasons.append("Atypical comment density.")
+    if features["generic_name_density"] > 0.02:
+        reasons.append("Frequent use of generic variable names.")
+
+    return {"score": round(score, 1), "label": label, "reasons": reasons, "features": features}
+
+
+# =============================
+# URL fetching
+# =============================
+def fetch_from_url(url: str) -> str:
+    try:
+        resp = requests.get(url, timeout=12)
+        resp.raise_for_status()
+        ct = resp.headers.get("Content-Type", "")
+        if "text/plain" in ct or url.lower().endswith((".py", ".txt", ".md")):
+            return resp.text
+        if "text/html" in ct:
+            soup = BeautifulSoup(resp.text, "html.parser")
+            for s in soup(["script", "style", "noscript"]):
+                s.extract()
+            return soup.get_text(separator="\n")
+        return resp.text
+    except Exception as e:
+        return f"❌ Error fetching URL: {str(e)}"
+
+
+# =============================
+# Copy button
+# =============================
+def copy_button(label: str, text: str, key: str):
+    if text is None:
+        text = ""
+    b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
+    html_button = f"""
+        <button onclick="navigator.clipboard.writeText(atob('{b64}'))"
+                style="background:transparent;border:1px solid rgba(255,255,255,0.06);
+                       color: #EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
+                       font-weight:700;box-shadow:0 6px 18px rgba(0,120,255,0.06);">
+            📋 {label}
+        </button>
+    """
+    st.markdown(html_button, unsafe_allow_html=True)
+
+
+# =============================
+# Main app
+# =============================
+def main():
+    set_canvas_stars()
+    st.title("🌌 TechNova — Study & Code Assistant")
+    st.caption("Summarize documents, analyze Python code with smart debugging, detect AI-generated code — neon starry UI")
+
+    tab1, tab2, tab3 = st.tabs(["📄 Document Summarizer", "💻 Code Analyzer", "🌐 URL Fetch & Explain"])
+
+    # ----------------------------
+    with tab1:
+        st.subheader("Summarize Documents")
+        text_input = st.text_area("Paste text here:", height=200)
+        uploaded_file = st.file_uploader("Or upload a document (.txt, .md)", type=["txt", "md"])
+        length = st.slider("Summary length (sentences)", 1, 12, 5)
+        as_bullets = st.checkbox("Return bullet outline", value=False)
+
+        if st.button("Summarize Document"):
+            content = ""
+            if uploaded_file:
+                try:
+                    content = uploaded_file.read().decode("utf-8")
+                except Exception:
+                    content = uploaded_file.read().decode("latin-1")
+            elif text_input.strip():
+                content = text_input
+            if not content:
+                st.warning("Paste text or upload a file.")
+            else:
+                summary = summarize_text_advanced(content, max_sentences=length, as_bullets=as_bullets)
+                st.markdown("### 📌 Summary")
+                if as_bullets:
+                    st.markdown(summary)
+                else:
+                    st.write(summary)
+                copy_button("Copy Summary", summary, key="doc_copy")
+                st.download_button("⬇️ Download Summary", summary, "document_summary.txt", mime="text/plain")
+
+    # ----------------------------
+    with tab2:
+        st.subheader("Analyze Python Code with Smart Debugging + AI Detection")
+        code_input = st.text_area("Paste Python code here:", height=220)
+        uploaded_code = st.file_uploader("Or upload a Python file (.py)", type=["py"])
+        length_code = st.slider("Code purpose summary length (items)", 1, 8, 4, key="code_len")
+
+        if st.button("Analyze Code"):
+            code_str = ""
+            if uploaded_code:
+                try:
+                    code_str = uploaded_code.read().decode("utf-8")
+                except Exception:
+                    code_str = uploaded_code.read().decode("latin-1")
+            elif code_input.strip():
+                code_str = code_input
+            if not code_str:
+                st.warning("Paste code or upload a Python file.")
+            else:
+                report = analyze_python(code_str, summary_length=length_code)
+                ai_det = detect_ai_generated_code(code_str)
+
+                st.markdown("### 📊 Code Analysis Report")
+                colA, colB = st.columns(2)
+                with colA:
+                    st.markdown("**Functions:**")
+                    st.write(", ".join(report["functions"]) if report["functions"] else "_none_")
+                    st.markdown("**Classes:**")
+                    st.write(", ".join(report["classes"]) if report["classes"] else "_none_")
+                with colB:
+                    st.markdown("**Imports:**")
+                    if report["imports"]:
+                        for imp in report["imports"]:
+                            st.code(imp)
+                    else:
+                        st.write("_none_")
+
+                st.markdown("**Purpose summary:**")
+                st.write(report["purpose_summary"] or "_No summary available_")
+
+                st.markdown("**Errors Detected:**")
+                if report["errors"]:
+                    for err in report["errors"]:
+                        st.error(err)
+                else:
+                    st.write("_No syntax errors detected_")
+
+                st.markdown("**Warnings / Runtime Issues:**")
+                if report["warnings"]:
+                    for w in report["warnings"]:
+                        st.warning(w)
+                else:
+                    st.write("_No obvious runtime issues detected_")
+
+                st.markdown("**Actionable Fixes:**")
+                if report["fixes"]:
+                    for fix in report["fixes"]:
+                        st.info(fix)
+                else:
+                    st.write("_No fixes suggested_")
+
+                st.markdown("### 🤖 AI-Generated Code Detection")
+                st.metric(label="Likelihood Score (0-100)", value=ai_det["score"])
+                st.write(f"Assessment: **{ai_det['label']}**")
+                if ai_det["reasons"]:
+                    st.markdown("**Reasons:**")
+                    for r in ai_det["reasons"]:
+                        st.write(f"- {r}")
+
+                copy_button("Copy Report", str({"analysis": report, "ai_detection": ai_det}), key="code_copy")
+                st.download_button("⬇️ Download Code Report", str({"analysis": report, "ai_detection": ai_det}), "code_analysis.txt", mime="text/plain")
+
+    # ----------------------------
+    with tab3:
+        st.subheader("Fetch, Summarize & Explain from URL")
+        url_input = st.text_input("Enter a URL:")
+
+        if st.button("Fetch & Analyze URL"):
+            if not url_input.strip():
+                st.warning("Please enter a valid URL.")
+            else:
+                data = fetch_from_url(url_input.strip())
+                if data.startswith("❌ Error"):
+                    st.error(data)
+                else:
+                    st.markdown("### 📄 Content Preview")
+                    st.code(data[:1200] + ("..." if len(data) > 1200 else ""), language="text")
+                    is_code = url_input.strip().lower().endswith(".py") or ("def " in data or "class " in data)
+                    if is_code:
+                        st.markdown("### 💻 Code Analysis with Smart Debugging")
+                        report = analyze_python(data, summary_length=5)
+                        ai_det = detect_ai_generated_code(data)
+                        st.json({"analysis": report, "ai_detection": ai_det})
+                        copy_button("Copy Report", str({"analysis": report, "ai_detection": ai_det}), key="url_code_copy")
+                        st.download_button("⬇️ Download Code Report", str({"analysis": report, "ai_detection": ai_det}), "url_code_analysis.txt")
+                    else:
+                        st.markdown("### 📌 Document Summary")
+                        summary = summarize_text_advanced(data, max_sentences=5, as_bullets=False)
+                        st.write(summary)
+                        copy_button("Copy Summary", summary, key="url_summary_copy")
+                        st.download_button("⬇️ Download Summary", summary, "url_summary.txt")
+
+
+if __name__ == "__main__":
+    main()
+
+
EOF
)