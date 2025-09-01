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
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import re
import base64
import ast
from collections import Counter, defaultdict
import io
import json
import hashlib
import random
import string
from datetime import datetime, timedelta
import os
from typing import Optional, Dict, List, Tuple

# Page config
st.set_page_config(
    page_title="TechNova AI Nexus",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# In-memory database simulation (replacing SQLite for Streamlit compatibility)
class InMemoryDB:
    def __init__(self):
        if 'db_users' not in st.session_state:
            st.session_state.db_users = {}
        if 'db_usage' not in st.session_state:
            st.session_state.db_usage = defaultdict(lambda: defaultdict(int))
    
    def create_user(self, username: str, password_hash: str) -> bool:
        if username in st.session_state.db_users:
            return False
        
        st.session_state.db_users[username] = {
            'password_hash': password_hash,
            'created_at': datetime.now(),
            'subscription_type': 'free',
            'subscription_expires': datetime.now() + timedelta(days=14),
            'id': len(st.session_state.db_users) + 1
        }
        return True
    
    def get_user(self, username: str) -> Optional[Dict]:
        return st.session_state.db_users.get(username)
    
    def log_usage(self, username: str, tab_name: str):
        today = datetime.now().date()
        key = f"{username}_{tab_name}_{today}"
        st.session_state.db_usage[key] += 1
    
    def get_usage_count(self, username: str, tab_name: str) -> int:
        today = datetime.now().date()
        key = f"{username}_{tab_name}_{today}"
        return st.session_state.db_usage.get(key, 0)

# Initialize database
db = InMemoryDB()

# Authentication Functions
class AuthManager:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    @staticmethod
    def create_user(username: str, password: str) -> Tuple[bool, str]:
        """Create a new user account"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        try:
            password_hash = AuthManager.hash_password(password)
            
            if db.create_user(username, password_hash):
                return True, "Account created successfully! You have a 14-day free trial."
            else:
                return False, "Username already exists."
                
        except Exception as e:
            return False, f"Error creating account: {str(e)}"
    
    @staticmethod
    def login_user(username: str, password: str) -> Tuple[bool, str, Dict]:
        """Login user and return user info"""
        try:
            user = db.get_user(username)
            if not user:
                return False, "Invalid username or password.", {}
            
            if not AuthManager.verify_password(password, user['password_hash']):
                return False, "Invalid username or password.", {}
            
            # Check subscription status
            sub_type = user['subscription_type']
            if user['subscription_expires'] and datetime.now() > user['subscription_expires']:
                sub_type = 'expired'
            
            user_info = {
                'id': user['id'],
                'username': username,
                'subscription_type': sub_type,
                'subscription_expires': user['subscription_expires']
            }
            
            return True, "Login successful!", user_info
            
        except Exception as e:
            return False, f"Login error: {str(e)}", {}

# Usage Management
class UsageManager:
    @staticmethod
    def can_use_tab(username: str, tab_name: str) -> Tuple[bool, str]:
        """Check if user can use a specific tab"""
        try:
            user = db.get_user(username)
            if not user:
                return False, "User not found."
            
            sub_type = user['subscription_type']
            
            # Check if subscription expired
            if user['subscription_expires'] and datetime.now() > user['subscription_expires']:
                sub_type = 'expired'
            
            # If TechNova Plus, allow unlimited usage
            if sub_type == 'plus':
                return True, ""
            
            # If expired, deny access
            if sub_type == 'expired':
                return False, "Your free trial has expired. Please upgrade to TechNova Plus."
            
            # Check daily usage for free users
            usage_count = db.get_usage_count(username, tab_name)
            
            if usage_count >= 4:
                return False, f"Daily limit reached for {tab_name}. You have used 4/4 attempts today."
            
            return True, ""
            
        except Exception as e:
            return False, f"Error checking usage: {str(e)}"
    
    @staticmethod
    def log_usage(username: str, tab_name: str):
        """Log tab usage for a user"""
        try:
            db.log_usage(username, tab_name)
        except Exception as e:
            st.error(f"Error logging usage: {str(e)}")
    
    @staticmethod
    def get_usage_stats(username: str) -> Dict[str, int]:
        """Get usage statistics for a user"""
        try:
            stats = {}
            tabs = ["Text Summarizer", "Web Scraper", "Python Analyzer", "AI Chat", "Document Enhancer"]
            for tab in tabs:
                stats[tab] = db.get_usage_count(username, tab)
            return stats
        except Exception:
            return {}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Enhanced Styling
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
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .auth-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 2rem;
        border: 2px solid rgba(0, 249, 255, 0.3);
        border-radius: 15px;
        background: rgba(0, 20, 40, 0.7);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 249, 255, 0.1);
    }
    
    .feature-card {
        background: rgba(0, 20, 40, 0.6);
        border: 1px solid rgba(0, 249, 255, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(0, 249, 255, 0.6);
        box-shadow: 0 4px 20px rgba(0, 249, 255, 0.2);
    }
    
    .usage-warning {
        background: rgba(255, 193, 7, 0.1);
        border: 2px solid #ffc107;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .subscription-info {
        background: rgba(0, 249, 255, 0.1);
        border: 2px solid rgba(0, 249, 255, 0.3);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .metric-card {
        background: rgba(0, 20, 40, 0.8);
        border: 1px solid rgba(0, 249, 255, 0.3);
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stTextArea textarea, .stTextInput input {
        background: rgba(0, 20, 40, 0.8) !important;
        border: 2px solid rgba(0, 249, 255, 0.3) !important;
        color: #00f9ff !important;
        border-radius: 8px !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: rgba(0, 249, 255, 0.6) !important;
        box-shadow: 0 0 10px rgba(0, 249, 255, 0.3) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3)) !important;
        border: 2px solid rgba(0, 249, 255, 0.5) !important;
        color: #00f9ff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 249, 255, 0.3), rgba(0, 153, 204, 0.4)) !important;
        border-color: rgba(0, 249, 255, 0.8) !important;
        box-shadow: 0 4px 15px rgba(0, 249, 255, 0.3) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(0, 20, 40, 0.8) !important;
        border: 2px solid rgba(0, 249, 255, 0.3) !important;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: #00ff00; }
    .status-warning { background-color: #ffc107; }
    .status-offline { background-color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

set_tech_styling()

# Enhanced copy button function
def copy_button(text: str, label: str = "Copy", key: str = None):
    """Enhanced copy button with better error handling"""
    if text is None:
        text = ""
    
    # Escape HTML characters properly
    import html
    escaped_text = html.escape(str(text))
    button_key = f"copy_btn_{key}" if key else f"copy_btn_{abs(hash(str(text)[:50]))}"
    
    copy_html = f"""
    <div style="margin: 15px 0;">
        <button onclick="copyToClipboard_{button_key}()" 
                style="background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3));
                       border: 2px solid rgba(0, 249, 255, 0.5);
                       color: #00f9ff;
                       padding: 10px 20px;
                       border-radius: 8px;
                       cursor: pointer;
                       font-weight: bold;
                       transition: all 0.3s ease;">
            📋 {label}
        </button>
        <span id="copy_status_{button_key}" style="margin-left: 15px; color: #00f9ff; font-weight: bold;"></span>
    </div>
    <textarea id="copy_text_{button_key}" readonly 
              style="width: 100%; height: 150px; 
                     background: rgba(0, 20, 40, 0.9);
                     border: 2px solid rgba(0, 249, 255, 0.3);
                     color: #00f9ff;
                     padding: 15px;
                     border-radius: 8px;
                     font-family: 'Rajdhani', monospace;
                     resize: vertical;">{escaped_text}</textarea>
    
    <script>
    function copyToClipboard_{button_key}() {{
        const textArea = document.getElementById('copy_text_{button_key}');
        const statusSpan = document.getElementById('copy_status_{button_key}');
        
        if (navigator.clipboard && window.isSecureContext) {{
            navigator.clipboard.writeText(textArea.value).then(() => {{
                statusSpan.innerHTML = '✅ Copied successfully!';
                setTimeout(() => {{
                    statusSpan.innerHTML = '';
                }}, 3000);
            }}).catch(() => {{
                fallbackCopy();
            }});
        }} else {{
            fallbackCopy();
        }}
        
        function fallbackCopy() {{
            textArea.select();
            textArea.setSelectionRange(0, 99999);
            try {{
                document.execCommand('copy');
                statusSpan.innerHTML = '✅ Copied successfully!';
                setTimeout(() => {{
                    statusSpan.innerHTML = '';
                }}, 3000);
            }} catch (err) {{
                statusSpan.innerHTML = '❌ Copy failed - please select text manually';
                setTimeout(() => {{
                    statusSpan.innerHTML = '';
                }}, 5000);
            }}
        }}
    }}
    </script>
    """
    
    components.html(copy_html, height=220)

# Enhanced download function
def download_button_enhanced(content: str, filename: str, label: str, mime_type: str = "text/plain"):
    """Enhanced download button"""
    try:
        b64_content = base64.b64encode(str(content).encode()).decode()
        href = f'data:{mime_type};base64,{b64_content}'
        
        download_html = f"""
        <a href="{href}" download="{filename}"
           style="background: linear-gradient(135deg, rgba(0, 249, 255, 0.2), rgba(0, 153, 204, 0.3));
                  border: 2px solid rgba(0, 249, 255, 0.5);
                  color: #00f9ff;
                  padding: 10px 20px;
                  text-decoration: none;
                  border-radius: 8px;
                  font-weight: bold;
                  display: inline-block;
                  transition: all 0.3s ease;
                  font-family: 'Rajdhani', sans-serif;">
            💾 {label}
        </a>
        """
        components.html(download_html, height=60)
    except Exception as e:
        st.error(f"Error creating download: {str(e)}")

# Enhanced stopwords and analysis functions
STOPWORDS = set([
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into",
    "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then",
    "there", "these", "they", "this", "to", "was", "will", "with", "you", "your", "from",
    "our", "we", "he", "she", "his", "her", "its", "were", "been", "being", "than",
    "also", "can", "could", "should", "would", "may", "might", "have", "has", "had",
    "do", "does", "did", "done", "just", "over", "under", "more", "most", "other",
    "some", "any", "each", "many", "few", "those", "them", "which", "who", "whom",
    "whose", "where", "when", "why", "how", "about", "up", "out", "so", "what"
])

def safe_sentence_split(text: str) -> List[str]:
    """Split text into sentences safely"""
    try:
        # Enhanced sentence splitting pattern
        pattern = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences = pattern.split(str(text))
        return [s.strip() for s in sentences if s.strip()]
    except Exception:
        return [str(text)]

def analyze_text_metrics(text: str) -> Dict:
    """Comprehensive text analysis"""
    try:
        if not text:
            return {}
        
        text = str(text)
        
        # Basic metrics
        char_count = len(text)
        word_count = len(re.findall(r'\b\w+\b', text))
        line_count = len(text.splitlines())
        sentences = safe_sentence_split(text)
        sentence_count = len(sentences)
        
        # Word frequency analysis
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
        word_freq = Counter(filtered_words)
        
        # Reading metrics
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        avg_chars_per_word = char_count / word_count if word_count > 0 else 0
        
        return {
            'characters': char_count,
            'words': word_count,
            'lines': line_count,
            'sentences': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'avg_chars_per_word': round(avg_chars_per_word, 1),
            'top_words': word_freq.most_common(10),
            'unique_words': len(set(filtered_words)),
            'word_diversity': len(set(filtered_words)) / len(filtered_words) if filtered_words else 0
        }
    except Exception as e:
        st.error(f"Error analyzing text: {str(e)}")
        return {}

def summarize_text_advanced(text: str, max_sentences: int = 5, as_bullets: bool = False) -> str:
    """Advanced text summarization using frequency analysis"""
    try:
        if not text or not str(text).strip():
            return "No content to summarize."
        
        text = str(text)
        sentences = safe_sentence_split(text)
        
        if len(sentences) <= max_sentences:
            if as_bullets:
                return "\n".join(f"• {s}" for s in sentences)
            return " ".join(sentences)
        
        # Word frequency analysis
        word_freq = Counter()
        for sentence in sentences:
            words = re.findall(r'\b[a-zA-Z]+\b', sentence.lower())
            for word in words:
                if word not in STOPWORDS and len(word) > 2:
                    word_freq[word] += 1
        
        if not word_freq:
            if as_bullets:
                return "\n".join(f"• {s}" for s in sentences[:max_sentences])
            return " ".join(sentences[:max_sentences])
        
        # Score sentences based on word frequency
        sentence_scores = []
        for idx, sentence in enumerate(sentences):
            words = re.findall(r'\b[a-zA-Z]+\b', sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words)
            score = score / len(words) if words else 0
            sentence_scores.append((score, idx, sentence))
        
        # Get top sentences
        sentence_scores.sort(key=lambda x: x[0], reverse=True)
        top_sentences = sorted(sentence_scores[:max_sentences], key=lambda x: x[1])
        
        if as_bullets:
            return "\n".join(f"• {sentence[2]}" for sentence in top_sentences)
        else:
            return " ".join(sentence[2] for sentence in top_sentences)
            
    except Exception as e:
        return f"Error creating summary: {str(e)}"

# Python code analysis functions
def analyze_python_code(code: str) -> Dict:
    """Comprehensive Python code analysis"""
    try:
        analysis = {
            'syntax_valid': False,
            'errors': [],
            'metrics': {},
            'suggestions': [],
            'functions': [],
            'classes': [],
            'imports': [],
            'complexity_score': 0
        }
        
        if not code or not str(code).strip():
            return analysis
        
        code = str(code)
        lines = code.splitlines()
        
        # Basic metrics
        analysis['metrics'] = {
            'total_lines': len(lines),
            'code_lines': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
            'comment_lines': len([l for l in lines if l.strip().startswith('#')]),
            'blank_lines': len([l for l in lines if not l.strip()]),
            'avg_line_length': sum(len(l) for l in lines) / len(lines) if lines else 0
        }
        
        # Try to parse AST
        try:
            tree = ast.parse(code)
            analysis['syntax_valid'] = True
            
            # Extract functions, classes, imports
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        analysis['imports'].append(f"{module}.{alias.name}" if module else alias.name)
            
            # Calculate complexity (simplified)
            complexity = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    complexity += 1
            analysis['complexity_score'] = complexity
            
        except SyntaxError as e:
            analysis['errors'].append(f"Syntax Error: {str(e)}")
        except Exception as e:
            analysis['errors'].append(f"Parse Error: {str(e)}")
        
        # Code quality suggestions
        if analysis['metrics']['comment_lines'] == 0:
            analysis['suggestions'].append("Consider adding comments to explain your code")
        
        if analysis['metrics']['avg_line_length'] > 100:
            analysis['suggestions'].append("Some lines are very long - consider breaking them up")
        
        if len(analysis['functions']) == 0 and analysis['metrics']['code_lines'] > 20:
            analysis['suggestions'].append("Consider organizing code into functions for better structure")
        
        return analysis
        
    except Exception as e:
        return {'error': f"Analysis failed: {str(e)}"}

def fix_python_code(code: str) -> Tuple[str, List[str]]:
    """Attempt to fix common Python syntax errors"""
    try:
        if not code:
            return code, []
        
        fixed_code = str(code)
        fixes_applied = []
        
        # Fix 1: Add missing colons
        lines = fixed_code.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped.startswith(('if ', 'elif ', 'else', 'for ', 'while ', 'def ', 'class ', 'try', 'except', 'finally')) 
                and not stripped.endswith(':') and not stripped.endswith(':\\')):
                lines[i] = line + ':'
                fixes_applied.append(f"Line {i+1}: Added missing colon")
        
        fixed_code = '\n'.join(lines)
        
        # Fix 2: Convert print statements to functions
        if 'print ' in fixed_code and 'print(' not in fixed_code:
            fixed_code = re.sub(r'print\s+([^(].*?)$', r'print(\1)', fixed_code, flags=re.MULTILINE)
            fixes_applied.append("Converted print statements to print() functions")
        
        # Fix 3: Basic indentation (simplified)
        lines = fixed_code.splitlines()
        indent_level = 0
        for i, line in enumerate(lines):
            if line.strip():
                if line.strip().endswith(':'):
                    # Next line should be indented
                    if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith('    '):
                        lines[i + 1] = '    ' + lines[i + 1]
                        fixes_applied.append(f"Line {i+2}: Added indentation")
        
        fixed_code = '\n'.join(lines)
        
        return fixed_code, fixes_applied
        
    except Exception as e:
        return code, [f"Fix attempt failed: {str(e)}"]

# Authentication Pages
def login_page():
    st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3>🚀 Advanced AI-Powered Tools for Modern Developers</h3>
        <p style="font-size: 1.1rem; color: rgba(0, 249, 255, 0.8);">
            Text Analysis • Code Enhancement • Web Scraping • AI Integration • Document Processing
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.subheader("🔐 Login to Your Account")
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_signup = st.columns(2)
            
            with col_login:
                if st.button("🚀 Login", use_container_width=True):
                    if username and password:
                        success, message, user_info = AuthManager.login_user(username, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_info = user_info
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("Please enter both username and password.")
            
            with col_signup:
                if st.button("📝 Create Account", use_container_width=True):
                    st.session_state.page = 'signup'
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Demo features section
    st.markdown("---")
    st.markdown("### 🎯 What You Get Access To:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📝 Text Analysis Suite</h4>
            <ul>
                <li>Advanced text summarization</li>
                <li>Word frequency analysis</li>
                <li>Reading metrics & statistics</li>
                <li>Multiple export formats</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🐍 Python Code Tools</h4>
            <ul>
                <li>Syntax error detection & fixing</li>
                <li>Code complexity analysis</li>
                <li>Quality metrics & suggestions</li>
                <li>AI-powered enhancements</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🌐 Web & AI Integration</h4>
            <ul>
                <li>Smart web content scraping</li>
                <li>Document processing & enhancement</li>
                <li>AI chat assistant</li>
                <li>Multi-format support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def signup_page():
    st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            st.subheader("📝 Create Your TechNova Account")
            
            st.info("🎉 Start with a 14-day free trial! No email verification required.")
            
            username = st.text_input("Username", placeholder="Choose a unique username")
            password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            # Password strength indicator
            if password:
                strength = "Weak"
                color = "#ff4444"
                if len(password) >= 8:
                    strength = "Good"
                    color = "#ffaa00"
                if len(password) >= 12 and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
                    strength = "Strong"
                    color = "#00ff00"
                
                st.markdown(f"Password Strength: <span style='color: {color}; font-weight: bold;'>{strength}</span>", unsafe_allow_html=True)
            
            col_create, col_back = st.columns(2)
            
            with col_create:
                if st.button("🚀 Create Account", use_container_width=True):
                    if not username or not username.strip():
                        st.error("Please enter a username.")
                    elif not password or not password.strip():
                        st.error("Please enter a password.")
                    elif not confirm_password or not confirm_password.strip():
                        st.error("Please confirm your password.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        success, message = AuthManager.create_user(username.strip(), password)
                        if success:
                            st.success(message)
                            st.balloons()
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error(message)
            
            with col_back:
                if st.button("← Back to Login", use_container_width=True):
                    st.session_state.page = 'login'
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# Enhanced subscription and usage functions
def show_subscription_info():
    """Display enhanced subscription information and usage stats"""
    user_info = st.session_state.user_info
    sub_type = user_info.get('subscription_type', 'free')
    username = user_info.get('username', '')
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if sub_type == 'free':
            sub_expires = user_info.get('subscription_expires')
            if sub_expires:
                days_left = max(0, (sub_expires - datetime.now()).days)
                st.markdown(f"""
                <div class="subscription-info">
                    <span class="status-indicator status-warning"></span>
                    <strong>🆓 Free Trial Active</strong><br>
                    Days remaining: <strong>{days_left} days</strong><br>
                    Daily limit: <strong>4 uses per tool</strong><br>
                    <small>Upgrade to unlock unlimited usage!</small>
                </div>
                """, unsafe_allow_html=True)
        elif sub_type == 'plus':
            st.markdown("""
            <div class="subscription-info">
                <span class="status-indicator status-online"></span>
                <strong>⭐ TechNova Plus Active</strong><br>
                Status: <strong>Premium Member</strong><br>
                Usage: <strong>Unlimited across all tools</strong><br>
                <small>Thank you for supporting TechNova!</small>
            </div>
            """, unsafe_allow_html=True)
        elif sub_type == 'expired':
            st.markdown("""
            <div class="usage-warning">
                <span class="status-indicator status-offline"></span>
                <strong>⚠️ Trial Expired</strong><br>
                Your free trial has ended. Upgrade to continue using all features.<br>
                <strong>Monthly:</strong> $15/month | <strong>Annual:</strong> $150/year (30% off!)
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Show today's usage stats for free users
        if sub_type == 'free':
            usage_stats = UsageManager.get_usage_stats(username)
            if usage_stats:
                st.markdown("**📊 Today's Usage:**")
                for tool, count in usage_stats.items():
                    if count > 0:
                        color = "#ff4444" if count >= 4 else "#00f9ff"
                        st.markdown(f"<span style='color: {color};'>• {tool}: {count}/4</span>", unsafe_allow_html=True)

def check_tab_access(tab_name: str) -> bool:
    """Enhanced tab access checking with better messaging"""
    username = st.session_state.user_info['username']
    can_use, message = UsageManager.can_use_tab(username, tab_name)
    
    if not can_use:
        st.error(message)
        if "expired" in message.lower():
            st.markdown("""
            ### 🚀 Upgrade to TechNova Plus
            
            **🎯 What you get:**
            - ♾️ Unlimited usage across all tools
            - 🚀 Priority processing speed
            - 🆕 Early access to new features
            - 📧 Premium email support
            
            **💰 Pricing:**
            - **Monthly**: $15/month
            - **Annual**: $150/year (Save 30% - Best Value!)
            
            📞 Contact our support team to upgrade your account.
            """)
        return False
    
    return True

def log_tab_usage(tab_name: str):
    """Enhanced usage logging"""
    username = st.session_state.user_info['username']
    UsageManager.log_usage(username, tab_name)

# File processing functions
def process_uploaded_file(uploaded_file) -> Tuple[str, str]:
    """Process uploaded files with enhanced error handling"""
    try:
        if uploaded_file is None:
            return "", "No file uploaded"
        
        file_type = uploaded_file.type
        file_name = uploaded_file.name
        
        # Read file content based on type
        if file_type == "text/plain" or file_name.endswith(('.txt', '.md', '.py', '.js', '.html', '.css')):
            content = str(uploaded_file.read(), "utf-8")
            return content, f"Successfully loaded {file_name}"
        
        elif file_type == "application/pdf":
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
                return content, f"Successfully extracted text from {file_name}"
            except ImportError:
                return "", "PDF processing not available - PyPDF2 not installed"
            except Exception as e:
                return "", f"Error reading PDF: {str(e)}"
        
        else:
            return "", f"Unsupported file type: {file_type}"
            
    except Exception as e:
        return "", f"Error processing file: {str(e)}"

# Enhanced AI detection for code
def detect_ai_generated_code(code: str) -> Dict:
    """Detect if code might be AI-generated"""
    try:
        if not code:
            return {'probability': 0, 'indicators': [], 'confidence': 'Low'}
        
        code = str(code)
        indicators = []
        score = 0
        
        # Check for AI patterns
        lines = code.splitlines()
        
        # 1. Comment density
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        if comment_lines / len(lines) > 0.3:
            indicators.append("High comment density")
            score += 15
        
        # 2. Perfect formatting
        if all(not line.endswith(' ') for line in lines if line.strip()):
            indicators.append("Perfect formatting (no trailing spaces)")
            score += 10
        
        # 3. Generic variable names
        generic_vars = ['data', 'result', 'output', 'input', 'temp', 'item', 'value']
        var_matches = sum(1 for var in generic_vars if var in code.lower())
        if var_matches >= 3:
            indicators.append("Multiple generic variable names")
            score += 20
        
        # 4. Docstring patterns
        if '"""' in code or "'''" in code:
            docstring_count = code.count('"""') + code.count("'''")
            if docstring_count >= 2:
                indicators.append("Comprehensive docstrings")
                score += 15
        
        # 5. Error handling patterns
        if 'try:' in code and 'except' in code:
            indicators.append("Comprehensive error handling")
            score += 10
        
        # 6. Import organization
        import_lines = [l for l in lines if l.strip().startswith('import') or l.strip().startswith('from')]
        if len(import_lines) > 3 and all('import' in l for l in import_lines[:3]):
            indicators.append("Well-organized imports")
            score += 10
        
        # Determine confidence
        if score >= 50:
            confidence = 'High'
        elif score >= 25:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return {
            'probability': min(score, 100),
            'indicators': indicators,
            'confidence': confidence,
            'score_breakdown': {
                'formatting': score
            }
        }
        
    except Exception as e:
        return {'probability': 0, 'indicators': [f'Analysis error: {str(e)}'], 'confidence': 'Error'}

# Main application pages
def main_page():
    """Enhanced main application page"""
    st.markdown('<h1 class="main-title">🌌 TECHNOVA AI NEXUS</h1>', unsafe_allow_html=True)
    
    # Enhanced header with user info
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"**🚀 Welcome back, {st.session_state.user_info['username']}!**")
    with col2:
        current_time = datetime.now().strftime("%H:%M")
        st.markdown(f"**🕒 {current_time}**")
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    with col4:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.session_state.page = 'login'
            st.rerun()
    
    # Show subscription info
    show_subscription_info()
    
    # Enhanced tabs with more functionality
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Text Analyzer", 
        "🐍 Python Tools", 
        "🌐 Web Scraper", 
        "📄 Document Processor",
        "🤖 AI Assistant"
    ])
    
    # Tab 1: Enhanced Text Analyzer
    with tab1:
        st.header("📝 Advanced Text Analysis Suite")
        
        if not check_tab_access("Text Analyzer"):
            return
        
        # Input methods
        input_method = st.radio("Choose input method:", ["Direct Input", "File Upload"], horizontal=True)
        
        text_content = ""
        
        if input_method == "Direct Input":
            text_content = st.text_area("📝 Paste your text here:", height=200, placeholder="Enter or paste your text for analysis...")
        else:
            uploaded_file = st.file_uploader("📁 Upload a text file", type=['txt', 'md', 'py', 'js', 'html', 'css'])
            if uploaded_file:
                text_content, status = process_uploaded_file(uploaded_file)
                if text_content:
                    st.success(status)
                    st.text_area("📄 File Content Preview:", text_content[:1000] + "..." if len(text_content) > 1000 else text_content, height=150)
                else:
                    st.error(status)
        
        if text_content:
            col1, col2, col3 = st.columns(3)
            with col1:
                max_sentences = st.slider("📏 Summary length (sentences)", 1, 15, 5)
            with col2:
                summary_style = st.selectbox("📋 Summary style", ["Paragraph", "Bullet Points", "Numbered List"])
            with col3:
                analysis_depth = st.selectbox("🔍 Analysis depth", ["Basic", "Detailed", "Comprehensive"])
            
            if st.button("🚀 Analyze Text", type="primary", use_container_width=True):
                log_tab_usage("Text Analyzer")
                
                with st.spinner("🔍 Analyzing your text..."):
                    # Get text metrics
                    metrics = analyze_text_metrics(text_content)
                    
                    if metrics:
                        # Display metrics in cards
                        st.subheader("📊 Text Metrics")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3>{metrics.get('words', 0):,}</h3>
                                <p>Words</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3>{metrics.get('characters', 0):,}</h3>
                                <p>Characters</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3>{metrics.get('sentences', 0)}</h3>
                                <p>Sentences</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col4:
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3>{metrics.get('unique_words', 0)}</h3>
                                <p>Unique Words</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Detailed analysis
                        if analysis_depth in ["Detailed", "Comprehensive"]:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("📈 Reading Metrics")
                                st.write(f"**Average words per sentence:** {metrics.get('avg_words_per_sentence', 0)}")
                                st.write(f"**Average characters per word:** {metrics.get('avg_chars_per_word', 0)}")
                                st.write(f"**Word diversity ratio:** {metrics.get('word_diversity', 0):.2%}")
                                
                                # Reading difficulty estimate
                                avg_words = metrics.get('avg_words_per_sentence', 0)
                                if avg_words < 15:
                                    difficulty = "Easy"
                                elif avg_words < 25:
                                    difficulty = "Medium"
                                else:
                                    difficulty = "Complex"
                                st.write(f"**Estimated difficulty:** {difficulty}")
                            
                            with col2:
                                if metrics.get('top_words'):
                                    st.subheader("🔤 Most Common Words")
                                    for word, count in metrics['top_words']:
                                        st.write(f"**{word}:** {count} times")
                        
                        # Generate summary
                        st.subheader("📋 Text Summary")
                        as_bullets = summary_style == "Bullet Points"
                        as_numbered = summary_style == "Numbered List"
                        
                        summary = summarize_text_advanced(text_content, max_sentences, as_bullets)
                        
                        if as_numbered:
                            sentences = summary.split('. ')
                            summary = '\n'.join(f"{i+1}. {s.strip('• ')}" for i, s in enumerate(sentences) if s.strip())
                        
                        st.write(summary)
                        
                        # Export options
                        col1, col2 = st.columns(2)
                        with col1:
                            copy_button(summary, "Copy Summary", "text_summary")
                        with col2:
                            full_report = f"""TechNova AI Nexus - Text Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TEXT METRICS:
- Words: {metrics.get('words', 0):,}
- Characters: {metrics.get('characters', 0):,}
- Sentences: {metrics.get('sentences', 0)}
- Lines: {metrics.get('lines', 0)}
- Unique Words: {metrics.get('unique_words', 0)}
- Word Diversity: {metrics.get('word_diversity', 0):.2%}

SUMMARY:
{summary}

MOST COMMON WORDS:
{chr(10).join([f"- {word}: {count}" for word, count in metrics.get('top_words', [])[:10]])}
"""
                            download_button_enhanced(full_report, f"text_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "Download Report")
    
    # Tab 2: Enhanced Python Tools
    with tab2:
        st.header("🐍 Python Code Analysis & Enhancement")
        
        if not check_tab_access("Python Tools"):
            return
        
        # Input methods for code
        code_input_method = st.radio("Code input method:", ["Direct Input", "File Upload"], horizontal=True)
        
        code_content = ""
        
        if code_input_method == "Direct Input":
            code_content = st.text_area("🐍 Enter your Python code:", height=250, placeholder="# Paste your Python code here\nprint('Hello, TechNova!')")
        else:
            uploaded_code = st.file_uploader("📁 Upload Python file", type=['py'])
            if uploaded_code:
                code_content, status = process_uploaded_file(uploaded_code)
                if code_content:
                    st.success(status)
                    st.code(code_content, language="python")
                else:
                    st.error(status)
        
        if code_content:
            # Analysis options
            col1, col2, col3 = st.columns(3)
            with col1:
                analyze_syntax = st.checkbox("🔍 Syntax Analysis", value=True)
            with col2:
                analyze_quality = st.checkbox("📊 Quality Metrics", value=True)
            with col3:
                detect_ai = st.checkbox("🤖 AI Detection", value=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
                    log_tab_usage("Python Tools")
                    
                    with st.spinner("🔍 Analyzing Python code..."):
                        analysis = analyze_python_code(code_content)
                        
                        # Syntax Analysis
                        if analyze_syntax:
                            st.subheader("🔍 Syntax Analysis")
                            if analysis.get('syntax_valid'):
                                st.success("✅ Code syntax is valid!")
                            else:
                                st.error("❌ Syntax errors detected:")
                                for error in analysis.get('errors', []):
                                    st.write(f"• {error}")
                        
                        # Code Metrics
                        if analyze_quality and 'metrics' in analysis:
                            st.subheader("📊 Code Quality Metrics")
                            metrics = analysis['metrics']
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Lines", metrics.get('total_lines', 0))
                            with col2:
                                st.metric("Code Lines", metrics.get('code_lines', 0))
                            with col3:
                                st.metric("Comments", metrics.get('comment_lines', 0))
                            with col4:
                                st.metric("Functions", len(analysis.get('functions', [])))
                            
                            # Additional metrics
                            if analysis.get('functions'):
                                st.write(f"**Functions found:** {', '.join(analysis['functions'])}")
                            if analysis.get('classes'):
                                st.write(f"**Classes found:** {', '.join(analysis['classes'])}")
                            if analysis.get('imports'):
                                st.write(f"**Imports:** {', '.join(analysis['imports'][:10])}")
                            
                            st.write(f"**Complexity Score:** {analysis.get('complexity_score', 0)}")
                        
                        # Suggestions
                        if analysis.get('suggestions'):
                            st.subheader("💡 Improvement Suggestions")
                            for suggestion in analysis['suggestions']:
                                st.write(f"• {suggestion}")
                        
                        # AI Detection
                        if detect_ai:
                            ai_analysis = detect_ai_generated_code(code_content)
                            st.subheader("🤖 AI Generation Analysis")
                            
                            prob = ai_analysis.get('probability', 0)
                            confidence = ai_analysis.get('confidence', 'Low')
                            
                            if prob >= 60:
                                st.warning(f"⚠️ High probability ({prob}%) of AI generation - Confidence: {confidence}")
                            elif prob >= 30:
                                st.info(f"🤔 Moderate probability ({prob}%) of AI generation - Confidence: {confidence}")
                            else:
                                st.success(f"✅ Low probability ({prob}%) of AI generation - Confidence: {confidence}")
                            
                            if ai_analysis.get('indicators'):
                                st.write("**Indicators found:**")
                                for indicator in ai_analysis['indicators']:
                                    st.write(f"• {indicator}")
            
            with col2:
                if st.button("🔧 Auto-Fix Code", type="secondary", use_container_width=True):
                    log_tab_usage("Python Tools")
                    
                    with st.spinner("🔧 Attempting to fix code issues..."):
                        fixed_code, fixes = fix_python_code(code_content)
                        
                        if fixes:
                            st.subheader("🔧 Code Fixes Applied")
                            for fix in fixes:
                                st.write(f"✅ {fix}")
                            
                            st.subheader("🐍 Fixed Code")
                            st.code(fixed_code, language="python")
                            copy_button(fixed_code, "Copy Fixed Code", "fixed_code")
                        else:
                            st.info("✅ No fixes needed - your code looks good!")
    
    # Tab 3: Enhanced Web Scraper
    with tab3:
        st.header("🌐 Advanced Web Content Scraper")
        
        if not check_tab_access("Web Scraper"):
            return
        
        url_input = st.text_input("🌍 Enter URL to scrape:", placeholder="https://example.com")
        
        # Scraping options
        col1, col2 = st.columns(2)
        with col1:
            include_links = st.checkbox("🔗 Extract links", value=False)
        with col2:
            clean_content = st.checkbox("🧹 Clean content", value=True)
        
        if st.button("🚀 Scrape Content", type="primary", use_container_width=True):
            if url_input.strip():
                log_tab_usage("Web Scraper")
                
                with st.spinner("🌐 Scraping web content..."):
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                        
                        response = requests.get(url_input, headers=headers, timeout=15)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract title
                        title = soup.find('title')
                        page_title = title.get_text().strip() if title else "No title found"
                        
                        # Remove unwanted elements
                        for element in soup(["script", "style", "nav", "footer", "header"]):
                            element.decompose()
                        
                        # Extract main content
                        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))
                        if not main_content:
                            main_content = soup.find('body') or soup
                        
                        # Get text content
                        text = main_content.get_text(separator=' ', strip=True)
                        
                        if clean_content:
                            # Clean up whitespace and formatting
                            text = re.sub(r'\s+', ' ', text)
                            text = re.sub(r'\n\s*\n', '\n', text)
                        
                        # Extract links if requested
                        links = []
                        if include_links:
                            for link in soup.find_all('a', href=True):
                                href = link['href']
                                link_text = link.get_text().strip()
                                if href.startswith('http') and link_text:
                                    links.append({'url': href, 'text': link_text})
                        
                        if text:
                            st.success(f"✅ Successfully scraped content from: {page_title}")
                            
                            # Show metrics
                            metrics = analyze_text_metrics(text)
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("📝 Words", f"{metrics.get('words', 0):,}")
                            with col2:
                                st.metric("📄 Characters", f"{metrics.get('characters', 0):,}")
                            with col3:
                                st.metric("📖 Sentences", metrics.get('sentences', 0))
                            
                            # Content preview
                            st.subheader("📄 Content Preview")
                            preview_length = min(2000, len(text))
                            preview = text[:preview_length]
                            if len(text) > preview_length:
                                preview += "..."
                            
                            st.text_area("Content:", preview, height=200)
                            
                            # Links section
                            if links:
                                st.subheader(f"🔗 Links Found ({len(links)})")
                                for i, link in enumerate(links[:10]):  # Show first 10 links
                                    st.write(f"[{link['text']}]({link['url']})")
                                if len(links) > 10:
                                    st.write(f"... and {len(links) - 10} more links")
                            
                            # Export options
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                copy_button(text, "Copy Full Content", "scraped_content")
                            
                            with col2:
                                if st.button("📋 Generate Summary"):
                                    summary = summarize_text_advanced(text, 7, False)
                                    st.write("**Summary:**")
                                    st.write(summary)
                                    copy_button(summary, "Copy Summary", "scraped_summary")
                            
                            with col3:
                                # Create comprehensive report
                                report = f"""TechNova Web Scraping Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
URL: {url_input}
Title: {page_title}

CONTENT METRICS:
- Words: {metrics.get('words', 0):,}
- Characters: {metrics.get('characters', 0):,}
- Sentences: {metrics.get('sentences', 0)}

CONTENT:
{text}

LINKS FOUND: {len(links)}
{chr(10).join([f"- {link['text']}: {link['url']}" for link in links[:20]])}
"""
                                download_button_enhanced(report, f"web_scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "Download Report")
                        
                        else:
                            st.warning("⚠️ No readable content found on this page.")
                            
                    except requests.exceptions.Timeout:
                        st.error("⏰ Request timed out. The website may be slow or unresponsive.")
                    except requests.exceptions.ConnectionError:
                        st.error("🌐 Connection error. Please check the URL and your internet connection.")
                    except requests.exceptions.HTTPError as e:
                        st.error(f"🚫 HTTP Error: {e.response.status_code} - {e.response.reason}")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")
            else:
                st.error("⚠️ Please enter a valid URL to scrape.")
    
    # Tab 4: Document Processor
    with tab4:
        st.header("📄 Document Processing & Enhancement")
        
        if not check_tab_access("Document Processor"):
            return
        
        uploaded_doc = st.file_uploader(
            "📁 Upload document for processing", 
            type=['txt', 'md', 'py', 'js', 'html', 'css', 'json'],
            help="Supported formats: TXT, Markdown, Python, JavaScript, HTML, CSS, JSON"
        )
        
        if uploaded_doc:
            doc_content, status = process_uploaded_file(uploaded_doc)
            
            if doc_content:
                st.success(status)
                log_tab_usage("Document Processor")
                
                # Document analysis
                file_type = uploaded_doc.name.split('.')[-1].lower()
                metrics = analyze_text_metrics(doc_content)
                
                # Show document info
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📁 File Type", file_type.upper())
                with col2:
                    st.metric("📝 Words", f"{metrics.get('words', 0):,}")
                with col3:
                    st.metric("📄 Lines", metrics.get('lines', 0))
                with col4:
                    file_size = len(doc_content.encode('utf-8'))
                    st.metric("💾 Size", f"{file_size:,} bytes")
                
                # Content preview
                st.subheader("📖 Document Preview")
                preview = doc_content[:1500] + "..." if len(doc_content) > 1500 else doc_content
                
                if file_type in ['py', 'js', 'html', 'css', 'json']:
                    st.code(preview, language=file_type if file_type != 'py' else 'python')
                else:
                    st.text_area("Content Preview:", preview, height=200)
                
                # Processing options
                st.subheader("🔧 Processing Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📊 Generate Analysis Report", use_container_width=True):
                        with st.spinner("🔍 Analyzing document..."):
                            # Comprehensive analysis
                            summary = summarize_text_advanced(doc_content, 5, False)
                            
                            # Create detailed report
                            analysis_report = f"""TechNova Document Analysis Report
========================================
File: {uploaded_doc.name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DOCUMENT METRICS:
- File Type: {file_type.upper()}
- Total Words: {metrics.get('words', 0):,}
- Total Characters: {metrics.get('characters', 0):,}
- Total Lines: {metrics.get('lines', 0)}
- Total Sentences: {metrics.get('sentences', 0)}
- Unique Words: {metrics.get('unique_words', 0)}
- Word Diversity: {metrics.get('word_diversity', 0):.2%}
- Average Words per Sentence: {metrics.get('avg_words_per_sentence', 0):.1f}

SUMMARY:
{summary}

MOST FREQUENT WORDS:
{chr(10).join([f"{i+1}. {word}: {count} occurrences" for i, (word, count) in enumerate(metrics.get('top_words', [])[:15])])}

DOCUMENT STRUCTURE:
- Estimated Reading Time: {metrics.get('words', 0) // 200 + 1} minutes
- Complexity Level: {"High" if metrics.get('avg_words_per_sentence', 0) > 20 else "Medium" if metrics.get('avg_words_per_sentence', 0) > 15 else "Simple"}
"""
                            
                            st.text_area("📊 Analysis Report", analysis_report, height=300)
                            download_button_enhanced(analysis_report, f"analysis_{uploaded_doc.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "Download Analysis")
                
                with col2:
                    if file_type == 'py' and st.button("🐍 Python Code Analysis", use_container_width=True):
                        with st.spinner("🔍 Analyzing Python code..."):
                            py_analysis = analyze_python_code(doc_content)
                            
                            if py_analysis.get('syntax_valid'):
                                st.success("✅ Valid Python syntax!")
                            else:
                                st.error("❌ Syntax errors found:")
                                for error in py_analysis.get('errors', []):
                                    st.write(f"• {error}")
                            
                            # Show code metrics
                            if 'metrics' in py_analysis:
                                st.write("**Code Metrics:**")
                                metrics = py_analysis['metrics']
                                st.write(f"• Code lines: {metrics.get('code_lines', 0)}")
                                st.write(f"• Comment lines: {metrics.get('comment_lines', 0)}")
                                st.write(f"• Functions: {len(py_analysis.get('functions', []))}")
                                st.write(f"• Classes: {len(py_analysis.get('classes', []))}")
                                st.write(f"• Complexity: {py_analysis.get('complexity_score', 0)}")
                
                # Additional processing options
                st.subheader("🚀 Enhancement Options")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📝 Create Summary", use_container_width=True):
                        summary_length = st.slider("Summary sentences:", 3, 10, 5)
                        summary = summarize_text_advanced(doc_content, summary_length, False)
                        
                        st.subheader("📋 Document Summary")
                        st.write(summary)
                        copy_button(summary, "Copy Summary", "doc_summary")
                
                with col2:
                    if st.button("🔤 Extract Keywords", use_container_width=True):
                        keywords = metrics.get('top_words', [])[:20]
                        
                        st.subheader("🔑 Key Terms")
                        keyword_text = ", ".join([word for word, count in keywords])
                        st.write(keyword_text)
                        copy_button(keyword_text, "Copy Keywords", "keywords")
                
                with col3:
                    if file_type in ['txt', 'md'] and st.button("📚 Reading Stats", use_container_width=True):
                        reading_time = max(1, metrics.get('words', 0) // 200)  # Average 200 words per minute
                        
                        st.subheader("📊 Reading Statistics")
                        st.write(f"**Estimated reading time:** {reading_time} minutes")
                        st.write(f"**Reading difficulty:** {'Advanced' if metrics.get('avg_words_per_sentence', 0) > 20 else 'Intermediate' if metrics.get('avg_words_per_sentence', 0) > 15 else 'Easy'}")
                        st.write(f"**Vocabulary richness:** {metrics.get('word_diversity', 0):.1%}")
            else:
                st.error(status)
    
    # Tab 5: AI Assistant (Mock implementation)
    with tab5:
        st.header("🤖 AI-Powered Assistant")
        
        if not check_tab_access("AI Assistant"):
            return
        
        # Check for API key configuration
        api_key_configured = bool(os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY'))
        
        if not api_key_configured:
            st.warning("⚙️ OpenAI API key not configured. Using demo mode with simulated responses.")
        
        # Chat interface
        st.subheader("💬 Ask the AI Assistant")
        
        # Conversation history in session state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Assistant type selection
        assistant_type = st.selectbox(
            "🤖 Choose assistant type:",
            ["General Assistant", "Code Helper", "Writing Assistant", "Data Analyst", "Web Developer"]
        )
        
        user_message = st.text_area("💭 Your message:", height=100, placeholder="Ask me anything! I can help with code, writing, analysis, and more...")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("🚀 Send Message", type="primary", use_container_width=True):
                if user_message.strip():
                    log_tab_usage("AI Assistant")
                    
                    with st.spinner("🤖 AI is thinking..."):
                        # Since we can't use actual OpenAI API without proper configuration,
                        # provide intelligent mock responses based on the message content
                        
                        message_lower = user_message.lower()
                        
                        # Generate contextual responses based on keywords
                        if any(word in message_lower for word in ['code', 'python', 'programming', 'function', 'bug']):
                            ai_response = f"""I'd be happy to help with your coding question! Based on your message about "{user_message[:50]}...", here are some suggestions:

🐍 **For Python code issues:**
- Check for proper indentation (Python is strict about this)
- Ensure all parentheses and brackets are properly closed
- Verify variable names are spelled consistently
- Use print() statements for debugging

🔧 **General coding tips:**
- Break complex problems into smaller functions
- Add comments to explain your logic
- Test your code with different inputs
- Consider edge cases

Would you like me to analyze any specific code you're working on? You can paste it in the Python Tools tab for detailed analysis!"""

                        elif any(word in message_lower for word in ['write', 'writing', 'essay', 'article', 'content']):
                            ai_response = f"""I can help you improve your writing! For your request about "{user_message[:50]}...", here are some suggestions:

✍️ **Writing improvement tips:**
- Start with a clear outline of your main points
- Use active voice when possible
- Vary your sentence length for better flow
- Include specific examples to support your arguments

📝 **Structure recommendations:**
- Introduction: Hook + thesis statement
- Body: One main idea per paragraph
- Conclusion: Summarize and call to action

💡 **Enhancement ideas:**
- Use the Text Analyzer tab to check readability
- Try the Document Processor for detailed analysis
- Consider your target audience's knowledge level

Would you like me to help you with any specific aspect of your writing?"""

                        elif any(word in message_lower for word in ['data', 'analyze', 'analysis', 'statistics', 'numbers']):
                            ai_response = f"""Great question about data analysis! Regarding "{user_message[:50]}...", here's how I can help:

📊 **Data analysis approach:**
- Define your research questions clearly
- Identify what metrics are most important
- Look for patterns and trends in your data
- Consider both quantitative and qualitative aspects

🔍 **TechNova tools for analysis:**
- Use Text Analyzer for content metrics
- Web Scraper for gathering online data
- Document Processor for file analysis
- Python Tools for data processing scripts

📈 **Key analysis steps:**
1. Data collection and cleaning
2. Exploratory data analysis
3. Statistical testing or modeling
4. Interpretation and visualization
5. Drawing actionable conclusions

What type of data are you working with? I can provide more specific guidance!"""

                        elif any(word in message_lower for word in ['web', 'website', 'html', 'css', 'javascript']):
                            ai_response = f"""I can definitely help with web development! For your question about "{user_message[:50]}...", here are some insights:

🌐 **Web development best practices:**
- Use semantic HTML for better accessibility
- Implement responsive design for all devices
- Optimize images and assets for faster loading
- Follow modern CSS practices (Flexbox, Grid)

🛠️ **TechNova tools for web development:**
- Web Scraper: Analyze competitor websites
- Python Tools: Process web-related scripts
- Document Processor: Analyze HTML/CSS files
- Text Analyzer: Optimize content for readability

💻 **Current trends to consider:**
- Progressive Web Apps (PWAs)
- Mobile-first design approach
- Core Web Vitals optimization
- Accessibility (WCAG guidelines)

What specific aspect of web development are you working on? I can provide more targeted advice!"""

                        else:
                            # General response
                            ai_response = f"""Thank you for your question about "{user_message[:50]}..."! 

I'm here to help you with a wide range of tasks. Here's what I can assist you with using TechNova's powerful tools:

🔧 **Available capabilities:**
- **Text Analysis**: Summarize documents, analyze readability, extract key insights
- **Code Analysis**: Debug Python code, improve code quality, detect issues  
- **Web Scraping**: Extract content from websites, analyze online data
- **Document Processing**: Handle various file formats, generate reports
- **Content Enhancement**: Improve writing, optimize for different audiences

💡 **How to get the best help:**
- Be specific about what you're trying to accomplish
- Share relevant code, text, or URLs when applicable  
- Let me know your experience level with the topic
- Ask follow-up questions to dive deeper

🚀 **Next steps:**
Try using the specific tabs above for hands-on analysis, or ask me more detailed questions about your project. I'm designed to provide practical, actionable advice!

What would you like to explore first?"""

                        # Add to chat history
                        st.session_state.chat_history.append({
                            'user': user_message,
                            'assistant': ai_response,
                            'timestamp': datetime.now()
                        })
                        
                        st.rerun()
                else:
                    st.error("⚠️ Please enter a message to send to the AI assistant.")
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        # Display chat history
        if st.session_state.chat_history:
            st.subheader("💬 Conversation History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5 exchanges
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(0, 249, 255, 0.1); padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 3px solid #00f9ff;">
                        <strong>🧑 You:</strong> {chat['user']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="background: rgba(0, 153, 204, 0.1); padding: 10px; border-radius: 5px; margin: 10px 0; border-left: 3px solid #0099cc;">
                        <strong>🤖 AI Assistant:</strong><br>{chat['assistant'].replace(chr(10), '<br>')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Copy response button
                    copy_button(chat['assistant'], f"Copy Response #{len(st.session_state.chat_history)-i}", f"chat_{i}")
                    
                    if i < len(st.session_state.chat_history) - 1:
                        st.markdown("---")
        
        # Usage tips
        with st.expander("💡 AI Assistant Tips"):
            st.markdown("""
            **🎯 Get better responses by:**
            - Being specific about your goals and requirements
            - Providing context about your skill level
            - Asking follow-up questions to clarify details
            - Using the specialized tabs for detailed analysis
            
            **🔧 Best practices:**
            - Start with general questions, then get more specific
            - Combine AI advice with hands-on tool usage
            - Experiment with different approaches
            - Save important responses using the copy buttons
            
            **⚡ Pro tip:** The AI assistant works great in combination with other TechNova tools - analyze your content first, then ask for specific improvement suggestions!
            """)

# Enhanced main application logic
def main():
    """Main application function with enhanced error handling"""
    
    try:
        # Handle authentication flow
        if not st.session_state.authenticated:
            if st.session_state.page == 'login':
                login_page()
            elif st.session_state.page == 'signup':
                signup_page()
            return
        
        # Show main application
        main_page()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: rgba(0, 249, 255, 0.6); margin: 2rem 0;">
            <p>🌌 <strong>TechNova AI Nexus</strong> - Advanced AI Tools for Modern Developers</p>
            <p>Powered by cutting-edge technology • Built for productivity • Designed for innovation</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()
