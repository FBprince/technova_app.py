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















































# # technova_app.py
# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter
# import io

# # PDF extraction (PyPDF2)
# try:
#     import PyPDF2
# except Exception:
#     PyPDF2 = None

# # Page config
# st.set_page_config(page_title="Technova AI Toolkit", layout="wide")

# # ----------------------------
# # Utility: Copy button (real clipboard via JS)
# # ----------------------------
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """
#     Renders a button that copies `text` to the user's clipboard using JS.
#     key - unique identifier for the button element.
#     """
#     if text is None:
#         text = ""
#     safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text))}"
#     html = f"""
#     <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
#         style="background:transparent;border:1px solid rgba(255,255,255,0.06);
#                color:#EAF9FF;padding:8px 12px;border-radius:8px;cursor:pointer;
#                font-weight:700;margin-right:8px;">
#       📋 {label}
#     </button>
#     <script>
#     const btn_{el_id} = document.getElementById('{el_id}');
#     btn_{el_id}.addEventListener('click', () => {{
#       const old = btn_{el_id}.innerText;
#       btn_{el_id}.innerText = '✅ Copied';
#       setTimeout(()=>{{ btn_{el_id}.innerText = old; }}, 1400);
#     }});
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)

# # ----------------------------
# # Neon star background & basic styles
# # ----------------------------
# def set_canvas_stars():
#     canvas_html = """
#     <canvas id="star-canvas" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1000;"></canvas>
#     <script>
#     const canvas = document.getElementById('star-canvas');
#     const ctx = canvas.getContext('2d');
#     function resize(){ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
#     window.addEventListener('resize', resize);
#     resize();
#     const numStars = 80;
#     const stars = [];
#     for(let i=0;i<numStars;i++){
#       stars.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*2+1,dx:(Math.random()-0.5)*0.3,dy:(Math.random()-0.5)*0.3,alpha:Math.random()});
#     }
#     function draw(){
#       ctx.fillStyle='#0a0b1c'; ctx.fillRect(0,0,canvas.width,canvas.height);
#       for(let s of stars){
#         ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
#         ctx.fillStyle='rgba(0,255,255,'+s.alpha+')'; ctx.fill();
#         s.x+=s.dx; s.y+=s.dy; s.alpha+=(Math.random()-0.5)*0.02;
#         if(s.alpha<0)s.alpha=0; if(s.alpha>1)s.alpha=1;
#         if(s.x<0)s.x=canvas.width; if(s.x>canvas.width)s.x=0;
#         if(s.y<0)s.y=canvas.height; if(s.y>canvas.height)s.y=0;
#       }
#       requestAnimationFrame(draw);
#     }
#     draw();
#     </script>
#     <style>
#     body, [data-testid="stAppViewContainer"] {
#       background-color:#0a0b1c; color:#00f9ff;
#       font-family: 'Orbitron', 'Trebuchet MS', monospace;
#       text-shadow:0 0 6px #00f9ff,0 0 12px #00cfff; overflow-x:hidden;
#     }
#     .stButton>button, .stDownloadButton>button { background: linear-gradient(90deg,#00f0ff,#0066ff); color:#02121b; border-radius:10px; padding:8px 14px; font-weight:700; }
#     </style>
#     """
#     st.markdown(canvas_html, unsafe_allow_html=True)

# set_canvas_stars()
# st.title("🌌 Technova AI Toolkit")
# st.caption("Document summarizer • Code analyzer • AI vs Human scanner • URL fetcher — neon UI")

# # ----------------------------
# # Summarization helpers
# # ----------------------------
# STOPWORDS = set(
#     "a an and are as at be but by for if in into is it no not of on or such that the their then there these they this to was will with you your from our we he she his her its were been being than also can could should would may might have has had do does did done just over under more most other some any each many few those them which who whom whose where when why how".split()
# )

# def safe_sentence_split(text: str):
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
#     if not sentences:
#         return text

#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
#     if as_bullets:
#         return "\n".join([f"- {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# # ----------------------------
# # Code analyzer (AST) with fixes
# # ----------------------------
# def analyze_python(code: str):
#     report = {"functions": [], "classes": [], "imports": [], "purpose_summary": "", "errors": [], "warnings": [], "fixes": []}

#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             report["functions"].append(l.split("(")[0][4:].strip())
#         elif l.startswith("class "):
#             report["classes"].append(l.split("(")[0][6:].strip().rstrip(":"))
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=5)

#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check indentation, missing colons, parentheses, or quotes.")
#         return report

#     imported_names = set()
#     used_names = set()
#     assigned_names = set()
#     function_defs = []
#     class_defs = []

#     class Analyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             function_defs.append(node)
#             assigned_names.add(node.name)
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in function '{node.name}' at line {node.lineno}")
#                     report["fixes"].append(f"Use None as default for mutable types in '{node.name}' and create new objects inside the function.")
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             class_defs.append(node)
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#             if isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
#                 report["warnings"].append(f"Use of {node.func.id} detected at line {node.lineno}")
#                 report["fixes"].append(f"Avoid {node.func.id}; consider safer alternatives or explicit parsing.")
#             self.generic_visit(node)

#         def visit_ExceptHandler(self, node):
#             if node.type is None:
#                 report["warnings"].append(f"Bare except detected at line {node.lineno}")
#                 report["fixes"].append("Catch specific exception classes instead of a bare except.")
#             elif isinstance(node.type, ast.Name) and node.type.id in {"Exception", "BaseException"}:
#                 report["warnings"].append(f"Overly broad exception handler '{node.type.id}' at line {node.lineno}")
#                 report["fixes"].append("Catch the narrowest relevant exception type.")
#             if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
#                 report["warnings"].append(f"Exception swallowed with pass at line {node.lineno}")
#                 report["fixes"].append("Handle the exception or log it; avoid silent failures.")
#             self.generic_visit(node)

#     Analyzer().visit(tree)

#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             report["warnings"].append(f"Possibly unused import '{name}'")
#             report["fixes"].append(f"Remove the unused import '{name}'.")

#     for name in assigned_names:
#         if name in dir(__builtins__):
#             report["warnings"].append(f"Variable or function '{name}' shadows built-in")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing built-ins.")

#     # Simple unreachable code detection
#     for fn in function_defs:
#         seen_terminator = False
#         for node in fn.body:
#             if seen_terminator:
#                 report["warnings"].append(f"Unreachable code in function '{fn.name}' after a return/raise at line {getattr(node, 'lineno', '?')}")
#                 report["fixes"].append(f"Remove or refactor unreachable code in '{fn.name}'.")
#                 break
#             if isinstance(node, (ast.Return, ast.Raise)):
#                 seen_terminator = True

#     # Docstrings
#     if ast.get_docstring(tree) is None:
#         report["warnings"].append("Module is missing a top-level docstring")
#         report["fixes"].append("Add a brief module docstring describing purpose and usage.")
#     for fn in function_defs:
#         if ast.get_docstring(fn) is None:
#             report["warnings"].append(f"Function '{fn.name}' missing a docstring")
#             report["fixes"].append(f"Add a concise docstring for '{fn.name}'.")
#     for cl in class_defs:
#         if ast.get_docstring(cl) is None:
#             report["warnings"].append(f"Class '{cl.name}' missing a docstring")
#             report["fixes"].append(f"Add a concise docstring for class '{cl.name}'.")

#     # Undefined function calls (simple)
#     defined = {fn.name for fn in function_defs} | {cl.name for cl in class_defs}
#     called = set()
#     class CallVisitor(ast.NodeVisitor):
#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 called.add(node.func.id)
#             self.generic_visit(node)
#     CallVisitor().visit(tree)
#     for func in sorted(called):
#         if func not in defined and func not in dir(__builtins__):
#             report["warnings"].append(f"Call to undefined function '{func}' detected")
#             report["fixes"].append(f"Define '{func}' or import it before use.")

#     if not report["errors"]:
#         if report["warnings"]:
#             report["fixes"].append("Review warnings and apply the proposed fixes.")
#         else:
#             report["fixes"].append("No obvious issues; add tests and run linters for confidence.")

#     return report

# # ----------------------------
# # Heuristic AI detector (works for text/code)
# # ----------------------------
# def detect_ai_generated_code(code: str) -> dict:
#     lines = [ln for ln in code.splitlines()]
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
#     features = {}
#     total = max(1, len(lines))
#     features["comment_density"] = len(comment_lines) / total
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
#     docstring_like = re.findall(r'\"\"\"(.*?)\"\"\"|\'\'\'(.*?)\'\'\'', code, flags=re.S)
#     docstrings = [d[0] or d[1] for d in docstring_like]
#     templated_docs = sum(1 for d in docstrings if re.match(r"(?i)\s*(this function|returns|parameters)\b", d.strip()))
#     features["templated_doc_ratio"] = (templated_docs / max(1, len(docstrings))) if docstrings else 0.0
#     generic_names = {"data", "result", "results", "temp", "value", "values", "item", "items", "input", "output", "res"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens)) if tokens else 0.0
#     words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", code)]
#     trigrams = [tuple(words[i:i+3]) for i in range(len(words) - 2)]
#     trigram_counts = Counter(trigrams)
#     repeating_trigram_ratio = sum(1 for c in trigram_counts.values() if c > 1) / max(1, len(trigram_counts)) if trigram_counts else 0.0
#     features["repeating_trigram_ratio"] = repeating_trigram_ratio
#     score = (
#         35 * features["repeating_trigram_ratio"]
#         + 20 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15)
#         + 20 * features["repeated_line_ratio"]
#         + 15 * features["templated_doc_ratio"]
#         + 10 * min(1.0, features["generic_name_density"] * 20)
#     )
#     score = max(0.0, min(100.0, score))
#     if score >= 65:
#         label = "Likely AI-generated"
#     elif score >= 45:
#         label = "Unclear / Mixed"
#     else:
#         label = "Likely human-written"
#     reasons = []
#     if features["repeating_trigram_ratio"] > 0.08:
#         reasons.append("High repeated phrasing patterns.")
#     if features["repeated_line_ratio"] > 0.06:
#         reasons.append("Notable repetition of similar lines.")
#     if features["templated_doc_ratio"] > 0.4:
#         reasons.append("Docstrings appear templated.")
#     if features["comment_density"] < 0.03 or features["comment_density"] > 0.4:
#         reasons.append("Atypical comment density.")
#     if features["generic_name_density"] > 0.02:
#         reasons.append("Frequent use of generic variable names.")
#     return {"score": round(score, 1), "label": label, "reasons": reasons, "features": features}

# # ----------------------------
# # Fetch from URL
# # ----------------------------
# def fetch_from_url(url: str) -> str:
#     try:
#         resp = requests.get(url, timeout=12)
#         resp.raise_for_status()
#         ct = resp.headers.get("Content-Type", "")
#         if "text/html" in ct:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             for s in soup(["script", "style", "noscript"]):
#                 s.extract()
#             return soup.get_text(separator="\n")
#         return resp.text
#     except Exception as e:
#         return f"❌ Error fetching URL: {str(e)}"

# # ----------------------------
# # Tabs (unique keys for all widgets)
# # ----------------------------
# tabs = st.tabs(["Document Summarizer", "Code Analyzer", "AI vs Human Scanner", "URL Fetch & Explain"])

# # Document Summarizer tab
# with tabs[0]:
#     st.header("📄 Document Summarizer")
#     doc_text = st.text_area("Paste text", key="doc_text_input")
#     doc_file = st.file_uploader("Upload a file (.txt, .md, .pdf)", type=["txt", "md", "pdf"], key="doc_file_upload")
#     doc_url = st.text_input("Or enter URL to fetch content", key="doc_url_input")
#     doc_len = st.slider("Summary length (sentences)", 1, 12, 5, key="doc_summary_len")
#     doc_bullets = st.checkbox("Return bullets", value=False, key="doc_as_bullets")

#     if st.button("Summarize Document", key="doc_summarize_btn"):
#         content = ""
#         if doc_file:
#             fn = getattr(doc_file, "name", "")
#             if fn.lower().endswith(".pdf"):
#                 if PyPDF2 is None:
#                     st.error("PDF support requires PyPDF2. Install it with 'pip install PyPDF2'.")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for p in reader.pages:
#                             pages_text.append(p.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"Failed to extract PDF text: {e}")
#                         content = ""
#             else:
#                 try:
#                     content = doc_file.read().decode("utf-8", errors="ignore")
#                 except Exception:
#                     content = doc_file.read().decode("latin-1", errors="ignore")
#         elif doc_url.strip():
#             content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please paste text, upload a file, or enter a URL.")
#         else:
#             summary = summarize_text_advanced(content, max_sentences=doc_len, as_bullets=doc_bullets)
#             with st.expander("📂 Summary (click to expand)", expanded=True):
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
#                 # copy + download
#                 copy_button(summary, label="Copy Summary", key="doc_summary_copy")
#                 st.download_button("⬇ Download Summary", summary.encode("utf-8"), "document_summary.txt", key="doc_summary_download")

# # Code Analyzer tab
# with tabs[1]:
#     st.header("💻 Code Analyzer")
#     code_text = st.text_area("Paste Python code", key="code_text_input")
#     code_file = st.file_uploader("Upload Python file (.py)", type=["py"], key="code_file_upload")
#     code_url = st.text_input("Or enter URL to fetch code", key="code_url_input")
#     code_len = st.slider("Purpose summary length (items)", 1, 8, 4, key="code_summary_len")

#     if st.button("Analyze Code", key="code_analyze_btn"):
#         code_str = ""
#         if code_file:
#             try:
#                 code_str = code_file.read().decode("utf-8", errors="ignore")
#             except Exception:
#                 code_str = code_file.read().decode("latin-1", errors="ignore")
#         elif code_url.strip():
#             code_str = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_str = code_text

#         if not code_str:
#             st.warning("Please paste code, upload a file, or enter a URL.")
#         else:
#             # show syntax highlighted preview
#             with st.expander("💻 Code Preview (syntax-highlighted)", expanded=False):
#                 st.code(code_str, language="python")

#             report = analyze_python(code_str)

#             with st.expander("📂 Code Purpose Summary", expanded=True):
#                 st.write(report["purpose_summary"])
#                 copy_button(report["purpose_summary"], label="Copy Summary", key="code_purpose_copy")
#                 st.download_button("⬇ Download Purpose Summary", report["purpose_summary"].encode("utf-8"), "code_purpose.txt", key="code_purpose_download")

#             with st.expander("❌ Errors"):
#                 if report["errors"]:
#                     for e in report["errors"]:
#                         st.error(e)
#                 else:
#                     st.write("_No syntax errors detected_")

#             with st.expander("⚠️ Warnings"):
#                 if report["warnings"]:
#                     for w in report["warnings"]:
#                         st.warning(w)
#                 else:
#                     st.write("_No warnings detected_")

#             with st.expander("💡 Fixes & Recommendations"):
#                 if report["fixes"]:
#                     for f in report["fixes"]:
#                         st.info(f)
#                 else:
#                     st.write("_No fixes suggested_")

#             copy_button(str(report), label="Copy Full Report", key="code_full_report_copy")
#             st.download_button("⬇ Download Full Report", str(report).encode("utf-8"), "code_analysis_report.txt", key="code_full_report_download")

# # AI vs Human Scanner tab
# with tabs[2]:
#     st.header("🤖 AI vs Human Scanner")
#     ai_text = st.text_area("Paste text or code", key="ai_text_input")
#     ai_file = st.file_uploader("Upload file (.txt, .md, .py, .pdf)", type=["txt", "md", "py", "pdf"], key="ai_file_upload")
#     ai_url = st.text_input("Or enter URL to fetch content", key="ai_url_input")
#     ai_mode = st.radio("Content type", ["Auto-detect", "Treat as Text", "Treat as Code"], index=0, key="ai_mode_radio")

#     if st.button("Detect AI / Human Likelihood", key="ai_detect_btn"):
#         content = ""
#         if ai_file:
#             fn = getattr(ai_file, "name", "")
#             if fn.lower().endswith(".pdf"):
#                 if PyPDF2 is None:
#                     st.error("PDF support requires PyPDF2. Install it with 'pip install PyPDF2'.")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(ai_file.read()))
#                         pages_text = []
#                         for p in reader.pages:
#                             pages_text.append(p.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"Failed to extract PDF text: {e}")
#                         content = ""
#             else:
#                 try:
#                     content = ai_file.read().decode("utf-8", errors="ignore")
#                 except Exception:
#                     content = ai_file.read().decode("latin-1", errors="ignore")
#         elif ai_url.strip():
#             content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please paste content, upload a file, or enter a URL.")
#         else:
#             result = detect_ai_generated_code(content)
#             header = f"📊 Likelihood: {result['label']} (Score: {result['score']}%)"
#             with st.expander(header, expanded=True):
#                 st.markdown("**Reasons / Indicators:**")
#                 if result["reasons"]:
#                     for r in result["reasons"]:
#                         st.markdown(f"- {r}")
#                 else:
#                     st.markdown("- _No strong heuristics triggered_")
#                 st.markdown("**Detailed Features:**")
#                 for k, v in result["features"].items():
#                     st.markdown(f"- {k}: {v}")

#                 copy_button(str(result), label="Copy AI Result", key="ai_result_copy")
#                 st.download_button("⬇ Download AI Result", str(result).encode("utf-8"), "ai_result.txt", key="ai_result_download")

# # URL Fetch & Explain tab
# with tabs[3]:
#     st.header("🌐 URL Fetch & Explain")
#     url_input = st.text_input("Enter any URL to fetch content", key="url_fetch_input")
#     url_len = st.slider("Summary length (sentences)", 1, 12, 6, key="url_summary_len")
#     url_bullets = st.checkbox("Return bullets", value=True, key="url_as_bullets")

#     if st.button("Fetch & Explain", key="url_fetch_btn"):
#         if not url_input.strip():
#             st.warning("Enter a valid URL.")
#         else:
#             content = fetch_from_url(url_input.strip())
#             if content.startswith("❌ Error"):
#                 st.error(content)
#             else:
#                 with st.expander("📄 Content Preview", expanded=False):
#                     st.code(content[:4000] + ("..." if len(content) > 4000 else ""), language="text")
#                 summary = summarize_text_advanced(content, max_sentences=url_len, as_bullets=url_bullets)
#                 with st.expander("📂 Summary", expanded=True):
#                     if url_bullets:
#                         st.markdown(summary)
#                     else:
#                         st.write(summary)
#                     copy_button(summary, label="Copy Summary", key="url_summary_copy")
#                     st.download_button("⬇ Download Summary", summary.encode("utf-8"), "url_summary.txt", key="url_summary_download")




































# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Enhanced copy button
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Enhanced copy button with styling"""
#     if text is None:
#         text = ""
#     safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text))}"
    
#     html = f"""
#     <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
#         style="
#             background: linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2));
#             border: 1px solid rgba(0, 249, 255, 0.4);
#             color: #00f9ff;
#             padding: 8px 16px;
#             border-radius: 8px;
#             font-family: monospace;
#             font-weight: bold;
#             cursor: pointer;
#             margin: 5px;
#             transition: all 0.3s ease;
#         "
#         onmouseover="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3))'"
#         onmouseout="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))'">
#         ⚡ {label}
#     </button>
#     <script>
#     document.getElementById('{el_id}').addEventListener('click', function() {{
#         const btn = this;
#         const oldText = btn.innerHTML;
#         btn.innerHTML = '✅ Copied!';
#         btn.style.background = 'linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.3))';
#         setTimeout(() => {{
#             btn.innerHTML = oldText;
#             btn.style.background = 'linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))';
#         }}, 1500);
#     }});
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python(code: str):
#     """Comprehensive Python code analysis"""
#     report = {
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": []
#     }

#     # Basic parsing
#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             func_name = l.split("(")[0][4:].strip()
#             report["functions"].append(func_name)
#         elif l.startswith("class "):
#             class_name = l.split("(")[0][6:].strip().rstrip(":")
#             report["classes"].append(class_name)
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Analyze AST
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()

#     class CodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
#                 report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                 report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#             self.generic_visit(node)

#     CodeAnalyzer().visit(tree)

#     # Check for unused imports
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}'")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     for name in assigned_names:
#         if name in builtins_list:
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("Code looks good! Consider adding tests and documentation.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes.")

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * (1.0 if len(code_lines) > 50 and features["comment_density"] < 0.05 else 0.0)
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             with st.expander("📊 Results", expanded=True):
#                 st.subheader("Summary")
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     copy_button(summary, "Copy Summary", key="doc_copy_btn")
#                 with col2:
#                     st.download_button(
#                         "💾 Download", 
#                         summary, 
#                         "summary.txt",
#                         mime="text/plain",
#                         key="doc_download_btn"
#                     )

# # Tab 2: Code Analyzer
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing..."):
#                 report = analyze_python(code_content)

#             st.success("Analysis Complete!")

#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("📋 Summary")
#                 st.write(report["purpose_summary"])
                
#                 st.subheader("❌ Errors")
#                 if report["errors"]:
#                     for error in report["errors"]:
#                         st.error(error)
#                 else:
#                     st.success("No syntax errors found!")
            
#             with col2:
#                 st.subheader("⚠️ Warnings")
#                 if report["warnings"]:
#                     for warning in report["warnings"]:
#                         st.warning(warning)
#                 else:
#                     st.success("No warnings!")
                
#                 st.subheader("💡 Recommendations")
#                 for fix in report["fixes"]:
#                     st.info(fix)
            
#             # Copy and download options
#             col3, col4 = st.columns(2)
#             with col3:
#                 copy_button(str(report), "Copy Report", key="code_copy_btn")
#             with col4:
#                 st.download_button(
#                     "💾 Download Report", 
#                     str(report), 
#                     "code_analysis.txt",
#                     mime="text/plain",
#                     key="code_download_btn"
#                 )

# # Tab 3: AI Detection
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("Analysis Complete!")
            
#             # Display results
#             score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
#             with st.expander(f"{score_color} Detection Results", expanded=True):
#                 col1, col2, col3 = st.columns(3)
                
#                 with col2:
#                     st.metric(
#                         "AI Likelihood Score", 
#                         f"{result['score']}%",
#                         delta=f"{result['score'] - 50}% vs baseline"
#                     )
                
#                 st.markdown(f"**Assessment:** {result['label']}")
                
#                 if result["reasons"]:
#                     st.subheader("🔍 Key Indicators")
#                     for reason in result["reasons"]:
#                         st.write(f"• {reason}")
#                 else:
#                     st.success("No significant AI patterns detected")
                
#                 st.subheader("📊 Feature Analysis")
#                 for feature, value in result["features"].items():
#                     feature_name = feature.replace("_", " ").title()
#                     st.write(f"• {feature_name}: `{value:.3f}`")
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(str(result), "Copy Results", key="ai_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Analysis", 
#                         str(result), 
#                         "ai_detection.txt",
#                         mime="text/plain",
#                         key="ai_download_btn"
#                     )

# # Tab 4: URL Extractor
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "Target URL", 
#             placeholder="Enter any URL for content extraction...",
#             key="url_input_field"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 10, 5, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullets", value=True, key="url_use_bullets")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("Please enter a valid URL.")
#         else:
#             with st.spinner("Extracting content..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("Content extracted successfully!")
                
#                 # Show metrics
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.metric("Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("Words", f"{len(content.split()):,}")
#                 with col3:
#                     st.metric("Lines", f"{len(content.splitlines()):,}")
                
#                 # Show preview
#                 with st.expander("📄 Content Preview", expanded=False):
#                     preview = content[:2000] + "..." if len(content) > 2000 else content
#                     st.text(preview)
                
#                 # Generate summary
#                 with st.spinner("Generating summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 st.subheader("📊 Content Summary")
#                 if url_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(summary, "Copy Summary", key="url_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Summary", 
#                         summary.encode("utf-8"), 
#                         "url_summary.txt",
#                         key="url_download_btn"
#                     )

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 20px; color: rgba(0, 249, 255, 0.6); font-family: monospace;">
#     🌌 TECHNOVA AI NEXUS v2.0 • Advanced Neural Processing Suite
# </div>
# """, unsafe_allow_html=True)























# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Enhanced copy button
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Enhanced copy button with styling"""
#     if text is None:
#         text = ""
#     safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
#     el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text[:100]))}"
    
#     html = f"""
#     <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
#         style="
#             background: linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2));
#             border: 1px solid rgba(0, 249, 255, 0.4);
#             color: #00f9ff;
#             padding: 8px 16px;
#             border-radius: 8px;
#             font-family: monospace;
#             font-weight: bold;
#             cursor: pointer;
#             margin: 5px;
#             transition: all 0.3s ease;
#         "
#         onmouseover="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3))'"
#         onmouseout="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))'">
#         ⚡ {label}
#     </button>
#     <script>
#     document.getElementById('{el_id}').addEventListener('click', function() {{
#         const btn = this;
#         const oldText = btn.innerHTML;
#         btn.innerHTML = '✅ Copied!';
#         btn.style.background = 'linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.3))';
#         setTimeout(() => {{
#             btn.innerHTML = oldText;
#             btn.style.background = 'linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))';
#         }}, 1500);
#     }});
#     </script>
#     """
#     st.markdown(html, unsafe_allow_html=True)

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python(code: str):
#     """Comprehensive Python code analysis"""
#     report = {
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": []
#     }

#     # Basic parsing
#     for line in code.splitlines():
#         l = line.strip()
#         if l.startswith("def "):
#             func_name = l.split("(")[0][4:].strip()
#             report["functions"].append(func_name)
#         elif l.startswith("class "):
#             class_name = l.split("(")[0][6:].strip().rstrip(":")
#             report["classes"].append(class_name)
#         elif l.startswith("import ") or l.startswith("from "):
#             report["imports"].append(l)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Analyze AST
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()

#     class CodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
#                 report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                 report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#             self.generic_visit(node)

#     CodeAnalyzer().visit(tree)

#     # Check for unused imports
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}'")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     for name in assigned_names:
#         if name in builtins_list:
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("Code looks good! Consider adding tests and documentation.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes.")

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * (1.0 if len(code_lines) > 50 and features["comment_density"] < 0.05 else 0.0)
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             with st.expander("📊 Results", expanded=True):
#                 st.subheader("Summary")
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     copy_button(summary, "Copy Summary", key="doc_copy_btn")
#                 with col2:
#                     st.download_button(
#                         "💾 Download", 
#                         summary, 
#                         "summary.txt",
#                         mime="text/plain",
#                         key="doc_download_btn"
#                     )

# # Tab 2: Code Analyzer
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing..."):
#                 report = analyze_python(code_content)

#             st.success("Analysis Complete!")

#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("📋 Summary")
#                 st.write(report["purpose_summary"])
                
#                 st.subheader("❌ Errors")
#                 if report["errors"]:
#                     for error in report["errors"]:
#                         st.error(error)
#                 else:
#                     st.success("No syntax errors found!")
            
#             with col2:
#                 st.subheader("⚠️ Warnings")
#                 if report["warnings"]:
#                     for warning in report["warnings"]:
#                         st.warning(warning)
#                 else:
#                     st.success("No warnings!")
                
#                 st.subheader("💡 Recommendations")
#                 for fix in report["fixes"]:
#                     st.info(fix)
            
#             # Copy and download options
#             col3, col4 = st.columns(2)
#             with col3:
#                 copy_button(str(report), "Copy Report", key="code_copy_btn")
#             with col4:
#                 st.download_button(
#                     "💾 Download Report", 
#                     str(report), 
#                     "code_analysis.txt",
#                     mime="text/plain",
#                     key="code_download_btn"
#                 )

# # Tab 3: AI Detection
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("Analysis Complete!")
            
#             # Display results
#             score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
#             with st.expander(f"{score_color} Detection Results", expanded=True):
#                 col1, col2, col3 = st.columns(3)
                
#                 with col2:
#                     st.metric(
#                         "AI Likelihood Score", 
#                         f"{result['score']}%",
#                         delta=f"{result['score'] - 50}% vs baseline"
#                     )
                
#                 st.markdown(f"**Assessment:** {result['label']}")
                
#                 if result["reasons"]:
#                     st.subheader("🔍 Key Indicators")
#                     for reason in result["reasons"]:
#                         st.write(f"• {reason}")
#                 else:
#                     st.success("No significant AI patterns detected")
                
#                 st.subheader("📊 Feature Analysis")
#                 for feature, value in result["features"].items():
#                     feature_name = feature.replace("_", " ").title()
#                     st.write(f"• {feature_name}: `{value:.3f}`")
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(str(result), "Copy Results", key="ai_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Analysis", 
#                         str(result), 
#                         "ai_detection.txt",
#                         mime="text/plain",
#                         key="ai_download_btn"
#                     )

# # Tab 4: URL Extractor
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "Target URL", 
#             placeholder="Enter any URL for content extraction...",
#             key="url_input_field"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 10, 5, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullets", value=True, key="url_use_bullets")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("Please enter a valid URL.")
#         else:
#             with st.spinner("Extracting content..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("Content extracted successfully!")
                
#                 # Show metrics
#                 col1, col2, col3 = st.columns(3)
#                 with col1:
#                     st.metric("Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("Words", f"{len(content.split()):,}")
#                 with col3:
#                     st.metric("Lines", f"{len(content.splitlines()):,}")
                
#                 # Show preview
#                 with st.expander("📄 Content Preview", expanded=False):
#                     preview = content[:2000] + "..." if len(content) > 2000 else content
#                     st.text(preview)
                
#                 # Generate summary
#                 with st.spinner("Generating summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 st.subheader("📊 Content Summary")
#                 if url_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     copy_button(summary, "Copy Summary", key="url_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Summary", 
#                         summary, 
#                         "url_summary.txt",
#                         mime="text/plain",
#                         key="url_download_btn"
#                     )

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 20px; color: rgba(0, 249, 255, 0.6); font-family: monospace;">
#     🌌 TECHNOVA AI NEXUS v2.0 • Advanced Neural Processing Suite
# </div>
# """, unsafe_allow_html=True)






















# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter, defaultdict
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Enhanced copy button with better reliability
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Reliable copy button with fallback"""
#     if text is None:
#         text = ""
    
#     button_key = f"copy_{key}" if key else f"copy_{abs(hash(text[:100]))}"
    
#     # Create button
#     if st.button(f"⚡ {label}", key=button_key, help="Click to prepare text for copying"):
#         st.session_state[f"text_to_copy_{button_key}"] = text
#         st.success("✅ Ready to copy! Use the text area below:")
        
#     # Show text area if button was clicked
#     if f"text_to_copy_{button_key}" in st.session_state:
#         st.text_area(
#             "📋 Select all text and copy (Ctrl+A, Ctrl+C or Cmd+A, Cmd+C):",
#             value=st.session_state[f"text_to_copy_{button_key}"],
#             height=150,
#             key=f"copy_area_{button_key}",
#             help="Select all text in this box and copy it to your clipboard"
#         )

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .metric-card {
#         background: rgba(0, 20, 40, 0.6);
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#         padding: 15px;
#         margin: 10px 0;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
    
#     .success-metric {
#         color: #00ff00;
#         font-weight: bold;
#     }
    
#     .warning-metric {
#         color: #ffaa00;
#         font-weight: bold;
#     }
    
#     .error-metric {
#         color: #ff4444;
#         font-weight: bold;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite v2.1</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python_enhanced(code: str):
#     """Comprehensive Python code analysis with enhanced metrics"""
#     report = {
#         "basic_stats": {},
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "variables": [],
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": [],
#         "complexity_metrics": {},
#         "code_quality": {},
#         "detailed_counts": {}
#     }

#     if not code or not code.strip():
#         return report

#     lines = code.splitlines()
#     code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
#     comment_lines = [line for line in lines if line.strip().startswith("#")]
#     blank_lines = [line for line in lines if not line.strip()]

#     # Basic statistics
#     report["basic_stats"] = {
#         "total_lines": len(lines),
#         "code_lines": len(code_lines),
#         "comment_lines": len(comment_lines),
#         "blank_lines": len(blank_lines),
#         "characters": len(code),
#         "words": len(code.split())
#     }

#     # Initialize counters
#     function_count = 0
#     class_count = 0
#     import_count = 0
#     print_count = 0
#     if_count = 0
#     for_count = 0
#     while_count = 0
#     try_count = 0
#     with_count = 0
#     def_count = 0
#     lambda_count = 0
#     list_comp_count = 0
#     dict_comp_count = 0

#     # Pattern-based counting
#     for line in code_lines:
#         stripped_line = line.strip()
        
#         # Count various constructs
#         if stripped_line.startswith("def "):
#             def_count += 1
#         if stripped_line.startswith("class "):
#             class_count += 1
#         if stripped_line.startswith(("import ", "from ")):
#             import_count += 1
        
#         # Count control structures and statements
#         print_count += len(re.findall(r'\bprint\s*\(', line))
#         if_count += len(re.findall(r'\bif\b', line))
#         for_count += len(re.findall(r'\bfor\b', line))
#         while_count += len(re.findall(r'\bwhile\b', line))
#         try_count += len(re.findall(r'\btry\b', line))
#         with_count += len(re.findall(r'\bwith\b', line))
#         lambda_count += len(re.findall(r'\blambda\b', line))
#         list_comp_count += len(re.findall(r'\[.*for.*in.*\]', line))
#         dict_comp_count += len(re.findall(r'\{.*for.*in.*\}', line))

#     report["detailed_counts"] = {
#         "functions": def_count,
#         "classes": class_count,
#         "imports": import_count,
#         "print_statements": print_count,
#         "if_statements": if_count,
#         "for_loops": for_count,
#         "while_loops": while_count,
#         "try_blocks": try_count,
#         "with_statements": with_count,
#         "lambda_expressions": lambda_count,
#         "list_comprehensions": list_comp_count,
#         "dict_comprehensions": dict_comp_count
#     }

#     # Calculate complexity metrics
#     total_constructs = sum([if_count, for_count, while_count, try_count, def_count])
#     complexity_score = total_constructs / max(1, len(code_lines)) * 100
    
#     report["complexity_metrics"] = {
#         "cyclomatic_complexity_estimate": total_constructs + 1,
#         "complexity_per_line": round(complexity_score, 2),
#         "nesting_level_estimate": max(0, len(re.findall(r'    ', code)) // len(code_lines) * 10) if code_lines else 0
#     }

#     # Code quality metrics
#     comment_ratio = len(comment_lines) / max(1, len(lines)) * 100
#     avg_line_length = sum(len(line) for line in code_lines) / max(1, len(code_lines))
    
#     report["code_quality"] = {
#         "comment_ratio": round(comment_ratio, 2),
#         "avg_line_length": round(avg_line_length, 2),
#         "code_to_comment_ratio": round(len(code_lines) / max(1, len(comment_lines)), 2)
#     }

#     # Basic parsing for simple analysis
#     for line in code_lines:
#         stripped = line.strip()
#         if stripped.startswith("def "):
#             match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["functions"].append(match.group(1))
#         elif stripped.startswith("class "):
#             match = re.match(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["classes"].append(match.group(1))
#         elif stripped.startswith(("import ", "from ")):
#             report["imports"].append(stripped)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Enhanced AST analysis
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()
#     builtin_functions_used = set()
    
#     builtin_funcs = {
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     }

#     class EnhancedCodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
            
#             # Check for long functions
#             func_lines = len([n for n in ast.walk(node) if hasattr(n, 'lineno')])
#             if func_lines > 50:
#                 report["warnings"].append(f"Function '{node.name}' is very long ({func_lines} lines)")
#                 report["fixes"].append(f"Consider breaking down '{node.name}' into smaller functions")
            
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#                 if node.id in builtin_funcs:
#                     builtin_functions_used.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#                 report["variables"].append(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 if node.func.id in {"eval", "exec"}:
#                     report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                     report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#                 elif node.func.id == "print" and len(node.args) == 0:
#                     report["warnings"].append("Empty print() statement found")
#                     report["fixes"].append("Remove empty print() or add meaningful content")
#             self.generic_visit(node)

#     EnhancedCodeAnalyzer().visit(tree)

#     # Add builtin functions used to report
#     report["builtin_functions_used"] = sorted(list(builtin_functions_used))

#     # Check for unused imports
#     unused_imports = []
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             unused_imports.append(name)
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}' if not needed")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     shadowed_builtins = []
#     for name in assigned_names:
#         if name in builtins_list:
#             shadowed_builtins.append(name)
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Code quality analysis
#     if report["code_quality"]["comment_ratio"] < 5:
#         report["warnings"].append("Low comment density - consider adding more documentation")
#         report["fixes"].append("Add docstrings to functions and classes, and inline comments for complex logic")
    
#     if report["code_quality"]["avg_line_length"] > 100:
#         report["warnings"].append("Some lines are very long - consider breaking them up")
#         report["fixes"].append("Break long lines at logical points (after commas, operators, etc.)")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("🎉 Code looks excellent! Consider adding unit tests and type hints.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes for better code quality.")

#     # Remove duplicate variables
#     report["variables"] = sorted(list(set(report["variables"])))

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res", "var", "obj"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Perfect formatting (suspicious)
#     perfect_indent = all(len(line) - len(line.lstrip()) % 4 == 0 for line in code_lines if line.strip())
#     features["perfect_formatting"] = 1.0 if perfect_indent and len(code_lines) > 10 else 0.0
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * features["perfect_formatting"]
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
#     if features["perfect_formatting"] == 1.0:
#         reasons.append("Suspiciously perfect code formatting")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             # Show document metrics
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.metric("Characters", f"{len(content):,}")
#             with col2:
#                 st.metric("Words", f"{len(content.split()):,}")
#             with col3:
#                 st.metric("Lines", f"{len(content.splitlines()):,}")
#             with col4:
#                 st.metric("Paragraphs", f"{len([p for p in content.split('\\n\\n') if p.strip()]):,}")
            
#             with st.expander("📊 Summary Results", expanded=True):
#                 st.subheader("📋 Generated Summary")
#                 if doc_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     copy_button(summary, "Copy Summary", key="doc_copy_btn")
#                 with col2:
#                     st.download_button(
#                         "💾 Download", 
#                         summary, 
#                         "summary.txt",
#                         mime="text/plain",
#                         key="doc_download_btn"
#                     )

# # Tab 2: Enhanced Code Analyzer
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis with comprehensive metrics and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing code..."):
#                 report = analyze_python_enhanced(code_content)

#             st.success("🎉 Analysis Complete!")

#             # Basic Statistics Section
#             st.subheader("📊 Code Statistics")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("Total Lines", report["basic_stats"].get("total_lines", 0))
#                 st.metric("Functions", report["detailed_counts"].get("functions", 0))
#             with col2:
#                 st.metric("Code Lines", report["basic_stats"].get("code_lines", 0))
#                 st.metric("Classes", report["detailed_counts"].get("classes", 0))
#             with col3:
#                 st.metric("Comments", report["basic_stats"].get("comment_lines", 0))
#                 st.metric("Imports", report["detailed_counts"].get("imports", 0))
#             with col4:
#                 st.metric("Characters", f"{report['basic_stats'].get('characters', 0):,}")
#                 st.metric("Print Statements", report["detailed_counts"].get("print_statements", 0))

#             # Detailed Counts Section
#             st.subheader("🔧 Code Constructs")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("If Statements", report["detailed_counts"].get("if_statements", 0))
#                 st.metric("For Loops", report["detailed_counts"].get("for_loops", 0))
#             with col2:
#                 st.metric("While Loops", report["detailed_counts"].get("while_loops", 0))
#                 st.metric("Try Blocks", report["detailed_counts"].get("try_blocks", 0))
#             with col3:
#                 st.metric("With Statements", report["detailed_counts"].get("with_statements", 0))
#                 st.metric("Lambda Expressions", report["detailed_counts"].get("lambda_expressions", 0))
#             with col4:
#                 st.metric("List Comprehensions", report["detailed_counts"].get("list_comprehensions", 0))
#                 st.metric("Dict Comprehensions", report["detailed_counts"].get("dict_comprehensions", 0))

#             # Code Quality Metrics
#             st.subheader("📈 Quality Metrics")
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 comment_ratio = report["code_quality"].get("comment_ratio", 0)
#                 st.metric("Comment Ratio", f"{comment_ratio:.1f}%")
                
#             with col2:
#                 avg_line_length = report["code_quality"].get("avg_line_length", 0)
#                 st.metric("Avg Line Length", f"{avg_line_length:.1f} chars")
                
#             with col3:
#                 complexity = report["complexity_metrics"].get("cyclomatic_complexity_estimate", 0)
#                 st.metric("Complexity Score", complexity)

#             # Main Analysis Results
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.subheader("📋 Code Summary")
#                 st.write(report["purpose_summary"])
                
#                 if report["functions"]:
#                     st.subheader("🔧 Functions Found")
#                     for func in report["functions"][:10]:  # Show first 10
#                         st.write(f"• `{func}()`")
#                     if len(report["functions"]) > 10:
#                         st.write(f"... and {len(report['functions']) - 10} more")
                
#                 if report["classes"]:
#                     st.subheader("🏗️ Classes Found")
#                     for cls in report["classes"]:
#                         st.write(f"• `{cls}`")
                
#                 if report["builtin_functions_used"]:
#                     st.subheader("🐍 Built-in Functions Used")
#                     builtin_display = ", ".join(f"`{func}()`" for func in report["builtin_functions_used"][:15])
#                     st.write(builtin_display)
#                     if len(report["builtin_functions_used"]) > 15:
#                         st.write(f"... and {len(report['builtin_functions_used']) - 15} more")
            
#             with col2:
#                 # Errors Section
#                 st.subheader("❌ Errors")
#                 if report["errors"]:
#                     for error in report["errors"]:
#                         st.error(error)
#                 else:
#                     st.success("✅ No syntax errors found!")
                
#                 # Warnings Section
#                 st.subheader("⚠️ Warnings")
#                 if report["warnings"]:
#                     for warning in report["warnings"][:8]:  # Show first 8 warnings
#                         st.warning(warning)
#                     if len(report["warnings"]) > 8:
#                         st.info(f"... and {len(report['warnings']) - 8} more warnings")
#                 else:
#                     st.success("✅ No warnings!")
                
#                 # Recommendations Section
#                 st.subheader("💡 Recommendations")
#                 for fix in report["fixes"][:6]:  # Show first 6 recommendations
#                     st.info(fix)
#                 if len(report["fixes"]) > 6:
#                     st.info(f"... and {len(report['fixes']) - 6} more recommendations")

#             # Imports and Variables
#             with st.expander("📦 Imports & Variables Details", expanded=False):
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     if report["imports"]:
#                         st.subheader("📥 Imports")
#                         for imp in report["imports"]:
#                             st.code(imp, language="python")
#                     else:
#                         st.write("No imports found")
                
#                 with col2:
#                     if report["variables"]:
#                         st.subheader("📝 Variables")
#                         variables_display = ", ".join(f"`{var}`" for var in report["variables"][:20])
#                         st.write(variables_display)
#                         if len(report["variables"]) > 20:
#                             st.write(f"... and {len(report['variables']) - 20} more variables")
#                     else:
#                         st.write("No variables detected")
            
#             # Copy and download options
#             col3, col4 = st.columns(2)
#             with col3:
#                 # Create a formatted report for copying
#                 formatted_report = f"""
# CODE ANALYSIS REPORT
# ==================

# BASIC STATISTICS:
# - Total Lines: {report['basic_stats'].get('total_lines', 0)}
# - Code Lines: {report['basic_stats'].get('code_lines', 0)}
# - Comment Lines: {report['basic_stats'].get('comment_lines', 0)}
# - Characters: {report['basic_stats'].get('characters', 0):,}

# CODE CONSTRUCTS:
# - Functions: {report['detailed_counts'].get('functions', 0)}
# - Classes: {report['detailed_counts'].get('classes', 0)}
# - Imports: {report['detailed_counts'].get('imports', 0)}
# - Print Statements: {report['detailed_counts'].get('print_statements', 0)}
# - If Statements: {report['detailed_counts'].get('if_statements', 0)}
# - For Loops: {report['detailed_counts'].get('for_loops', 0)}
# - While Loops: {report['detailed_counts'].get('while_loops', 0)}

# QUALITY METRICS:
# - Comment Ratio: {report['code_quality'].get('comment_ratio', 0):.1f}%
# - Avg Line Length: {report['code_quality'].get('avg_line_length', 0):.1f} chars
# - Complexity Score: {report['complexity_metrics'].get('cyclomatic_complexity_estimate', 0)}

# SUMMARY: {report['purpose_summary']}

# ERRORS: {len(report['errors'])} found
# WARNINGS: {len(report['warnings'])} found
# RECOMMENDATIONS: {len(report['fixes'])} provided
# """
#                 copy_button(formatted_report, "Copy Report", key="code_copy_btn")
#             with col4:
#                 st.download_button(
#                     "💾 Download Report", 
#                     formatted_report, 
#                     "code_analysis_report.txt",
#                     mime="text/plain",
#                     key="code_download_btn"
#                 )

# # Tab 3: AI Detection
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Advanced pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze for AI patterns...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("🔍 Analysis Complete!")
            
#             # Display results with enhanced visualization
#             score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
#             with st.expander(f"{score_color} Detection Results", expanded=True):
#                 # Main score display
#                 col1, col2, col3 = st.columns([1, 2, 1])
                
#                 with col2:
#                     # Create a visual score indicator
#                     score_val = result['score']
#                     if score_val < 45:
#                         color = "success"
#                         interpretation = "Human-like patterns detected"
#                     elif score_val < 65:
#                         color = "warning"
#                         interpretation = "Mixed or uncertain patterns"
#                     else:
#                         color = "error"
#                         interpretation = "AI-like patterns detected"
                    
#                     st.metric(
#                         "🎯 AI Likelihood Score", 
#                         f"{score_val}%",
#                         delta=f"{score_val - 50:+.1f}% vs baseline",
#                         delta_color="inverse"
#                     )
                    
#                     # Progress bar for visual representation
#                     progress_color = "#ff4444" if score_val >= 65 else "#ffaa00" if score_val >= 45 else "#00ff00"
#                     st.markdown(f"""
#                     <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 5px; margin: 10px 0;">
#                         <div style="background: {progress_color}; height: 20px; width: {score_val}%; border-radius: 8px; transition: all 0.3s;"></div>
#                     </div>
#                     <p style="text-align: center; color: {progress_color}; font-weight: bold;">{interpretation}</p>
#                     """, unsafe_allow_html=True)
                
#                 st.markdown(f"**🏷️ Assessment:** {result['label']}")
                
#                 # Key indicators
#                 if result["reasons"]:
#                     st.subheader("🔍 Key Indicators Found")
#                     for i, reason in enumerate(result["reasons"], 1):
#                         st.write(f"{i}. {reason}")
#                 else:
#                     st.success("✅ No significant AI patterns detected")
                
#                 # Detailed feature analysis
#                 st.subheader("📊 Detailed Feature Analysis")
                
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.write("**📈 Pattern Metrics:**")
#                     for feature, value in result["features"].items():
#                         feature_name = feature.replace("_", " ").title()
                        
#                         # Color code based on feature values
#                         if "density" in feature or "ratio" in feature:
#                             if value > 0.3:
#                                 color = "🔴"
#                             elif value > 0.15:
#                                 color = "🟡"
#                             else:
#                                 color = "🟢"
#                         else:
#                             color = "🔵"
                        
#                         st.write(f"{color} **{feature_name}:** `{value:.3f}`")
                
#                 with col2:
#                     st.write("**🎯 Confidence Breakdown:**")
                    
#                     # Create confidence indicators for each feature
#                     features = result["features"]
                    
#                     if "comment_density" in features:
#                         cd_score = abs(features["comment_density"] - 0.15) / 0.15
#                         st.write(f"📝 Comment Pattern: `{cd_score:.2f}` {'⚠️' if cd_score > 0.5 else '✅'}")
                    
#                     if "repeated_line_ratio" in features:
#                         rr_score = features["repeated_line_ratio"]
#                         st.write(f"🔄 Code Repetition: `{rr_score:.2f}` {'⚠️' if rr_score > 0.1 else '✅'}")
                    
#                     if "generic_name_density" in features:
#                         gn_score = features["generic_name_density"]
#                         st.write(f"🏷️ Generic Names: `{gn_score:.2f}` {'⚠️' if gn_score > 0.03 else '✅'}")
                    
#                     if "perfect_formatting" in features:
#                         pf_score = features["perfect_formatting"]
#                         st.write(f"✨ Perfect Format: `{pf_score:.2f}` {'⚠️' if pf_score > 0.5 else '✅'}")
                
#                 # Copy and download
#                 col4, col5 = st.columns(2)
#                 with col4:
#                     detection_report = f"""
# AI DETECTION ANALYSIS REPORT
# ============================

# OVERALL ASSESSMENT: {result['label']}
# CONFIDENCE SCORE: {result['score']}%

# KEY INDICATORS:
# {chr(10).join(f"- {reason}" for reason in result['reasons']) if result['reasons'] else "- No significant patterns detected"}

# FEATURE ANALYSIS:
# {chr(10).join(f"- {k.replace('_', ' ').title()}: {v:.3f}" for k, v in result['features'].items())}

# INTERPRETATION:
# {interpretation}
# """
#                     copy_button(detection_report, "Copy Results", key="ai_copy_btn")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Analysis", 
#                         detection_report, 
#                         "ai_detection_report.txt",
#                         mime="text/plain",
#                         key="ai_download_btn"
#                     )

# # Tab 4: URL Extractor
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and intelligent analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "🎯 Target URL", 
#             placeholder="Enter any URL for intelligent content extraction...",
#             key="url_input_field",
#             help="Supports web pages, GitHub files, documentation, articles, and more"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 15, 7, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullet Points", value=True, key="url_use_bullets")
#         url_show_preview = st.checkbox("Show Content Preview", value=True, key="url_show_preview")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("⚠️ Please enter a valid URL to proceed.")
#         else:
#             with st.spinner("🔄 Extracting content from URL..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("✅ Content extracted successfully!")
                
#                 # Enhanced metrics display
#                 words = content.split()
#                 sentences = len(re.findall(r'[.!?]+', content))
#                 paragraphs = len([p for p in content.split('\n\n') if p.strip()])
                
#                 col1, col2, col3, col4, col5 = st.columns(5)
#                 with col1:
#                     st.metric("📄 Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("📝 Words", f"{len(words):,}")
#                 with col3:
#                     st.metric("📋 Lines", f"{len(content.splitlines()):,}")
#                 with col4:
#                     st.metric("📖 Sentences", f"{sentences:,}")
#                 with col5:
#                     st.metric("📑 Paragraphs", f"{paragraphs:,}")
                
#                 # Reading time estimation
#                 avg_reading_speed = 200  # words per minute
#                 reading_time = max(1, len(words) // avg_reading_speed)
#                 st.info(f"📚 Estimated reading time: ~{reading_time} minute{'s' if reading_time != 1 else ''}")
                
#                 # Content preview with better formatting
#                 if url_show_preview:
#                     with st.expander("📄 Content Preview", expanded=False):
#                         preview_length = 3000
#                         preview = content[:preview_length]
#                         if len(content) > preview_length:
#                             preview += f"\n\n... [Content truncated - showing first {preview_length:,} characters of {len(content):,} total]"
                        
#                         # Try to detect if it's code
#                         if any(keyword in content.lower()[:500] for keyword in ['def ', 'class ', 'import ', 'function', '#include', 'public class']):
#                             st.code(preview, language="python" if "def " in preview or "import " in preview else "text")
#                         else:
#                             st.text(preview)
                
#                 # Generate enhanced summary
#                 with st.spinner("🧠 Generating intelligent summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 # Display summary with better styling
#                 st.subheader("🎯 Intelligent Content Summary")
                
#                 summary_container = st.container()
#                 with summary_container:
#                     if url_bullets:
#                         st.markdown(summary)
#                     else:
#                         st.write(summary)
                
#                 # Additional analysis
#                 with st.expander("📊 Content Analysis", expanded=False):
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.write("**📈 Content Statistics:**")
#                         avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
#                         st.write(f"• Average word length: {avg_word_length:.1f} characters")
                        
#                         if sentences > 0:
#                             avg_sentence_length = len(words) / sentences
#                             st.write(f"• Average sentence length: {avg_sentence_length:.1f} words")
                        
#                         # Most common words (excluding stopwords)
#                         filtered_words = [word.lower().strip('.,!?";()[]') for word in words 
#                                         if len(word) > 3 and word.lower() not in STOPWORDS]
#                         if filtered_words:
#                             common_words = Counter(filtered_words).most_common(5)
#                             st.write("• Most frequent words:")
#                             for word, count in common_words:
#                                 st.write(f"  - **{word}**: {count} times")
                    
#                     with col2:
#                         st.write("**🔍 Content Characteristics:**")
                        
#                         # Detect content type
#                         if any(keyword in content.lower() for keyword in ['function', 'variable', 'method', 'class', 'algorithm']):
#                             st.write("• 💻 **Type**: Technical/Programming content")
#                         elif any(keyword in content.lower() for keyword in ['research', 'study', 'analysis', 'data', 'results']):
#                             st.write("• 🔬 **Type**: Research/Academic content")
#                         elif any(keyword in content.lower() for keyword in ['tutorial', 'how to', 'step', 'guide', 'instructions']):
#                             st.write("• 📚 **Type**: Educational/Tutorial content")
#                         else:
#                             st.write("• 📰 **Type**: General/Article content")
                        
#                         # Complexity estimate
#                         complex_words = [word for word in words if len(word) > 7]
#                         complexity = len(complex_words) / max(len(words), 1) * 100
                        
#                         if complexity > 20:
#                             st.write("• 🎓 **Complexity**: Advanced")
#                         elif complexity > 12:
#                             st.write("• 📖 **Complexity**: Intermediate")
#                         else:
#                             st.write("• 📝 **Complexity**: Beginner-friendly")
                        
#                         st.write(f"• 📊 **Complexity Score**: {complexity:.1f}%")
                
#                 # Enhanced copy and download options
#                 col4, col5, col6 = st.columns(3)
#                 with col4:
#                     copy_button(summary, "Copy Summary", key="url_copy_summary")
#                 with col5:
#                     copy_button(content, "Copy Full Content", key="url_copy_full")
#                 with col6:
#                     # Create comprehensive report
#                     comprehensive_report = f"""
# URL EXTRACTION REPORT
# ====================

# SOURCE URL: {url_input}
# EXTRACTION DATE: {st.session_state.get('current_date', 'Today')}

# CONTENT METRICS:
# - Characters: {len(content):,}
# - Words: {len(words):,}
# - Lines: {len(content.splitlines()):,}
# - Sentences: {sentences:,}
# - Paragraphs: {paragraphs:,}
# - Estimated Reading Time: ~{reading_time} minute(s)

# INTELLIGENT SUMMARY:
# {summary}

# FULL EXTRACTED CONTENT:
# {content}
# """
#                     st.download_button(
#                         "💾 Download Full Report", 
#                         comprehensive_report, 
#                         f"url_analysis_report_{url_input.split('/')[-1][:20]}.txt",
#                         mime="text/plain",
#                         key="url_download_full"
#                     )

# # Enhanced Footer with additional info
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 30px;">
#     <h3 style="color: rgba(0, 249, 255, 0.8); font-family: 'Orbitron', monospace;">🌌 TECHNOVA AI NEXUS v2.1</h3>
#     <p style="color: rgba(0, 249, 255, 0.6); font-family: monospace; margin: 10px 0;">
#         Advanced Neural Processing Suite • Quantum Code Analysis • AI Pattern Detection
#     </p>
#     <p style="color: rgba(0, 249, 255, 0.4); font-size: 0.9em;">
#         Enhanced with comprehensive metrics, intelligent analysis, and reliable copy functionality
#     </p>
#     <div style="margin-top: 20px; color: rgba(0, 249, 255, 0.3);">
#         🚀 Built for developers, researchers, and AI enthusiasts
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Add session state management for better UX
# if 'analysis_history' not in st.session_state:
#     st.session_state['analysis_history'] = []

# # Optional: Add a sidebar with tips and shortcuts
# with st.sidebar:
#     st.header("⚡ Quick Tips")
#     st.write("""
#     **🔧 Code Analyzer:**
#     • Upload .py files for best results
#     • Supports GitHub raw URLs
#     • Detects 12+ code constructs
    
#     **🤖 AI Detection:**
#     • Analyzes patterns in code/text
#     • Uses multiple indicators
#     • Confidence scoring system
    
#     **🌐 URL Extractor:**
#     • Works with most websites
#     • Intelligent content filtering
#     • Automatic summarization
    
#     **📋 Copy Functionality:**
#     • Click copy button first
#     • Select all text in the box
#     • Use Ctrl+C (or Cmd+C) to copy
#     """)
    
#     if st.button("🗑️ Clear All Data", key="clear_all"):
#         for key in list(st.session_state.keys()):
#             if key.startswith(('text_to_copy_', 'copied_text_')):
#                 del st.session_state[key]
#         st.success("All temporary data cleared!")
#         st.rerun()








































# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# import re
# import base64
# import ast
# from collections import Counter, defaultdict
# import io

# # PDF extraction (optional)
# try:
#     import PyPDF2
#     PDF_AVAILABLE = True
# except ImportError:
#     PDF_AVAILABLE = False

# # Page config
# st.set_page_config(
#     page_title="Technova AI Nexus", 
#     layout="wide", 
#     initial_sidebar_state="collapsed"
# )

# # Simple and reliable copy function using streamlit components
# def copy_button(text: str, label: str = "Copy", key: str = None):
#     """Simple copy button using streamlit text area"""
#     if text is None:
#         text = ""
    
#     button_key = f"copy_btn_{key}" if key else f"copy_btn_{abs(hash(text[:50]))}"
#     area_key = f"copy_area_{key}" if key else f"copy_area_{abs(hash(text[:50]))}"
    
#     # Show copy button and text area side by side
#     col1, col2 = st.columns([1, 6])
    
#     with col1:
#         st.button(f"📋 {label}", key=button_key, help="Click to show text for copying")
    
#     with col2:
#         st.text_area(
#             "Select all text below and copy (Ctrl+A, Ctrl+C):",
#             value=text,
#             height=120,
#             key=area_key,
#             help="Select all text and copy to clipboard"
#         )

# # Simplified styling
# def set_tech_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
#     .stApp {
#         background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
#         color: #00f9ff;
#         font-family: 'Rajdhani', sans-serif;
#     }
    
#     h1, h2, h3, h4, h5, h6 {
#         font-family: 'Orbitron', monospace !important;
#         color: #00f9ff !important;
#         text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
#     }
    
#     .main-title {
#         font-size: 3rem;
#         text-align: center;
#         background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         margin: 2rem 0;
#     }
    
#     .subtitle {
#         text-align: center;
#         color: rgba(0, 249, 255, 0.8);
#         font-style: italic;
#         margin-bottom: 2rem;
#     }
    
#     .stTextArea textarea, .stTextInput input {
#         background: rgba(0, 20, 40, 0.8) !important;
#         border: 1px solid rgba(0, 249, 255, 0.3) !important;
#         color: #00f9ff !important;
#     }
    
#     .stButton > button {
#         background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
#         border: 1px solid rgba(0, 249, 255, 0.5) !important;
#         color: #00f9ff !important;
#         font-weight: bold !important;
#     }
    
#     .stTabs [data-baseweb="tab"] {
#         color: #00f9ff !important;
#         font-family: 'Orbitron', monospace !important;
#     }
    
#     .stExpander {
#         border: 1px solid rgba(0, 249, 255, 0.3);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Initialize styling
# set_tech_styling()

# # Main title
# st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
# st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite v2.1</p>', unsafe_allow_html=True)

# # Stopwords for summarization
# STOPWORDS = set([
#     "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", 
#     "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", 
#     "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from", 
#     "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than", 
#     "also", "can", "could", "should", "would", "may", "might", "have", "has", "had", 
#     "do", "does", "did", "done", "just", "over", "under", "more", "most", "other", 
#     "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom", 
#     "whose", "where", "when", "why", "how"
# ])

# def safe_sentence_split(text: str):
#     """Split text into sentences safely"""
#     pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
#     return [s.strip() for s in pattern.split(text) if s.strip()]

# def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
#     """Advanced text summarization using frequency analysis"""
#     if not text or not text.strip():
#         return "No content to summarize."
    
#     paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
#     sentences = []
#     for para in paragraphs:
#         sentences.extend(safe_sentence_split(para))
    
#     if not sentences:
#         return text

#     # Word frequency analysis
#     word_freq = Counter()
#     for s in sentences:
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         for w in words:
#             if w not in STOPWORDS and len(w) > 2:
#                 word_freq[w] += 1
    
#     if not word_freq:
#         return " ".join(sentences[:max_sentences])

#     # Normalize frequencies
#     max_freq = max(word_freq.values())
#     for w in list(word_freq.keys()):
#         word_freq[w] /= max_freq

#     # Score sentences
#     scored = []
#     for idx, s in enumerate(sentences):
#         words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
#         score = sum(word_freq.get(w, 0.0) for w in words)
#         length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
#         position_boost = 1.1 if idx < 3 else 1.0
#         scored.append((score / length_penalty * position_boost, idx, s))

#     # Select top sentences
#     scored.sort(key=lambda x: (-x[0], x[1]))
#     top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
#     if as_bullets:
#         return "\n".join([f"• {s}" for _, _, s in top])
#     return " ".join([s for _, _, s in top])

# def analyze_python_enhanced(code: str):
#     """Comprehensive Python code analysis with enhanced metrics"""
#     report = {
#         "basic_stats": {},
#         "functions": [], 
#         "classes": [], 
#         "imports": [], 
#         "variables": [],
#         "purpose_summary": "", 
#         "errors": [], 
#         "warnings": [], 
#         "fixes": [],
#         "complexity_metrics": {},
#         "code_quality": {},
#         "detailed_counts": {},
#         "builtin_functions_used": []  # Initialize this key
#     }

#     if not code or not code.strip():
#         return report

#     lines = code.splitlines()
#     code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
#     comment_lines = [line for line in lines if line.strip().startswith("#")]
#     blank_lines = [line for line in lines if not line.strip()]

#     # Basic statistics
#     report["basic_stats"] = {
#         "total_lines": len(lines),
#         "code_lines": len(code_lines),
#         "comment_lines": len(comment_lines),
#         "blank_lines": len(blank_lines),
#         "characters": len(code),
#         "words": len(code.split())
#     }

#     # Initialize counters
#     function_count = 0
#     class_count = 0
#     import_count = 0
#     print_count = 0
#     if_count = 0
#     for_count = 0
#     while_count = 0
#     try_count = 0
#     with_count = 0
#     def_count = 0
#     lambda_count = 0
#     list_comp_count = 0
#     dict_comp_count = 0

#     # Pattern-based counting
#     for line in code_lines:
#         stripped_line = line.strip()
        
#         # Count various constructs
#         if stripped_line.startswith("def "):
#             def_count += 1
#         if stripped_line.startswith("class "):
#             class_count += 1
#         if stripped_line.startswith(("import ", "from ")):
#             import_count += 1
        
#         # Count control structures and statements
#         print_count += len(re.findall(r'\bprint\s*\(', line))
#         if_count += len(re.findall(r'\bif\b', line))
#         for_count += len(re.findall(r'\bfor\b', line))
#         while_count += len(re.findall(r'\bwhile\b', line))
#         try_count += len(re.findall(r'\btry\b', line))
#         with_count += len(re.findall(r'\bwith\b', line))
#         lambda_count += len(re.findall(r'\blambda\b', line))
#         list_comp_count += len(re.findall(r'\[.*for.*in.*\]', line))
#         dict_comp_count += len(re.findall(r'\{.*for.*in.*\}', line))

#     report["detailed_counts"] = {
#         "functions": def_count,
#         "classes": class_count,
#         "imports": import_count,
#         "print_statements": print_count,
#         "if_statements": if_count,
#         "for_loops": for_count,
#         "while_loops": while_count,
#         "try_blocks": try_count,
#         "with_statements": with_count,
#         "lambda_expressions": lambda_count,
#         "list_comprehensions": list_comp_count,
#         "dict_comprehensions": dict_comp_count
#     }

#     # Calculate complexity metrics
#     total_constructs = sum([if_count, for_count, while_count, try_count, def_count])
#     complexity_score = total_constructs / max(1, len(code_lines)) * 100
    
#     report["complexity_metrics"] = {
#         "cyclomatic_complexity_estimate": total_constructs + 1,
#         "complexity_per_line": round(complexity_score, 2),
#         "nesting_level_estimate": max(0, len(re.findall(r'    ', code)) // len(code_lines) * 10) if code_lines else 0
#     }

#     # Code quality metrics
#     comment_ratio = len(comment_lines) / max(1, len(lines)) * 100
#     avg_line_length = sum(len(line) for line in code_lines) / max(1, len(code_lines))
    
#     report["code_quality"] = {
#         "comment_ratio": round(comment_ratio, 2),
#         "avg_line_length": round(avg_line_length, 2),
#         "code_to_comment_ratio": round(len(code_lines) / max(1, len(comment_lines)), 2)
#     }

#     # Basic parsing for simple analysis
#     for line in code_lines:
#         stripped = line.strip()
#         if stripped.startswith("def "):
#             match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["functions"].append(match.group(1))
#         elif stripped.startswith("class "):
#             match = re.match(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
#             if match:
#                 report["classes"].append(match.group(1))
#         elif stripped.startswith(("import ", "from ")):
#             report["imports"].append(stripped)

#     # Generate purpose summary
#     report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

#     # AST analysis for deeper insights
#     try:
#         tree = ast.parse(code)
#     except SyntaxError as e:
#         report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
#         report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
#         return report

#     # Enhanced AST analysis
#     imported_names = set()
#     used_names = set()
#     assigned_names = set()
#     builtin_functions_used = set()
    
#     builtin_funcs = {
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     }

#     class EnhancedCodeAnalyzer(ast.NodeVisitor):
#         def visit_Import(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name.split(".")[0])
#             self.generic_visit(node)

#         def visit_ImportFrom(self, node):
#             for alias in node.names:
#                 imported_names.add(alias.asname or alias.name)
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             assigned_names.add(node.name)
#             # Check for mutable default arguments
#             for default in node.args.defaults:
#                 if isinstance(default, (ast.List, ast.Dict, ast.Set)):
#                     report["warnings"].append(f"Mutable default argument in '{node.name}'")
#                     report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
            
#             # Check for long functions
#             func_lines = len([n for n in ast.walk(node) if hasattr(n, 'lineno')])
#             if func_lines > 50:
#                 report["warnings"].append(f"Function '{node.name}' is very long ({func_lines} lines)")
#                 report["fixes"].append(f"Consider breaking down '{node.name}' into smaller functions")
            
#             self.generic_visit(node)

#         def visit_ClassDef(self, node):
#             assigned_names.add(node.name)
#             self.generic_visit(node)

#         def visit_Name(self, node):
#             if isinstance(node.ctx, ast.Load):
#                 used_names.add(node.id)
#                 if node.id in builtin_funcs:
#                     builtin_functions_used.add(node.id)
#             elif isinstance(node.ctx, ast.Store):
#                 assigned_names.add(node.id)
#                 report["variables"].append(node.id)
#             self.generic_visit(node)

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 if node.func.id in {"eval", "exec"}:
#                     report["warnings"].append(f"Dangerous {node.func.id} usage detected")
#                     report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
#                 elif node.func.id == "print" and len(node.args) == 0:
#                     report["warnings"].append("Empty print() statement found")
#                     report["fixes"].append("Remove empty print() or add meaningful content")
#             self.generic_visit(node)

#     EnhancedCodeAnalyzer().visit(tree)

#     # Add builtin functions used to report
#     report["builtin_functions_used"] = sorted(list(builtin_functions_used))

#     # Check for unused imports
#     unused_imports = []
#     for name in sorted(imported_names):
#         if name not in used_names and name not in {"__future__"}:
#             unused_imports.append(name)
#             report["warnings"].append(f"Possibly unused import: '{name}'")
#             report["fixes"].append(f"Remove unused import '{name}' if not needed")

#     # Check for builtin shadowing
#     builtins_list = [
#         'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
#         'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
#         'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
#         'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
#         'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
#     ]
    
#     shadowed_builtins = []
#     for name in assigned_names:
#         if name in builtins_list:
#             shadowed_builtins.append(name)
#             report["warnings"].append(f"Variable '{name}' shadows builtin")
#             report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

#     # Code quality analysis
#     if report["code_quality"]["comment_ratio"] < 5:
#         report["warnings"].append("Low comment density - consider adding more documentation")
#         report["fixes"].append("Add docstrings to functions and classes, and inline comments for complex logic")
    
#     if report["code_quality"]["avg_line_length"] > 100:
#         report["warnings"].append("Some lines are very long - consider breaking them up")
#         report["fixes"].append("Break long lines at logical points (after commas, operators, etc.)")

#     # Add general recommendations
#     if not report["errors"]:
#         if not report["warnings"]:
#             report["fixes"].append("🎉 Code looks excellent! Consider adding unit tests and type hints.")
#         else:
#             report["fixes"].append("Review warnings above and apply suggested fixes for better code quality.")

#     # Remove duplicate variables
#     report["variables"] = sorted(list(set(report["variables"])))

#     return report

# def detect_ai_generated_code(code: str) -> dict:
#     """Detect if code might be AI-generated based on patterns"""
#     if not code or not code.strip():
#         return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
#     lines = code.splitlines()
#     code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
#     comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
#     features = {}
#     total_lines = max(1, len(lines))
    
#     # Comment density
#     features["comment_density"] = len(comment_lines) / total_lines
    
#     # Repeated lines
#     normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
#     counts = Counter(normalized)
#     repeated = sum(c for c in counts.values() if c > 1)
#     features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
#     # Generic variable names
#     generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res", "var", "obj"}
#     tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
#     generic_count = sum(1 for t in tokens if t in generic_names)
#     features["generic_name_density"] = generic_count / max(1, len(tokens))
    
#     # Perfect formatting (suspicious)
#     perfect_indent = all(len(line) - len(line.lstrip()) % 4 == 0 for line in code_lines if line.strip())
#     features["perfect_formatting"] = 1.0 if perfect_indent and len(code_lines) > 10 else 0.0
    
#     # Calculate score
#     score = (
#         25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
#         35 * features["repeated_line_ratio"] +
#         20 * min(1.0, features["generic_name_density"] * 20) +
#         20 * features["perfect_formatting"]
#     )
    
#     score = max(0.0, min(100.0, score))
    
#     # Determine label
#     if score >= 70:
#         label = "🚨 Likely AI-generated"
#     elif score >= 45:
#         label = "🤔 Unclear/Mixed"
#     else:
#         label = "✅ Likely human-written"
    
#     # Generate reasons
#     reasons = []
#     if features["repeated_line_ratio"] > 0.1:
#         reasons.append("High repetition of similar code patterns")
#     if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
#         reasons.append("Unusual comment density")
#     if features["generic_name_density"] > 0.03:
#         reasons.append("Frequent generic variable names")
#     if features["perfect_formatting"] == 1.0:
#         reasons.append("Suspiciously perfect code formatting")
    
#     return {
#         "score": round(score, 1), 
#         "label": label, 
#         "reasons": reasons, 
#         "features": features
#     }

# def fetch_from_url(url: str) -> str:
#     """Fetch and extract text content from URL"""
#     try:
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         }
#         resp = requests.get(url, timeout=10, headers=headers)
#         resp.raise_for_status()
        
#         content_type = resp.headers.get("Content-Type", "")
#         if "text/html" in content_type:
#             soup = BeautifulSoup(resp.text, "html.parser")
#             # Remove unwanted elements
#             for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
#                 element.extract()
#             return soup.get_text(separator="\n", strip=True)
#         else:
#             return resp.text
            
#     except requests.exceptions.RequestException as e:
#         return f"❌ Error fetching URL: {str(e)}"
#     except Exception as e:
#         return f"❌ Error processing content: {str(e)}"

# # Create tabs
# tabs = st.tabs([
#     "📄 Document Processor", 
#     "🧠 Code Analyzer", 
#     "🤖 AI Detection", 
#     "🌐 URL Extractor"
# ])

# # Tab 1: Document Processor
# with tabs[0]:
#     st.header("📄 Neural Document Processor")
#     st.write("*Advanced text analysis and summarization*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         doc_text = st.text_area(
#             "Input Text", 
#             height=200, 
#             placeholder="Paste your document content here...",
#             key="doc_text_input"
#         )
    
#     with col2:
#         doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
#         doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
#         doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
#         doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

#     if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
#         content = ""
        
#         # Get content from various sources
#         if doc_file:
#             if doc_file.name.lower().endswith(".pdf"):
#                 if not PDF_AVAILABLE:
#                     st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
#                 else:
#                     try:
#                         reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
#                         pages_text = []
#                         for page in reader.pages:
#                             pages_text.append(page.extract_text() or "")
#                         content = "\n".join(pages_text)
#                     except Exception as e:
#                         st.error(f"PDF error: {e}")
#             else:
#                 content = doc_file.read().decode("utf-8", errors="ignore")
#         elif doc_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(doc_url.strip())
#         elif doc_text.strip():
#             content = doc_text

#         if not content:
#             st.warning("Please provide content via text, file, or URL.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Processing..."):
#                 summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
#             st.success("Analysis Complete!")
            
#             # Show summary FIRST (most important)
#             st.subheader("📋 Generated Summary")
#             if doc_bullets:
#                 st.markdown(summary)
#             else:
#                 st.write(summary)
            
#             # Copy functionality for summary
#             st.subheader("📋 Copy Summary")
#             copy_button(summary, "Copy Summary", key="doc_summary")
            
#             # Then show document metrics
#             st.subheader("📊 Document Statistics")
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.metric("Characters", f"{len(content):,}")
#             with col2:
#                 st.metric("Words", f"{len(content.split()):,}")
#             with col3:
#                 st.metric("Lines", f"{len(content.splitlines()):,}")
#             with col4:
#                 st.metric("Paragraphs", f"{len([p for p in content.split('\\n\\n') if p.strip()]):,}")
            
#             # Download option
#             st.download_button(
#                 "💾 Download Summary", 
#                 summary, 
#                 "summary.txt",
#                 mime="text/plain",
#                 key="doc_download_btn"
#             )

# # Tab 2: Enhanced Code Analyzer with reordered sections
# with tabs[1]:
#     st.header("🧠 Quantum Code Analyzer")
#     st.write("*Deep code analysis with comprehensive metrics and optimization recommendations*")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         code_text = st.text_area(
#             "Python Code", 
#             height=250, 
#             placeholder="Paste your Python code here...",
#             key="code_text_input"
#         )
    
#     with col2:
#         code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
#         code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

#     if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
#         code_content = ""
        
#         if code_file:
#             code_content = code_file.read().decode("utf-8", errors="ignore")
#         elif code_url.strip():
#             with st.spinner("Fetching code..."):
#                 code_content = fetch_from_url(code_url.strip())
#         elif code_text.strip():
#             code_content = code_text

#         if not code_content:
#             st.warning("Please provide code via input, file, or URL.")
#         elif code_content.startswith("❌"):
#             st.error(code_content)
#         else:
#             with st.expander("Code Preview", expanded=False):
#                 st.code(code_content, language="python")

#             with st.spinner("Analyzing code..."):
#                 report = analyze_python_enhanced(code_content)

#             st.success("🎉 Analysis Complete!")

#             # PRIORITY SECTION 1: ERRORS (Most Important)
#             st.header("❌ Errors")
#             if report["errors"]:
#                 for error in report["errors"]:
#                     st.error(error)
#             else:
#                 st.success("✅ No syntax errors found!")
            
#             # PRIORITY SECTION 2: WARNINGS
#             st.header("⚠️ Warnings")
#             if report["warnings"]:
#                 for warning in report["warnings"]:
#                     st.warning(warning)
#             else:
#                 st.success("✅ No warnings!")
            
#             # PRIORITY SECTION 3: SUGGESTIONS/RECOMMENDATIONS
#             st.header("💡 Suggestions & Recommendations")
#             for fix in report["fixes"]:
#                 st.info(fix)
            
#             # PRIORITY SECTION 4: CODE SUMMARY
#             st.header("📋 Code Summary")
#             st.write(report["purpose_summary"])
            
#             # Copy functionality for main analysis
#             st.header("📋 Copy Analysis Report")
#             formatted_report = f"""
# CODE ANALYSIS REPORT
# ==================

# ERRORS ({len(report['errors'])} found):
# {chr(10).join(f"- {error}" for error in report['errors']) if report['errors'] else "✅ No errors"}

# WARNINGS ({len(report['warnings'])} found):
# {chr(10).join(f"- {warning}" for warning in report['warnings']) if report['warnings'] else "✅ No warnings"}

# RECOMMENDATIONS:
# {chr(10).join(f"- {fix}" for fix in report['fixes'])}

# CODE SUMMARY:
# {report['purpose_summary']}

# FUNCTIONS FOUND ({len(report['functions'])}):
# {', '.join(report['functions']) if report['functions'] else "None"}

# CLASSES FOUND ({len(report['classes'])}):
# {', '.join(report['classes']) if report['classes'] else "None"}

# DETAILED STATISTICS:
# - Total Lines: {report['basic_stats'].get('total_lines', 0)}
# - Code Lines: {report['basic_stats'].get('code_lines', 0)}
# - Comment Lines: {report['basic_stats'].get('comment_lines', 0)}
# - Functions: {report['detailed_counts'].get('functions', 0)}
# - Classes: {report['detailed_counts'].get('classes', 0)}
# - Imports: {report['detailed_counts'].get('imports', 0)}
# - Print Statements: {report['detailed_counts'].get('print_statements', 0)}
# - If Statements: {report['detailed_counts'].get('if_statements', 0)}
# - For Loops: {report['detailed_counts'].get('for_loops', 0)}
# - While Loops: {report['detailed_counts'].get('while_loops', 0)}
# """
#             copy_button(formatted_report, "Copy Full Report", key="code_report")
            
#             # NOW SHOW DETAILED METRICS (Lower Priority)
#             st.header("📊 Detailed Code Metrics")
            
#             # Functions and Classes Found
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 if report["functions"]:
#                     st.subheader("🔧 Functions Found")
#                     for func in report["functions"][:10]:  # Show first 10
#                         st.write(f"• `{func}()`")
#                     if len(report["functions"]) > 10:
#                         st.write(f"... and {len(report['functions']) - 10} more")
                
#                 # SAFE ACCESS TO builtin_functions_used - FIXED LINE
#                 builtin_functions = report.get("builtin_functions_used", [])
#                 if builtin_functions:
#                     st.subheader("🐍 Built-in Functions Used")
#                     builtin_display = ", ".join(f"`{func}()`" for func in builtin_functions[:15])
#                     st.write(builtin_display)
#                     if len(builtin_functions) > 15:
#                         st.write(f"... and {len(builtin_functions) - 15} more")
            
#             with col2:
#                 if report["classes"]:
#                     st.subheader("🏗️ Classes Found")
#                     for cls in report["classes"]:
#                         st.write(f"• `{cls}`")
                
#                 if report["variables"]:
#                     st.subheader("📝 Variables")
#                     variables_display = ", ".join(f"`{var}`" for var in report["variables"][:20])
#                     st.write(variables_display)
#                     if len(report["variables"]) > 20:
#                         st.write(f"... and {len(report['variables']) - 20} more variables")

#             # Basic Statistics Section
#             st.subheader("📈 Line Statistics")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("Total Lines", report["basic_stats"].get("total_lines", 0))
#                 st.metric("Functions", report["detailed_counts"].get("functions", 0))
#             with col2:
#                 st.metric("Code Lines", report["basic_stats"].get("code_lines", 0))
#                 st.metric("Classes", report["detailed_counts"].get("classes", 0))
#             with col3:
#                 st.metric("Comments", report["basic_stats"].get("comment_lines", 0))
#                 st.metric("Imports", report["detailed_counts"].get("imports", 0))
#             with col4:
#                 st.metric("Characters", f"{report['basic_stats'].get('characters', 0):,}")
#                 st.metric("Print Statements", report["detailed_counts"].get("print_statements", 0))

#             # Detailed Counts Section
#             st.subheader("🔧 Code Constructs")
#             col1, col2, col3, col4 = st.columns(4)
            
#             with col1:
#                 st.metric("If Statements", report["detailed_counts"].get("if_statements", 0))
#                 st.metric("For Loops", report["detailed_counts"].get("for_loops", 0))
#             with col2:
#                 st.metric("While Loops", report["detailed_counts"].get("while_loops", 0))
#                 st.metric("Try Blocks", report["detailed_counts"].get("try_blocks", 0))
#             with col3:
#                 st.metric("With Statements", report["detailed_counts"].get("with_statements", 0))
#                 st.metric("Lambda Expressions", report["detailed_counts"].get("lambda_expressions", 0))
#             with col4:
#                 st.metric("List Comprehensions", report["detailed_counts"].get("list_comprehensions", 0))
#                 st.metric("Dict Comprehensions", report["detailed_counts"].get("dict_comprehensions", 0))

#             # Code Quality Metrics
#             st.subheader("📊 Quality Metrics")
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 comment_ratio = report["code_quality"].get("comment_ratio", 0)
#                 st.metric("Comment Ratio", f"{comment_ratio:.1f}%")
                
#             with col2:
#                 avg_line_length = report["code_quality"].get("avg_line_length", 0)
#                 st.metric("Avg Line Length", f"{avg_line_length:.1f} chars")
                
#             with col3:
#                 complexity = report["complexity_metrics"].get("cyclomatic_complexity_estimate", 0)
#                 st.metric("Complexity Score", complexity)

#             # Imports and Variables Details
#             with st.expander("📦 Imports & Variables Details", expanded=False):
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     if report["imports"]:
#                         st.subheader("📥 Imports")
#                         for imp in report["imports"]:
#                             st.code(imp, language="python")
#                     else:
#                         st.write("No imports found")
                
#                 with col2:
#                     if report["variables"]:
#                         st.subheader("📝 All Variables")
#                         variables_display = ", ".join(f"`{var}`" for var in report["variables"])
#                         st.write(variables_display)
#                     else:
#                         st.write("No variables detected")
            
#             # Download option
#             st.download_button(
#                 "💾 Download Full Report", 
#                 formatted_report, 
#                 "code_analysis_report.txt",
#                 mime="text/plain",
#                 key="code_download_btn"
#             )

# # Tab 3: AI Detection with reordered sections
# with tabs[2]:
#     st.header("🤖 AI Detection Matrix")
#     st.write("*Advanced pattern recognition for AI-generated content*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         ai_text = st.text_area(
#             "Content for Analysis", 
#             height=200, 
#             placeholder="Paste text or code to analyze for AI patterns...",
#             key="ai_text_input"
#         )
    
#     with col2:
#         ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
#         ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

#     if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
#         content = ""
        
#         if ai_file:
#             content = ai_file.read().decode("utf-8", errors="ignore")
#         elif ai_url.strip():
#             with st.spinner("Fetching content..."):
#                 content = fetch_from_url(ai_url.strip())
#         elif ai_text.strip():
#             content = ai_text

#         if not content:
#             st.warning("Please provide content for analysis.")
#         elif content.startswith("❌"):
#             st.error(content)
#         else:
#             with st.spinner("Analyzing patterns..."):
#                 result = detect_ai_generated_code(content)
            
#             st.success("🔍 Analysis Complete!")
            
#             # PRIORITY 1: MAIN ASSESSMENT (Most Important)
#             score_val = result['score']
#             if score_val < 45:
#                 color = "#00ff00"
#                 interpretation = "Human-like patterns detected"
#             elif score_val < 65:
#                 color = "#ffaa00"
#                 interpretation = "Mixed or uncertain patterns"
#             else:
#                 color = "#ff4444"
#                 interpretation = "AI-like patterns detected"
            
#             st.header(f"🎯 AI Detection Result: {result['label']}")
            
#             # Visual score indicator
#             col1, col2, col3 = st.columns([1, 2, 1])
#             with col2:
#                 st.metric(
#                     "AI Likelihood Score", 
#                     f"{score_val}%",
#                     delta=f"{score_val - 50:+.1f}% vs baseline",
#                     delta_color="inverse"
#                 )
                
#                 # Progress bar for visual representation
#                 st.markdown(f"""
#                 <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 5px; margin: 10px 0;">
#                     <div style="background: {color}; height: 20px; width: {score_val}%; border-radius: 8px; transition: all 0.3s;"></div>
#                 </div>
#                 <p style="text-align: center; color: {color}; font-weight: bold;">{interpretation}</p>
#                 """, unsafe_allow_html=True)
            
#             # PRIORITY 2: KEY INDICATORS
#             st.header("🔍 Key Indicators")
#             if result["reasons"]:
#                 for i, reason in enumerate(result["reasons"], 1):
#                     st.warning(f"{i}. {reason}")
#             else:
#                 st.success("✅ No significant AI patterns detected")
            
#             # PRIORITY 3: COPY FUNCTIONALITY
#             st.header("📋 Copy Detection Report")
#             detection_report = f"""
# AI DETECTION ANALYSIS REPORT
# ============================

# OVERALL ASSESSMENT: {result['label']}
# CONFIDENCE SCORE: {result['score']}%
# INTERPRETATION: {interpretation}

# KEY INDICATORS:
# {chr(10).join(f"- {reason}" for reason in result['reasons']) if result['reasons'] else "- No significant patterns detected"}

# DETAILED FEATURE ANALYSIS:
# {chr(10).join(f"- {k.replace('_', ' ').title()}: {v:.3f}" for k, v in result['features'].items())}

# CONFIDENCE BREAKDOWN:
# - Comment Pattern Score: {abs(result['features'].get('comment_density', 0) - 0.15) / 0.15:.2f}
# - Code Repetition Score: {result['features'].get('repeated_line_ratio', 0):.2f}
# - Generic Names Score: {result['features'].get('generic_name_density', 0):.2f}
# - Perfect Format Score: {result['features'].get('perfect_formatting', 0):.2f}
# """
#             copy_button(detection_report, "Copy Detection Report", key="ai_report")
            
#             # LOWER PRIORITY: DETAILED METRICS
#             st.header("📊 Detailed Feature Analysis")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 st.write("**📈 Pattern Metrics:**")
#                 for feature, value in result["features"].items():
#                     feature_name = feature.replace("_", " ").title()
                    
#                     # Color code based on feature values
#                     if "density" in feature or "ratio" in feature:
#                         if value > 0.3:
#                             color_indicator = "🔴"
#                         elif value > 0.15:
#                             color_indicator = "🟡"
#                         else:
#                             color_indicator = "🟢"
#                     else:
#                         color_indicator = "🔵"
                    
#                     st.write(f"{color_indicator} **{feature_name}:** `{value:.3f}`")
            
#             with col2:
#                 st.write("**🎯 Confidence Breakdown:**")
                
#                 # Create confidence indicators for each feature
#                 features = result["features"]
                
#                 if "comment_density" in features:
#                     cd_score = abs(features["comment_density"] - 0.15) / 0.15
#                     st.write(f"📝 Comment Pattern: `{cd_score:.2f}` {'⚠️' if cd_score > 0.5 else '✅'}")
                
#                 if "repeated_line_ratio" in features:
#                     rr_score = features["repeated_line_ratio"]
#                     st.write(f"🔄 Code Repetition: `{rr_score:.2f}` {'⚠️' if rr_score > 0.1 else '✅'}")
                
#                 if "generic_name_density" in features:
#                     gn_score = features["generic_name_density"]
#                     st.write(f"🏷️ Generic Names: `{gn_score:.2f}` {'⚠️' if gn_score > 0.03 else '✅'}")
                
#                 if "perfect_formatting" in features:
#                     pf_score = features["perfect_formatting"]
#                     st.write(f"✨ Perfect Format: `{pf_score:.2f}` {'⚠️' if pf_score > 0.5 else '✅'}")
            
#             # Download option
#             st.download_button(
#                 "💾 Download Analysis", 
#                 detection_report, 
#                 "ai_detection_report.txt",
#                 mime="text/plain",
#                 key="ai_download_btn"
#             )

# # Tab 4: URL Extractor with reordered sections
# with tabs[3]:
#     st.header("🌐 URL Data Extraction Engine")
#     st.write("*Advanced web content extraction and intelligent analysis*")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         url_input = st.text_input(
#             "🎯 Target URL", 
#             placeholder="Enter any URL for intelligent content extraction...",
#             key="url_input_field",
#             help="Supports web pages, GitHub files, documentation, articles, and more"
#         )
    
#     with col2:
#         url_length = st.slider("Summary Length", 1, 15, 7, key="url_summary_length")
#         url_bullets = st.checkbox("Use Bullet Points", value=True, key="url_use_bullets")
#         url_show_preview = st.checkbox("Show Content Preview", value=True, key="url_show_preview")

#     if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
#         if not url_input.strip():
#             st.warning("⚠️ Please enter a valid URL to proceed.")
#         else:
#             with st.spinner("🔄 Extracting content from URL..."):
#                 content = fetch_from_url(url_input.strip())
            
#             if content.startswith("❌"):
#                 st.error(content)
#             else:
#                 st.success("✅ Content extracted successfully!")
                
#                 # Generate enhanced summary
#                 with st.spinner("🧠 Generating intelligent summary..."):
#                     summary = summarize_text_advanced(content, url_length, url_bullets)
                
#                 # PRIORITY 1: SUMMARY (Most Important)
#                 st.header("🎯 Intelligent Content Summary")
#                 if url_bullets:
#                     st.markdown(summary)
#                 else:
#                     st.write(summary)
                
#                 # PRIORITY 2: COPY FUNCTIONALITY
#                 st.header("📋 Copy Summary")
#                 copy_button(summary, "Copy Summary", key="url_summary")
                
#                 # Enhanced metrics display (LOWER PRIORITY)
#                 words = content.split()
#                 sentences = len(re.findall(r'[.!?]+', content))
#                 paragraphs = len([p for p in content.split('\n\n') if p.strip()])
                
#                 # Reading time estimation
#                 avg_reading_speed = 200  # words per minute
#                 reading_time = max(1, len(words) // avg_reading_speed)
#                 st.info(f"📚 Estimated reading time: ~{reading_time} minute{'s' if reading_time != 1 else ''}")
                
#                 st.header("📊 Content Statistics")
#                 col1, col2, col3, col4, col5 = st.columns(5)
#                 with col1:
#                     st.metric("📄 Characters", f"{len(content):,}")
#                 with col2:
#                     st.metric("📝 Words", f"{len(words):,}")
#                 with col3:
#                     st.metric("📋 Lines", f"{len(content.splitlines()):,}")
#                 with col4:
#                     st.metric("📖 Sentences", f"{sentences:,}")
#                 with col5:
#                     st.metric("📑 Paragraphs", f"{paragraphs:,}")
                
#                 # Content preview with better formatting
#                 if url_show_preview:
#                     with st.expander("📄 Content Preview", expanded=False):
#                         preview_length = 3000
#                         preview = content[:preview_length]
#                         if len(content) > preview_length:
#                             preview += f"\n\n... [Content truncated - showing first {preview_length:,} characters of {len(content):,} total]"
                        
#                         # Try to detect if it's code
#                         if any(keyword in content.lower()[:500] for keyword in ['def ', 'class ', 'import ', 'function', '#include', 'public class']):
#                             st.code(preview, language="python" if "def " in preview or "import " in preview else "text")
#                         else:
#                             st.text(preview)
                
#                 # Additional analysis
#                 with st.expander("📊 Content Analysis", expanded=False):
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.write("**📈 Content Statistics:**")
#                         avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
#                         st.write(f"• Average word length: {avg_word_length:.1f} characters")
                        
#                         if sentences > 0:
#                             avg_sentence_length = len(words) / sentences
#                             st.write(f"• Average sentence length: {avg_sentence_length:.1f} words")
                        
#                         # Most common words (excluding stopwords)
#                         filtered_words = [word.lower().strip('.,!?";()[]') for word in words 
#                                         if len(word) > 3 and word.lower() not in STOPWORDS]
#                         if filtered_words:
#                             common_words = Counter(filtered_words).most_common(5)
#                             st.write("• Most frequent words:")
#                             for word, count in common_words:
#                                 st.write(f"  - **{word}**: {count} times")
                    
#                     with col2:
#                         st.write("**🔍 Content Characteristics:**")
                        
#                         # Detect content type
#                         if any(keyword in content.lower() for keyword in ['function', 'variable', 'method', 'class', 'algorithm']):
#                             st.write("• 💻 **Type**: Technical/Programming content")
#                         elif any(keyword in content.lower() for keyword in ['research', 'study', 'analysis', 'data', 'results']):
#                             st.write("• 🔬 **Type**: Research/Academic content")
#                         elif any(keyword in content.lower() for keyword in ['tutorial', 'how to', 'step', 'guide', 'instructions']):
#                             st.write("• 📚 **Type**: Educational/Tutorial content")
#                         else:
#                             st.write("• 📰 **Type**: General/Article content")
                        
#                         # Complexity estimate
#                         complex_words = [word for word in words if len(word) > 7]
#                         complexity = len(complex_words) / max(len(words), 1) * 100
                        
#                         if complexity > 20:
#                             st.write("• 🎓 **Complexity**: Advanced")
#                         elif complexity > 12:
#                             st.write("• 📖 **Complexity**: Intermediate")
#                         else:
#                             st.write("• 📝 **Complexity**: Beginner-friendly")
                        
#                         st.write(f"• 📊 **Complexity Score**: {complexity:.1f}%")
                
#                 # Enhanced copy and download options
#                 col4, col5, col6 = st.columns(3)
#                 with col4:
#                     copy_button(content, "Copy Full Content", key="url_full")
#                 with col5:
#                     st.download_button(
#                         "💾 Download Summary", 
#                         summary, 
#                         "url_summary.txt",
#                         mime="text/plain",
#                         key="url_download_summary"
#                     )
#                 with col6:
#                     # Create comprehensive report
#                     comprehensive_report = f"""
# URL EXTRACTION REPORT
# ====================

# SOURCE URL: {url_input}
# EXTRACTION DATE: Today

# CONTENT SUMMARY:
# {summary}

# CONTENT METRICS:
# - Characters: {len(content):,}
# - Words: {len(words):,}
# - Lines: {len(content.splitlines()):,}
# - Sentences: {sentences:,}
# - Paragraphs: {paragraphs:,}
# - Estimated Reading Time: ~{reading_time} minute(s)

# FULL EXTRACTED CONTENT:
# {content}
# """
#                     st.download_button(
#                         "💾 Download Full Report", 
#                         comprehensive_report, 
#                         f"url_analysis_report.txt",
#                         mime="text/plain",
#                         key="url_download_full"
#                     )

# # Enhanced Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; padding: 30px;">
#     <h3 style="color: rgba(0, 249, 255, 0.8); font-family: 'Orbitron', monospace;">🌌 TECHNOVA AI NEXUS v2.1</h3>
#     <p style="color: rgba(0, 249, 255, 0.6); font-family: monospace; margin: 10px 0;">
#         Advanced Neural Processing Suite • Quantum Code Analysis • AI Pattern Detection
#     </p>
#     <p style="color: rgba(0, 249, 255, 0.4); font-size: 0.9em;">
#         Priority-ordered analysis with reliable copy functionality
#     </p>
#     <div style="margin-top: 20px; color: rgba(0, 249, 255, 0.3);">
#         🚀 Built for developers, researchers, and AI enthusiasts
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Add session state management for better UX
# if 'analysis_history' not in st.session_state:
#     st.session_state['analysis_history'] = []

# # Optional: Add a sidebar with tips and shortcuts
# with st.sidebar:
#     st.header("⚡ Quick Tips")
#     st.write("""
#     **🔧 Code Analyzer:**
#     • Shows errors & warnings first
#     • Upload .py files for best results
#     • Supports GitHub raw URLs
#     • Detects 12+ code constructs
    
#     **🤖 AI Detection:**
#     • Assessment result shown first
#     • Analyzes patterns in code/text
#     • Uses multiple indicators
#     • Confidence scoring system
    
#     **🌐 URL Extractor:**
#     • Summary appears first
#     • Works with most websites
#     • Intelligent content filtering
#     • Automatic summarization
    
#     **📋 Copy Functionality:**
#     • Click copy button
#     • Text area appears below
#     • Select all text (Ctrl+A)
#     • Copy to clipboard (Ctrl+C)
#     """)
    
#     if st.button("🗑️ Clear All Data", key="clear_all"):
#         keys_to_remove = []
#         for key in st.session_state.keys():
#             if any(prefix in key for prefix in ['text_to_copy_', 'copied_text_', 'copy_btn_', 'copy_area_']):
#                 keys_to_remove.append(key)
        
#         for key in keys_to_remove:
#             del st.session_state[key]
        
#         st.success("All temporary data cleared!")
#         st.rerun()










import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import base64
import ast
from collections import Counter, defaultdict
import io
import json
import openai
from typing import Optional, Dict, List

# PDF extraction (optional)
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="Technova AI Nexus",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced copy function with proper JavaScript
def copy_button(text: str, label: str = "Copy", key: str = None):
    """Enhanced copy button using JavaScript"""
    if text is None:
        text = ""
    
    button_key = f"copy_btn_{key}" if key else f"copy_btn_{abs(hash(text[:50]))}"
    
    # Create a unique ID for this copy operation
    unique_id = f"copy_text_{button_key}"
    
    # HTML with JavaScript for copy functionality
    copy_html = f"""
    <div style="margin: 10px 0;">
        <button onclick="copyToClipboard_{unique_id}()" 
                style="background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3));
                       border: 1px solid rgba(0, 249, 255, 0.5);
                       color: #00f9ff;
                       padding: 8px 16px;
                       border-radius: 4px;
                       cursor: pointer;
                       font-weight: bold;">
            📋 {label}
        </button>
        <span id="copy_status_{unique_id}" style="margin-left: 10px; color: #00f9ff;"></span>
    </div>
    <textarea id="{unique_id}" readonly 
              style="width: 100%; height: 120px; 
                     background: rgba(0, 20, 40, 0.8);
                     border: 1px solid rgba(0, 249, 255, 0.3);
                     color: #00f9ff;
                     padding: 10px;
                     border-radius: 4px;">{text}</textarea>
    
    <script>
    function copyToClipboard_{unique_id}() {{
        const textArea = document.getElementById('{unique_id}');
        const statusSpan = document.getElementById('copy_status_{unique_id}');
        
        textArea.select();
        textArea.setSelectionRange(0, 99999);
        
        try {{
            document.execCommand('copy');
            statusSpan.innerHTML = '✅ Copied!';
            setTimeout(() => {{
                statusSpan.innerHTML = '';
            }}, 2000);
        }} catch (err) {{
            statusSpan.innerHTML = '❌ Copy failed - please select text manually';
        }}
    }}
    </script>
    """
    
    st.markdown(copy_html, unsafe_allow_html=True)

# Enhanced download function
def download_button_enhanced(content: str, filename: str, label: str, mime_type: str = "text/plain"):
    """Enhanced download button"""
    b64_content = base64.b64encode(content.encode()).decode()
    href = f'data:{mime_type};base64,{b64_content}'
    
    download_html = f"""
    <a href="{href}" download="{filename}"
       style="background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3));
              border: 1px solid rgba(0, 249, 255, 0.5);
              color: #00f9ff;
              padding: 8px 16px;
              text-decoration: none;
              border-radius: 4px;
              font-weight: bold;
              display: inline-block;">
        💾 {label}
    </a>
    """
    st.markdown(download_html, unsafe_allow_html=True)

# Simplified styling
def set_tech_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;500&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #00f9ff;
        font-family: 'Rajdhani', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', monospace !important;
        color: #00f9ff !important;
        text-shadow: 0 0 10px rgba(0, 249, 255, 0.5);
    }
    
    .main-title {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(45deg, #00f9ff, #0099cc, #66ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 2rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(0, 249, 255, 0.8);
        font-style: italic;
        margin-bottom: 2rem;
    }
    
    .stTextArea textarea, .stTextInput input {
        background: rgba(0, 20, 40, 0.8) !important;
        border: 1px solid rgba(0, 249, 255, 0.3) !important;
        color: #00f9ff !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
        border: 1px solid rgba(0, 249, 255, 0.5) !important;
        color: #00f9ff !important;
        font-weight: bold !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00f9ff !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stExpander {
        border: 1px solid rgba(0, 249, 255, 0.3);
        border-radius: 10px;
    }
    
    .api-warning {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid #ffc107;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize styling
set_tech_styling()

# API Configuration
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False

# Sidebar for API configuration
with st.sidebar:
    st.header("🔧 API Configuration")
    
    # OpenAI API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key for enhanced AI features",
        key="openai_api_key"
    )
    
    if api_key:
        try:
            openai.api_key = api_key
            st.session_state.api_configured = True
            st.success("API key configured!")
        except Exception as e:
            st.error("Invalid API key")
    else:
        st.session_state.api_configured = False
    
    st.markdown("---")
    st.markdown("**Features requiring API:**")
    st.markdown("• Advanced Code Correction")
    st.markdown("• Document Enhancement")
    st.markdown("• Style Transformation")

# API-based functions
def fix_code_with_ai(code: str, api_key: str) -> Dict:
    """Fix code using OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""You are a Python code correction expert. Fix the following Python code and provide a detailed explanation of what was fixed.

IMPORTANT: Return your response in valid JSON format with these exact fields:
- "success": boolean
- "fixed_code": string (the corrected code)
- "fixes_applied": list of strings (what was fixed)
- "explanation": string (detailed explanation)

Original code:
```python
{code}
```

Make sure the corrected code:
1. Has proper syntax and can be parsed by Python
2. Follows PEP 8 style guidelines
3. Has appropriate error handling where needed
4. Uses best practices

Return only valid JSON, no other text."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except json.JSONDecodeError:
        return {
            "success": False,
            "fixed_code": code,
            "fixes_applied": ["Failed to parse AI response"],
            "explanation": "The AI response was not in valid JSON format."
        }
    except Exception as e:
        return {
            "success": False,
            "fixed_code": code,
            "fixes_applied": [f"API Error: {str(e)}"],
            "explanation": f"Failed to connect to OpenAI API: {str(e)}"
        }

def enhance_document_with_ai(text: str, style: str, api_key: str) -> Dict:
    """Enhance document using OpenAI API"""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        style_prompts = {
            "grammar_only": "Fix grammar, spelling, and punctuation errors while maintaining the original tone and structure.",
            "professional": "Transform into professional, business-appropriate language while maintaining clarity and key information.",
            "formal_concise": "Make formal, concise, and academically appropriate while preserving essential content.",
            "persuasive": "Make persuasive and motivational while keeping facts accurate and adding compelling language.",
            "clear_simple": "Simplify language for clarity while maintaining all important information and meaning."
        }
        
        instruction = style_prompts.get(style, style_prompts["grammar_only"])
        
        prompt = f"""You are a professional document editor. {instruction}

IMPORTANT: Return your response in valid JSON format with these exact fields:
- "success": boolean
- "enhanced_text": string (the improved text)
- "changes_made": list of strings (what was changed)
- "improvement_summary": string (summary of improvements)

Original text:
{text}

Return only valid JSON, no other text."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except json.JSONDecodeError:
        return {
            "success": False,
            "enhanced_text": text,
            "changes_made": ["Failed to parse AI response"],
            "improvement_summary": "The AI response was not in valid JSON format."
        }
    except Exception as e:
        return {
            "success": False,
            "enhanced_text": text,
            "changes_made": [f"API Error: {str(e)}"],
            "improvement_summary": f"Failed to connect to OpenAI API: {str(e)}"
        }

# Main title
st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite v3.0</p>', unsafe_allow_html=True)

# Stopwords for summarization
STOPWORDS = set([
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into",
    "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then",
    "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from",
    "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than",
    "also", "can", "could", "should", "would", "may", "might", "have", "has", "had",
    "do", "does", "did", "done", "just", "over", "under", "more", "most", "other",
    "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom",
    "whose", "where", "when", "why", "how"
])

def safe_sentence_split(text: str):
    """Split text into sentences safely"""
    pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
    return [s.strip() for s in pattern.split(text) if s.strip()]

def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
    """Advanced text summarization using frequency analysis"""
    if not text or not text.strip():
        return "No content to summarize."
    
    paragraphs = [p.strip() for p in text.splitlines() if p.strip()]
    sentences = []
    for para in paragraphs:
        sentences.extend(safe_sentence_split(para))
    
    if not sentences:
        return text
    
    # Word frequency analysis
    word_freq = Counter()
    for s in sentences:
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
        for w in words:
            if w not in STOPWORDS and len(w) > 2:
                word_freq[w] += 1
    
    if not word_freq:
        return " ".join(sentences[:max_sentences])
    
    # Normalize frequencies
    max_freq = max(word_freq.values())
    for w in list(word_freq.keys()):
        word_freq[w] /= max_freq
    
    # Score sentences
    scored = []
    for idx, s in enumerate(sentences):
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9_']+", s)]
        score = sum(word_freq.get(w, 0.0) for w in words)
        length_penalty = 1.0 + 0.2 * max(0, (len(words) - 20) / 20)
        position_boost = 1.1 if idx < 3 else 1.0
        scored.append((score / length_penalty * position_boost, idx, s))
    
    # Select top sentences
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = sorted(scored[:max_sentences], key=lambda x: x[1])
    
    if as_bullets:
        return "\n".join([f"• {s}" for _, _, s in top])
    return " ".join([s for _, _, s in top])

def fix_python_code(code: str) -> dict:
    """Enhanced Python code fixer - handles most common syntax errors accurately"""
    if not code or not code.strip():
        return {
            "success": False,
            "original": code,
            "fixed": code,
            "fixes_applied": [],
            "remaining_errors": ["No code provided"]
        }
    
    original_code = code
    fixed_code = code
    fixes_applied = []
    remaining_errors = []
    
    # Check if already correct
    try:
        ast.parse(code)
        return {
            "success": True,
            "original": code,
            "fixed": code,
            "fixes_applied": ["✅ Code is already syntactically correct!"],
            "remaining_errors": []
        }
    except SyntaxError as e:
        remaining_errors.append(f"Initial error: {e.msg} at line {e.lineno}")
    
    # Multiple pass fixing
    max_attempts = 5
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        lines = fixed_code.splitlines()
        new_lines = []
        made_changes = False
        
        for i, line in enumerate(lines):
            original_line = line
            
            # 1. Fix missing colons (most common error)
            stripped = line.strip()
            colon_keywords = ['if ', 'elif ', 'else', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'finally', 'with ']
            
            if any(stripped.startswith(kw) for kw in colon_keywords):
                if not stripped.endswith(':') and ':' not in stripped.split('#')[0]:  # Ignore comments
                    # Handle special cases
                    if stripped == 'else' or stripped == 'try' or stripped == 'finally':
                        line = line.rstrip() + ':'
                        fixes_applied.append(f"Added colon after '{stripped}' at line {i+1}")
                        made_changes = True
                    elif not any(op in stripped for op in ['==', '!=', '>=', '<=', '<', '>']):  # Not comparison
                        line = line.rstrip() + ':'
                        fixes_applied.append(f"Added missing colon at line {i+1}")
                        made_changes = True
            
            # 2. Fix indentation issues
            if i > 0 and line.strip():
                prev_line = lines[i-1].strip()
                current_indent = len(line) - len(line.lstrip())
                
                # Should be indented after colon
                if prev_line.endswith(':') and current_indent == 0:
                    if any(prev_line.startswith(kw) for kw in colon_keywords):
                        line = '    ' + line
                        fixes_applied.append(f"Added indentation after colon at line {i+1}")
                        made_changes = True
                
                # Fix over-indentation
                elif current_indent > 0 and not prev_line.endswith(':'):
                    # Check if previous non-empty line needs this to be indented
                    needs_indent = False
                    for j in range(i-1, -1, -1):
                        if lines[j].strip():
                            if lines[j].strip().endswith(':'):
                                needs_indent = True
                            break
                    
                    if not needs_indent and current_indent == 4:
                        line = line[4:]  # Remove one level of indentation
                        fixes_applied.append(f"Fixed over-indentation at line {i+1}")
                        made_changes = True
            
            # 3. Fix print statements (Python 3 style)
            print_pattern = r'\bprint\s+([^(][^#]*?)(?:#.*)?$'
            match = re.search(print_pattern, line)
            if match:
                print_content = match.group(1).strip()
                if not print_content.startswith('('):
                    new_line = re.sub(print_pattern, f'print({print_content})', line)
                    if new_line != line:
                        line = new_line
                        fixes_applied.append(f"Fixed print statement syntax at line {i+1}")
                        made_changes = True
            
            # 4. Fix unclosed parentheses and brackets
            for char_pair in [('(', ')'), ('[', ']'), ('{', '}')]:
                open_char, close_char = char_pair
                open_count = line.count(open_char)
                close_count = line.count(close_char)
                
                if open_count > close_count:
                    diff = open_count - close_count
                    line = line.rstrip() + (close_char * diff)
                    fixes_applied.append(f"Added {diff} missing '{close_char}' at line {i+1}")
                    made_changes = True
            
            # 5. Fix unclosed quotes (improved logic)
            single_quotes = len([m for m in re.finditer(r"(?<!\\)'", line)])
            double_quotes = len([m for m in re.finditer(r'(?<!\\)"', line)])
            
            if single_quotes % 2 != 0 and double_quotes % 2 == 0:
                line = line.rstrip() + "'"
                fixes_applied.append(f"Added missing single quote at line {i+1}")
                made_changes = True
            elif double_quotes % 2 != 0 and single_quotes % 2 == 0:
                line = line.rstrip() + '"'
                fixes_applied.append(f"Added missing double quote at line {i+1}")
                made_changes = True
            
            new_lines.append(line)
        
        fixed_code = '\n'.join(new_lines)
        
        # Check if we fixed the syntax
        try:
            ast.parse(fixed_code)
            success = True
            break
        except SyntaxError as e:
            if not made_changes:
                remaining_errors.append(f"Could not fix: {e.msg} at line {e.lineno}")
                break
            remaining_errors = [f"Attempt {attempt}: {e.msg} at line {e.lineno}"]
    
    # Final validation
    try:
        ast.parse(fixed_code)
        success = True
        remaining_errors = []
    except SyntaxError as e:
        success = False
        remaining_errors.append(f"Final error: {e.msg} at line {e.lineno}")
    
    return {
        "success": success,
        "original": original_code,
        "fixed": fixed_code,
        "fixes_applied": fixes_applied if fixes_applied else ["❌ No automatic fixes could be applied"],
        "remaining_errors": remaining_errors
    }

def analyze_python_enhanced(code: str):
    """Comprehensive Python code analysis with enhanced metrics"""
    report = {
        "basic_stats": {},
        "functions": [],
        "classes": [],
        "imports": [],
        "variables": [],
        "purpose_summary": "",
        "errors": [],
        "warnings": [],
        "fixes": [],
        "complexity_metrics": {},
        "code_quality": {},
        "detailed_counts": {},
        "builtin_functions_used": []
    }
    
    if not code or not code.strip():
        return report
    
    lines = code.splitlines()
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
    comment_lines = [line for line in lines if line.strip().startswith("#")]
    blank_lines = [line for line in lines if not line.strip()]
    
    # Basic statistics
    report["basic_stats"] = {
        "total_lines": len(lines),
        "code_lines": len(code_lines),
        "comment_lines": len(comment_lines),
        "blank_lines": len(blank_lines),
        "characters": len(code),
        "words": len(code.split())
    }
    
    # Initialize counters
    def_count = len([line for line in code_lines if line.strip().startswith("def ")])
    class_count = len([line for line in code_lines if line.strip().startswith("class ")])
    import_count = len([line for line in code_lines if line.strip().startswith(("import ", "from "))])
    print_count = sum(len(re.findall(r'\bprint\s*\(', line)) for line in code_lines)
    if_count = sum(len(re.findall(r'\bif\b', line)) for line in code_lines)
    for_count = sum(len(re.findall(r'\bfor\b', line)) for line in code_lines)
    while_count = sum(len(re.findall(r'\bwhile\b', line)) for line in code_lines)
    try_count = sum(len(re.findall(r'\btry\b', line)) for line in code_lines)
    with_count = sum(len(re.findall(r'\bwith\b', line)) for line in code_lines)
    lambda_count = sum(len(re.findall(r'\blambda\b', line)) for line in code_lines)
    
    report["detailed_counts"] = {
        "functions": def_count,
        "classes": class_count,
        "imports": import_count,
        "print_statements": print_count,
        "if_statements": if_count,
        "for_loops": for_count,
        "while_loops": while_count,
        "try_blocks": try_count,
        "with_statements": with_count,
        "lambda_expressions": lambda_count
    }
    
    # Calculate complexity
    total_constructs = sum([if_count, for_count, while_count, try_count, def_count])
    complexity_score = total_constructs / max(1, len(code_lines)) * 100
    
    report["complexity_metrics"] = {
        "cyclomatic_complexity_estimate": total_constructs + 1,
        "complexity_per_line": round(complexity_score, 2)
    }
    
    # Code quality metrics
    comment_ratio = len(comment_lines) / max(1, len(lines)) * 100
    avg_line_length = sum(len(line) for line in code_lines) / max(1, len(code_lines))
    
    report["code_quality"] = {
        "comment_ratio": round(comment_ratio, 2),
        "avg_line_length": round(avg_line_length, 2)
    }
    
    # Extract function and class names
    for line in code_lines:
        stripped = line.strip()
        if stripped.startswith("def "):
            match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
            if match:
                report["functions"].append(match.group(1))
        elif stripped.startswith("class "):
            match = re.match(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
            if match:
                report["classes"].append(match.group(1))
        elif stripped.startswith(("import ", "from ")):
            report["imports"].append(stripped)
    
    # Generate purpose summary
    report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)
    
    return report

def detect_ai_generated_code(code: str) -> dict:
    """Detect if code might be AI-generated based on patterns"""
    if not code or not code.strip():
        return {"score": 0, "label": "No content", "reasons": [], "features": {}}
    
    lines = code.splitlines()
    code_lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    comment_lines = [ln for ln in lines if ln.strip().startswith("#")]
    
    features = {}
    total_lines = max(1, len(lines))
    
    # Comment density
    features["comment_density"] = len(comment_lines) / total_lines
    
    # Repeated lines
    normalized = [re.sub(r"\s+", " ", ln.strip()) for ln in code_lines]
    counts = Counter(normalized)
    repeated = sum(c for c in counts.values() if c > 1)
    features["repeated_line_ratio"] = repeated / max(1, len(code_lines))
    
    # Generic variable names
    generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res", "var", "obj"}
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
    generic_count = sum(1 for t in tokens if t in generic_names)
    features["generic_name_density"] = generic_count / max(1, len(tokens))
    
    # Perfect formatting
    perfect_indent = all(len(line) - len(line.lstrip()) % 4 == 0 for line in code_lines if line.strip())
    features["perfect_formatting"] = 1.0 if perfect_indent and len(code_lines) > 10 else 0.0
    
    # Calculate score
    score = (
        25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
        35 * features["repeated_line_ratio"] +
        20 * min(1.0, features["generic_name_density"] * 20) +
        20 * features["perfect_formatting"]
    )
    
    score = max(0.0, min(100.0, score))
    
    # Determine label
    if score >= 70:
        label = "Likely AI-generated"
    elif score >= 45:
        label = "Unclear/Mixed"
    else:
        label = "Likely human-written"
    
    # Generate reasons
    reasons = []
    if features["repeated_line_ratio"] > 0.1:
        reasons.append("High repetition of similar code patterns")
    if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
        reasons.append("Unusual comment density")
    if features["generic_name_density"] > 0.03:
        reasons.append("Frequent generic variable names")
    if features["perfect_formatting"] == 1.0:
        reasons.append("Suspiciously perfect code formatting")
    
    return {
        "score": round(score, 1),
        "label": label,
        "reasons": reasons,
        "features": features
    }

def fetch_from_url(url: str) -> str:
    """Fetch and extract text content from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, timeout=10, headers=headers)
        resp.raise_for_status()
        
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" in content_type:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
                element.extract()
            return soup.get_text(separator="\n", strip=True)
        else:
            return resp.text
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}"

def extract_pdf_text(file) -> str:
    """Extract text from PDF file"""
    if not PDF_AVAILABLE:
        return "PyPDF2 not available for PDF processing"
    
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

# Main application tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Text Analysis", 
    "🐍 Python Code Tools", 
    "🌐 Web Content", 
    "📄 Document Processing", 
    "🤖 AI Enhancement"
])

# Tab 1: Text Analysis
with tab1:
    st.header("📊 Advanced Text Analysis")
    
    text_input = st.text_area(
        "Enter text to analyze:",
        height=200,
        placeholder="Paste your text here for comprehensive analysis..."
    )
    
    if text_input:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Basic Statistics")
            words = len(text_input.split())
            chars = len(text_input)
            lines = len(text_input.splitlines())
            sentences = len(safe_sentence_split(text_input))
            
            st.metric("Words", words)
            st.metric("Characters", chars)
            st.metric("Lines", lines)
            st.metric("Sentences", sentences)
            
            # Word frequency analysis
            st.subheader("🔤 Top Words")
            words_list = re.findall(r'[A-Za-z]+', text_input.lower())
            filtered_words = [w for w in words_list if w not in STOPWORDS and len(w) > 2]
            word_freq = Counter(filtered_words)
            
            for word, freq in word_freq.most_common(10):
                st.write(f"**{word}**: {freq}")
        
        with col2:
            st.subheader("📝 Summary")
            summary = summarize_text_advanced(text_input, max_sentences=5)
            st.write(summary)
            
            st.subheader("🎯 Key Points")
            bullet_summary = summarize_text_advanced(text_input, max_sentences=5, as_bullets=True)
            st.markdown(bullet_summary)
        
        # Copy and download options
        st.subheader("💾 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            copy_button(summary, "Copy Summary", key="summary")
        
        with col2:
            download_button_enhanced(
                f"Text Analysis Report\n{'='*30}\n\nOriginal Text:\n{text_input}\n\nSummary:\n{summary}\n\nKey Points:\n{bullet_summary}",
                "text_analysis_report.txt",
                "Download Report"
            )

# Tab 2: Python Code Tools
with tab2:
    st.header("🐍 Python Code Analysis & Fixing")
    
    code_input = st.text_area(
        "Enter Python code:",
        height=300,
        placeholder="Paste your Python code here for analysis and fixing..."
    )
    
    if code_input:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Code Fixing")
            if st.button("Fix Code Syntax", type="primary"):
                with st.spinner("Analyzing and fixing code..."):
                    fix_result = fix_python_code(code_input)
                
                if fix_result["success"]:
                    st.success("✅ Code fixed successfully!")
                else:
                    st.error("❌ Some issues could not be automatically fixed")
                
                st.subheader("Fixed Code:")
                st.code(fix_result["fixed"], language="python")
                
                st.subheader("Fixes Applied:")
                for fix in fix_result["fixes_applied"]:
                    st.write(f"• {fix}")
                
                if fix_result["remaining_errors"]:
                    st.subheader("⚠️ Remaining Issues:")
                    for error in fix_result["remaining_errors"]:
                        st.write(f"• {error}")
                
                # Copy fixed code
                copy_button(fix_result["fixed"], "Copy Fixed Code", key="fixed_code")
        
        with col2:
            st.subheader("📊 Code Analysis")
            analysis = analyze_python_enhanced(code_input)
            
            # Basic stats
            stats = analysis["basic_stats"]
            st.metric("Total Lines", stats.get("total_lines", 0))
            st.metric("Code Lines", stats.get("code_lines", 0))
            st.metric("Functions", len(analysis["functions"]))
            st.metric("Classes", len(analysis["classes"]))
            
            # Detailed counts
            if analysis["detailed_counts"]:
                st.subheader("🔍 Code Structure")
                counts = analysis["detailed_counts"]
                for item, count in counts.items():
                    if count > 0:
                        st.write(f"**{item.replace('_', ' ').title()}**: {count}")
            
            # Functions and classes
            if analysis["functions"]:
                st.subheader("⚙️ Functions")
                st.write(", ".join(analysis["functions"]))
            
            if analysis["classes"]:
                st.subheader("🏗️ Classes")
                st.write(", ".join(analysis["classes"]))
        
        # AI-generated code detection
        st.subheader("🤖 AI Generation Detection")
        ai_result = detect_ai_generated_code(code_input)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("AI Score", f"{ai_result['score']}%")
        with col2:
            st.metric("Classification", ai_result['label'])
        with col3:
            confidence = "High" if ai_result['score'] > 70 or ai_result['score'] < 30 else "Medium"
            st.metric("Confidence", confidence)
        
        if ai_result['reasons']:
            st.write("**Detection Factors:**")
            for reason in ai_result['reasons']:
                st.write(f"• {reason}")

# Tab 3: Web Content
with tab3:
    st.header("🌐 Web Content Analysis")
    
    url_input = st.text_input(
        "Enter URL to analyze:",
        placeholder="https://example.com"
    )
    
    if url_input and st.button("Fetch & Analyze", type="primary"):
        with st.spinner("Fetching content from URL..."):
            content = fetch_from_url(url_input)
        
        if content and not content.startswith("Error"):
            st.success("✅ Content fetched successfully!")
            
            # Show content preview
            st.subheader("📄 Content Preview")
            st.text_area("Fetched Content", content[:1000] + "..." if len(content) > 1000 else content, height=200)
            
            # Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Statistics")
                words = len(content.split())
                chars = len(content)
                lines = len(content.splitlines())
                
                st.metric("Words", words)
                st.metric("Characters", chars)
                st.metric("Lines", lines)
            
            with col2:
                st.subheader("📝 Summary")
                summary = summarize_text_advanced(content, max_sentences=5)
                st.write(summary)
            
            # Export options
            st.subheader("💾 Export Options")
            col1, col2 = st.columns(2)
            
            with col1:
                copy_button(content, "Copy Full Content", key="web_content")
            
            with col2:
                download_button_enhanced(
                    f"Web Content Analysis\nURL: {url_input}\n{'='*50}\n\n{content}",
                    f"web_content_{url_input.split('/')[-1] or 'page'}.txt",
                    "Download Content"
                )
        else:
            st.error(f"Failed to fetch content: {content}")

# Tab 4: Document Processing
with tab4:
    st.header("📄 Document Processing")
    
    uploaded_file = st.file_uploader(
        "Upload a document",
        type=['txt', 'pdf', 'py', 'md'],
        help="Supported formats: TXT, PDF, Python, Markdown"
    )
    
    if uploaded_file is not None:
        file_type = uploaded_file.type
        file_name = uploaded_file.name
        
        st.success(f"✅ Uploaded: {file_name}")
        
        # Extract content based on file type
        try:
            if file_type == "application/pdf":
                content = extract_pdf_text(uploaded_file)
            else:
                content = str(uploaded_file.read(), "utf-8")
            
            # Show content preview
            st.subheader("📄 Content Preview")
            st.text_area("Document Content", content[:1000] + "..." if len(content) > 1000 else content, height=200)
            
            # Analysis based on file type
            if file_name.endswith('.py'):
                st.subheader("🐍 Python Code Analysis")
                analysis = analyze_python_enhanced(content)
                
                col1, col2 = st.columns(2)
                with col1:
                    stats = analysis["basic_stats"]
                    st.metric("Total Lines", stats.get("total_lines", 0))
                    st.metric("Code Lines", stats.get("code_lines", 0))
                    st.metric("Functions", len(analysis["functions"]))
                
                with col2:
                    if analysis["functions"]:
                        st.write("**Functions:**")
                        st.write(", ".join(analysis["functions"]))
                    
                    if analysis["classes"]:
                        st.write("**Classes:**")
                        st.write(", ".join(analysis["classes"]))
            
            else:
                st.subheader("📊 Text Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    words = len(content.split())
                    chars = len(content)
                    lines = len(content.splitlines())
                    
                    st.metric("Words", words)
                    st.metric("Characters", chars)
                    st.metric("Lines", lines)
                
                with col2:
                    summary = summarize_text_advanced(content, max_sentences=5)
                    st.write("**Summary:**")
                    st.write(summary)
            
            # Export options
            st.subheader("💾 Export Options")
            col1, col2 = st.columns(2)
            
            with col1:
                copy_button(content, "Copy Content", key="doc_content")
            
            with col2:
                download_button_enhanced(
                    content,
                    f"processed_{file_name}",
                    "Download Processed"
                )
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Tab 5: AI Enhancement
with tab5:
    st.header("🤖 AI-Powered Enhancement")
    
    if not st.session_state.api_configured:
        st.markdown("""
        <div class="api-warning">
            ⚠️ <strong>API Key Required</strong><br>
            Please enter your OpenAI API key in the sidebar to use AI enhancement features.
        </div>
        """, unsafe_allow_html=True)
    
    enhancement_type = st.selectbox(
        "Enhancement Type:",
        ["Code Fixing", "Document Enhancement"],
        help="Choose the type of AI enhancement you need"
    )
    
    if enhancement_type == "Code Fixing":
        st.subheader("🔧 AI Code Correction")
        code_to_fix = st.text_area(
            "Enter Python code to fix:",
            height=250,
            placeholder="Paste broken Python code here..."
        )
        
        if code_to_fix and st.button("Fix with AI", type="primary"):
            if st.session_state.api_configured:
                with st.spinner("AI is analyzing and fixing your code..."):
                    result = fix_code_with_ai(code_to_fix, st.session_state.get("openai_api_key"))
                
                if result["success"]:
                    st.success("✅ Code fixed by AI!")
                    
                    st.subheader("🔧 Fixed Code:")
                    st.code(result["fixed_code"], language="python")
                    
                    st.subheader("📋 Fixes Applied:")
                    for fix in result["fixes_applied"]:
                        st.write(f"• {fix}")
                    
                    st.subheader("💬 AI Explanation:")
                    st.write(result["explanation"])
                    
                    copy_button(result["fixed_code"], "Copy Fixed Code", key="ai_fixed")
                    
                else:
                    st.error("❌ AI couldn't fix the code")
                    for fix in result["fixes_applied"]:
                        st.write(f"• {fix}")
            else:
                st.warning("Please configure your OpenAI API key in the sidebar first.")
    
    else:  # Document Enhancement
        st.subheader("📝 AI Document Enhancement")
        
        enhancement_style = st.selectbox(
            "Enhancement Style:",
            [
                ("grammar_only", "Grammar & Spelling Only"),
                ("professional", "Professional Tone"),
                ("formal_concise", "Formal & Concise"),
                ("persuasive", "Persuasive & Engaging"),
                ("clear_simple", "Clear & Simple")
            ],
            format_func=lambda x: x[1]
        )
        
        doc_to_enhance = st.text_area(
            "Enter text to enhance:",
            height=250,
            placeholder="Paste your document text here..."
        )
        
        if doc_to_enhance and st.button("Enhance with AI", type="primary"):
            if st.session_state.api_configured:
                with st.spinner("AI is enhancing your document..."):
                    result = enhance_document_with_ai(
                        doc_to_enhance, 
                        enhancement_style[0], 
                        st.session_state.get("openai_api_key")
                    )
                
                if result["success"]:
                    st.success("✅ Document enhanced by AI!")
                    
                    st.subheader("📄 Enhanced Text:")
                    st.write(result["enhanced_text"])
                    
                    st.subheader("📋 Changes Made:")
                    for change in result["changes_made"]:
                        st.write(f"• {change}")
                    
                    st.subheader("📊 Improvement Summary:")
                    st.write(result["improvement_summary"])
                    
                    copy_button(result["enhanced_text"], "Copy Enhanced Text", key="ai_enhanced")
                    
                else:
                    st.error("❌ AI couldn't enhance the document")
                    for change in result["changes_made"]:
                        st.write(f"• {change}")
            else:
                st.warning("Please configure your OpenAI API key in the sidebar first.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(0, 249, 255, 0.6); font-style: italic;">
    🌌 Technova AI Nexus v3.0 | Advanced AI-Powered Analysis Suite<br>
    Built with Streamlit & Enhanced with OpenAI Integration
</div>
""", unsafe_allow_html=True)
