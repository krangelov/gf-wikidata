const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get("lang") == null)
    urlParams.set("lang","ParseEng")
if (urlParams.get("edit") && !urlParams.get("qid"))
    urlParams.delete("edit")

function showSearches(searchbox) {
    if (searchbox.value.length < 3) return;

    const lang = urlParams.get("lang");
    let lang_code = null;
    for (let i in gfwordnet.languages) {
        if (gfwordnet.languages[i][1] == lang) {
            lang_code = gfwordnet.languages[i][2];
        }
    }
    if (!lang_code)
        return;
	fetch("https://www.wikidata.org/w/api.php?action=wbsearchentities&language="+lang_code+"&uselang="+lang_code+"&type=item&continue=0&origin=*&format=json&search="+encodeURIComponent(searchbox.value),
          { method: "GET" })
       .then((response) => response.json())
       .then((data) => {
                const searchResults = document.getElementById("searchResults");
                searchResults.innerHTML = "";
                searchResults.style.display = "none";
                for (const res of data.search) {
                    searchResults.style.display = "block";

                    const option = document.createElement("TR");
                    option.dataset.qid = res.id;
                    if (res.label != null) {
                        const value = document.createElement("DIV");
                        value.appendChild(document.createTextNode(res.label));
                        option.appendChild(value);
                    }
                    if (res.description != null) {
                        const descr = document.createElement("DIV");
                        descr.appendChild(document.createTextNode(res.description));
                        option.appendChild(descr);
                    }

                    option.addEventListener('mouseenter', (event) => {
                        let element = searchResults.firstElementChild;
                        while (element != null) {
                            element.className = null;
                            element = element.nextElementSibling;
                        }
                        event.target.className = "current";
                    });
                    option.addEventListener('mouseleave', (event) => {
                        let element = searchResults.firstElementChild;
                        while (element != null) {
                            element.className = null;
                            element = element.nextElementSibling;
                        }
                    });
                    option.addEventListener('click', (event) => {
                        loadEntity(event.target.parentElement.dataset.qid);
                    });

                    searchResults.appendChild(option);
                    
                    if (res.label == searchbox.value) {
                        searchbox.dataset.qid = res.id;
                    }
                }
             });
}

function searchInputOnKeyPress(event) {
    if (event.key === "Enter") {
        event.preventDefault();

        let element = searchResults.firstElementChild;
        while (element != null) {
            if (element.className == "current") {
                break;
            }
            element = element.nextElementSibling;
        }
        if (element == null)
            element = searchResults.firstElementChild;
        if (element != null) {
            loadEntity(element.dataset.qid);
        }
    }
}
function searchInputOnKeyDown(event) {
    const searchResults = document.getElementById("searchResults");
    if (event.code === "ArrowUp") {
        event.preventDefault();
        let element = searchResults.firstElementChild;
        let last    = null;
        while (element != null) {
            if (element.className == "current") {
                if (last != null) {
                    element.className = null;
                    last.className = "current";
                }
                break;
            }
            last    = element;
            element = element.nextElementSibling;
        }
    } else if (event.code === "ArrowDown") {
        event.preventDefault();
        let element = searchResults.firstElementChild;
        while (element != null) {
            const next = element.nextElementSibling;
            if (element.className == "current") {
                if (next != null) {
                    element.className = null;
                    next.className = "current";
                }
                break;
            }
            element = next;
        }
        if (element == null) {
            searchResults.firstElementChild.className = "current";
        }
    }
}
function loadEntity(qid) {
    const searchInput = document.getElementById("searchInput");
    searchInput.value = "";
    const searchResults = document.getElementById("searchResults");
    searchResults.style.display = "none";
    window.location.href = "gf-wikidata.wiki?qid="+qid+"&lang="+urlParams.get("lang");
}

function init_editor() {
    let langs = []
    if (urlParams.get("edit")) {
        let s = window.localStorage.getItem('gp-languages');
        if (s) langs = s.split(' ');
    }

    const from = element('from');
    for (let i in gfwordnet.languages) {
        const name = gfwordnet.languages[i][0];
        let checked = langs.includes(name);
        if (gfwordnet.languages[i][1] == urlParams.get("lang")) {
            var row = tr([td([node("b",{},[text(name)])])]);
            checked = true;
        } else {
            let url = "gf-wikidata.wiki"
            url += "?lang="+gfwordnet.languages[i][1];
            const qid = urlParams.get("qid");
            if (qid != null)
                url += "&qid="+qid;
            var row = tr([td([node("a",{href: url},[text(name)])])]);
        }

        if (urlParams.get("edit")) {
            const checkbox = node("input",{type: "checkbox"},[]);
            if (checked)
                checkbox.checked = true;
            row.appendChild(checkbox);
        }

        from.appendChild(row);
    }

    if (urlParams.get("qid")) {
        editor = element('editor');
        const evalBtn = element("eval");
        const navigation = element("navigation");
        const params = new URLSearchParams(window.location.search);
        if (urlParams.get("edit")) {
            params.delete("edit");
            const href = window.location.href.split('?')[0]+"?"+params.toString();
            navigation.appendChild(node("li", {}, [node("a", {"href": href}, [text("Page")])]));
            navigation.appendChild(node("li", {"class": "selected"}, [text("Edit")]));

            const prog = editor.innerText; editor.innerText = "";
            editor = CodeMirror(editor,{lineNumbers: true, mode: "haskell"});
            editor.getDoc().setValue(prog);
            editor.setSize(null,  300);

            evalBtn.addEventListener("click", test);
        } else {
            params.set("edit",1);
            const href = window.location.href.split('?')[0]+"?"+params.toString();
            navigation.appendChild(node("li", {"class": "selected"}, [text("Page")]));
            navigation.appendChild(node("li", {}, [node("a", {"href": href}, [text("Edit")])]));

            editor.style.display = "none";
            evalBtn.style.display = "none";
        }
    } else {
        const editor = element('editor');
        const evalBtn = element("eval");
        editor.style.display = "none";
        evalBtn.style.display = "none";
    }

    var user   = getCookie("user");
    var author = getCookie("author");
    var token  = getCookie("token");
    if (user != null && author != 0) {
        var logIn      = element('logIn');
        var commit     = element('commit');
        logIn.innerHTML = "Log Out "+user;
        logIn.href = "javascript:logOut()"

        gfwordnet.set_user(user,author,token,0,null,commit);
        commit.style.display = "inline";
    }
}

async function test() {
    const data = {
        lang: urlParams.get("lang"),
        code: editor.getValue(),
        qid: urlParams.get("qid")
    };
    const response = await fetch("FunctionsService.fcgi",
        {method: "POST",
         body: JSON.stringify(data),
        });
    const output   = element("output");
    output.innerHTML = "";
    if (response.status == 200) {
        const result = await response.json();
        output.appendChild(node("pre",{},[text(result.msg)]));
        if (result.groups.length == 0)
            output.appendChild(node("b",{},[text("No results")]));
        else if (result.groups.length == 1 &&
                 result.groups[0].headers.length == 1 &&
                 result.groups[0].dataset.length == 1) {
            const header = result.groups[0].headers[0];
            const value  = result.groups[0].dataset[0];
            if (header.type == "markup") {
                output.innerHTML = value;
            } else {
                output.appendChild(text(value));
            }
        } else {
            for (var group of result.groups) {
                const res_tbl = node("table",{"class": "dataset"},[]);
                const row = []
                for (var header of group.headers) {
                    row.push(th([text(header.label)]));
                }
                res_tbl.appendChild(tr(row))
                for (var record of group.dataset) {
                    const row = []
                    for (let i in record) {
                        const value  = record[i];
                        const header = group.headers[i];
                        if (header.type == "markup") {
                            const e = td([]);
                            e.innerHTML = value;
                            row.push(e);
                        } else if (header.type == "number") {
                            row.push(node("td",{style: "text-align: right"},[text(value)]));
                        } else if (header.type == "string") {
                            row.push(td([text(value)]));
                        } else if (header.type == "text") {
                            row.push(td(node("pre",{},[text(value)])));
                        }
                    }
                    res_tbl.appendChild(tr(row))
                }
                output.appendChild(res_tbl);
            }
        }

        await fetch(element('editor').dataset.prog,
            {method: "PUT",
             body: editor.getValue(),
            });
    } else {
        const message = await response.text();
        output.appendChild(node("pre",{},[text(message)]));
    }
}

function select_language() {
	let langs = ""
	let table = document.getElementById("from");
	let tr = table.lastElementChild.firstElementChild;
	while (tr != null) {
		var nameElem  = tr.firstElementChild.firstElementChild;
		var checkElem = tr.lastElementChild.firstElementChild;

		var name = nameElem.innerHTML;
		if (checkElem.checked) {
			langs = langs + " " + name;
		}
		tr = tr.nextElementSibling;
	}

	window.localStorage.setItem('gp-languages', langs);
}

function edit_lex(span,event) {
	if (span.classList.contains("selected-lexeme"))
		return;

	const lexical_id = span.dataset.fun;

	gfwordnet.selection = {langs_list: [], langs: {}}
	let table = document.getElementById("from");
	let tr = table.lastElementChild.firstElementChild;
	while (tr != null) {
		var nameElem  = tr.firstElementChild.firstElementChild;
		var checkElem = tr.lastElementChild.firstElementChild;

		var name = nameElem.innerHTML;
		if (checkElem.checked) {
			gfwordnet.selection.langs[checkElem.name] = {
				name:  name,
				index: gfwordnet.selection.langs_list.length+1
			}
			gfwordnet.selection.langs_list.push(checkElem.name);
		}
		if (nameElem.tagName == "B") {
			gfwordnet.selection.current = checkElem.name;
		}
		tr = tr.nextElementSibling;
	}

	const result = node("table",{class:"result"},[
                     node("thead",{},[]),
                     node("tbody",{},[])
                   ]);
    const popup = node("div",{},[result]);
    document.body.appendChild(popup);

    span.classList.add("selected-lexeme");

    document.body.addEventListener("click", function closeFn(event) {
		let hit = (event.target == span);
		if (!hit) {
			let e = event.target;
			while (e != null) {
				if (e.className == "result" || e.className == "editor") {
					hit = true;
					break;
				}
				e = e.parentElement;
			}
		}

		if (!hit) {
			popup.remove();
			span.classList.remove("selected-lexeme");
			document.body.removeEventListener("click",closeFn);
		}
	});

	const ctxt = {rows: gfwordnet.render_rows(result,gfwordnet.selection,true,[{lemma: lexical_id}])};
	const helper = function (senses) {
		gfwordnet.senses = senses; // save the result to be used for filtering
		gfwordnet.render_senses(ctxt,gfwordnet.selection,result,null,senses);
		setTimeout(function() {
			popup.style.position = "absolute";
			popup.style.top = span.offsetTop+span.offsetHeight-1;
			popup.style.left = span.offsetLeft;

			const offsetRight = span.offsetLeft + popup.offsetWidth;
			if (offsetRight > document.body.offsetWidth) {
				popup.style.left = span.offsetLeft - (offsetRight - document.body.offsetWidth);
			}
		})
	}
	gfwordnet.sense_call("lexical_ids="+encodeURIComponent(lexical_id),helper);
}


function logOut() {
	gfwordnet.set_user(null,null,null,0,element('result'),null);
	logIn.innerHTML = "Log In";
	logIn.href = "https://github.com/login/oauth/authorize?scope=user:email%20public_repo&client_id=3b54eb78b27f94e182d0";
	commit.style.display = "none";
	deleteCookie("user");
	deleteCookie("author");
	deleteCookie("token");
}

super_update_cells_lin = gfwordnet.update_cells_lin
gfwordnet.update_cells_lin = function(lex_id,lang) {
	super_update_cells_lin(lex_id,lang);

	if (lang != gfwordnet.selection.current)
		return;

	// Part 4. Update the linearization of all sentences in the document
    const spans = document.querySelectorAll("span[data-fun="+lex_id+"]");
    for (const span of spans) {
        if (span.parentElement.tagName != "SPAN")
            continue;
        const sentence = span.parentElement;
        if (sentence.dataset.expr == null)
			continue;

		gfwordnet.grammar_call("command=bracketedLinearize&to="+lang+"&tree="+encodeURIComponent(sentence.dataset.expr), (lins) => {

			sentence.innerHTML = "";
			let bind_state = true;
			function taggedBrackets(brackets, fun) {
				for (let i in brackets) {
					if ("bind" in brackets[i])
						bind_state = brackets[i].bind;
					else {
						if (!bind_state) {
							sentence.appendChild(text(" "));
							bind_state = true;
						}

						if ("token" in brackets[i]) {
							if (fun != null) {
								const span = node("span", {},
								                  [text(brackets[i].token)]);
								span.dataset.fun = fun;
								span.dataset.lang = lang;
                                span.setAttribute("onclick", "edit_lex(this,event)");
								sentence.appendChild(span);
							} else {
								sentence.appendChild(text(brackets[i].token));
							}
							bind_state = false;
						} else {
							taggedBrackets(brackets[i].children, brackets[i].fun);
						}
					}
				}
			}

			for (const lin of lins) {
				taggedBrackets(lin.brackets, null);
			}
		});
    }
}
