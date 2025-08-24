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










import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import base64
import ast
from collections import Counter
import io

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

# Enhanced copy button
def copy_button(text: str, label: str = "Copy", key: str = None):
    """Enhanced copy button with styling"""
    if text is None:
        text = ""
    safe_b64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    el_id = f"copy-btn-{key}" if key else f"copy-btn-{abs(hash(text))}"
    
    html = f"""
    <button id="{el_id}" onclick="navigator.clipboard.writeText(atob('{safe_b64}'))"
        style="
            background: linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2));
            border: 1px solid rgba(0, 249, 255, 0.4);
            color: #00f9ff;
            padding: 8px 16px;
            border-radius: 8px;
            font-family: monospace;
            font-weight: bold;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s ease;
        "
        onmouseover="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3))'"
        onmouseout="this.style.background='linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))'">
        ⚡ {label}
    </button>
    <script>
    document.getElementById('{el_id}').addEventListener('click', function() {{
        const btn = this;
        const oldText = btn.innerHTML;
        btn.innerHTML = '✅ Copied!';
        btn.style.background = 'linear-gradient(135deg, rgba(0, 255, 0, 0.2), rgba(0, 200, 0, 0.3))';
        setTimeout(() => {{
            btn.innerHTML = oldText;
            btn.style.background = 'linear-gradient(135deg, rgba(0, 249, 255, 0.1), rgba(0, 153, 204, 0.2))';
        }}, 1500);
    }});
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)

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
    </style>
    """, unsafe_allow_html=True)

# Initialize styling
set_tech_styling()

# Main title
st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced AI-Powered Analysis Suite</p>', unsafe_allow_html=True)

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

def analyze_python(code: str):
    """Comprehensive Python code analysis"""
    report = {
        "functions": [], 
        "classes": [], 
        "imports": [], 
        "purpose_summary": "", 
        "errors": [], 
        "warnings": [], 
        "fixes": []
    }

    # Basic parsing
    for line in code.splitlines():
        l = line.strip()
        if l.startswith("def "):
            func_name = l.split("(")[0][4:].strip()
            report["functions"].append(func_name)
        elif l.startswith("class "):
            class_name = l.split("(")[0][6:].strip().rstrip(":")
            report["classes"].append(class_name)
        elif l.startswith("import ") or l.startswith("from "):
            report["imports"].append(l)

    # Generate purpose summary
    report["purpose_summary"] = summarize_text_advanced(code, max_sentences=3)

    # AST analysis for deeper insights
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        report["errors"].append(f"SyntaxError: {e.msg} at line {e.lineno}")
        report["fixes"].append("Check syntax: indentation, colons, parentheses, quotes.")
        return report

    # Analyze AST
    imported_names = set()
    used_names = set()
    assigned_names = set()

    class CodeAnalyzer(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name.split(".")[0])
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            for alias in node.names:
                imported_names.add(alias.asname or alias.name)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            assigned_names.add(node.name)
            # Check for mutable default arguments
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    report["warnings"].append(f"Mutable default argument in '{node.name}'")
                    report["fixes"].append(f"Use None as default in '{node.name}' and create objects inside function")
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            assigned_names.add(node.name)
            self.generic_visit(node)

        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
            elif isinstance(node.ctx, ast.Store):
                assigned_names.add(node.id)
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                report["warnings"].append(f"Dangerous {node.func.id} usage detected")
                report["fixes"].append(f"Avoid {node.func.id}; use safer alternatives")
            self.generic_visit(node)

    CodeAnalyzer().visit(tree)

    # Check for unused imports
    for name in sorted(imported_names):
        if name not in used_names and name not in {"__future__"}:
            report["warnings"].append(f"Possibly unused import: '{name}'")
            report["fixes"].append(f"Remove unused import '{name}'")

    # Check for builtin shadowing
    builtins_list = [
        'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir', 'enumerate', 
        'filter', 'float', 'format', 'frozenset', 'hash', 'hex', 'id', 'input', 
        'int', 'isinstance', 'len', 'list', 'map', 'max', 'min', 'next', 'oct', 
        'open', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round', 
        'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
    ]
    
    for name in assigned_names:
        if name in builtins_list:
            report["warnings"].append(f"Variable '{name}' shadows builtin")
            report["fixes"].append(f"Rename '{name}' to avoid shadowing builtins")

    # Add general recommendations
    if not report["errors"]:
        if not report["warnings"]:
            report["fixes"].append("Code looks good! Consider adding tests and documentation.")
        else:
            report["fixes"].append("Review warnings above and apply suggested fixes.")

    return report

def detect_ai_generated_code(code: str) -> dict:
    """Detect if code might be AI-generated based on patterns"""
    if not code or not code.strip():
        return {"score": 0, "label": "❓ No content", "reasons": [], "features": {}}
    
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
    generic_names = {"data", "result", "temp", "value", "item", "input", "output", "res"}
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", code)
    generic_count = sum(1 for t in tokens if t in generic_names)
    features["generic_name_density"] = generic_count / max(1, len(tokens))
    
    # Calculate score
    score = (
        25 * min(1.0, abs(features["comment_density"] - 0.15) / 0.15) +
        35 * features["repeated_line_ratio"] +
        20 * min(1.0, features["generic_name_density"] * 20) +
        20 * (1.0 if len(code_lines) > 50 and features["comment_density"] < 0.05 else 0.0)
    )
    
    score = max(0.0, min(100.0, score))
    
    # Determine label
    if score >= 70:
        label = "🚨 Likely AI-generated"
    elif score >= 45:
        label = "🤔 Unclear/Mixed"
    else:
        label = "✅ Likely human-written"
    
    # Generate reasons
    reasons = []
    if features["repeated_line_ratio"] > 0.1:
        reasons.append("High repetition of similar code patterns")
    if features["comment_density"] < 0.02 or features["comment_density"] > 0.4:
        reasons.append("Unusual comment density")
    if features["generic_name_density"] > 0.03:
        reasons.append("Frequent generic variable names")
    
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
        return f"❌ Error fetching URL: {str(e)}"
    except Exception as e:
        return f"❌ Error processing content: {str(e)}"

# Create tabs
tabs = st.tabs([
    "📄 Document Processor", 
    "🧠 Code Analyzer", 
    "🤖 AI Detection", 
    "🌐 URL Extractor"
])

# Tab 1: Document Processor
with tabs[0]:
    st.header("📄 Neural Document Processor")
    st.write("*Advanced text analysis and summarization*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        doc_text = st.text_area(
            "Input Text", 
            height=200, 
            placeholder="Paste your document content here...",
            key="doc_text_input"
        )
    
    with col2:
        doc_file = st.file_uploader("Upload Document", type=["txt", "md", "pdf"], key="doc_file_upload")
        doc_url = st.text_input("Document URL", placeholder="https://...", key="doc_url_input")
        doc_length = st.slider("Summary Length", 1, 10, 5, key="doc_summary_length")
        doc_bullets = st.checkbox("Use Bullets", value=False, key="doc_use_bullets")

    if st.button("🚀 Analyze Document", type="primary", key="doc_analyze_btn"):
        content = ""
        
        # Get content from various sources
        if doc_file:
            if doc_file.name.lower().endswith(".pdf"):
                if not PDF_AVAILABLE:
                    st.error("PDF processing requires PyPDF2. Install with: pip install PyPDF2")
                else:
                    try:
                        reader = PyPDF2.PdfReader(io.BytesIO(doc_file.read()))
                        pages_text = []
                        for page in reader.pages:
                            pages_text.append(page.extract_text() or "")
                        content = "\n".join(pages_text)
                    except Exception as e:
                        st.error(f"PDF error: {e}")
            else:
                content = doc_file.read().decode("utf-8", errors="ignore")
        elif doc_url.strip():
            with st.spinner("Fetching content..."):
                content = fetch_from_url(doc_url.strip())
        elif doc_text.strip():
            content = doc_text

        if not content:
            st.warning("Please provide content via text, file, or URL.")
        elif content.startswith("❌"):
            st.error(content)
        else:
            with st.spinner("Processing..."):
                summary = summarize_text_advanced(content, doc_length, doc_bullets)
            
            st.success("Analysis Complete!")
            
            with st.expander("📊 Results", expanded=True):
                st.subheader("Summary")
                if doc_bullets:
                    st.markdown(summary)
                else:
                    st.write(summary)
                
                col1, col2 = st.columns(2)
                with col1:
                    copy_button(summary, "Copy Summary", key="doc_copy_btn")
                with col2:
                    st.download_button(
                        "💾 Download", 
                        summary.encode("utf-8"), 
                        "summary.txt",
                        key="doc_download_btn"
                    )

# Tab 2: Code Analyzer
with tabs[1]:
    st.header("🧠 Quantum Code Analyzer")
    st.write("*Deep code analysis and optimization recommendations*")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        code_text = st.text_area(
            "Python Code", 
            height=250, 
            placeholder="Paste your Python code here...",
            key="code_text_input"
        )
    
    with col2:
        code_file = st.file_uploader("Upload Python File", type=["py"], key="code_file_upload")
        code_url = st.text_input("Code URL", placeholder="https://...", key="code_url_input")

    if st.button("🔍 Analyze Code", type="primary", key="code_analyze_btn"):
        code_content = ""
        
        if code_file:
            code_content = code_file.read().decode("utf-8", errors="ignore")
        elif code_url.strip():
            with st.spinner("Fetching code..."):
                code_content = fetch_from_url(code_url.strip())
        elif code_text.strip():
            code_content = code_text

        if not code_content:
            st.warning("Please provide code via input, file, or URL.")
        elif code_content.startswith("❌"):
            st.error(code_content)
        else:
            with st.expander("Code Preview", expanded=False):
                st.code(code_content, language="python")

            with st.spinner("Analyzing..."):
                report = analyze_python(code_content)

            st.success("Analysis Complete!")

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Summary")
                st.write(report["purpose_summary"])
                
                st.subheader("❌ Errors")
                if report["errors"]:
                    for error in report["errors"]:
                        st.error(error)
                else:
                    st.success("No syntax errors found!")
            
            with col2:
                st.subheader("⚠️ Warnings")
                if report["warnings"]:
                    for warning in report["warnings"]:
                        st.warning(warning)
                else:
                    st.success("No warnings!")
                
                st.subheader("💡 Recommendations")
                for fix in report["fixes"]:
                    st.info(fix)
            
            # Copy and download options
            col3, col4 = st.columns(2)
            with col3:
                copy_button(str(report), "Copy Report", key="code_copy_btn")
            with col4:
                st.download_button(
                    "💾 Download Report", 
                    str(report).encode("utf-8"), 
                    "code_analysis.txt",
                    key="code_download_btn"
                )

# Tab 3: AI Detection
with tabs[2]:
    st.header("🤖 AI Detection Matrix")
    st.write("*Pattern recognition for AI-generated content*")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ai_text = st.text_area(
            "Content for Analysis", 
            height=200, 
            placeholder="Paste text or code to analyze...",
            key="ai_text_input"
        )
    
    with col2:
        ai_file = st.file_uploader("Upload File", type=["txt", "py", "md"], key="ai_file_upload")
        ai_url = st.text_input("Content URL", placeholder="https://...", key="ai_url_input")

    if st.button("🔬 Scan for AI Patterns", type="primary", key="ai_analyze_btn"):
        content = ""
        
        if ai_file:
            content = ai_file.read().decode("utf-8", errors="ignore")
        elif ai_url.strip():
            with st.spinner("Fetching content..."):
                content = fetch_from_url(ai_url.strip())
        elif ai_text.strip():
            content = ai_text

        if not content:
            st.warning("Please provide content for analysis.")
        elif content.startswith("❌"):
            st.error(content)
        else:
            with st.spinner("Analyzing patterns..."):
                result = detect_ai_generated_code(content)
            
            st.success("Analysis Complete!")
            
            # Display results
            score_color = "🟢" if result['score'] < 45 else "🟡" if result['score'] < 65 else "🔴"
            
            with st.expander(f"{score_color} Detection Results", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col2:
                    st.metric(
                        "AI Likelihood Score", 
                        f"{result['score']}%",
                        delta=f"{result['score'] - 50}% vs baseline"
                    )
                
                st.markdown(f"**Assessment:** {result['label']}")
                
                if result["reasons"]:
                    st.subheader("🔍 Key Indicators")
                    for reason in result["reasons"]:
                        st.write(f"• {reason}")
                else:
                    st.success("No significant AI patterns detected")
                
                st.subheader("📊 Feature Analysis")
                for feature, value in result["features"].items():
                    feature_name = feature.replace("_", " ").title()
                    st.write(f"• {feature_name}: `{value:.3f}`")
                
                # Copy and download
                col4, col5 = st.columns(2)
                with col4:
                    copy_button(str(result), "Copy Results", key="ai_copy_btn")
                with col5:
                    st.download_button(
                        "💾 Download Analysis", 
                        str(result).encode("utf-8"), 
                        "ai_detection.txt",
                        key="ai_download_btn"
                    )

# Tab 4: URL Extractor
with tabs[3]:
    st.header("🌐 URL Data Extraction Engine")
    st.write("*Advanced web content extraction and analysis*")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url_input = st.text_input(
            "Target URL", 
            placeholder="Enter any URL for content extraction...",
            key="url_input_field"
        )
    
    with col2:
        url_length = st.slider("Summary Length", 1, 10, 5, key="url_summary_length")
        url_bullets = st.checkbox("Use Bullets", value=True, key="url_use_bullets")

    if st.button("🚀 Extract & Analyze", type="primary", key="url_analyze_btn"):
        if not url_input.strip():
            st.warning("Please enter a valid URL.")
        else:
            with st.spinner("Extracting content..."):
                content = fetch_from_url(url_input.strip())
            
            if content.startswith("❌"):
                st.error(content)
            else:
                st.success("Content extracted successfully!")
                
                # Show metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Characters", f"{len(content):,}")
                with col2:
                    st.metric("Words", f"{len(content.split()):,}")
                with col3:
                    st.metric("Lines", f"{len(content.splitlines()):,}")
                
                # Show preview
                with st.expander("📄 Content Preview", expanded=False):
                    preview = content[:2000] + "..." if len(content) > 2000 else content
                    st.text(preview)
                
                # Generate summary
                with st.spinner("Generating summary..."):
                    summary = summarize_text_advanced(content, url_length, url_bullets)
                
                st.subheader("📊 Content Summary")
                if url_bullets:
                    st.markdown(summary)
                else:
                    st.write(summary)
                
                # Copy and download
                col4, col5 = st.columns(2)
                with col4:
                    copy_button(summary, "Copy Summary", key="url_copy_btn")
                with col5:
                    st.download_button(
                        "💾 Download Summary", 
                        summary.encode("utf-8"), 
                        "url_summary.txt",
                        key="url_download_btn"
                    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: rgba(0, 249, 255, 0.6); font-family: monospace;">
    🌌 TECHNOVA AI NEXUS v2.0 • Advanced Neural Processing Suite
</div>
""", unsafe_allow_html=True)

